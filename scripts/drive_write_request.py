#!/usr/bin/env python3
"""Create a same-ID Drive write request for .github/workflows/drive-write.yml.

usage: drive_write_request.py <repo> --file-id ID --name video-prompts.md \
         --base <fresh Drive bytes the edit started from> --new <edited file> \
         --by claude-monitor --reason "Scene 20 finished" [--sync]
Writes drive-write-requests/<stamp>-<name>.json + .payload; the caller commits and pushes
them. The workflow refuses the write if Drive no longer equals --base.
"""
import argparse, hashlib, json, shutil
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("--file-id", required=True)
ap.add_argument("--name", required=True)
ap.add_argument("--base", required=True)
ap.add_argument("--new", required=True)
ap.add_argument("--by", required=True)
ap.add_argument("--reason", required=True)
ap.add_argument("--sync", action="store_true")
a = ap.parse_args()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
d = Path(a.repo) / "drive-write-requests"
d.mkdir(exist_ok=True)
stem = f"{stamp}-{a.name.replace('/', '_')}"
payload = d / f"{stem}.payload"
shutil.copyfile(a.new, payload)
req = {"file_id": a.file_id, "name": a.name, "payload": f"drive-write-requests/{stem}.payload",
       "base_sha256": sha(a.base), "result_sha256": sha(a.new), "requested_by": a.by,
       "reason": a.reason, "sync_trigger": a.sync, "created_at": stamp}
(d / f"{stem}.json").write_text(json.dumps(req, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"request": f"drive-write-requests/{stem}.json", **{k: req[k] for k in ("base_sha256", "result_sha256")}}))
