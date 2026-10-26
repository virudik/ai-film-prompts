#!/usr/bin/env python3
"""Owner-panel robot, phase 3 (owner approval 17.10.2026): site buttons that do not edit the master.

  queue_up / queue_down     «▲ выше» / «▼ ниже»  – swap the scene with its neighbour in the launch order
  queue_remove              «✕ убрать»           – hold every not-yet-launched item of the scene
  queue_add                 «в очередь»          – restore a held scene / release a scene waiting for the
                                                    owner; otherwise a task for an agent to package it
  owner_task                «✎ Задача»           – goes to the inbox ops/owner-tasks.json for Claude / ChatGPT
  ref_feedback ok|redraw    у референсов          – references/reference-review.json; «перерисовать» also
                                                    becomes an inbox task for ChatGPT

Back-flow: when an agent closes an inbox task (done / needs_owner / cancelled) the Supabase row gets the
same state and the agent's result text, so the owner sees it on the site.

Safety:
- Queue edits only when the canon lock (ops/canon-lock.json) is free; otherwise the row waits and its
  reason is shown on the site. Only `priority`, `state` and a few new `*_site*` fields of items change;
  every other field (including ones other writers add later) is kept byte-for-byte via json round-trip.
- Never launches a generation, never touches video-prompts.md, never approves anything.
- commit → push → read-back → ONLY THEN Supabase acknowledgement. A rejected push = someone else wrote:
  re-read main and redo from scratch.

usage: robot_site_actions.py [--root DIR] [--no-sync] [--dry-run]
env:   SUPABASE_SERVICE_ROLE_KEY (secret). Never prints keys or owner notes.
"""
import argparse
import copy
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import canon_lock                          # noqa: E402
import process_owner_decisions as pod      # noqa: E402
import projects as prj                     # noqa: E402
from operation_journal import atomic_json  # noqa: E402

QUEUE = "ops/topview-launch-queue.json"
INBOX = "ops/owner-tasks.json"
INBOX_ARCHIVE = "archive/ops/owner-tasks-archive.json"
REF_REVIEW = "references/reference-review.json"
LOCK = canon_lock.LOCK
QUEUE_ACTIONS = ("queue_up", "queue_down", "queue_remove", "queue_add")
SITE_ACTIONS = QUEUE_ACTIONS + ("owner_task", "ref_feedback")
INBOX_CLAIM = "site-inbox:"
# Items that are already launched or finished are never moved: only the waiting part of the queue changes.
FINAL_STATES = {"submitted", "cancelled_owner", "completed", "held_owner_site"}
HELD = "held_owner_site"
INBOX_DONE = {"done": "applied", "needs_owner": "needs_owner", "cancelled": "superseded"}
KEEP_CLOSED_DAYS = 14
POLICY_PREFIX = ("OWNER SITE ORDER (18.10.2026): кнопки владельца на сайте (owner_site_actions) меняют priority; "
                 "порядок по priority важнее текстового порядка ниже. ")
MAX_ATTEMPTS = 4
MSK = timezone(timedelta(hours=3))


def iso(dt):
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def msk(value):
    dt = canon_lock.parse(value)
    return dt.astimezone(MSK).strftime("%d.%m %H:%M МСК") if dt else str(value)


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def read_json(root, rel, default):
    p = Path(root) / rel
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return copy.deepcopy(default)


EMPTY_INBOX = {"schema_version": 1, "rules": "ops/OWNER-TASKS.md", "updated_at": None, "tasks": []}
EMPTY_REVIEW = {"schema_version": 1,
                "rules": "Отметки владельца у референсов (сайт, кнопки «подходит» / «перерисовать»). "
                         "Последняя запись по пути — действующая. Пишет робот кнопок; «перерисовать» "
                         "дополнительно становится задачей ChatGPT в ops/owner-tasks.json.",
                "updated_at": None, "reviews": []}


# --------------------------------------------------------------------------- queue logic (pure)
def _is_waiting(item):
    st = str(item.get("state") or "")
    return st not in FINAL_STATES and not st.startswith("superseded") and not st.startswith("cancelled")


def scene_order(queue):
    """Scenes of the waiting part of the queue, by their lowest priority."""
    band = {}
    for it in queue.get("items", []):
        if _is_waiting(it):
            sid = int(it.get("scene_id"))
            p = float(it.get("priority") or 0)
            band[sid] = min(band.get(sid, p), p)
    return [s for s, _ in sorted(band.items(), key=lambda kv: (kv[1], kv[0]))], band


def _deps_note(queue, sid):
    ids = {it.get("id") for it in queue.get("items", []) if int(it.get("scene_id")) == sid and _is_waiting(it)}
    deps = sorted({d for it in queue.get("items", []) if it.get("id") in ids
                   for d in (it.get("depends_on_submitted") or []) if d not in ids})
    return (" Зависит от " + ", ".join(deps[:4]) + ": запустится только после них.") if deps else ""


def _swap_scenes(queue, a, b, band):
    for it in queue.get("items", []):
        if not _is_waiting(it):
            continue
        sid = int(it.get("scene_id"))
        if sid not in (a, b):
            continue
        src, dst = (band[a], band[b]) if sid == a else (band[b], band[a])
        new = round(dst + (float(it.get("priority") or 0) - src), 3)
        it["priority"] = int(new) if new == int(new) else new
    order = queue.get("new_scene_order")
    if isinstance(order, list) and a in order and b in order:
        i, j = order.index(a), order.index(b)
        order[i], order[j] = order[j], order[i]


def apply_queue_action(queue, action, sid):
    """Mutates queue. Returns (outcome, note): outcome in applied | noop | inbox."""
    order, band = scene_order(queue)
    if action in ("queue_up", "queue_down"):
        if sid not in order:
            return "noop", f"Сцены {sid} нет среди ожидающих запуска; порядок не менялся."
        i = order.index(sid)
        j = i - 1 if action == "queue_up" else i + 1
        if j < 0 or j >= len(order):
            return "noop", f"Сцена {sid} уже {'первая' if j < 0 else 'последняя'} в очереди."
        other = order[j]
        _swap_scenes(queue, sid, other, band)
        where = "выше" if action == "queue_up" else "ниже"
        return "applied", f"Сцена {sid} поставлена {where} сцены {other}." + _deps_note(queue, sid)
    items = [it for it in queue.get("items", []) if int(it.get("scene_id")) == sid]
    if action == "queue_remove":
        waiting = [it for it in items if _is_waiting(it)]
        if not waiting:
            return "noop", f"У сцены {sid} нет пунктов, ожидающих запуска; запущенные задачи кнопка не трогает."
        for it in waiting:
            it["previous_state_before_site_hold"] = it.get("state")
            it["state"] = HELD
        return "applied", f"Сцена {sid} убрана из очереди ({len(waiting)} п.); вернуть — кнопка «в очередь»."
    # queue_add
    held = [it for it in items if it.get("state") == HELD]
    if held:
        for it in held:
            it["state"] = it.pop("previous_state_before_site_hold", None) or "waiting_for_slot"
        return "applied", f"Сцена {sid} возвращена в очередь ({len(held)} п.)." + _deps_note(queue, sid)
    gated = [it for it in items if it.get("state") == "blocked_owner_decision"]
    if gated:
        for it in gated:
            it["previous_state_before_site_add"] = it.get("state")
            it["state"] = "waiting_for_slot"
        return "applied", (f"Сцена {sid}: ваше решение «в очередь» записано, {len(gated)} п. ждут свободного слота "
                           "(только безлимит, 0 кредитов; перед запуском сверяется текст промта)." + _deps_note(queue, sid))
    if any(_is_waiting(it) for it in items):
        return "noop", f"Сцена {sid} уже в очереди." + _deps_note(queue, sid)
    return "inbox", f"Сцену {sid} нужно подготовить к запуску (пакет промта и картинок): передано агенту."


def log_queue(queue, row, outcome, note, stamp):
    log = queue.setdefault("owner_site_actions", [])
    log.append({"at": stamp, "decision_id": row["id"], "action": row["action"], "scene_id": row.get("scene_id"),
                "outcome": outcome, "note": note})
    del log[:-100]
    pol = queue.get("selection_policy")
    if isinstance(pol, str) and not pol.startswith("OWNER SITE ORDER"):
        queue["selection_policy"] = POLICY_PREFIX + pol
    queue["updated_at"] = stamp


# --------------------------------------------------------------------------- inbox logic (pure)
def inbox_task(row, *, to, text, source, stamp):
    return {"id": row["id"], "created_at": row.get("created_at") or stamp, "scene_id": row.get("scene_id"),
            "to": to, "source": source, "text": text, "status": "open", "taken_by": None, "taken_at": None,
            "result": None, "result_commit": None, "closed_at": None}


def parse_ref_note(note):
    path, _, comment = str(note or "").partition(" | ")
    return path.strip(), comment.strip()


def prune_inbox(inbox, open_ids, now, archive):
    """Archive exact closed records before removal, including tasks with no Supabase row."""
    if not isinstance(archive, dict) or not isinstance(archive.get("tasks"), list):
        raise ValueError("Invalid owner task archive; keep inbox unchanged")
    saved = {}
    for task in archive["tasks"]:
        if not task.get("id") or task["id"] in saved:
            raise ValueError("Invalid/duplicate task ID in archive")
        saved[task["id"]] = task
    keep = []
    for t in inbox.get("tasks", []):
        closed = canon_lock.parse(t.get("closed_at"))
        if t.get("status") in INBOX_DONE and closed and closed < now - timedelta(days=KEEP_CLOSED_DAYS) \
                and t.get("id") not in open_ids:
            tid = t.get("id")
            if not tid or (tid in saved and saved[tid] != t):
                raise ValueError("Task archive conflict; fresh-read before retry")
            if tid not in saved:
                archive["tasks"].append(copy.deepcopy(t))
                saved[tid] = t
            continue
        keep.append(t)
    inbox["tasks"] = keep


def plan(rows, files, now):
    """Pure planning. rows = open Supabase rows; files = {QUEUE, INBOX, REF_REVIEW, LOCK} dicts.
    Returns (new_files, acks): new_files only for files that change; acks = [(row, status, note)]
    to send AFTER a verified push (or at once when nothing has to be written)."""
    stamp = iso(now)
    queue, inbox, review = (copy.deepcopy(files[QUEUE]), copy.deepcopy(files[INBOX]), copy.deepcopy(files[REF_REVIEW]))
    lock = files.get(LOCK) or {}
    before = {QUEUE: dumps(files[QUEUE]), INBOX: dumps(files[INBOX]), REF_REVIEW: dumps(files[REF_REVIEW])}
    archive = copy.deepcopy(files.get(INBOX_ARCHIVE, {"schema_version": 1, "tasks": []}))
    before_archive = dumps(archive)
    acks = []
    in_inbox = {t.get("id"): t for t in inbox.get("tasks", [])}
    lock_busy = canon_lock.is_held(lock, now)

    for row in sorted(rows, key=lambda r: str(r.get("created_at") or "")):
        action, status = row.get("action"), row.get("status")
        if action not in SITE_ACTIONS:
            continue
        # ---- back-flow: an agent closed the task in the inbox
        if status == "in_progress" and str(row.get("result_note") or "").startswith(INBOX_CLAIM):
            t = in_inbox.get(row["id"])
            if t and t.get("status") in INBOX_DONE:
                who = t.get("taken_by") or "агент"
                res = (t.get("result") or "").strip() or "без комментария"
                tail = f" Коммит {str(t['result_commit'])[:7]}." if t.get("result_commit") else ""
                acks.append((row, INBOX_DONE[t["status"]], f"{who}: {res}{tail}"[:1000]))
            elif t and t.get("status") == "taken":
                note = f"{INBOX_CLAIM} в работе у {t.get('taken_by') or 'агента'} с {msk(t.get('taken_at'))}"
                if row.get("result_note") != note:
                    acks.append((row, "in_progress", note))
            continue
        if status != "pending":
            continue
        sid = row.get("scene_id")
        pid = prj.project_of_row(row)              # projects/README.md: tasks of every project share this inbox
        if action in QUEUE_ACTIONS and pid != prj.ROOT_ID:
            continue                               # another project's queue: phase 4 (robot_project_actions.py)
        if action == "owner_task":
            to = row.get("value") if row.get("value") in ("claude", "chatgpt", "any") else "any"
            if row["id"] not in in_inbox:
                t = inbox_task(row, to=to, text=prj.strip_note_tag(row.get("note")), source="site", stamp=stamp)
                if pid != prj.ROOT_ID:
                    t["project"] = pid
                inbox.setdefault("tasks", []).append(t)
                in_inbox[row["id"]] = t
            who = {"claude": "Claude", "chatgpt": "ChatGPT", "any": "Claude или ChatGPT"}[to]
            where = "" if pid == prj.ROOT_ID else f", проект {pid}"
            acks.append((row, "in_progress", f"{INBOX_CLAIM} задача в ops/owner-tasks.json, ждёт исполнителя ({who}{where})"))
        elif action == "ref_feedback":
            path, comment = parse_ref_note(row.get("note"))
            verdict = row.get("value")
            if verdict not in ("ok", "redraw") or not path:
                acks.append((row, "needs_owner", "Не понял отметку референса: нет пути к картинке или вердикта."))
                continue
            if not any(r.get("id") == row["id"] for r in review.get("reviews", [])):
                review.setdefault("reviews", []).append({"id": row["id"], "at": stamp, "path": path, "scene_id": sid,
                                                         "verdict": verdict, "comment": comment or None,
                                                         **({"project": pid} if pid != prj.ROOT_ID else {})})
                review["updated_at"] = stamp
            if verdict == "ok":
                acks.append((row, "applied", f"Отметка «подходит» записана в {REF_REVIEW}."))
            else:
                if row["id"] not in in_inbox:
                    text = f"Перерисовать референс {path}" + (f": {comment}" if comment else "") + \
                           " (по правилам manifest: PNG + SHA + миниатюра, слот в промте)."
                    t = inbox_task(row, to="chatgpt", text=text, source="ref_feedback", stamp=stamp)
                    if pid != prj.ROOT_ID:
                        t["project"] = pid
                    inbox.setdefault("tasks", []).append(t)
                    in_inbox[row["id"]] = t
                acks.append((row, "in_progress", f"{INBOX_CLAIM} перерисовка передана ChatGPT (ops/owner-tasks.json)"))
        elif action in QUEUE_ACTIONS:
            if sid is None:
                acks.append((row, "needs_owner", "Не указан номер сцены."))
                continue
            if lock_busy:
                note = f"Ждёт: канон занят ({lock.get('holder')}) до {msk(lock.get('expires_at'))}; применю сразу после."
                if row.get("result_note") != note:
                    acks.append((row, "pending", note))
                continue
            outcome, note = apply_queue_action(queue, action, int(sid))
            log_queue(queue, row, outcome, note, stamp)
            if outcome == "inbox":
                if row["id"] not in in_inbox:
                    t = inbox_task(row, to="any", source="queue_add", stamp=stamp,
                                   text=f"Подготовить сцену {sid} к запуску и поставить её в очередь "
                                        f"(кнопка владельца «в очередь» на сайте). Только безлимит, 0 кредитов.")
                    inbox.setdefault("tasks", []).append(t)
                    in_inbox[row["id"]] = t
                acks.append((row, "in_progress", f"{INBOX_CLAIM} {note}"))
            else:
                acks.append((row, "applied", note))

    open_ids = {r["id"] for r in rows if r.get("status") in ("pending", "in_progress")}
    prune_inbox(inbox, open_ids, now, archive)
    new_files = {}
    # Archive first, then compact inbox; both are published in the same CAS commit.
    if dumps(archive) != before_archive:
        new_files[INBOX_ARCHIVE] = dumps(archive)
    for name, obj in ((QUEUE, queue), (INBOX, inbox), (REF_REVIEW, review)):
        text = dumps(obj)
        if text != before[name]:
            if name in (INBOX,):
                obj["updated_at"] = stamp
                text = dumps(obj)
            new_files[name] = text
    return new_files, acks


# --------------------------------------------------------------------------- io
class SupabaseStore:
    def list_open(self):
        return pod.api("GET", {"select": "id,created_at,scene_id,action,task_id,value,note,status,result_note",
                               "action": "in.(" + ",".join(SITE_ACTIONS) + ")",
                               "status": "in.(pending,in_progress)", "order": "created_at.asc",
                               "limit": str(pod.MAX_ROWS)})

    def mark(self, row, to_status, note):
        return pod.patch_status(row["id"], row["status"], to_status, note)


def load_files(root):
    return {QUEUE: read_json(root, QUEUE, {}), INBOX: read_json(root, INBOX, EMPTY_INBOX),
            INBOX_ARCHIVE: read_json(root, INBOX_ARCHIVE, {"schema_version": 1, "tasks": []}),
            REF_REVIEW: read_json(root, REF_REVIEW, EMPTY_REVIEW), LOCK: read_json(root, LOCK, {})}


def run(root, store, git, *, now=None, sync=True, dry=False):
    root = Path(root)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if sync:
            git.sync()
        rows = store.list_open()
        files = load_files(root)
        if not files[QUEUE].get("items"):
            print("::warning title=robot-site-actions::launch queue missing or empty; queue buttons wait")
            rows = [r for r in rows if r.get("action") not in QUEUE_ACTIONS]
        new_files, acks = plan(rows, files, now or datetime.now(timezone.utc))
        summary = {"rows": len(rows), "files": sorted(new_files), "acks": len(acks)}
        print(json.dumps(summary, ensure_ascii=False))
        if dry:
            for row, st, note in acks:
                print(f"  {row['action']} сцена {row.get('scene_id')}: → {st}")
            return 0
        if new_files:
            for name, text in new_files.items():
                atomic_json(root / name, json.loads(text))
            what = ", ".join(sorted({r["action"] for r, _, _ in acks})) or "inbox"
            commit = git.commit(f"Owner panel robot: site buttons ({what})", sorted(new_files))
            if commit and not git.push():
                print(f"push rejected ({attempt}/{MAX_ATTEMPTS}); re-reading main and starting over")
                git.reset()
                if not sync:          # without a fresh fetch a retry would see its own unpushed edit
                    return 1
                continue
            if commit and not git.head_is_on_remote():
                print("::error title=robot-site-actions::commit not found on origin after push; no acknowledgement")
                return 1
        for row, st, note in acks:
            store.mark(row, st, note)
        return 0
    print("::error title=robot-site-actions::push rejected 4 times; buttons stay pending and are retried next run")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--no-sync", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip():
        print("::notice::Site actions not configured: missing SUPABASE_SERVICE_ROLE_KEY")
        return 0
    import robot_master_actions as rma   # Git helper (fetch/reset/commit/push as github-actions[bot])
    branch = os.environ.get("GITHUB_REF_NAME") or "main"
    return run(args.root, SupabaseStore(), rma.Git(args.root, branch), sync=not args.no_sync, dry=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
