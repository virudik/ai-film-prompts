#!/usr/bin/env python3
"""Apply only deterministic owner button decisions from Supabase to review-ledger.json.

Used by the EXISTING scheduled sync-from-drive.yml. Never edits Google Drive,
retires a scene, starts a render, or infers editorial approval. Supabase's
service-role key must live ONLY in GitHub Actions Secrets, never in Pages.
Two-phase operation: prepare -> validated GitHub push -> ack. A claimed
in_progress row is retryable after an interrupted run.
"""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://vzohfatqzyioydtgjiyd.supabase.co/rest/v1/owner_decisions"
AUTO = {"tv_mark_status"}
# Owner review must atomically update ledger AND canonical slow (phase 2).
MASTER_ACTIONS = {"in_film", "scene_not_needed", "tv_drop_task", "accept", "redo", "to_montage"}
MAX_ROWS = 100
CLAIM = "github-owner-sync:"
ROOT = Path(__file__).resolve().parents[1]


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def api(method, query, value=None):
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not key:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is not configured")
    headers = {"apikey": key, "Authorization": "Bearer " + key,
               "Content-Type": "application/json", "Accept": "application/json",
               "Prefer": "return=representation"}
    data = None if value is None else json.dumps(value, ensure_ascii=False).encode("utf-8")
    req = Request(BASE + "?" + urlencode(query, safe=".,()*"), data=data,
                  headers=headers, method=method)
    try:
        with urlopen(req, timeout=20) as response:
            body = response.read().decode("utf-8")
    except HTTPError as e:
        raise RuntimeError("Supabase HTTP " + str(e.code)) from e
    return json.loads(body) if body else []


def patch_status(row_id, from_status, to_status, note):
    matches = api("PATCH", {"id": "eq." + row_id, "status": "eq." + from_status,
                            "select": "id"},
                  {"status": to_status, "result_note": note})
    return bool(matches)


def button_token(row):
    """Normalised meaning of a button row, used for conflict detection between phases."""
    action, value = row.get("action"), row.get("value")
    if action == "tv_mark_status":
        return "result_bad" if value == "result_bad" else "result_ok" if value == "result_ok" else "tv_mark_status"
    return action


# in_film only contradicts a rejection; scene_not_needed contradicts every verdict on the same scene.
_CONFLICTS = {
    "in_film": {"redo", "result_bad", "scene_not_needed"},
    "scene_not_needed": {"accept", "to_montage", "redo", "result_bad", "result_ok", "in_film"},
    "accept": {"redo", "result_bad", "scene_not_needed"},
    "redo": {"accept", "to_montage", "result_ok", "in_film", "scene_not_needed"},
    "to_montage": {"redo", "result_bad", "scene_not_needed"},
}


def master_conflict(master_tokens, other_tokens):
    """True when a pending master button (in_film / scene_not_needed) contradicts another open button."""
    return any(_CONFLICTS.get(m, set()) & set(other_tokens) for m in master_tokens)


def eligible(row):
    action = row["action"]
    return action == "tv_mark_status" and row.get("value") == "result_bad"


def transform(ledger_row, action, stamp):
    row = dict(ledger_row)
    if action == "redo" and row.get("inserted_into_film") is True:
        raise ValueError("сцена уже отмечена «в фильме», откат требует решения владельца")
    row["reviewed"] = True
    row["reviewed_at"] = stamp
    row["last_human_update_at"] = stamp
    if action == "accept":
        row["accepted"] = True
        row["needs_redo"] = False
    elif action == "redo":
        row["accepted"] = False
        row["needs_redo"] = True
    elif action == "to_montage":
        row["accepted"] = True
        row["needs_redo"] = False
        row["montage_note"] = "в монтаж"
    elif action == "tv_mark_status":
        row["accepted"] = False
        row["needs_redo"] = True
    else:
        raise ValueError("not an automatic ledger action")
    return row


def prepare(plan_path):
    # Includes retryable claimed rows, but excludes manual owner_tasks.
    fetched = api("GET", {"select": "id,created_at,scene_id,action,task_id,value,status,result_note",
                          "status": "in.(pending,in_progress)",
                          "order": "created_at.asc", "limit": str(MAX_ROWS)})
    # Buttons of the other projects (projects/README.md, 20.10.2026) belong to phase 4, never to this ledger.
    import projects as prj
    tel = prj.project_tasks(ROOT)
    fetched = [r for r in fetched if prj.is_root_row(r, tel)]
    rows = [r for r in fetched if eligible(r) and
            (r["status"] == "pending" or str(r.get("result_note") or "").startswith(CLAIM))]
    by_scene = {}
    for r in rows:
        by_scene.setdefault(str(r["scene_id"]), []).append(r)
    # A scene whose pending master button (in_film / scene_not_needed) contradicts a ledger button is
    # left untouched here: the master-actions phase (scripts/robot_master_actions.py) classifies the
    # whole scene as needs_owner. Applying e.g. «Переделать» first would hide the conflict.
    master_by_scene = {}
    for r in fetched:
        if r["action"] in MASTER_ACTIONS and r["action"] != "tv_drop_task":
            master_by_scene.setdefault(str(r["scene_id"]), set()).add(button_token(r))
    held = {sid for sid, mt in master_by_scene.items()
            if master_conflict(mt, {button_token(x) for x in by_scene.get(sid, [])})}
    ledger_path = ROOT / "review-ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    stamp = utcnow()
    planned = []
    for scene, items in by_scene.items():
        if scene in held:
            continue
        actions = {x["action"] for x in items}
        if (("accept" in actions or "to_montage" in actions)
                and ("redo" in actions or
                     any(x["action"] == "tv_mark_status" for x in items))):
            for x in items:
                if x["status"] == "pending":
                    patch_status(x["id"], "pending", "needs_owner",
                                 "Противоречивые кнопки «Принять/В монтаж» и «Переделать/Брак»; нужно одно решение владельца")
            continue
        original = ledger.get("scenes", {}).get(scene)
        if original is None:
            for x in items:
                if x["status"] == "pending":
                    patch_status(x["id"], "pending", "needs_owner",
                                 "Scene ID отсутствует в review-ledger; автоматическая правка остановлена")
            continue
        result = dict(original)
        try:
            for item in items:
                result = transform(result, item["action"], stamp)
        except ValueError as e:
            for x in items:
                if x["status"] == "pending":
                    patch_status(x["id"], "pending", "needs_owner", str(e))
            continue
        claimed = []
        for item in items:
            if item["status"] == "in_progress":
                claimed.append(item)
            elif patch_status(item["id"], "pending", "in_progress",
                              CLAIM + " GitHub Actions принял решение, ожидается проверенный commit"):
                claimed.append(item)
        if not claimed:
            continue
        # Recompute from actual claimed rows; a cancelled row must not apply.
        result = dict(original)
        for item in claimed:
            result = transform(result, item["action"], stamp)
        ledger["scenes"][scene] = result
        planned.extend({"id": x["id"], "scene_id": scene, "action": x["action"]}
                       for x in claimed)
    plan = {"updates": planned, "prepared_at": stamp}
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if planned:
        ledger["updated_at"] = stamp
        ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"planned": len(planned), "manual_rows_skipped": len(fetched) - len(rows)}))


def ack(plan_path):
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    for item in plan["updates"]:
        patch_status(item["id"], "in_progress", "applied",
                     "Автоматически применено к review-ledger.json через проверенный GitHub commit; master и генерации не изменялись")
    print(json.dumps({"acknowledged": len(plan["updates"])}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "ack"))
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(Path(args.plan))
    else:
        ack(Path(args.plan))
