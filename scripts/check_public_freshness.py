#!/usr/bin/env python3
"""Independent watchdog for already-published AI Film data.

This checker has NO Topview/Drive credentials and never claims to refresh either.
In particular, GitHub master-sync time and automation run time cannot substitute
for Topview status.checked_at or the seven-file instruction certificate checked_at.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def stamp(value):
    if not isinstance(value, str):
        raise ValueError("missing ISO 8601 timestamp")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timezone missing")
    return dt.astimezone(timezone.utc)


def inspect(root, now, topview_limit=105, instruction_limit=165, master_limit=100):
    """Return a public-safe, deterministic report. No writes, no network."""
    root = Path(root)
    errors = []
    ages = {}

    def load(filename):
        try:
            return json.loads((root / filename).read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(f"{filename}: missing or invalid JSON ({type(exc).__name__})")
            return {}

    top = load("topview-status.json")
    task = load("topview-task-map.json")
    checkpoint = load("topview-checkpoint.json")
    instruction = load("instruction-sync-status.json")
    project = load("project-status.json")

    def check_age(label, value, limit):
        try:
            minutes = (now - stamp(value)).total_seconds() / 60
            ages[label] = round(minutes, 1)
            if minutes > limit:
                errors.append(f"{label}: {minutes:.0f} min old (limit {limit} min)")
            if minutes < -5:
                errors.append(f"{label}: timestamp is more than 5 min in the future")
        except (ValueError, TypeError) as exc:
            errors.append(f"{label}: invalid verification timestamp ({type(exc).__name__})")

    check_age("Topview PUBLIC checked_at", top.get("checked_at"), topview_limit)
    check_age("Instruction exact-check checked_at", instruction.get("checked_at"), instruction_limit)
    check_age("Canonical master sync", project.get("synced_at"), master_limit)

    checked = top.get("checked_at")
    if not (checked and checked == checkpoint.get("checked_at")
            == task.get("updated_at") == task.get("last_scan_at")):
        errors.append("Topview public/map/stable-checkpoint timestamps differ")

    active = top.get("active_tasks") or []
    top_ids = [x.get("task_id") for x in active]
    map_groups = task.get("active_by_scene") or {}
    map_ids = [x for group in map_groups.values() for x in group]
    cp_ids = checkpoint.get("active_task_ids") or []
    if (any(not x for x in top_ids) or len(top_ids) != len(set(top_ids))
            or sorted(top_ids) != sorted(map_ids) or sorted(top_ids) != sorted(cp_ids)):
        errors.append("Topview active task IDs differ between public/map/checkpoint")

    capacity = top.get("slot_capacity")
    occupied = top.get("occupied_slots")
    if (not isinstance(capacity, int) or not isinstance(occupied, int)
            or occupied != len(active) or top.get("free_slots") != capacity - occupied
            or not 0 <= occupied <= capacity
            or checkpoint.get("occupied_slots") != occupied):
        errors.append("Topview slot capacity/count invariant failed")

    public_scenes = sorted({int(x["scene_id"]) for x in active if str(x.get("scene_id", "")).isdigit()})
    mapped_scenes = sorted(int(k) for k, group in map_groups.items() if group and str(k).isdigit())
    checkpoint_scenes = sorted(checkpoint.get("active_scene_ids") or [])
    project_scenes = sorted(project.get("slow_scenes") or [])
    if not (public_scenes == mapped_scenes == checkpoint_scenes == project_scenes):
        errors.append("Unique slow Scene IDs do not agree across public/map/checkpoint/master status")

    if project.get("health") != "ok":
        errors.append("Canonical project-status health is not ok")
    try:
        actual_hash = hashlib.sha256((root / "video-prompts.md").read_bytes()).hexdigest()
        if actual_hash != project.get("canonical_master_sha256"):
            errors.append("Published master bytes disagree with project-status SHA-256")
    except OSError:
        errors.append("Published video-prompts.md unavailable for hash check")

    files = instruction.get("files") or {}
    if (instruction.get("health") != "ok" or instruction.get("all_match") is not True
            or len(files) != 7 or any(f.get("match") is not True for f in files.values())):
        errors.append("Seven-document instruction exact-match certificate is missing/unhealthy")

    return {
        "ok": not errors,
        "checked_at": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "ages_minutes": ages,
        "topview_last_verified_at": checked,
        "instruction_last_verified_at": instruction.get("checked_at"),
        "observed_slots": occupied,
        "observed_capacity": capacity,
        "errors": errors,
        "note": ("Independent freshness assessment only; never advances timestamps, "
                 "queries Topview, approves/reruns scenes, or treats last master-sync "
                 "time as proof of Topview/instruction verification."),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--topview-limit", type=int, default=105)
    parser.add_argument("--instruction-limit", type=int, default=165)
    parser.add_argument("--master-limit", type=int, default=100)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    report = inspect(args.root, datetime.now(timezone.utc),
                     args.topview_limit, args.instruction_limit, args.master_limit)
    data = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.write_text(data + "\n", encoding="utf-8")
    print(data)
    for error in report["errors"]:
        print("::error::AI Film public freshness: " + error)
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
