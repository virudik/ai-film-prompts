#!/usr/bin/env python3
"""Delete byte-identical PNG copies and point every text link at the file that stays.

The image bytes do not change. Only the path in prompts, JSON, HTML and other text does.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

TEXT_EXT = {".md", ".json", ".html", ".js", ".yml", ".yaml", ".txt", ".py", ".css"}


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_groups(root):
    root = Path(root)
    groups = {}
    for path in root.rglob("*.png"):
        if not path.is_file() or ".git" in path.parts:
            continue
        groups.setdefault(file_sha256(path), []).append(path.relative_to(root).as_posix())
    return {digest: sorted(paths) for digest, paths in groups.items() if len(paths) > 1}


def reference_counts(root, paths):
    root = Path(root)
    counts = {path: 0 for path in paths}
    wanted = set(paths)
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_EXT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for rel in wanted:
            counts[rel] += text.count(rel)
    return counts


def choose_keeper(paths, counts):
    """Prefer the path other files already cite, then a name that is not marked as a copy."""

    def rank(path):
        low = path.lower()
        penalty = 1 if any(mark in low for mark in ("copy", "old", "backup", "duplicate", "(1)")) else 0
        return (-counts.get(path, 0), penalty, len(path), path)

    return sorted(paths, key=rank)[0]


def plan(root):
    """Return {removed_path: keeper_path} for identical PNGs."""
    root = Path(root)
    mapping = {}
    for paths in png_groups(root).values():
        counts = reference_counts(root, paths)
        keeper = choose_keeper(paths, counts)
        for path in paths:
            if path != keeper:
                mapping[path] = keeper
    return mapping


def apply_plan(root, mapping, write=False):
    """Rewrite text links and delete the copies. Returns (rewritten_files, deleted_paths)."""
    root = Path(root)
    if not mapping:
        return [], []
    ordered = sorted(mapping, key=len, reverse=True)
    rewritten = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_EXT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        new = text
        for old in ordered:
            new = new.replace(old, mapping[old])
        if new != text:
            rewritten.append(path.relative_to(root).as_posix())
            if write:
                path.write_text(new, encoding="utf-8")
    deleted = []
    for old in ordered:
        target = root / old
        if target.is_file():
            deleted.append(old)
            if write:
                target.unlink()
    return rewritten, deleted


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    mapping = plan(args.root)
    rewritten, deleted = apply_plan(args.root, mapping, write=args.write)
    for old in sorted(mapping):
        print(f"{old} -> {mapping[old]}")
    print(f"copies={len(mapping)} rewritten={len(rewritten)} deleted={len(deleted)} write={args.write}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
