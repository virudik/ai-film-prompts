#!/usr/bin/env python3
"""Primary/standby decision for one monitor cycle. Read-only.

usage: monitor_role.py <repo> --me claude|chatgpt
prints JSON {"action": "run"|"failover"|"skip", "reason": ...}; exit code 0 always.
"""
import argparse, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser(); ap.add_argument("repo"); ap.add_argument("--me", required=True, choices=["claude", "chatgpt"])
a = ap.parse_args(); repo = Path(a.repo)
role = json.loads((repo / "monitor-role.json").read_text(encoding="utf-8"))
mon = json.loads((repo / "automation-monitor-status.json").read_text(encoding="utf-8"))
now = datetime.now(timezone.utc)
other = "chatgpt" if a.me == "claude" else "claude"
author = role["monitors"][other]["commit_author"]


def minutes_since(iso):
    try:
        return (now - datetime.fromisoformat(str(iso).replace("Z", "+00:00"))).total_seconds() / 60
    except Exception:
        return float("inf")


# collision guard: recent commits by the other monitor
try:
    out = subprocess.run(["git", "log", "origin/main", f"--since={role['collision_guard_minutes']} minutes ago", f"--author={author}", "--format=%h %s"],
                         cwd=repo, capture_output=True, text=True).stdout.strip()
except Exception:
    out = ""
cycle = mon.get("last_scheduled_cycle") or {}
runner = cycle.get("runner", "chatgpt_scheduled_task" if "runner" not in cycle else "")
last_runner = "claude" if "claude" in str(runner) else "chatgpt"
age = minutes_since(cycle.get("completed_at"))
if out:
    res = {"action": "skip", "reason": f"other monitor ({other}) committed within {role['collision_guard_minutes']} min: {out.splitlines()[0]}"}
elif role["primary"] == a.me:
    res = {"action": "run", "reason": "primary"}
else:
    primary = role["primary"]
    if last_runner == primary and age <= role["failover_after_minutes"]:
        res = {"action": "skip", "reason": f"standby; primary {primary} last cycle {age:.0f} min ago"}
    elif last_runner == a.me and age <= role["failover_after_minutes"]:
        res = {"action": "failover", "reason": f"standby already covering for {primary}; continue (last own cycle {age:.0f} min ago)"}
    else:
        res = {"action": "failover", "reason": f"primary {primary} late: last recorded cycle by {last_runner} {age:.0f} min ago"}
print(json.dumps(res, ensure_ascii=False))
