#!/usr/bin/env python3
"""Certify exact GitHub instruction bytes, not semantic correctness or live execution.

Rebuild a small allowlisted certificate so obsolete runtime/Drive-authority snapshots
cannot survive recertification. Pre-migration metadata is preserved in archive/ops/.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

FILES = ["NEW-CHAT-HANDOFF.md", "SYNC-RUNBOOK.md", "AI-PROJECT-GUIDE.md", "PROMPT-STYLE-GUIDE.md",
         "USER-GUIDE.md", "README-AI-SYNC.md", "BACKUP-AI-RUNBOOK.md"]
COPY_FIELDS = ("drive_file_id", "drive_copy_sha256", "drive_copy_checked_at", "drive_copy_modified_at")


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def build(repo, old, *, copies=None, modified=None, now=None):
    repo = Path(repo)
    now = now or datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    out = {"schema_version": 3, "checked_at": now, "verification_mode": "github_canonical_blob_check",
           "verification_scope": "Exact local canonical bytes only; not a semantic audit or proof of scheduler execution.",
           "source_of_truth": "github", "freshness_max_hours": 48, "health": "ok", "all_match": True,
           "files": {}, "rules": "SYNC-RUNBOOK.md", "consistency_rules": "ops/AUTOMATION-CONSISTENCY.md"}
    for name in FILES:
        data = (repo / name).read_bytes()
        previous = old.get("files", {}).get(name, {})
        info = {k: previous[k] for k in COPY_FIELDS if k in previous}
        info.update(github_blob=blob(data), mirror_sha256=hashlib.sha256(data).hexdigest(), match=True)
        if copies is not None and (Path(copies) / name).is_file():
            info.update(drive_copy_sha256=hashlib.sha256((Path(copies) / name).read_bytes()).hexdigest(),
                        drive_copy_checked_at=now)
        if name in (modified or {}):
            info["drive_copy_modified_at"] = modified[name]
        if info.get("drive_copy_sha256"):
            info["drive_copy_match"] = info["drive_copy_sha256"] == info["mirror_sha256"]
        out["files"][name] = info
    state_path = repo / "automation-monitor-status.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    hourly = state.get("automation") or {}
    if hourly:
        out["automation_schedule"] = {
            "active_automation_id": hourly["id"], "schedule": hourly["schedule"],
            "timezone": hourly.get("timezone", "Europe/Moscow"), "active_project_automation_count": 1,
            "active_project_automation_count_semantics": "One hourly ChatGPT monitor; excludes the separate Relay event handler.",
            "retired_automation_ids": [x["id"] for x in state.get("retired_automations", [])],
            "source": "automation-monitor-status.json (configured state; live Automations readback required)",
            "execution_verified_by_this_certificate": False}
    out["recovery_sync"] = {"separately_scheduled": False, "phase": "embedded_in_hourly_monitor"}
    claude = repo / "CLAUDE.md"
    if claude.exists():
        out["claude_code_bootstrap"] = {
            "path": "CLAUDE.md", "canonical": False, "included_in_7_of_7": False,
            "github_blob": blob(claude.read_bytes()), "verified": True,
            "verification_scope": "Exact file bytes only; not a semantic audit.",
            "rule": "Bootstrap pointer only; fresh GitHub main instructions always win."}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--drive-copy-dir")
    ap.add_argument("--drive-modified", nargs="*", default=[])
    a = ap.parse_args()
    p = Path(a.repo) / "instruction-sync-status.json"
    old = json.loads(p.read_text(encoding="utf-8"))
    out = build(a.repo, old, copies=a.drive_copy_dir, modified=dict(x.split("=", 1) for x in a.drive_modified))
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({n: out["files"][n].get("drive_copy_match") for n in FILES}))


if __name__ == "__main__":
    main()
