#!/usr/bin/env python3
"""Topview public-API scanner for the GitHub robot — SHADOW MODE (owner decision 11.10.2026).

Read-only: GET /boards/list, GET /boards/tasks/list, GET /boards/tasks/detail. Never submits,
approves, reruns, deletes or spends credits. Auth headers `Authorization: Bearer <key>` and
`Topview-Uid: <uid>` come from the environment (TOPVIEW_API_KEY secret, TOPVIEW_UID variable) and
are never printed.

Light / full logic is the monitor's (scripts/topview_light_check.py::decide):
  * light  — board list + newest page of the main board + detail of every known-active task;
  * full   — every owned board, every page of video tasks (when counters changed, the last full
             scan is >170 min old, or there is no record of one).
Task ↔ Scene mapping comes ONLY from topview-task-map.json (the monitor's map). A task that is not
in it is reported as `unknown_new`; a Scene ID is never invented.

Output: shadow/topview-robot-status.json (written only when its non-volatile content changed) and a
comparison with the monitor's topview-status.json. The robot does NOT write topview-status.json,
topview-task-map.json or any telemetry the monitor owns; switching over is the owner's decision.

usage: topview_api_scan.py [--repo DIR] [--output shadow/topview-robot-status.json] [--mode auto|light|full]
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
import topview_light_check as light      # noqa: E402

BASE = "https://api.topview.ai"
MAIN_BOARD = light.MAIN
SLOT_CAPACITY = 6
ACTIVE = {"init", "queued", "running", "processing"}          # = build_project_status.ACTIVE_TOPVIEW_STATUSES
TERMINAL = {"success", "fail", "failed", "cancelled"}         # = build_project_status.TERMINAL_TOPVIEW_STATUSES
VOLATILE = {"checked_at", "generated_at", "last_full_scan_at", "api_requests", "monitor_age_minutes"}
MAX_PAGES_PER_BOARD = 60
DETAIL_CAP = 40
OUTPUT = "shadow/topview-robot-status.json"


class ApiError(RuntimeError):
    """Never carries headers, keys or response bodies."""


class Client:
    def __init__(self, key, uid, opener=urlopen, sleep=time.sleep):
        self._headers = {"Authorization": "Bearer " + key.strip(), "Topview-Uid": uid.strip(),
                         "Accept": "application/json"}
        self._open, self._sleep, self.requests = opener, sleep, 0

    def get(self, path, query=None):
        url = BASE + path + (("?" + urlencode(query)) if query else "")
        last = None
        for delay in (0, 2, 6):
            if delay:
                self._sleep(delay)
            self.requests += 1
            try:
                with self._open(Request(url, headers=self._headers, method="GET"), timeout=30) as r:
                    payload = json.loads(r.read(4_000_000).decode("utf-8"))
            except HTTPError as e:
                last = f"HTTP {e.code}"
                if e.code in (429, 500, 502, 503, 504):
                    continue
                break
            except (URLError, TimeoutError, ValueError) as e:
                last = type(e).__name__
                continue
            code = str(payload.get("code", "200"))
            if code not in ("200", "0") or payload.get("result") is None:
                raise ApiError(f"{path}: api code {code[:20]}")
            return payload["result"]
        raise ApiError(f"{path}: {last}")


def items_of(result):
    """The API reference says result.list, the verified live answer uses result.data — accept both."""
    if isinstance(result, dict):
        for k in ("data", "list"):
            if isinstance(result.get(k), list):
                return result[k], int(result.get("total") or 0)
    if isinstance(result, list):
        return result, len(result)
    return [], 0


def list_boards(c):
    out, page = [], 1
    while page <= 10:
        items, total = items_of(c.get("/boards/list", {"pageNo": page, "pageSize": 50}))
        out += items
        if not items or len(out) >= total:
            break
        page += 1
    return out


def list_tasks(c, board, page_no, page_size):
    return items_of(c.get("/boards/tasks/list", {"boardId": board, "mediaType": "video", "sortField": "gmtCreate",
                                                  "sortOrder": "desc", "pageNo": page_no, "pageSize": page_size}))


def task_detail(c, task_id):
    try:
        return c.get("/boards/tasks/detail", {"taskId": task_id})
    except ApiError:
        return None


def is_unlimited(t):
    p = t.get("parameters") if isinstance(t.get("parameters"), dict) else {}
    return bool(t.get("useUnlimitMode") or p.get("useUnlimitMode"))


def status_of(t):
    return str(t.get("status") or "").lower()


def iso(dt):
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def strip_volatile(x):
    if isinstance(x, dict):
        return {k: strip_volatile(v) for k, v in x.items() if k not in VOLATILE}
    if isinstance(x, list):
        return [strip_volatile(v) for v in x]
    return x


# --------------------------------------------------------------------------- scan
def scan(c, repo, prev, *, mode="auto", now=None):
    repo = Path(repo)
    now = now or datetime.now(timezone.utc)
    tm = read_json(repo / "topview-task-map.json", {})
    monitor = read_json(repo / "topview-status.json", {})
    scene_of = {tid: int(sid) for sid, ids in (tm.get("active_by_scene") or {}).items() for tid in ids}
    done_scene = {p["task_id"]: p.get("scene_id") for p in tm.get("processed_tasks", []) if p.get("task_id")}
    known_active = set(scene_of)
    # Active tasks of the other projects (projects/topview-projects.json, owner decision 20.10.2026) are watched
    # like known tasks, so their terminal state is never missed even if a robot cycle did not publish.
    projects_tel = read_json(repo / "projects" / "topview-projects.json", {}) or {}
    known_active |= {t["task_id"] for t in projects_tel.get("active", []) if t.get("task_id")}
    prev_active = {a["task_id"] for a in prev.get("active_tasks", []) if a.get("task_id")}

    boards = list_boards(c)
    main_items, _ = list_tasks(c, MAIN_BOARD, 1, 20)
    basis = {"scan_cursor": prev.get("cursor") or {}, "last_scan_at": prev.get("checked_at") or tm.get("last_scan_at"),
             "active_by_scene": tm.get("active_by_scene") or {}, "processed_tasks": tm.get("processed_tasks") or []}
    decision = light.decide(basis, boards, main_items, force=(mode == "full"), now=now)
    scan_mode = "light" if (mode == "light" or (mode == "auto" and decision["mode"] == "light")) else "full"

    seen = {}          # boardTaskId -> task dict (+ _board)
    pages = 1
    for t in main_items:
        seen[t["boardTaskId"]] = dict(t, _board=MAIN_BOARD)
    if scan_mode == "full":
        seen, pages = {}, 0
        for b in boards:
            if int(b.get("taskCount") or 0) == 0:
                continue
            page_no, got = 1, 0
            while page_no <= MAX_PAGES_PER_BOARD:
                items, total = list_tasks(c, b["boardId"], page_no, 100)
                pages += 1
                for t in items:
                    seen[t["boardTaskId"]] = dict(t, _board=b["boardId"])
                got += len(items)
                if not items or got >= total:
                    break
                page_no += 1
    # refresh every task we expect to be alive, plus anything active in the data we already hold
    watch = (known_active | prev_active | {i for i, t in seen.items() if status_of(t) in ACTIVE})
    details, detail_failed = {}, []
    for tid in sorted(watch)[:DETAIL_CAP]:
        d = task_detail(c, tid)
        if d is None:
            detail_failed.append(tid)
        else:
            details[tid] = d
    detail_failed += sorted(watch)[DETAIL_CAP:]

    def best(tid):
        """Most authoritative record we have for a task: detail > list entry."""
        return details.get(tid) or seen.get(tid)

    active, finished, missing = [], [], []
    for tid in sorted(watch):
        rec = best(tid)
        if rec is None:
            if tid in known_active or tid in prev_active:
                missing.append(tid)
            continue
        st = status_of(rec)
        if st in ACTIVE:
            est = rec.get("estimateInfo") or {}
            p = rec.get("parameters") if isinstance(rec.get("parameters"), dict) else {}
            sid = scene_of.get(tid)
            active.append({"task_id": tid, "board_id": rec.get("boardId") or seen.get(tid, {}).get("_board"),
                           "status": st, "unlimited": is_unlimited(rec), "created_at": rec.get("gmtCreate"),
                           "model": p.get("modelName"), "scene_id": sid,
                           "mapping": "task_map" if sid is not None else "unknown_new",
                           "queue_count": est.get("queueCount"), "wait_seconds": est.get("estimatedWaitSeconds"),
                           "process_seconds": est.get("estimatedProcessSeconds")})
        elif st in TERMINAL and (tid in known_active or tid in prev_active):
            finished.append({"task_id": tid, "scene_id": scene_of.get(tid), "final_status": st,
                             "completed_at": rec.get("completedAt"),
                             "error_code": rec.get("errorCode") if st != "success" else None})
    # A task that the monitor's map does not know: created after the previous robot scan, or active now.
    last_scan = light.ts(basis["last_scan_at"])
    unknown = {}
    for tid, t in seen.items():
        created = light.ts(t.get("gmtCreate"))
        if tid in scene_of or tid in done_scene:
            continue
        if (last_scan and created and created > last_scan) or status_of(t) in ACTIVE:
            p = t.get("parameters") if isinstance(t.get("parameters"), dict) else {}
            unknown[tid] = {"task_id": tid, "board_id": t.get("_board"), "status": status_of(t),
                            "created_at": t.get("gmtCreate"), "model": p.get("modelName"),
                            "unlimited": is_unlimited(t), "prompt_head": (p.get("positivePrompt") or "")[:200]}
    for a in active:
        if a["mapping"] == "unknown_new" and a["task_id"] not in unknown:
            unknown[a["task_id"]] = {"task_id": a["task_id"], "board_id": a["board_id"], "status": a["status"],
                                     "created_at": a["created_at"], "model": a["model"],
                                     "unlimited": a["unlimited"], "prompt_head": ""}
    unknown_new_list = sorted(unknown.values(), key=lambda u: u["created_at"] or "")
    unlimited_active = [a for a in active if a["unlimited"]]
    cutoff = now - timedelta(hours=24)
    recent = []
    for tid, t in seen.items():
        done = light.ts(t.get("completedAt"))
        if status_of(t) in TERMINAL and done and done >= cutoff:
            recent.append({"task_id": tid, "scene_id": scene_of.get(tid, done_scene.get(tid)),
                           "mapping": "task_map" if (tid in scene_of or tid in done_scene) else "unknown_new",
                           "final_status": status_of(t), "completed_at": t.get("completedAt")})
    recent.sort(key=lambda r: r["completed_at"] or "", reverse=True)

    counts = decision["board_task_counts"]
    complete = scan_mode == "full" and not detail_failed
    cursor = dict(prev.get("cursor") or {})
    cursor["board_task_counts"] = counts
    if scan_mode == "full":
        cursor["last_full_scan_at"] = iso(now)
    status = {
        "schema_version": 1, "mode": "shadow", "source": "topview public API (read-only)",
        "generated_by": "scripts/topview_api_scan.py", "checked_at": iso(now),
        "note": "ТЕНЕВОЙ режим: не источник истины. Телеметрию публикует монитор; сравнение — в comparison.",
        "scan": {"mode": scan_mode, "reasons": decision["reasons"], "boards": len(boards),
                 "board_task_counts": counts, "pages_scanned": pages, "tasks_seen": len(seen),
                 "api_requests": c.requests, "detail_failed": detail_failed},
        "cursor": cursor,
        "slots": {"capacity": SLOT_CAPACITY, "occupied": len(unlimited_active),
                  "free": max(0, SLOT_CAPACITY - len(unlimited_active)),
                  "basis": "active unlimited video tasks on all owned boards",
                  "complete": complete,
                  "active_not_unlimited": len(active) - len(unlimited_active)},
        "active_tasks": active, "unknown_new": unknown_new_list, "finished_known": finished,
        "missing_known_active": missing, "recent_completions": recent[:30],
    }
    status["comparison"] = compare(status, monitor, now)
    return status


def compare(robot, monitor, now):
    """Robot vs the monitor's published topview-status.json. Differences are information, not alarms:
    the monitor runs every ~3 h, so a lagging monitor is flagged as `monitor_may_lag`."""
    m_checked = monitor.get("checked_at")
    m_dt = light.ts(m_checked)
    age = round((now - m_dt).total_seconds() / 60) if m_dt else None
    m_tasks = {t.get("task_id"): t for t in monitor.get("active_tasks", []) if t.get("task_id")}
    r_tasks = {a["task_id"]: a for a in robot["active_tasks"] if a["unlimited"]}
    diffs = []
    for tid in sorted(set(m_tasks) - set(r_tasks)):
        diffs.append({"type": "only_in_monitor", "task_id": tid, "scene_id": m_tasks[tid].get("scene_id")})
    for tid in sorted(set(r_tasks) - set(m_tasks)):
        diffs.append({"type": "only_in_robot", "task_id": tid, "scene_id": r_tasks[tid]["scene_id"],
                      "mapping": r_tasks[tid]["mapping"]})
    for tid in sorted(set(m_tasks) & set(r_tasks)):
        if str(m_tasks[tid].get("topview_status", "")).lower() != r_tasks[tid]["status"]:
            diffs.append({"type": "status_differs", "task_id": tid, "monitor": m_tasks[tid].get("topview_status"),
                          "robot": r_tasks[tid]["status"]})
    if monitor.get("occupied_slots") is not None and monitor.get("occupied_slots") != robot["slots"]["occupied"]:
        diffs.append({"type": "occupied_differs", "monitor": monitor.get("occupied_slots"),
                      "robot": robot["slots"]["occupied"]})
    return {"monitor_checked_at": m_checked, "monitor_age_minutes": age,
            "monitor_occupied": monitor.get("occupied_slots"), "robot_occupied": robot["slots"]["occupied"],
            "consistent": not diffs, "monitor_may_lag": bool(diffs) and (age is None or age > 45),
            "differences": diffs}


def notice(status):
    s, cmp_ = status["slots"], status["comparison"]
    brief = {"scan": status["scan"]["mode"], "boards": status["scan"]["boards"],
             "occupied": f"{s['occupied']}/{s['capacity']}", "complete": s["complete"],
             "active": len(status["active_tasks"]), "unknown_new": len(status["unknown_new"]),
             "finished_known": len(status["finished_known"]), "consistent_with_monitor": cmp_["consistent"],
             "monitor_age_min": cmp_["monitor_age_minutes"],
             "differences": [f"{d['type']}:{str(d.get('task_id', ''))[:8]}" for d in cmp_["differences"][:8]]}
    return "::notice title=topview-robot-shadow::" + json.dumps(brief, ensure_ascii=False)


def write_if_changed(path, status):
    path = Path(path)
    old = read_json(path, None)
    if old is not None and strip_volatile(old) == strip_volatile(status):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--output", default=OUTPUT)
    ap.add_argument("--mode", choices=("auto", "light", "full"), default="auto")
    a = ap.parse_args()
    key, uid = os.environ.get("TOPVIEW_API_KEY", ""), os.environ.get("TOPVIEW_UID", "")
    if not key.strip() or not uid.strip():
        print("::notice title=topview-robot-shadow::not configured: TOPVIEW_API_KEY or TOPVIEW_UID absent; nothing done")
        return 0
    repo = Path(a.repo)
    out = repo / a.output
    try:
        status = scan(Client(key, uid), repo, read_json(out, {}), mode=a.mode)
    except ApiError as e:
        print(f"::error title=topview-robot-shadow::Topview API unavailable: {e}")
        return 1
    changed = write_if_changed(out, status)
    print(notice(status))
    print(json.dumps({"written": changed, "scan_mode": status["scan"]["mode"], "occupied": status["slots"]["occupied"],
                      "requests": status["scan"]["api_requests"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
