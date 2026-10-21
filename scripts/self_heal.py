#!/usr/bin/env python3
"""Self-check and self-repair of the automation (owner request 19.10.2026: «если что-то зависло или долго
обновляется, пускай само ищет ошибки и исправляется»).

Runs every 30 minutes (.github/workflows/self-heal.yml). For each known way the automation gets stuck it does
the one safe, repeatable fix; when the fix did not help, it hands the problem to an AI agent as a task
(`to: any`) in ops/owner-tasks.json, with the diagnosis. ChatGPT reads that inbox every hour, Claude
schedules three times a day.

Fixes it may do (nothing else):
  * re-start the canon check (sync-from-drive.yml) or the Topview robot (topview-robot.yml) when their output is stale;
  * re-run the failed jobs of a failed robot run once;
  * rebuild GitHub Pages when the live site lags behind main;
  * mark an expired, never-released canon lock as free.
It never approves, deletes, reruns or launches Topview generations, never edits master or instructions.

State: ops/self-heal.json (written only when something changed). Shown on the site under the launch queue.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import canon_lock  # noqa: E402

STATE = "ops/self-heal.json"
INBOX = "ops/owner-tasks.json"
LOCK = "ops/canon-lock.json"

SYNC_STALE = timedelta(minutes=210)       # status heartbeat is 180 min; one missed check gets a 30 min grace
SCAN_STALE = timedelta(minutes=40)        # shadow/topview-robot-status.json: robot scan every ~10 minutes
TELEMETRY_STALE = timedelta(minutes=110)  # topview-status.json: heartbeat 50 min, site says «устарела» at 105
PAGES_LAG = timedelta(minutes=30)
LOCK_FORGOTTEN = timedelta(minutes=30)
ESCALATE_AFTER = timedelta(minutes=25)    # a fix gets one cycle to work before an agent is asked
RUN_FRESH = timedelta(hours=3)            # older failed runs are history, not a current problem
LOG_KEEP = 20

WATCHED_RUNS = {
    "sync-from-drive.yml": "проверка канона и кнопок",
    "topview-robot.yml": "робот Topview",
    "validate-site.yml": "проверка сайта",
    "canon-health.yml": "здоровье канона",
}


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(v):
    return canon_lock.parse(v)


def age(now, v):
    t = parse(v)
    return (now - t) if t else None


def mins(td):
    return f"{int(td.total_seconds() // 60)} мин" if td is not None else "неизвестно сколько"


# --------------------------------------------------------------------------- detection (pure)
def detect(f, now):
    """f = facts gathered by the runner. Returns {key: problem} with problem = {text, fix, fix_text}.
    fix is an action dict or None (nothing safe to do, hand to an agent)."""
    out = {}

    def add(key, text, fix=None, fix_text=None):
        out[key] = {"text": text, "fix": fix, "fix_text": fix_text}

    ps = f.get("project_status") or {}
    a = age(now, ps.get("synced_at"))
    if a is None or a > SYNC_STALE:
        add("sync-stale", f"Статус проекта не обновлялся {mins(a)} (heartbeat — каждые 180 минут, порог ремонта — 210).",
            {"kind": "dispatch", "workflow": "sync-from-drive.yml"}, "перезапустил проверку канона")
    elif ps.get("health") != "ok":
        add("health-" + "-".join(sorted(ps.get("warnings") or ["unknown"]))[:60],
            f"Статус проекта: health = {ps.get('health')}, предупреждения: {', '.join(ps.get('warnings') or []) or 'нет'}.",
            {"kind": "dispatch", "workflow": "sync-from-drive.yml"}, "перезапустил проверку канона (она же чинит сертификат)")

    a = age(now, f.get("scan_checked_at"))
    if a is None or a > SCAN_STALE:
        add("scan-stale", f"Робот Topview не сканировал {mins(a)} (норма — каждые 10 минут).",
            {"kind": "dispatch", "workflow": "topview-robot.yml"}, "перезапустил робота Topview")
    else:
        t = age(now, f.get("telemetry_checked_at"))
        if t is None or t > TELEMETRY_STALE:
            hold = f.get("robot_last_decision") or ""
            add("telemetry-stale", f"Робот сканирует, но статус Topview на сайте не обновлялся {mins(t)}. "
                f"Последнее решение робота: «{hold or 'нет данных'}». Обычно это пауза робота (hold): "
                "задача без сцены, неполный скан или сбой проверки публикации.",
                {"kind": "dispatch", "workflow": "topview-robot.yml", "inputs": {"mode": "full"}},
                "запустил полный скан Topview")

    for wf, name in WATCHED_RUNS.items():
        r = (f.get("runs") or {}).get(wf)
        if not r or r.get("status") != "completed" or r.get("conclusion") != "failure":
            continue
        ra = age(now, r.get("updated_at") or r.get("created_at"))
        if ra is None or ra > RUN_FRESH:
            continue
        key = f"run-failed-{wf.split('.')[0]}"
        text = f"Последний запуск «{name}» на GitHub упал (попытка {r.get('run_attempt', 1)}): {r.get('html_url', '')}"
        if int(r.get("run_attempt") or 1) < 2:
            add(key, text, {"kind": "rerun", "run_id": r["id"]}, f"повторил упавший запуск «{name}»")
        else:
            add(key, text)

    pl, main_sync = f.get("pages_synced_at"), ps.get("synced_at")
    if pl and main_sync and f.get("pages_build_status") not in ("building", "queued"):
        lag = (parse(main_sync) - parse(pl)) if parse(main_sync) and parse(pl) else None
        if lag is not None and lag > PAGES_LAG:
            add("pages-lag", f"Сайт показывает статус от {pl}, а в main уже {main_sync} (отставание {mins(lag)}).",
                {"kind": "pages_build"}, "пересобрал сайт на GitHub Pages")

    lock = f.get("lock") or {}
    exp = parse(lock.get("expires_at"))
    if lock.get("state") == "held" and exp and now - exp > LOCK_FORGOTTEN:
        add("lock-forgotten", f"Замок канона ({lock.get('holder')}) истёк {exp:%d.%m %H:%M} UTC и не снят.",
            {"kind": "release_lock"}, "снял просроченный замок канона")
    return out


# --------------------------------------------------------------------------- planning (pure)
def plan(f, prev, inbox, now):
    """Returns (actions, state, inbox, changed). actions are executed by the runner AFTER the state is pushed."""
    found = detect(f, now)
    old = (prev or {}).get("problems") or {}
    log = list((prev or {}).get("log") or [])
    problems, actions = {}, []
    open_keys = {t.get("heal_key") for t in inbox.get("tasks", []) if t.get("status") in ("open", "taken")}

    for key, p in found.items():
        o = old.get(key) or {}
        st = {"text": p["text"], "since": o.get("since") or iso(now), "fixes": int(o.get("fixes") or 0),
              "last_fix_at": o.get("last_fix_at"), "escalated_at": o.get("escalated_at")}
        last_fix = parse(st["last_fix_at"])
        if p["fix"] and st["fixes"] == 0:
            actions.append(p["fix"])
            st["fixes"], st["last_fix_at"] = 1, iso(now)
            log.append({"at": iso(now), "kind": "fixed", "key": key, "text": f"Нашёл: {p['text']} Сделал: {p['fix_text']}."})
        elif not st["escalated_at"] and (not p["fix"] or (last_fix and now - last_fix >= ESCALATE_AFTER)):
            if key not in open_keys:
                tried = f" Робот уже {p['fix_text']} {st['last_fix_at']}, не помогло." if p["fix"] else ""
                inbox.setdefault("tasks", []).append({
                    "id": f"self-heal-{key}-{now:%Y%m%d%H%M}", "heal_key": key, "created_at": iso(now),
                    "scene_id": None, "to": "any", "source": "self-heal",
                    "text": f"Самопроверка: {p['text']}{tried} Найти причину и починить; правила — ops/SELF-HEAL.md.",
                    "status": "open", "taken_by": None, "taken_at": None})
            st["escalated_at"] = iso(now)
            log.append({"at": iso(now), "kind": "escalated", "key": key,
                        "text": f"Не чинится само: {p['text']} Передал агенту (задача в списке под очередью)."})
        problems[key] = st

    for key, o in old.items():
        if key not in found:
            log.append({"at": iso(now), "kind": "resolved", "key": key, "text": f"Прошло: {o.get('text', key)}"})

    state = {"schema_version": 1, "rules": "ops/SELF-HEAL.md",
             "status": "ok" if not problems else ("escalated" if any(p["escalated_at"] for p in problems.values()) else "fixing"),
             "problems": problems, "log": log[-LOG_KEEP:]}
    same = json.dumps({k: v for k, v in (prev or {}).items() if k != "changed_at"}, sort_keys=True, ensure_ascii=False) \
        == json.dumps(state, sort_keys=True, ensure_ascii=False)
    state["changed_at"] = (prev or {}).get("changed_at") if same else iso(now)
    return actions, state, inbox, not same


# --------------------------------------------------------------------------- runner (side effects)
def sh(*args, check=False):
    r = subprocess.run(list(args), text=True, capture_output=True)
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(args[:4])}: {r.stderr.strip()[:300]}")
    return r


def gh_json(path):
    r = sh("gh", "api", "-H", "Accept: application/vnd.github+json", path)
    if r.returncode or not r.stdout.strip():
        print(f"::warning::self-heal could not read {path}: {(r.stderr or '').strip()[:200]}")
        return None
    return json.loads(r.stdout)


def read_json(root, rel, default=None):
    try:
        return json.loads((Path(root) / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def gather(root):
    repo = os.environ.get("GITHUB_REPOSITORY", "virudik/ai-film-prompts")
    f = {"project_status": read_json(root, "project-status.json", {}),
         "scan_checked_at": (read_json(root, "shadow/topview-robot-status.json", {}) or {}).get("checked_at"),
         "telemetry_checked_at": (read_json(root, "topview-status.json", {}) or {}).get("checked_at"),
         "lock": read_json(root, LOCK, {}), "runs": {}}
    r = sh("git", "-C", str(root), "log", "-1", "--format=%s", "--grep=^GitHub robot:")
    f["robot_last_decision"] = r.stdout.strip().removeprefix("GitHub robot: ")[:160]
    for wf in WATCHED_RUNS:
        d = gh_json(f"repos/{repo}/actions/workflows/{wf}/runs?branch=main&per_page=1")
        if d and d.get("workflow_runs"):
            w = d["workflow_runs"][0]
            f["runs"][wf] = {k: w.get(k) for k in ("id", "status", "conclusion", "run_attempt", "created_at", "updated_at", "html_url")}
    owner, name = repo.split("/")
    try:
        url = f"https://{owner}.github.io/{name}/project-status.json?selfheal={int(datetime.now().timestamp())}"
        with urllib.request.urlopen(url, timeout=20) as resp:
            f["pages_synced_at"] = json.loads(resp.read().decode("utf-8")).get("synced_at")
    except Exception as e:  # noqa: BLE001 - the live site being unreachable is itself only a signal
        print(f"::notice::live site not readable: {e}")
    b = gh_json(f"repos/{repo}/pages/builds/latest")
    f["pages_build_status"] = (b or {}).get("status")
    return f


def act(root, a):
    repo = os.environ.get("GITHUB_REPOSITORY", "virudik/ai-film-prompts")
    if a["kind"] == "dispatch":
        args = ["gh", "workflow", "run", a["workflow"], "--ref", "main"]
        for k, v in (a.get("inputs") or {}).items():
            args += ["-f", f"{k}={v}"]
        return sh(*args)
    if a["kind"] == "rerun":
        return sh("gh", "api", "-X", "POST", f"repos/{repo}/actions/runs/{a['run_id']}/rerun-failed-jobs")
    if a["kind"] == "pages_build":
        return sh("gh", "api", "-X", "POST", f"repos/{repo}/pages/builds")
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--dry", action="store_true", help="print the plan, change nothing")
    ap.add_argument("--facts", help="read facts from this JSON file instead of GitHub (tests, debugging)")
    a = ap.parse_args(argv)
    root = Path(a.root)
    for attempt in range(1, 5):
        if not a.dry and not a.facts:
            sh("git", "-C", str(root), "fetch", "-q", "origin", "main")
            sh("git", "-C", str(root), "reset", "-q", "--hard", "origin/main")
        now = datetime.now(timezone.utc)
        facts = json.loads(Path(a.facts).read_text(encoding="utf-8")) if a.facts else gather(root)
        prev = read_json(root, STATE, {}) or {}
        inbox = read_json(root, INBOX, {"schema_version": 1, "rules": "ops/OWNER-TASKS.md", "tasks": []})
        before_inbox = json.dumps(inbox, ensure_ascii=False, sort_keys=True)
        actions, state, inbox, changed = plan(facts, prev, inbox, now)
        lock_release = any(x["kind"] == "release_lock" for x in actions)
        print(json.dumps({"status": state["status"], "problems": list(state["problems"]), "actions": actions,
                          "seen_runs": sorted(facts.get("runs") or {}), "pages_synced_at": facts.get("pages_synced_at"),
                          "pages_build": facts.get("pages_build_status")}, ensure_ascii=False))
        if a.dry:
            return 0
        files = []
        if changed:
            (root / STATE).write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            files.append(STATE)
        if json.dumps(inbox, ensure_ascii=False, sort_keys=True) != before_inbox:
            inbox["updated_at"] = iso(now)
            (root / INBOX).write_text(json.dumps(inbox, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            files.append(INBOX)
        if lock_release:
            lock = read_json(root, LOCK, {})
            if not canon_lock.is_held(lock, now):     # only an already-expired lock
                rel = canon_lock.release(lock, lock.get("holder") or "self-heal", now)
                rel["task"] = (rel.get("task") or "") + " · снят самопроверкой (истёк)"
                (root / LOCK).write_text(json.dumps(rel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                files.append(LOCK)
        if files:
            sh("git", "-C", str(root), "add", *files, check=True)
            sh("git", "-C", str(root), "commit", "-q", "-m", f"Self-heal: {state['status']} ({', '.join(state['problems']) or 'всё в порядке'})", check=True)
            if sh("git", "-C", str(root), "push", "-q", "origin", "HEAD:main").returncode:
                print(f"push rejected ({attempt}/4); re-reading main")
                continue
        for x in actions:
            if x["kind"] == "release_lock":
                continue
            r = act(root, x)
            ok = r is not None and r.returncode == 0
            print(("done: " if ok else "::warning::failed: ") + json.dumps(x) + ("" if ok else " " + (r.stderr or "")[:300]))
        return 0
    print("::error::self-heal: push rejected 4 times")
    return 1


if __name__ == "__main__":
    sys.exit(main())
