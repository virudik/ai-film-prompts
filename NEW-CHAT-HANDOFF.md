# NEW CHAT HANDOFF — AI Film Project

**Checkpoint:** 22.09.2026  
**Назначение:** единая актуальная точка передачи следующему чату. Если старый chat summary, Notion note, Library copy или исторический commit противоречат этому файлу и live sources, сначала проверять live authority, а не продолжать старое предположение.

## 0. CURRENT CHECKPOINT — 22.09.2026

Этот блок — быстрый вход для сменщика; подробные правила ниже остаются обязательными.

- Fresh runtime authority: Drive master + `project-status.json`; на текущем snapshot активные Scene ID: `1,2,3,4,5,10,11,13,16,17,19,20`, `health: ok`.
- Fresh Topview snapshot на момент передачи: capacity `6`, occupied `6`; UI обязан считать **tasks/slots**, а не уникальные Scene ID.
- Компактная строка Topview на сайте: **`занято X из 6 · DD.MM.YYYY, HH:MM:SS`**. Не показывать `свободно Y` и не писать `синхр.`. Timestamp — обычный цвет/вес текста.
- `PROMPT-STYLE-GUIDE.md` обновлён до **v1.3 / 22.09.2026** и является единственным prompt-writing standard.
- Prompt guide теперь prompt-only: Topview runtime/slot contract живёт в `SYNC-RUNBOOK.md`; полные копии live-сцен не считаются каноническими примерами.
- Главный принцип prompt-writing: **maximum useful specificity, minimum redundant wording**.
- Каждый отдельно копируемый production prompt самодостаточен: short real `CHARACTER APPEARANCE / IDENTITY LOCK`, reference ownership/priority, feasible timing, coherent camera/space, risk-specific negatives, START/END state для последовательностей где полезно.
- Качество legacy prompts проверяется **семантически**, а не буквальным grep по названию секции. Новые/перерабатываемые prompts приводятся к актуальному формату.
- Не спрашивать пользователя повторно об известной внешности/continuity: resolve из fresh `character-references.json` + master/current variant.

## 1. TAKEOVER GATE — прочитать до любой работы

Новый чат **не вступает в роль редактора**, пока не прочитал весь обязательный seven-document set:

1. `NEW-CHAT-HANDOFF.md` — этот файл
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

Затем обязательно:
8. fresh Google Drive `video-prompts.md`, ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
9. live GitHub `project-status.json`
10. live `topview-status.json`
11. live `instruction-sync-status.json`

Для сюжета/монтажа дополнительно:
- `film-analysis.md`
- `film-backlog.md`
- при необходимости `PROGRESS.md`
- `Seregius_montazhny_razbor.html`
- релевантные страницы Notion `Кино`.

Перед любой записью в master — ещё один fresh-read exact Drive master.

**Не спрашивать пользователя повторно то, что однозначно уже записано в этих источниках.**

## 2. Source of truth / storage roles

### Google Drive — authority
Folder `AI Film Prompts Master`  
ID `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`

Editable prompt master:
`video-prompts.md`  
ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`

Canonical seven docs:
- Handoff `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- Sync Runbook `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- Project Guide `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- Prompt Style Guide `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`
- User Guide `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- README AI Sync `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- Backup AI Runbook `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`

### GitHub
Repo `virudik/ai-film-prompts`  
Mirror + status + site + Pages. Not editable prompt authority.

### Notion
`Кино` = story/ideas/history bank.  
Operational page = `AI Film — Актуальная инструкция / Handoff`.  
`Важные промты` = legacy prompt bank, не current style authority.

### ChatGPT Library
Recovery mirror/cache. Never override accessible Drive.

### Topview
Read-only render telemetry. `success` != approval.

### Supabase
Comments backend only; no prompt/master rights.

## 3. Current live project checkpoint

На checkpoint после Scene 20:
- 12 active scenes
- 24 full prompt texts
- W5, W7, W8
- active IDs: `1,2,3,4,5,10,11,13,16,17,19,20`
- deleted/reserved IDs: `6,7,9`
- canonical slow: `2,3,4,5,13,19`
- latest Scene ID: `20`

Runtime SHA/counts/status всё равно fresh-check по `project-status.json`; checkpoint здесь нужен только для takeover orientation.

## 4. Current scene decisions

- Scene 2 — canonical slow rerun, Seedance 2.5.
- Scenes 3, 4, 5 и 13 — существующие canonical Scene IDs с новыми running Topview tasks; task↔Scene mappings подтверждены по exact/normalization-equivalent canonical prompts, поэтому они canonical slow без создания новых Scene ID.
- Scenes 12, 14, 15 и 18 — **отработаны и удалены из active master** по прямому решению пользователя. Это retired Scene IDs: не возвращать в active set и не переиспользовать их номера без нового прямого решения пользователя.
- Scene 19 `Рыбалка и Маша-Лагуна` — active + slow, Wan 3.0, 30s.
- Scene 20 `Маша-Лагуна: рок-припев у озера` — active, READY, Seedance 2.5, 30s, **не slow**.
- Scene 17 остаётся active post-monster continuation.
- 6/7/9 не восстанавливать и не переиспользовать без прямого нового решения пользователя.

## 5. Scene 20 — latest added scene

`Маша-Лагуна: рок-припев у озера`

- Seedance 2.5
- 30s
- READY / IDLE
- @Image1 = location/lakeshore only
- @Image2 = exact Masha identity
- one continuous stable music-performance shot
- original English chorus; prompt **не упоминает название группы или существующей песни**
- master-level structure по `PROMPT-STYLE-GUIDE.md`
- `FRAME FILL / NO BARS`

Используемый оригинальный chorus:
`Hear the silence, hear it calling,`
`Through the dark, the echoes falling,`
`In my heart the fire is rising,`
`Still I stand, no more disguising.`

Если будущий edit касается этой сцены — fresh-read Scene 20 из Drive, не использовать handoff как prompt body.

## 6. Prompt-writing standard

`PROMPT-STYLE-GUIDE.md` — обязательная полная инструкция, а не памятка.

Новый/существенно перерабатываемый prompt:
1. fresh guide;
2. fresh master;
3. 1–2 current related master scenes;
4. current engine/reference assignment;
5. master-level prompt.

Требуемый уровень обычно включает:
- tech line;
- exact References;
- identity/reference priority;
- scene/style/environment;
- timeline/story flow;
- camera/continuity;
- performance;
- dialogue/vocals/lip sync;
- lighting/material realism;
- native audio;
- scene-specific negative prompt;
- `FRAME FILL / NO BARS`.

Если новый prompt заметно проще лучших current master scenes без объективной причины — он не готов.

Следующий Scene ID не спрашивать, если он однозначен: использовать следующий unused stable ID.

## 7. Routine master write

`fresh Drive master`
→ minimal edit same Drive ID
→ `SYNC-TRIGGER.txt`
→ `sync-from-drive.yml`
→ validation
→ exact GitHub mirror
→ `project-status.json`
→ Pages
→ verification
→ report.

Никаких duplicate master files.

## 8. Current Control Center baseline

Viewer:
`https://virudik.github.io/ai-film-prompts/`

Уже реализовано:
- Russian UI;
- active scene navigation + full prompts;
- merged canonical slow / Topview table;
- model/status/start/elapsed/queue/ETA;
- three-state sync lightsaber;
- character/reference viewer;
- light/dark side switch; `localStorage: ai-film-theme`;
- collapsible `Контрольный отпечаток`;
- сразу под ним отдельная collapsible секция `💬 Комментарии, идеи и предложения`;
- native comments/replies через Supabase без GitHub account.

Старой кнопки `Архив GitHub` нет.

## 9. Supabase comments — current architecture

Organization: `Vint`  
Project: `ai-film-comments`  
Ref: `vzohfatqzyioydtgjiyd`

- public read published comments;
- anonymous post;
- threaded replies via `parent_id`;
- Edge Function `submit-comment`;
- RLS;
- honeypot;
- rate limit 5 messages / 10 minutes / IP;
- only publishable key in frontend;
- `service_role`/admin secret never in public HTML;
- no master/Scene ID/slow/approval/generation permissions.

## 10. Site-only changes

Permanent scene/prompt content must not be hard-coded into `index.html`.

After site edit:
- JS syntax check;
- duplicate IDs;
- secret scan;
- Pages build verification.

Если site change становится постоянной функцией, выполнить Documentation Duty ниже.

## 11. DOCUMENTATION DUTY — обязательное правило всех следующих чатов

Любое **материальное нововведение**, влияющее на будущую работу, не считается завершённым одной реализацией.

К material change относятся:
- новая постоянная функция сайта;
- новый backend/integration;
- новое обязательное правило prompt-writing;
- изменение workflow/sync;
- изменение authority/source-of-truth;
- новый status/recovery behavior;
- изменение takeover procedure.

В том же рабочем цикле нужно:
1. обновить relevant canonical Drive docs;
2. обновить SAME `NEW-CHAT-HANDOFF.md`;
3. обновить SAME `PROMPT-STYLE-GUIDE.md`, если касается prompt-writing;
4. exact-mirror all affected docs Drive → GitHub;
5. refresh `instruction-sync-status.json`;
6. проверить `project-status.json`/Pages;
7. обновить Notion operational pointer;
8. обновить Library recovery copies;
9. не создавать `v2/final/copy`.

Эфемерные runtime facts (queue/ETA/current SHA) не размножать во все docs.

## 12. Instruction sync

`AI Film Recovery Sync` должен читать и сравнивать **все семь** обязательных документов.

Repair direction:
**Drive → GitHub only**.

`instruction-sync-status.json` должен включать all seven docs, а не старый five-file set.

Если instruction status stale — обновить verification; это не повод считать master повреждённым.

## 13. Topview rules

Canonical slow membership = fresh `project-status.json.slow_scenes`.

Exact task mapping:
- compare with fresh scene body;
- no stale-title matching;
- queue/ETA per exact task;
- no guessed task;
- no auto rerun;
- no auto approval;
- technical completion never means approval; a tracked scene leaves slow automatically only when its last active Topview task becomes terminal.

## 14. Story / film priorities

Основные незакрытые направления:
- W5 — Канцлер / Warcraft 3 / мотивация и payoff;
- W7 — переходы между крупными группами;
- W8 — transport/racing continuity;
- Scene 17 — последствия monster battle / карта;
- дальнейшие идеи из Sasha/Notion — только после проверки master/backlog.

Не массово переписывать NEEDS_FIX/NEEDS_RERENDER. Разбирать по одной сцене.

## 15. Notion / Library

Notion:
- банк сюжета и истории;
- operational pointer должен отражать current workflow;
- старые prompt pages не использовать как master.

Library:
- recovery mirror/cache;
- после material instruction changes refresh all seven docs;
- также поддерживать `READ-FIRST.txt`, `CURRENT-STATE.json`, `SITE-STATUS.md`, `SHIFT-HANDOFF.md` и recovery package, если он используется;
- accessible Drive всегда сильнее Library copy.

## 16. Known recovery history

Известные классы инцидентов:
- non-fast-forward from concurrent GitHub writers;
- UTF-8 BOM;
- stale validator filename;
- stale current-state prose;
- false Topview mismatch due to old scene snapshot.

Current rules:
- refetch/rebuild/retry;
- master UTF-8 without BOM;
- runtime truth from live sources;
- historical/checkpoint text != current invariant;
- Topview task checked against fresh scene body.

## 17. Как вести себя следующему чату

Следующий чат должен сразу уметь:
- продолжать работу без повторного онбординга пользователя;
- читать/писать SAME Drive IDs;
- сам определять следующий Scene ID;
- писать prompts в master style;
- менять сайт и проверять Pages;
- поддерживать all-seven instruction mirrors;
- фиксировать material changes в docs/HANDOFF/Notion/Library;
- отличать telemetry от approval;
- не объявлять `ГОТОВО` до verification.

Если инструментально какой-то шаг невозможен, назвать **конкретно** невозможный шаг, а не утверждать общо, что «нет доступа», не проверив подключённые инструменты.

## 18. ОБЯЗАТЕЛЬНО: персонажи / референсы перед вступлением в роль

После seven docs + fresh master/live JSON следующий чат обязан открыть Control Center → **Персонажи / Референсы** (`references.html`) и прочитать `character-references.json` без протаскивания огромных base64 image payload в рабочий текст. Нужно построить compact name map и сопоставить его с current prompts.

Current global registry:
- **Серёга** — aliases `Канцлер`, `The Chancellor`; естественное `Серёжа` при однозначном контексте → Серёга.
- **Юля**.
- **Паша** — `JEDI-A`, `Navy Jedi`.
- **Артём** — `Bearded Jedi`.
- **Илюша** — `Hooded Jedi`.
- **Саша** — `JEDI-B`, `Glasses Jedi`.
- **Лёша** — `PURPLE`.
- **Виталик** — `BLACK`.

Approved individual model sheets are identity authority. Current master is current scene-usage authority. Scene-specific characters not in global registry are resolved from fresh scene references.

Практическое правило: запрос пользователя `Паша говорит Саше; потом заходит Серёжа` должен быть достаточен. Следующий чат сам подставляет правильные identities/model sheets/appearance/costume descriptions в master-level prompt и не просит пользователя повторить известную внешность.

## 19. ОБЯЗАТЕЛЬНО: монтажный разбор фильма перед вступлением в роль

До readiness report открыть сайт → **Монтажный разбор фильма** (`Seregius_montazhny_razbor.html`) и ознакомиться с current-useful содержанием: структура фильма, сюжетные пробелы, диалоги, переходы, финал, персонажи, рекомендации. Сверить с `film-analysis.md`, `film-backlog.md`, при необходимости `PROGRESS.md` и Notion `Кино`.

Результат onboarding — компактная working map фильма, а не дословное удержание огромного HTML. Для конкретной монтажной задачи дочитывать релевантный раздел полностью. Facts / recommendations / manual-review items не смешивать.

## 20. FINAL TAKEOVER AUDIT — только после него можно сказать «готов»

Перед докладом пользователю новый чат обязан проверить и при необходимости актуализировать documentation/recovery layer относительно реального current state:
1. seven canonical Drive docs;
2. seven GitHub mirrors;
3. fresh `instruction-sync-status.json`;
4. fresh master ↔ `project-status.json`;
5. Topview/canonical slow consistency;
6. current Control Center permanent features;
7. character registry/reference viewer vs current prompts;
8. montage report + `film-analysis.md` + `film-backlog.md`;
9. Notion operational pointer / legacy labels;
10. Library recovery copies / READ-FIRST / current-state package.

Безопасный drift инструкций/mirrors исправить по Drive authority до readiness report. Нельзя автоматически менять творческий канон, scene approval или slow decision ради «согласования» документации — такие конфликты вынести пользователю.

Финальный доклад takeover должен содержать: **что прочитано и проверено; current scene/slow checkpoint; понимание character map и film priorities; были ли исправлены stale docs; какие реальные unresolved issues остались.** Только после этого: `готов продолжать работу предшественника`.

## 21. CURRENT AUTOMATION: Topview Scene Intake & Slow Watch

Старый `Topview Slow Watch` расширен и переименован в **`Topview Scene Intake & Slow Watch`**.

Он теперь:
- продолжает следить за canonical slow tasks, queue/ETA/status;
- ищет ранее неизвестные Topview **video-generation tasks** и обязан классифицировать каждую как: existing-scene render/retry, genuinely new scene или ambiguous;
- если actual Topview prompt exact/normalization-equivalent существующей active canonical scene (допустима только несемантическая нормализация `@image` ↔ `<<<Image>>>`, whitespace/reference-token formatting) либо есть explicit provenance, новый task привязывается к **существующему Scene ID**;
- если такой existing-scene task queued/running/init/processing — существующий Scene ID добавляется в canonical slow, сохраняя его editorial/production state; новый Scene ID не создаётся;
- одна лишь semantic similarity недостаточна ни для привязки, ни для тихого игнорирования; ambiguous task должен быть вынесен пользователю;
- genuinely new task с actual prompt/model metadata получает следующий stable Scene ID в SAME Drive master;
- actual Topview prompt новой сцены сохраняется verbatim; добавляются Russian title/context/references/summary;
- running genuinely new task делает новую сцену canonical slow;
- уже successful genuinely new task импортируется как `RESULT_RECEIVED`, не APPROVED;
- затем прогоняется normal Drive→GitHub validation/Pages и записывается task↔Scene mapping;
- non-video task игнорируется.

Следующий чат обязан при takeover проверить эту automation и помнить, что она имеет два ограниченных write-разрешения: **создать новую scene из genuinely new video task** и **привязать newly discovered running task к существующей canonical scene с добавлением её existing Scene ID в slow**. Это не разрешение auto-approve/rerun/delete/slow-clear существующих сцен и не разрешение переписывать existing prompt по одной semantic similarity.

## 22. Служебные файлы на сайте

В `Control Center → Служебные файлы` теперь опубликован полный seven-document takeover/recovery set русскими названиями:
- Передача дел новому чату
- Главная инструкция проекта
- Стандарт написания промтов
- Инструкция по синхронизации
- Схема синхронизации и хранилищ
- Инструкция владельца
- Инструкция резервного ИИ

Также доступны канонический master, карта/анализ фильма и рабочий backlog.

## 23. CURRENT RECOVERY AUTOMATION ARCHITECTURE

`AI Film Recovery Sync` теперь объединяет два уровня в **одной hourly automation**:
- **hourly light recovery** — быстрые проверки seven docs/mirrors, instruction status, master/status consistency, ключевых файлов сайта/референсов/контекста и security baseline;
- **daily deep audit** — раз в 24 часа внутри той же automation проверяются master structure, качество prompts относительно style guide, character mapping, монтажный контекст, Notion, Library, site, Supabase, GitHub Actions/Pages и recovery-readiness.

Cadence deep audit хранится в `deep-audit-status.json`. Missing/invalid/older-than-24h successful timestamp заставляет следующий hourly Recovery run выполнить deep audit. При material failure successful timestamp не продвигается, чтобы следующий run повторил аудит.

Отдельной daily automation нет. Отдельно остаётся только `Topview Scene Intake & Slow Watch`, потому что он работает с production tasks, queue/ETA и auto-import новых Topview video tasks в Scene IDs. Recovery Sync **не должен** создавать сцены или дублировать Topview intake.

Следующий чат при takeover обязан прочитать `deep-audit-status.json` вместе с остальными live status files и учитывать его warnings/unresolved в readiness report.

## 25. Служебные файлы: что является инструкцией, а что нет

На Control Center шторка **«Служебные файлы»** теперь визуально разделена на два блока.

### Инструкции — читать строго по порядку
1. `NEW-CHAT-HANDOFF.md` — Передача дел новому чату
2. `SYNC-RUNBOOK.md` — Инструкция по синхронизации
3. `AI-PROJECT-GUIDE.md` — Главная инструкция проекта
4. `PROMPT-STYLE-GUIDE.md` — Стандарт написания промтов
5. `USER-GUIDE.md` — Инструкция владельца
6. `README-AI-SYNC.md` — Схема синхронизации и хранилищ
7. `BACKUP-AI-RUNBOOK.md` — Инструкция резервного ИИ

Это и есть полный seven-document takeover/recovery set. На сайте эти семь кнопок располагаются **вертикально, одна под другой, в этом порядке**.

### Рабочие файлы проекта — НЕ инструкции
Эти три кнопки также отображаются **вертикально, одна под другой**, отдельным блоком после семи инструкций:
1. `video-prompts.md` — Канонический мастер промтов
2. `film-analysis.md` — Карта и анализ фильма
3. `film-backlog.md` — Рабочий бэклог фильма

Наличие этих трёх ссылок под той же общей шторкой не увеличивает число инструкций: это project data/context, а не дополнительные инструкции и не копии seven-document set. UI не должен смешивать их с seven-document list и не должен раскладывать их в две колонки.

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
12. **Over-capacity guard:** если из-за race/provider anomaly `occupied_slots > 6`, не скрывать проблему: показывать фактическое `занято X из 6 · DD.MM.YYYY, HH:MM:SS`, считать это warning и уведомлять пользователя/аудит.
13. **Никакой тяжёлой истории:** это правило не возвращает старую permanent `attempts[]` модель. `active_tasks[]` содержит только текущие активные задачи; после terminal state подробная telemetry не хранится бессрочно.
14. **Recovery/audit:** при проверке сайта и Topview state отдельно сверять `occupied_slots == len(active_tasks[]) == sum(len(active_by_scene[scene]))` и `free_slots == max(0, 6 - occupied_slots)`. Не сравнивать `occupied_slots` с количеством уникальных `slow_scenes`.


### Обязательное правило автономных prompts

Для любого prompt-блока, который копируется в Seedance / Veo / Topview отдельно, действует правило из `PROMPT-STYLE-GUIDE.md`: **каждый блок самодостаточен и содержит короткий `CHARACTER APPEARANCE / IDENTITY LOCK` с реальными отличительными признаками персонажа**. Нельзя оставлять production prompt зависимым от общего блока выше по странице. Известную внешность сменщик сам разрешает через `character-references.json` + fresh master/current variant и не просит пользователя повторять её.

Рабочий критерий: **один блок → одно копирование → references → generation**.

### Prompt-quality standard — current rule

Before writing or materially revising prompts, read fresh `PROMPT-STYLE-GUIDE.md` + fresh master. The production rule is **maximum useful specificity, minimum redundant wording**. Every independently copied prompt must be self-contained, carry short real appearance/identity locks for important characters, explicit reference ownership/priority when references can conflict, feasible timing, coherent camera/space, and risk-specific negatives. For sequences use compatible START STATE / END STATE where useful. Do not ask the user to re-specify known identity; resolve it from fresh registry/master. Do not rely on stale full prompt examples in docs. Legacy prompts are audited semantically, not by literal heading grep. Topview slot/runtime rules live in `SYNC-RUNBOOK.md`, not the prompt guide.


### UI decision — Topview compact header (22.09.2026)

User explicitly simplified the Topview header. The compact line to the right of `⏳ Сейчас в медленной генерации — Topview` must show **only**:

`занято X из 6 · DD.MM.YYYY, HH:MM:SS`

Show `занято X из 6 · DD.MM.YYYY, HH:MM:SS`. Do **not** show `свободно Y` or the label `синхр.`. The timestamp comes from `checked_at` and is rendered in ordinary text color/weight; `free_slots` remains telemetry only.

Current verified checkpoint while preparing this handoff:
- canonical master: **12 active Scene IDs / 24 prompt texts**;
- active Scene IDs: `1,2,3,4,5,10,11,13,16,17,19,20`;
- canonical slow scenes: `2,3,4,5,13,19`;
- Topview capacity: **6**, occupied active task slots: **6** at last verified fetch;
- `project-status.json`: `health: ok`;
- prompt standard is already refactored: prompt-only guide, no full copied live-scene examples, no Topview runtime contract inside it, and core rule **maximum useful specificity, minimum redundant wording**;
- every standalone production prompt must be self-contained and include short real appearance/identity locks for important characters.
\n\n---\n\n## ENGINE ROUTING — RUSSIAN DIALOGUE\n\n- Постоянное правило проекта: **любая сцена со слышимым разговорным диалогом на русском языке должна использовать Wan 3**.\n- Причина рабочего решения: Seedance 2.5 в текущем workflow недостаточно надёжен для естественной русской речи, произношения и lip sync.\n- Seedance 2.5 не назначать русскоязычной dialogue scene автоматически, даже если визуально он подходит лучше.\n- Исключение — только новая явная команда пользователя для конкретной сцены.\n- При fresh-read существующей сцены с `dialogue.language = ru` проверять, что `target_engine = Wan 3`; при существенной переработке исправлять старое engine assignment в рамках той же Scene ID.\n- Это routing-правило не означает автоматически перезапускать уже активную slow-задачу или менять одобренный результат без решения пользователя.\n