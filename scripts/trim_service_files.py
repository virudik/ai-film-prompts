#!/usr/bin/env python3
"""Weekly trim of the agents' service files (owner decision 23.10.2026).

The checkpoint, the resume register and the launch queue only grow: every check appends to them.
This tool moves old, already finished entries VERBATIM into archive files and leaves the live files
short. Nothing is deleted and nothing live is touched:

* reports/current-work-checkpoint.md — keeps the newest KEEP_SECTIONS top-level sections (newest on
  top); older sections go on top of archive/checkpoints/current-work-checkpoint-archive.md.
* work-resume-register.json — finished entries leave `active_work` for `completed_work`;
  `completed_work` keeps the newest KEEP_COMPLETED, the rest go to archive/work-resume-register-archive.json;
  a live entry keeps the last KEEP_DONE points of its `done` list, older points go to the same archive.
* ops/topview-launch-queue.json — superseded / cancelled items, and submitted / completed items older
  than SUBMITTED_DAYS, go to archive/ops/topview-launch-queue-archive.json. A short stub of each stays in
  `archived_items` (id, scene, block label, state, task ID, prompt SHA), so duplicate checks and the
  site's «▶ запущена» badges keep working. Waiting, claimed, blocked and held items are never moved.

The same is done for every project in projects/projects.json under its own folder.
Run: python3 scripts/trim_service_files.py .            (dry run, prints what would move)
     python3 scripts/trim_service_files.py . --write    (writes; commit under the canon lock)
"""
import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

KEEP_SECTIONS = 5
KEEP_COMPLETED = 10
KEEP_DONE = 10
SUBMITTED_DAYS = 7
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


def trim_checkpoint(text, archive_text, archive_rel, keep=KEEP_SECTIONS):
    pre, sections = split_sections(text)
    pointer = POINTER.format(archive_rel)
    sections = [s.replace(pointer, "").rstrip() + "\n" for s in sections]
    if len(sections) <= keep:
        return None
    live, old = sections[:keep], sections[keep:]
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
    long_done = [w for w in active if w not in done and isinstance(w.get("done"), list) and len(w["done"]) > keep_done]
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
            cut = len(w["done"]) - keep_done
            trimmed.append({"work_id": w.get("work_id"), "done": w["done"][:cut]})
            w["done"] = w["done"][cut:]
            w["done_archived_points"] = int(w.get("done_archived_points") or 0) + cut
            w["done_archive"] = archive_rel
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


def trim_queue(queue, archive, now, archive_rel=QUEUE_ARCHIVE, days=SUBMITTED_DAYS):
    items = queue.get("items") or []
    old = [it for it in items if movable(it, now, days)]
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


# ----------------------------------------------------------------------------- driver
def bases(root):
    yield "", root
    reg = root / "projects" / "projects.json"
    if reg.is_file():
        for p in load_json(reg).get("projects", []):
            pid = p.get("id")
            if pid and pid != "seregius" and (root / "projects" / pid).is_dir():
                yield pid, root / "projects" / pid


def run(root, write=False, now=None):
    now = now or datetime.now(timezone.utc)
    report = []
    for pid, base in bases(Path(root)):
        name = pid or "seregius"
        prefix = "" if not pid else "projects/{}/".format(pid)
        cp = base / CHECKPOINT
        if cp.is_file():
            arch = base / CHECKPOINT_ARCHIVE
            res = trim_checkpoint(cp.read_text(encoding="utf-8"),
                                  arch.read_text(encoding="utf-8") if arch.is_file() else "", prefix + CHECKPOINT_ARCHIVE)
            if res:
                report.append("{}: checkpoint → архив {} разделов".format(name, res[2]))
                if write:
                    arch.parent.mkdir(parents=True, exist_ok=True)
                    cp.write_text(res[0], encoding="utf-8")
                    arch.write_text(res[1], encoding="utf-8")
        rp = base / REGISTER
        if rp.is_file():
            arch = base / REGISTER_ARCHIVE
            res = trim_register(load_json(rp), load_json(arch) if arch.is_file() else None, prefix + REGISTER_ARCHIVE)
            if res:
                report.append("{}: register — {} законченных из active_work, {} записей в архив".format(name, res[2], res[3]))
                if write:
                    dump_json(rp, res[0])
                    if res[3]:
                        dump_json(arch, res[1])
        qp = base / QUEUE
        if qp.is_file():
            arch = base / QUEUE_ARCHIVE
            res = trim_queue(load_json(qp), load_json(arch) if arch.is_file() else None, now, prefix + QUEUE_ARCHIVE)
            if res:
                report.append("{}: очередь → архив {} пунктов".format(name, res[2]))
                if write:
                    dump_json(qp, res[0])
                    dump_json(arch, res[1])
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("repo")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    rep = run(a.repo, a.write)
    print("\n".join(rep) if rep else "нечего переносить")


if __name__ == "__main__":
    main()
