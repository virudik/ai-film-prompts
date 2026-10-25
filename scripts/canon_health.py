#!/usr/bin/env python3
"""Canon health check (owner decision 18.10.2026): finds stale, oversized and broken parts of the canon.

Staleness is judged by project state; dates are only signals. Writes canon-health.json (shown on the site
as «Здоровье канона»). Read-only for the canon itself: it never edits instructions, master or queue.

Exit code: 0 normally; 1 with --fail-on-new when a warning appeared that the previous canon-health.json
did not have (GitHub then e-mails the owner once per new problem, not every day).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT = "canon-health.json"
DOCS = ["NEW-CHAT-HANDOFF.md", "SYNC-RUNBOOK.md", "AI-PROJECT-GUIDE.md", "PROMPT-STYLE-GUIDE.md",
        "USER-GUIDE.md", "README-AI-SYNC.md", "BACKUP-AI-RUNBOOK.md"]
HANDOFF_MAX_BYTES = 35_000          # «Сейчас + журнал»: live block + stable rules + cleanup rule
PROJECT_HANDOFF_MAX_BYTES = 12_000  # projects/<id>/HANDOFF.md: only «Сейчас», decisions, open items (22.10.2026)
PROJECTS = "projects/projects.json"
INSTRUCTION_MAX_BYTES = 60_000
NOW_BLOCK_MAX_DAYS = 3
OPS_REVIEW_DAYS = 14
TASK_MAX_DAYS = 3
# Service files of the agents (owner decision 23.10.2026): they only grow; the weekly cleanup trims them
# with scripts/trim_service_files.py. Over the limit = warn, so the cleanup also runs outside Sunday.
SERVICE_FILES_MAX_BYTES = {"reports/current-work-checkpoint.md": 80_000, "work-resume-register.json": 100_000,
                           "ops/topview-launch-queue.json": 400_000,
                           "reports/topview-event-wake.json": 200_000}
# Names that live outside the repository (generated Project files / Library copies) or are mentioned as removed.
EXTERNAL_REFS = {"00-START-HERE.md", "CHARACTERS.md", "CURRENT-STATE.json", "CURRENT-STATE.md", "READ-FIRST.txt",
                 "SHIFT-HANDOFF.md", "SITE-STATUS.md", "TAKEOVER-BRIEF.md", "PROGRESS.md", "claude/CURRENT-STATE.md"}
REMOVED_MARK = re.compile(r"[Уу]бран|[Уу]дал[её]н|archive/", re.U)
REF = re.compile(r"`((?:[\w.-]+/)*[\w.-]+\.(?:md|py|json|yml|yaml|html|txt|sql|ts))(?:#[^`]*)?`")
DATE = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(20\d\d)\b")
CHECKED = re.compile(r"(?:Проверено|Checked)\s*:\s*(\d{1,2}\.\d{1,2}\.20\d\d)", re.I)
NOW_BLOCK_DATE = re.compile(r"^##\s+СЕЙЧАС(?:\s+\(обновлено)?\s+(\d{1,2}\.\d{1,2}\.20\d\d)", re.I | re.M)


def ru_date(s):
    m = DATE.search(s or "")
    if not m:
        return None
    try:
        return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)), tzinfo=timezone.utc)
    except ValueError:
        return None


def parse_iso(v):
    try:
        return datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def read(root, rel):
    try:
        return (Path(root) / rel).read_text(encoding="utf-8")
    except OSError:
        return None


def read_json(root, rel):
    t = read(root, rel)
    try:
        return json.loads(t) if t else None
    except json.JSONDecodeError:
        return None


def tracked(root):
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
        return set(out.split())
    except (OSError, subprocess.CalledProcessError):
        return {str(p.relative_to(root)) for p in Path(root).rglob("*") if p.is_file() and ".git" not in p.parts}


def check(root, now):
    problems = []

    def add(level, code, text, file=None):
        problems.append({"level": level, "code": code, "text": text, "file": file})

    files = tracked(root)
    names = {os.path.basename(f) for f in files}

    # 1. Handoff: size and age of the top live block
    h = read(root, "NEW-CHAT-HANDOFF.md") or ""
    size = len(h.encode("utf-8"))
    if size > HANDOFF_MAX_BYTES:
        add("warn", "handoff-size", f"Хендоф {size // 1000} КБ (цель до {HANDOFF_MAX_BYTES // 1000} КБ): "
            "старые блоки перенести в журнал archive/handoff-log.md.", "NEW-CHAT-HANDOFF.md")
    top_match = NOW_BLOCK_DATE.search(h[:4000])
    top = ru_date(top_match.group(1)) if top_match else None
    if top is None:
        add("warn", "handoff-now-undated", "Верхний блок хендофа без даты.", "NEW-CHAT-HANDOFF.md")
    elif now - top > timedelta(days=NOW_BLOCK_MAX_DAYS, hours=12):
        add("warn", "handoff-now-stale", f"Верхний блок хендофа от {top:%d.%m.%Y}: старше {NOW_BLOCK_MAX_DAYS} дней, "
            "проверить, что «Сейчас» ещё правда.", "NEW-CHAT-HANDOFF.md")

    # 2. Instructions: size and broken file references
    for d in DOCS:
        t = read(root, d)
        if t is None:
            add("warn", "instruction-missing", f"Нет инструкции {d}.", d)
            continue
        if d != "NEW-CHAT-HANDOFF.md" and len(t.encode("utf-8")) > INSTRUCTION_MAX_BYTES:
            add("info", "instruction-size", f"{d}: {len(t.encode('utf-8')) // 1000} КБ, проверить на повторы.", d)
        missing = set()
        for line in t.splitlines():
            if REMOVED_MARK.search(line):
                continue
            for ref in REF.findall(line):
                if "*" in ref or "-N/" in ref or ref in EXTERNAL_REFS:
                    continue
                if ref in files or (Path(root) / ref).exists() or ("/" not in ref and ref in names):
                    continue
                missing.add(ref)
        for ref in sorted(missing):
            add("warn", "broken-ref", f"{d} ссылается на файл `{ref}`, которого нет в репозитории.", d)

    # 3. ops/*.md: every working doc says its status and when it was last checked
    for p in sorted(Path(root, "ops").glob("*.md")):
        rel = f"ops/{p.name}"
        head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:12])
        m = CHECKED.search(head)
        when = ru_date(m.group(1)) if m else None
        if when is None:
            add("info", "ops-unchecked", f"{rel}: в шапке нет строки «Статус: … Проверено: дд.мм.гггг». "
                "Нужен — проверить и поставить дату, не нужен — в archive/ops/.", rel)
        elif now - when > timedelta(days=OPS_REVIEW_DAYS):
            add("info", "ops-stale", f"{rel}: проверялся {when:%d.%m.%Y}, больше {OPS_REVIEW_DAYS} дней назад.", rel)

    # 4. Owner task inbox: nothing waits silently
    inbox = read_json(root, "ops/owner-tasks.json") or {}
    for t in inbox.get("tasks", []):
        st = t.get("status")
        since = parse_iso(t.get("taken_at") if st == "taken" else t.get("created_at"))
        if st in ("open", "taken") and since and now - since > timedelta(days=TASK_MAX_DAYS):
            who = {"claude": "Claude", "chatgpt": "ChatGPT", "any": "любого агента"}.get(t.get("to"), t.get("to"))
            what = "никто не взял" if st == "open" else f"в работе у {t.get('taken_by')}"
            add("warn", "task-stuck", f"Задача владельца для {who} {what} больше {TASK_MAX_DAYS} дней: "
                f"«{str(t.get('text') or '')[:90]}».", "ops/owner-tasks.json")

    # 5. Launch queue: waiting items must point to scenes that are still in the master
    q = read_json(root, "ops/topview-launch-queue.json") or {}
    st = read_json(root, "project-status.json") or {}
    active = set(map(int, st.get("scene_ids") or []))
    final = re.compile(r"^(submitted|completed|held_owner_site|superseded|cancelled)")
    if active:
        gone = sorted({int(i["scene_id"]) for i in q.get("items", [])
                       if str(i.get("scene_id", "")).isdigit() and not final.match(str(i.get("state", "")))
                       and int(i["scene_id"]) not in active})
        if gone:
            add("warn", "queue-scene-gone", "В очереди запуска ждут сцены, которых уже нет в мастере (в фильме или закрыты): "
                + ", ".join(map(str, gone)) + ". Их элементы очереди закрыть.", "ops/topview-launch-queue.json")
    if st and st.get("health") not in (None, "ok"):
        add("warn", "status-health", f"project-status.json: health = {st.get('health')}.", "project-status.json")

    # 6. Canon lock that nobody released
    lock = read_json(root, "ops/canon-lock.json") or {}
    exp = parse_iso(lock.get("expires_at"))
    if lock.get("state") == "held" and exp and now - exp > timedelta(hours=2):
        add("info", "lock-expired", f"Замок канона ({lock.get('holder')}) истёк {exp:%d.%m %H:%M} UTC и не снят; "
            "он считается свободным, но запись стоит убрать.", "ops/canon-lock.json")

    # 7. Other projects (projects/<id>/, owner decision 20.10.2026): same signals per project
    reg = read_json(root, PROJECTS) or {}
    for pr in reg.get("projects", []):
        base = str(pr.get("root") or ".").strip("/")
        if base in ("", "."):
            continue                                  # Серёгиус = the root checks above
        name = pr.get("name") or pr.get("id")
        hrel = pr.get("handoff") or f"{base}/HANDOFF.md"
        ph = read(root, hrel)
        if ph is None:
            add("warn", "project-handoff-missing", f"{name}: нет хендофа {hrel}.", hrel)
        elif len(ph.encode("utf-8")) > PROJECT_HANDOFF_MAX_BYTES:
            add("warn", "project-handoff-size", f"{name}: хендоф {len(ph.encode('utf-8')) // 1000} КБ "
                f"(цель до {PROJECT_HANDOFF_MAX_BYTES // 1000} КБ): контрольные точки — в {base}/reports/current-work-checkpoint.md, "
                f"история — в {base}/archive/handoff-log.md.", hrel)
        pst = read_json(root, pr.get("status") or f"{base}/project-status.json") or {}
        if pst and pst.get("health") not in (None, "ok"):
            add("warn", "status-health", f"{name}: project-status.json health = {pst.get('health')}.",
                pr.get("status"))
        pactive = set(map(int, pst.get("scene_ids") or []))
        pq = read_json(root, pr.get("queue") or f"{base}/ops/topview-launch-queue.json") or {}
        pgone = sorted({int(i["scene_id"]) for i in pq.get("items", [])
                        if str(i.get("scene_id", "")).isdigit() and not final.match(str(i.get("state", "")))
                        and int(i["scene_id"]) not in pactive})
        if pgone:
            add("warn", "queue-scene-gone", f"{name}: в очереди ждут сцены, которых нет в мастере проекта: "
                + ", ".join(map(str, pgone)) + ".", pr.get("queue"))
        plock = read_json(root, pr.get("lock") or f"{base}/canon-lock.json") or {}
        pexp = parse_iso(plock.get("expires_at"))
        if plock.get("state") == "held" and pexp and now - pexp > timedelta(hours=2):
            add("info", "lock-expired", f"{name}: замок проекта ({plock.get('holder')}) истёк {pexp:%d.%m %H:%M} UTC "
                "и не снят; он считается свободным, но запись стоит убрать.", pr.get("lock"))

    # 8. Service files (checkpoint, resume register, launch queue) of every project must stay trimmed
    bases = [""] + [str(pr.get("root") or "").strip("/") + "/" for pr in reg.get("projects", [])
                    if str(pr.get("root") or ".").strip("/") not in ("", ".")]
    for base in bases:
        for rel, limit in SERVICE_FILES_MAX_BYTES.items():
            if base and rel == "reports/topview-event-wake.json":
                continue  # Relay receipt journal is global, not a per-project file.
            t = read(root, base + rel)
            if t is not None and len(t.encode("utf-8")) > limit:
                add("warn", "service-file-size", f"{base + rel}: {len(t.encode('utf-8')) // 1000} КБ (предел {limit // 1000} КБ): "
                    "старые записи перенести в архив — python3 scripts/trim_service_files.py . --write "
                    "(раздел хендофа «Как чистить», п. 8).", base + rel)

    warn = sum(p["level"] == "warn" for p in problems)
    return {"schema_version": 1, "checked_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "warn" if warn else "ok", "warnings": warn,
            "info": sum(p["level"] == "info" for p in problems),
            "rules": "scripts/canon_health.py; проверка ежедневно и при каждом изменении main. "
                     "Устаревание по состоянию проекта, даты только сигнал. Чистку делает ChatGPT по предупреждению или в воскресенье 08:55 МСК.",
            "problems": problems}


def key(p):
    return (p["code"], p.get("file"), p["text"])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--write", action="store_true", help=f"write {OUT} when the problem list changed")
    ap.add_argument("--fail-on-new", action="store_true")
    a = ap.parse_args(argv)
    now = datetime.now(timezone.utc)
    res = check(a.root, now)
    prev = read_json(a.root, OUT) or {}
    old = {key(p) for p in prev.get("problems", [])}
    new = [p for p in res["problems"] if p["level"] == "warn" and key(p) not in old]
    same = ([key(p) for p in prev.get("problems", [])] == [key(p) for p in res["problems"]]
            and prev.get("rules") == res["rules"])
    for p in res["problems"]:
        print(f"[{p['level']}] {p['text']}")
    print(f"status={res['status']} warnings={res['warnings']} info={res['info']} new={len(new)}")
    if a.write and not same:
        (Path(a.root) / OUT).write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {OUT}")
    if a.fail_on_new and new and prev:
        print("NEW WARNINGS:\n" + "\n".join("- " + p["text"] for p in new))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
