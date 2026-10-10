#!/usr/bin/env python3
"""Record one Claude monitor cycle in automation-monitor-status.json (honest times only).

usage: monitor_status.py <repo> --started ISO --completed ISO --health ok|degraded|error
       [--phase NAME ...] [--missing NAME ...] [--note TEXT] [--topview-checked ISO]
The site's "Монитор" chip and the D3 alert read last_scheduled_cycle.completed_at.
A cycle that could not finish its required phases must use --health degraded and
list them in --missing; never move completed_at forward without a real run.
"""
import argparse, json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("repo"); ap.add_argument("--started", required=True); ap.add_argument("--completed", required=True)
ap.add_argument("--health", required=True, choices=["ok", "degraded", "error"])
ap.add_argument("--phase", action="append", default=[]); ap.add_argument("--missing", action="append", default=[])
ap.add_argument("--note", default=""); ap.add_argument("--topview-checked")
a = ap.parse_args()
p = Path(a.repo) / "automation-monitor-status.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["last_scheduled_cycle"] = {"started_at": a.started, "completed_at": a.completed, "health": a.health,
                             "phases_completed": a.phase, "phases_missing": a.missing, "runner": "claude_scheduled_task",
                             "note": a.note}
d["last_completed_cycle_at"] = a.completed
# Last completed cycle per actual runner: standby cycles must never count as
# proof that the preferred primary has recovered.
d.setdefault("last_completed_by_runner", {})["claude"] = a.completed
d["last_scheduled_cycle"]["runner"] = "claude_scheduled_task"
if a.health == "ok":
    d["last_successful_cycle_at"] = a.completed
d["health"] = a.health
if a.topview_checked:
    d.setdefault("phases", {}).setdefault("topview", {})["checked_at"] = a.topview_checked
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("recorded", a.health, a.completed)
