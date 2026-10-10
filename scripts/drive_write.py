#!/usr/bin/env python3
"""Same-ID Google Drive writer for AI Film (runs in GitHub Actions, no owner computer).

Processes request files drive-write-requests/<name>.json:
  {
    "file_id": "<Drive file ID>",
    "name": "video-prompts.md",                 # expected Drive title (safety check)
    "payload": "drive-write-requests/<name>.payload",
    "base_sha256": "<sha256 of the CURRENT Drive bytes the edit was made from>",
    "result_sha256": "<sha256 of payload>",
    "requested_by": "claude-monitor | chatgpt-monitor | claude-chat | ...",
    "reason": "short text",
    "sync_trigger": true                        # optional: write SYNC-TRIGGER.txt after success
  }

For each request: fresh-read the Drive file → refuse if its bytes != base_sha256
(someone changed Drive since the edit was prepared; never overwrite newer content) →
upload payload to the SAME file ID (files.update, media) → download again and require
sha256 == result_sha256 → write drive-write-results/<name>.json and remove the request.
Never creates files, never changes sharing, never deletes anything on Drive.

Auth: env GDRIVE_SA_KEY = service-account JSON (GitHub secret). If it is missing the
script only reports "not_configured" and changes nothing.
"""
import base64, hashlib, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path

REQ = Path("drive-write-requests")
RES = Path("drive-write-results")
ALLOWED_PARENT = "1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6"  # AI Film Prompts Master


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def session():
    key = os.environ.get("GDRIVE_SA_KEY", "").strip()
    if not key:
        return None
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    creds = service_account.Credentials.from_service_account_info(
        json.loads(key), scopes=["https://www.googleapis.com/auth/drive"])
    return AuthorizedSession(creds)


def meta(s, fid):
    r = s.get(f"https://www.googleapis.com/drive/v3/files/{fid}",
              params={"fields": "id,name,size,modifiedTime,parents,mimeType", "supportsAllDrives": "true"})
    r.raise_for_status()
    return r.json()


def download(s, fid):
    r = s.get(f"https://www.googleapis.com/drive/v3/files/{fid}", params={"alt": "media", "supportsAllDrives": "true"})
    r.raise_for_status()
    return r.content


def upload(s, fid, data, mime):
    r = s.patch(f"https://www.googleapis.com/upload/drive/v3/files/{fid}",
                params={"uploadType": "media", "supportsAllDrives": "true", "fields": "id,size,modifiedTime"},
                data=data, headers={"Content-Type": mime})
    r.raise_for_status()
    return r.json()


def process(s, req_path):
    req = json.loads(req_path.read_text(encoding="utf-8"))
    out = {"request": req_path.name, "file_id": req.get("file_id"), "name": req.get("name"),
           "requested_by": req.get("requested_by"), "reason": req.get("reason"), "processed_at": now()}
    payload = Path(req["payload"]).read_bytes()
    if sha(payload) != req["result_sha256"]:
        return dict(out, status="rejected", detail="payload sha256 != result_sha256")
    m = meta(s, req["file_id"])
    if m.get("name") != req.get("name") or ALLOWED_PARENT not in (m.get("parents") or []):
        return dict(out, status="rejected", detail=f"file name/folder mismatch: {m.get('name')} {m.get('parents')}")
    current = download(s, req["file_id"])
    out["drive_before"] = {"sha256": sha(current), "size": len(current), "modifiedTime": m.get("modifiedTime")}
    if sha(current) == req["result_sha256"]:
        return dict(out, status="applied", detail="Drive already has exactly these bytes (idempotent)")
    if sha(current) != req["base_sha256"]:
        return dict(out, status="rejected", detail="Drive changed since the edit was prepared (base_sha256 mismatch); prepare the edit again from fresh Drive")
    up = upload(s, req["file_id"], payload, m.get("mimeType") or "text/markdown")
    for attempt in range(5):
        back = download(s, req["file_id"])
        if sha(back) == req["result_sha256"]:
            break
        time.sleep(3)
    ok = sha(back) == req["result_sha256"]
    return dict(out, status="applied" if ok else "error", drive_after={"sha256": sha(back), "size": len(back), "modifiedTime": up.get("modifiedTime")},
                detail="same-ID write + byte-exact read-back" if ok else "read-back mismatch after upload")


def main():
    reqs = sorted(REQ.glob("*.json")) if REQ.exists() else []
    if not reqs:
        print(json.dumps({"status": "nothing_to_do"}))
        return 0
    s = session()
    if s is None:
        print(json.dumps({"status": "not_configured", "detail": "GitHub secret GDRIVE_SA_KEY is not set; requests left untouched", "pending": [p.name for p in reqs]}))
        return 0
    RES.mkdir(exist_ok=True)
    sync = False
    failed = False
    for p in reqs:
        try:
            r = process(s, p)
        except Exception as e:  # network/auth errors: keep the request for a retry
            print(json.dumps({"request": p.name, "status": "retry_later", "error": f"{type(e).__name__}: {e}"[:500]}))
            failed = True
            continue
        (RES / p.name).write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(r, ensure_ascii=False))
        req = json.loads(p.read_text(encoding="utf-8"))
        if r["status"] == "applied" and req.get("sync_trigger"):
            sync = True
        Path(req["payload"]).unlink(missing_ok=True)
        p.unlink()
        failed |= r["status"] == "error"
    if sync:
        Path("SYNC-TRIGGER.txt").write_text(f"{now()} drive-write workflow: same-ID Drive write applied; re-sync master.\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
