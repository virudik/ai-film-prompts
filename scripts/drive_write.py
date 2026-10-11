#!/usr/bin/env python3
"""Google Drive copy writer for AI Film (GitHub Actions, no owner computer, NO key file).

Since 11.10.2026 the canon is GitHub `main`; Drive «AI Film Prompts Master» holds read-only COPIES.
This script refreshes those copies from `main` — it never writes canon to Drive and never creates,
moves, shares or deletes anything. Authentication is keyless: google-github-actions/auth (Workload
Identity Federation, GitHub OIDC → service account `ai-film-writer`) exports
GOOGLE_APPLICATION_CREDENTIALS; no JSON key exists anywhere (org policy forbids it).
Without those credentials every mode is a clean no-op reporting `not_configured`.

usage: drive_write.py [sync|probe|requests]          (default: sync)

sync / probe  — daily: for video-prompts.md, the 7 instructions, film-backlog.md, film-analysis.md
  1. resolve the file (known Drive ID; film-analysis.md by exact name inside the folder, exactly one hit)
     and check name + parent folder;
  2. download the Drive bytes; equal to `main` → `current`, nothing written;
  3. otherwise the Drive bytes must equal ONE OF THE PAST VERSIONS of that file in git (the copy is just
     stale). Anything else was edited by hand on Drive → `drift`: NOT overwritten; the workflow opens
     the issue `drive-drift` so an agent ports the edit into `main`;
  4. write the exact bytes of `main` to the SAME file ID (files.update), read back and require equal
     sha256 → `written`; otherwise `error`.
  `probe` does everything except the write (status `would_write`).
  Afterwards the workflow runs `scripts/cert_github.py . --drive-copy-dir <copies>`.
requests      — legacy request files drive-write-requests/*.json (base_sha256 guarded same-ID writes).

Result summary: drive-write-results/copy-sync.json (+ copies directory given by DRIVE_COPY_DIR).
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REQ = Path("drive-write-requests")
RES = Path("drive-write-results")
ALLOWED_PARENT = "1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6"  # AI Film Prompts Master
HISTORY_DEPTH = 400
INSTRUCTIONS = ["NEW-CHAT-HANDOFF.md", "SYNC-RUNBOOK.md", "AI-PROJECT-GUIDE.md", "PROMPT-STYLE-GUIDE.md",
                "USER-GUIDE.md", "README-AI-SYNC.md", "BACKUP-AI-RUNBOOK.md"]
KNOWN_IDS = {"video-prompts.md": "1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj",
             "film-backlog.md": "1YixC7zQFY7z3Bn1XGXxeQIMema3inCT9"}
COPY_FILES = ["video-prompts.md", *INSTRUCTIONS, "film-backlog.md", "film-analysis.md"]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def session():
    """Authorised HTTP session from Application Default Credentials (external-account / WIF)."""
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip():
        return None
    import google.auth
    from google.auth.transport.requests import AuthorizedSession
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/drive"])
    s = AuthorizedSession(creds)
    request = s.request

    def with_timeout(method, url, **kw):      # never hang a scheduled run on a stuck connection
        kw.setdefault("timeout", 90)
        return request(method, url, **kw)

    s.request = with_timeout
    return s


def meta(s, fid):
    r = s.get(f"https://www.googleapis.com/drive/v3/files/{fid}",
              params={"fields": "id,name,size,modifiedTime,parents,mimeType", "supportsAllDrives": "true"})
    r.raise_for_status()
    return r.json()


def find_by_name(s, name):
    q = f"'{ALLOWED_PARENT}' in parents and name = '{name}' and trashed = false"
    r = s.get("https://www.googleapis.com/drive/v3/files",
              params={"q": q, "fields": "files(id,name,parents,mimeType,modifiedTime)", "pageSize": 5,
                      "supportsAllDrives": "true", "includeItemsFromAllDrives": "true"})
    r.raise_for_status()
    return r.json().get("files", [])


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


# --------------------------------------------------------------------------- copy sync
def variants(b):
    """A file as git/Drive may hold it: raw and without a UTF-8 BOM."""
    return {sha(b), sha(b[3:] if b.startswith(b"\xef\xbb\xbf") else b)}


def history_shas(repo, name, depth=HISTORY_DEPTH):
    """SHA-256 of every past version (raw and BOM-less) of `name` in git history."""
    out = set()
    revs = subprocess.run(["git", "log", f"--max-count={depth}", "--format=%H", "--", name], cwd=repo,
                          capture_output=True, text=True).stdout.split()
    for r in revs:
        blob = subprocess.run(["git", "show", f"{r}:{name}"], cwd=repo, capture_output=True)
        if blob.returncode == 0:
            out |= variants(blob.stdout)
    return out


def sync_copies(s, repo, *, dry_run=False, copy_dir=None, sleep=time.sleep):
    repo = Path(repo)
    results = []
    for name in COPY_FILES:
        item = {"name": name}
        results.append(item)
        local = repo / name
        if not local.is_file():
            item.update(status="skipped", detail="file is not in the repository")
            continue
        wanted = local.read_bytes()
        item["github_sha256"] = sha(wanted)
        try:
            fid = KNOWN_IDS.get(name)
            if name in INSTRUCTIONS:
                info = json.loads((repo / "instruction-sync-status.json").read_text(encoding="utf-8"))
                fid = info["files"][name]["drive_file_id"]
            if fid is None:
                hits = find_by_name(s, name)
                if len(hits) != 1:
                    item.update(status="skipped", detail=f"{len(hits)} files named {name} in the Drive folder; not guessing")
                    continue
                fid = hits[0]["id"]
            item["file_id"] = fid
            m = meta(s, fid)
            if m.get("name") != name or ALLOWED_PARENT not in (m.get("parents") or []):
                item.update(status="rejected", detail=f"name/folder mismatch: {m.get('name')} {m.get('parents')}")
                continue
            current = download(s, fid)
            item["drive_sha256"] = sha(current)
            if current == wanted:
                item.update(status="current", drive_modified=m.get("modifiedTime"))
            elif not (variants(current) & history_shas(repo, name)):
                item.update(status="drift", detail="Drive content never existed in git: edited by hand; NOT overwritten")
                continue
            elif dry_run:
                item.update(status="would_write", drive_modified=m.get("modifiedTime"))
                continue
            else:
                up = upload(s, fid, wanted, m.get("mimeType") or "text/markdown")
                back = b""
                for _ in range(5):
                    back = download(s, fid)
                    if back == wanted:
                        break
                    sleep(3)
                if back != wanted:
                    item.update(status="error", detail="read-back sha256 differs after upload", drive_sha256=sha(back))
                    continue
                current = back
                item.update(status="written", drive_sha256=sha(back), drive_modified=up.get("modifiedTime"))
            if copy_dir and name in INSTRUCTIONS and current == wanted:
                Path(copy_dir).mkdir(parents=True, exist_ok=True)
                (Path(copy_dir) / name).write_bytes(current)
        except Exception as e:      # network/auth/quota: report, keep going with the other files
            item.update(status="error", detail=f"{type(e).__name__}: {e}"[:300])
    return results


def summarize(results):
    c = {}
    for r in results:
        c[r["status"]] = c.get(r["status"], 0) + 1
    return c


def run_sync(dry_run):
    s = session()
    if s is None:
        print(json.dumps({"status": "not_configured",
                          "detail": "no Google credentials (variables GCP_WORKLOAD_IDENTITY_PROVIDER / GCP_SERVICE_ACCOUNT not set); nothing done"}))
        return 0
    copy_dir = os.environ.get("DRIVE_COPY_DIR") or None
    results = sync_copies(s, ".", dry_run=dry_run, copy_dir=copy_dir)
    out = {"checked_at": now(), "mode": "probe" if dry_run else "sync", "summary": summarize(results), "files": results}
    RES.mkdir(exist_ok=True)
    (RES / "copy-sync.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"mode": out["mode"], "summary": out["summary"]}, ensure_ascii=False))
    for r in results:
        print(f"  {r['name']}: {r['status']}" + (f" — {r['detail']}" if r.get("detail") else ""))
    return 1 if out["summary"].get("error") or out["summary"].get("rejected") else 0


# --------------------------------------------------------------------------- legacy request files
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


def run_requests():
    reqs = sorted(REQ.glob("*.json")) if REQ.exists() else []
    if not reqs:
        print(json.dumps({"status": "nothing_to_do"}))
        return 0
    s = session()
    if s is None:
        print(json.dumps({"status": "not_configured", "detail": "no Google credentials; requests left untouched", "pending": [p.name for p in reqs]}))
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


def main(argv):
    mode = argv[1] if len(argv) > 1 else "sync"
    if mode == "requests":
        return run_requests()
    if mode in ("sync", "probe"):
        return run_sync(dry_run=(mode == "probe"))
    print("usage: drive_write.py [sync|probe|requests]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
