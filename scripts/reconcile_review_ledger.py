#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ledger_path = ROOT / "review-ledger.json"
project_path = ROOT / "project-status.json"
taskmap_path = ROOT / "topview-task-map.json"

ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
project = json.loads(project_path.read_text(encoding="utf-8"))
taskmap = json.loads(taskmap_path.read_text(encoding="utf-8"))
changed = False

# Human decision fields are never inferred by this reconciler.\nblank = {
    "result_received": False,
    "result_received_at": None,
    "reviewed": None,
    "reviewed_at": None,
    "accepted": None,
    "needs_redo": None,
    "inserted_into_film": None,
    "montage_note": None,
    "last_human_update_at": None,
}

for scene_id in project.get("scene_ids", []):
    sid = str(scene_id)
    if sid not in ledger["scenes"]:
        ledger["scenes"][sid] = dict(blank)
        changed = True

for item in taskmap.get("processed_tasks", []):
    if str(item.get("final_status", "")).lower() != "success":
        continue
    sid = str(item.get("scene_id"))
    if sid not in ledger["scenes"]:
        continue
    row = ledger["scenes"][sid]
    if row.get("result_received") is not True:
        row["result_received"] = True
        row["result_received_at"] = item.get("finished_at")
        changed = True
    elif not row.get("result_received_at") and item.get("finished_at"):
        row["result_received_at"] = item["finished_at"]
        changed = True

if changed:
    ledger["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("review-ledger reconciled")
else:
    print("review-ledger already current")
