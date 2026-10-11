"""Offline fixtures for the owner-panel robot tests (no network, no secrets).

make_origin(tmp) builds a bare "origin" repo plus one working clone with a compact but
validator-valid canonical master (scenes 13, 24, 25, 30), a review ledger and Topview
telemetry. FakeStore stands in for Supabase and records every status write together with
what origin/main contained at that moment (commit-before-ack evidence).
"""
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T0 = "2026-10-11T10:00:00Z"
ACTIVE_TASK = "a" * 32
OLD_TASK = "b" * 32


def scene_block(n, title, deps=None, slow=False, sep=True, prompts=1):
    meta = {"target_engine": "Wan 3", "production_state": "READY", "duration_s": 30,
            "dialogue": {"enabled": False, "language": None}, "dependencies": deps or [], "tags": ["fixture"]}
    parts = []
    if sep:
        parts.append("---\n\n")
    parts.append(f'<a id="scene-{n}"></a>\n\n## Сцена {n} — {title}\n\n')
    if slow:
        parts.append("**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**\n\n")
    parts.append("<!-- scene-meta: " + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + " -->\n\n")
    parts.append(f"**Контекст использования:** фикстура сцены {n}.\n\n")
    for i in range(prompts):
        parts.append(f"```text\nMode: reference-to-video | prompt {i + 1} of scene {n}\n```\n\n")
    return "".join(parts)


def master_text(slow_rows="", slow=(), latest=30):
    toc = {13: "Совет", 24: "Кабина", 25: "Сражение", 30: "Колоннада"}
    rows = "\n".join(
        f"| {n} | [{t}](#scene-{n}) | @image1 | Что происходит {n}." + (f"<br>**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**" if n in slow else "") + " |"
        for n, t in toc.items())
    slow_ids = ", ".join(map(str, sorted(slow))) if slow else "нет"
    return (
        "# Актуальные видео-сцены и промты\n\n"
        "Рабочий мастер-файл.\n\n"
        "**Канонический источник:** `video-prompts.md`.\n\n"
        "## 📌 РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС\n\n"
        "**4 сцен к генерации/доработке · 4 полных текста промта**\n\n"
        "- **🛠️ 2** рабочих направлений в блоке **«Сцены в работе»**: W5–W6.\n"
        f"- **⏳ {len(slow)}** сцен сейчас в медленной генерации: **{slow_ids}** — **{len(slow)} активных Topview-задач / {len(slow)} занятых слотов из 6**. Редакционная приёмка отдельно.\n"
        f"- **Последняя оформленная активная сцена:** {latest} — фикстура.\n"
        "- **Последняя полная синхронизация:** **11.10.2026 · фикстура**.\n\n"
        "**Синхронизация контекста:** **11.10.2026**. В active master остаются **4 актуальных сцены и 4 полных текста промта**. "
        "Сцены **1, 2 и 12** удалены из active master; их Scene ID зарезервированы и не переиспользуются. "
        f"Canonical slow-list сейчас: **{slow_ids}**.\n\n"
        "## ⏳ Сейчас в медленной генерации\n\n"
        "| Сцена | Статус | Действие |\n|---|---|---|\n"
        f"{slow_rows}\n"
        "Slow-статус снимается автоматически.\n\n"
        "| # | Сцена | Референсы | Что происходит |\n|---|-------|-----------|-----------------|\n"
        f"{rows}\n\n"
        "---\n\n## Сцены в работе\n\n"
        "| ID | Очередь | Статус |\n|---|---|---|\n| W5 | **Идея** | В РАЗРАБОТКЕ |\n| W6 | **Идея 2** | В РАЗРАБОТКЕ |\n\n"
        + scene_block(13, "Совет", sep=True)
        + scene_block(24, "Кабина", sep=True)
        + scene_block(25, "Сражение", deps=[{"type": "continues", "scene": 24}], sep=False)
        + scene_block(30, "Колоннада", slow=30 in slow, sep=True)
        + "---\n")


def slow_row_active(task=ACTIVE_TASK):
    return (f"| 30 — Колоннада | ⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ · `running` · Wan 3.0 | "
            f"task `{task}`; ждать terminal и проверить результат отдельно |")


def slow_row_done(task=OLD_TASK):
    return (f"| 13 — Совет | ✅ Технический результат получен · `success` · Wan 3.0 | "
            f"task `{task}`; требуется отдельная редакционная проверка |")


def ledger_row(**kw):
    row = {"result_received": True, "result_received_at": None, "reviewed": None, "reviewed_at": None,
           "accepted": None, "needs_redo": None, "inserted_into_film": None, "montage_note": None,
           "last_human_update_at": None}
    row.update(kw)
    return row


def telemetry(active=True):
    tasks = ([{"scene_id": 30, "task_id": ACTIVE_TASK, "model": "Wan 3.0", "model_id": "wan",
               "topview_status": "running", "started_at": T0, "queue_count": 1,
               "topview_estimated_wait_seconds": 5, "checked_at": T0, "verified": True,
               "mapping_confidence": "fixture"}] if active else [])
    ids = [ACTIVE_TASK] if active else []
    status = {"schema_version": 3, "checked_at": T0, "slot_capacity": 6, "occupied_slots": len(tasks),
              "free_slots": 6 - len(tasks), "active_tasks": tasks,
              "scenes": {"30": {"scene_id": 30, "task_id": ACTIVE_TASK, "topview_status": "running" if active else "success",
                                "active_task_ids": ids, "completed_at": None}},
              "ui_contract": {"three_view_checked_at": T0},
              "account_observation": {"checked_at": T0, "occupied_slots": len(tasks), "free_slots": 6 - len(tasks),
                                      "active_task_ids": ids, "slot_capacity": 6}}
    task_map = {"schema_version": 3, "updated_at": T0, "last_scan_at": T0, "retention": {"processed_tasks_max": 200},
                "active_by_scene": {"30": ids} if active else {},
                "processed_tasks": [{"task_id": OLD_TASK, "scene_id": 13, "final_status": "success", "finished_at": T0}],
                "scan_cursor": {}}
    checkpoint = {"schema_version": 1, "committed_at": T0, "checked_at": T0, "occupied_slots": len(tasks),
                  "active_task_ids": ids, "active_scene_ids": [30] if active else []}
    journal = {"schema_version": 1, "retention_max_events": 500, "events": []}
    return status, task_map, checkpoint, journal


def write_repo_files(root, *, with_active_task=True, master=None):
    root = Path(root)
    (root / "scripts").mkdir(exist_ok=True)
    for name in ("build_project_status.py", "validate_review_ledger.py"):
        shutil.copy(ROOT / "scripts" / name, root / "scripts" / name)
    slow_rows = (slow_row_done() + "\n" + (slow_row_active() if with_active_task else "")).strip("\n")
    text = master or master_text(slow_rows=slow_rows, slow=(30,) if with_active_task else ())
    (root / "video-prompts.md").write_text(text, encoding="utf-8", newline="")
    status, task_map, checkpoint, journal = telemetry(with_active_task)
    for name, obj in (("topview-status.json", status), ("topview-task-map.json", task_map),
                      ("topview-checkpoint.json", checkpoint), ("topview-operation-journal.json", journal)):
        (root / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger = {"schema_version": 2, "updated_at": T0,
              "scenes": {"13": ledger_row(), "24": ledger_row(reviewed=True, reviewed_at=T0, accepted=True, needs_redo=False),
                         "25": ledger_row(), "30": ledger_row(result_received=False),
                         "12": ledger_row(reviewed=True, accepted=True, needs_redo=False, inserted_into_film=True)}}
    (root / "review-ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "SYNC-TRIGGER.txt").write_text("old trigger\n", encoding="utf-8")
    seed = subprocess.run(
        ["python3", "scripts/build_project_status.py", "video-prompts.md", "--output", "project-status.json",
         "--synced-at", T0, "--topview-status-file", "topview-status.json",
         "--topview-task-map-file", "topview-task-map.json"], cwd=root, text=True, capture_output=True)
    status = json.loads((root / "project-status.json").read_text(encoding="utf-8"))
    assert status["health"] == "ok", (seed.stderr[-300:], [k for k, v in status["checks"].items() if not v])


def git(cwd, *args, check=True):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=cwd, text=True,
                          capture_output=True, check=check)


def make_origin(tmp, **kw):
    """Returns (origin_bare_path, work_clone_path); `main` is pushed and tracked."""
    tmp = Path(tmp)
    origin, seed, work = tmp / "origin.git", tmp / "seed", tmp / "work"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    seed.mkdir()
    git(seed, "init", "-q", "-b", "main")
    write_repo_files(seed, **kw)
    git(seed, "add", "-A")
    git(seed, "commit", "-q", "-m", "fixture")
    git(seed, "remote", "add", "origin", str(origin))
    git(seed, "push", "-q", "origin", "main")
    subprocess.run(["git", "clone", "-q", str(origin), str(work)], check=True)
    return origin, work


class FakeStore:
    """Supabase stand-in. `rows` are dicts like the owner_decisions table; every write is logged
    with the origin/main head at that time so tests can prove commit-before-ack."""

    def __init__(self, rows, origin=None):
        self.rows = {r["id"]: dict(r) for r in rows}
        self.origin = origin
        self.log = []

    def _head(self):
        if not self.origin:
            return None
        return subprocess.run(["git", "--git-dir", str(self.origin), "rev-parse", "main"], text=True,
                              capture_output=True).stdout.strip()

    def list_open(self):
        return [dict(r) for r in self.rows.values() if r["status"] in ("pending", "in_progress")]

    def mark(self, row, to_status, note):
        cur = self.rows[row["id"]]
        if cur["status"] != row["status"]:
            return False
        cur["status"], cur["result_note"] = to_status, note
        self.log.append({"id": row["id"], "to": to_status, "note": note, "origin_head": self._head()})
        return True

    def status_of(self, rid):
        return self.rows[rid]["status"]


def row(rid, scene, action, status="pending", task_id=None, value=None, note=None):
    return {"id": rid, "created_at": "2026-10-11T09:00:00Z", "scene_id": scene, "action": action,
            "task_id": task_id, "value": value, "status": status, "result_note": note}
