#!/usr/bin/env python3
"""Record an agent's actual takeover, never infer one from generated readiness.

Local canonical writer: caller must hold the project lock, CAS-push and read back.
Evidence describes observations made by the receiving agent, not this script.
"""
import argparse
import copy
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_resume_packet import build
from resume_project import context
from resume_state import digest, local_file

CHECKS = {"fresh_main", "instructions", "checkpoint", "owner_inbox",
          "owner_decisions", "capabilities", "project_lock"}
KEEP = 20


def timestamp(value):
    when = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if when.tzinfo is None:
        raise ValueError("timestamp requires timezone")
    return when


def validate(receipt, project):
    if receipt.get("schema_version") != 1 or receipt.get("project") != project:
        raise ValueError("receipt schema/project mismatch")
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,100}", receipt.get("receipt_id", "")):
        raise ValueError("invalid receipt ID")
    chat = receipt.get("chat", {})
    if not chat.get("label") or not chat.get("session_id") or not chat.get("agent"):
        raise ValueError("receiving agent, label and session ID required")
    if chat.get("identity_status") == "verified":
        if not chat.get("chat_id") or not chat.get("identity_evidence"):
            raise ValueError("verified chat identity requires actual ID and evidence")
    elif chat.get("identity_status") != "unavailable" or chat.get("chat_id") is not None:
        raise ValueError("unknown chat identity must be explicit, never invented")
    checks = receipt.get("checks", [])
    if not isinstance(checks, list) or len(checks) != len(CHECKS) or {c.get("id") for c in checks} != CHECKS:
        raise ValueError("all takeover checks required exactly once")
    if any(c.get("result") not in {"passed", "blocked"} or not c.get("evidence") for c in checks):
        raise ValueError("checks require result and concrete evidence")
    started, accepted = timestamp(receipt["started_at"]), timestamp(receipt["accepted_at"])
    if accepted < started or accepted > datetime.now(timezone.utc):
        raise ValueError("invalid takeover time")
    outcome = receipt.get("outcome")
    action = receipt.get("first_action", {})
    if outcome not in {"accepted", "waiting_for_owner", "blocked"}:
        raise ValueError("invalid takeover outcome")
    if outcome != "blocked" and any(c["result"] != "passed" for c in checks):
        raise ValueError("blocked checks cannot claim acceptance")
    if not action.get("description") or not action.get("evidence"):
        raise ValueError("first action and evidence are required")
    expected = {"accepted": {"started", "completed"}, "waiting_for_owner": {"waiting"}, "blocked": {"not_started"}}
    if action.get("state") not in expected[outcome]:
        raise ValueError("first action state contradicts takeover outcome")
    if not started <= timestamp(action["at"]) <= accepted:
        raise ValueError("first action outside takeover interval")


def record(root, receipt, project="seregius"):
    root = Path(root)
    validate(receipt, project)
    ctx = context(root, project)
    path = root / ctx["receipts"]
    archive = root / ctx["prefix"] / "archive/reports/handoff-receipts.json"
    live = json.loads(path.read_bytes()) if path.exists() else {"schema_version": 1, "project": project, "receipts": []}
    old = json.loads(archive.read_bytes()) if archive.exists() else {"schema_version": 1, "project": project, "receipts": []}
    request_sha = digest(json.dumps(receipt, sort_keys=True, ensure_ascii=False).encode())
    for collection in (live, old):
        if collection.get("project") != project or not isinstance(collection.get("receipts"), list):
            raise ValueError("invalid receipt history")
        for r in collection["receipts"]:
            if r["receipt_id"] == receipt["receipt_id"]:
                if r.get("request_sha256") != request_sha:
                    raise ValueError("receipt ID conflict; history is immutable")
                return r  # retry after push uncertainty: no duplicate or new timestamp
    lock = json.loads(local_file(root, ctx["lock"]).read_bytes())
    if (lock.get("state") != "held" or lock.get("holder") != receipt["chat"]["agent"]
            or timestamp(lock["expires_at"]) <= datetime.now(timezone.utc)):
        raise ValueError("own unexpired project lock required")
    packet = build(root, project=project)
    if receipt["outcome"] != "blocked" and not packet["ready_for_resume"]:
        raise ValueError("recovery not verified: " + "; ".join(packet["reasons"]))
    selected = packet.get("selected_work") or {}
    if receipt.get("work_id") != selected.get("work_id"):
        raise ValueError("receipt work does not match project focus")
    if receipt["outcome"] == "waiting_for_owner" and selected.get("status") != "waiting_for_owner":
        raise ValueError("waiting receipt requires idle project state")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
    if receipt.get("source_head") != head:
        raise ValueError("takeover source HEAD changed; recheck before recording")
    saved = copy.deepcopy(receipt)
    sources = [s for s in packet["sources"] if s["file"] != ctx["receipts"]]
    saved.update(request_sha256=request_sha, checked_sources=sources,
                 source_fingerprint=digest(json.dumps(sources, sort_keys=True).encode()),
                 recorded_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 source_scope="Checkout HEAD plus source bytes in the same canonical transaction", execution_authorized=False)
    live["receipts"].insert(0, saved)
    spill = live["receipts"][KEEP:]
    if spill:
        by_id = {r["receipt_id"]: r for r in old["receipts"]}
        for r in spill:
            if r["receipt_id"] in by_id and by_id[r["receipt_id"]] != r:
                raise ValueError("archive receipt ID conflict")
        old["receipts"] = [r for r in spill if r["receipt_id"] not in by_id] + old["receipts"]
        atomic(archive, old)  # archive before trimming, and both files in the same CAS commit
        live["receipts"] = live["receipts"][:KEEP]
        live["archive"] = str(archive.relative_to(root))
    atomic(path, live)
    return saved


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", nargs="?", default=".")
    p.add_argument("--project", default="seregius")
    p.add_argument("--input", required=True, help="JSON with actual observations; see CONTINUE-PROTOCOL")
    a = p.parse_args()
    r = record(a.repo, json.loads(Path(a.input).read_bytes()), a.project)
    print(json.dumps({k: r[k] for k in ("receipt_id", "project", "work_id", "outcome")}, ensure_ascii=False))
