#!/usr/bin/env python3
"""Archive already-successful, mapped Topview video attempts to private Drive.

Separate from monitoring and editorial state. Does not generate, approve, rerun or
remove scenes. Never publishes temporary signed URLs, source media or credentials.
GitHub Actions WIF authentication; Drive folder is a *backup* under the already
authorized AI Film Prompts Master folder.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests

BOARD = "1a6244cf1ae747ef847d949a80d6133c"
TOPVIEW_API = "https://api.topview.ai/boards/tasks/detail"
DRIVE_API = "https://www.googleapis.com/drive/v3/files"
DRIVE_UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
AUTHORIZED_PARENT = "1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6"  # existing shared folder
ARCHIVE_FOLDER = "AI Film Generated Videos"
INDEX = Path("topview-video-archive.json")
TASK_MAP = Path("topview-task-map.json")
CHUNK_SIZE = 8 * 1024 * 1024
MAX_BYTES = 350 * 1024 * 1024
HEX_ID = re.compile(r"^[0-9a-f]{32}$")


def iso_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def candidates(task_map, index):
    """Only proven task↔scene mappings, and successful *terminal* attempts."""
    seen = set(index.get("videos", {}))
    out = []
    for t in task_map.get("processed_tasks", []):
        task_id, scene_id = t.get("task_id"), t.get("scene_id")
        if (not isinstance(task_id, str) or not HEX_ID.fullmatch(task_id)
                or task_id in seen or t.get("final_status") != "success"
                or not isinstance(scene_id, int) or scene_id < 1):
            continue
        out.append((t.get("finished_at") or "", scene_id, task_id))
    out.sort(reverse=True)
    return [(scene, task_id) for _, scene, task_id in out]


def topview_detail(task_id, key, uid):
    r = requests.get(TOPVIEW_API,
                     params={"taskId": task_id},
                     headers={"Authorization": "Bearer " + key, "Topview-Uid": uid,
                              "Accept": "application/json"},
                     timeout=(20, 45))
    r.raise_for_status()
    body = r.json()
    if str(body.get("code", "")) not in ("200", "0"):
        raise RuntimeError("Topview returned non-success API code")
    task = body.get("result") or {}
    if (task.get("boardId") != BOARD or task.get("boardTaskId") != task_id
            or str(task.get("status", "")).lower() != "success"
            or task.get("mediaType") != "video"):
        raise RuntimeError("Topview task identity/status/board mismatch")
    video = (task.get("result") or {}).get("originVideo") or {}
    url = video.get("url")
    if not isinstance(url, str) or not url:
        raise RuntimeError("Topview completed task has no originVideo URL")
    parts = urlsplit(url)
    # Do not allow the provider result to make arbitrary network requests.
    host = parts.hostname or ""
    if parts.scheme != "https" or not (host == "topviewai.app" or host.endswith(".topviewai.app")
                                        or host == "topview.ai" or host.endswith(".topview.ai")):
        raise RuntimeError("Topview video URL host is not an approved CDN")
    return url


def fetch_mp4(url, output):
    md5, sha = hashlib.md5(), hashlib.sha256()
    count = 0
    with requests.get(url, stream=True, timeout=(25, 120)) as response:
        response.raise_for_status()
        if any(urlsplit(x.url).scheme != "https" for x in [*response.history, response]):
            raise RuntimeError("Insecure video redirect")
        with open(output, "wb") as f:
            for data in response.iter_content(chunk_size=1024 * 1024):
                if not data:
                    continue
                count += len(data)
                if count > MAX_BYTES:
                    raise RuntimeError("Video exceeds maximum safe download size")
                f.write(data)
                md5.update(data)
                sha.update(data)
    if count < 1024:
        raise RuntimeError("Video too small / empty")
    with open(output, "rb") as f:
        if f.read(12).lower().find(b"ftyp") < 0:
            raise RuntimeError("Downloaded content is not an MP4 container")
    return count, md5.hexdigest(), sha.hexdigest()


def drive_session():
    from google.auth import default
    from google.auth.transport.requests import AuthorizedSession
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/drive"])
    return AuthorizedSession(credentials)


def drive_list(s, parent, name):
    q = f"'{parent}' in parents and name = '{name}' and trashed = false"
    r = s.get(DRIVE_API, params={
        "q": q, "pageSize": 100,
        "fields": "nextPageToken,files(id,name,mimeType,parents,size,md5Checksum,webViewLink,appProperties)",
        "supportsAllDrives": "true", "includeItemsFromAllDrives": "true"
    }, timeout=45)
    r.raise_for_status()
    data = r.json()
    if data.get("nextPageToken"):
        raise RuntimeError("Ambiguous Drive result (pagination)")
    return data.get("files", [])


def folder(s, parent, name):
    items = drive_list(s, parent, name)
    if len(items) > 1:
        raise RuntimeError("Multiple folders with the same name")
    if items:
        if items[0].get("mimeType") != "application/vnd.google-apps.folder":
            raise RuntimeError("Drive name exists but is not a folder")
        return items[0]["id"]
    r = s.post(DRIVE_API, params={"fields": "id,name,mimeType", "supportsAllDrives": "true"},
               json={"name": name, "mimeType": "application/vnd.google-apps.folder",
                     "parents": [parent]}, timeout=45)
    r.raise_for_status()
    return r.json()["id"]


def verify(s, fid, scene_folder, task_id, size, md5):
    r = s.get(DRIVE_API + "/" + fid,
              params={"fields": "id,name,size,md5Checksum,mimeType,parents,appProperties,webViewLink",
                      "supportsAllDrives": "true"}, timeout=45)
    r.raise_for_status()
    f = r.json()
    if (f.get("name") != task_id + ".mp4" or f.get("mimeType") != "video/mp4"
            or scene_folder not in f.get("parents", [])
            or f.get("appProperties", {}).get("topview_task_id") != task_id
            or int(f.get("size") or -1) != size
            or f.get("md5Checksum") != md5):
        raise RuntimeError("Drive upload read-back / checksum mismatch; do not certify")
    return f


def upload_mp4(s, parent, task_id, scene_id, path, size):
    metadata = {
        "name": task_id + ".mp4", "parents": [parent], "mimeType": "video/mp4",
        "appProperties": {"topview_task_id": task_id, "scene_id": str(scene_id),
                          "source": "Topview", "archive_schema": "1"}}
    r = s.post(DRIVE_UPLOAD,
               params={"uploadType": "resumable", "fields": "id,name,size,md5Checksum,parents,appProperties"},
               json=metadata,
               headers={"X-Upload-Content-Type": "video/mp4",
                        "X-Upload-Content-Length": str(size)},
               timeout=60)
    r.raise_for_status()
    location = r.headers.get("Location", "")
    url = urlsplit(location)
    if url.scheme != "https" or not (url.hostname == "www.googleapis.com" or
                                       (url.hostname or "").endswith(".googleapis.com")):
        raise RuntimeError("Unexpected Google resumable upload URL")
    start = 0
    with open(path, "rb") as src:
        while start < size:
            src.seek(start)
            part = src.read(min(CHUNK_SIZE, size - start))
            end = start + len(part) - 1
            for attempt in range(4):
                try:
                    result = s.put(location, data=part, headers={
                        "Content-Type": "video/mp4",
                        "Content-Length": str(len(part)),
                        "Content-Range": f"bytes {start}-{end}/{size}"}, timeout=150)
                    if result.status_code in (200, 201):
                        return result.json()["id"]
                    if result.status_code == 308:
                        last = result.headers.get("Range", "")
                        next_start = int(last.rsplit("-", 1)[-1]) + 1 if last else 0
                        if next_start <= start and attempt < 3:
                            time.sleep(2 ** attempt)
                            continue
                        start = next_start
                        break
                    if result.status_code in (429, 500, 502, 503, 504):
                        time.sleep(2 ** attempt)
                        continue
                    result.raise_for_status()
                except requests.RequestException:
                    if attempt == 3:
                        raise
                    time.sleep(2 ** attempt)
            else:
                raise RuntimeError("Drive upload retry budget exhausted")
    raise RuntimeError("Drive upload ended without a confirmed final response")


def run(limit, task_id=None):
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("::error title=Topview archive::No WIF Google credentials")
        return 2
    key, uid = os.environ.get("TOPVIEW_API_KEY", ""), os.environ.get("TOPVIEW_UID", "")
    if not key or not uid:
        print("::error title=Topview archive::Topview API configuration missing")
        return 2
    mapping = json.loads(TASK_MAP.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {
        "schema_version": 1, "location": "AI Film Prompts Master/AI Film Generated Videos",
        "videos": {}}
    jobs = candidates(mapping, index)
    if task_id:
        # Only select already-mapped success; no arbitrary ID supplied by CI/operator.
        jobs = [j for j in jobs if j[1] == task_id]
    else:
        jobs = jobs[:limit]
    if not jobs:
        print("Topview archive: no unmapped/unarchived successful video tasks")
        return 0
    s = drive_session()
    archive_id = folder(s, AUTHORIZED_PARENT, ARCHIVE_FOLDER)
    errors = []
    successes = 0
    for scene_id, tid in jobs:
        phase = "prepare_scene_folder"
        try:
            scene_folder = folder(s, archive_id, f"Scene-{scene_id:02d}")
            phase = "topview_task_detail"
            url = topview_detail(tid, key, uid)
            with tempfile.TemporaryDirectory(prefix="topview-mp4-") as d:
                temp = Path(d) / "video.mp4"
                phase = "download_mp4"
                size, md5, sha = fetch_mp4(url, temp)
                phase = "drive_lookup_existing"
                already = drive_list(s, scene_folder, tid + ".mp4")
                if len(already) > 1:
                    raise RuntimeError("Multiple archived files with this task ID")
                if already:
                    drive_id = already[0]["id"]
                else:
                    phase = "drive_upload"
                    drive_id = upload_mp4(s, scene_folder, tid, scene_id, temp, size)
                phase = "drive_verify"
                verified = verify(s, drive_id, scene_folder, tid, size, md5)
            # Index only verified successes. No signed Topview media URLs in git.
            index["videos"][tid] = {
                "scene_id": scene_id, "file_id": verified["id"],
                "size_bytes": size, "md5": md5, "sha256": sha,
                "archived_at": iso_now(),
                "drive_url": "https://drive.google.com/file/d/" + verified["id"] + "/view"}
            INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8")
            successes += 1
            print(f"::notice title=Topview archive::Verified Scene {scene_id}, task {tid[:8]}, bytes {size}")
        except Exception as e:
            # Never print exception messages, responses or URLs: signed MP4 URLs may
            # appear there. Stage and HTTP status are sufficient for safe triage.
            status = getattr(getattr(e, "response", None), "status_code", None)
            code = f" HTTP {status}" if isinstance(status, int) else ""
            print(f"::error title=Topview archive::Scene {scene_id}, task {tid[:8]}: "
                  f"{phase}: {type(e).__name__}{code}")
            errors.append((scene_id, tid))
    print(f"Topview archive: verified={successes}, failed={len(errors)}, pending_before={len(jobs)}")
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=2)
    parser.add_argument("--task-id", default=None)
    args = parser.parse_args()
    if not 1 <= args.limit <= 10:
        parser.error("limit must be 1..10")
    if args.task_id and not HEX_ID.fullmatch(args.task_id):
        parser.error("invalid task id")
    return run(args.limit, args.task_id)


if __name__ == "__main__":
    sys.exit(main())
