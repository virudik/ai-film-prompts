# USER-GUIDE v4.0 — AI Film Project


**Дата актуализации:** 22.09.2026  
**Для кого:** владелец проекта и любой чат/агент, который должен быстро понять, как проект устроен.


## 1. Главное правило


Единственный editable master промтов:


`Google Drive / AI Film Prompts Master / video-prompts.md`  
Drive ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`


GitHub, сайт, Notion и Library не являются вторым prompt master.


## 2. Что обязан прочитать новый чат


Перед вступлением в роль редактора новый чат читает **все семь** документов:


1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`


После этого:
- fresh Drive `video-prompts.md`;
- live `project-status.json`;
- live `topview-status.json`;
- live `instruction-sync-status.json`;
- при работе с сюжетом: `film-analysis.md`, `film-backlog.md` и релевантный Notion `Кино`.


Чат не должен заставлять пользователя повторять сведения, которые уже есть в этих источниках.


## 3. Как изменить существующую сцену


Правильный процесс:


1. fresh-read exact Drive master;
2. найти Scene ID;
3. проверить slow/status/dependencies;
4. если меняется сам prompt — прочитать `PROMPT-STYLE-GUIDE.md`;
5. сделать минимальную правку;
6. сохранить в **тот же Drive file ID**;
7. trigger GitHub sync;
8. дождаться validation/status/Pages;
9. проверить результат;
10. только после этого сообщить о завершении.


## 4. Как добавить новую сцену


Удалённые Scene IDs не переиспользуются.


Если следующий Scene ID однозначно определяется из fresh master, чат **сам присваивает следующий новый стабильный ID** и не спрашивает пользователя номер.


Новая сцена должна получить:
- TOC entry;
- anchor;
- title;
- `scene-meta`;
- контекст;
- references;
- human summary;
- полный master-level prompt;
- корректные counts/status.


Slow-marker добавляется только при реальном запуске/решении о canonical slow.


## 5. Как писать промты


Полная обязательная инструкция:


`PROMPT-STYLE-GUIDE.md`  
Drive ID: `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`


Она обязательна для всех новых и существенно перерабатываемых prompts.


Перед prompt work чат:
- перечитывает guide;
- перечитывает master;
- сверяется с 1–2 актуальными похожими сценами.


Обычно master-level prompt должен проработать:
- engine/technical parameters;
- exact reference roles;
- identity/reference priority;
- scene goal;
- timeline/story flow;
- camera/continuity;
- performance;
- dialogue/vocal/lip-sync;
- lighting/material/environment;
- native audio;
- scene-specific negative prompt;
- `FRAME FILL / NO BARS`.


Нельзя возвращаться к коротким общим промтам, если master использует более детальную режиссёрскую структуру.


## 6. Slow и Topview


Slow membership определяет master / `project-status.json`, а не Topview.


Topview даёт telemetry:
- task;
- model;
- status;
- start/finish;
- queue;
- ETA.


`success` = задача технически закончилась. Это **не означает**, что ролик принят.


Для Topview-managed scene slow означает наличие активной генерации: когда последняя отслеживаемая попытка завершается/падает/отменяется, automation снимает slow автоматически. Это не означает принятие ролика и не меняет editorial state.


## 7. Control Center


Сайт:


`https://virudik.github.io/ai-film-prompts/`


Текущий baseline:
- активные сцены и полные prompts;
- merged slow + Topview;
- модель/status/start/elapsed/queue/ETA;
- sync lightsaber;
- reference viewer;
- светлая/тёмная тема;
- `Контрольный отпечаток`;
- непосредственно под ним отдельная раскрывающаяся секция `💬 Комментарии, идеи и предложения`;
- comments/replies без GitHub account через Supabase;
- старой кнопки `Архив GitHub` нет.


Site-only правки делаются в GitHub `index.html`, затем обязательны JS syntax check, duplicate IDs check и Pages verification.


## 8. Комментарии


Supabase:
- organization `Vint`;
- project `ai-film-comments`;
- ref `vzohfatqzyioydtgjiyd`;
- Edge Function `submit-comment`.


Есть:
- public read;
- anonymous posting;
- replies;
- RLS;
- honeypot;
- rate limit 5 / 10 min / IP.


В публичном HTML запрещён `service_role`. Comments не могут менять master или запускать генерации.


## 9. Где что хранится


**Drive** — editable master и инструкции.  
**GitHub** — mirror/status/site/Pages.  
**Notion** — идеи, сюжет, история, старый prompt bank.  
**Library** — recovery mirror/cache.  
**Topview** — telemetry генераций.  
**Supabase** — comments backend.


Если источники конфликтуют, current prompt/runtime truth берётся из fresh Drive master + live status JSON, а не из старой Library/Notion копии.


## 10. Как фиксировать новые функции и правила


Если в проекте появляется постоянное нововведение — функция сайта, backend, новый prompt rule, workflow, status, источник истины, recovery step — недостаточно просто изменить код.


В том же цикле нужно:
1. обновить релевантные Drive-инструкции;
2. обновить SAME `NEW-CHAT-HANDOFF.md`;
3. обновить `PROMPT-STYLE-GUIDE.md`, если меняется prompt-writing;
4. зеркалировать в GitHub;
5. refresh `instruction-sync-status.json`;
6. проверить status/Pages;
7. обновить Notion operational pointer;
8. обновить Library recovery copies.


Это обязательный Definition of Done для материальных изменений.


## 11. Notion


Notion `Кино` остаётся полезным для:
- старого сценарного плана;
- идей;
- локаций;
- исторических промтов;
- альтернативных сюжетных решений.


Но это не текущий prompt master.


Операционный указатель:
`AI Film — Актуальная инструкция / Handoff`.


Страница `Важные промты` считается legacy bank и должна использоваться как inspiration/history, а не как актуальный стандарт.


## 12. Library


Library нужна для восстановления между чатами.


Она должна содержать свежие recovery copies семи инструкций и связанных summary/status файлов, но при наличии Drive:
**Drive всегда сильнее Library**.


## 13. Что новый чат не должен делать


- не спрашивать известный Scene ID, если он выводится из master;
- не просить пользователя вручную вставлять текст, если доступна запись;
- не создавать параллельный master;
- не брать GitHub/Library copy как editable authority;
- не массово переписывать NEEDS_FIX;
- не approve/rerun по Topview success;
- не использовать старый Notion prompt как новый master prompt без проверки;
- не считать старый GitHub failure email текущей аварией без live-check.


## 14. Как понять, что задача реально завершена


Master change:
Drive write → GitHub sync → validation → current status → Pages.


Instruction/material change:
seven Drive docs → seven GitHub mirrors → fresh instruction status → Notion pointer → Library recovery copies.


До этого слово `ГОТОВО` преждевременно.


## 15. Персонажи и обычные имена в запросах


Новый чат обязан заранее ознакомиться со вкладкой сайта **Персонажи / Референсы** и `character-references.json`. Поэтому пользователь может писать естественно: «Паша говорит Саше», «заходит Серёжа», «Лёша идёт рядом с Виталиком» — без повторного описания внешности.


Редактор сам связывает имя с approved model sheet и current master, а в prompt фиксирует каноническую внешность/костюм/роль и reference priority. Если персонаж scene-specific и не находится в глобальном registry, используются свежие references конкретной сцены. Уточнение нужно только при настоящей неоднозначности.


Текущие global names: Серёга/Канцлер, Юля, Паша, Артём, Илюша, Саша, Лёша, Виталик. `Серёжа` в однозначном контексте = Серёга.


## 16. Монтажный разбор как часть onboarding


Перед сообщением «готов продолжать» новый чат открывает на сайте **Монтажный разбор фильма**, затем сверяет его с `film-analysis.md` и `film-backlog.md`. Это нужно, чтобы он понимал не только отдельные prompts, но и весь фильм: структуру, сюжетные пробелы, переходы, диалоги, финал и уже предложенные исправления.


Он не обязан держать весь большой HTML в активном контексте дословно; обязан извлечь актуальную рабочую карту и при конкретной монтажной задаче дочитать нужный участок.


## 17. Финальный onboarding check


Новый чат докладывает о готовности **только после** проверки актуальности Drive, GitHub, сайта, instruction status, references, montage context, Notion pointer и Library recovery. Если документация безопасно устарела — сначала актуализирует её. Если обнаружено противоречие, которое меняет творческий канон или approval, сообщает его пользователю вместо самовольного решения.


## 18. Новая генерация Topview может сама появиться как сцена


Автоматизация теперь умеет импортировать **новую видеогенерацию Topview**, которой ещё нет в проекте:
- находит новую video task;
- определяет: это новая attempt уже существующей Scene ID или действительно новая творческая сцена;
- берёт настоящий prompt и модель из Topview;
- сама присваивает следующий Scene ID;
- создаёт описание сцены и сохраняет фактический prompt;
- любая новая active attempt существующей или новой сцены (`init/queued/running/processing`) добавляет/возвращает её Scene ID в slow;
- completed result помечает `RESULT_RECEIVED`, но не «принято»;
- синхронизирует Drive → GitHub → сайт.


Если данных недостаточно или непонятно, новая ли это сцена, автоматизация ничего не записывает и просит решение вместо угадывания.


## 19. Служебные файлы на сайте


В шторке **«Служебные файлы»** теперь должен быть виден полный набор из семи инструкций с русскими названиями, плюс master, анализ фильма и backlog.


## 20. Как теперь работает Recovery Sync


Отдельной ежедневной automation нет. Одна `AI Film Recovery Sync` запускается каждый час:
- обычно делает лёгкую проверку проекта;
- один раз примерно в 24 часа, когда это показывает `deep-audit-status.json`, в том же запуске выполняет глубокий техосмотр master, prompts, персонажей, монтажного анализа, Notion, Library, сайта, Supabase и GitHub Actions/Pages.


Topview остаётся отдельным процессом: `Topview Scene Intake & Slow Watch`. Это специально, чтобы production intake/очереди/создание новых Scene ID не смешивались с recovery-аудитом.


## 22. Почему в «Служебных файлах» больше семи кнопок


Инструкций по-прежнему **ровно семь**. Они идут сверху вертикально и пронумерованы 1–7 в порядке обязательного чтения.


Ниже отдельно находятся три рабочих файла, и их кнопки тоже идут **строго друг под другом**:
1. канонический master;
2. анализ фильма;
3. backlog.


Это не восьмая, девятая и десятая инструкции и не копии существующих документов.


## Canonical Topview state — minimal operational model


This is the permanent Topview rule for the master, watcher, recovery and Control Center:


- **Scene ID** identifies the creative scene. **Topview task ID** identifies one render attempt.
- A rerun/rerender/revised prompt for the same creative scene keeps the same Scene ID.
- Persistent Topview state is intentionally minimal:
  - `topview-task-map.json.active_by_scene` stores only currently active task IDs per Scene ID;
  - `topview-task-map.json.processed_tasks` stores only a bounded recent dedup/statistics journal: `task_id`, `scene_id`, `final_status`, `finished_at`;
  - keep at most the most recent 200 processed tasks and do not persist queue/ETA history or permanent `attempts[]` / `active_attempts[]` trees.
- `SLOW` / `SLOW_PENDING` means that a Topview-managed scene currently has at least one active task in `init`, `queued`, `running` or `processing`.
- A new active task for an existing scene adds/returns that same Scene ID to canonical slow.
- If several tasks of one scene are active, canonical slow still contains the Scene ID once; all active task IDs remain in `active_by_scene`.
- When one task becomes terminal (`success`, `fail`, `failed`, `cancelled`), remove that task ID from active state and append/update the minimal processed journal.
- When the **last Topview-managed active task** for that scene becomes terminal, remove the Scene ID from canonical slow automatically. This changes only render state: **never auto-approve, never auto-rerun, and do not change editorial/production state because rendering ended**.
- Never auto-clear a canonical slow scene when there is no proven Topview active mapping; unknown/manual slow state is not cleared by guess.
- `topview-status.json` stays compact but exposes transient `active_tasks[]`: one telemetry object for every task that is active **right now**. It also keeps the backward-compatible current/primary scene snapshot plus `active_task_ids`. No terminal task history, queue history or ETA history is stored there.
- Control Center slow table deliberately shows **one row per active Topview task / occupied slot**. Therefore the same Scene ID may appear in several rows when it has several simultaneous renders. This is a slot view, not a duplicate-scene model.
- A new Scene ID is created only for a genuinely new creative scene. Ambiguous classification means no master write and user notification.


Principle: **keep only the state required for correctness and deduplication; detailed render history is not a permanent project entity**.


### Точное ТЗ — Topview slow slots, capacity = 6


Это постоянный UI/automation contract:


1. **Ёмкость:** Topview допускает максимум **6 одновременно активных slow-generation tasks**. `slot_capacity = 6`.
2. **Что занимает слот:** каждый отдельный Topview `task_id` в состоянии `init`, `queued`, `running` или `processing` занимает **ровно 1 слот**.
3. **Scene ID и слоты — разные счётчики:** canonical `slow_scenes` остаётся множеством уникальных Scene ID без дублей. Число slow Scene ID **нельзя** использовать как число занятых слотов.
4. **Повторный запуск той же сцены:** если одна Scene ID одновременно запущена 2–3 раза, она остаётся одной canonical scene, но занимает 2–3 Topview slot и должна появляться 2–3 отдельными строками в slow-таблице сайта.
5. **Заголовок сайта:** справа от `⏳ Сейчас в медленной генерации — Topview` показывать компактно:
   - `занято X из 6 · DD.MM.YYYY, HH:MM:SS`
   - `X` = количество реально активных `task_id`;
   - дата и время берутся из свежего `topview-status.json → checked_at` и отображаются в локальном формате интерфейса;
   - **не выводить** слова/поля `свободно Y` и `синхр.`;
   - дата и время показываются **обычным цветом текста и обычным начертанием**, отдельно от цветовой индикации заполненности слотов;
   - `free_slots` остаётся внутренним telemetry/diagnostic полем и не удаляется из JSON.
   При текущих шести active tasks пример вида: **`занято 6 из 6 · 22.09.2026, 01:36:34`**.
6. **Таблица:** одна строка = один active `task_id` = один занятый slot. Сохраняются прежние 8 колонок и их базовые пропорции: `#`, `Сцена`, `Модель`, `Статус`, `Запуск`, `Прошло`, `Очередь`, `Оценка времени`. Новую колонку `Attempt`/`Task ID` не добавлять. Если Scene ID повторяется, номер и название сцены повторяются в нескольких строках.
7. **Telemetry:** `topview-status.json` должен содержать:
   - `slot_capacity`;
   - `occupied_slots`;
   - `free_slots`;
   - transient `active_tasks[]`, где на каждый активный task есть как минимум `scene_id`, `task_id`, `model/model_id`, `topview_status`, `started_at`, `checked_at`, `queue_count`, provider wait/process estimates и verification/mapping confidence, если известны.
8. **Точность строки:** queue/ETA/status/start time каждой строки берутся **только из того task_id, которому принадлежит эта строка**. Не усреднять и не переносить очередь/ETA между параллельными попытками одной сцены.
9. **Primary scene snapshot:** scene-level поля в `topview-status.json` можно сохранять для обратной совместимости/других частей сайта, но они **не являются источником slot-count** и не заменяют `active_tasks[]`.
10. **Завершение:** terminal task (`success`, `fail`, `failed`, `cancelled`) немедленно перестаёт занимать slot и удаляется из `active_tasks[]`/`active_by_scene`. В minimal `processed_tasks` можно оставить только дедуп-факт.
11. **Slow lifecycle:** если у Scene ID остаётся хотя бы один active task, Scene ID остаётся canonical slow. Если завершается последний Topview-managed active task, watcher снимает только render slow-state; approval/editorial/production state не меняются автоматически.
12. **Over-capacity guard:** если из-за race/provider anomaly `occupied_slots > 6`, не скрывать проблему: показывать фактическое `занято X из 6`, считать это warning и уведомлять пользователя/аудит.
13. **Никакой тяжёлой истории:** это правило не возвращает старую permanent `attempts[]` модель. `active_tasks[]` содержит только текущие активные задачи; после terminal state подробная telemetry не хранится бессрочно.
14. **Recovery/audit:** при проверке сайта и Topview state отдельно сверять `occupied_slots == len(active_tasks[]) == sum(len(active_by_scene[scene]))` и `free_slots == max(0, 6 - occupied_slots)`. Не сравнивать `occupied_slots` с количеством уникальных `slow_scenes`.




### Что система автоматически добавляет в prompt


Пользователю не нужно отдельно диктовать или копировать описание внешности уже известных персонажей. Для каждого автономного prompt-блока система сама добавляет короткий `CHARACTER APPEARANCE / IDENTITY LOCK` по approved model sheet/current scene variant. Поэтому любой отдельный prompt должен быть готов к схеме: **скопировать блок целиком → приложить указанные references → запустить генерацию**.


### Как теперь готовятся prompts автоматически


Пользователю достаточно описать сцену и приложить/указать нужные references. Система сама должна разрешить известных персонажей, встроить краткое описание внешности, назначить роли/приоритет references, проверить реалистичность тайминга, continuity и камеру, убрать лишние повторы и выдать автономный copy-paste prompt. Пользователь не должен собирать prompt из нескольких мест или заново диктовать уже известную внешность.

## Control Center — «Сейчас» (23.09.2026)

В верхней рабочей части Control Center есть компактный блок **«🎬 Сейчас»**. Он не является новым source of truth и ничего не записывает сам: это read-only рабочая сводка из fresh `project-status.json`, `topview-status.json`, `review-ledger.json` и названий сцен из master.

Четыре карточки: **«Генерируется сейчас»** (активные Topview task/slot; повтор Scene ID показывается как несколько попыток), **«Результат получен»** (technical `result_received`), **«Нужно ваше решение»** (полученный результат, по которому human review/accept/redo ещё не определены), **«Следующие действия»** (детерминированная подсказка: проверить результат, переделать по явному флагу, можно запускать READY idle, обсудить NEEDS_FIX). Клик по сцене переводит к её canonical prompt.

Блок не должен превращать Topview `success` в approval, не должен сам ставить `reviewed/accepted/needs_redo/inserted_into_film` и не должен запускать генерации.

## AUDIT HARDENING UPDATE — 24.09.2026

Этот блок фиксирует внедрённые после комплексного аудита правила. При конфликте со старым checkpoint/prose выше этот блок и fresh live sources имеют приоритет.

- Текущий подтверждённый canonical checkpoint после Scene 21: **11 active scenes / 21 prompt texts / latest Scene 21 / work items W5–W15 / health ok**. Active Scene IDs: `3,4,5,10,11,13,16,17,19,20,21`. Reserved/retired IDs: `1,2,6,7,9,12,14,15,18`.
- W6 не удалён: это рабочее направление **«Татуин: гигантский червь, карта и побег Канцлера»**. Диапазон рабочих направлений — W5–W15, всего 11.
- Scene 21 — current latest scene. Любой старый текст «latest Scene 20», «10 scenes / 20 prompts» или список только W5/W7/W8 является historical checkpoint, а не runtime truth.
- `project-status.json` обязан публиковаться даже при validator health != ok. Нельзя оставлять на Control Center старый зелёный snapshot только потому, что validator завершился non-zero. Generated non-green status записывается/публикуется, затем workflow может сообщить ошибку.
- Control Center считается зелёным только когда загруженный master соответствует `project-status.json.canonical_master_sha256`; stale green при несовпадении SHA недопустим.
- Instruction certificate freshness является частью health. `instruction-sync-status.json` должен подтверждать fresh exact-match всех **7/7** canonical Drive docs; contradictory hashes или stale certificate должны давать non-green status, а не молча приниматься.
- Recovery/integration tests не должны использовать жёстко зашитый исторический `synced_at`. Production snapshot test использует текущий `project-status.json.synced_at`, чтобы freshness-проверки тестировались относительно актуального production checkpoint.
- Workflow `AI Film integration recovery tests` должен запускаться при изменении самого integration test, validator, master и зависимых status/mapping/instruction artifacts. Исправленный прогон после audit hardening прошёл успешно.
- `deep-audit-status.json` и `recovery-manifest.json` — recovery metadata, не authority. После material canonical change они должны быть пересчитаны до текущего master fingerprint. Текущий verified checkpoint: 11 scenes / 21 prompts / latest Scene 21.
- Technical render success остаётся отделён от editorial state. `review-ledger.json`: `result_received` может выставляться по доказанному terminal success; `reviewed`, `accepted`, `needs_redo`, `inserted_into_film` — только человеческое/редакторское решение. Не auto-approve и не auto-rerun.
- `NEEDS_FIX` — не разрешение на автоматическую творческую перепись. Массовый auto-rewrite промтов по validator/audit запрещён; разбирать сцены по одной с учётом master и решения владельца.
- Не внедрять без отдельной реальной необходимости: третью конкурирующую automation/writer, тяжёлую permanent Topview attempt history, автоматический rerender, автоматический editorial acceptance, миграцию reference/base64 только ради размера, сложный anti-spam state machine или борьбу с каждым timestamp-only commit.
- Dependency order после material change: fresh authority → validator/generated status (включая честный non-green) → exact mirrors/certificates → deep-audit/recovery checkpoint → Control Center/Pages → read-back verification. Не объявлять изменение завершённым до успешной проверки опубликованного состояния.

## AUDIT VERIFICATION CLOSURE — 24.09.2026

- Topview watcher остаётся единственным штатным writer для Topview-derived render state. После recovery он должен быть `is_enabled:true`; при ручной аварийной сверке writer временно останавливается, затем обязательно включается обратно.
- Scene 3 task достиг technical `success` 23.09.2026 20:30:53 UTC. Scene 3 снята только с render slow-state и отмечена `result_received`; editorial approval не выводится автоматически. Current canonical slow после сверки: **4, 17, 19, 20**. Scene 20 занимает два task slots, поэтому current occupancy = **5/6 task slots** при четырёх unique slow Scene IDs.
- `review-ledger.json` использует **schema_version 2**. Validator и reconciler обязаны поддерживать поля `selected_result_task_id`, `result_url`, `film_version`, `insert_timecode`, `export_reviewed`; новые строки создаются сразу в schema 2. Human/editorial fields не выводятся из technical success.
- Recovery integration tests не должны закреплять конкретный live slow-набор или конкретную текущую сцену как вечный fixture. Production snapshot проверяется по общим invariants, переходы — на synthetic/invariant fixtures.
- `instruction-sync-status.json.github_blob` теперь проверяется против фактического Git blob текущего mirror-файла; `match:true` сам по себе недостаточен.
- Sync workflow различает ожидаемый validator `health=error` и фатальный сбой. Перед публикацией non-green status он обязан доказать, что JSON создан текущим invocation, parseable и его master SHA совпадает со свежим Drive master. Отсутствующий/stale status после exception не публикуется как свежий.
- Reconcile review-ledger использует safe retry/rebuild from fresh origin при concurrent GitHub writer, а не слепой повтор старого commit.
- `character-references.json` поле `scenes` трактуется как **current active scene usage**, не исторический архив. Historical/retired usage не должен выглядеть текущим.
- `film-backlog.md` current operational block должен отражать live состояние; старые FUTURE/NEXT design notes явно помечаются historical, если функция уже реализована.
- После material Topview/master transition обновляются operation journal, recovery manifest/deep-audit snapshot и Control Center dependency chain.

## CONTROL CENTER FILTER HYGIENE — 24.09.2026

- Левый набор фильтров Control Center должен строиться только из **актуального** `project-status.json.scene_meta` и текущих active scenes; historical/retired Scene IDs не должны создавать видимые фильтры.
- Все user-facing названия фильтров — **на русском**. Raw technical tags могут оставаться в `scene-meta`, но неизвестный/английский tag нельзя автоматически показывать пользователю без явного русского label/group mapping.
- Перед добавлением нового фильтра нужно проверить весь текущий набор тегов по всем активным сценам: частоту, смысл, дубли, синонимы и пересечение с уже существующими фильтрами `production_state`, engine, dialogue, dependencies и slow.
- Семантически одинаковые tags объединяются в **один** user-facing filter. Пример: `comedy` + `deadpan_comedy` + `fantasy_comedy` → `Комедия`; `music_performance` + `vocal_performance` + `cinematic_music_video` + `musical` → `Музыкальный номер`.
- Не выводить отдельные фильтры только потому, что tag существует. Узкие scene-specific tags, ведущие фактически к одной сцене (`map`, `lakeshore`, `mission_return`, `space_battle`, `character_identity` и аналогичные), обычно остаются метками сцены, но не засоряют левую панель. Исключение допускается, если singleton-фильтр имеет явную рабочую ценность для владельца (например `Музыкальный номер`, `Альтернативный вариант`, `Ручная проверка`).
- Не создавать дубль фильтра из tag, если тот же смысл уже покрывает workflow/state. Например `needs_fix` не должен дублировать `production_state=NEEDS_FIX`, а `dialogue` не должен выводиться второй кнопкой поверх основного фильтра `Диалог`.
- После добавления/удаления/существенного изменения сцен или их `scene-meta.tags` выполнить **filter audit**: пересчитать встречаемость tags, убрать stale/duplicate filters, объединить новые синонимы, проверить русский перевод и убедиться, что полезный новый тип сцен не потерян.
- Текущий baseline полезных tag-групп: `Экшен`, `Комедия`, `Непрерывный дубль`, `Связность сцен`, `Музыкальный номер`; workflow-specific singleton exceptions: `Альтернативный вариант`, `Ручная проверка`. Остальные фильтры формируются отдельно из status/engine/dialogue/dependencies/slow. Этот baseline не является вечным списком: его нужно пересматривать по fresh active scenes.
- После любого изменения фильтров обязательны read-back `index.html`, `Validate Control Center`, проверка отсутствия raw-English user-facing labels и успешный GitHub Pages deployment.

