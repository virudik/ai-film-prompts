# AI Film Prompts — передача управления в новый чат v2

Дата checkpoint: **17.09.2026**.

Этот файл нужен для восстановления проекта без памяти старого чата. Он отражает состояние после полного v2-checkpoint, когда Drive, GitHub, Library, Notion и GitHub Pages были повторно сверены.

## 1. Текущее подтверждённое состояние

- Canonical master: Google Drive `AI Film Prompts Master/video-prompts.md`.
- Active scenes: **17**.
- Full prompt texts: **20**.
- Work items: **W5, W7, W8**.
- Slow scenes: **2, 6, 14, 15**.
- Сцена **8 «Кашиик — спор на мосту»** завершена и удалена из active master.
- Scene IDs стабильны; после удаления сцен остальные ID не перенумеровывать. Gaps допустимы.
- `project-status.json` → **health: ok**; все invariant checks true.
- Full checkpoint sync run **#75** завершён `success`.
- GitHub Pages deployment **#107** завершён `success`.

## 2. Архитектура v2

Routine workflow:

**fresh-read Drive master → edit same Drive file ID → `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → validation → GitHub `video-prompts.md` + `project-status.json` → GitHub Pages → verification**.

Library, Notion и Drive `video-prompts.html` — backup/documentation layers и не обновляются после каждой обычной scene edit.

Полный обход всех зеркал выполняется только при explicit backup/checkpoint, изменении архитектуры/инструкций или по команде **«полная ручная синхронизация всего и везде»**.

## 3. Главные точки

- Drive folder ID: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
- Drive master ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- Drive HTML ID: `1AZK6XafZng4M_I7ciqdhEjfgfkf3CA01`
- `SYNC-RUNBOOK.md`: `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `AI-PROJECT-GUIDE.md`: `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `USER-GUIDE.md`: `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md`: `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `CLAUDE-TAKEOVER-RUNBOOK.md`: `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`
- Notion Hub ID: `3ddfe763-7762-81c0-b8fd-e7c61895df4a`
- GitHub repo: `virudik/ai-film-prompts`
- Viewer: `https://virudik.github.io/ai-film-prompts/`
- Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
- Montage review: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`

## 4. Что читать новому основному редактору

1. `NEW-CHAT-HANDOFF.md`;
2. `SYNC-RUNBOOK.md`;
3. `AI-PROJECT-GUIDE.md`;
4. fresh Drive `video-prompts.md`;
5. при story/continuity — `film-analysis.md` + `film-backlog.md`;
6. для deep montage — `Seregius_montazhny_razbor.html`, `EDIT_PLAN_V2.csv`, `PROGRESS.md` при необходимости.

Не опираться на старую память/старые Library-файлы, если они расходятся с Drive.

## 5. Master invariants

- Scene IDs unique + increasing; gaps allowed.
- Declared scene count = TOC rows = full scene sections.
- Declared prompt count = fenced prompt blocks.
- W-count совпадает с W-list.
- Slow list/count совпадает во всех обязательных местах.
- Exact slow label: `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`.
- Slow status должен быть в **4 местах**: global status, dedicated slow table/block, TOC row, full scene section.
- Не relaunch slow scene без результата/ошибки или отдельного решения пользователя.
- После принятого ролика удалить prompt из active master, если он больше не нужен.

## 6. Site invariants

- `index.html` — viewer, not master.
- Fetch `video-prompts.md` and `project-status.json` with `cache: no-store`.
- `Инструкция для ИИ` + `Для владельца` — две соседние half-width buttons.
- `Инструкция для ИИ` must not wrap.
- Montage review opens rendered GitHub Pages HTML.
- Legacy `_source/part-*` / `build-master.yml` не использовать.
- Obsolete one-time instruction finalizer disabled.

## 7. Human formatting

- Human-readable dates: **DD.MM.YYYY**.
- Machine ISO timestamps can remain ISO in JSON/API.

## 8. Полный checkpoint v2 от 17.09.2026

Подтверждено:
- 5 canonical Drive instructions updated in-place;
- GitHub instruction mirrors updated;
- Library master/HTML/instructions/index updated;
- stale Library master mirror `video-prompts(8).md` and stale HTML mirror `video-prompts(1).html` updated;
- Notion Hub + 5 instruction child pages updated;
- `sync-from-drive.yml` run #75 success;
- `project-status.json` health ok;
- Pages deployment #107 success.

Исторический Library file `video-prompts(1).md` — отдельная старая prompt compilation, не canonical master mirror; его не перезаписывать как master.

## 9. Готовая команда новому ChatGPT

> Мы продолжаем AI-film project. Сначала прочитай `NEW-CHAT-HANDOFF.md`, `SYNC-RUNBOOK.md`, `AI-PROJECT-GUIDE.md` и fresh Google Drive `video-prompts.md`. Canonical master только Drive. Routine sync: Drive → trigger → validation → GitHub/status → Pages. Library/Notion/Drive HTML — backup layers. Scene IDs stable and may have gaps. Slow-status uses exact phrase `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` in 4 places. Перед `ГОТОВО` проверяй health/workflow/Pages. Ничего не меняй без моей команды.
