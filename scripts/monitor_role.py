#!/usr/bin/env python3
"""Decide one AI Film monitor cycle (one writer, sticky automatic takeover).

usage: python3 scripts/monitor_role.py <repo> --me claude|chatgpt [--dry-run]
prints {"action": "run"|"failover"|"skip", "reason": "...", "swapped": bool}
Uses monitor-role.json as live config. The set_at timestamp is the failover
grace baseline until a verified primary cycle has been recorded.

Owner decision 10.10.2026: whoever takes over becomes the primary. On
"failover" this script swaps primary/standby in monitor-role.json (unless
--dry-run); the caller MUST commit monitor-role.json together with its cycle
and tell the owner once: "основным монитором стал <me>". The old primary then
acts as standby and takes over back only if the new primary is silent > threshold.
"""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("repo")
parser.add_argument("--me", choices=("claude", "chatgpt"), required=True)
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

repo = Path(args.repo)
role = json.loads((repo / "monitor-role.json").read_text(encoding="utf-8"))
status = json.loads((repo / "automation-monitor-status.json").read_text(encoding="utf-8"))
now = datetime.now(timezone.utc)
primary = role["primary"]
standby = role["standby"]
other = "chatgpt" if args.me == "claude" else "claude"
guard = int(role["collision_guard_minutes"])
threshold = int(role["failover_after_minutes"])
standby_yield = int(role.get("standby_yield_minutes", 100))


def minutes_since(value):
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return float("inf")
        return (now - dt).total_seconds() / 60
    except (TypeError, ValueError, OverflowError):
        return float("inf")


def normalize_runner(value):
    value = str(value or "").lower()
    if "claude" in value:
        return "claude"
    if "chatgpt" in value:
        return "chatgpt"
    return None


cycle = status.get("last_scheduled_cycle") or {}
runner = normalize_runner(cycle.get("runner"))
# Older snapshots without a runner are not evidence of a Claude primary cycle.
if runner is None and cycle.get("completed_at"):
    runner = "chatgpt"
age_last_cycle = minutes_since(cycle.get("completed_at"))
per_runner = status.get("last_completed_by_runner") or {}
primary_at = per_runner.get(primary)
standby_at = per_runner.get(standby)
if runner == primary:
    primary_at = cycle.get("completed_at")
elif runner == standby:
    standby_at = cycle.get("completed_at")
# On a just-switched primary without a recorded cycle allow the full 3h
# from the owner's role-selection decision (not from a standby heartbeat).
primary_age = minutes_since(primary_at or role.get("set_at"))
standby_age = minutes_since(standby_at)
other_author = role["monitors"][other].get("commit_author") or ""

# The 50-minute guard protects against real concurrent GitHub writes.
# A failed git-log inspection is uncertainty: skip rather than race.
try:
    proc = subprocess.run(
        ["git", "log", "origin/main", f"--since={guard} minutes ago",
         f"--author={other_author}", "--format=%h %s"],
        cwd=repo, check=True, capture_output=True, text=True,
    )
    recent_other = proc.stdout.strip()
except (OSError, subprocess.CalledProcessError) as exc:
    print(json.dumps({"action": "skip", "reason": "collision guard unavailable; avoid concurrent write", "error": type(exc).__name__}))
    raise SystemExit(0)

if recent_other:
    action = "skip"
    reason = f"other monitor ({other}) wrote within {guard} minutes: {recent_other.splitlines()[0]}"
elif args.me == primary:
    action = "run"
    reason = "preferred primary; no recent conflicting write"
elif args.me != standby:
    action = "skip"
    reason = "not assigned primary or standby"
elif standby_age < standby_yield:
    action = "skip"
    reason = f"standby yield {standby_age:.0f}/{standby_yield} min; allow preferred primary to recover"
elif primary_age <= threshold:
    action = "skip"
    reason = f"standby; primary last verified (or owner role set) {primary_age:.0f}/{threshold} min ago"
else:
    action = "failover"
    reason = f"primary {primary} has no verified cycle for {primary_age:.0f} min (threshold {threshold} min); takeover: {args.me} becomes primary"

swapped = False
if action == "failover" and not args.dry_run:
    role.update(primary=args.me, standby=primary, set_by="auto_takeover",
                set_at=now.isoformat(timespec="seconds").replace("+00:00", "Z"),
                reason=f"automatic takeover: {primary} had no verified cycle for {primary_age:.0f} min; {args.me} became primary (owner rule 10.10.2026)")
    (repo / "monitor-role.json").write_text(json.dumps(role, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    swapped = True

print(json.dumps({"action": action, "reason": reason, "primary": role["primary"],
                  "runner": args.me, "primary_age_minutes": round(primary_age, 1), "swapped": swapped}))
