#!/usr/bin/env python3
"""Yandex Disk links for finished videos, same format for every project (owner decision 26.11.2026).

Each project keeps its list in <project root>/topview-video-archive.json ("Серёгиус": repository root,
others: projects/<id>/). An entry (key = Topview task id, or a short id for a video made elsewhere):
  scene_id, project, yandex_path, yandex_public_key, yandex_verified_at, size_bytes, md5, sha256
  (+ file_id / drive_url for the older Google Drive copy, kept as a fallback).
The site (video-source.js) asks the public Yandex API for a fresh download link on every open.

Two jobs, run on a machine with rclone set up for Yandex (the owner's box; no keys in GitHub):
  publish  -- for entries without a Yandex key: find the file under --remote (task id in the name, else
              exact size), compare md5 (rclone) and md5+sha256+size (public API after publishing) with the
              entry; publish only that one file, never a folder; on any mismatch unpublish and report.
  import   -- merge records from a manifest (list or {"videos": [...]}) with project, scene,
              yandex_public_key, yandex_path, optional task_id/key, part, source, label: the public API must answer for the key;
              size/md5/sha256 come from it.
Never prints tokens or rclone.conf. Deletes nothing, renames nothing. Writes only with --write.
"""
import argparse, json, re, subprocess, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://cloud-api.yandex.net/v1/disk/public/resources?fields=md5,sha256,size,name,type&public_key="
KEY_RE = re.compile(r"^https://(yadi\.sk|disk\.yandex\.(ru|com))/(i|d)/[A-Za-z0-9_-]{6,}$")
TASK_RE = re.compile(r"[0-9a-f]{32}")


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def archive_path(project):
    return ROOT / "topview-video-archive.json" if project == "seregius" else ROOT / "projects" / project / "topview-video-archive.json"


def load(project):
    p = archive_path(project)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"schema_version": 1, "project": project, "videos": {}}


def save(project, data):
    p = archive_path(project)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def public_meta(key):
    for i in range(5):
        try:
            with urllib.request.urlopen(API + urllib.parse.quote(key, safe=""), timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 + i)
    return None


def rclone(*args, timeout=900):
    return subprocess.run(["rclone", *args], capture_output=True, text=True, timeout=timeout)


def publish(args):
    data = load(args.project)
    remote = args.remote.rstrip("/") + "/"
    sizes = {}
    for line in rclone("lsf", "-R", "--files-only", "--format", "ps", remote).stdout.splitlines():
        path, size = line.rsplit(";", 1)
        sizes[path] = int(size)
    md5 = {}
    for line in rclone("md5sum", remote).stdout.splitlines():
        h, path = line.split("  ", 1)
        md5[path] = h
    done, bad = 0, []
    for tid, e in sorted(data["videos"].items()):
        if e.get("yandex_public_key") and not args.recheck:
            continue
        cands = [p for p in sizes if tid in p] or [p for p in sizes if sizes[p] == e.get("size_bytes")]
        cands = [p for p in cands if md5.get(p) == e.get("md5") and sizes[p] == e.get("size_bytes")]
        if not cands:
            bad.append((tid, "no file with the same size and md5"))
            continue
        path = sorted(cands)[0]
        if not args.write:
            print("would publish", tid, path)
            continue
        out = rclone("link", remote + path, timeout=120).stdout.strip()
        meta = public_meta(out) if KEY_RE.match(out) else None
        if not meta or meta.get("md5") != e.get("md5") or meta.get("sha256") != e.get("sha256") or meta.get("size") != e.get("size_bytes"):
            rclone("link", "--unlink", remote + path, timeout=120)
            bad.append((tid, "public API check failed, unpublished"))
            continue
        e.update({"project": args.project, "yandex_public_key": out, "yandex_verified_at": now(),
                  "yandex_path": args.remote.split(":", 1)[-1].rstrip("/") + "/" + path})
        save(args.project, data)
        done += 1
    print(f"published and verified: {done}; problems: {len(bad)}")
    for tid, why in bad:
        print("  ", tid, why)
    return 1 if bad else 0


def import_manifest(args):
    raw = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    rows = raw.get("videos", raw) if isinstance(raw, dict) else raw
    if isinstance(rows, dict):
        rows = [dict(v, key=k) for k, v in rows.items()]
    by_project, bad = {}, []
    for r in rows:
        pid = str(r.get("project") or "").strip()
        key = str(r.get("yandex_public_key") or "")
        scene = r.get("scene_id", r.get("scene"))
        vkey = str(r.get("task_id") or r.get("key") or "")
        if not vkey:
            m = TASK_RE.search(str(r.get("yandex_path") or ""))
            vkey = m.group(0) if m else ""
        if not re.fullmatch(r"[a-z0-9-]+", pid) or not KEY_RE.match(key) or not str(scene).isdigit() or not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", vkey):
            bad.append((vkey or key, "needs project, scene, yandex_public_key and task_id/key"))
            continue
        meta = public_meta(key) if args.write else {"size": r.get("size_bytes")}
        if not meta or (args.write and meta.get("type") not in (None, "file")):
            bad.append((vkey, "Yandex public API did not answer for this key"))
            continue
        if args.write and r.get("md5") and meta.get("md5") != r.get("md5"):
            bad.append((vkey, "md5 from Yandex differs from the manifest"))
            continue
        data = by_project.setdefault(pid, load(pid))
        e = data["videos"].setdefault(vkey, {})
        e.update({"project": pid, "scene_id": int(scene), "yandex_public_key": key,
                  "yandex_path": str(r.get("yandex_path") or ""), "yandex_verified_at": now()})
        for k_out, k_in in (("size_bytes", "size"), ("md5", "md5"), ("sha256", "sha256")):
            if meta.get(k_in) is not None:
                e[k_out] = meta[k_in]
        for k in ("part", "source", "label"):
            if r.get(k):
                e[k] = str(r[k])[:60]
        e.setdefault("archived_at", r.get("archived_at") or now())
    for pid, data in by_project.items():
        if args.write:
            save(pid, data)
        print(pid, len(data["videos"]), "videos", "(written)" if args.write else "(dry run)")
    for k, why in bad:
        print("  problem", k, why)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("publish")
    a.add_argument("--project", default="seregius")
    a.add_argument("--remote", required=True, help='e.g. "ya-api:Нейровидео/Серёгиус/. Topview"')
    a.add_argument("--recheck", action="store_true")
    a.add_argument("--write", action="store_true")
    b = sub.add_parser("import")
    b.add_argument("manifest")
    b.add_argument("--write", action="store_true")
    args = ap.parse_args()
    sys.exit(publish(args) if args.cmd == "publish" else import_manifest(args))


if __name__ == "__main__":
    main()
