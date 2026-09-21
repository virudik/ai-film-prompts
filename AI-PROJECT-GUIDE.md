# AI Film Project — Start Here v4.0

**Дата актуализации:** 20.09.2026  
**Назначение:** главная операционная инструкция проекта для текущего редактора и любого следующего чата/сменщика.

## 1. Takeover gate — что обязательно прочитать до начала работы

Новый чат **не считается вступившим в роль редактора**, пока не прочитал весь обязательный набор из семи документов:

1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md` — этот файл
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

После них обязательно прочитать:
- fresh Google Drive `video-prompts.md`, file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`;
- live GitHub `project-status.json`;
- live `topview-status.json`;
- live `instruction-sync-status.json`;
- для сюжета/монтажа — `film-analysis.md` и `film-backlog.md`, а при необходимости `PROGRESS.md`, `Seregius_montazhny_razbor.html` и релевантные страницы Notion `Кино`.

Перед **любой записью** в prompt master нужен ещё один fresh-read exact Drive master.

Нельзя просить пользователя повторить то, что однозначно уже записано в этих источниках. Сначала найти ответ в каноне, затем действовать.

## 2. Источники истины и роли хранилищ

### Google Drive — канон
Папка: `AI Film Prompts Master`  
Folder ID: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`

Единственный editable prompt master:
- `video-prompts.md`
- Drive ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`

Канонические инструкции/recovery:
- `NEW-CHAT-HANDOFF.md` — `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- `SYNC-RUNBOOK.md` — `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `AI-PROJECT-GUIDE.md` — `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `PROMPT-STYLE-GUIDE.md` — `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`
- `USER-GUIDE.md` — `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` — `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `BACKUP-AI-RUNBOOK.md` — `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`

### GitHub — mirror + сайт + machine status
Repo: `virudik/ai-film-prompts`

GitHub содержит:
- публичное зеркало master;
- зеркало семи инструкций;
- `index.html` Control Center;
- `project-status.json`;
- `instruction-sync-status.json`;
- `topview-status.json`;
- references и служебные файлы;
- GitHub Pages.

GitHub `video-prompts.md` **не редактируется как второй master**.

### Notion — сюжет/идеи/история
База `Кино` остаётся банком идей, старого сценария, локаций и исторических промтов.  
Она не заменяет Drive master и не определяет current runtime state.

Актуальный операционный указатель в Notion:
`AI Film — Актуальная инструкция / Handoff`.

### ChatGPT Library — recovery mirror/cache
Library используется для аварийного восстановления и переносимости между чатами.  
Она **не является источником истины**, если доступен Drive.

### Topview — production telemetry
Topview сообщает task/model/status/queue/ETA/result.  
`success` означает только техническое завершение задачи и **не равен пользовательскому approval**.

### Supabase — comments backend
Project `ai-film-comments`, ref `vzohfatqzyioydtgjiyd`, organization `Vint`.  
Supabase обслуживает только комментарии сайта и **не получает прав на master, Scene IDs, slow-lock, approval или запуск генераций**.

## 3. Master: как вести `video-prompts.md`

- Редактировать только exact Drive file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
- Не создавать `v2`, `final`, `copy`, `final-final`.
- Перед каждой записью fresh-read master.
- Менять только нужную сцену и связанные с ней TOC/count/status/slow markers.
- Scene IDs стабильны и не перенумеровываются.
- Удалённые IDs не переиспользуются. В текущей истории зарезервированы как удалённые 6, 7, 9.
- Если следующий Scene ID однозначно определяется из fresh master, **не спрашивать пользователя**, а брать следующий новый стабильный ID.
- Готовую сцену удалять из active master только после пользовательского решения, что ролик принят и prompt больше не нужен.
- `Topview success` недостаточно для удаления сцены.
- `NEEDS_FIX` и `NEEDS_RERENDER` не дают автоматического разрешения на rewrite/rerun.
- Slow-сцены не перезапускать и не снимать с slow без результата/ошибки/явного решения пользователя.

## 4. Как писать промты

Полный обязательный стандарт: `PROMPT-STYLE-GUIDE.md`.

Перед новым или существенно перерабатываемым prompt:
1. fresh-read `PROMPT-STYLE-GUIDE.md`;
2. fresh-read exact master;
3. открыть минимум 1–2 актуальные близкие сцены master;
4. проверить engine, Scene ID и роли референсов;
5. только после этого писать prompt.

Master-level prompt обычно содержит:
- техническую строку;
- точные роли `References`;
- `IMPORTANT REFERENCE RULE` / приоритет identity;
- `SCENE` / style goal / environment;
- `TIMELINE` или `STORY FLOW`;
- `CAMERA / CONTINUITY`;
- `PERFORMANCE / ACTING`;
- dialogue/vocals/lip-sync, если применимо;
- lighting/material/production design;
- native audio;
- подробный scene-specific negative prompt;
- глобальный `FRAME FILL / NO BARS`.

Короткий generic prompt не считается готовым master prompt.

Глобальные правила continuity:
- единые внешность/одежда/свет/цветокоррекция/окружение;
- coherent 3D space;
- physically stable cinematic camera;
- controlled inertia;
- no random jitter / micro-shake;
- объекты раскрываются движением камеры, а не возникают из ничего;
- approved exact model sheet сильнее случайного визуального сходства.

## 5. Routine master write

Стандартный путь:

`fresh Drive master → minimal edit SAME file ID → update SYNC-TRIGGER.txt → sync-from-drive.yml → validation → GitHub mirror + project-status.json → Pages → final verification`

Перед словом `ГОТОВО` проверить:
- Drive содержит нужное изменение;
- GitHub mirror совпадает;
- validator зелёный;
- `project-status.json` отражает сцену;
- Pages build успешен;
- slow/Topview telemetry не была самовольно изменена.

## 6. Instruction / handoff maintenance

Есть **семь** обязательных project/recovery документов. Google Drive — их канон.

Любое материальное нововведение должно быть документировано **в том же рабочем цикле**, а не «когда-нибудь позже». Материальным считается:
- новая функция сайта;
- новый backend/service;
- изменение источника истины;
- изменение workflow/sync;
- новое обязательное правило prompt-writing;
- новый тип статуса;
- новый recovery procedure;
- изменение обязательного порядка takeover;
- новая постоянная интеграция.

Минимальный Definition of Done для материального изменения:
1. обновить релевантные Drive-инструкции;
2. обновить SAME `NEW-CHAT-HANDOFF.md`, если это важно следующему чату;
3. при изменении prompt-standard обновить SAME `PROMPT-STYLE-GUIDE.md`;
4. exact-mirror Drive → GitHub;
5. refresh `instruction-sync-status.json`;
6. проверить `project-status.json` / Pages, если изменение влияет на них;
7. обновить Notion operational pointer, если меняется способ будущей работы;
8. обновить Library recovery copies;
9. не создавать параллельные «новые финальные» инструкции.

Если меняется только временный runtime факт (queue, ETA, текущий SHA), не размножать его по всем инструкциям. Runtime truth берётся из live JSON/master.

## 7. Instruction sync

`AI Film Recovery Sync` должен проверять **все семь** обязательных документов:
- полный Drive text;
- одноимённый GitHub mirror;
- exact text match;
- семантические противоречия current rules.

Разрешённое автоматическое направление ремонта:
**Drive → GitHub only**.

Никогда автоматически:
**GitHub → Drive**.

`instruction-sync-status.json` должен содержать all seven files и не считаться актуальным, если snapshot устарел.

## 8. Control Center — текущий baseline

Control Center:
`https://virudik.github.io/ai-film-prompts/`

Текущие функции:
- русский UI;
- active scene map + full prompts;
- merged canonical slow + Topview telemetry;
- model/status/start/elapsed/queue/ETA;
- трёхсостоянийный sync lightsaber;
- character/reference viewer;
- светлая/тёмная тема, `localStorage` key `ai-film-theme`;
- `Контрольный отпечаток`;
- сразу под ним отдельная раскрывающаяся шторка `💬 Комментарии, идеи и предложения`;
- нативные Supabase comments: public read, anonymous post, replies, без GitHub login;
- кнопка старого `Архив GitHub` удалена.

Site-only UI change:
- править GitHub `index.html`;
- не hard-code scene/prompt content;
- после правки проверить JS syntax, duplicate IDs и Pages;
- если изменение становится постоянной функцией/архитектурным правилом — обновить инструкции/HANDOFF/Notion/Library по правилу раздела 6.

## 9. Comments security

Supabase comments:
- project ref `vzohfatqzyioydtgjiyd`;
- Edge Function `submit-comment`;
- public read published comments;
- anonymous posting;
- threaded replies через `parent_id`;
- RLS;
- honeypot;
- rate limit 5 сообщений / 10 минут / IP;
- frontend содержит только publishable key;
- `service_role`/admin secret запрещён в `index.html`;
- comments backend не может менять prompt master.

## 10. Slow / Topview

Canonical membership slow берётся из fresh master / `project-status.json.slow_scenes`.  
Пассивная Topview telemetry сама по себе не меняет master. Исключение — отдельная `Topview Scene Intake & Slow Watch`: она может создать genuinely new scene либо при доказанном newly discovered existing-scene render/retry добавить **существующий Scene ID** в canonical slow и обновить task mapping.

Для каждой сцены:
- использовать её exact verified task;
- `queueCount` брать только из этой task;
- provider ETA брать только из этой task;
- historical ETA держать отдельно;
- не копировать queue/ETA между сценами;
- если mapping не доказан — `verified=false`, ETA/queue не показывать как факт.

`success` → технически завершено, но canonical slow остаётся до решения пользователя.

## 11. Runtime state и исторические snapshot

Текущие counts, active IDs, slow IDs, SHA:
- fresh Drive master;
- live `project-status.json`.

Текущие Topview task/status/queue/ETA:
- live `topview-status.json` после exact mapping verification.

Исторические разделы, старые коммиты, письма GitHub Actions и старые Notion pages — evidence, не current authority.

Не объявлять систему сломанной по старому failure email, если после него есть новый successful run и live status здоров.

## 12. Resilience / известные сбои

Уже встречались:
- concurrent GitHub writers → non-fast-forward;
- UTF-8 BOM → strict header validation failure;
- старое имя backup-runbook в validator;
- stale runtime claims в документации;
- stale Topview mapping сравнивался со старым prompt.

Защита:
- sync refetch/rebuild/retry;
- raw master UTF-8 without BOM;
- current runtime facts не дублировать как eternal truth;
- mapping сравнивать с fresh canonical scene body;
- `instruction-sync-status.json` регулярно обновлять.

## 13. Как работать с Notion и Library

Notion:
- читать для story/ideas/history;
- новые сюжетные решения пользователя сильнее старых заметок;
- не переносить старый Notion prompt в master автоматически;
- поддерживать operational pointer актуальным при material workflow changes.

Library:
- recovery mirror/cache;
- обновлять копии семи инструкций/HANDOFF при материальных изменениях;
- не использовать Library-copy `video-prompts.md` как editable master при доступном Drive;
- recovery package/summary должен указывать Drive IDs и live-source hierarchy.

## 14. Поведение нового сменщика

Новый чат должен:
- сначала прочитать все семь документов;
- доказать доступ к exact Drive master и same-ID write перед редактированием;
- проверить live status;
- не спрашивать повторно известные IDs, роли хранилищ, Scene ID или правила prompt style;
- не «предлагать пользователю вставить самому», если инструменты позволяют выполнить каноническую запись;
- выполнять изменения до конца: write → sync → validation → mirror → Pages/status → documentation/recovery update, где применимо;
- ясно отделять факт, рекомендацию и то, что требует пользовательского решения.

Если capability same-ID Drive write недоступна в конкретном окружении, такой агент остаётся review-only и должен прямо сообщить ограничение, а не создавать новый master.

## 15. Персонажи / референсы — обязательный takeover слой

До доклада «готов продолжать» новый чат обязан открыть на Control Center вкладку `Персонажи / Референсы` (`references.html`) и прочитать `character-references.json`. Он формирует рабочую карту **каноническое имя → алиасы → exact model sheet → текущие scene usages → отличительные признаки/костюм** и сверяет её с fresh `video-prompts.md`.

Текущий глобальный registry содержит восемь подтверждённых model sheets: **Серёга (Канцлер / The Chancellor), Юля, Паша (JEDI-A / Navy Jedi), Артём (Bearded Jedi), Илюша (Hooded Jedi), Саша (JEDI-B / Glasses Jedi), Лёша (PURPLE), Виталик (BLACK)**. Естественный вариант имени `Серёжа` трактуется как `Серёга`, если контекст однозначен. Нельзя автоматически расширять алиасы до других людей с похожими именами.

Если пользователь пишет «Паша говорит Саше», «заходит Серёжа» и т. п., редактор **не просит заново описывать внешность**, а сначала разрешает имена через registry + current master. В prompt нужно сохранить каноническую identity, использовать approved model sheet как PRIMARY identity reference (если он прикреплён/доступен в задаче) и дать достаточное текстовое описание внешности/одежды/роли, чтобы модель не перепутала персонажей.

Если персонаж не входит в глобальный registry, но однозначно определён current master/scene references (например, Маша-Лагуна или конкретный офицер), использовать current scene reference mapping. Если имя реально неоднозначно и канон не позволяет установить личность, только тогда задать уточняющий вопрос.

`character-references.json` — registry/публикационный слой, а не второй prompt master. При конфликте current scene usage с устаревшим полем `scenes` сначала сверять fresh master; exact user-approved model sheet всегда сильнее случайного сходства группового кадра.

## 16. Монтажный разбор фильма — обязательный takeover слой

До доклада о готовности новый чат обязан открыть `Монтажный разбор фильма` на сайте (`Seregius_montazhny_razbor.html`) и ознакомиться как минимум с его structural analysis, сюжетными пробелами, рекомендациями по диалогам, финалу, переходам и персонажам. Затем сверить выводы с `film-analysis.md`, `film-backlog.md`, при необходимости `PROGRESS.md` и релевантным Notion `Кино`.

Цель — не запомнить весь HTML дословно, а построить компактную рабочую карту: **что в фильме уже есть → что подтверждено фактами → что является рекомендацией → какие сюжетные/монтажные пробелы остаются → какие идеи уже закрыты новыми сценами**.

Нельзя выдавать старую рекомендацию монтажного разбора за текущую задачу, если master/backlog/new user decision уже её superseded. Для глубокой монтажной работы читать нужный участок отчёта полностью.

## 17. Readiness audit перед докладом «готов»

После чтения источников новый чат обязан **проверить актуальность самой системы**, а не только принять документы на веру. Минимальный audit:
- seven Drive docs существуют и внутренне согласованы;
- GitHub mirrors совпадают с Drive;
- `instruction-sync-status.json` fresh и учитывает seven-file set;
- fresh master ↔ `project-status.json` согласованы;
- Topview telemetry не противоречит canonical slow membership;
- `references.html` / `character-references.json` доступны и mapping не явно устарел относительно current master;
- `Seregius_montazhny_razbor.html`, `film-analysis.md`, `film-backlog.md` доступны;
- Control Center содержит заявленные permanent features;
- Notion operational pointer и Library recovery не выдают себя за более свежий authority и не содержат очевидно устаревшие takeover rules.

Если найден безопасно исправимый documentation/mirror drift — исправить по правилам authority и только затем докладывать готовность. Если исправление может изменить творческий канон/master/approval, не угадывать: сообщить конфликт пользователю. Доклад готовности должен кратко перечислить, что проверено, текущий checkpoint и известные нерешённые вопросы.

## 18. Topview Scene Intake — new scene + existing-scene render binding

Автоматизация `Topview Scene Intake & Slow Watch` выполняет три функции:
1. обслуживает telemetry известных canonical slow-сцен;
2. обнаруживает previously unknown Topview video task, которая относится к **существующей active canonical scene**, привязывает её к existing Scene ID и при running/init/queued/processing ставит этот existing ID в canonical slow;
3. обнаруживает genuinely new Topview **video-generation task**, которой нет среди active canonical Scene IDs, и при достаточных данных импортирует её как новую Scene ID.

Классификация unknown task:
- image-only/non-video tasks игнорируются;
- exact/normalization-equivalent canonical prompt либо explicit provenance → existing-scene render/retry; новый Scene ID запрещён;
- normalization может игнорировать только несемантические различия `@image` ↔ `<<<Image>>>`, whitespace/line endings/reference-token formatting; model/duration/reference structure должны быть совместимы;
- одна semantic similarity / общая сюжетная тема не считается доказательством и не является основанием тихо отбросить task;
- clearly distinct task → genuinely new scene;
- ambiguous → no write, notify user.

Existing-scene binding:
- newly launched replacement/retry task может заменить прежний task mapping той же scene;
- queued/running/init/processing → existing Scene ID добавляется в canonical slow во всех связанных slow markers/table/TOC;
- editorial/production state (`READY`, `NEEDS_FIX`, `NEEDS_RERENDER` и т.п.) сохраняется независимо от render slow state;
- `success` → технически завершено, never `APPROVED`; duplicate Scene ID не создаётся;
- failed/cancelled → no auto-rerun.

Genuinely-new-scene import:
- task должен иметь concrete task ID, model и retrievable actual prompt;
- перед записью делается fresh-read exact Drive master;
- новый ID = следующий unused stable Scene ID; удалённые ID не переиспользуются;
- фактический prompt, отправленный в Topview, сохраняется **дословно как historical source prompt**; его нельзя задним числом «улучшать» и выдавать улучшенную версию за фактически использованную;
- рядом создаются русский заголовок, `Контекст использования`, `Референсы` (если известны) и `Что происходит`;
- known character names resolve через `character-references.json` + current master;
- queued/running/init/processing → новая scene входит в canonical slow;
- `success` → production state `RESULT_RECEIVED`, но не `APPROVED`;
- failed/cancelled task не rerun автоматически.

После любого canonical write обязателен normal Drive→GitHub sync, validation, `project-status.json`, Pages и task↔Scene mapping/telemetry refresh.

Это ограниченное исключение из общего правила «telemetry сама не меняет master»: разрешены только **создание genuinely new scene** и **добавление existing Scene ID в slow при доказанном newly discovered existing-scene render/retry**. Автоматика не может auto-approve/delete/clear slow, не может переписывать existing prompt по semantic similarity и не может автоматически rerun.

## 19. Служебные файлы на Control Center

Под раскрывающейся шторкой **«Служебные файлы»** сайт должен показывать полный seven-document set русскими названиями: передача дел новому чату, главная инструкция проекта, стандарт написания промтов, инструкция по синхронизации, схема синхронизации и хранилищ, инструкция владельца, инструкция резервного ИИ. Там же остаются канонический master, карта/анализ фильма и рабочий бэклог.

## 20. AI Film Recovery Sync: hourly light + daily deep

`AI Film Recovery Sync` — одна главная recovery/integrity automation с двумя уровнями внутри одного hourly schedule.

**Каждый час:** лёгкий контроль seven Drive docs ↔ GitHub, fresh instruction status, master/project-status consistency, наличие ключевых site/context artifacts, character-registry metadata, permanent site baseline и отсутствие публичных privileged secrets. Этот проход не перечитывает тяжёлый монтажный HTML, весь Notion/Library или Supabase security stack без причины.

**Раз в 24 часа внутри той же automation:** глубокий аудит master structure, prompt-style regressions, characters ↔ master, montage/film-analysis/backlog, Notion operational pointer, Library recovery, site JS/links, Supabase comments security, GitHub Actions/Pages и recovery-readiness. Cadence хранится в GitHub `deep-audit-status.json`. Если успешного deep audit нет или он старше 24 часов, следующий hourly run выполняет deep audit.

`deep-audit-status.json` фиксирует `last_deep_audit_at`, health по секциям, repairs, warnings и unresolved. Timestamp успешного deep audit обновляется только после реально завершённого глубокого прохода; при материальной ошибке следующий hourly run повторяет попытку.

`Topview Scene Intake & Slow Watch` остаётся отдельной automation: только она занимается Topview intake/slow telemetry и авторизованным учётом Topview render attempts и созданием новых Scene ID только из genuinely new Topview video tasks. Recovery Sync не создаёт сцены и не дублирует Topview intake.

## 22. Семь инструкций ≠ все ссылки в «Служебных файлах»

Seven-document set состоит ровно из семи canonical instruction/recovery файлов. На сайте они должны идти **одной вертикальной колонкой в обязательном порядке чтения 1→7**: HANDOFF → Sync Runbook → Project Guide → Prompt Style Guide → User Guide → README AI Sync → Backup AI Runbook.

`video-prompts.md`, `film-analysis.md`, `film-backlog.md` расположены ниже в отдельной группе **«Рабочие файлы проекта»**. Эти три кнопки тоже идут **вертикально, одна под другой**, в порядке: master → анализ → backlog. Это данные/контекст проекта, не дополнительные инструкции и не копии.

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
- `topview-status.json` stays compact: one current/primary telemetry snapshot per Topview-slow Scene ID plus `active_task_ids`. If several tasks are active, the newest active task is the primary row snapshot; all active IDs are still checked internally.
- Control Center deliberately shows **one compact row per Scene ID**, with no attempt counters, expansion UI or duplicate scene rows.
- A new Scene ID is created only for a genuinely new creative scene. Ambiguous classification means no master write and user notification.

Principle: **keep only the state required for correctness and deduplication; detailed render history is not a permanent project entity**.
