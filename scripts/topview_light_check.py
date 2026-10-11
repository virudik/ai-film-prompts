#!/usr/bin/env python3
"""Decide light vs full Topview scan for the hourly monitor (owner decision 11.10.2026).

usage: topview_light_check.py <repo> <boards.json> <main_newest_page.json> [--force-full]
  boards.json            — result of topview_list_boards(mode=my-boards, pageSize=50)
  main_newest_page.json  — result of topview_list_board_tasks(boardId=<main>, mediaType=video,
                           sortField=gmtCreate, sortOrder=desc, pageSize=20, pageNo=1)
Prints JSON {"mode": "light"|"full", "reasons": [...], "board_task_counts": {...},
             "unknown_new": [...], "main_new_seen": N}.

Light is allowed only when completeness is still provable without reading every page:
  * a full scan happened less than FULL_EVERY_MIN ago and its board task counts are stored;
  * every board other than the main one has exactly the stored taskCount;
  * the main board grew by no more than the number of NEW tasks visible on its newest page
    (so every new task is on that page). Active known tasks are then refreshed one by one
    with topview_get_board_task by the monitor.
Anything else → full scan (all boards, all pages). Read-only; changes nothing.
"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path

FULL_EVERY_MIN = 170   # full scan at least every ~3 hours (hourly runs at HH:10)
MAIN = "1a6244cf1ae747ef847d949a80d6133c"


def ts(v):
    """Parse ISO ('…Z') or Topview 'YYYY-MM-DD HH:MM:SS' (UTC) timestamps."""
    if not v:
        return None
    try:
        s = str(v).strip().replace(" ", "T")
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def decide(tm, boards, page, force=False, now=None):
    """Pure decision (also used by scripts/topview_api_scan.py).
    tm     — task-map-shaped dict: scan_cursor{last_full_scan_at, board_task_counts}, last_scan_at,
             active_by_scene, processed_tasks
    boards — list of board dicts (boardId, taskCount); page — newest tasks of the main board."""
    cur = tm.get("scan_cursor", {})
    counts = {b["boardId"]: int(b.get("taskCount") or 0) for b in boards}
    stored = cur.get("board_task_counts") or {}
    last_full = ts(cur.get("last_full_scan_at"))
    last_scan = ts(tm.get("last_scan_at") or cur.get("last_successful_scan_at"))
    now = now or datetime.now(timezone.utc)
    reasons = []
    if force:
        reasons.append("forced")
    if not last_full:
        reasons.append("no recorded full scan")
    elif (now - last_full).total_seconds() / 60 >= FULL_EVERY_MIN:
        reasons.append(f"last full scan {int((now - last_full).total_seconds() / 60)} min ago")
    if not stored:
        reasons.append("no stored board task counts")
    for bid, n in counts.items():
        if bid != MAIN and stored and stored.get(bid) != n:
            reasons.append(f"board {bid} count {stored.get(bid)} -> {n}")
    if stored and set(stored) != set(counts):
        reasons.append("board set changed")

    known_active = {t for ids in tm.get("active_by_scene", {}).values() for t in ids}
    known_done = {p["task_id"] for p in tm.get("processed_tasks", [])}
    unknown, new_seen = [], 0
    for x in page:
        created = ts(x.get("gmtCreate"))
        if last_scan and created and created > last_scan:
            new_seen += 1
        if x["boardTaskId"] in known_active or x["boardTaskId"] in known_done:
            continue
        if last_scan and created and created > last_scan:
            p = x.get("parameters") or {}
            unknown.append({"task_id": x["boardTaskId"], "status": str(x.get("status", "")).lower(),
                            "created_utc": x.get("gmtCreate"), "model": p.get("modelName"),
                            "unlimited": bool(p.get("useUnlimitMode") or x.get("useUnlimitMode")),
                            "prompt_head": (p.get("positivePrompt") or "")[:300]})
    if stored and MAIN in counts:
        grew = counts[MAIN] - int(stored.get(MAIN, counts[MAIN]))
        if grew < 0:
            reasons.append(f"main board shrank by {-grew}")
        elif grew > new_seen:
            reasons.append(f"main board grew by {grew}, newest page shows only {new_seen} new")
        if new_seen >= len(page) and page:
            reasons.append("newest page is entirely new tasks; older pages may hold more")
    return {"mode": "full" if reasons else "light", "reasons": reasons,
            "board_task_counts": counts, "unknown_new": unknown, "main_new_seen": new_seen}


def main():
    args = sys.argv[1:]
    force = "--force-full" in args
    args = [a for a in args if a != "--force-full"]
    repo, boards_f, page_f = Path(args[0]), args[1], args[2]
    tm = json.loads((repo / "topview-task-map.json").read_text(encoding="utf-8"))
    boards = json.load(open(boards_f, encoding="utf-8"))["result"]["data"]
    page = json.load(open(page_f, encoding="utf-8"))["result"]["data"]
    print(json.dumps(decide(tm, boards, page, force), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
