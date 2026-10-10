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
AUTO = {"accept", "redo", "to_montage", "tv_mark_status"}
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


def eligible(row):
    action = row["action"]
    return (action in ("accept", "redo", "to_montage")
            or (action == "tv_mark_status" and row.get("value") == "result_bad"))


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
    fetched = api("GET", {"select": "id,created_at,scene_id,action,value,status,result_note",
                          "status": "in.(pending,in_progress)",
                          "order": "created_at.asc", "limit": str(MAX_ROWS)})
    rows = [r for r in fetched if eligible(r) and
            (r["status"] == "pending" or str(r.get("result_note") or "").startswith(CLAIM))]
    by_scene = {}
    for r in rows:
        by_scene.setdefault(str(r["scene_id"]), []).append(r)
    ledger_path = ROOT / "review-ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    stamp = utcnow()
    planned = []
    for scene, items in by_scene.items():
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
