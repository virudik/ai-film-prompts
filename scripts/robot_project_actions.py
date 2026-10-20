#!/usr/bin/env python3
"""Phase 4 of the owner-buttons robot: buttons of the OTHER projects (owner decision 20.10.2026).

The site writes the same Supabase owner_decisions rows for every project; rows of another project carry
value "project:<id>" (scene and queue buttons) or a task id recorded in projects/topview-projects.json
(«Брак», «Не ждать»). Phases 1–3 of sync-from-drive.yml skip those rows; this script applies them to the
project's own files only:

  queue_up / queue_down / queue_remove / queue_add  -> projects/<id>/ops/topview-launch-queue.json
                                                       (only while the project lock is free; same logic as
                                                       scripts/robot_site_actions.py)
  accept / redo / to_montage / tv_mark_status(result_bad) / tv_drop_task
                                                    -> projects/<id>/review-ledger.json (never while the
                                                       scene still has an active Topview task)
  in_film / scene_not_needed                        -> the scene leaves projects/<id>/video-prompts.md, its
                                                       number is reserved for ever; ledger as above

Text tasks and reference feedback of every project stay with phase 3 (shared inbox ops/owner-tasks.json).
Nothing here starts, approves or deletes a Topview task, spends credits or touches the film's root files.
Contradicting buttons for one scene -> needs_owner. Supabase is marked only after a verified push.

usage: robot_project_actions.py [--root DIR] [--dry-run] [--no-sync]
"""
import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import canon_lock                          # noqa: E402
import process_owner_decisions as pod      # noqa: E402
import projects as prj                     # noqa: E402
import robot_master_actions as rma         # noqa: E402
import robot_site_actions as rsa           # noqa: E402

DECISIONS = ("accept", "redo", "to_montage", "in_film", "scene_not_needed", "tv_mark_status", "tv_drop_task")
ACTIONS = rsa.QUEUE_ACTIONS + DECISIONS
INBOX = rsa.INBOX
MAX_ATTEMPTS = 4
VERDICT = {"accept": "accept", "to_montage": "accept", "in_film": "accept", "redo": "reject",
           "scene_not_needed": "close"}
SCENE_RE = r"^## Сцена {n}\b"


def iso(dt):
    return rsa.iso(dt)


def dumps(obj):
    return rsa.dumps(obj)


def token(row):
    if row["action"] == "tv_mark_status":
        return {"result_bad": "reject"}.get(row.get("value"))
    return VERDICT.get(row["action"])


# --------------------------------------------------------------------------- master edit (pure)
def plural(n, one, few, many):
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return one
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return few
    return many


def remove_scene(text, sid):
    """Remove scene `sid` from a project master: its section, its table-of-contents row; reserve the number.
    Returns the new text, or None when the scene is not in the master."""
    lines = text.split("\n")
    head = next((i for i, l in enumerate(lines) if re.match(SCENE_RE.format(n=sid), l)), None)
    if head is None:
        return None
    start = head
    while start > 0 and (lines[start - 1].strip() == "" or re.match(rf'<a\s+id=["\']scene-{sid}["\']', lines[start - 1].strip())):
        start -= 1
    end = next((i for i in range(head + 1, len(lines))
                if re.match(r"^## ", lines[i]) or re.match(r'<a\s+id=["\']scene-\d+["\']', lines[i].strip())), len(lines))
    out = lines[:start] + [""] + lines[end:]
    out = [l for l in out if not re.match(rf"^\|\s*{sid}\s*\|\s*\[", l)]
    new = "\n".join(out)
    new = re.sub(r"\n{3,}", "\n\n", new).rstrip("\n") + "\n"
    scenes = len(re.findall(r"^## Сцена \d+\b", new, re.M))
    prompts = len([l for l in new.splitlines() if l.strip().startswith("```")]) // 2
    new = re.sub(r"\*\*\d+ сцен[^·\n]*· \d+ полн[^*\n]*\*\*",
                 f"**{scenes} {plural(scenes, 'сцена', 'сцены', 'сцен')} к генерации/доработке · {prompts} "
                 f"{plural(prompts, 'полный текст', 'полных текста', 'полных текстов')} промта**", new, count=1)
    m = re.search(r"(?-i:Сцены)\s+([^\n]+?)\s+удалены из active master[^\n]*?зарезервированы[^\n]*", new)
    if m:
        ids = sorted(set(int(x) for x in re.findall(r"\d+", m.group(1))) | {sid})
        new = new[:m.start()] + f"Сцены {', '.join(map(str, ids))} удалены из active master; их Scene ID зарезервированы и не переиспользуются." + new[m.end():]
    else:
        anchor = re.search(r"^- \*\*Последняя полная синхронизация:\*\*[^\n]*\n", new, re.M)
        line = f"\nСцены {sid} удалены из active master; их Scene ID зарезервированы и не переиспользуются.\n"
        new = (new[:anchor.end()] + line + new[anchor.end():]) if anchor else new.rstrip("\n") + "\n" + line
    return re.sub(r"\n{3,}", "\n\n", new)


# --------------------------------------------------------------------------- planning (pure)
def ledger_row(ledger, sid):
    return ledger.setdefault("scenes", {}).setdefault(str(sid), {
        "result_received": None, "reviewed": None, "reviewed_at": None, "accepted": None, "needs_redo": None,
        "inserted_into_film": None, "montage_note": None, "decided_task_ids": [], "last_human_update_at": None})


def tasks_of(tel, pid, sid):
    act = [t for t in tel.get("active") or [] if t.get("project") == pid and int(t.get("scene_id") or -1) == sid]
    done = [t for t in tel.get("recent") or [] if t.get("project") == pid and int(t.get("scene_id") or -1) == sid]
    return act, done


def plan(rows, state, tel, now):
    """rows: open Supabase rows of the other projects. state: {pid: {queue, ledger, master, lock, path...}}.
    Returns (changed {relpath: text}, acks [(row, status, note)], projects_touched set)."""
    stamp = iso(now)
    st = {pid: {k: copy.deepcopy(v) for k, v in s.items()} for pid, s in state.items()}
    acks, touched, inbox_new = [], set(), []
    by_scene = {}
    for r in rows:
        pid = prj.project_of_row(r, tel)
        if pid not in st:
            acks.append((r, "needs_owner", f"Кнопка проекта «{pid}», которого нет в projects/projects.json."))
            continue
        r = dict(r, _pid=pid)
        if r["action"] in rsa.QUEUE_ACTIONS:
            s = st[pid]
            if r.get("scene_id") is None:
                acks.append((r, "needs_owner", "Не указан номер сцены."))
                continue
            if canon_lock.is_held(s["lock"], now):
                note = f"Ждёт: проект {pid} занят ({s['lock'].get('holder')}) до {rsa.msk(s['lock'].get('expires_at'))}; применю сразу после."
                if r.get("result_note") != note:
                    acks.append((r, "pending", note))
                continue
            outcome, note = rsa.apply_queue_action(s["queue"], r["action"], int(r["scene_id"]))
            rsa.log_queue(s["queue"], r, outcome, note, stamp)
            touched.add((pid, "queue"))
            if outcome == "inbox":
                inbox_new.append({"id": r["id"], "created_at": r.get("created_at") or stamp, "scene_id": r.get("scene_id"),
                                  "to": "any", "source": "queue_add", "project": pid, "status": "open", "taken_by": None,
                                  "taken_at": None, "result": None, "result_commit": None, "closed_at": None,
                                  "text": f"Проект {pid}: подготовить сцену {r['scene_id']} к запуску и поставить её в очередь "
                                          f"проекта (кнопка владельца «в очередь»). Только безлимит, 0 кредитов."})
                acks.append((r, "in_progress", f"{rsa.INBOX_CLAIM} проект {pid}: {note}"))
            else:
                acks.append((r, "applied", f"Проект {pid}: {note}"))
            continue
        if r["action"] == "tv_mark_status" and r.get("value") != "result_bad":
            continue                       # «Готово ✓» is applied by an agent / the owner, as in the film
        sid = r.get("scene_id")
        if sid is None:
            acks.append((r, "needs_owner", "Не указан номер сцены."))
            continue
        by_scene.setdefault((pid, int(sid)), []).append(r)

    for (pid, sid), items in sorted(by_scene.items()):
        s = st[pid]
        toks = {token(r) for r in items if token(r)}
        if len(toks) > 1:
            for r in items:
                acks.append((r, "needs_owner", f"Проект {pid}, сцена {sid}: кнопки противоречат друг другу "
                                               "(например «Принять» и «Переделать»). Отмените лишнюю."))
            continue
        act, done = tasks_of(tel, pid, sid)
        row = None
        for r in items:
            a = r["action"]
            if a == "tv_drop_task":
                row = row or ledger_row(s["ledger"], sid)
                tid = r.get("task_id")
                if tid and tid not in row.setdefault("decided_task_ids", []):
                    row["decided_task_ids"].append(tid)
                row.setdefault("abandoned_task_ids", [])
                if tid and tid not in row["abandoned_task_ids"]:
                    row["abandoned_task_ids"].append(tid)
                row["last_human_update_at"] = stamp
                touched.add((pid, "ledger"))
                acks.append((r, "applied", f"Проект {pid}, сцена {sid}: задачу больше не ждём. Саму задачу в Topview "
                                           "это не отменяет и её слот не освобождает."))
                continue
            if act:
                note = f"Ждёт: в проекте {pid} сцена {sid} ещё генерируется в Topview. Применю автоматически, когда закончится."
                if r.get("result_note") != note:
                    acks.append((r, "pending", note))
                continue
            if a in ("in_film", "scene_not_needed"):
                new_master = remove_scene(s["master"], sid)
                if new_master is None:
                    acks.append((r, "needs_owner", f"Проект {pid}: сцены {sid} нет в мастере проекта."))
                    continue
                s["master"] = new_master
                touched.add((pid, "master"))
            row = row or ledger_row(s["ledger"], sid)
            row.update(reviewed=True, reviewed_at=stamp, last_human_update_at=stamp)
            if a in ("accept", "to_montage", "in_film"):
                row.update(accepted=True, needs_redo=False)
            if a == "to_montage":
                row["montage_note"] = "в монтаж"
            if a == "in_film":
                row.update(inserted_into_film=True, montage_note="в фильме")
            if a in ("redo", "tv_mark_status"):
                row.update(accepted=False, needs_redo=True)
            if a == "scene_not_needed":
                row["closed_not_needed"] = True
            for t in done:
                if t["task_id"] not in row.setdefault("decided_task_ids", []):
                    row["decided_task_ids"].append(t["task_id"])
            touched.add((pid, "ledger"))
            say = {"accept": "принята", "to_montage": "в монтаж", "in_film": "в фильме, убрана из мастера проекта, номер закрыт",
                   "redo": "на переделку (новый запуск — только по отдельной команде)",
                   "tv_mark_status": "брак (на переделку)", "scene_not_needed": "не нужна, убрана из мастера проекта, номер закрыт"}[a]
            acks.append((r, "applied", f"Проект {pid}, сцена {sid}: {say}."))

    changed = {}
    for pid, s in st.items():
        if (pid, "queue") in touched and dumps(s["queue"]) != dumps(state[pid]["queue"]):
            s["queue"]["updated_at"] = stamp
            changed[s["paths"]["queue"]] = dumps(s["queue"])
        if (pid, "ledger") in touched:
            s["ledger"]["updated_at"] = stamp
            changed[s["paths"]["ledger"]] = dumps(s["ledger"])
        if (pid, "master") in touched and s["master"] != state[pid]["master"]:
            changed[s["paths"]["master"]] = s["master"]
    return changed, acks, inbox_new


# --------------------------------------------------------------------------- io
class SupabaseStore:
    def list_open(self):
        return pod.api("GET", {"select": "id,created_at,scene_id,action,task_id,value,note,status,result_note",
                               "action": "in.(" + ",".join(ACTIONS) + ")",
                               "status": "in.(pending,in_progress)", "order": "created_at.asc",
                               "limit": str(pod.MAX_ROWS)})

    def mark(self, row, to_status, note):
        return pod.patch_status(row["id"], row["status"], to_status, note)


def load_state(root):
    root = Path(root)
    out = {}
    for p in prj.projects(root):
        def rj(rel, default):
            try:
                return json.loads((root / rel).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                return copy.deepcopy(default)
        ledger_rel = f"{p['root']}/review-ledger.json"
        out[p["id"]] = {"queue": rj(p["queue"], {"project": p["id"], "items": []}),
                        "ledger": rj(ledger_rel, {"schema_version": 1, "project": p["id"], "scenes": {}}),
                        "lock": rj(p["lock"], {}),
                        "master": (root / p["master"]).read_text(encoding="utf-8"),
                        "paths": {"queue": p["queue"], "ledger": ledger_rel, "master": p["master"], "status": p["status"]}}
    return out


def run(root, store, git, *, now=None, sync=True, dry=False):
    root = Path(root)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if sync:
            git.sync()
        now_ = now or datetime.now(timezone.utc)
        tel = prj.project_tasks(root)
        rows = [r for r in store.list_open() if r.get("status") == "pending" and not prj.is_root_row(r, tel)]
        if not rows:
            print("::notice title=robot-project-actions::no buttons of other projects")
            return 0
        state = load_state(root)
        changed, acks, inbox_new = plan(rows, state, tel, now_)
        print(json.dumps({"rows": len(rows), "files": sorted(changed), "acks": len(acks), "inbox": len(inbox_new)},
                         ensure_ascii=False))
        if dry:
            return 0
        paths = sorted(changed)
        if changed or inbox_new:
            for rel, text in changed.items():
                (root / rel).write_text(text, encoding="utf-8", newline="")
            bad = []
            for pid, s in state.items():
                if s["paths"]["master"] in changed:
                    st, _ = prj.build_status(root, pid, write=True)
                    paths.append(s["paths"]["status"])
                    if st["health"] != "ok":
                        bad.append(pid)
            if bad:
                git.reset()
                for r, _, _ in acks:
                    if r["action"] in ("in_film", "scene_not_needed") and r.get("_pid") in bad:
                        store.mark(r, "needs_owner", f"Проект {r['_pid']}: после удаления сцены мастер не прошёл проверку; "
                                                     "ничего не изменено, нужен агент.")
                return 1
            if inbox_new:
                inbox = rsa.read_json(root, INBOX, rsa.EMPTY_INBOX)
                have = {t.get("id") for t in inbox.get("tasks", [])}
                inbox.setdefault("tasks", []).extend(t for t in inbox_new if t["id"] not in have)
                inbox["updated_at"] = iso(now_)
                (root / INBOX).write_text(dumps(inbox), encoding="utf-8")
                paths.append(INBOX)
            what = ", ".join(sorted({r["action"] for r, _, _ in acks})) or "buttons"
            commit = git.commit(f"Owner panel robot: project buttons ({what})", sorted(set(paths)))
            if commit and not git.push():
                print(f"push rejected ({attempt}/{MAX_ATTEMPTS}); re-reading main and starting over")
                git.reset()
                if not sync:
                    return 1
                continue
            if commit and not git.head_is_on_remote():
                print("::error title=robot-project-actions::commit not found on origin after push; no acknowledgement")
                return 1
        for row, status, note in acks:
            store.mark(row, status, note)
        return 0
    print("::error title=robot-project-actions::push rejected 4 times; buttons stay pending and are retried next run")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--no-sync", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    return run(a.root, SupabaseStore(), rma.Git(a.root), sync=not a.no_sync, dry=a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
