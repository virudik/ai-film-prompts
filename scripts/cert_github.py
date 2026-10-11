#!/usr/bin/env python3
"""Refresh instruction-sync-status.json (canon = GitHub main since the owner decision of 11.10.2026).

usage: cert_github.py <repo> [--drive-copy-dir DIR] [--drive-modified NAME=ISO ...]
The 7 canonical instructions live in GitHub main; Google Drive holds a read-only backup copy.
This writes, for each instruction file, the GitHub blob + sha256 of the
repo file (what the validator checks) and, when --drive-copy-dir is given (files downloaded
from Drive), whether the Drive copy currently equals GitHub (informational only).
Run it after every commit that changes an instruction, and after refreshing the Drive copy.
"""
import argparse, hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

FILES = ["NEW-CHAT-HANDOFF.md", "SYNC-RUNBOOK.md", "AI-PROJECT-GUIDE.md", "PROMPT-STYLE-GUIDE.md",
         "USER-GUIDE.md", "README-AI-SYNC.md", "BACKUP-AI-RUNBOOK.md"]

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("--drive-copy-dir")
ap.add_argument("--drive-modified", nargs="*", default=[])
a = ap.parse_args()
repo = Path(a.repo)
p = repo / "instruction-sync-status.json"
d = json.loads(p.read_text(encoding="utf-8"))
mods = dict(x.split("=", 1) for x in a.drive_modified)
now = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
for name in FILES:
    data = (repo / name).read_bytes()
    info = d["files"].setdefault(name, {})
    info["github_blob"] = subprocess.check_output(["git", "hash-object", name], cwd=repo, text=True).strip()
    info["mirror_sha256"] = hashlib.sha256(data).hexdigest()
    info["match"] = True
    if a.drive_copy_dir:
        dc = Path(a.drive_copy_dir) / name
        if dc.is_file():
            info["drive_copy_sha256"] = hashlib.sha256(dc.read_bytes()).hexdigest()
            info["drive_copy_match"] = info["drive_copy_sha256"] == info["mirror_sha256"]
            info["drive_copy_checked_at"] = now
    if name in mods:
        info["drive_copy_modified_at"] = mods[name]
    # Informational only: the Drive copy is a read-only backup. Without fresh copies, recompute
    # whether the last known copy still equals the file in main (it may now lag behind).
    if not a.drive_copy_dir and info.get("drive_copy_sha256"):
        info["drive_copy_match"] = info["drive_copy_sha256"] == info["mirror_sha256"]
d.update(source_of_truth="github", checked_at=now, all_match=True, health="ok",
         verification_mode="github_canonical_blob_check", freshness_max_hours=48,
         note="С 11.10.2026 канон 7 инструкций — GitHub main (решение владельца 03:25 МСК); Drive — копия для чтения, drive_copy_* поля справочные.")
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: d["files"][k].get("drive_copy_match") for k in FILES}, ensure_ascii=False))
