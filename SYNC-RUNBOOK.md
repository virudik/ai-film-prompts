# AI Film Prompts — Full Sync Runbook v3.5

Эта инструкция — главный нормативный технический runbook для ChatGPT/основного редактора проекта. При новом чате или восстановлении сначала читать этот файл, затем `AI-PROJECT-GUIDE.md`, затем свежий Drive `video-prompts.md`.

## Неизменяемые правила v3.5

- Единственный редактируемый prompt master: Google Drive `AI Film Prompts Master/video-prompts.md`, file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
- GitHub `virudik/ai-film-prompts` — публичное read-only зеркало и источник GitHub Pages. GitHub не становится master даже при недоступности других слоёв.
- Пять Drive-инструкций — канонические для своих GitHub-зеркал: `AI-PROJECT-GUIDE.md`, `SYNC-RUNBOOK.md`, `USER-GUIDE.md`, `README-AI-SYNC.md`, `CLAUDE-TAKEOVER-RUNBOOK.md`.
- `project-status.json` schema v3 — автоматически генерируемый machine-status; вручную его не редактировать.
- Routine sync: **fresh-read Drive master → edit same Drive file ID → update `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → validation → GitHub `video-prompts.md` + generated `project-status.json` → GitHub Pages → verification**.
- `sync-from-drive.yml` выполняет страховочную проверку примерно каждые 30 минут. На текущем этапе он автоматически читает Drive master; приватные Drive-инструкции через Actions не скачиваются.
- Перед каждой фактической записью в master обязательно заново читать свежий Drive `video-prompts.md`.
- Scene ID — стабильный идентификатор. После удаления сцены остальные ID не перенумеровывать; пропуски допустимы.
- После принятия и закрытия сцены удалять её из активного master, если промт больше не нужен.
- Точная видимая slow-надпись: `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`.
- Slow-status должен совпадать в четырёх ручных местах master: верхний status block, dedicated slow block/table, TOC row, full scene section. Валидатор это проверяет.
- `render_state` в schema v3 **вычисляется** из существующего slow-list: slow → `SLOW_PENDING`, иначе `IDLE`. Не создавать пятое ручное slow-поле.
- Медленную сцену нельзя запускать повторно без подтверждённого результата/ошибки или отдельного разрешения пользователя.
- `scene_meta` опционален; если блок присутствует, он обязан быть валидным. Невалидный JSON, production state, duration или dependency target должны валить validation.
- Человекочитаемые даты: **DD.MM.YYYY**. ISO — machine/API/JSON only.
- `index.html` — viewer, не master; сценовый контент не hard-code. Он читает root `video-prompts.md` и `project-status.json` с `cache: no-store`.
- Library, Notion и Drive `video-prompts.html` — backup/documentation layers, не gate routine edit.
- Полный checkpoint обязателен при architecture/instruction changes, milestone, explicit backup/full-sync.
- Старый `_source/part-*.md` + `build-master.yml` — legacy и не используется.
- Не говорить `ГОТОВО`, пока обязательные проверки выбранного режима не подтверждены фактически.

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
- `film-analysis.md`: `1O3bsGGivBktRSbeg-9JWeMLK4J_JYu0M`
- `film-backlog.md`: `1YixC7zQFY7z3Bn1XGXxeQIMema3inCT9`
- Notion Hub: `3ddfe763-7762-81c0-b8fd-e7c61895df4a`
- GitHub repo: `virudik/ai-film-prompts`
- Public viewer: `https://virudik.github.io/ai-film-prompts/`
- Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
- Rendered montage review: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`

## Schema v3 / project-status.json

`project-status.json` сохраняет старые top-level поля для backward compatibility и добавляет:

- `schema_version: 3`;
- `canonical_master_sha256` + `canonical_master_bytes`;
- `audit_fingerprint`;
- `scene_meta`;
- `instruction_sync`;
- дополнительные validator checks.

### Audit fingerprint

Минимум:
- revision date;
- sync timestamp;
- canonical master SHA-256;
- scene/prompt counts;
- scene IDs;
- W-items;
- slow scenes;
- project health;
- instruction sync health.

Перед внешним аудитом ИИ обязан повторить фактически видимый fingerprint. Если он не совпадает с текущим — сначала обновить sources.

### Production state vs render state

Если `scene_meta` используется, допустимые production states:
- `DRAFT`
- `READY`
- `NEEDS_FIX`
- `RESULT_RECEIVED`
- `NEEDS_RERENDER`
- `APPROVED`
- `IN_EDIT`
- `CLOSED`

`render_state` — отдельное machine state и не заменяет production state.

Правила interpretation:
- `NEEDS_FIX` — сцена/промт помечены для отдельного обсуждения необходимости правки. Сам статус **не разрешает** переписывать prompt или запускать новый render.
- `NEEDS_RERENDER` — проблема результата уже известна; это не отменяет slow-lock и не разрешает duplicate render без явного условия запуска.
- `READY + SLOW_PENDING` допустимо: prompt подготовлен, но уже находится в медленной генерации.
- `NEEDS_FIX + SLOW_PENDING` допустимо: известная потенциальная правка обсуждается **после текущего результата**, без повторного запуска текущей slow-задачи.

### instruction_sync

Пять instruction Drive files остаются приватными/каноническими. GitHub Actions не получает Google Drive credentials и **не должен** пытаться скачивать эти файлы анонимно.

Авторизованная сверка выполняется ежечасной automation `Topview Slow Watch` через подключённые Google Drive + GitHub:
1. fresh-read пяти Drive-инструкций по фиксированным file ID;
2. exact-text compare с текущими GitHub mirrors;
3. запись результата в `instruction-sync-status.json`;
4. `sync-from-drive.yml` перечитывает snapshot и пересобирает `project-status.json`.

Состояния:
- `ok` — пять файлов совпадают, snapshot не старше 3 часов;
- `stale` — snapshot старше 3 часов;
- `error` — mismatch/read failure;
- `unverified` — snapshot отсутствует/невалиден.

`error` нельзя исправлять автоматически копированием одной стороны поверх другой: сначала определить источник drift. Drive остаётся authoritative.

## Topview как производственный источник наблюдений

Подключённый Topview можно использовать **read-only** для сверки реального производства: список boards/tasks, состояние задачи, модель, параметры, prompt, время запуска/завершения и наличие результата. Это полезный дополнительный источник для проверки, действительно ли ролик запускался, завершился или каким движком делался.

Но Topview **не является вторым master**:
- creative intent, scene ID, production state и slow-lock канонически фиксируются в Drive `video-prompts.md`;
- сопоставлять Topview task со сценой можно только при достаточно однозначном совпадении prompt/reference/model/context;
- неоднозначную задачу не привязывать к scene ID автоматически;
- Topview сам по себе не переводит сцену в `APPROVED`, `IN_EDIT` или `CLOSED` и не разрешает удалять prompt;
- `render_state` в `project-status.json` по-прежнему вычисляется только из canonical slow-list master;
- найденный в Topview `success` означает, что генерация технически завершилась, но не означает, что дубль принят пользователем.

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

## scene-meta

`scene-meta` — optional structured layer. Его отсутствие допустимо. Если он есть, он не должен дублировать slow-state вручную.

Разрешённые conceptual fields:
- `target_engine`;
- `production_state`;
- `duration_s`;
- `dialogue`;
- `dependencies`;
- `tags`.

Dependency targets обязаны указывать на существующие active scene IDs. Prose inference не является authoritative dependency state.

Не вставлять metadata массово во все сцены только ради заполнения полей. Добавлять постепенно и проверяемо.

## Integrity check master

Перед записью/публикацией проверить:
- declared scene count = количество `## Сцена N`;
- declared scene count = количество TOC rows;
- TOC IDs = section IDs;
- ID уникальны и возрастают; непрерывность не требуется;
- declared prompt count = число fenced prompt blocks;
- W-count = число W-items;
- slow-count/list совпадает с dedicated slow block, TOC и sections;
- нет старой версии изменяемой сцены в другом месте;
- присутствующий `scene-meta` валиден;
- dependency targets существуют.

## Обычный sync

1. Fresh-read Drive master.
2. Внести только утверждённую правку в тот же Drive file ID.
3. Обновить `SYNC-TRIGGER.txt`.
4. Дождаться `sync-from-drive.yml`.
5. Проверить Actions success.
6. Проверить `project-status.json` → `health: ok`.
7. Проверить fingerprint/counts/slow list.
8. Проверить успешный GitHub Pages deployment.
9. Проверить raw/site на изменённую фразу/статус.
10. Только после этого сообщить `ГОТОВО`.

`instruction_sync: stale/unverified` сам по себе routine scene edit не блокирует, если instructions в этой операции не менялись. `instruction_sync: error` означает фактический drift/read failure и должен быть отдельно разобран.

Library/Notion/Drive HTML при routine edit не трогать без отдельной причины.

## Instruction edit / architecture edit

Если изменяется одна из пяти Drive-инструкций:
1. редактировать тот же Drive file ID;
2. считать Drive версию authoritative;
3. обновить соответствующий GitHub mirror;
4. не делать инструкцию публичной в Drive только ради GitHub Actions;
5. проверить содержимое/хэш Drive↔GitHub доступным authenticated способом;
6. выполнить full checkpoint, если изменение архитектурное;
7. после изменения инструкции обновить её GitHub mirror и дождаться новой авторизованной проверки; ожидаемый финальный статус — `instruction_sync.health = ok`.

## Полная ручная синхронизация всего и везде

При explicit full checkpoint / architecture change:
1. fresh-read Drive master;
2. проверить целостность master;
3. проверить `project-status.json` schema/fingerprint;
4. обновить Drive `video-prompts.html` при необходимости;
5. привести пять Drive-инструкций к актуальной архитектуре;
6. обновить GitHub master/изменённые instructions/site files;
7. trigger/дождаться `sync-from-drive.yml`;
8. проверить Actions success;
9. проверить `project-status.json` health + fingerprint;
10. проверить Pages deployment success;
11. обновить Library master/HTML/instructions/site reserve при наличии;
12. обновить Notion Hub и instruction pages;
13. end-to-end проверить raw master и public viewer;
14. сообщить `ГОТОВО` только если обязательные пункты подтверждены; отдельно перечислить всё, что осталось `stale`, `unverified` или `error`.

## Как обслуживать сайт

- Источник scene content — GitHub root `video-prompts.md`.
- `index.html` только отображает master/status.
- UI использует schema v3, но не становится editable source-of-truth.
- Пользовательские статусы/служебные подписи выводить по-русски; machine enums в JSON не переименовывать.
- Фильтры по state/engine/dialogue/dependencies показывать только при наличии подтверждённых `scene_meta`.
- `NEEDS_FIX` на сайте означает «нужно обсудить/скорректировать», но не запускает автоматическое изменение prompt.
- Медленная генерация берётся только из machine `slow_scenes` / generated `render_state`, а не из hard-coded списка в HTML.
- После изменения master проверять Pages deployment и публичную ревизию.
- Если сайт кажется старым: Drive → GitHub root → `project-status.json` → Pages deployment → viewer.
- `Seregius_montazhny_razbor.html` публикуется отдельной rendered Pages page.

## Notion

Notion Hub — navigation/documentation hub, не второй master. Live counts/timestamps брать из master/`project-status.json`, не дублировать как источник истины.

## Library

Library — резерв ChatGPT. Никогда не считать её свежее Drive без проверки. Routine sync от Library не зависит.

## Recovery

При потере чата:
1. `NEW-CHAT-HANDOFF.md`;
2. этот `SYNC-RUNBOOK.md`;
3. `AI-PROJECT-GUIDE.md`;
4. fresh Drive `video-prompts.md`;
5. `project-status.json` fingerprint;
6. при необходимости `film-analysis.md` + `film-backlog.md`;
7. проверить Pages.
