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
8. Library recovery refresh — best-effort/non-blocking; если требуется интерактивное подтверждение владельца, пометить pending/stale и не прерывать основной цикл;
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
- пытаться обновлять копии семи инструкций/HANDOFF при материальных изменениях best-effort; permission prompt не должен блокировать работу владельца;
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
- Notion operational pointer актуален; Library recovery, если stale/pending, явно остаётся recovery-only и не блокирует readiness при доступном Drive/GitHub.








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
   - `занято X из 6 · свободно Y · DD.MM.YYYY, HH:MM:SS`
   - `X` = количество реально активных `task_id`;
   - дата и время берутся из свежего `topview-status.json → checked_at` и отображаются в локальном формате интерфейса;
   - **выводить** `свободно Y`; поле/метку `синхр.` не показывать;
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




### Invariant — автоматическое ежечасное обновление Topview во всех трёх пользовательских представлениях




Это **жёсткий runtime/publish-контракт**, а не рекомендация. Каждый успешный запуск `Topview Scene Intake & Slow Watch` обязан не только прочитать Topview, но и **опубликовать новый свежий `topview-status.json` snapshot**, даже если набор Scene ID не изменился и поменялись только `checked_at`, status, queue или ETA.




Три пользовательских представления:
1. `РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС`;
2. `⏳ В медленной генерации — Topview`;
3. `🎬 Активные сцены проекта — карта и навигация`.




Все три должны автоматически актуализироваться **на каждом ежечасном Topview refresh** из **одного и того же** freshly committed `topview-status.json.active_tasks[]` и одного `checked_at`. На сайте запрещены три независимые копии live Topview state. `project-status.json` и canonical master участвуют как consistency gate для slow membership, но не заменяют `topview-status.json` как realtime telemetry source.




### Что watcher обязан публиковать каждый час




Для каждого active task watcher обновляет и сохраняет как минимум:
- exact `task_id`;
- `scene_id`;
- `topview_status`;
- `queue_count`;
- provider ETA/process fields, если Topview их отдаёт;
- `started_at` / `completed_at`, если применимо;
- fresh `checked_at` текущего успешного цикла;
- `occupied_slots`, `free_slots`;
- per-Scene `active_task_ids` / multiplicity.




**Queue/status/ETA-only изменение не является no-op.** Если watcher получил свежие данные Topview, но не записал новый `topview-status.json` и не обновил публичный snapshot сайта, hourly run считается незавершённым.




### Как эти данные должны выглядеть в трёх местах




- `init` / `queued` → **`В ОЧЕРЕДИ`**;
- `running` / `processing` → **`ВЫПОЛНЯЕТСЯ`**;
- terminal task после reconciliation больше не считается active slot;
- если у одной Scene несколько active tasks, кратность обязательна (`20×2`, `2 задачи`) и второй task нельзя терять;
- если статусы нескольких tasks одной Scene различаются, scene-level отображение обязано отражать смешанное состояние, а не выбирать только `primary` task;
- если где-либо показывается числовая очередь/ETA, она берётся только из **exact соответствующего task object** в `active_tasks[]`, без копирования scene-level значения на другие attempts.




**Кардинальность трёх представлений:**
- `РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС` показывает **N уникальных slow-сцен / M active tasks** и Scene IDs с кратностью;
- `⏳ В медленной генерации — Topview` показывает **ровно M строк**, одна строка = один active task/slot;
- `🎬 Активные сцены проекта — карта и навигация` показывает **ровно N уникальных active Scene ID** с агрегированным live status и кратностью.




Например, **5 slow-сцен / 6 active tasks** — корректно только если явно видно, какая Scene занимает два слота, например `20×2`.




### Hourly publish gate




Каждый ежечасный watcher run считается успешным только если одновременно выполнено:
- `unique(active_tasks[].scene_id) == project-status.json.slow_scenes == canonical slow Scene IDs`;
- `occupied_slots == len(active_tasks[]) == число строк Topview-таблицы`;
- `free_slots == max(0, 6 - occupied_slots)`;
- Scene IDs в active-scene map == `unique(active_tasks[].scene_id)`;
- multiplicity каждой Scene в summary/map == числу её active tasks;
- scene-level `В ОЧЕРЕДИ / ВЫПОЛНЯЕТСЯ` вычислен из тех же task statuses;
- все три представления относятся к одному `topview-status.json.checked_at`;
- canonical master slow declaration/table/TOC/scene markers совпадают с unique active Scene IDs;
- fresh `topview-status.json` реально закоммичен в GitHub;
- Pages/public Control Center не оставлен заведомо на более старом telemetry snapshot.




После успешной записи `topview-status.json` обычный GitHub Pages pipeline должен опубликовать новый snapshot. При изменении canonical slow/master дополнительно выполняется обычный `SYNC-TRIGGER.txt` → Drive sync/validation. Если меняются только queue/status/ETA, master переписывать не нужно, но **fresh `topview-status.json` + Pages refresh обязательны**.




Если хотя бы один пункт расходится, Control Center **не считается зелёным**, watcher run не считается завершённым. `AI Film Recovery Sync` через свой watchdog должен автоматически попытаться восстановить deterministic state и публикацию. Пользователя нельзя просить вручную сравнивать эти три места или следить за очередью.




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
- Instruction certificate **exact-match** является частью blocking health: подтверждённое различие/ошибка чтения 7/7 canonical docs даёт non-green. Возраст `checked_at` — отдельная maintenance freshness; stale certificate сам по себе не делает master/project sync красным и должен автоматически обновляться Recovery.
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




## TOPVIEW HOURLY LIVENESS SLA — 24.09.2026




- Владелец проекта не должен вручную проверять занятость слотов, свежесть `checked_at`, появление новых Topview-задач или исправность watcher; это обязанность автоматики.
- `Topview Scene Intake & Slow Watch` — primary single writer Topview-derived state — работает в **exact hourly schedule** ровно в `:00` каждого часа по Europe/Moscow. Hourly job должен оставаться лёгким: refresh всех tracked active task IDs, recent Board VIDEO discovery, deterministic mapping, slow lifecycle, task-map/status/journal и sync trigger. Не смешивать сюда тяжёлый deep audit, instruction maintenance или unrelated prompt upgrades.
- Discovery обязан просматривать все строки в scanned Board pages, а не считать первый результат самым новым. Использовать large page size (предпочтительно 100) и overlap минимум 6 часов от durable `last_scan_at`; pinned/старые строки не должны скрывать новые задачи.
- Если новая active-задача exact/normalization-equivalent existing canonical Scene, она маппится на **тот же Scene ID** и немедленно добавляет/возвращает Scene в canonical slow. Новый Scene ID создаётся только для genuinely new creative scene; ambiguity требует owner decision.
- `topview-status.json.checked_at` — фактическое время успешного telemetry refresh, а не время последней публикации сайта. Occupied slots = число active task IDs; один Scene ID может занимать несколько слотов.
- `AI Film Recovery Sync` работает **exact hourly в `:05` каждого часа** по Europe/Moscow — через пять минут после primary watcher в `:00`. Этот offset обязателен: одновременный старт двух automation создавал race, при котором Recovery мог завершиться до того, как watcher успевал отключиться/опубликовать degraded state. One-writer правило сохраняется: Recovery не конкурирует с выполняющимся здоровым watcher, но после его окна может re-enable/repair доказанный сбой. Он считает watcher unhealthy если тот disabled, `last_run_time` или telemetry checkpoint старше 75 минут, run не дал checkpoint более 10 минут, либо Board task, существовавший к моменту run, остался вне active+processed state.
- При unhealthy watcher Recovery сначала re-enable его; если authoritative Topview data однозначны, Recovery выполняет один deterministic emergency reconciliation сам, а не просит владельца вручную проверять Topview.
- One-writer правило сохраняется в нормальном режиме: Recovery не переписывает свежий здоровый Topview state. Emergency write разрешён только при доказанном unhealthy/missed watcher и deterministic mapping.
- Routine healthy/repaired maintenance остаётся silent. Owner notification нужна только для ambiguous mapping, verified unrepaired failure, task failure/cancel, capacity >6 или реального творческого решения.
- Любое изменение schedule/prompt automation обязано явно сохранять `is_enabled=true`; если watcher после run оказывается disabled без явного решения владельца, Recovery должен автоматически вернуть его в enabled state.
- **Scheduled-task connector degradation rule:** Topview Board connector может быть доступен в интерактивном Project Chat, но отсутствовать в background Scheduled Task. В этом случае watcher **не имеет права self-disable**, не подделывает новый `checked_at`, не двигает `last_scan_at` и не меняет canonical slow по догадке; он остаётся enabled и повторяет попытку в следующий `HH:00`.
- Recovery в `HH:05` обязан проверить `is_enabled`; если watcher был автоматически disabled, re-enable его. Если Topview connector недоступен и Recovery тоже, сохраняется последний verified snapshot с честным возрастом telemetry; это **degraded Topview telemetry**, а не ошибка Drive/master sync.
- Control Center не должен показывать stale instruction certificate как общую красную `ОШИБКА СИНХРОНИЗАЦИИ`. Красный глобальный sync reserved для реального mismatch/corruption/unavailable authoritative data. Для slow summary использовать понятную формулировку `N сцен · M генераций`; если одна Scene имеет несколько active tasks, multiplicity показывать явно (`20×2`), а не дублировать тот же summary в нескольких статусных строках.




## CHATGPT PROJECT MODE — AI Film Серёгиус — 24.09.2026




- Проект ChatGPT `AI Film Серёгиус` является **контекстным рабочим контейнером**, а не новым источником истины. Чаты, Project files и Project Instructions помогают continuity/onboarding, но не заменяют fresh authoritative sources.
- При конфликте проектной памяти, старого чата, вложения или сохранённой копии с live-источниками приоритет: exact Google Drive master/instructions → live GitHub status/runtime → Topview telemetry для генераций → Notion для story/history → Library как recovery cache.
- Новый Chat или Work внутри Project не должен начинать с нуля и не должен просить пользователя повторять известное. Он обязан использовать контекст Project, затем выполнить canonical takeover/preflight из `NEW-CHAT-HANDOFF.md`.
- **Project context не отменяет fresh-read.** Перед любой записью в prompt master нужен свежий exact Drive master; перед prompt work — fresh `PROMPT-STYLE-GUIDE.md` + 1–2 близкие current scenes; перед story/editing — fresh `film-analysis.md` + `film-backlog.md` и при необходимости Notion `Кино`.
- Static/generated copies of `video-prompts.md`, handoff или status, попавшие в старые чаты/вложения Project, считаются только historical context. Нельзя брать их как editable authority, если доступен live Drive/GitHub.
- Для длинных многошаговых технических задач, аудитов, массовой сверки источников и handoff/recovery предпочтителен **Work внутри этого Project**. Для обычного обсуждения/написания одной сцены подходит обычный Project Chat. Оба режима обязаны соблюдать один canonical workflow.
- Смена конкретного чата — штатная операция: новый Project Chat/Work восстанавливает состояние из Project context + canonical handoff/live sources. Нельзя строить архитектуру на предположении, что один чат будет жить бесконечно.
- Scheduled Tasks/automations остаются независимой operational автомatikой; Project Chat не должен дублировать их ручным мониторингом, если live tools позволяют проверить состояние.
- Владелец должен заниматься фильмом, а не обслуживать инфраструктуру: deterministic sync/status/site/Topview drift чинится автоматически или редактором; пользователя спрашивать только о genuinely creative/editorial/ambiguous decisions.




## LIBRARY RECOVERY — NON-BLOCKING / BEST-EFFORT — 24.09.2026




- ChatGPT Library остаётся **recovery mirror/cache**, а не authority и не обязательный транзакционный слой.
- Обязательный путь завершения material change: relevant SAME-ID Drive canonical docs/master → exact GitHub mirrors/status/validation/Pages где применимо → fresh `instruction-sync-status.json` → Notion operational pointer, если меняется будущий workflow.
- Library refresh выполняется **best-effort**. Если запись возможна без интерактивного подтверждения владельца — обновить. Если интерфейс требует отдельное `Разрешить это изменение в Библиотеке?`, consent/permission недоступен automation или мобильное приложение даёт только `Try again` — **не блокировать работу, не повторять prompt и не просить владельца переключаться в браузер**. Зафиксировать `pending/stale` и продолжить.
- `pending/stale` Library не делает проект non-green, не отменяет verified Drive/GitHub/Pages change и не запрещает сообщить о завершении основной работы. Нельзя только утверждать, что Library свежая, если она фактически не обновлена.
- `AI Film Recovery Sync` / daily deep audit может повторить Library refresh позже, когда write доступен без нового интерактивного разрешения. Не создавать цикл повторных consent prompts.
- На takeover stale/missing Library — информационный recovery warning only, пока доступны fresh Drive canonical sources и live GitHub status.




## ERROR-PREVENTION ARCHITECTURE — 24.09.2026




Цель этой архитектуры — не «чинить красные ошибки после каждого служебного шага», а не создавать ложные ошибки из временных/неавторитетных состояний вообще.




### 1. Пять независимых health-доменов




Нельзя сворачивать все служебные состояния в один красный `ОШИБКА СИНХРОНИЗАЦИИ`.




1. **Authoritative project sync — blocking/red только при реальной поломке.** Google Drive master ↔ GitHub mirror/hash, валидность generated `project-status.json`, exact mismatch/read failure 7 canonical instruction mirrors.
2. **Topview telemetry — operational/non-blocking.** Возраст snapshot, queue/ETA и доступность Topview connector. Stale/degraded telemetry показывается отдельно и не делает master-sync красным.
3. **Topview task-map — internal cache/non-blocking.** `topview-task-map.json` нужен для dedupe/discovery, но его временный drift относительно публичного snapshot является maintenance, а не corruption проекта.
4. **Instruction certificate freshness — maintenance/non-blocking.** Старый `checked_at` сам по себе не является mismatch. Блокирует только подтверждённое различие Drive↔GitHub или read/validation error.
5. **Library recovery — best-effort/non-blocking.** Никогда не completion gate.




### 2. Один публичный источник Topview + stable checkpoint




- `topview-status.json` — единственный PUBLIC/RUNTIME источник Topview для трёх пользовательских представлений сайта.
- `topview-task-map.json` — внутренний cache/dedupe слой; UI не строит live state из него.
- `topview-checkpoint.json` — стабильный commit marker. Его пишут **последним**, только после read-back verification status + task-map.
- Integration tests не должны запускаться на каждом промежуточном commit `topview-status.json` или `topview-task-map.json`; они запускаются по stable checkpoint. Это исключает красные тесты на половине транзакции.




### 3. Транзакционный порядок Topview publication




При доступном Topview watcher сначала вычисляет полный intended state в памяти и публикует только в таком порядке:




A. если реально меняется canonical slow/master — fresh exact Drive read → same-ID master write → read-back verification;
B. внутренний `topview-task-map.json` + компактный journal → read-back verification;
C. публичный `topview-status.json` из того же вычисленного state → read-back verification;
D. `topview-checkpoint.json` **LAST** с тем же `checked_at`, active task IDs, unique Scene IDs и occupied slots;
E. только после checkpoint — обычный sync trigger, если менялся canonical master/slow.




Если шаг B не прошёл, C/D не выполняются. Если C не прошёл, D не выполняется. Нельзя продвигать checkpoint поверх partial state.




### 4. Schedule / one-writer / watchdog




- Primary `Topview Scene Intake & Slow Watch`: exact hourly **HH:00 Europe/Moscow**.
- `AI Film Recovery Sync`: exact hourly **HH:05 Europe/Moscow**. Пятиминутный offset обязателен для prevention: Recovery наблюдает уже завершившийся/сорвавшийся watcher-cycle, а не стартует одновременно и не создаёт race.
- Watcher — normal single writer Topview-derived runtime state.
- Recovery не конкурирует со здоровым watcher. Emergency write разрешён только после доказанного missed/failed/degraded watcher и при однозначном authoritative mapping.
- Любое изменение automation сохраняет `is_enabled:true`, если владелец явно не просил остановить задачу.




### 5. Background connector degradation




Если Topview connector отсутствует именно в background Scheduled Task:




- watcher **не self-disable**;
- не выдумывает status/queue/ETA;
- не обновляет `checked_at`, `last_scan_at` или checkpoint;
- не меняет canonical slow по догадке;
- сохраняет последний verified snapshot и остаётся enabled для следующего HH:00.




Recovery в HH:05 повторно оценивает ситуацию. Если connector недоступен и там, это честное состояние **Topview telemetry stale/degraded**, а не ошибка Drive/master sync.




### 6. Validator и Control Center




Blocking checks проекта используют только authoritative/self-contained invariants. Временный task-map cache drift хранится в `project-status.json.maintenance.topview_task_map` и не меняет `health=ok` сам по себе.




Control Center:
- green global label = `ПРОЕКТ СИНХРОНИЗИРОВАН`; red global label = `ОШИБКА КАНОНИЧЕСКОЙ СИНХРОНИЗАЦИИ`; красный reserved только для реальной authoritative corruption/unavailability;
- stale instruction certificate, stale Topview telemetry, historical superseded workflow failures и Library pending не должны давать global red;
- Topview stale показывается отдельной предупреждающей строкой с временем последнего verified snapshot;
- Topview card показывает slot-summary: крупно `M из 6`, ниже `Свободно Y · N сцен`; длинный список Scene IDs остаётся в подробном Topview-блоке.




### 7. Definition of Done для Topview state




Успешный telemetry cycle считается опубликованным только когда:
- public `topview-status.json` self-consistent;
- task-map read-back выполнен;
- stable `topview-checkpoint.json` соответствует public snapshot;
- Pages публикация не оставлена заведомо старее успешного snapshot;
- при canonical slow change прошёл normal master/status sync.




Partial intermediate commits не считаются final state и не должны порождать owner-facing красную ошибку.


### 8. Serialized canonical instruction writes


- Seven canonical instruction docs изменяются **только последовательно**, никогда одним длинным multi-write batch.
- Для каждого файла: fresh-read/version check → SAME-ID Drive write → read-back → exact GitHub mirror → verify → следующий файл.
- Если tool-call timeout/unknown outcome, перед следующей записью заново прочитать affected Drive file. Нельзя повторно заливать prepared stale copy вслепую: late completion предыдущего write может перетереть более свежую версию.
- Read-only проверки можно batch-ить; canonical writes — serial transaction.
- Это правило распространяется на Handoff и все relevant canonical instruction changes и должно сохраняться следующими чатами/Work.




## CONTROL CENTER OWNER UI — SLOT CAPACITY & COMPACT NAV — 24.09.2026


Этот блок имеет приоритет над более ранним owner-facing UI text.
- Верхняя Topview-карточка показывает **`M из 6` занятых слотов**, а под ним **`Свободно Y · N сцен`**. Слот = active task; slow Scene ID уникальны отдельно.
- Детальный Topview header: **`занято M из 6 · свободно Y · DD.MM.YYYY, HH:MM:SS`**.
- В карточке рабочих направлений показывать только число; не выводить `W5…W15` как owner-facing summary.
- Sidebar должен быть компактным без потери функций: плотные отступы/TOC, основные ссылки рядом, Service Files и Filters collapsed by default, active filter виден в summary.
- После существенной прокрутки показывать floating **↑ Наверх** с smooth scroll.
- Validator + Pages должны защищать этот контракт от регрессии; Recovery его не откатывает.

## AUTOMATIC MASTER REVISION DATE — 26.09.2026

Дата `Ревизия` в Control Center является машинно вычисляемой датой последнего **содержательного изменения canonical master**. Источник — semantic fingerprint `canonical_revision_sha256` в `project-status.json`, а не ручная дата внутри `video-prompts.md`. Добавление/удаление сцены, изменение prompt body, canonical slow/render-state или важного master-context меняет fingerprint и двигает ревизию. Чистая техническая пересинхронизация без semantic change сохраняет прежнюю дату. Legacy/manual revision date в master больше не использовать.
