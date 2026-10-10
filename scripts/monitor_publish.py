#!/usr/bin/env python3
"""Publish one verified Topview snapshot (Claude monitor). Writes, in contract order:
topview-task-map.json → topview-operation-journal.json → topview-status.json →
review-ledger.json (result_received only) → topview-checkpoint.json (LAST).

usage: monitor_publish.py <repo> <cycle.json>
cycle.json:
{
 "checked_at": "<ISO Z, real time the scan finished>",
 "boards": 11, "pages": 13, "video_tasks": 554,
 "active": [{"scene_id":16,"task_id":"…","model":"Wan 3.0","model_id":"qwen-wan3.0-video",
             "status":"init","started_at":"…Z","queue_count":1,"wait_seconds":2,
             "mapping_confidence":"exact canonical Scene 16 prompt/reference/model match"}],
 "finished": [{"scene_id":30,"task_id":"…","final_status":"success","finished_at":"…Z"}],
 "operation": "claude_monitor_hourly_cycle", "previous_status": "…", "new_status": "…",
 "verification": "…", "note": "…",
 "canonical": {"verified_at":"…Z","master_sha256":"…","health":"ok"}
}
Never approves, reruns or deletes anything; editorial fields are not touched.
"""
import json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def main():
    repo, cyc = Path(sys.argv[1]), json.load(open(sys.argv[2], encoding="utf-8"))
    T = cyc["checked_at"]
    load = lambda n: json.loads((repo / n).read_text(encoding="utf-8"))
    save = lambda n, d: (repo / n).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    act = cyc.get("active", []); fin = cyc.get("finished", [])
    ids = [a["task_id"] for a in act]
    assert len(ids) == len(set(ids))
    by_scene = {}
    for a in act:
        by_scene.setdefault(str(a["scene_id"]), []).append(a["task_id"])

    m = load("topview-task-map.json")
    m["updated_at"] = T; m["last_scan_at"] = T
    m["active_by_scene"] = by_scene
    known = {p["task_id"] for p in m["processed_tasks"]}
    for f in fin:
        if f["task_id"] not in known:
            m["processed_tasks"].append({"task_id": f["task_id"], "scene_id": f["scene_id"], "final_status": f["final_status"], "finished_at": f["finished_at"]})
    m["processed_tasks"] = m["processed_tasks"][-m.get("retention", {}).get("processed_tasks_max", 200):]
    c = m["scan_cursor"]
    ov = (datetime.fromisoformat(T.replace("Z", "+00:00")) - timedelta(hours=6)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    c.update(last_successful_scan_at=T, pages_scanned=cyc["pages"], tasks_scanned=cyc["video_tasks"], total_video_tasks=cyc["video_tasks"], overlap_from=ov, unknown_recent_tasks=0, boards_scanned=cyc["boards"])
    save("topview-task-map.json", m)

    j = load("topview-operation-journal.json")
    j["events"].append({"timestamp": T, "operation": cyc.get("operation", "claude_monitor_hourly_cycle"), "scene_id": None,
                        "task_fingerprint": None, "previous_status": cyc.get("previous_status", ""), "new_status": cyc.get("new_status", ""),
                        "source_checkpoint": T, "outcome": "canonical_and_telemetry_verified_pending_public_readback", "verification": cyc.get("verification", "")})
    j["events"] = j["events"][-j.get("retention_max_events", 500):]
    save("topview-operation-journal.json", j)

    t = load("topview-status.json")
    t["checked_at"] = T
    if cyc.get("note"):
        t["note"] = cyc["note"]
    t["ui_contract"]["three_view_checked_at"] = T
    t["occupied_slots"] = len(act); t["free_slots"] = max(0, t.get("slot_capacity", 6) - len(act))
    prev = {x.get("task_id"): x for x in t.get("active_tasks", [])}
    t["active_tasks"] = []
    for a in act:
        row = dict(prev.get(a["task_id"], {}))
        row.update(scene_id=a["scene_id"], task_id=a["task_id"], model=a["model"], model_id=a.get("model_id"), topview_status=a["status"],
                   started_at=a.get("started_at"), queue_count=a.get("queue_count"), topview_estimated_wait_seconds=a.get("wait_seconds"),
                   checked_at=T, topview_estimated_process_seconds=None, verified=True,
                   mapping_confidence=a.get("mapping_confidence", row.get("mapping_confidence", "")))
        t["active_tasks"].append(row)
    sc = t.setdefault("scenes", {})
    for sid, tids in by_scene.items():
        lead = next(x for x in t["active_tasks"] if x["task_id"] == tids[0])
        e = dict(sc.get(sid, {})); e.update({k: lead[k] for k in ("scene_id", "task_id", "model", "model_id", "topview_status", "started_at", "queue_count", "topview_estimated_wait_seconds", "checked_at", "verified", "mapping_confidence")})
        e.update(active_task_ids=tids, completed_at=None, topview_estimated_process_seconds=None)
        sc[sid] = e
    for f in fin:
        sid = str(f["scene_id"])
        if sid in by_scene:
            continue  # scene still has another active task
        e = dict(sc.get(sid, {"scene_id": f["scene_id"]}))
        e.update(task_id=f["task_id"], topview_status=f["final_status"], queue_count=None, topview_estimated_wait_seconds=None,
                 topview_estimated_process_seconds=None, checked_at=T, active_task_ids=[], completed_at=f["finished_at"])
        sc[sid] = e
    ao = t.setdefault("account_observation", {})
    ao.update(scope="all_owned_boards_unlimited_video_tasks", complete=True, checked_at=T, boards_scanned=cyc["boards"],
              video_tasks_scanned=cyc["video_tasks"], pages_scanned=cyc["pages"], slot_capacity=t.get("slot_capacity", 6),
              occupied_slots=len(act), free_slots=t["free_slots"], active_task_ids=ids)
    save("topview-status.json", t)

    r = load("review-ledger.json")
    changed = False
    for f in fin:
        if f["final_status"] != "success":
            continue
        e = r["scenes"].setdefault(str(f["scene_id"]), {"result_received": False, "result_received_at": None, "reviewed": None, "reviewed_at": None, "accepted": None, "needs_redo": None, "inserted_into_film": None, "montage_note": None, "last_human_update_at": None})
        if e.get("result_received") in (False, None) or e.get("selected_result_task_id") != f["task_id"]:
            e.update(result_received=True, result_received_at=f["finished_at"], selected_result_task_id=f["task_id"], result_url=None)
            changed = True
    if changed:
        r["updated_at"] = T
        save("review-ledger.json", r)

    cp = load("topview-checkpoint.json")
    now = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    can = cyc["canonical"]
    cp.update(committed_at=now, checked_at=T, occupied_slots=len(act), active_task_ids=ids,
              active_scene_ids=sorted(int(s) for s in by_scene), task_map_updated_at=T, task_map_last_scan_at=T,
              canonical_validation={"verified_at": can["verified_at"], "health": can["health"], "canonical_master_sha256": can["master_sha256"], "all_project_checks_true": can["health"] == "ok"})
    save("topview-checkpoint.json", cp)
    print(json.dumps({"checked_at": T, "occupied": len(act), "slow": sorted(int(s) for s in by_scene), "ledger_changed": changed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
