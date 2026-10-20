#!/usr/bin/env python3
"""Canon writer lock: ops/canon-lock.json says who is editing the canon right now (owner decision 17.10.2026).

usage: canon_lock.py <repo> status [--project ID]
       canon_lock.py <repo> acquire --holder NAME --task TEXT [--minutes 45] [--project ID] [--push]
       canon_lock.py <repo> release --holder NAME [--project ID] [--push]

--project ID uses the lock of another project, projects/<id>/canon-lock.json (owner decision 20.10.2026,
projects/README.md): it covers edits inside projects/<id>/ only; everything else keeps the common lock.

The lock is advisory and never blocks a push by itself: git still rejects a stale push.
It tells the other writer (ChatGPT or a Claude thread) "I am working on the canon until T".
A missing file, state "free" or an expired lock all mean the canon is free.
The GitHub robot and the owner-panel robot write their own status files and never take the lock.
With --push the change is committed and pushed at once; a rejected push means someone else
wrote first: re-read and try again (never force).
"""
import argparse, json, re, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOCK = "ops/canon-lock.json"
DEFAULT_MINUTES = 45
MAX_MINUTES = 120


def now_utc():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


def parse(value):
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return dt if dt.tzinfo else None
    except (TypeError, ValueError):
        return None


def lock_path(project=None):
    """Common lock for the root project and shared files; projects/<id>/canon-lock.json for another project."""
    if project and project != "seregius":
        if not re.match(r"^[a-z0-9][a-z0-9-]{1,30}$", project):
            raise ValueError(f"bad project id {project!r}")
        return f"projects/{project}/canon-lock.json"
    return LOCK


def read(repo, project=None):
    p = Path(repo) / lock_path(project)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def is_held(lock, now):
    """Held = state 'held' and expires_at is in the future. Anything else is free."""
    if (lock or {}).get("state") != "held":
        return False
    exp = parse(lock.get("expires_at"))
    return bool(exp and exp > now)


def acquire(lock, holder, task, minutes, now):
    """Return the new lock dict, or raise RuntimeError if someone else holds it."""
    minutes = max(1, min(int(minutes), MAX_MINUTES))
    if is_held(lock, now) and lock.get("holder") != holder:
        raise RuntimeError(f"канон занят: {lock.get('holder')} до {lock.get('expires_at')} ({lock.get('task')})")
    same = is_held(lock, now) and lock.get("holder") == holder
    return {
        "schema_version": 1,
        "state": "held",
        "holder": holder,
        "task": task,
        "acquired_at": lock.get("acquired_at") if same else iso(now),
        "expires_at": iso(now + timedelta(minutes=minutes)),
        "released_at": None,
        "rules": "ops/CANON-LOCK.md",
    }


def release(lock, holder, now):
    if is_held(lock, now) and lock.get("holder") != holder:
        raise RuntimeError(f"замок держит {lock.get('holder')}, не {holder}")
    out = dict(lock or {})
    out.update(schema_version=1, state="free", released_at=iso(now), expires_at=None, rules="ops/CANON-LOCK.md")
    out.setdefault("holder", holder)
    out.setdefault("task", "")
    return out


def describe(lock, now):
    if not is_held(lock, now):
        return "free"
    return f"held by {lock.get('holder')} until {lock.get('expires_at')}: {lock.get('task')}"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)


def write_and_push(repo, lock, message, push, project=None):
    rel = lock_path(project)
    p = Path(repo) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not push:
        return True
    git(repo, "add", rel)
    c = git(repo, "commit", "-m", message)
    if c.returncode != 0:
        print(c.stdout + c.stderr, file=sys.stderr)
        return False
    r = git(repo, "push", "origin", "HEAD:main")
    if r.returncode != 0:
        print("push rejected: someone else wrote first; re-read and retry.\n" + r.stderr, file=sys.stderr)
        return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("action", choices=("status", "acquire", "release"))
    ap.add_argument("--holder")
    ap.add_argument("--task", default="")
    ap.add_argument("--minutes", type=int, default=DEFAULT_MINUTES)
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--project", help="another project's lock: projects/<id>/canon-lock.json")
    a = ap.parse_args(argv)
    now = now_utc()
    lock = read(a.repo, a.project)
    if a.action == "status":
        print(describe(lock, now))
        return 0
    if not a.holder:
        ap.error("--holder is required")
    try:
        if a.action == "acquire":
            new = acquire(lock, a.holder, a.task, a.minutes, now)
            msg = f"Canon lock: {a.holder} takes the canon until {new['expires_at']}"
        else:
            new = release(lock, a.holder, now)
            msg = f"Canon lock: {a.holder} frees the canon"
        if a.project and a.project != "seregius":
            new["project"] = a.project
            msg = msg.replace("Canon lock:", f"Project lock ({a.project}):")
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 2
    return 0 if write_and_push(a.repo, new, msg, a.push, a.project) else 1


if __name__ == "__main__":
    sys.exit(main())
