#!/usr/bin/env python3
"""Summarize a full Topview account scan from saved list_board_tasks pages.

usage: topview_scan_summary.py <repo> <page.json> [<page.json> ...] [--inline-total N]
Each page file is the JSON returned by topview_list_board_tasks (result.data[]).
Pass --inline-total for tasks counted from small boards read inline (all terminal).
Prints JSON: totals, active tasks, known/unknown classification against
topview-task-map.json, terminal transitions of previously active tasks, and
tasks created after the last scan (candidates for scene intake). Read-only.
"""
import json, sys
from datetime import datetime
from pathlib import Path

ACTIVE = {"init", "queued", "queue", "running", "processing", "pending"}


def main():
    args = sys.argv[1:]
    repo = Path(args.pop(0))
    inline = 0
    if "--inline-total" in args:
        i = args.index("--inline-total"); inline = int(args[i + 1]); del args[i:i + 2]
    tasks = {}
    boards = set()
    for f in args:
        data = json.load(open(f, encoding="utf-8"))["result"]["data"]
        for x in data:
            tasks[x["boardTaskId"]] = x
            boards.add(x["boardId"])
    tm = json.loads((repo / "topview-task-map.json").read_text(encoding="utf-8"))
    known_active = {t: int(s) for s, ids in tm["active_by_scene"].items() for t in ids}
    known_processed = {p["task_id"] for p in tm["processed_tasks"]}
    last_scan = datetime.fromisoformat(tm["last_scan_at"].replace("Z", "+00:00"))
    out = {"video_tasks": len(tasks) + inline, "boards_seen_in_pages": len(boards),
           "active": [], "finished_known": [], "unknown_new": [], "missing_known_active": []}
    for tid, x in tasks.items():
        st = str(x.get("status", "")).lower()
        created = datetime.fromisoformat(x["gmtCreate"].replace(" ", "T") + "+00:00")
        p = x.get("parameters") or {}
        row = {"task_id": tid, "status": st, "model": p.get("modelName"), "model_id": p.get("modelId"),
               "created_utc": x["gmtCreate"], "completed_utc": x.get("completedAt"),
               "board_id": x["boardId"], "unlimited": bool(p.get("useUnlimitMode") or x.get("useUnlimitMode"))}
        if tid in known_active:
            row["scene_id"] = known_active[tid]
            (out["active"] if st in ACTIVE else out["finished_known"]).append(row)
        elif tid not in known_processed and (st in ACTIVE or created > last_scan):
            row["prompt_head"] = (p.get("positivePrompt") or "")[:300]
            out["unknown_new"].append(row)
    seen = set(tasks)
    out["missing_known_active"] = [t for t in known_active if t not in seen]
    out["occupied_slots"] = sum(1 for x in tasks.values() if str(x.get("status", "")).lower() in ACTIVE)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
