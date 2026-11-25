#!/usr/bin/env python3
"""Assemble the GitHub Pages artifact without generation stills.

GitHub Pages from the root of main publishes the whole repository and fails or
gets cancelled when that tree is near the 1 GB site limit. The site shows
thumbs and previews; the full PNG/JPEG stills stay in git for prompts.

`ops/pages-deploy.json` `source` says what is live:
* legacy — the whole tracked tree (today's branch deploy)
* workflow — this filtered artifact
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HEAVY_EXT = {".png", ".jpg", ".jpeg"}
TEXT_EXT = {".html", ".js", ".css"}
MODES = ("legacy", "workflow")


def deploy_mode(root):
    path = Path(root) / "ops" / "pages-deploy.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "legacy"
    source = data.get("source") if isinstance(data, dict) else None
    return source if source in MODES else "legacy"


def list_files(root):
    root = Path(root)
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
        files = [line for line in out.splitlines() if line]
        if files:
            return files
    except (OSError, subprocess.CalledProcessError):
        pass
    found = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        found.append(str(path.relative_to(root)))
    return found


def static_image_refs(root, files):
    """Image paths written into HTML, JS or CSS. Runtime JSON paths are not included."""
    refs = set()
    root = Path(root)
    for rel in files:
        if Path(rel).suffix.lower() not in TEXT_EXT:
            continue
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        token = []
        for char in text:
            if char.isalnum() or char in "./_\\-":
                token.append(char)
            else:
                word = "".join(token)
                token = []
                low = word.lower()
                if low.endswith((".png", ".jpg", ".jpeg", ".webp")):
                    refs.add(word.lstrip("./").replace("\\", "/"))
        word = "".join(token)
        if word.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            refs.add(word.lstrip("./").replace("\\", "/"))
    return refs


def is_heavy_still(rel):
    norm = rel.replace("\\", "/")
    if Path(norm).suffix.lower() not in HEAVY_EXT:
        return False
    if "/thumbs/" in f"/{norm}" or "/previews/" in f"/{norm}":
        return False
    return norm.startswith("references/") or "/references/" in norm or norm.startswith("archive/")


def include_file(rel, image_refs):
    norm = rel.replace("\\", "/")
    if is_heavy_still(norm) and norm not in image_refs:
        return False
    return True


def selected_files(root, mode):
    files = list_files(root)
    if mode != "workflow":
        return files
    refs = static_image_refs(root, files)
    return [rel for rel in files if include_file(rel, refs)]


def published_bytes(root, mode=None):
    root = Path(root)
    mode = deploy_mode(root) if mode is None else mode
    total = 0
    for rel in selected_files(root, mode):
        path = root / rel
        if path.is_file():
            total += path.stat().st_size
    return total


def assemble(root, dest, mode="workflow"):
    root, dest = Path(root), Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for rel in selected_files(root, mode):
        src = root / rel
        if not src.is_file():
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    (dest / ".nojekyll").write_text("", encoding="utf-8")
    return dest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root")
    parser.add_argument("dest", nargs="?")
    parser.add_argument("--mode", choices=MODES)
    args = parser.parse_args(argv)
    mode = args.mode or ("workflow" if args.dest else deploy_mode(args.root))
    if args.dest:
        assemble(args.root, args.dest, mode)
    size = published_bytes(args.root, mode)
    print(json.dumps({"mode": mode, "bytes": size, "megabytes": size // 1_000_000}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
