# AI Film Prompts — Full Sync Runbook v2

Эта инструкция — главный технический runbook для ChatGPT/основного редактора проекта. При новом чате или восстановлении сначала читать этот файл, затем `AI-PROJECT-GUIDE.md`, затем свежий Drive `video-prompts.md`.

## Неизменяемые правила v2

- Единственный редактируемый master: Google Drive `AI Film Prompts Master/video-prompts.md`, file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
- GitHub `virudik/ai-film-prompts` — публичное read-only зеркало и источник GitHub Pages.
- `project-status.json` — автоматически генерируемый machine-status; вручную его не редактировать.
- Обычная синхронизация: **fresh-read Drive master → edit same Drive file ID → update `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → validation → GitHub `video-prompts.md` + `project-status.json` → GitHub Pages → verification**.
- `sync-from-drive.yml` также выполняет страховочную проверку по расписанию примерно каждые 30 минут.
- ChatGPT Library, Notion и Drive `video-prompts.html` — backup/documentation layers. Они **не являются gate обычной правки сцены**.
- Полный обход Drive HTML + инструкции + Library + GitHub + Pages + Notion выполняется только при explicit backup/checkpoint, изменении архитектуры или по команде **«полная ручная синхронизация всего и везде»**.
- Перед каждой фактической записью в master обязательно заново читать свежий Drive `video-prompts.md`.
- Scene ID — стабильный идентификатор. После удаления готовой сцены остальные сцены **не перенумеровывать ради непрерывности**. Пропуски допустимы; IDs должны быть уникальными и идти по возрастанию в TOC/sections.
- После успешной генерации и закрытия сцены удалять её из активного master, если промт больше не нужен.
- Точная видимая надпись slow-status: `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`.
- Slow-status должен совпадать **в четырёх местах**: (1) верхний status block, (2) dedicated slow-generation table/block, (3) TOC row, (4) full scene section.
- Медленную сцену нельзя запускать повторно без подтверждённого результата/ошибки или отдельного разрешения пользователя.
- Человекочитаемые даты: **DD.MM.YYYY**. ISO допустим только внутри machine/API/JSON полей.
- На сайте `Инструкция для ИИ` и `Для владельца` должны быть рядом как две половинные кнопки; `Инструкция для ИИ` не должна переноситься (`white-space: nowrap`).
- `Монтажный разбор фильма` должен открывать rendered GitHub Pages HTML `Seregius_montazhny_razbor.html`, а не Google Drive preview.
- `index.html` — viewer, не master; сценовый контент не hard-code. Он читает root `video-prompts.md` и `project-status.json` с `cache: no-store`.
- Старый `_source/part-*.md` + `build-master.yml` считается legacy и не используется для построения master.
- Нельзя говорить `ГОТОВО`, пока обязательная для выбранного режима проверка фактического результата не завершена.

## Постоянные точки проекта

- Drive folder `AI Film Prompts Master`: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
- Drive master `video-prompts.md`: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- Drive viewer `video-prompts.html`: `1AZK6XafZng4M_I7ciqdhEjfgfkf3CA01`
- `SYNC-RUNBOOK.md`: `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `AI-PROJECT-GUIDE.md`: `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `USER-GUIDE.md`: `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md`: `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `CLAUDE-TAKEOVER-RUNBOOK.md`: `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`
- `NEW-CHAT-HANDOFF.md`: `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- Notion Hub: `3ddfe763-7762-81c0-b8fd-e7c61895df4a`
- GitHub repo: `virudik/ai-film-prompts`
- Public viewer: `https://virudik.github.io/ai-film-prompts/`
- Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
- Rendered montage review: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`

## Как обслуживать master

При добавлении новой активной сцены:
1. fresh-read Drive master;
2. выбрать следующий свободный scene ID;
3. добавить TOC row;
4. добавить anchor `<a id="scene-N"></a>` и полный `## Сцена N — ...`;
5. обновить counts;
6. убрать соответствующий W-item, если он превратился в полноценную сцену;
7. проверить отсутствие дублей;
8. A/B-варианты одной смысловой сцены хранить внутри одной scene ID.

При изменении существующей сцены менять только целевой блок и связанные статусы/счётчики. Значения `@imageN`/`@videoN` локальны для конкретной сцены.

При удалении принятой сцены удалить TOC row и section, обновить counts/statuses. Остальные ID не сдвигать.

## Integrity check master

Перед записью/публикацией проверить:
- declared scene count = количество `## Сцена N`;
- declared scene count = количество TOC rows;
- TOC IDs = section IDs;
- ID уникальны и возрастают; непрерывность не требуется;
- declared prompt count = фактическое число fenced prompt blocks;
- W-count = число W-items;
- slow-count/list совпадает с dedicated slow table, TOC и sections;
- нет старой версии изменяемой сцены в другом месте файла.

## Обычный sync

1. Fresh-read Drive master.
2. Внести только утверждённую правку в тот же Drive file ID.
3. Обновить `SYNC-TRIGGER.txt`.
4. Дождаться `sync-from-drive.yml`.
5. Проверить `project-status.json` → `health: ok`.
6. Проверить успешный GitHub Pages deployment.
7. Проверить raw/site на наличие изменённой фразы/статуса.
8. Только после этого сообщить `ГОТОВО`.

Library/Notion/Drive HTML при этом не трогать, если не было отдельной причины.

## Полная ручная синхронизация всего и везде

При explicit full checkpoint:
1. fresh-read Drive master;
2. проверить целостность master;
3. обновить Drive `video-prompts.html`;
4. привести пять Drive-инструкций к актуальной архитектуре;
5. обновить Library master + HTML + пять инструкций + резерв сайта/index при наличии;
6. обновить GitHub master/изменённые инструкции/site files;
7. trigger/дождаться `sync-from-drive.yml`;
8. проверить Actions success;
9. проверить `project-status.json` health;
10. проверить Pages deployment success;
11. обновить Notion Hub и пять instruction pages;
12. end-to-end проверить raw master и публичный viewer;
13. сообщить `ГОТОВО` только если обязательные пункты подтверждены.

## Как обслуживать сайт

- Источник scene content — GitHub root `video-prompts.md`.
- `index.html` только отображает master/status.
- После изменения master проверять Pages deployment и публичную ревизию.
- Если сайт кажется старым: Drive → GitHub root → `project-status.json` → Pages deployment → viewer.
- `Seregius_montazhny_razbor.html` публикуется как отдельная rendered Pages page.

## Notion

Notion Hub — navigation/documentation hub, не второй master. В нём должны быть ссылки на Drive/GitHub/site и пять дочерних копий инструкций. Live counts/timestamps не дублировать как источник истины; брать их из master/`project-status.json`.

## Library

Library — резерв ChatGPT. Никогда не считать её свежее Drive без проверки. При полном checkpoint Library master/HTML/instructions должны быть обновлены до текущего состояния, но routine sync от этого не зависит.

## Recovery

При потере чата:
1. `NEW-CHAT-HANDOFF.md`;
2. этот `SYNC-RUNBOOK.md`;
3. `AI-PROJECT-GUIDE.md`;
4. fresh Drive `video-prompts.md`;
5. при необходимости `film-analysis.md` + `film-backlog.md`;
6. проверить `project-status.json` и Pages.
