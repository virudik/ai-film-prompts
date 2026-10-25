#!/usr/bin/env python3
"""GitHub robot: publish REAL Topview telemetry (the work of the hourly AI monitor cycle) without an AI.

Owner decision 13.10.2026: routine monitoring moves to the robot so the project does not depend on
a Claude/ChatGPT schedule. Two modes (GitHub variable ROBOT_TELEMETRY; the workflow defaults to `on` since the owner
made the robot the primary writer on 13.10.2026, the CLI defaults to `shadow`):

  shadow  compute exactly what the robot WOULD publish and write only shadow/robot-cycle-preview.json
          (decision, reasons, would-be changes, a short event log). Nothing canonical is touched.
  on      publish: topview-task-map / operation journal / topview-status / review-ledger
          (result_received only) / topview-checkpoint (last), plus the minimal master edit for
          slow add/finish (master_slow_edit.apply_plan), validated by build_project_status
          (health=ok) before commit, committed in ONE push (CAS), read back, then recorded in
          automation-monitor-status.json (runner `robot`). Allowed only while monitor-role.json says
          primary == robot (scripts/monitor_role.py --me robot); otherwise it refuses to write.

What it never does: start/approve/rerun/delete anything, spend credits, create a Scene ID, clear
canonical slow (only the owner's button does), guess a task↔scene mapping (only an exact or
normalised prompt match against exactly one master scene is accepted), or publish a snapshot that
contradicts itself — in doubt it HOLDS, records an honest `degraded` cycle once and notifies.

usage: robot_telemetry.py [--root DIR] [--mode shadow|on] [--scan shadow/topview-robot-status.json]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import master_slow_edit as mse            # noqa: E402
import robot_master_actions as rma        # noqa: E402
import relay_wake                         # noqa: E402
import topview_prompt_match as pm         # noqa: E402
import queue_readiness                    # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
HEARTBEAT_MIN = 50            # refresh unchanged telemetry before the site's 120-minute "stale" mark
HOLD_REPEAT_MIN = 50          # repeat the same degraded record no more often than this
PREVIEW = "shadow/robot-cycle-preview.json"
MAX_EVENTS = 40
MAX_SCAN_AGE_MIN = 15
MAX_ATTEMPTS = 4
ACTIVE = {"init", "queued", "running", "processing"}
TERMINAL = {"success", "fail", "failed", "cancelled"}
# backendModelCode of the Topview video config (topview_get_generation_config, 13.10.2026)
MODEL_IDS = {"Wan 3.0": "qwen-wan3.0-video", "Wan 3.0 Prime": "qwen-wan3.0-video-prime",
             "Seedance 2.0": "seedance-2.0-style", "Seedance 2.0 Fast": "seedance-2.0-style-fast",
             "Seedance 2.0 Mini": "seedance-2.0-mini", "Seedance 2.5": "seedance-2.5"}
RUNNER = "robot"
PROJECTS_TELEMETRY = "projects/topview-projects.json"   # tasks of the other projects (owner decision 20.10.2026)


# --------------------------------------------------------------------------- helpers
def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def parse_ts(value):
    """Topview gives '2026-10-13 16:07:41' (UTC) or ISO; returns aware datetime or None."""
    if not value:
        return None
    s = str(value).strip().replace(" ", "T")
    if not s.endswith("Z") and "+" not in s[10:]:
        s += "Z"
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def iso_z(value):
    dt = parse_ts(value)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def utc_label(value):
    dt = parse_ts(value)
    return dt.astimezone(timezone.utc).strftime("%d.%m.%Y %H:%M:%S UTC") if dt else "время неизвестно"


def now_z(now):
    return now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def minutes_since(value, now):
    dt = parse_ts(value)
    return None if dt is None else (now - dt).total_seconds() / 60


def scene_title(master, sid):
    m = re.search(rf"^## Сцена {sid} — (.+)$", master, re.M)
    return m.group(1).strip() if m else f"Сцена {sid}"


def part_from_label(label):
    """Sub-scene code of a master prompt block label: '28 B2' -> 'B2', '27 · Seedance 2.0 часть 2' -> 'Seedance 2.0
    часть 2', '16' -> None (topview_prompt_match.label_for)."""
    m = re.match(r"^\d+\s*(?:·\s*)?(.*)$", str(label or "").strip())
    return (m.group(1).strip() or None) if m else None


def part_from_confidence(text):
    """Sub-scene code from a stored mapping_confidence: '… master block 28 B6 (robot)' -> 'B6'."""
    m = re.search(r"master block (\d+[^()]*?) \(robot\)", str(text or ""))
    return part_from_label(m.group(1)) if m else None


def part_heading(master, sid, part):
    """Title of the sub-scene heading '#### B6 · Танец 6 — …' inside scene `sid`, or None."""
    m = re.search(rf"^## Сцена {sid} — .*?$(.*?)(?=^## |\Z)", master, re.M | re.S)
    if not m or not part:
        return None
    h = re.search(rf"^#{{3,4}}\s+{re.escape(part)}\s*·\s*(.+)$", m.group(1), re.M)
    return h.group(1).strip() if h else None


def row_title(master, sid, part):
    """First cell of a slow-table row: the sub-scene code is part of it, so the owner sees WHICH part runs."""
    if not part:
        return f"{sid} — {scene_title(master, sid)}"
    sub = part_heading(master, sid, part)
    return f"{sid} · {part} · {sub}" if sub else f"{sid} · {part} — {scene_title(master, sid)}"


def table_rows(master):
    """Rows of the dedicated slow table keyed by task id → text of the row."""
    lines = master.split("\n")
    try:
        h = next(i for i, l in enumerate(lines) if l.startswith("## ⏳ Сейчас в медленной генерации"))
    except StopIteration:
        return {}
    i = next((k for k in range(h, min(h + 6, len(lines))) if lines[k].startswith("|---")), None)
    out = {}
    if i is None:
        return out
    for l in lines[i + 1:]:
        if not l.startswith("|"):
            break
        m = re.search(r"task `([0-9a-f]{32})`", l)
        if m:
            out[m.group(1)] = l
    return out


# --------------------------------------------------------------------------- planning (pure)
def plan_cycle(scan, root, now, *, resolver=None, project_resolver=None):
    """Decide what to do from one robot scan and the repository state. No side effects.

    returns dict(decision=noop|publish|hold, reasons, changes, cycle, master_plan, events, mapped_by_prompt,
                 projects)
    Tasks of the other projects (projects/projects.json, owner decision 20.10.2026) are recognised by an
    exact/normalised prompt match with exactly one active scene of exactly one project master
    (`project_resolver`), or because the previous cycle already recognised them (projects/topview-projects.json).
    They never touch the root master, its slow list or its status; they are published separately in
    projects/topview-projects.json and no longer make the robot HOLD.
    """
    root = Path(root)
    prj_prev = read_json(root / PROJECTS_TELEMETRY, {}) or {}
    prj_known = {t.get("task_id"): t for t in prj_prev.get("active", []) if t.get("task_id")}
    prj_recent = {t.get("task_id") for t in prj_prev.get("recent", []) if t.get("task_id")}
    foreign, foreign_finished = [], []

    def project_hit(task_id):
        k = prj_known.get(task_id)
        if k:
            return {"project": k.get("project"), "scene": k.get("scene_id"), "label": k.get("label"),
                    "confidence": k.get("confidence") or "known from the previous robot cycle"}
        return project_resolver(task_id) if project_resolver else None

    tm = read_json(root / "topview-task-map.json", {})
    ts = read_json(root / "topview-status.json", {})
    ps = read_json(root / "project-status.json", {})
    master = (root / "video-prompts.md").read_text(encoding="utf-8")
    scene_ids = set(ps.get("scene_ids") or [])
    reasons, events = [], []

    sc = scan.get("scan") or {}
    if sc.get("detail_failed"):
        reasons.append("detail_failed:" + ",".join(t[:8] for t in sc["detail_failed"][:5]))
    if scan.get("missing_known_active"):
        reasons.append("task_vanished:" + ",".join(t[:8] for t in scan["missing_known_active"][:5]))
    if not scan.get("checked_at"):
        reasons.append("scan_has_no_time")

    prev_rows = {r.get("task_id"): r for r in ts.get("active_tasks", []) if r.get("task_id")}
    processed = {p.get("task_id") for p in tm.get("processed_tasks", [])}

    mapped, unmapped = [], []
    for a in scan.get("active_tasks", []):
        if not a.get("unlimited"):
            continue                       # slots count only active unlimited tasks (monitor rule)
        (mapped if a.get("scene_id") is not None else unmapped).append(dict(a))

    resolved = {}
    still = []
    for a in unmapped:
        hit = resolver(a["task_id"], master, scene_ids) if resolver else None
        if hit:
            a["scene_id"], a["mapping_confidence"] = hit["scene"], hit["confidence"]
            resolved[a["task_id"]] = hit
            mapped.append(a)
        else:
            ph = project_hit(a["task_id"])
            if ph:
                foreign.append({"project": ph["project"], "scene_id": int(ph["scene"]), "task_id": a["task_id"],
                                "model": a.get("model") or (prj_known.get(a["task_id"]) or {}).get("model"),
                                "status": a["status"], "started_at": iso_z(a.get("created_at"))
                                or (prj_known.get(a["task_id"]) or {}).get("started_at"),
                                "queue_count": a.get("queue_count"), "wait_seconds": a.get("wait_seconds"),
                                "label": ph.get("label"), "part": part_from_label(ph.get("label")),
                                "confidence": ph.get("confidence")})
            else:
                still.append(a)
    if still:
        reasons.append("unmapped_active:" + ",".join(a["task_id"][:8] for a in still))
        for a in still:
            events.append({"kind": "unmapped", "key": "unmapped:" + a["task_id"], "task_id": a["task_id"],
                           "title": "Новая задача Topview без сцены",
                           "text": f"Задача `{a['task_id']}` ({a.get('model') or 'модель неизвестна'}, {a.get('status')}) "
                                   "занимает слот, но не совпала точно ни с одним промтом активной сцены. Робот ничего не публикует "
                                   "и ничего не угадывает: нужен ответ владельца (какая это сцена) или агент."})

    known_parts = dict(ts.get("task_parts") or {})
    for a in mapped:
        if int(a["scene_id"]) not in scene_ids:
            reasons.append(f"scene_not_in_master:{a['scene_id']}")
        prow = prev_rows.get(a["task_id"], {})
        hit = resolved.get(a["task_id"]) or {}
        a["part"] = (part_from_label(hit.get("label")) or part_from_confidence(a.get("mapping_confidence"))
                     or prow.get("part") or part_from_confidence(prow.get("mapping_confidence"))
                     or known_parts.get(a["task_id"]))

    finished = []
    for f in scan.get("finished_known", []):
        if f.get("task_id") in processed:
            continue
        f = dict(f)  # resolving a first-seen terminal task must not mutate the scan
        if f.get("scene_id") is None:
            if f["task_id"] in prj_recent:
                continue                   # a task of another project, already recorded as finished
            hit = None if f["task_id"] in prj_known else (resolver(f["task_id"], master, scene_ids) if resolver else None)
            if not hit:
                ph = project_hit(f["task_id"])
                if ph:
                    k = prj_known.get(f["task_id"]) or {}
                    foreign_finished.append({"project": ph["project"], "scene_id": int(ph["scene"]),
                                             "task_id": f["task_id"], "model": k.get("model"),
                                             "final_status": f["final_status"],
                                             "finished_at": iso_z(f.get("completed_at")) or now_z(now),
                                             "started_at": k.get("started_at"), "label": ph.get("label"),
                                             "part": part_from_label(ph.get("label"))})
                    continue
                reasons.append("finished_without_scene:" + f["task_id"][:8])
                continue
            f["scene_id"] = hit["scene"]
            resolved[f["task_id"]] = hit
        if int(f["scene_id"]) not in scene_ids:
            reasons.append(f"scene_not_in_master:{f['scene_id']}")
            continue
        prow = prev_rows.get(f["task_id"], {})
        hit = resolved.get(f["task_id"]) or {}
        part = (part_from_label(hit.get("label")) or prow.get("part")
                or part_from_confidence(prow.get("mapping_confidence")) or known_parts.get(f["task_id"]))
        finished.append({"scene_id": int(f["scene_id"]), "task_id": f["task_id"], "final_status": f["final_status"],
                         "finished_at": iso_z(f.get("completed_at")) or now_z(now), **({"part": part} if part else {})})

    cur = {a["task_id"]: a for a in mapped}
    new_ids = sorted(set(cur) - set(prev_rows))
    gone_ids = sorted(set(prev_rows) - set(cur))
    fin_ids = {f["task_id"] for f in finished}
    vanished = [t for t in gone_ids if t not in fin_ids and t not in processed]
    if vanished:
        reasons.append("published_task_gone_without_result:" + ",".join(t[:8] for t in vanished[:5]))
    status_changed = sorted(t for t in set(cur) & set(prev_rows)
                            if str(prev_rows[t].get("topview_status", "")).lower() != cur[t]["status"])
    changes = {"new": new_ids, "gone": gone_ids, "finished": sorted(fin_ids), "status_changed": status_changed}

    fcur = {a["task_id"]: a for a in foreign}
    f_new = sorted(set(fcur) - set(prj_known))
    f_gone = sorted(set(prj_known) - set(fcur))
    f_fin = {f["task_id"] for f in foreign_finished}
    f_vanished = [t for t in f_gone if t not in f_fin]
    if f_vanished:
        reasons.append("project_task_gone_without_result:" + ",".join(t[:8] for t in f_vanished[:5]))
    f_status = sorted(t for t in set(fcur) & set(prj_known)
                      if str(prj_known[t].get("status", "")).lower() != str(fcur[t]["status"]).lower())
    changes["projects"] = {"new": f_new, "finished": sorted(f_fin), "status_changed": f_status}

    age = minutes_since(ts.get("checked_at"), now)
    unchanged = not (new_ids or gone_ids or fin_ids or status_changed or f_new or f_fin or f_status)

    rows = table_rows(master)
    plan = {"add": [], "finish": []}
    for tid in new_ids:
        a = cur[tid]
        if tid not in rows:
            plan["add"].append({"scene": int(a["scene_id"]), "task_id": tid, "model": a.get("model") or "модель неизвестна",
                                "status": a["status"], "row_title": row_title(master, a["scene_id"], a.get("part"))})
    for f in finished:
        row = rows.get(f["task_id"])
        if row and mse.LABEL in row and "Технический результат получен" not in row and "Ошибка Topview" not in row \
                and "Снята с учёта" not in row:
            model = (prev_rows.get(f["task_id"]) or {}).get("model") or "модель неизвестна"
            plan["finish"].append({"scene": f["scene_id"], "task_id": f["task_id"], "model": model,
                                   "final_status": "success" if f["final_status"] == "success" else f["final_status"],
                                   "finished_utc": utc_label(f["finished_at"])})
    # Repair: a master row still shows an active status although the task map already recorded the task as
    # terminal (a cycle published telemetry but its master edit was lost). Deterministic: model from the row,
    # status and time from the task map; the row stays canonical slow (only the owner's button clears it).
    planned = {x["task_id"] for x in plan["finish"]}
    proc_by_id = {p.get("task_id"): p for p in tm.get("processed_tasks", []) if p.get("task_id")}
    repairs = []
    for tid, row in rows.items():
        p = proc_by_id.get(tid)
        m = re.search(r"`(?:init|queued|running|processing)` · ([^|]+?) \|", row)
        if not p or tid in planned or tid in cur or not m or mse.LABEL not in row:
            continue
        fs = str(p.get("final_status") or "").lower()
        if fs not in TERMINAL and fs != mse.ABANDONED:
            continue
        repairs.append(tid)
        plan["finish"].append({"scene": int(p.get("scene_id") or re.match(r"^\|\s*(\d+)", row).group(1)), "task_id": tid,
                               "model": m.group(1).strip(), "final_status": fs,
                               "finished_utc": utc_label(p.get("finished_at") or p.get("completed_at"))})
    plan["occupied_slots"] = len(cur)      # physical Topview occupancy, not a count of master rows
    for f in finished:
        free = max(0, 6 - len(cur) - len(foreign))
        events.append({"kind": "result", "key": "result:" + f["task_id"], "task_id": f["task_id"],
                       "title": f"Сцена {f['scene_id']}: технический результат {f['final_status']}",
                       "text": f"Сцена {f['scene_id']}, задача `{f['task_id']}`: `{f['final_status']}`. "
                               f"Свободных слотов Topview: {free} из 6. Это не одобрение: сцена остаётся в ожидании кнопки владельца."})

    for f in foreign_finished:
        free = max(0, 6 - len(cur) - len(foreign))
        pname = f["project"]
        events.append({"kind": "result", "key": "result:" + f["task_id"], "task_id": f["task_id"],
                       "title": f"Проект {pname}, сцена {f['scene_id']}: технический результат {f['final_status']}",
                       "text": f"Проект `{pname}`, сцена {f['scene_id']}, задача `{f['task_id']}`: `{f['final_status']}`. "
                               f"Свободных слотов Topview (на все проекты): {free} из 6. Это не одобрение: решение — кнопкой владельца."})

    if reasons:
        decision = "hold"
    elif unchanged and not repairs and age is not None and age < HEARTBEAT_MIN:
        decision = "noop"
    else:
        decision = "publish"

    cycle = None
    if decision == "publish":
        mode = "full" if sc.get("mode") == "full" else "light"
        active = []
        for tid, a in sorted(cur.items()):
            prow = prev_rows.get(tid, {})
            model = a.get("model") or prow.get("model") or "модель неизвестна"
            active.append({"scene_id": int(a["scene_id"]), "task_id": tid, "model": model,
                           "model_id": MODEL_IDS.get(model) or prow.get("model_id"),
                           "status": a["status"], "started_at": iso_z(a.get("created_at")) or prow.get("started_at"),
                           "queue_count": a.get("queue_count"), "wait_seconds": a.get("wait_seconds"), "part": a.get("part"),
                           "mapping_confidence": a.get("mapping_confidence") or prow.get("mapping_confidence")
                           or "Topview task map (exact Scene mapping from the monitor's map)"})
        cycle = {"checked_at": scan["checked_at"], "active": active, "finished": finished, "scan_mode": mode,
                 "board_task_counts": sc.get("board_task_counts") or {},
                 "operation": "github_robot_cycle", "previous_status": f"{len(prev_rows)} активных задач",
                 "new_status": f"{len(active)} активных задач", "verification": "robot scan (public Topview API, GET only)",
                 "note": f"GitHub robot: {len(active)} из 6 слотов занято, новых {len(new_ids)}, завершено {len(fin_ids)}.",
                 "canonical": {"verified_at": ps.get("synced_at"), "master_sha256": ps.get("canonical_master_sha256"),
                               "health": ps.get("health")}}
        if mode == "full":     # light keeps the totals of the last full scan (monitor_publish contract)
            cycle.update(boards=sc.get("boards"), pages=sc.get("pages_scanned"), video_tasks=sc.get("tasks_seen"))
    if repairs:
        changes["repaired_rows"] = sorted(repairs)
    projects_out = None
    if decision == "publish":
        recent = [dict(f, recorded_at=now_z(now)) for f in foreign_finished] + \
            [r for r in prj_prev.get("recent", []) if r.get("task_id") not in f_fin]
        projects_out = {"schema_version": 1, "checked_at": scan["checked_at"], "updated_by": "GitHub robot (robot_telemetry.py)",
                        "rules": "projects/README.md",
                        "note": "Задачи Topview других проектов (не Серёгиуса). Слоты общие: занято на аккаунте = "
                                "topview-status.json.occupied_slots + число active здесь. Технический success ≠ одобрение.",
                        "active": sorted(foreign, key=lambda x: (x["project"], x["scene_id"], x["task_id"])),
                        "recent": recent[:100]}
    return {"decision": decision, "reasons": reasons, "changes": changes, "cycle": cycle, "master_plan": plan,
            "events": events, "resolved_by_prompt": resolved, "age_minutes": None if age is None else round(age, 1),
            "projects": projects_out}


# --------------------------------------------------------------------------- prompt resolver
def make_resolver(fetch_prompt):
    """Accept a mapping ONLY for an exact/normalised match with exactly one master scene that is active."""
    def resolve(task_id, master, scene_ids):
        prompt, _model = fetch_prompt(task_id)
        if not prompt:
            return None
        blocks = pm.master_blocks(master)
        label, level, _best, _runner = pm.classify(prompt, blocks)
        if level not in ("exact", "normalized"):
            return None
        norm = pm.normalise(prompt)
        scenes = set()
        for l, b in blocks:
            if b.replace("\r\n", "\n").strip() == prompt.replace("\r\n", "\n").strip() or pm.normalise(b) == norm:
                m = re.match(r"\d+", l)
                if m:
                    scenes.add(int(m.group(0)))
        if len(scenes) != 1:
            return None
        scene = next(iter(scenes))
        if scene not in scene_ids:
            return None
        return {"scene": scene, "confidence": f"prompt {level} match with master block {label} (robot)", "label": label}
    return resolve


def make_project_resolver(fetch_prompt, root):
    """Map a task to ANOTHER project (projects/<id>/video-prompts.md): exact/normalised prompt match with exactly
    one active scene of exactly one project master. Anything less is not a mapping (the robot then holds)."""
    import projects as prj

    def resolve(task_id):
        prompt, _model = fetch_prompt(task_id)
        if not prompt:
            return None
        norm = pm.normalise(prompt)
        exact = prompt.replace("\r\n", "\n").strip()
        found = set()
        best = {}
        for p in prj.projects(root):
            path = Path(root) / p["master"]
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            active = set(int(x) for x in re.findall(r"^## Сцена (\d+)\b", text, re.M))
            for label, body in pm.master_blocks(text):
                level = "exact" if body.replace("\r\n", "\n").strip() == exact else \
                    "normalized" if pm.normalise(body) == norm else None
                m = re.match(r"\d+", label)
                if level and m and int(m.group(0)) in active:
                    found.add((p["id"], int(m.group(0))))
                    best[(p["id"], int(m.group(0)))] = (label, level)
        if len(found) != 1:
            return None
        (pid, scene), = found
        label, level = best[(pid, scene)]
        return {"project": pid, "scene": scene, "label": label,
                "confidence": f"prompt {level} match with project {pid} master block {label} (robot)"}
    return resolve


# --------------------------------------------------------------------------- notifications
class GhNotifier:
    """Rolling GitHub issue `topview-events`; every event is one comment (= one e-mail to the owner)."""
    LABEL = "topview-events"
    TITLE = "Topview: события робота (результаты, слоты, сбои)"

    def post(self, title, text):
        env = dict(os.environ)
        q = subprocess.run(["gh", "api", "-X", "GET", "repos/{owner}/{repo}/issues", "-f", "state=open",
                            "-f", f"labels={self.LABEL}", "--jq", ".[0].number // empty"],
                           text=True, capture_output=True, env=env)
        number = q.stdout.strip()
        if not number:
            subprocess.run(["gh", "api", "repos/{owner}/{repo}/labels", "-f", f"name={self.LABEL}", "-f", "color=0e8a16"],
                           text=True, capture_output=True, env=env)
            c = subprocess.run(["gh", "api", "repos/{owner}/{repo}/issues", "-f", f"title={self.TITLE}",
                                "-f", "body=Лента событий GitHub-робота. Каждый комментарий — отдельное событие. "
                                       "Робот ничего не одобряет и не запускает.\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_",
                                "-f", f"labels[]={self.LABEL}", "--jq", ".number"], text=True, capture_output=True, env=env)
            number = c.stdout.strip()
        if not number:
            return False
        r = subprocess.run(["gh", "api", f"repos/{{owner}}/{{repo}}/issues/{number}/comments", "-f",
                            f"body=**{title}**\n\n{text}\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_"],
                           text=True, capture_output=True, env=env)
        return r.returncode == 0

    def wake(self, signal):
        """Wake: a NEW issue per slot event (audit record the executor verifies), then one Agent Relay DM.

        The DM to the subscribed ChatGPT inbox is what wakes the executor (owner decision 25.10.2026);
        older open wake issues are closed afterwards."""
        env = dict(os.environ)
        subprocess.run(["gh", "api", "repos/{owner}/{repo}/labels", "-f", f"name={WAKE_LABEL}", "-f", "color=d93f0b"],
                       text=True, capture_output=True, env=env)
        c = subprocess.run(["gh", "api", "repos/{owner}/{repo}/issues", "-f", f"title={wake_issue_title(signal)}",
                            "-f", f"body={wake_issue_body(signal)}", "-f", f"labels[]={WAKE_LABEL}",
                            "--jq", '.number, .html_url'], text=True, capture_output=True, env=env)
        out = c.stdout.split()
        if c.returncode != 0 or len(out) < 2:
            return False
        number, url = out[0], out[1]
        status, detail = relay_wake.send_dm(SCRIPTS.parent, wake_dm_text(signal, url),
                                            {"marker": WAKE_MARKER, "event_id": signal["event_id"],
                                             "issue_number": int(number), "issue_url": url,
                                             "observed_at": signal["observed_at"],
                                             "free_slots_global": signal["free_slots_global"]})
        print(f"::notice title=robot-wake::issue #{number}; relay {status} ({detail})")
        q = subprocess.run(["gh", "api", "-X", "GET", "repos/{owner}/{repo}/issues", "-f", "state=open",
                            "-f", f"labels={WAKE_LABEL}", "-f", "per_page=50", "--jq", ".[].number"],
                           text=True, capture_output=True, env=env)
        for old in q.stdout.split():
            if old != number:
                subprocess.run(["gh", "api", "-X", "PATCH", f"repos/{{owner}}/{{repo}}/issues/{old}", "-f", "state=closed",
                                "-f", "state_reason=completed"], text=True, capture_output=True, env=env)
        return True


class NullNotifier:
    def post(self, title, text):
        return True

    def wake(self, signal):
        return True


# --------------------------------------------------------------------------- shadow
def write_preview(root, scan, plan, now):
    path = Path(root) / PREVIEW
    old = read_json(path, {}) or {}
    events = list(old.get("events") or [])
    sig = (plan["decision"], tuple(plan["reasons"]), json.dumps(plan["changes"], sort_keys=True))
    last = events[-1] if events else None
    if plan["decision"] != "noop" and not (last and last.get("sig") == repr(sig)):
        events.append({"at": now_z(now), "decision": plan["decision"], "reasons": plan["reasons"],
                       "changes": plan["changes"], "master_plan": plan["master_plan"], "sig": repr(sig)})
    body = {"schema_version": 1, "mode": "shadow",
            "note": "ТЕНЕВОЙ режим: что робот ОПУБЛИКОВАЛ БЫ. Канон не затронут. События — только когда решение не 'noop'.",
            "generated_at": now_z(now), "scan_checked_at": scan.get("checked_at"),
            "decision": plan["decision"], "reasons": plan["reasons"], "changes": plan["changes"],
            "master_plan": plan["master_plan"], "published_age_minutes": plan["age_minutes"],
            "events": events[-MAX_EVENTS:]}
    cmp_old = {k: v for k, v in old.items() if k not in ("generated_at", "scan_checked_at", "published_age_minutes")}
    cmp_new = {k: v for k, v in body.items() if k not in ("generated_at", "scan_checked_at", "published_age_minutes")}
    if cmp_old == cmp_new:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


# --------------------------------------------------------------------------- publish ("on")
def role_allows(root):
    p = subprocess.run([sys.executable, str(SCRIPTS / "monitor_role.py"), str(root), "--me", RUNNER, "--dry-run"],
                       text=True, capture_output=True)
    try:
        info = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return False, "monitor_role.py gave no answer"
    return info.get("action") == "run", info.get("reason", "")


def record_cycle(root, started, completed, health, phases, missing, note, topview_checked):
    cmd = [sys.executable, str(SCRIPTS / "monitor_status.py"), str(root), "--started", started, "--completed", completed,
           "--runner", RUNNER, "--health", health, "--note", note]
    for p in phases:
        cmd += ["--phase", p]
    for m in missing:
        cmd += ["--missing", m]
    if topview_checked:
        cmd += ["--topview-checked", topview_checked]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


LEDGER_BLANK = {"result_received": False, "result_received_at": None, "reviewed": None, "reviewed_at": None,
                "accepted": None, "needs_redo": None, "inserted_into_film": None, "montage_note": None,
                "last_human_update_at": None}


def ensure_ledger_rows(root, scene_ids):
    """Add an EMPTY review-ledger row for every active scene that has none (a new scene was added to the master).

    Same blank row as scripts/reconcile_review_ledger.py: no human decision is ever inferred. 16.10.2026 the
    reconciler did not run after scenes 39–40 (the status rebuild was a bot push) and the ledger validator then
    refused every robot publish for 3 h. Returns the added scene ids."""
    path = Path(root) / "review-ledger.json"
    led = read_json(path, None)
    if not isinstance(led, dict) or not isinstance(led.get("scenes"), dict):
        return []
    added = [str(s) for s in sorted(int(x) for x in scene_ids) if str(s) not in led["scenes"]]
    if not added:
        return []
    for sid in added:
        led["scenes"][sid] = dict(LEDGER_BLANK)
    path.write_text(json.dumps(led, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added


def record_failure(root, git, scan, now, started, reason, notifier):
    """A publish that failed validation is a DEGRADED cycle, recorded once (like a hold) and announced once.

    Before 16.10.2026 such a failure only printed an error: the site kept showing old telemetry with no reason
    and nobody was told. Telemetry files are never written here, only automation-monitor-status.json."""
    note = ("publish failed: " + reason)[:200]
    status = read_json(Path(root) / "automation-monitor-status.json", {})
    last = status.get("last_scheduled_cycle") or {}
    if (last.get("runner") == f"{RUNNER}_scheduled_task" and last.get("health") == "degraded" and last.get("note") == note
            and (minutes_since(last.get("completed_at"), now) or 1e9) < HOLD_REPEAT_MIN):
        return
    key = "publish_failed:" + re.sub(r"[^0-9A-Za-z_:,\[\]' -]", "", reason)[:120]
    notified = set((status.get("notification_state") or {}).get("robot_notified_keys") or [])
    try:
        record_cycle(root, started, now_z(now), "degraded", ["topview_scan"], ["telemetry_publish"], note, scan.get("checked_at"))
        if key not in notified:
            mark_notified(root, [key])
        if git.commit("GitHub robot: publish failed — " + reason[:70], ["automation-monitor-status.json"]) is None or not git.push():
            git.reset()
            return
    except (subprocess.CalledProcessError, OSError):
        git.reset()
        return
    if key not in notified:
        notifier.post("Робот Topview: публикация не прошла проверку",
                      f"Причина: `{reason[:300]}`. Телеметрия на сайте не обновляется, пока причина не устранена; "
                      "робот повторяет попытку каждые 10 минут. Ничего не запускалось и не одобрялось.")


def mark_notified(root, keys):
    path = Path(root) / "automation-monitor-status.json"
    d = read_json(path, {})
    ns = d.setdefault("notification_state", {})
    seen = list(ns.get("robot_notified_keys") or [])
    for k in keys:
        if k not in seen:
            seen.append(k)
    ns["robot_notified_keys"] = seen[-300:]
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


WAKE_LABEL = "topview-slot-wake"
WAKE_MARKER = "TOPVIEW_SLOT_WAKE_V2"


def slot_wake_signal(event, plan):
    """Only verified published results may wake the executor; the handler rescans before any launch.

    Returns None unless the cycle is a publish, the event is a finished result and the account (all projects)
    has fewer than 6 active tasks."""
    if plan["decision"] != "publish" or event["kind"] != "result":
        return None
    occupied = len(plan["cycle"]["active"]) + len((plan.get("projects") or {}).get("active", []))
    free = max(0, 6 - occupied)
    if not free:
        return None
    return {"event_id": event["key"], "observed_at": plan["cycle"]["checked_at"], "free_slots_global": free}


def wake_issue_title(signal):
    # The ChatGPT Gmail trigger matches the mail subject "[virudik/ai-film-prompts] TOPVIEW_SLOT_WAKE_V2 ..."
    return f"{WAKE_MARKER} · свободно {signal['free_slots_global']} · {signal['event_id']}"


def wake_issue_body(signal):
    return (f"Робот подтвердил свободный слот Topview; исполнитель будится через Agent Relay и проверяет свежую очередь.\n\n"
            f"{WAKE_MARKER}\nevent_id: {signal['event_id']}\nobserved_at: {signal['observed_at']}\n"
            f"free_slots_global: {signal['free_slots_global']}\n\n"
            "Сигнал не является разрешением на оплату или одобрением качества. Порядок — ops/TOPVIEW-EVENT-WAKE.md."
            "\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_")


def wake_candidates(root, plan):
    """Result events that have never woken the executor. Kept apart from robot_notified_keys: a hold cycle
    announces the result (and marks it notified) but publishes nothing, so the wake must wait for the publish."""
    ns = (read_json(Path(root) / "automation-monitor-status.json", {}) or {}).get("notification_state") or {}
    sent = set(ns.get("robot_wake_keys") or [])
    return [e for e in plan["events"] if e["kind"] == "result" and e["key"] not in sent]


def mark_woken(root, keys):
    path = Path(root) / "automation-monitor-status.json"
    d = read_json(path, {})
    ns = d.setdefault("notification_state", {})
    seen = list(ns.get("robot_wake_keys") or [])
    seen += [k for k in keys if k not in seen]
    ns["robot_wake_keys"] = seen[-300:]
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def wake_dm_text(signal, issue_url):
    """Agent Relay DM: plain data for the executor, verified against the issue and fresh main."""
    return (f"{WAKE_MARKER}\nevent_id: {signal['event_id']}\nissue: {issue_url}\n"
            f"observed_at: {signal['observed_at']}\nfree_slots_global: {signal['free_slots_global']}\n"
            "repo: virudik/ai-film-prompts (main). Это сигнал пробуждения, не разрешение: свежий main, полный скан, "
            "замок и claim по ops/TOPVIEW-EVENT-WAKE.md.")


def published_event_text(event, plan):
    """Legacy V1 wake text in the rolling issue #18 (kept while the ChatGPT trigger moves to V2)."""
    text = event["text"]
    sig = slot_wake_signal(event, plan)
    if not sig:
        return text
    return text + (f"\n\n@virudik — подтверждён свободный слот; проверить свежую очередь.\n"
                   f"TOPVIEW_SLOT_WAKE_V1\nevent_id: {sig['event_id']}\n"
                   f"observed_at: {sig['observed_at']}\nfree_slots_global: {sig['free_slots_global']}\n"
                   "Сигнал не является разрешением на оплату или одобрением качества.")


def run_on(root, scan, git, *, now, resolver, notifier, project_resolver=None):
    root = Path(root)
    started = now_z(now)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        git.sync()
        ok, why = role_allows(root)
        if not ok:
            print(f"::notice title=robot-telemetry::not the writer ({why}); nothing written")
            return 0
        plan = plan_cycle(scan, root, now, resolver=resolver, project_resolver=project_resolver)
        d = plan["decision"]
        status = read_json(root / "automation-monitor-status.json", {})
        notified = set((status.get("notification_state") or {}).get("robot_notified_keys") or [])
        fresh = [e for e in plan["events"] if e["key"] not in notified]

        if d == "noop":
            print("::notice title=robot-telemetry::nothing changed; telemetry is fresh")
            return 0

        if d == "hold":
            last = status.get("last_scheduled_cycle") or {}
            same = (last.get("runner") == f"{RUNNER}_scheduled_task" and last.get("health") == "degraded"
                    and last.get("note") == "hold: " + "; ".join(plan["reasons"])[:200]
                    and (minutes_since(last.get("completed_at"), now) or 1e9) < HOLD_REPEAT_MIN)
            if not same:
                record_cycle(root, started, now_z(now), "degraded", ["topview_scan"], ["telemetry_publish"],
                             "hold: " + "; ".join(plan["reasons"])[:200], scan.get("checked_at"))
                mark_notified(root, [e["key"] for e in fresh])
                git.commit("GitHub robot: hold — " + "; ".join(plan["reasons"])[:80],
                           ["automation-monitor-status.json"])
                if not git.push():
                    git.reset()
                    continue
                for e in fresh:
                    notifier.post(e["title"], e["text"])
            print("::warning title=robot-telemetry::HOLD: " + "; ".join(plan["reasons"]))
            return 0

        # ---- publish
        cycle = plan["cycle"]
        cyc_path = root / ".robot-cycle.tmp"
        tmp_master, tmp_status = root / ".robot-master.tmp", root / ".robot-status.tmp"
        try:
            cyc_path.write_text(json.dumps(cycle, ensure_ascii=False), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPTS / "monitor_publish.py"), str(root), str(cyc_path)],
                           check=True, capture_output=True, text=True)
            mp = plan["master_plan"]
            master_text = rma.read_raw(root / "video-prompts.md")
            files = ["topview-task-map.json", "topview-operation-journal.json", "topview-status.json",
                     "topview-checkpoint.json", "review-ledger.json", "automation-monitor-status.json"]
            if plan.get("projects") is not None and (root / "projects").is_dir():
                (root / PROJECTS_TELEMETRY).write_text(json.dumps(plan["projects"], ensure_ascii=False, indent=2) + "\n",
                                                      encoding="utf-8")
                files.append(PROJECTS_TELEMETRY)
            new_master = None
            if mp["add"] or mp["finish"]:
                new_master, _info = mse.apply_plan(master_text, mp, rma.moscow_date(now))
                tmp_master.write_text(new_master, encoding="utf-8", newline="")
            synced = now_z(now)
            check_master = tmp_master if new_master is not None else root / "video-prompts.md"
            st, bad = rma.build_status(root, check_master, tmp_status, synced)
            if bad:
                raise ValueError("validator: " + ", ".join(bad)[:200])
            added = ensure_ledger_rows(root, st.get("scene_ids") or [])
            if added:
                print(f"::notice title=robot-telemetry::added empty review-ledger rows for new scenes {', '.join(added)}")
            ok, msg = rma.validate_ledger(root)
            if not ok:
                raise ValueError("review-ledger: " + msg)
            if new_master is not None:
                (root / "video-prompts.md").write_text(new_master, encoding="utf-8", newline="")
                files.append("video-prompts.md")
            (root / "project-status.json").write_text(tmp_status.read_text(encoding="utf-8"), encoding="utf-8")
            files.append("project-status.json")
            if queue_readiness.write(root):
                files.append("ops/queue-readiness.json")
            # the checkpoint records the validation that actually happened (publish wrote the old one)
            cp = read_json(root / "topview-checkpoint.json", {})
            cp["canonical_validation"] = {"verified_at": synced, "health": st.get("health"),
                                          "canonical_master_sha256": st.get("canonical_master_sha256"),
                                          "all_project_checks_true": st.get("health") == "ok"}
            (root / "topview-checkpoint.json").write_text(json.dumps(cp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            if new_master is not None:
                sha = rma.sha256(rma.read_raw(root / "video-prompts.md"))
                (root / "SYNC-TRIGGER.txt").write_text(
                    f"{rma.utcnow(now)} GitHub robot (Topview telemetry): slow add/finish; SHA256 {sha}. "
                    "Sync exact master -> validator -> project-status -> GitHub Pages.\n", encoding="utf-8")
                files.append("SYNC-TRIGGER.txt")
            record_cycle(root, started, now_z(now), "ok",
                         ["role_check", "topview_scan_api", "task_map_master_consistency", "telemetry_publish",
                          "project_status_health_ok", "checkpoint_last"], [], cycle["note"], scan.get("checked_at"))
            mark_notified(root, [e["key"] for e in fresh])
            wake_events = wake_candidates(root, plan)
            mark_woken(root, [e["key"] for e in wake_events])
        except (ValueError, subprocess.CalledProcessError, AssertionError, KeyError) as e:
            git.reset()
            print(f"::error title=robot-telemetry::publish validation failed ({type(e).__name__}: {str(e)[:160]}); telemetry not committed")
            record_failure(root, git, scan, now, started, f"{type(e).__name__}: {str(e)[:160]}", notifier)
            return 1
        finally:
            for t in (cyc_path, tmp_master, tmp_status):
                t.unlink(missing_ok=True)
        summary = f"{len(cycle['active'])}/6 slots, +{len(plan['changes']['new'])} new, {len(plan['changes']['finished'])} finished" + (
            f", {len(plan['changes']['repaired_rows'])} master rows repaired" if plan['changes'].get('repaired_rows') else "")
        commit = git.commit(f"GitHub robot: Topview telemetry — {summary}", sorted(set(files)))
        if commit is None:
            return 0
        if not git.push():
            print(f"push rejected ({attempt}/{MAX_ATTEMPTS}); re-reading main and starting over")
            git.reset()
            continue
        if not git.head_is_on_remote():
            print("::error title=robot-telemetry::commit not found on origin/main after push")
            return 1
        for e in fresh:
            notifier.post(e["title"], published_event_text(e, plan))
        wakes = [w for w in (slot_wake_signal(e, plan) for e in wake_events) if w]
        if wakes:                 # one new mail thread per cycle is enough: the handler fills every free slot
            notifier.wake(wakes[-1])
        print(f"::notice title=robot-telemetry::published {summary}; commit {commit[:7]}")
        return 0
    print("::error title=robot-telemetry::push rejected 4 times; will retry next run")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(SCRIPTS.parent))
    ap.add_argument("--mode", choices=("shadow", "on"), default=os.environ.get("ROBOT_TELEMETRY", "shadow") or "shadow")
    ap.add_argument("--scan", default="shadow/topview-robot-status.json")
    ap.add_argument("--commit", action="store_true",
                    help="allow git commit/push; implied inside GitHub Actions, otherwise files are only written locally")
    a = ap.parse_args()
    may_commit = a.commit or os.environ.get("GITHUB_ACTIONS") == "true"
    root = Path(a.root)
    scan = read_json(root / a.scan, None)
    if not scan:
        print("::notice title=robot-telemetry::no scan file; nothing done")
        return 0
    now = datetime.now(timezone.utc)
    age = minutes_since(scan.get("checked_at"), now)
    if age is None or age > MAX_SCAN_AGE_MIN or age < -5:
        # Never decide on an old scan (e.g. its commit was rejected): telemetry must describe NOW.
        print(f"::warning title=robot-telemetry::scan is {age} min old (limit {MAX_SCAN_AGE_MIN}); nothing done")
        return 0
    key, uid = os.environ.get("TOPVIEW_API_KEY", ""), os.environ.get("TOPVIEW_UID", "")
    resolver = project_resolver = None
    if key.strip() and uid.strip():
        import topview_api_scan as scan_mod
        client = scan_mod.Client(key, uid)
        cache = {}

        def fetch(tid):          # one GET per task even when both resolvers look at it
            if tid not in cache:
                cache[tid] = pm.fetch_prompt(client, tid)
            return cache[tid]
        resolver = make_resolver(fetch)
        project_resolver = make_project_resolver(fetch, root)
    git = rma.Git(root)
    if a.mode == "shadow":
        plan = plan_cycle(scan, root, now, resolver=resolver, project_resolver=project_resolver)
        changed = write_preview(root, scan, plan, now)
        print("::notice title=robot-telemetry-shadow::" + json.dumps(
            {"decision": plan["decision"], "reasons": plan["reasons"], "changes": plan["changes"],
             "master_plan": {k: len(v) if isinstance(v, list) else v for k, v in plan["master_plan"].items()}}, ensure_ascii=False))
        if changed and not may_commit:
            print("::notice title=robot-telemetry-shadow::preview written locally; commit/push only inside GitHub Actions")
        if changed and may_commit:
            git.commit("GitHub robot (shadow): telemetry preview", [PREVIEW])
            for _ in range(MAX_ATTEMPTS):
                if git.push():
                    break
                git.run("fetch", "origin", "main")
                git.run("rebase", "origin/main", check=False)
        return 0
    if not may_commit:
        print("::error title=robot-telemetry::mode=on writes and pushes; refused outside GitHub Actions (use --commit deliberately)")
        return 2
    notifier = GhNotifier() if os.environ.get("GH_TOKEN") else NullNotifier()
    return run_on(root, scan, git, now=now, resolver=resolver, notifier=notifier, project_resolver=project_resolver)


if __name__ == "__main__":
    sys.exit(main())

