#!/usr/bin/env python3
"""Weekly trim of the agents' service files (owner decision 23.10.2026).

The checkpoint, the resume register and the launch queue only grow: every check appends to them.
This tool moves old, already finished entries VERBATIM into archive files and leaves the live files
short. Nothing is deleted and nothing live is touched:

* reports/current-work-checkpoint.md — keeps the newest KEEP_SECTIONS top-level sections (newest on
  top), plus recovery checkpoints pinned by unfinished work; other older sections go on top of archive/checkpoints/current-work-checkpoint-archive.md.
* work-resume-register.json — finished entries leave `active_work` for `completed_work`;
  `completed_work` keeps the newest KEEP_COMPLETED, the rest go to archive/work-resume-register-archive.json;
  a live entry keeps the last KEEP_DONE points of each `done` / `completed` list; older points go to the same archive.
* ops/topview-launch-queue.json — superseded / cancelled items, and submitted / completed items older
  than SUBMITTED_DAYS, go to archive/ops/topview-launch-queue-archive.json. Submitted tasks additionally
  require a recorded provider terminal result; all physically active task IDs stay live. A short stub stays in
  `archived_items` (id, scene, block label, state, task ID, prompt SHA), so duplicate checks and the
  site's «▶ запущена» badges keep working. Waiting, claimed, blocked and held items are never moved.
* reports/topview-event-wake.json (root only) — keeps at most 100 completed receipts from the last
  30 days, plus every unresolved/blocked/unknown receipt. Only explicitly non-retryable, known terminal
  outcomes with valid past checked_at are archived verbatim. archived_event_ids preserves exact IDs
  for deduplication and robot ACK checks; diagnostic ACKs and acceptance evidence stay.
  Old test sections named in WAKE_TEST_SECTIONS (slack_test, relay_test, v2_new_thread, comparison
  and the same kind of finished test block) move verbatim into the same archive. Anything not on
  that list stays, including events, robot_relay, test_acks and primary_backup_acceptance.
* Owner instruction / policy / hold records on the launch queue move only when the record itself is
  explicitly superseded, cancelled, replaced, or already marked history_only with archived_to.
  Live policies read by queue_readiness stay. Ambiguous records stay. Items, budgets and receipts
  are not decided by this rule.

The same is done for every project in projects/projects.json under its own folder.
Run: python3 scripts/trim_service_files.py .            (dry run, prints what would move)
     python3 scripts/trim_service_files.py . --write    (writes; commit under the canon lock)
     python3 scripts/trim_service_files.py . --root-only --write (root lock only; no project writes)
     python3 scripts/trim_service_files.py . --relay-only --write (same event-receipt commit)
"""
import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import canon_lock  # noqa: E402

KEEP_SECTIONS = 5
KEEP_COMPLETED = 10
KEEP_DONE = 10
SUBMITTED_DAYS = 7
KEEP_RELAY_EVENTS = 100
RELAY_DAYS = 30
RELAY_REPORT = "reports/topview-event-wake.json"
RELAY_ARCHIVE = "archive/reports/topview-event-wake-archive.json"
RELAY_TERMINAL = frozenset({"submitted", "launched", "completed", "success", "done",
                            "no_update", "stale", "invalid_timestamp", "skipped", "processed", "handled"})
CHECKPOINT = "reports/current-work-checkpoint.md"
REGISTER = "work-resume-register.json"
QUEUE = "ops/topview-launch-queue.json"
CHECKPOINT_ARCHIVE = "archive/checkpoints/current-work-checkpoint-archive.md"
REGISTER_ARCHIVE = "archive/work-resume-register-archive.json"
QUEUE_ARCHIVE = "archive/ops/topview-launch-queue-archive.json"
POINTER = "Более ранние записи — `{}` (перенесены дословно при недельной чистке)."
FINISHED_WORK = re.compile(r"^(completed|done|closed|cancelled|superseded)", re.I)
TERMINAL_ITEM = re.compile(r"^(superseded|cancelled)", re.I)
DONE_ITEM = re.compile(r"^(submitted|completed)$", re.I)
STUB_KEYS = ("id", "scene_id", "prompt_id", "canonical_block_label", "state", "task_id", "submitted_at",
             "completed_at", "canonical_prompt_sha256", "normalized_prompt_sha256")
OWNER_RECORD_RE = re.compile(r"^owner_(instruction|policy|hold)_")
# queue_readiness.py reads these as the live launch order. Never archive them from a nested word.
PROTECTED_OWNER_KEYS = frozenset({
    "owner_policy_20261108_t369u",
    "owner_policy_20261109_t422u",
    "owner_policy_20261113_t601u",
})
LIVE_OWNER_EFFECTS = frozenset({
    "music_requires_owner_consent",
    "tatooine_chain_first",
    "explicit_front_order",
})
TERMINAL_EFFECT_RE = re.compile(r"^(superseded|cancelled|canceled|replaced|obsolete)\b", re.I)
TERMINAL_OWNER_STATUS = frozenset({"superseded", "cancelled", "canceled", "replaced", "obsolete"})
# Finished wake-journal test blocks. Not receipts, not the live robot_relay config.
WAKE_TEST_SECTIONS = (
    "slack_test", "slack_test_ack", "v2_new_thread", "relay_test", "comparison",
    "previous_tests", "robot_relay_bridge",
)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_time(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        t = datetime.fromisoformat(value.strip().replace("Z", "+00:00").replace(" ", "T"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


# ----------------------------------------------------------------------------- checkpoint
def split_sections(text):
    """Top-level '# ' sections; a preamble before the first one stays with the live file."""
    lines = text.splitlines(keepends=True)
    pre, sections, cur = [], [], None
    for line in lines:
        if line.startswith("# "):
            cur = [line]
            sections.append(cur)
        elif cur is None:
            pre.append(line)
        else:
            cur.append(line)
    return "".join(pre), ["".join(s) for s in sections]


def trim_checkpoint(text, archive_text, archive_rel, keep=KEEP_SECTIONS, protected_anchors=()):
    pre, sections = split_sections(text)
    pointer = POINTER.format(archive_rel)
    sections = [s.replace(pointer, "").rstrip() + "\n" for s in sections]
    if len(sections) <= keep:
        return None
    live = [s for i, s in enumerate(sections) if i < keep or s.splitlines()[0] in protected_anchors]
    old = [s for i, s in enumerate(sections) if i >= keep and s.splitlines()[0] not in protected_anchors]
    if not old:
        return None
    body_live = "\n".join(live).rstrip()
    if body_live.endswith("\n---"):
        body_live = body_live[:-4].rstrip()
    live_text = pre + body_live + "\n\n---\n\n" + pointer + "\n"
    head = "# Архив контрольных точек\n\nНовые сверху. Дословные разделы, убранные из `{}` при недельной чистке.\n\n".format(
        CHECKPOINT)
    body = archive_text[len(head):] if archive_text.startswith(head) else archive_text
    new_archive = head + "\n".join(old).rstrip() + "\n\n" + body.lstrip()
    return live_text, new_archive.rstrip() + "\n", len(old)


# ----------------------------------------------------------------------------- register
def work_time(w):
    for k in ("completed_at", "updated_at", "verified_at", "last_updated_at"):
        t = parse_time(w.get(k))
        if t:
            return t
    return datetime.min.replace(tzinfo=timezone.utc)


def trim_register(reg, archive, archive_rel=REGISTER_ARCHIVE, keep=KEEP_COMPLETED, keep_done=KEEP_DONE):
    active = reg.get("active_work") or []
    done = [w for w in active if FINISHED_WORK.match(str(w.get("status") or ""))]
    long_done = [w for w in active if w not in done and any(
        isinstance(w.get(key), list) and len(w[key]) > keep_done for key in ("done", "completed"))]
    if not done and not long_done and len(reg.get("completed_work") or []) <= keep:
        return None
    reg = dict(reg)
    trimmed = []
    live = []
    for w in active:
        if w in done:
            continue
        if w in long_done:
            w = dict(w)
            for key in ("done", "completed"):
                if not isinstance(w.get(key), list) or len(w[key]) <= keep_done:
                    continue
                cut = len(w[key]) - keep_done
                trimmed.append({"work_id": w.get("work_id"), key: w[key][:cut]})
                w[key] = w[key][cut:]
                w[key + "_archived_points"] = int(w.get(key + "_archived_points") or 0) + cut
                w[key + "_archive"] = archive_rel
        live.append(w)
    reg["active_work"] = live
    completed = sorted(done + list(reg.get("completed_work") or []), key=work_time, reverse=True)
    reg["completed_work"], old = completed[:keep], completed[keep:]
    archive = dict(archive or {"schema_version": 1, "description": "Finished work moved from " + REGISTER +
                                 " at the weekly cleanup; newest first. History only, not live work.",
                                 "completed_work": []})
    archive["completed_work"] = old + list(archive.get("completed_work") or [])
    if trimmed:
        archive["trimmed_done"] = trimmed + list(archive.get("trimmed_done") or [])
    if old:
        reg["archived_completed_work"] = archive_rel
    return reg, archive, len(done), len(old) + len(trimmed)


# ----------------------------------------------------------------------------- queue
def item_time(it):
    for k in ("completed_at", "submitted_at", "claimed_at"):
        t = parse_time(it.get(k))
        if t:
            return t
    claim = it.get("claim") if isinstance(it.get("claim"), dict) else {}
    return parse_time(claim.get("claimed_at"))


def movable(it, now, days=SUBMITTED_DAYS):
    st = str(it.get("state") or "")
    if TERMINAL_ITEM.match(st):
        return True
    if DONE_ITEM.match(st):
        t = item_time(it)
        return t is not None and now - t > timedelta(days=days)
    return False


def trim_queue(queue, archive, now, archive_rel=QUEUE_ARCHIVE, days=SUBMITTED_DAYS,
               active_task_ids=(), terminal_task_ids=()):
    items = queue.get("items") or []
    old = [it for it in items if movable(it, now, days) and it.get("task_id") not in active_task_ids
           and (it.get("state") != "submitted" or it.get("task_id") in terminal_task_ids)]
    if not old:
        return None
    queue = dict(queue)
    queue["items"] = [it for it in items if it not in old]
    stubs = [{k: it.get(k) for k in STUB_KEYS if it.get(k) is not None} for it in old]
    queue["archived_items"] = stubs + list(queue.get("archived_items") or [])
    queue["archived_items_file"] = archive_rel
    archive = dict(archive or {"schema_version": 1, "description": "Finished launch-queue items moved verbatim "
                                 "at the weekly cleanup; newest first. History only: never relaunch from here.",
                                 "items": []})
    archive["items"] = old + list(archive.get("items") or [])
    return queue, archive, len(old)


# ----------------------------------------------------------------------------- relay receipts
def relay_completed_at(event, now):
    """Ambiguous or unfinished records stay live regardless of age or file size."""
    if not isinstance(event, dict) or not isinstance(event.get("event_id"), str) or not event["event_id"]:
        return None
    if (event.get("retryable") is not False or not isinstance(event.get("outcome"), str)
            or event["outcome"] not in RELAY_TERMINAL):
        return None
    checked = parse_time(event.get("checked_at"))
    return checked if checked is not None and checked <= now else None


def trim_relay_events(data, archive, now, archive_rel=RELAY_ARCHIVE,
                      keep=KEEP_RELAY_EVENTS, days=RELAY_DAYS):
    """Return live/archive/count, or None. Never infer successful processing from arbitrary text."""
    if keep < 0 or days < 0:
        raise ValueError("Relay retention bounds must be non-negative")
    if not isinstance(data, dict) or not isinstance(data.get("events", []), list):
        raise ValueError("Invalid Relay receipt report; refusing to archive")
    events = data.get("events", [])
    index = data.get("archived_event_ids", [])
    if not isinstance(index, list) or any(not isinstance(x, str) or not x for x in index):
        raise ValueError("Invalid archived_event_ids; refusing to replace the dedup index")
    completed = {i: relay_completed_at(e, now) for i, e in enumerate(events)}
    # If any attempt for an ID is unresolved, keep all its versions and do not mark it archived.
    protected = {e.get("event_id") for i, e in enumerate(events)
                 if isinstance(e, dict) and isinstance(e.get("event_id"), str) and completed[i] is None}
    eligible = sorted((i for i, t in completed.items() if t is not None
                       and events[i]["event_id"] not in protected),
                      key=lambda i: (completed[i], i), reverse=True)
    cutoff = now - timedelta(days=days)
    retained = {i for i in eligible[:keep] if completed[i] >= cutoff}
    moving = set(eligible) - retained
    if not moving:
        return None
    old = [events[i] for i in eligible if i in moving]
    archive = archive if archive is not None else {"schema_version": 1,
        "description": "Completed Relay event receipts, preserved verbatim. History only; never relaunch.",
        "events": []}
    if not isinstance(archive, dict) or not isinstance(archive.get("events"), list):
        raise ValueError("Invalid Relay archive; refusing to overwrite it")
    archived = list(archive["events"])
    # A crash after writing the archive but before the live file must be safe to retry.
    # Preserve differing versions of the same ID; suppress only identical records.
    additions = []
    for event in old:
        if event not in archived and event not in additions:
            additions.append(event)
    live = dict(data)
    live.update(events=[e for i, e in enumerate(events) if i not in moving],
                archived_event_ids=sorted(set(index) | {e["event_id"] for e in old}),
                events_archive=archive_rel)
    return live, dict(archive, events=additions + archived), len(old)


def run_relay(root, write, now):
    path = Path(root) / RELAY_REPORT
    if not path.is_file():
        return []
    data = load_json(path)
    # Ordinary cycles don't load the growing archive at all.
    if trim_relay_events(data, None, now) is None:
        return []
    arch = Path(root) / RELAY_ARCHIVE
    res = trim_relay_events(data, load_json(arch) if arch.is_file() else None, now)
    if write:
        dump_relay_json(arch, res[1])  # persist original details before removing them from the live file
        dump_relay_json(path, res[0])
    return ["seregius: Relay → архив {} событий; точные ID сохранены".format(res[2])]


def dump_relay_json(path, data):
    """Replace complete files atomically; an interrupted archive write must not truncate history."""
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


def classify_owner_record(key, value):
    """'move', 'keep', 'ambiguous', or None when the key is not an owner instruction/policy/hold.

    A nested word such as "superseded" inside a quote is not a mark. Only the record's own
    effect/status/superseded_by/replaced_by/cancelled_by, or an explicit history_only+archived_to stub.
    """
    if not isinstance(key, str) or not OWNER_RECORD_RE.match(key):
        return None
    if key in PROTECTED_OWNER_KEYS:
        return "keep"
    if not isinstance(value, dict):
        return "ambiguous"
    effect = value.get("effect")
    if isinstance(effect, str) and effect in LIVE_OWNER_EFFECTS:
        return "keep"
    if isinstance(effect, str) and TERMINAL_EFFECT_RE.match(effect.strip()):
        return "move"
    for field in ("state", "status"):
        raw = value.get(field)
        if isinstance(raw, str) and raw.strip().lower() in TERMINAL_OWNER_STATUS:
            return "move"
    for field in ("superseded_by", "replaced_by", "cancelled_by"):
        raw = value.get(field)
        if isinstance(raw, str) and raw.strip():
            return "move"
    if value.get("history_only") is True and isinstance(value.get("archived_to"), str) and value["archived_to"].strip():
        return "move"
    return "ambiguous"


def _store_verbatim(bucket, versions, key, value):
    """Keep the previous body if a different one was already archived under the same key."""
    if key in bucket and bucket[key] != value:
        previous = {"key": key, "value": bucket[key]}
        if previous not in versions:
            versions.append(previous)
    bucket[key] = value


def trim_owner_records(queue, archive):
    """Move explicitly retired owner records. Returns a result dict, or None when nothing moves.

    `ambiguous` is always the keys left in place for the owner to judge. Items are not touched.
    """
    if not isinstance(queue, dict):
        raise ValueError("Invalid launch queue; refusing to archive owner records")
    moving, ambiguous = {}, []
    for key, value in queue.items():
        verdict = classify_owner_record(key, value)
        if verdict == "move":
            moving[key] = value
        elif verdict == "ambiguous":
            ambiguous.append(key)
    if not moving:
        return {"queue": queue, "archive": archive, "moved": [], "ambiguous": sorted(ambiguous)}
    live = dict(queue)
    for key in moving:
        del live[key]
    archive = dict(archive or {"schema_version": 1,
        "description": "Finished launch-queue items and retired owner records, verbatim. History only.",
        "items": []})
    records = dict(archive.get("owner_records") or {})
    versions = list(archive.get("owner_record_versions") or [])
    for key, value in moving.items():
        _store_verbatim(records, versions, key, value)
    archive["owner_records"] = records
    if versions:
        archive["owner_record_versions"] = versions
    return {"queue": live, "archive": archive, "moved": sorted(moving), "ambiguous": sorted(ambiguous)}


def trim_wake_test_sections(data, archive, archive_rel=RELAY_ARCHIVE):
    """Move the named old test sections. Receipts and unnamed fields stay. None if nothing moves."""
    if not isinstance(data, dict):
        raise ValueError("Invalid wake journal; refusing to archive test sections")
    moving = {key: data[key] for key in WAKE_TEST_SECTIONS if key in data}
    if not moving:
        return None
    live = dict(data)
    for key in moving:
        del live[key]
    archive = dict(archive or {"schema_version": 1,
        "description": "Completed Relay receipts and old wake-journal test sections, verbatim. History only.",
        "events": []})
    if not isinstance(archive.get("events", []), list):
        raise ValueError("Invalid wake archive; refusing to overwrite it")
    sections = dict(archive.get("test_sections") or {})
    versions = list(archive.get("test_section_versions") or [])
    for key, value in moving.items():
        _store_verbatim(sections, versions, key, value)
    archive["test_sections"] = sections
    if versions:
        archive["test_section_versions"] = versions
    live["test_sections_archive"] = archive_rel
    return live, archive, sorted(moving)


def run_wake_tests(root, write):
    path = Path(root) / RELAY_REPORT
    if not path.is_file():
        return []
    data = load_json(path)
    arch = Path(root) / RELAY_ARCHIVE
    res = trim_wake_test_sections(data, load_json(arch) if arch.is_file() else None)
    if not res:
        return []
    if write:
        dump_relay_json(arch, res[1])
        dump_relay_json(path, res[0])
    return ["seregius: тестовые разделы журнала → архив {}".format(", ".join(res[2]))]


# ----------------------------------------------------------------------------- driver
def bases(root):
    yield "", root
    reg = root / "projects" / "projects.json"
    if reg.is_file():
        for p in load_json(reg).get("projects", []):
            pid = p.get("id")
            if pid and pid != "seregius" and (root / "projects" / pid).is_dir():
                yield pid, root / "projects" / pid


def run(root, write=False, now=None, relay_only=False, root_only=False, skip_held_locks=False):
    now = now or datetime.now(timezone.utc)
    root = Path(root)
    report = run_relay(root, write, now)
    if relay_only:
        return report
    report.extend(run_wake_tests(root, write))
    for pid, base in bases(root):
        if root_only and pid:
            continue
        name = pid or "seregius"
        if skip_held_locks and canon_lock.is_held(canon_lock.read(root, pid or None), now):
            report.append("{}: замок занят, пропуск".format(name))
            continue
        prefix = "" if not pid else "projects/{}/".format(pid)
        cp = base / CHECKPOINT
        if cp.is_file():
            arch = base / CHECKPOINT_ARCHIVE
            reg_path = base / REGISTER
            reg = load_json(reg_path) if reg_path.is_file() else {}
            protected = {(w.get("recovery") or {}).get("checkpoint", {}).get("anchor")
                         for w in reg.get("active_work", []) + ([reg["idle_state"]] if isinstance(reg.get("idle_state"), dict) else [])
                         if not FINISHED_WORK.match(str(w.get("status") or ""))}
            res = trim_checkpoint(cp.read_text(encoding="utf-8"),
                                  arch.read_text(encoding="utf-8") if arch.is_file() else "", prefix + CHECKPOINT_ARCHIVE,
                                  protected_anchors=protected)
            if res:
                report.append("{}: checkpoint → архив {} разделов".format(name, res[2]))
                if write:
                    arch.parent.mkdir(parents=True, exist_ok=True)
                    arch.write_text(res[1], encoding="utf-8")
                    cp.write_text(res[0], encoding="utf-8")
        rp = base / REGISTER
        if rp.is_file():
            arch = base / REGISTER_ARCHIVE
            res = trim_register(load_json(rp), load_json(arch) if arch.is_file() else None, prefix + REGISTER_ARCHIVE)
            if res:
                report.append("{}: register — {} законченных из active_work, {} записей в архив".format(name, res[2], res[3]))
                if write:
                    if res[3]:
                        dump_json(arch, res[1])
                    dump_json(rp, res[0])
        qp = base / QUEUE
        if qp.is_file():
            arch = base / QUEUE_ARCHIVE
            tm_path, tv_path = base / "topview-task-map.json", base / "topview-status.json"
            tm = load_json(tm_path) if tm_path.is_file() else {}
            tv = load_json(tv_path) if tv_path.is_file() else {}
            active_ids = {tid for ids in tm.get("active_by_scene", {}).values() for tid in ids}
            active_ids.update(t.get("task_id") for t in tv.get("active_tasks", []))
            terminal_ids = {t.get("task_id") for t in tm.get("processed_tasks", [])
                            if t.get("final_status") in ("success", "fail", "failed", "cancelled", "canceled")}
            queue = load_json(qp)
            stored = load_json(arch) if arch.is_file() else None
            res = trim_queue(queue, stored, now, prefix + QUEUE_ARCHIVE,
                             active_task_ids=active_ids, terminal_task_ids=terminal_ids)
            if res:
                queue, stored = res[0], res[1]
                report.append("{}: очередь → архив {} пунктов".format(name, res[2]))
            owner = trim_owner_records(queue, stored)
            if owner["moved"]:
                queue, stored = owner["queue"], owner["archive"]
                report.append("{}: указания владельца → архив {}".format(name, ", ".join(owner["moved"])))
            if owner["ambiguous"]:
                report.append("{}: указания без явной отмены, оставлены: {}".format(
                    name, ", ".join(owner["ambiguous"])))
            if write and (res or owner["moved"]):
                dump_json(arch, stored if stored is not None else owner["archive"])
                dump_json(qp, queue)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("repo")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--relay-only", action="store_true", help="only Relay receipts; no queue or project changes")
    ap.add_argument("--root-only", action="store_true", help="root files only; never write other projects")
    ap.add_argument("--skip-held-locks", action="store_true",
                    help="do not trim a project whose canon lock is still held")
    a = ap.parse_args()
    rep = run(a.repo, a.write, relay_only=a.relay_only, root_only=a.root_only,
              skip_held_locks=a.skip_held_locks)
    print("\n".join(rep) if rep else "нечего переносить")


if __name__ == "__main__":
    main()
