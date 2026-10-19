#!/usr/bin/env python3
"""Owner-panel robot, phase 2: buttons that change the canonical master (video-prompts.md).

  in_film           «🎞 В фильме»   – scene is done and already in the film: ledger + remove from master
  scene_not_needed  «✕ Не нужна»    – remove the scene from master (no ledger verdict)
  tv_drop_task      «Не ждать»      – stop waiting for a Topview task (slow list, task map, telemetry)
  accept/redo/to_montage – explicit review decision; atomically updates ledger and slow after terminal

Scene IDs are reserved forever. Everything ambiguous → Supabase `needs_owner`, nothing touched:
active Topview task on the scene, contradicting buttons, an open owner_task on the scene,
missing ledger row, unrecognised master format, validator not green.

Safety order (commit-before-ack):
  plan → (on) claim rows `in_progress` → edit files → validate (project-status health=ok,
  review-ledger) → commit → push to main → read-back verification → ONLY THEN `applied`.
A rejected push means another writer: everything is re-read and redone from scratch.

Switch: GitHub variable ROBOT_MASTER_ACTIONS=on. Anything else = "plan without writing":
the plan is printed as a workflow annotation, nothing in Supabase or git is changed.

usage: robot_master_actions.py [--root DIR] [--no-sync]
env:   SUPABASE_SERVICE_ROLE_KEY (secret), ROBOT_MASTER_ACTIONS (variable)
Never prints keys or free-text owner notes.
"""
import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import master_scene_edit as mse          # noqa: E402
import master_slow_edit as slow_edit     # noqa: E402
import process_owner_decisions as pod    # noqa: E402

CLAIM = pod.CLAIM
RETIRE = ("in_film", "scene_not_needed")
REVIEW = ("accept", "redo", "to_montage")
TASK_RE = re.compile(r"^[0-9a-f]{32}$")
FILES = ("video-prompts.md", "review-ledger.json", "topview-task-map.json", "topview-status.json",
         "topview-checkpoint.json", "topview-operation-journal.json")
MAX_ATTEMPTS = 4


# --------------------------------------------------------------------------- helpers
def utcnow(now=None):
    return (now or datetime.now(timezone.utc)).isoformat(timespec="seconds").replace("+00:00", "Z")


def moscow_date(now=None):
    return ((now or datetime.now(timezone.utc)) + timedelta(hours=3)).strftime("%d.%m.%Y")


def read_raw(path):
    """UTF-8 text without newline translation (Path.read_text(newline=) needs Python 3.13)."""
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def master_mode(env=None):
    return "on" if str((env or os.environ).get("ROBOT_MASTER_ACTIONS", "")).strip().lower() == "on" else "off"


def is_mine(row):
    """Pending master-action rows plus rows this robot claimed earlier (retry after an interrupted run)."""
    return (row.get("action") in pod.MASTER_ACTIONS and
            (row.get("status") == "pending" or
             (row.get("status") == "in_progress" and str(row.get("result_note") or "").startswith(CLAIM))))


@dataclass
class Group:
    kind: str                 # 'retire' | 'drop' | 'review'
    scene: int
    actions: list
    rows: list
    task_id: str = None
    verdict: str = "needs_owner"   # apply | needs_owner | defer | noop
    reason: str = ""
    also: list = field(default_factory=list)   # other open rows that become needs_owner together
    report: dict = field(default_factory=dict)

    def brief(self):
        what = "+".join(sorted(set(self.actions)))
        tail = f" task {self.task_id[:8]}…" if self.task_id else ""
        return f"{what} сцена {self.scene}{tail}: {self.verdict}" + (f" ({self.reason})" if self.reason else "")


# --------------------------------------------------------------------------- state
def load_state(root):
    root = Path(root)
    st = {name: read_raw(root / name) for name in FILES}
    for name in FILES[1:]:
        st[name] = json.loads(st[name])
    ps = root / "project-status.json"
    st["project-status.json"] = json.loads(ps.read_text(encoding="utf-8-sig")) if ps.exists() else {}
    return st


def serialise(name, value):
    return value if isinstance(value, str) else dumps(value)


# --------------------------------------------------------------------------- telemetry edits
def ledger_in_film(row, stamp):
    row = dict(row)
    row.update(reviewed=True, reviewed_at=row.get("reviewed_at") if row.get("reviewed") and row.get("reviewed_at") else stamp,
               accepted=True, needs_redo=False, inserted_into_film=True, montage_note="в фильме",
               last_human_update_at=stamp)
    return row


def drop_task_telemetry(st, scene, task_id, stamp):
    """Owner pressed «Не ждать». Release ONLY editorial slow, NOT a physical Topview slot.

    Retain the actual active task in map/snapshot/checkpoint until Topview confirms
    it is terminal. A completed task remains processed with its real terminal status.
    Owner releases are tracked independently to prevent re-adding canonical slow.
    """
    tm = st["topview-task-map.json"]
    journal = st["topview-operation-journal.json"]
    owner_released = tm.setdefault("owner_released_task_ids", [])
    if task_id not in owner_released:
        owner_released.append(task_id)
    tm["updated_at"] = stamp  # Does NOT advance the Topview scan timestamp.
    journal["events"].append({
        "timestamp": stamp, "operation": "robot_owner_drop_task",
        "scene_id": scene, "task_fingerprint": task_id[:8],
        "previous_status": "owner_waiting", "new_status": slow_edit.ABANDONED,
        "source_checkpoint": st["topview-checkpoint.json"].get("checked_at"),
        "outcome": "owner_stopped_waiting_physical_topview_task_unchanged",
        "verification": "explicit owner panel decision; physical slot counts and provider task status unchanged"
    })
    journal["events"] = journal["events"][-journal.get("retention_max_events", 500):]


# --------------------------------------------------------------------------- planning
def _task_location(tm, task_id):
    for sid, ids in tm.get("active_by_scene", {}).items():
        if task_id in ids:
            return ("active", int(sid))
    for p in tm.get("processed_tasks", []):
        if p.get("task_id") == task_id:
            return ("processed", p.get("scene_id"))
    return (None, None)


def _scene_has_physical_active_task(st, scene):
    sid = str(scene)
    if st["topview-task-map.json"].get("active_by_scene", {}).get(sid):
        return True
    return any(str(t.get("scene_id")) == sid for t in st["topview-status.json"].get("active_tasks", []))


def _scene_has_confirmed_terminal(st, scene):
    sid = str(scene)
    terminal = ("success", "fail", "failed", "cancelled", "canceled")
    return (any(str(t.get("scene_id")) == sid and
                str(t.get("final_status", "")).lower() in terminal
                for t in st["topview-task-map.json"].get("processed_tasks", []))
            or str(st["topview-status.json"].get("scenes", {}).get(sid, {}).get("topview_status", "")).lower()
               in terminal)


def _scene_has_active_task(st, scene):
    sid = str(scene)
    if st["topview-task-map.json"].get("active_by_scene", {}).get(sid):
        return True
    if any(t.get("scene_id") == scene for t in st["topview-status.json"].get("active_tasks", [])):
        return True
    return scene in (st["project-status.json"].get("slow_scenes") or [])


def evaluate(rows, st, *, now=None):
    """Pure planning + editing. Returns (groups, files) where files = {name: new text} only for
    files that really change when every 'apply' group is applied. No I/O."""
    stamp, today = utcnow(now), moscow_date(now)
    st = copy.deepcopy(st)
    original = {n: serialise(n, st[n]) for n in FILES}
    mine = [r for r in rows if is_mine(r)]
    mine_ids = {r["id"] for r in mine}
    others = [r for r in rows if r["id"] not in mine_ids]

    def open_for_scene(scene):
        return [r for r in others if str(r.get("scene_id")) == str(scene)]

    groups = []
    # ---- tv_drop_task: one group per (scene, task)
    drops = {}
    for r in mine:
        if r["action"] == "tv_drop_task":
            drops.setdefault((str(r.get("scene_id")), str(r.get("task_id") or "")), []).append(r)
    for (sid, tid), rs in sorted(drops.items()):
        try:
            scene = int(sid)
        except ValueError:
            groups.append(Group("drop", -1, ["tv_drop_task"], rs, tid, reason="Scene ID не указан"))
            continue
        g = Group("drop", scene, ["tv_drop_task"], rs, tid)
        groups.append(g)
        if not TASK_RE.match(tid):
            g.reason = "ID задачи Topview не указан или некорректен"
            continue
        same_task = [r for r in others if str(r.get("task_id")) == tid and r.get("action") == "tv_mark_status"]
        if same_task:
            g.reason, g.also = "для этой задачи есть и «Не ждать», и «Готово/Брак»", same_task
            continue
        if any(r.get("action") == "owner_task" for r in open_for_scene(scene)):
            g.verdict, g.reason = "defer", "по сцене открыта текстовая задача владельца"
            continue
        where, owner_scene = _task_location(st["topview-task-map.json"], tid)
        if tid in st["topview-task-map.json"].get("owner_released_task_ids", []):
            g.verdict, g.reason = "noop", "ожидание уже снято решением владельца"
            continue
        if where not in ("active", "processed") or owner_scene != scene:
            g.reason = "задача не найдена среди активных задач этой сцены в карте Topview"
            continue
        model = next((t.get("model") for t in st["topview-status.json"].get("active_tasks", [])
                      if t.get("task_id") == tid), None) or "Topview"
        plan = {"occupied_slots": st["topview-status.json"].get("occupied_slots", 0),
                "finish": [{"scene": scene, "task_id": tid, "model": model, "final_status": slow_edit.ABANDONED,
                            "finished_utc": datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y %H:%M:%S UTC")}]}
        try:
            new_master, info = slow_edit.apply_plan(st["video-prompts.md"], plan, today)
        except (AssertionError, StopIteration, ValueError, KeyError, AttributeError) as e:
            g.reason = f"формат master не позволяет снять отметку (задача не найдена в таблице медленной генерации): {type(e).__name__}"
            continue
        try:
            trial = copy.deepcopy(st)
            drop_task_telemetry(trial, scene, tid, stamp)
        except (KeyError, TypeError, ValueError) as e:
            g.reason = f"телеметрия Topview не в ожидаемом формате: {type(e).__name__}"
            continue
        st.update({k: trial[k] for k in FILES[1:]})
        st["video-prompts.md"] = new_master
        g.verdict, g.report = "apply", {"slow_after": info["slow"], "occupied_after": st["topview-status.json"].get("occupied_slots", 0)}

    # ---- in_film / scene_not_needed: one group per scene
    scenes = {}
    for r in mine:
        if r["action"] in RETIRE:
            scenes.setdefault(str(r.get("scene_id")), []).append(r)
    review_scenes = {}
    for r in mine:
        if r["action"] in REVIEW:
            review_scenes.setdefault(str(r.get("scene_id")), []).append(r)
    review_consumed = set()
    for sid, rs in sorted(scenes.items(), key=lambda kv: kv[0].zfill(6)):
        review_here = review_scenes.get(sid, [])
        if review_here:
            review_consumed.add(sid)
            rs = rs + review_here
        actions = sorted({r["action"] for r in rs if r["action"] in RETIRE})
        try:
            scene = int(sid)
        except ValueError:
            groups.append(Group("retire", -1, actions, rs, reason="Scene ID не указан"))
            continue
        g = Group("retire", scene, actions, rs)
        groups.append(g)
        if len(actions) > 1:
            g.reason = "одновременно «В фильме» и «Не нужна»"
            continue
        mode = actions[0]
        review_actions = {r["action"] for r in rs if r["action"] in REVIEW}
        if review_actions and (mode != "in_film" or not review_actions.issubset({"accept", "to_montage"})):
            g.reason = "«В фильме»/«Не нужна» противоречит принятию/переделке"
            continue
        around = [r for r in open_for_scene(scene) if r.get("action") != "tv_drop_task"]
        if any(r.get("action") == "owner_task" for r in around):
            g.verdict, g.reason = "defer", "по сцене открыта текстовая задача владельца"
            continue
        clash = [r for r in around if pod.master_conflict({mode}, {pod.button_token(r)})]
        if clash:
            g.reason, g.also = "кнопки противоречат друг другу (нужно одно решение владельца)", clash
            continue
        if _scene_has_physical_active_task(st, scene):
            g.reason = "у сцены есть активная задача Topview — master не трогаю"
            continue
        canonical_slow = scene in st["project-status.json"].get("slow_scenes", [])
        if canonical_slow and not _scene_has_confirmed_terminal(st, scene):
            g.verdict, g.reason = "defer", "нет подтверждённого terminal Topview"
            continue
        ledger_row = st["review-ledger.json"].get("scenes", {}).get(sid)
        if mode == "in_film" and ledger_row is None:
            g.reason = "сцены нет в review-ledger.json"
            continue
        try:
            candidate_master = st["video-prompts.md"]
            if canonical_slow:
                candidate_master, _ = slow_edit.apply_plan(
                    candidate_master,
                    {"occupied_slots": st["topview-status.json"].get("occupied_slots", 0),
                     "release": [{"scene": scene, "action": "accept"}]}, today)
            new_master, rep = mse.retire_scene(candidate_master, scene, mode=mode, date=today)
        except mse.NeedsOwner as e:
            g.reason = str(e)
            continue
        except (AssertionError, StopIteration, ValueError, KeyError, AttributeError) as e:
            g.reason = "формат slow master не позволяет снять ожидание: " + type(e).__name__
            continue
        if mode == "in_film":
            st["review-ledger.json"]["scenes"][sid] = ledger_in_film(ledger_row, stamp)
            st["review-ledger.json"]["updated_at"] = stamp
        st["video-prompts.md"] = new_master
        if canonical_slow:
            st["project-status.json"]["slow_scenes"].remove(scene)
        g.report = rep
        if rep.get("already_retired") and mode == "scene_not_needed":
            g.verdict, g.reason = "noop", "сцена уже убрана из master (Scene ID зарезервирован)"
        else:
            g.verdict = "apply"

    # ---- Reviewed by explicit owner button: ledger and canonical slow are
    # committed atomically; physical Topview telemetry and Scene ID stay intact.
    for sid, rs in sorted(review_scenes.items(), key=lambda kv: kv[0].zfill(6)):
        if sid in review_consumed:
            continue
        acts = sorted({r["action"] for r in rs})
        try:
            scene = int(sid)
        except ValueError:
            groups.append(Group("review", -1, acts, rs, reason="Scene ID не указан"))
            continue
        g = Group("review", scene, acts, rs)
        groups.append(g)
        others_here = open_for_scene(scene)
        if any(r.get("action") == "owner_task" for r in others_here):
            g.verdict, g.reason = "defer", "по сцене открыта текстовая задача владельца"
            continue
        other_tokens = {pod.button_token(r) for r in others_here if r.get("action") != "tv_drop_task"}
        conflicts = [r for r in others_here if pod.master_conflict(set(acts), {pod.button_token(r)})]
        if (len(acts) > 1 and "redo" in acts) or conflicts:
            g.reason, g.also = "противоречивые решения владельца", conflicts
            continue
        if scene not in st["project-status.json"].get("scene_ids", []):
            g.reason = "сцена отсутствует в active master"
            continue
        old = st["review-ledger.json"].get("scenes", {}).get(sid)
        if old is None:
            g.reason = "нет сцены в review-ledger.json"
            continue
        if _scene_has_physical_active_task(st, scene):
            g.verdict, g.reason = "defer", "ещё есть активная задача Topview"
            continue
        if scene in st["project-status.json"].get("slow_scenes", []) and not _scene_has_confirmed_terminal(st, scene):
            g.verdict, g.reason = "defer", "нет подтверждённого terminal Topview"
            continue
        result = dict(old)
        try:
            for r in rs:
                result = pod.transform(result, r["action"], stamp)
        except ValueError as e:
            g.reason = str(e)
            continue
        if scene in st["project-status.json"].get("slow_scenes", []):
            try:
                action = "redo" if "redo" in acts else "to_montage" if "to_montage" in acts else "accept"
                new_master, info = slow_edit.apply_plan(
                    st["video-prompts.md"],
                    {"occupied_slots": st["topview-status.json"].get("occupied_slots", 0),
                     "release": [{"scene": scene, "action": action}]}, today)
            except (AssertionError, StopIteration, ValueError, KeyError, AttributeError) as e:
                g.reason = "формат slow master не позволяет снять ожидание: " + type(e).__name__
                continue
            st["video-prompts.md"] = new_master
            g.report = {"slow_after": info["slow"], "physical_slots_unchanged": True}
            st["project-status.json"]["slow_scenes"].remove(scene)
        st["review-ledger.json"]["scenes"][sid] = result
        st["review-ledger.json"]["updated_at"] = stamp
        g.verdict = "apply"

    files = {}
    for n in FILES:
        new = serialise(n, st[n])
        if new != original[n]:
            files[n] = new
    # a group that only changes nothing (e.g. already retired + ledger already set) is a no-op
    for g in groups:
        if g.verdict == "apply" and not files:
            g.verdict, g.reason = "noop", "изменений нет — уже применено"
    return groups, files


# --------------------------------------------------------------------------- git / validation
class Git:
    def __init__(self, root, branch="main"):
        self.root, self.branch = str(root), branch

    def run(self, *args, check=True):
        return subprocess.run(["git", *args], cwd=self.root, text=True, capture_output=True, check=check)

    def sync(self):
        self.run("fetch", "origin", self.branch)
        self.run("reset", "--hard", "FETCH_HEAD")

    def commit(self, message, paths):
        self.run("add", "--", *paths)
        if self.run("diff", "--cached", "--quiet", check=False).returncode == 0:
            return None
        self.run("-c", "user.name=github-actions[bot]",
                 "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                 "commit", "-q", "-m", message)
        return self.run("rev-parse", "HEAD").stdout.strip()

    def push(self):
        return self.run("push", "origin", f"HEAD:{self.branch}", check=False).returncode == 0

    def head_is_on_remote(self):
        self.run("fetch", "origin", self.branch)
        return self.run("merge-base", "--is-ancestor", "HEAD", "FETCH_HEAD", check=False).returncode == 0

    def reset(self):
        self.run("reset", "--hard", "HEAD")
        self.run("clean", "-fdq")


def build_status(root, master_path, out_path, synced_at):
    """Same validator invocation as sync-from-drive.yml. Returns (status|None, failed_checks)."""
    root = Path(root)
    out = Path(out_path)
    out.unlink(missing_ok=True)
    cmd = [sys.executable, str(root / "scripts" / "build_project_status.py"), str(master_path), "--output", str(out),
           "--synced-at", synced_at, "--topview-status-file", "topview-status.json",
           "--topview-task-map-file", "topview-task-map.json", "--previous-status-file", "project-status.json",
           "--previous-master-file", "video-prompts.md", "--revision-timezone", "Europe/Moscow"]
    p = subprocess.run(cmd, cwd=root, text=True, capture_output=True)
    if not out.is_file() or out.stat().st_size == 0:
        return None, ["validator produced no status: " + (p.stderr or p.stdout)[-200:]]
    status = json.loads(out.read_text(encoding="utf-8"))
    bad = [k for k, v in (status.get("checks") or {}).items() if not v]
    if p.returncode != 0 or status.get("health") != "ok":
        return status, bad or ["health != ok"]
    return status, []


def validate_ledger(root):
    p = subprocess.run([sys.executable, str(Path(root) / "scripts" / "validate_review_ledger.py"), str(root)],
                       text=True, capture_output=True)
    return p.returncode == 0, (p.stderr or p.stdout).strip()[-300:]


# --------------------------------------------------------------------------- store
class SupabaseStore:
    def list_open(self):
        return pod.api("GET", {"select": "id,created_at,scene_id,action,task_id,value,status,result_note",
                               "status": "in.(pending,in_progress)", "order": "created_at.asc",
                               "limit": str(pod.MAX_ROWS)})

    def mark(self, row, to_status, note):
        return pod.patch_status(row["id"], row["status"], to_status, note)


def _note(text):
    return CLAIM + " " + text


# --------------------------------------------------------------------------- main flow
def report_plan(groups, files, mode):
    lines = [g.brief() for g in groups]
    print(json.dumps({"mode": mode, "groups": len(groups), "files_that_would_change": sorted(files)}, ensure_ascii=False))
    for line in lines:
        print("  " + line)
    summary = "; ".join(lines[:12]) or "нет кнопок in_film / scene_not_needed / tv_drop_task"
    prefix = "Фаза 2 ВЫКЛЮЧЕНА (ROBOT_MASTER_ACTIONS не 'on') — план без записи: " if mode != "on" else "Фаза 2: "
    print("::notice title=robot-master-actions::" + prefix + summary)


def run(root, store, git, *, mode, now=None, sync=True):
    root = Path(root)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if sync:
            git.sync()
        rows = store.list_open()
        st = load_state(root)
        if mode != "on":
            # plan-only must never turn the 30-minute sync red because of an unexpected master/telemetry shape
            try:
                groups, files = evaluate(rows, st, now=now)
            except Exception as e:  # noqa: BLE001
                print(f"::warning title=robot-master-actions::plan failed ({type(e).__name__}); nothing was changed")
                return 0
            report_plan(groups, files, mode)
            return 0
        groups, files = evaluate(rows, st, now=now)
        applying = [g for g in groups if g.verdict == "apply"]
        # 1. everything ambiguous → owner, nothing else touched
        for g in groups:
            if g.verdict == "needs_owner":
                for r in g.rows + g.also:
                    if r.get("status") in ("pending", "in_progress"):
                        store.mark(r, "needs_owner", "Робот не тронул master: " + g.reason + ". Нужно решение владельца")
        # 1b. waiting buttons: show the reason on the site (owner 18.10), status stays pending
        for g in groups:
            if g.verdict == "defer":
                note = "Ждёт: " + g.reason + ". Применю автоматически, когда это изменится"
                for r in g.rows:
                    if r.get("status") == "pending" and r.get("result_note") != note:
                        store.mark(r, "pending", note)
        if not applying and not files:
            for g in groups:
                if g.verdict == "noop":
                    ok = (st["project-status.json"].get("health") == "ok")
                    if ok:
                        for r in g.rows:
                            store.mark(r, "applied", "Изменений не потребовалось: " + g.reason)
            report_plan(groups, files, mode)
            return 0
        # 2. claim; a lost claim (row cancelled/changed meanwhile) → plan again from scratch
        stale = False
        for g in applying:
            for r in g.rows:
                if r["status"] == "pending" and not store.mark(r, "in_progress",
                                                               _note("GitHub Actions принял решение, ожидается проверенный commit master")):
                    stale = True
        if stale:
            continue
        # 3. write files, validate, commit
        now_dt = now or datetime.now(timezone.utc)
        synced_at = now_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        tmp_master = root / ".robot-master.tmp"
        tmp_status = root / ".robot-status.tmp"
        try:
            for name, text in files.items():
                if name == "video-prompts.md":
                    tmp_master.write_text(text, encoding="utf-8", newline="")
                else:
                    (root / name).write_text(text, encoding="utf-8", newline="")
            master_for_check = tmp_master if "video-prompts.md" in files else root / "video-prompts.md"
            status, bad = build_status(root, master_for_check, tmp_status, synced_at)
            if bad:
                raise ValueError("валидатор master: " + ", ".join(bad)[:200])
            if "video-prompts.md" in files:
                (root / "video-prompts.md").write_text(files["video-prompts.md"], encoding="utf-8", newline="")
            (root / "project-status.json").write_text(tmp_status.read_text(encoding="utf-8"), encoding="utf-8")
            ok, msg = validate_ledger(root)
            if not ok:
                raise ValueError("review-ledger: " + msg)
        except ValueError as e:
            tmp_master.unlink(missing_ok=True)
            tmp_status.unlink(missing_ok=True)
            git.reset()
            for g in applying:
                for r in g.rows:
                    r = dict(r, status="in_progress")
                    store.mark(r, "needs_owner", "Автоправка не прошла проверку (" + str(e)[:200] + "); master не изменён")
            print("::warning title=robot-master-actions::validation failed; rows moved to needs_owner")
            return 0
        finally:
            tmp_master.unlink(missing_ok=True)
            tmp_status.unlink(missing_ok=True)
        master_sha = sha256(read_raw(root / "video-prompts.md"))
        summary = "; ".join(g.brief().split(":")[0] for g in applying)
        (root / "SYNC-TRIGGER.txt").write_text(
            f"{utcnow(now)} GitHub robot (owner panel): {summary}; SHA256 {master_sha}. "
            "Sync exact master -> validator -> project-status -> GitHub Pages.\n", encoding="utf-8")
        paths = sorted(set(files) | {"project-status.json", "SYNC-TRIGGER.txt"})
        commit = git.commit(f"Owner panel robot: {summary} (validator health=ok)", paths)
        if commit is None:
            print("nothing to commit after edit")
            return 0
        # 4. push; rejected = someone else wrote → redo from scratch
        if not git.push():
            print(f"push rejected ({attempt}/{MAX_ATTEMPTS}); re-reading main and starting over")
            git.reset()
            continue
        # 5. read-back verification, then — and only then — acknowledge
        problems = []
        if not git.head_is_on_remote():
            problems.append("commit не найден в origin/main после push")
        status, bad = build_status(root, root / "video-prompts.md", root / ".robot-verify.tmp", synced_at)
        (root / ".robot-verify.tmp").unlink(missing_ok=True)
        if bad or status.get("canonical_master_sha256") != master_sha:
            problems.append("project-status.health != ok после push: " + ", ".join(bad)[:150])
        if problems:
            print("::error title=robot-master-actions::" + "; ".join(problems))
            return 1                      # rows stay in_progress (claimed) → retried by the next run
        for g in applying:
            for r in g.rows:
                note = {"in_film": "Автоматически: сцена убрана из active master, Scene ID зарезервирован, журнал «в фильме»",
                        "scene_not_needed": "Автоматически: сцена убрана из active master, Scene ID зарезервирован",
                        "tv_drop_task": "Автоматически: ожидание задачи снято (abandoned_by_owner); саму задачу в Topview отмените вручную",
                        "accept": "Решение «Принять»: журнал обновлён, slow снят после terminal, физические слоты без изменений",
                        "redo": "Решение «Переделать»: журнал обновлён, старое slow снято; новый рендер не запускался",
                        "to_montage": "Решение «В монтаж»: журнал обновлён, slow снято, сцена остаётся в master"}[r["action"]]
                store.mark(dict(r, status="in_progress"), "applied",
                           f"{note}. Commit {commit[:7]}, project-status.health=ok, SHA {master_sha[:12]}")
        for g in groups:
            if g.verdict == "noop":
                for r in g.rows:
                    store.mark(r, "applied", "Изменений не потребовалось: " + g.reason)
        report_plan(groups, files, mode)
        return 0
    print("::error title=robot-master-actions::push rejected 4 times; rows stay claimed and are retried next run")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--no-sync", action="store_true")
    args = ap.parse_args()
    if not os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip():
        print("::notice::Master actions not configured: missing SUPABASE_SERVICE_ROLE_KEY")
        return 0
    # GITHUB_REF_NAME = branch the workflow runs on (main for the schedule; a test branch for a manual
    # dispatch from a branch, so a trial run can never write into main by accident).
    branch = os.environ.get("GITHUB_REF_NAME") or "main"
    return run(args.root, SupabaseStore(), Git(args.root, branch), mode=master_mode(), sync=not args.no_sync)


if __name__ == "__main__":
    sys.exit(main())
