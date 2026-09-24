# AI Film Project — Start Here v4.0


**Дата актуализации:** 22.09.2026  
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




### Prompt self-sufficiency / appearance lock


Каждый production prompt, предназначенный для отдельного копирования в генератор, обязан содержать собственный короткий `CHARACTER APPEARANCE / IDENTITY LOCK` с реальными отличительными признаками каждого важного персонажа. Источник — approved model sheet / `character-references.json` + fresh master/current scene variant. Общий scene-level identity bible может существовать только как документация; production prompt не должен ссылаться на него вместо собственного appearance lock. Не спрашивать пользователя повторно о внешности, если identity однозначно известна системе.


### Prompt quality / anti-bloat rule


Canonical prompt style is defined by fresh `PROMPT-STYLE-GUIDE.md`: maximize useful specificity while minimizing redundant wording. Standalone prompts must include their own short appearance lock, reference ownership/priority, feasible action/dialogue timing and continuity handoff when relevant. Shared scene bibles are documentation/continuity layers and must not make a copied production prompt dependent on external prose. Audit quality semantically; do not treat a missing literal heading in a legacy prompt as failure when equivalent protection is clear. Runtime Topview slot rules belong to `SYNC-RUNBOOK.md`.

---

## ENGINE ROUTING — RUSSIAN DIALOGUE

- Постоянное правило проекта: **любая сцена со слышимым разговорным диалогом на русском языке должна использовать Wan 3**.
- Причина рабочего решения: Seedance 2.5 в текущем workflow недостаточно надёжен для естественной русской речи, произношения и lip sync.
- Seedance 2.5 не назначать русскоязычной dialogue scene автоматически, даже если визуально он подходит лучше.
- Исключение — только новая явная команда пользователя для конкретной сцены.
- При fresh-read существующей сцены с `dialogue.language = ru` проверять, что `target_engine = Wan 3`; при существенной переработке исправлять старое engine assignment в рамках той же Scene ID.
- Это routing-правило не означает автоматически перезапускать уже активную slow-задачу или менять одобренный результат без решения пользователя.

## CONTINUOUS KNOWLEDGE TRANSFER — подтверждённые улучшения

Любое подтверждённое новое знание, улучшение, ограничение, удачная практика или изменение, которое может сделать будущую работу проекта качественнее, надёжнее или эффективнее, нельзя оставлять только в текущем чате.

- Сразу определить, к какой канонической инструкции относится новое знание, и записать его туда в том же рабочем цикле.
- Если знание важно следующему чату для продолжения работы, дополнительно обновить SAME `NEW-CHAT-HANDOFF.md`.
- Если оно меняет стандарт промтов, обновить SAME `PROMPT-STYLE-GUIDE.md`.
- Это относится в том числе к особенностям/ограничениям моделей, выбору engine, улучшениям prompt-writing, reference handling, continuity, генерации, монтажного workflow, сайта, sync/recovery, telemetry и новым способам предотвращения уже найденных ошибок.
- Не хранить такое знание только в переписке, памяти одного чата, временной заметке или историческом snapshot.
- Не размножать чисто эфемерные runtime-факты (queue/ETA/current SHA), если они не образуют нового постоянного правила.
- После записи выполнить обычный Documentation Duty / Drive → GitHub mirror / recovery update, чтобы правило пережило смену чатов.

Принцип: **если подтверждённая новая информация способна улучшить будущую работу — она должна пережить текущий чат через каноническую документацию.**

## CONTROL CENTER FILTER DEDUPLICATION

Постоянное правило UI: в боковом меню Control Center пользователь не должен видеть два фильтра с одинаковой подписью, даже если один пришёл из `production_state`, а другой из `tags`. `availableFilters()` должен дедуплицировать фильтры по итоговой пользовательской подписи. Например, `production_state=NEEDS_FIX` и `tag=needs_fix` отображаются как один фильтр `Нужна доработка`; каноническим считается state-фильтр, а семантически дублирующий tag-фильтр не добавляется.

### Invariant — согласованность slow-состояния во всех представлениях

При **любом** добавлении или снятии Scene ID из Topview-managed slow изменение считается завершённым только после атомарной сверки всех представлений. Обязательно проверить, что один и тот же набор уникальных slow Scene ID отражён одновременно в: (1) `video-prompts.md` — строке `РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС`, canonical slow-list, dedicated slow table, TOC badge и marker внутри секции сцены; (2) `project-status.json.slow_scenes` и `scene_meta[*].render_state`; (3) `topview-status.json.scenes` / `active_tasks[]` и `topview-task-map.json.active_by_scene` для Topview-managed active tasks; (4) Control Center — блоке `РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС`, таблице `Сейчас в медленной генерации — Topview` и `Активные сцены проекта — карта и навигация`.

Для Topview-managed сцены с хотя бы одним task в `init/queued/running/processing` Scene ID **обязан** присутствовать в canonical slow. После terminal последнего active task он **обязан** исчезнуть из canonical slow. Нельзя считать изменение законченным, если хотя бы одно из трёх пользовательских представлений сайта показывает другой набор/число slow-сцен. Slot count (`занято X из 6`) проверяется отдельно по `active_tasks[]`: при одном active task на каждую slow-сцену число совпадает, но архитектурно это разные величины.

## Reliability write contract — 23.09.2026

Permanent set-and-forget rule for technical project state:

- **One writer per derived state domain.** `Topview Scene Intake & Slow Watch` is the normal single writer for Topview-derived render state: `topview-task-map.json`, `topview-status.json`, canonical slow transitions, and Topview-derived fields in `project-status.json`. `AI Film Recovery Sync` verifies/repairs infrastructure and mirrors and must not race the watcher during normal operation.
- **Watcher watchdog.** Recovery must verify that the Topview watcher is enabled and re-enable it if it became disabled without an explicit owner request. When either project automation is updated, preserve `is_enabled: true`; prompt/config edits must never silently disable it.
- **Fresh-read before every write.** Immediately before changing a canonical Drive file or GitHub state file, fetch the current authoritative version and fingerprint/version where available.
- **Optimistic conflict handling.** If the source changed after preparation, discard the stale prepared write, refetch, recompute, and retry once. Never replay a stale full-file body over a newer version. GitHub writes must use the fresh file SHA.
- **Read-back verification.** After every write, read back the same Drive file ID or GitHub path and verify the intended semantic change and content/hash/fingerprint before rebuilding dependent artifacts or reporting success.
- **Dependency order.** Authority first, then derived status/mirrors, then Control Center/Pages verification. Never let a generated status snapshot overwrite fresh authority.
- **No owner maintenance burden.** Deterministic drift that can be repaired from unambiguous authority is repaired silently. Ask the owner only for genuine creative/editorial ambiguity, unsafe/destructive action, security uncertainty, ambiguous task-to-scene mapping, or a deterministic repair that failed after one verified attempt.
- **No blind rollback.** Recovery may restore only from a verified authoritative source/version; historical checkpoints and cached copies are not current truth.



## Review / montage ledger — permanent contract (23.09.2026)

`review-ledger.json` separates technical render receipt from human editorial and montage decisions. It is generated/maintained on GitHub and does not override the Drive master, Topview telemetry, or the actual film edit.

Per Scene ID it tracks five independent facts: `result_received`, `reviewed`, `accepted`, `needs_redo`, `inserted_into_film`. Technical Topview `success` may set only `result_received=true`. It must never imply review, acceptance, no-redo, or insertion into the film. Human-decision fields remain `null` until explicitly known. `inserted_into_film=true` requires `reviewed=true` and `accepted=true`; `accepted=true` and `needs_redo=true` is invalid unless a future explicit schema rule defines partial acceptance.

`Reconcile review ledger` may add newly active canonical Scene IDs and advance `result_received` from verified `processed_tasks` success. It must never infer or overwrite human review/editorial/montage fields. `Validate review ledger` blocks structurally contradictory state.

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

