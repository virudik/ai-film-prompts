#!/usr/bin/env python3
"""Build the context-file set for the claude.ai / ChatGPT Project «AI Film Серёгиус» (read-only backup copies).

Canon is GitHub `main`; Project files are copies that help a chat start. This writes into OUT_DIR:
  00-START-HERE.md       what the project is, where the canon is, how to take over (generated)
  CURRENT-STATE.md       = shadow/current-checkpoint.md (verbatim top blocks of NEW-CHAT-HANDOFF.md)
  TAKEOVER-BRIEF.md      = shadow/takeover-brief.md (short takeover, decision D7)
  CHARACTERS.md          compact character map from character-references.json (no base64)
  the 7 instructions, video-prompts.md, film-analysis.md, film-backlog.md (exact copies)
  model-sheets/*.jpg     exact owner model sheets (references/full), optional for visual identity
Nothing in the repository is modified. Usage: python3 scripts/build_project_files.py [repo] OUT_DIR
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

DOCS = ["NEW-CHAT-HANDOFF.md", "SYNC-RUNBOOK.md", "AI-PROJECT-GUIDE.md", "PROMPT-STYLE-GUIDE.md",
        "USER-GUIDE.md", "README-AI-SYNC.md", "BACKUP-AI-RUNBOOK.md"]
EXTRA = ["video-prompts.md", "film-analysis.md", "film-backlog.md"]
PAGES = "https://virudik.github.io/ai-film-prompts/"


def characters_md(refs, ps):
    active = set(ps.get("scene_ids") or [])
    out = ["# Персонажи «AI Film Серёгиус» — карта для промтов",
           "",
           f"Собрано из `character-references.json` (обновлён {refs.get('updated_at') or refs.get('checked_at')}). "
           "Канон — GitHub `main`; картинки — `references/full/` (точные оригиналы владельца) и сайт "
           f"{PAGES}references.html. Индивидуальный model sheet важнее групповых и композиционных помощников.",
           ""]
    for c in refs.get("characters", []):
        sc = c.get("scenes") or []
        act = [s for s in sc if s in active]
        ms = c.get("model_sheet") or {}
        out.append(f"## {c.get('name')} (`{c.get('id')}`)")
        if c.get("aliases"):
            out.append(f"- Другие имена: {', '.join(c['aliases'])}")
        out.append(f"- Активные сцены: {', '.join(map(str, act)) or '—'}" + (f" (всего в реестре: {', '.join(map(str, sc))})" if sc != act else ""))
        if c.get("outfit_variant"):
            out.append(f"- Внешность / костюм: {c['outfit_variant']}")
        for v in c.get("variants") or []:
            out.append(f"- Вариант «{v.get('label')}» (сцены {', '.join(map(str, v.get('scenes') or [])) or '—'}): {v.get('notes', '')}")
        if c.get("reference_priority"):
            out.append(f"- Приоритет референса: {c['reference_priority']}")
        if ms.get("full_image"):
            out.append(f"- Model sheet: `{ms['full_image']}` ({PAGES}{ms['full_image']})")
        elif ms.get("public_image"):
            out.append(f"- Превью: `{ms['public_image']}` ({PAGES}{ms['public_image']})")
        out.append("")
    for key in ("non_character_reference_rules", "name_resolution_policy"):
        val = refs.get(key)
        if val:
            out += [f"## {key}", "", "```json", json.dumps(val, ensure_ascii=False, indent=1), "```", ""]
    return "\n".join(out) + "\n"


def main(repo, out):
    repo, out = Path(repo), Path(out)
    if out.exists():
        shutil.rmtree(out)
    (out / "model-sheets").mkdir(parents=True)
    ps = json.loads((repo / "project-status.json").read_text(encoding="utf-8"))
    refs = json.loads((repo / "character-references.json").read_text(encoding="utf-8"))
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=repo, text=True, capture_output=True).stdout.strip()
    rows = []
    for name in DOCS + EXTRA:
        b = (repo / name).read_bytes()
        (out / name).write_bytes(b)
        rows.append((name, len(b), hashlib.sha256(b).hexdigest()[:16]))
    shutil.copyfile(repo / "shadow/current-checkpoint.md", out / "CURRENT-STATE.md")
    shutil.copyfile(repo / "shadow/takeover-brief.md", out / "TAKEOVER-BRIEF.md")
    (out / "CHARACTERS.md").write_text(characters_md(refs, ps), encoding="utf-8")
    for img in sorted((repo / "references/full").glob("*.jpg")):
        shutil.copyfile(img, out / "model-sheets" / img.name)
    start = [
        "# 00 — START HERE · проект «AI Film Серёгиус»",
        "",
        f"Файлы проекта — **резервные копии только для чтения**, собраны из GitHub `main` (коммит `{head}`, "
        f"master SHA `{(ps.get('canonical_master_sha256') or '')[:16]}`). Они могут отставать: **канон — GitHub "
        "`virudik/ai-film-prompts`, ветка `main`**; при любом расхождении побеждает свежий `main`. Ничего в этих копиях не править.",
        "",
        "## Как начать (решение D7, 14.10.2026)",
        "1. Если есть доступ к GitHub — `git pull` и работать по свежему `main` (эти файлы — только запасной контекст).",
        "2. `TAKEOVER-BRIEF.md` (короткий приём смены) → `CURRENT-STATE.md` (живое состояние = верхние блоки хендофа) → "
        "живые статусы из `main` (`project-status.json`, `topview-status.json`, `monitor-role.json`, `automation-monitor-status.json`) и открытые задачи владельца в Supabase `owner_decisions`.",
        "3. Под задачу — полные разделы инструкций (список «Что читать под задачу» в брифе). Полное чтение 7 инструкций — если бриф не сходится с каноном, при правке инструкций или порядка работы, после сбоя, при сомнении или по просьбе владельца.",
        "",
        "## Что здесь лежит",
        "| Файл | Зачем |",
        "|---|---|",
        "| `CURRENT-STATE.md` | живое состояние: кто пишет, автоматика, кнопки, slow, открытые вопросы |",
        "| `TAKEOVER-BRIEF.md` | короткий приём смены (15 обязательных правил, индекс сцен, что читать под задачу) |",
        "| `NEW-CHAT-HANDOFF.md` … `BACKUP-AI-RUNBOOK.md` | 7 инструкций (порядок чтения — как перечислено в `CLAUDE.md` репозитория) |",
        "| `video-prompts.md` | master промтов (активные сцены) |",
        "| `film-analysis.md`, `film-backlog.md` | сюжет, монтаж, план работ |",
        "| `CHARACTERS.md` + `model-sheets/` | персонажи и точные model sheets владельца |",
        "",
        "## Главное (подробно — в `CURRENT-STATE.md`)",
        "- Телеметрию Topview пишет GitHub-робот (каждые 10 минут); ChatGPT — резерв; монитор Claude выключен.",
        "- Генерации Topview — только по команде владельца, только безлимит через сайт Topview; MCP/Canvas — платно, запрещено.",
        "- Технический success ≠ одобрение; сцену из медленной генерации снимает только кнопка владельца.",
        "- Правка канона — только коммитом в `main` (master → `SYNC-TRIGGER.txt` → health=ok; инструкции → `scripts/cert_github.py`). Один писатель канона одновременно.",
        f"- Сайт: {PAGES}",
        "",
        "## Копии (размер, sha256)",
    ] + [f"- `{n}` · {b} B · `{h}`" for n, b, h in rows]
    (out / "00-START-HERE.md").write_text("\n".join(start) + "\n", encoding="utf-8")
    files = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    print(json.dumps({"out": str(out), "files": len(files), "bytes": sum((out / f).stat().st_size for f in files)}, ensure_ascii=False))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1:
        args = ["."] + args
    if len(args) != 2:
        sys.exit(__doc__)
    main(*args)
