# AI Film Project — Start Here v3.5

Эта инструкция задаёт стартовые правила для ChatGPT, Work, Claude, Gemini, DeepSeek, Grok и других ИИ, работающих с проектом.

## Safety summary v3.5

Полный нормативный operational block находится в `SYNC-RUNBOOK.md`. Даже если открыт только этот файл, соблюдать минимум:

- Единственный редактируемый prompt master: Google Drive `AI Film Prompts Master/video-prompts.md`, file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
- GitHub `virudik/ai-film-prompts` — публичное read-only зеркало и источник GitHub Pages, не второй master.
- Пять Drive-инструкций (`AI-PROJECT-GUIDE.md`, `SYNC-RUNBOOK.md`, `USER-GUIDE.md`, `README-AI-SYNC.md`, `CLAUDE-TAKEOVER-RUNBOOK.md`) — канонические для своих GitHub-зеркал. Их GitHub-копии нельзя считать свежее Drive без проверки.
- `project-status.json` — автоматически генерируемый machine-status schema v3; вручную его не редактировать.
- Перед записью в master обязательно fresh-read Drive master. Scene ID стабильны и не перенумеровываются после удаления.
- Slow-generation — отдельное render-state. Сцену с `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` нельзя запускать повторно без результата/ошибки или отдельного разрешения пользователя.
- `index.html` — viewer, не master. Library/Notion/Drive HTML — backup/documentation layers, не gate routine edit.

## V3.5 machine state

`project-status.json` schema v3 сохраняет старые top-level поля и дополнительно содержит:

- `canonical_master_sha256` и размер канонического master;
- `audit_fingerprint` — revision, hash, scene/prompt counts, scene IDs, W-items, slow list и health;
- `scene_meta` — optional validated metadata по сценам;
- `render_state`, вычисляемый из существующего slow-list (`SLOW_PENDING` / `IDLE`), а не из пятого ручного статуса;
- `instruction_sync`.

Приватные Drive-инструкции автоматически сверяются через авторизованное подключение Google Drive в ежечасной automation `Topview Slow Watch`. Результат пишется в `instruction-sync-status.json`, а `project-status.json` учитывает его свежесть.

Допустимые состояния:
- `instruction_sync.health = ok` — все пять Drive-инструкций совпадают с GitHub-зеркалами, авторизованная проверка свежая;
- `stale` — последняя проверка старше 3 часов;
- `error` — найдено расхождение или файл недоступен;
- `unverified` — авторизованный snapshot отсутствует/невалиден.

GitHub Actions **не получает Google Drive credentials** и не должен пытаться скачивать приватные инструкции анонимно.

## Управление через AI Film Control Center

Публичный `index.html` — read-only Control Center поверх `video-prompts.md` + `project-status.json`.

Пользовательский интерфейс должен быть русским. В частности:
- `Slow` → **Медленная генерация**;
- `Work` → **В работе**;
- `Revision` → **Ревизия**;
- `Sync` → **Синхронизация**;
- `instruction_sync.health = ok` → **Инструкции: ПРОВЕРЕНЫ**;
- `stale` → **Инструкции: ПРОВЕРКА УСТАРЕЛА**;
- `error` → **Инструкции: НАЙДЕНО РАСХОЖДЕНИЕ**;
- `unverified` → **Инструкции: НЕ ПРОВЕРЕНЫ**;
- `Audit fingerprint` → **Контрольный отпечаток**;
- текст статуса instruction-sync показывать по-русски и явно отличать `stale/unverified` от фактического drift.

Machine enum-значения (`READY`, `NEEDS_FIX`, `NEEDS_RERENDER` и т. п.) остаются стабильными в JSON, а сайт отображает их русскими подписями.

`NEEDS_FIX` означает **кандидат на отдельное обсуждение/корректировку**, а не команду автоматически переписать prompt. `NEEDS_RERENDER` означает, что существующий результат уже требует нового дубля/повторной генерации, но slow-lock и явное решение пользователя всё равно имеют приоритет.

## Audit freshness rule

Перед внешним аудитом или большой правкой сначала повторить fingerprint, который фактически виден в `project-status.json`:

- `revision_date`;
- `canonical_master_sha256`;
- `scene_count` / `prompt_count`;
- `scene_ids`;
- `work_items`;
- `slow_scenes`;
- `health`;
- `instruction_sync_health`.

Если snapshot расходится с текущим fingerprint — остановить аудит и обновить источники. Не анализировать старую сцену/старый slow-list как актуальные.

## Источник истины и контекст

Канонический prompt master — только Google Drive `AI Film Prompts Master/video-prompts.md`.

Для обычной правки одного промта достаточно fresh master + реальные reference images/videos нужной сцены.

Для story/continuity/placement дополнительно читать:
- `film-analysis.md` — factual map/current cut и ограничения;
- `film-backlog.md` — unresolved tasks/dependencies/recommendations.

Для глубокой структуры при необходимости:
- `Seregius_montazhny_razbor.html`;
- `EDIT_PLAN_V2.csv`;
- `PROGRESS.md`.

Не утверждать, что весь фильм был непрерывно просмотрен со звуком в реальном времени, если это не было фактически выполнено.

## Topview как производственный источник наблюдений

Подключённый Topview можно использовать **read-only** для сверки реального производства: список boards/tasks, состояние задачи, модель, параметры, prompt, время запуска/завершения и наличие результата. Это полезный дополнительный источник для проверки, действительно ли ролик запускался, завершился или каким движком делался.

Но Topview **не является вторым master**:
- creative intent, scene ID, production state и slow-lock канонически фиксируются в Drive `video-prompts.md`;
- сопоставлять Topview task со сценой можно только при достаточно однозначном совпадении prompt/reference/model/context;
- неоднозначную задачу не привязывать к scene ID автоматически;
- Topview сам по себе не переводит сцену в `APPROVED`, `IN_EDIT` или `CLOSED` и не разрешает удалять prompt;
- `render_state` в `project-status.json` по-прежнему вычисляется только из canonical slow-list master;
- найденный в Topview `success` означает, что генерация технически завершилась, но не означает, что дубль принят пользователем.

## Reference rules

- `@image1`, `@video1` и т. п. локальны для конкретной сцены.
- Для проверки внешности нужны реальные references; текстовое имя ref не заменяет изображение.
- Модель-лист/character reference имеет приоритет для внешности и одежды; environment/group refs вторичны.
- Для continuous take не смешивать требование непрерывного дубля с hard cuts/shot-reverse-shot/inserts без явной причины.
- Не вводить model-specific параметры как глобальное правило без проверки конкретного provider/model mode.

## Роли ИИ

### ChatGPT — основной редактор по умолчанию
При команде `добавь/измени/удали ... в мастер`:
1. fresh-read Drive master;
2. изменить только нужный блок;
3. сохранить тот же Drive file ID;
4. обновить связанные TOC/count/status;
5. обновить `SYNC-TRIGGER.txt`;
6. проверить workflow → `project-status.json` → Pages.

### Work
Использовать для многосценового, монтажного, backlog/analysis и широкого аудита. При записи в master — только тот же Drive file ID, без второго master.

### Claude
По умолчанию review-only. Если пользователь прямо назначает Claude временным основным редактором, Claude переходит на `CLAUDE-TAKEOVER-RUNBOOK.md` и сначала выполняет capability preflight.

### Gemini
Независимая проверка prompt + visual references. Не строить сайт/приложение только потому, что дан project URL.

### DeepSeek
Технический аудит: противоречия, тайминг, camera/action conflicts, overload, reference priority, negative constraints, continuity.

### Grok
Creative/comedy/pacing second opinion или red-team готового implementation plan. Не менять established continuity без запроса.

### Другие ИИ
Review-only по умолчанию. Привязывать рекомендации к точным scene IDs/names и сначала подтверждать audit fingerprint.

## Передача советов между ИИ

Внешний ИИ возвращает patch/replacement/recommendation. Канон меняет только один текущий редактор. Нельзя создавать `video-prompts-final`, `v2`, `copy`, `final-final`.

Consensus — evidence, not authority. Реальный актуальный master, validator и фактический результат генерации важнее количества голосов ИИ.

## Conflict priority

1. текущая явная команда пользователя;
2. свежий Drive `video-prompts.md` для состояния master;
3. factual `film-analysis.md`;
4. `film-backlog.md`;
5. старые Notion notes;
6. память чата/старые копии.

## Публичные ссылки

- Viewer: `https://virudik.github.io/ai-film-prompts/`
- Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
- Repo: `https://github.com/virudik/ai-film-prompts`
- Film map: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-analysis.md`
- Backlog: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-backlog.md`
- Montage review: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`
- Sync runbook: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/SYNC-RUNBOOK.md`
- Claude takeover: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/CLAUDE-TAKEOVER-RUNBOOK.md`