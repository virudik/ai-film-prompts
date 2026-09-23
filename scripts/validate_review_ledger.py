#!/usr/bin/env python3
import json
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
ledger = json.loads((repo / "review-ledger.json").read_text(encoding="utf-8"))
project = json.loads((repo / "project-status.json").read_text(encoding="utf-8"))

errors = []
if ledger.get("schema_version") != 1:
    errors.append("unsupported schema_version")
scenes = ledger.get("scenes")
if not isinstance(scenes, dict):
    errors.append("scenes must be an object")
    scenes = {}

active = {str(x) for x in project.get("scene_ids", [])}
missing = active - set(scenes)
if missing:
    errors.append(f"active scenes missing from ledger: {sorted(missing)}")

for sid, row in scenes.items():
    if not isinstance(row, dict):
        errors.append(f"scene {sid}: row is not object")
        continue
    for key in ("result_received","reviewed","accepted","needs_redo","inserted_into_film"):
        if row.get(key) not in (True, False, None):
            errors.append(f"scene {sid}: {key} must be true/false/null")
    if row.get("accepted") is True and row.get("needs_redo") is True:
        errors.append(f"scene {sid}: accepted and needs_redo cannot both be true")
    if row.get("inserted_into_film") is True and not (row.get("reviewed") is True and row.get("accepted") is True):
        errors.append(f"scene {sid}: inserted requires reviewed+accepted")
    if row.get("result_received_at") and row.get("result_received") is not True:
        errors.append(f"scene {sid}: result_received_at requires result_received=true")
    if row.get("reviewed_at") and row.get("reviewed") is not True:
        errors.append(f"scene {sid}: reviewed_at requires reviewed=true")

if errors:
    print("\n".join("ERROR: "+x for x in errors), file=sys.stderr)
    raise SystemExit(1)
print(f"review-ledger ok: {len(scenes)} rows; {len(active)} active scenes covered")
