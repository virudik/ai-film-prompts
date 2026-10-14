#!/usr/bin/env python3
"""One-time reconciliation: five explicitly confirmed pre-migration owner redo clicks.

Never creates owner approval. Only releases editorial slow if:
- Supabase has an already-applied latest redo click for that exact scene;
- canonical ledger confirms reviewed=true, accepted=false, needs_redo=true;
- no open owner decisions, active physical task, or unconfirmed terminal;
- live status is green and fresh. Fails closed.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import process_owner_decisions as pod
import robot_master_actions as robot
import master_slow_edit as slow

ROOT = Path(__file__).resolve().parents[1]
SCENES = (24, 25, 27, 30, 31)


def check(root=ROOT):
    st = robot.load_state(root)
    if st["project-status.json"].get("health") != "ok":
        raise ValueError("project status is not healthy")
    now = datetime.now(timezone.utc)
    checked = st["topview-status.json"].get("checked_at")
    try:
        scanned = datetime.fromisoformat(str(checked).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        raise ValueError("Topview scan date unavailable")
    if not -2 <= (now - scanned).total_seconds() / 60 <= 60:
        raise ValueError("Topview scan not fresh: no changes without verified observation")
    if st["project-status.json"].get("canonical_master_sha256") != robot.sha256(st["video-prompts.md"]):
        raise ValueError("status/master SHA mismatch")

    scenes_filter = "in.(" + ",".join(map(str, SCENES)) + ")"
    rows = pod.api("GET", {"select": "scene_id,action,status,created_at",
                            "scene_id": scenes_filter, "status": "eq.applied",
                            "order": "created_at.desc", "limit": "200"})
    pending = pod.api("GET", {"select": "scene_id,action,status",
                               "scene_id": scenes_filter,
                               "status": "in.(pending,in_progress,needs_owner)",
                               "limit": "100"})
    blocked = {int(x["scene_id"]) for x in pending}
    latest = {}
    for x in rows:
        sid = int(x["scene_id"])
        latest.setdefault(sid, x)

    today = robot.moscow_date()
    new_master = st["video-prompts.md"]
    selected = []
    for sid in SCENES:
        if sid not in st["project-status.json"].get("slow_scenes", []):
            continue
        if sid in blocked:
            print("HOLD", sid, "open owner decision")
            continue
        row = latest.get(sid)
        if not row or row.get("action") != "redo":
            print("HOLD", sid, "latest applied action is not redo")
            continue
        ledger = st["review-ledger.json"].get("scenes", {}).get(str(sid), {})
        if (ledger.get("reviewed") is not True or ledger.get("accepted") is not False
                or ledger.get("needs_redo") is not True
                or ledger.get("inserted_into_film") is True):
            print("HOLD", sid, "ledger does not confirm owner redo")
            continue
        if robot._scene_has_physical_active_task(st, sid):
            print("HOLD", sid, "active provider task")
            continue
        if not robot._scene_has_confirmed_terminal(st, sid):
            print("HOLD", sid, "no confirmed terminal")
            continue
        new_master, info = slow.apply_plan(
            new_master, {"release": [{"scene": sid, "action": "redo"}],
                         "occupied_slots": st["topview-status.json"].get("occupied_slots", 0)}, today)
        selected.append(sid)

    if not selected:
        print("No previously applied terminal redo scenes need reconciliation")
        return 0
    temp_m = root / ".prior-review-master.tmp"
    temp_s = root / ".prior-review-status.tmp"
    try:
        temp_m.write_text(new_master, encoding="utf-8", newline="")
        current = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        generated, failed = robot.build_status(root, temp_m, temp_s, current)
        if failed or not generated or generated.get("health") != "ok":
            raise ValueError("validator refused owner slow reconciliation: " + str(failed)[:150])
        # Keep the initial real scan's physical task occupancy unchanged.
        if generated.get("slow_scenes") != [n for n in st["project-status.json"]["slow_scenes"] if n not in selected]:
            raise ValueError("unexpected slow membership after reconciliation")
        (root / "video-prompts.md").write_text(new_master, encoding="utf-8", newline="")
        (root / "project-status.json").write_text(temp_s.read_text(encoding="utf-8"), encoding="utf-8")
        (root / "SYNC-TRIGGER.txt").write_text(
            f"{current} Reconcile previously applied explicit owner redo buttons for scenes {','.join(map(str,selected))}. "
            f"Reviewed in Supabase and ledger; no Topview tasks or physical slots changed.\n", encoding="utf-8")
    finally:
        temp_m.unlink(missing_ok=True)
        temp_s.unlink(missing_ok=True)
    print("Verified previously applied owner slow release:", ",".join(map(str, selected)))
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
