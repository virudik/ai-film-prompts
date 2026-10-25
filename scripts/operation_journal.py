"""Lossless retention for Topview operation history; publish both files in one CAS commit.

Archive offsets preserve even identical events. Archive-first atomic writes allow a retry
after interruption without either dropping records or copying the same batch twice.
"""
import json
import os
import tempfile
from pathlib import Path

JOURNAL = "topview-operation-journal.json"
ARCHIVE = "archive/ops/topview-operation-journal-archive.json"


def trim(journal, archive=None):
    events = journal.get("events")
    keep = journal.get("retention_max_events", 500)
    offset = journal.get("archived_event_count", 0)
    if (not isinstance(events, list) or type(keep) is not int or keep < 1
            or type(offset) is not int or offset < 0):
        raise ValueError("Invalid operation journal retention state")
    if len(events) <= keep:
        return None
    if archive is None:
        archive = {"schema_version": 1, "description": "Operation history, oldest first; never a launch queue.",
                   "events": []}
    if not isinstance(archive, dict) or not isinstance(archive.get("events"), list):
        raise ValueError("Invalid operation journal archive")
    old = events[:-keep]
    saved = archive["events"]
    pending = saved[offset:]
    if (len(saved) < offset or len(pending) > len(old)
            or pending != old[:len(pending)]):
        raise ValueError("Operation archive offset/content conflict; fresh-read before retry")
    live = dict(journal, events=events[-keep:], archived_event_count=offset + len(old),
                events_archive=ARCHIVE)
    return live, dict(archive, events=saved[:offset] + old)


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=path.name + ".", suffix=".tmp", delete=False) as f:
            temp = Path(f.name)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def write(root, journal):
    root = Path(root)
    archive = None
    # Avoid loading cold history on cycles that do not move any events.
    if len(journal.get("events", [])) > journal.get("retention_max_events", 500):
        path = root / ARCHIVE
        if path.exists():
            archive = json.loads(path.read_text(encoding="utf-8"))
    result = trim(journal, archive)
    if result:
        journal, archive = result
        atomic_json(root / ARCHIVE, archive)
    atomic_json(root / JOURNAL, journal)
