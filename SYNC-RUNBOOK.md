# AI Film Prompts — Full Sync Runbook

Эта инструкция нужна ChatGPT/основному редактору для восстановления проекта без памяти старого чата и для обслуживания мастера, автоматизации и сайта.

## 1. Единственный источник истины

**Google Drive → `AI Film Prompts Master/video-prompts.md` — единственный канонический редактируемый мастер промтов.**

Постоянные точки:
- Drive folder ID: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
- Drive master ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- Drive viewer ID: `1AZK6XafZng4M_I7ciqdhEjfgfkf3CA01`
- `AI-PROJECT-GUIDE.md`: `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `USER-GUIDE.md`: `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md`: `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `SYNC-RUNBOOK.md`: `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `CLAUDE-TAKEOVER-RUNBOOK.md`: `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`
- `film-analysis.md`: `1O3bsGGivBktRSbeg-9JWeMLK4J_JYu0M`
- `film-backlog.md`: `1YixC7zQFY7z3Bn1XGXxeQIMema3inCT9`
- GitHub repo: `virudik/ai-film-prompts`
- Viewer: `https://virudik.github.io/ai-film-prompts/`
- Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
- Notion Hub ID: `3ddfe763-7762-81c0-b8fd-e7c61895df4a`

Нельзя создавать `video-prompts-v2`, `final`, `copy`, `final-final` и другие конкурирующие мастера.

## 2. Что читать и когда

Перед **каждой реальной записью** в master заново читать свежий Drive `video-prompts.md` и целевую сцену.

Заново читать этот runbook:
- в новом чате или после потери/сомнения в памяти;
- перед изменением архитектуры, сайта или workflow;
- при рассинхронизации;
- перед восстановлением проекта;
- если пользователь сообщает, что Work/Claude/он сам менял Drive master.

Для обычного обсуждения без записи полный runbook перечитывать не нужно.

## 3. Упрощённая архитектура

Оперативный путь специально сведен к одному канону и одной автоматизации:

**Drive master → `SYNC-TRIGGER.txt` → GitHub Action → validation → GitHub mirror + `project-status.json` → GitHub Pages.**

Файлы автоматизации:
- `.github/workflows/sync-from-drive.yml`
- `scripts/build_project_status.py`
- `project-status.json` — generated file; вручную не редактировать.

`project-status.json` содержит автоматически рассчитанные counts, work-items, slow-scenes и health checks. Публичный сайт читает его для верхней строки состояния.

**ChatGPT Library, Drive `video-prompts.html` и Notion — backup/documentation layers, а не обязательные точки каждой правки.** Их обновлять при изменении архитектуры/инструкций, на крупных контрольных точках, при явной просьбе «обнови резервные копии» или когда они сами являются целью задачи.

## 4. Одна команда пользователя

Команда вида:

`Измени сцену N: ... и синхронизируй проект.`

означает:
1. прочитать свежий Drive master;
2. изменить только утверждённую сцену и связанные status/TOC поля;
3. записать **тот же Drive file ID**;
4. обновить `SYNC-TRIGGER.txt`;
5. дождаться GitHub Action;
6. проверить `project-status.json` → `health: ok`;
7. проверить успешный GitHub Pages deployment;
8. проверить публичный viewer/Raw master на характерную новую фразу.

После этого можно писать `ГОТОВО — синхронизация завершена`.

## 5. Health-check master-файла

`scripts/build_project_status.py` обязан останавливать публикацию при нарушении инвариантов. Проверяются минимум:
- declared scene count = числу `## Сцена N`;
- declared scene count = числу строк сцен в верхней таблице;
- номера/порядок сцен в TOC и sections совпадают;
- declared prompt count = числу fenced prompt blocks;
- число W-items совпадает со списком W-ID;
- число slow-scenes совпадает со списком;
- slow-scenes совпадают в dedicated table, TOC и full scene sections;
- номера сцен непрерывны.

Workflow должен быть self-healing для зеркал: каждый запуск генерирует deterministic `/tmp/project-status.json`, сравнивает его и Drive master с GitHub и исправляет только реально отличающиеся файлы. Не создавать commit только из-за прохода времени.

## 6. Правила master-файла

При добавлении активной сцены одновременно:
1. выбрать следующий свободный номер;
2. добавить строку в верхнюю таблицу;
3. добавить полный раздел `<a id="scene-N"></a>` + `## Сцена N — ...`;
4. обновить counts в заметном revision/status block;
5. при необходимости убрать соответствующий W-item;
6. проверить отсутствие старого дубля;
7. A/B-варианты держать внутри одной сцены, если это одна смысловая сцена.

Когда ролик принят и промт больше не нужен — удалить сцену из активного master и TOC. Master — активная очередь, не архив.

## 7. Slow-generation protection

Точная видимая фраза везде:

`⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`

Правила:
- в TOC сначала название сцены, следующей строкой status;
- без тире перед status;
- `⏳` не ставить перед названием;
- сама status-фраза не переносится внутри себя;
- та же фраза используется в dedicated slow table и full scene section;
- пояснение `уже запущено / не запускать повторно` хранится отдельно.

Добавление/снятие slow-status обновляет одновременно: верхний status block, dedicated slow block/table, TOC row и full scene section.

Нельзя повторно запускать slow-scene без явного решения пользователя или подтверждённой ошибки предыдущей генерации.

## 8. Сайт

`index.html` — viewer, а не отдельный master. Он должен:
- fetch `video-prompts.md` с `cache:'no-store'`;
- fetch `project-status.json` с `cache:'no-store'`;
- показывать health/status;
- сохранять `Инструкция для ИИ` одной строкой (`white-space: nowrap`);
- держать slow-status целиком (`white-space: nowrap`);
- вести `Монтажный разбор фильма` на rendered GitHub Pages: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`;
- содержать ссылки на User Guide, Sync Runbook, Raw master, film-analysis, film-backlog и Claude takeover.

Если сайт старый: сначала проверить GitHub root `video-prompts.md` и `project-status.json`. Если root актуален, затем проверять Pages deployment/cache.

## 9. Notion и Library

Notion `AI Video Prompts — Master Hub` — только hub + резерв инструкций. Не копировать туда полный master как вторую редактируемую версию и не переписывать live counts/timestamp после каждой сцены. Для оперативного статуса ссылаться на `project-status.json`/сайт.

Library — резерв ChatGPT. Она не блокирует routine sync. Обновлять при крупных milestones, architecture/instruction changes или явной просьбе пользователя.

## 10. Другие ИИ

Публичная стартовая инструкция:
`https://raw.githubusercontent.com/virudik/ai-film-prompts/main/AI-PROJECT-GUIDE.md`

Затем читать:
`https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`

При continuity/story добавлять `film-analysis.md` и `film-backlog.md`. Для внешности всегда передавать реальные image/video references конкретной сцены.

Claude по умолчанию review-only. Только при явном назначении пользователем временным основным редактором переходит на `CLAUDE-TAKEOVER-RUNBOOK.md`.

## 11. Восстановление без памяти

Если старый чат исчез:
1. открыть этот `SYNC-RUNBOOK.md`;
2. открыть `AI-PROJECT-GUIDE.md`;
3. fresh-read Drive `video-prompts.md`;
4. проверить `project-status.json` и публичный viewer;
5. при сюжетной задаче открыть `film-analysis.md` + `film-backlog.md`;
6. выполнить задачу по правилам выше.

## 12. Что означает «полная резервная синхронизация»

Если пользователь отдельно говорит `обнови всё и все резервные копии`, кроме штатного Drive→GitHub→Pages пути дополнительно обновить/проверить:
- Drive `video-prompts.html`;
- ChatGPT Library;
- все пять instruction files на Drive/GitHub/Library;
- Notion Hub и резервные Notion instruction pages.

Это **не нужно делать после каждой обычной правки сцены**.
