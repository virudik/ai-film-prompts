#!/usr/bin/env python3
"""Build lightweight WebP display thumbnails for reference images.

Originals under references/ are never modified. For every PNG/JPEG/WebP source a
thumbnail is written to references/thumbs/<same relative path>.webp (max 640 px
wide) and recorded in references/thumbs/manifest.json with the source SHA-256, so
the Control Center can show small cards while links/lightboxes keep opening the
exact full-size original.

  python3 scripts/build_thumbnails.py          # create/update thumbnails
  python3 scripts/build_thumbnails.py --check  # exit 1 if any thumbnail is missing/stale
"""
import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"
OUT = REF / "thumbs"
MANIFEST = OUT / "manifest.json"
MAX_W = 640
QUALITY = 82
EXTS = {".png", ".jpg", ".jpeg", ".webp"}
MIN_SOURCE_BYTES = 60_000  # smaller sources are already light; keep them as-is


def sources():
    for p in sorted(REF.rglob("*")):
        if p.is_file() and p.suffix.lower() in EXTS and OUT not in p.parents:
            yield p


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(src):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        w, h = im.size
        if w > MAX_W:
            im = im.resize((MAX_W, round(h * MAX_W / w)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=QUALITY, method=6)
        return buf.getvalue(), im.size, (w, h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        manifest = {"schema_version": 1, "items": {}}
    items = manifest.setdefault("items", {})
    wanted, stale = {}, []
    for src in sources():
        if src.stat().st_size < MIN_SOURCE_BYTES:
            continue
        rel = src.relative_to(ROOT).as_posix()
        digest = sha256(src)
        thumb = OUT / (src.relative_to(REF).as_posix() + ".webp")
        cur = items.get(rel)
        fresh = cur and cur.get("src_sha256") == digest and thumb.is_file()
        if not fresh:
            stale.append(rel)
            if not args.check:
                data, size, orig = render(src)
                thumb.parent.mkdir(parents=True, exist_ok=True)
                thumb.write_bytes(data)
                cur = {"thumb": thumb.relative_to(ROOT).as_posix(), "width": size[0], "height": size[1],
                       "src_width": orig[0], "src_height": orig[1], "src_bytes": src.stat().st_size,
                       "thumb_bytes": len(data), "src_sha256": digest}
        wanted[rel] = cur
    removed = sorted(set(items) - set(wanted))
    if args.check:
        if stale or removed:
            print("thumbnails out of date:", *stale, *("removed: " + r for r in removed), sep="\n  ")
            sys.exit(1)
        print(f"thumbnails current: {len(wanted)}")
        return
    for rel in removed:
        t = ROOT / items[rel]["thumb"]
        if t.is_file():
            t.unlink()
    manifest = {"schema_version": 1,
                "purpose": "Display thumbnails for reference images; originals are unchanged and remain the identity authority.",
                "max_width": MAX_W, "items": dict(sorted(wanted.items()))}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    src_total = sum(v["src_bytes"] for v in wanted.values())
    th_total = sum(v["thumb_bytes"] for v in wanted.values())
    print(f"thumbnails: {len(wanted)} (updated {len(stale)}, removed {len(removed)}); "
          f"sources {src_total/1048576:.1f} MB -> thumbs {th_total/1048576:.1f} MB")


if __name__ == "__main__":
    main()
