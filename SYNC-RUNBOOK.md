# SYNC-RUNBOOK v4.0 — AI Film Project


## Действующее расписание — решение владельца 06.10.2026


**Приоритет этого блока:** он заменяет все прежние указания ниже о двух/трёх project automations, HH:05 Recovery, восстановлении архивных задач и временном выключении writer при ручном ремонте. Исторические checkpoints ниже не являются текущей конфигурацией.


Единственная действующая задача: **AI Film — единый монитор**, ID `6aac794245e481919ee7155c461cc77e`, exact hourly **HH:00 Europe/Moscow**. Внутри одного запуска: Topview account slots + уведомления, AI Film scene intake/telemetry publication, проверка 7/7 Drive↔GitHub и canonical sync, hourly light health, daily deep audit при возрасте ≥24 ч. Recovery — фаза этой же задачи, без отдельного расписания.


Намеренно архивированы по просьбе владельца: Recovery `6aac3e4dfe6c81918b3eead8529edf30` и «Свободные слоты Topview» `6ac358bf36548191b64ae6326bcc1f9b`. Оставлять `is_enabled:false`; **не включать обратно**, не создавать заменяющие дубли. Их история сохраняется. Правило preserve-enabled относится только к единственному действующему монитору.


При недоступном connector, конфликте записи или partial publication не выключать задачу: сохранить старые подтверждённые timestamps, записать конкретный сбой, выполнить остальные доступные фазы и повторить недоступную фазу в следующем цикле. Не вызывать automations.update из фонового запуска. Для ручного ремонта использовать fresh-read/version guard/rebase и отложенную конфликтующую запись, без паузы расписания. Явное решение владельца остановить задачу имеет приоритет.


Уведомления — только новое освобождение slow slot, новый существенный результат/блокер либо восстановление; неизменные здоровые проверки не спамят. Дедупликация и последняя фактически выполненная фаза: `automation-monitor-status.json`. Глобальные slots считать по complete all-owned-boards VIDEO scan и уникальным active `useUnlimitMode=true` task IDs; project scene intake ограничен доказанными AI Film mappings. Не придумывать Scene ID чужой задаче. Успех генерации не является редакционным approval.


**Ограничение одного расписания:** независимой второй проверки работоспособности scheduler больше нет. Если платформа остановит саму задачу, отключённая задача себя не запустит. Доступный API не раскрывает причину последнего отключения и не предоставляет настройку «никогда не приостанавливать». Не выдавать prompt-запрет самоотключения за гарантию платформы. Не имитировать чтение уведомлений/активность пользователя. Проверка конфигурации — read-back automations и этот актуальный блок.


### Порядок фаз единого монитора


1. Fresh Topview account scan всех owned boards с полной pagination VIDEO и direct get каждого известного active ID. Unknown status / недоступный board — не полная достоверная ёмкость; queueCount не равен slots.
2. Уведомление о новом освобождении слота независимо от доступности Drive/GitHub. Baseline и последняя successful observation сохраняются по task IDs, учитывая вновь занятые места между наблюдениями. Не повторять один и тот же свободный слот.
3. AI Film intake с overlap ≥6ч, existing prompt → existing Scene ID; только однозначный новый project prompt → новый незарезервированный ID. Ambiguous → вопрос, без импорта.
4. Последовательная публикация: map → bounded journal → public status → checkpoint LAST; один фактический checked_at и равные active task IDs/counts. Canonical slow снимается только после terminal последней active задачи. При необходимости runtime-only master edit — fresh same-ID Drive guard/read-back, trigger, validator, exact mirror, Pages.
5. Exact полная сверка 7 Drive↔GitHub текстов каждый запуск. Mirror исправлять из Drive current SHA, serial/read-back. Сертификат выдавать только после полной реальной проверки.
6. Hourly light / due daily deep (≥24ч), public freshness: Topview >105мин, certificate >165мин. Один новый инцидент, один recovery notice; partial phase не отключает другие фазы. Library best effort не является completion gate.
7. В `automation-monitor-status.json` записывать фактически пройденные фазы, account snapshot и dedup state. Не заявлять scheduled-run успех на основании ручной проверки или сохранённого prompt. Проверять первый будущий запуск отдельно при доступном результате.


Приоритет/authority: Drive master и canonical docs → exact GitHub mirrors → Pages; Notion — operational pointer; Library — необязательный recovery cache. Полный исполняемый prompt сохранён в самой automation; scratch и chat history не являются обязательной зависимостью.


**Дата актуализации:** 22.09.2026  
**Назначение:** пошаговая инструкция записи, синхронизации, проверки и recovery для master, инструкций, сайта и связанных зеркал.


## 1. Обязательный preflight перед любой записью


Редактор сначала читает весь seven-document takeover set:


1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`


Затем:
- fresh Drive `video-prompts.md`;
- live GitHub `project-status.json`;
- live `topview-status.json`;
- live `instruction-sync-status.json`.


Для prompt work дополнительно обязательно fresh-read `PROMPT-STYLE-GUIDE.md` + 1–2 релевантные master-сцены.


Для story/editing work — `film-analysis.md`, `film-backlog.md`, при необходимости `PROGRESS.md`, монтажный HTML и Notion `Кино`.


Перед первой записью окружение должно подтвердить:
- read exact Drive master ID;
- same-ID Drive write;
- GitHub read/write;
- возможность проверить workflow/status/Pages.


Если same-ID Drive write недоступна, агент review-only.


## 2. Канонические Drive IDs


Folder:
`1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`


Prompt master:
`video-prompts.md` → `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`


Seven-document instruction/recovery set:
- `NEW-CHAT-HANDOFF.md` → `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- `SYNC-RUNBOOK.md` → `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `AI-PROJECT-GUIDE.md` → `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `PROMPT-STYLE-GUIDE.md` → `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`
- `USER-GUIDE.md` → `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` → `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `BACKUP-AI-RUNBOOK.md` → `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`


Никаких `v2`, `final`, `copy` вместо этих файлов.


## 3. Routine: изменить существующую scene / prompt


1. Fresh-read exact Drive master.
2. Найти exact Scene ID.
3. Проверить slow-lock и `scene-meta`.
4. Если prompt materially меняется — fresh-read `PROMPT-STYLE-GUIDE.md`.
5. Изменить только нужный scene block и связанные TOC/count/status/meta.
6. Сохранить **в тот же Drive file ID**.
7. Убедиться, что raw Markdown UTF-8 without BOM.
8. Обновить GitHub `SYNC-TRIGGER.txt`.
9. Дождаться `sync-from-drive.yml`.
10. Проверить validator.
11. Проверить Drive master == GitHub `video-prompts.md`.
12. Проверить `project-status.json`.
13. Проверить Pages build.
14. Если сцена slow — не менять Topview mapping без доказанной необходимости; newly launched replacement/retry task с exact/normalization-equivalent canonical prompt считается доказанной причиной обновить mapping.
15. Только затем сообщать `ГОТОВО`.


## 4. Routine: добавить новую scene


Перед добавлением:
- fresh-read master;
- получить `latest_scene`;
- учитывать удалённые historical IDs;
- не переиспользовать удалённые номера;
- если следующий ID однозначен, не спрашивать пользователя.


Добавить:
- anchor;
- заголовок `## Сцена N`;
- `scene-meta`;
- human wrapper: контекст / референсы / что происходит;
- полный master-level prompt;
- TOC row;
- counts/revision/current-state text, только где это действительно current;
- slow marker/table только если генерация реально запущена или пользователь явно перевёл сцену в canonical slow.


После — полный routine sync из раздела 3.


## 5. Routine: удалить/закрыть scene


Scene удаляется из active master только когда пользователь подтвердил, что результат принят и prompt больше не нужен.


Topview `success` сам по себе не является approval.


При удалении:
- убрать section;
- убрать TOC;
- убрать current slow entry, если применимо и пользователь это решил;
- обновить counts;
- **не переиспользовать Scene ID**;
- проверить зависимости других scene-meta;
- sync/validate/Pages.


## 6. Routine: site-only UI change


Site-only изменения делаются в GitHub `index.html`, если они не меняют prompt data.


После изменения:
1. JS syntax check;
2. duplicate HTML IDs check;
3. проверить отсутствие секретов;
4. проверить, что scene/prompt data по-прежнему грузится из master/status, а не hard-coded;
5. commit;
6. дождаться Pages;
7. проверить текущий UI/code state.


Если функция становится постоянной частью архитектуры — применить **Material Change Documentation Rule** из раздела 9.


Текущий baseline:
- merged slow/Topview;
- sync lightsaber;
- active scene map;
- references;
- light/dark theme;
- collapsible `Контрольный отпечаток`;
- отдельная collapsible `💬 Комментарии, идеи и предложения` сразу под ним;
- native Supabase comments/replies без GitHub login;
- старой кнопки `Архив GitHub` нет.


## 7. Routine: instruction change


Google Drive — authority.


Если меняется правило:
1. определить все затронутые документы;
2. fresh-read их Drive originals;
3. изменить SAME Drive IDs;
4. если изменение важно следующему чату — обновить SAME `NEW-CHAT-HANDOFF.md`;
5. если изменился prompt standard — обновить SAME `PROMPT-STYLE-GUIDE.md`;
6. exact-mirror Drive → GitHub;
7. re-read Drive + GitHub full text;
8. обновить `instruction-sync-status.json`;
9. проверить `project-status.json` не содержит blocking `instruction_sync_error`; `instruction_sync_stale` допустим только как non-blocking maintenance freshness;
10. обновить Notion operational pointer, если меняется будущий workflow;
11. Library recovery refresh — best-effort/non-blocking: выполнить только без интерактивного подтверждения владельца; иначе зафиксировать pending/stale и продолжить.


Автоматический repair допускается только **Drive → GitHub**.


## 8. `instruction-sync-status.json`


Status должен описывать **все семь** обязательных документов.


Для каждого:
- exact Drive file ID;
- Drive modified_at;
- GitHub blob SHA;
- `match: true/false`.


Общие поля:
- fresh `checked_at`;
- `health`;
- `all_match`;
- `freshness_max_hours`;
- `semantic_check`.


Нельзя оставлять старый five-file snapshot как якобы current после расширения recovery set.


Если status stale, сам факт stale не означает повреждение master; это означает, что verification нужно обновить.


## 9. Material Change Documentation Rule


Изменение считается материальным, если меняет способ работы следующих чатов или архитектуру проекта:
- новая постоянная функция сайта;
- новый backend/integration;
- новый обязательный prompt rule;
- смена authority/source of truth;
- новый status/workflow;
- новый recovery rule;
- новый обязательный документ;
- изменение способа синхронизации.


Такое изменение **не завершено**, пока:
- relevant Drive docs не обновлены;
- HANDOFF не обновлён;
- prompt guide обновлён, если касается prompt-writing;
- GitHub mirrors не синхронизированы;
- instruction status не refreshed;
- Notion operational pointer не обновлён, если меняется workflow;
- Library recovery mirror может быть stale/pending и **не блокирует** завершение, если Drive/GitHub/instruction status/Notion прошли проверку.


Runtime telemetry (queue/ETA/SHA) не нужно копировать во все docs: её читают live.


## 10. Topview telemetry


Canonical slow membership:
`project-status.json.slow_scenes`.


Для каждой slow scene:
- exact task mapping;
- сравнение task prompt/references с fresh canonical scene;
- `verified=true` только при доказанном match;
- queue_count только из exact task;
- provider ETA только из exact task;
- historical ETA отдельно;
- `success` одной попытки не снимает slow, если у сцены остаются другие active tasks; последняя terminal попытка снимает Topview-managed slow автоматически, не меняя approval/editorial state.


Нельзя:
- remap из-за старого handoff/title;
- копировать одну очередь на все сцены;
- автоматически rerun;
- автоматически approve.


## 11. Comments / Supabase


Backend:
- Supabase project `ai-film-comments`
- ref `vzohfatqzyioydtgjiyd`
- organization `Vint`
- Edge Function `submit-comment`


Security baseline:
- public read published comments;
- anonymous post/reply;
- RLS;
- honeypot;
- 5 сообщений / 10 минут / IP;
- frontend publishable key only;
- no service_role in public code;
- no permission to mutate master/status/generation.


Любое изменение этой архитектуры документировать как Material Change.


## 12. Library recovery maintenance


Library — recovery mirror/cache, not authority.


После материальных instruction/handoff changes **пытаться** обновлять Library copies best-effort, но не блокировать основной цикл и не требовать интерактивного подтверждения владельца:
- all seven docs;
- `READ-FIRST.txt`;
- `CURRENT-STATE.json`;
- `SITE-STATUS.md`;
- `SHIFT-HANDOFF.md`;
- recovery ZIP, если он поддерживается как актуальный пакет.


Library copy никогда не должна молча переопределять более свежий Drive.


## 13. Notion maintenance


Notion `Кино` — story/history/idea bank.


Операционный указатель:
`AI Film — Актуальная инструкция / Handoff`.


При material workflow change обновить указатель, чтобы он:
- указывал Drive как authority;
- перечислял current seven-document takeover set;
- не выдавал старые prompts за master.


`Важные промты` — legacy idea/prompt bank; использовать как reference/history, не как текущий standard.


## 14. Recovery / known failures


### Non-fast-forward / concurrent writers
Sync должен refetch latest `origin/main`, rebuild status и retry push; не перетирать более свежий telemetry commit.


### UTF-8 BOM
Master должен быть UTF-8 without BOM. Workflow может strip optional BOM до validation, но канонический raw master хранится без BOM.


### Stale instruction status
Refresh exact comparisons; не объявлять master broken только из-за старого timestamp.


### Historical/current semantic conflict
Исторический checkpoint не является live invariant. Current claims должны быть единичными и чётко помеченными.


### Topview false mismatch
Сравнивать exact task с fresh current scene body, а не с памятью/старым title.


## 15. Verification before final answer


Для master change:
- exact Drive same-ID write confirmed;
- workflow success;
- validator success;
- Drive/GitHub mirror match;
- project-status current;
- Pages success.


Для instruction/material change:
- all seven Drive docs contain new rule;
- all seven GitHub mirrors exact-match Drive;
- fresh instruction-sync-status all seven;
- project-status no stale/error instruction warning;
- Notion pointer current;
- Library recovery state известен (`current` или `pending/stale`); `pending/stale` не блокирует завершение при доступном fresh Drive/GitHub.


Не писать пользователю `ГОТОВО`, если relevant verification не завершена.


## 16. Character / film-context preflight для нового чата


Перед takeover-ready новый чат дополнительно обязан:
1. открыть `references.html` и прочитать `character-references.json`;
2. построить name/alias/model-sheet mapping и сверить active scene usage с fresh master;
3. открыть `Seregius_montazhny_razbor.html`;
4. сверить его current-useful conclusions с `film-analysis.md`, `film-backlog.md` и при необходимости Notion `Кино`;
5. сохранить в рабочем контексте компактную карту персонажей и монтажных приоритетов, а не тащить гигантские base64/images/HTML целиком в каждый последующий turn.


Для natural-language scene requests сначала resolve имена через registry/master. Approved model sheet = identity authority. Current master = scene usage authority. Не просить пользователя повторно описывать зарегистрированного персонажа.


## 17. Takeover readiness audit


До сообщения `ГОТОВ ПРОДОЛЖАТЬ` проверить:
- 7/7 canonical Drive docs readable;
- 7/7 GitHub mirrors exact-match Drive;
- fresh instruction status;
- master/status consistency;
- site baseline and Pages;
- character registry/reference viewer availability and obvious scene-usage drift;
- montage report + film-analysis/backlog availability;
- Notion operational pointer current enough for navigation;
- Library recovery copies, если доступны, marked recovery-only and not misleadingly newer/authoritative; stale/missing Library не блокирует takeover при доступном fresh Drive/GitHub.


Safe documentation drift может быть исправлен сразу по Drive→GitHub authority. Master/story/approval conflicts требуют user decision.


## 18. Что имеет смысл проверять автоматически, а что нет


Hourly recovery может делать **лёгкий integrity audit**: seven-doc mirror/freshness, site-file/link presence, наличие `character-references.json`, `references.html`, montage HTML, `film-analysis.md`, `film-backlog.md`, отсутствие явного public admin secret, и известные semantic invariants. Не нужно ежечасно заново читать/переписывать весь монтажный анализ или весь character image payload — это создаёт лишнюю нагрузку и шум.


Глубокая семантическая сверка персонажей с новыми prompts выполняется при material scene/prompt change и на takeover. Notion/Library можно проверять на явную устарелость, но автоматический hourly repair туда не должен слепо писать без необходимости.


## 19. Topview task intake / existing-scene binding


`Topview Scene Intake & Slow Watch` обрабатывает previously unknown Topview video tasks по трём веткам:


1. **Existing canonical scene render/retry.** Actual task prompt exact/normalization-equivalent active canonical prompt либо есть explicit provenance к Scene ID. Нормализация может игнорировать только несемантические различия (`@image` ↔ `<<<Image>>>`, whitespace/line endings/reference-token formatting). Model/duration/reference structure должны быть совместимы.
2. **Genuinely new scene.** Task явно описывает отдельную сцену, которой нет среди active canonical Scene IDs.
3. **Ambiguous.** Нельзя безопасно доказать 1 или 2 → no master mutation, notify user. Одна semantic similarity не даёт права тихо отбросить task.


Existing-scene routine:
1. fresh master + `project-status.json` + `topview-status.json` + `topview-task-map.json`;
2. scan recent Topview video tasks and exclude already-known task IDs/non-video jobs;
3. доказать exact/normalization-equivalent match или explicit provenance;
4. записать/обновить task↔**existing Scene ID** mapping; newly launched replacement/retry может заменить старый task binding;
5. если task queued/running/init/processing — fresh-read master и добавить existing Scene ID в canonical slow во всех связанных slow markers/table/TOC, сохранив editorial/production state;
6. если `success` — refresh telemetry, never `APPROVED`, не создавать duplicate Scene ID;
7. если failed/cancelled — no auto-rerun; notify;
8. SAME-ID Drive write только если canonical slow реально меняется;
9. normal trigger/sync/validation/GitHub mirror/`project-status.json`/Pages.


Genuinely-new-scene routine:
1. получить exact actual prompt/model/task metadata;
2. fresh-read master непосредственно перед write;
3. присвоить следующий unused stable Scene ID;
4. сохранить actual Topview prompt verbatim, добавить human-readable Russian wrapper;
5. valid `scene-meta`; running task → canonical slow, success → `RESULT_RECEIVED`, never `APPROVED`;
6. SAME-ID Drive write;
7. normal trigger/sync/validation/GitHub mirror/`project-status.json`/Pages;
8. записать task↔Scene mapping и refresh telemetry;
9. уведомить пользователя о созданной сцене.


## 20. Site service-file navigation


Control Center → **Служебные файлы** обязан давать прямые ссылки на все семь canonical/recovery docs с понятными русскими названиями, а также на master, film analysis и backlog. После изменения этого блока проверять JS syntax, duplicate IDs и Pages.


## 21. Двухуровневый Recovery schedule


`AI Film Recovery Sync` запускается каждый час, но выполняет два разных режима.


### Hourly light
- seven-doc exact Drive → GitHub verification/repair;
- свежий `instruction-sync-status.json`;
- master ↔ `project-status.json` consistency;
- key site/context files, character registry metadata, permanent UI/security invariants;
- без полного Notion/Library/montage/Supabase/GitHub-Actions обхода, если light check не нашёл конкретный incident.


### Daily deep inside the same hourly automation
Проверить `deep-audit-status.json`. Если `last_deep_audit_at` отсутствует, invalid или старше 24 часов — выполнить полный deep audit: master, prompts vs style guide, characters, montage/film context, Notion, Library, site, Supabase, GitHub Actions/Pages и recovery test. После успешного прохода обновить `deep-audit-status.json`.


Если deep audit завершился с material failure, не продвигать successful timestamp; следующий hourly run должен retry.


Topview intake остаётся отдельным `Topview Scene Intake & Slow Watch`; Recovery не создаёт/approve/rerun/delete/slow-clear сцены.


## 23. UI-порядок служебных инструкций


Control Center → **Служебные файлы** должен явно различать **7 инструкций** и **3 рабочих файла проекта**.


Инструкции отображаются вертикально и нумеруются в canonical takeover order:
1. HANDOFF
2. Sync Runbook
3. Project Guide
4. Prompt Style Guide
5. User Guide
6. README AI Sync
7. Backup AI Runbook


После них отдельным блоком `Рабочие файлы проекта` идут master, film-analysis и film-backlog. **Эти три ссылки тоже должны идти вертикально, одна под другой, в порядке master → analysis → backlog.** Они не считаются инструкциями. При site audit проверять наличие такого разделения, правильный порядок инструкций 1–7 и вертикальную раскладку обеих групп.


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


- Topview watcher остаётся единственным штатным writer для Topview-derived render state. После recovery он должен быть `is_enabled:true`; при ручной аварийной сверке расписание НЕ останавливается; использовать fresh-read/version guard/rebase, конфликтующую запись отложить. Актуальная архитектура одного монитора — в верхнем блоке от 06.10.2026.
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


Этот блок **заменяет более ранние owner-facing формулировки**, где предлагалось скрывать `free_slots` или считать верхнюю Topview-карточку по уникальным slow-сценам.


- Верхняя Topview-карточка: **`M из 6`** занятых task-slots; подпись **«Занято слотов Topview»**.
- Вторая строка: **`Свободно Y · N сцен`**. `M = len(active_tasks[])`, `Y = max(0, slot_capacity-M)`, `N = unique(active_tasks[].scene_id)`.
- Детальный заголовок Topview: **`занято M из 6 · свободно Y · DD.MM.YYYY, HH:MM:SS`**.
- Карточка рабочих направлений показывает только число; raw `W5…W15` в summary/fingerprint не выводить.
- Левое меню остаётся информационно полным, но компактным: уменьшенные отступы/ширина/TOC, основные ссылки рядом, Service Files и Filters свернуты по умолчанию; активный фильтр виден и раскрывает группу.
- После прокрутки вниз показывать плавающую **↑ Наверх**; действие — smooth scroll к началу страницы.
- Эти owner-facing правила валидируются вместе с `index.html` и Pages; Recovery не должен откатывать их к старому варианту.


## AUTOMATIC MASTER REVISION DATE — 26.09.2026


`revision_date` — вычисляемое поле, а не ручной маркер в master. `sync-from-drive.yml` вызывает `build_project_status.py` с `--previous-status-file project-status.json`, `--previous-master-file video-prompts.md` и `--revision-timezone Europe/Moscow`. Валидатор вычисляет `canonical_revision_sha256`; при semantic change ставит дату текущего sync, при отсутствии semantic change сохраняет предыдущую дату. Технические sync-only timestamps нормализуются и сами по себе ревизию не двигают.


Правило записи master: строку `**N сцен ... · M полных текста промта**` держать **без ручной даты**. После substantive master write нормальный Drive → trigger → validation → GitHub → Pages цикл обязан автоматически обновить `revision_date`. Не редактировать `project-status.json.revision_date` вручную для обычной работы.


## Master whitespace normalization / revision fingerprint — 27.09.2026
- Before writing canonical `video-prompts.md`, reject/normalize accidental repeated blank-line runs. Standard presentation is at most one empty separator line between blocks, including fenced production prompts.
- `canonical_revision_sha256` normalizes line endings and repeated blank-line-only layout noise in addition to technical timestamps. Therefore layout-only cleanup preserves the previous `revision_date`; semantic/content/status changes advance it.
- Recovery/validation should flag pathological whitespace growth rather than publishing it as normal prompt formatting.


## 27.09.2026 — whitespace / UI regression safeguards


### Master whitespace invariant
- Raw `video-prompts.md` must not accumulate repeated blank-line runs from connector/file conversions.
- Safe normalization: convert line endings consistently and collapse runs of 2+ blank separator lines to a single blank separator; do not alter non-whitespace prompt text.
- Validator revision fingerprint treats repeated blank-line layout noise as non-semantic, so whitespace cleanup alone preserves the previous `revision_date`.
- After normalization verify scene count, prompt-fence count, IDs/anchors and Drive↔GitHub mirror before completion.


### Control Center regression checks
- Metric `Промтов` must target `#full-prompts` inserted before the **first active scene heading** (`sceneIdFromTitle(...) !== null`), never hard-code `Scene 1`.
- In light theme `.analysis-picker > summary` must use the light button palette; verify both closed/open/hover states.
- These checks are part of normal site JS/CSS validation together with syntax, duplicate IDs and secret scan.


### Topview freshness separation
- `sync-from-drive.yml` freshness and `topview-status.json.checked_at` are independent. A successful master sync must never be interpreted as proof that Topview slots were refreshed.
- When Topview connector/background access is unavailable, preserve last verified snapshot; UI/operations must treat its age explicitly as telemetry freshness, not silently relabel it as current.


## 27.09.2026 — даты монтажных версий и незавершённая публикация Topview


- В chooser `Монтажный разбор` сохраняются два пункта: `Первая версия` с датой **17.09.2026** (публикация завершённого первого HTML; same-ID Drive modified 17.09) и `Вторая версия` с датой **24.09.2026** (дата отчёта в самом HTML новой сборки). Дата загрузки второго файла в Drive по Москве — 25.09 — не заменяет дату, указанную автором в отчёте. Обе ссылки сохраняются.
- При разборе stale Topview обнаружен journal-only cycle: запись о свежей проверке была добавлена, а публичный snapshot и stable checkpoint остались прежними. Выполнен live emergency refresh; подробная фактическая отметка хранится только в runtime JSON, не в этой инструкции.
- Уточнение уже действующего publication gate: свежая запись journal или успешный Drive sync не доказывает обновление Topview. Перед успешным завершением обязателен exact read-back map/status/checkpoint, совпадение `checked_at`, `updated_at`, `last_scan_at`, task IDs/counts и проверка опубликованного Pages snapshot. Нельзя завершать successful cycle после записи только journal.
- Watcher и Recovery сохраняют действующие расписания HH:00 / HH:05 Europe/Moscow и `is_enabled=true`. Recovery считает свежий journal при старом public checkpoint незавершённой публикацией; deterministic emergency refresh разрешён только по существующим stale/failed и one-writer правилам. При недоступном connector не подделывать timestamp.
- Для лёгкого hourly run хранить большие Board/task payloads внутри code-mode orchestration, если она доступна; в контекст выводить компактные ID/status/model/queue/ETA projections. Полные prompts/references нужны только для неизвестного candidate. Просматривать все строки требуемых страниц, но не выгружать в контекст base64 и повторяющиеся известные промты.


## 30.09.2026 — повторный stale-snapshot и приоритет публикации в hourly automation


- Диагностика инцидента: несмотря на включённые расписания watcher HH:00 и Recovery HH:05 (Europe/Moscow) и их фактические scheduled last-run, публичный `topview-status.json` и стабильный `topview-checkpoint.json` оставались на 28.09 22:57:50Z; `instruction-sync-status.json.checked_at` — на 28.09 23:09:38Z. Время `last_run_time` автоматизации или успешный Drive-sync не свидетельствует о публикации. Конкретную причину недопубликации без журналов scheduled execution не утверждать; background connector access может отличаться от интерактивного Project Chat.
- В live Project Chat прямая проверка Topview обнаружила завершившуюся техническим success Scene 21 и две новые активные 15s Seedance 2.0 задачи: PART 1 и PART 2 Scene 27, обе normalization-exact по соответствующим существующим prompt-блокам с reference-token заменами. На момент исправления canonical slow Scene ID = `22,23,24,26,27`; task slots = `6/6`, Scene 27 занимает два. Это исторический checkpoint от 30.09, НЕ вечная runtime-истина; в каждом новом цикле снова читать свежие master/status/Topview.
- Восстановление 30.09: same-ID Drive master minimal render-state reconciliation, затем `topview-task-map.json`/journal → PUBLIC `topview-status.json` → `topview-checkpoint.json` **последним**, read-back exact equality task IDs/counts/timestamps; `review-ledger` только result receipt, никакого auto-approval; полная сверка 7/7 Drive↔GitHub instructions и свежий сертификат; `SYNC-TRIGGER` → validator → mirror/status → успешный Pages build/deploy и проверка собранного статического артефакта.
- Приоритет почасовых prompt-ов уточнён без смены authority, cadence или one-writer модели: watcher **обязан сперва довести публикацию map/status/checkpoint до read-back**, а не останавливаться после чтения/journal. Recovery **сначала** отдельно обновляет честный 7/7 instruction certificate (независимо от доступности Topview), затем проверяет liveness Topview и выполняет разрешённый аварийный refresh, только потом тяжёлый daily deep audit. Нельзя считать scheduled run выполненным, если публичный timestamp не изменился после реальной успешной проверки.
- При недоступности фонового Topview/Drive connector не двигать checked_at/last_scan_at и не придумывать telemetry; оба задания оставлять enabled, повторять в следующий HH:00/HH:05. Если публичная свежесть превышает три часа на нескольких запусках — один конкретный сигнал о сбое вместо бесконечного молчаливого stale. Устаревшая telemetry/certificate сама по себе не делает канонический master красным без подтверждённого authority mismatch.
- Validator-предохранители, которые нельзя ломать при служебной правке master: дословное поле `**Последняя полная синхронизация:** **...**` и отдельная буквальная метка `**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**` в TOC и теле каждой slow-сцены. Количество параллельных task attempts (`Scene 27 × 2`) писать **за пределами** этой метки. Иначе validator закономерно опубликует non-green status, даже когда реальная Topview-карта верна.


## 30.09.2026 — уточнение двухуровневого восстановления без третьей автоматизации


Эта секция уточняет ранее установленную схему, не заменяя полный runbook выше. PRIMARY watcher `Topview Scene Intake & Slow Watch` (`6aac794245e481919ee7155c461cc77e`) работает exact hourly HH:00 Europe/Moscow; EXISTING `AI Film Recovery Sync` (`6aac3e4dfe6c81918b3eead8529edf30`) exact hourly HH:05. Оба сохранены `is_enabled=true`. Третью ChatGPT scheduled task НЕ создавать: текущий лимит активных задач достигнут; независимая публичная проверка добавлена в prompt самого Recovery (обновлён 30.09 около 14:34 UTC). Сам факт сохранения prompt не доказывает очередной успешный фоновый цикл: следующий `topview-status.json.checked_at` и инструкция-сертификат нужно проверять после HH:00/HH:05.


- Watcher: реальное чтение Topview → task-map + journal (internal) → `topview-status.json` (PUBLIC) → `topview-checkpoint.json` LAST. Обязательный read-back и единый actual `checked_at` / `map.updated_at` / `map.last_scan_at` / `checkpoint.checked_at`; число занятых слотов равно количеству активных уникальных task IDs (НЕ числу уникальных Scene IDs), `free_slots = capacity - occupied_slots`. Если статусы не изменились, после ДОКАЗАННОГО нового чтения всё равно обновить свежий checked_at/queue/ETA. Не завершаться после одного journal/операционного last-run.
- Recovery в КАЖДОМ HH:05 цикле, даже при недоступности Topview, сначала независимо читает live PUBLIC GitHub `topview-status.json`, `topview-task-map.json`, `topview-checkpoint.json`, `instruction-sync-status.json`, `project-status.json`. Порог инцидента Topview `checked_at` старше 105 минут; сертификат инструкций старше 165 минут; любое расхождение timestamp/task IDs/slots/slow Scene IDs — отдельное основание для восстановления. Новый `project-status.synced_at`, свежий journal, недавний Pages build или automation last-run НЕ означают свежую Topview-проверку.
- Recovery В КАЖДОМ HH:05 цикле повторяет ПОЛНУЮ exact content сверку семи канонических Drive docs с GitHub mirrors, а не только при stale-flag. Если mismatch — минимальная SERIAL mirror correction GitHub FROM Drive, без обратной записи в Drive. Только после реального 7/7 совпадения публикует `instruction-sync-status.json.checked_at` как фактическое время проверки, делает read-back и добивается, чтобы `project-status` и Pages отражали сертификат (через SYNC-TRIGGER/validator при необходимости). Никогда не обновлять дату сертификата без чтения источников.
- Если watcher не довёл публикацию до конца и НЕ продолжает запись прямо сейчас, Recovery при наличии фонового Topview connector выполняет deterministic emergency live exact task lookup + paginated VIDEO Board discovery и публикует всю transaction в правильном порядке. При недоступном коннекторе сохраняет реальные исторические timestamp/occupancy, не придумывает состояние и сообщает предметный liveness blocker; master authority health остаётся независимым от freshness telemetry. Уведомление — один компактный инцидент на один непрерывный сбой, без почасового спама, после восстановления допустима одна resolution отметка.
- На сайте последнее проверенное число занятых слотов НЕ должно без оговорки преподноситься как live, если timestamp устарел. Три представления Control Center обязаны читать один опубликованный snapshot. Опасные действия Topview (approve, delete, close, rerun, new launch) не выполняются автоматически; technical success только result receipt.
- В GitHub присутствует `scripts/check_public_freshness.py` — read-only проверка возраста/инвариантов, без доступа к Topview/Drive и без права освежать датировки. Попытка создать `.github/workflows/public-freshness-watchdog.yml` была заблокирована на записи: НЕ считать новый GitHub scheduled workflow установленным или работающим. Независимую проверку публичных JSON сейчас реализует prompt существующего Recovery; при будущей разрешённой активации отдельного CI workflow потребуются реальная проверка файла/run и обновление canonical docs/Handoff.
- В опубликованном master на 30.09: slow Scene IDs = 22,23,24,26,27 (пять сцен), шесть Topview tasks: Scenes 22/23/24/26 ×1 и Scene 27 ×2 (оба Seedance 2.0 15s). Scene 21 terminal success, не approval. Это исторический verified snapshot на `2026-09-30T13:45:38.844Z`, не подменяет следующий live read. Сверка семи инструкций на `2026-09-30T13:58:32.341Z`; `project-status.synced_at` на момент последней проверки `2026-09-30T14:21:09Z`. Не выводить свежесть одного домена из timestamp другого.
- Служебные метки master валидатора: дословные `**Последняя полная синхронизация:** **...**` и `**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**` в TOC/секции; примечание о параллельных попытках — вне жирной метки. Instruction status обновлять только после exact mirror read-back.
## 05.10.2026 — защита от повторного отставания Watcher / Recovery


- Если сайт снова показывает старый Topview timestamp или старую instruction-сверку, **первым шагом проверить `is_enabled` обеих существующих автоматизаций**, а не создавать третью задачу. Исторически 05.10 Watcher и Recovery были обнаружены `is_enabled=false`, из-за чего обновление остановилось.
- Существующие роли сохраняются: Topview Watcher — HH:00, Recovery — HH:05. Recovery уже является независимым freshness verifier / authorized repair layer; отдельный третий watchdog не нужен.
- Если автоматизация выключена не по явному решению владельца, разрешено восстановить `is_enabled=true` и затем сделать live reconciliation. Если владелец явно выключил её сам — не включать против его решения.
- Успешный automation run не доказывает свежесть. Success определяется только фактическим продвижением PUBLIC `topview-status.json.checked_at`, согласованным `task-map.updated_at/last_scan_at`, stable checkpoint и read-back.
- После пользовательского запуска новой Topview-задачи watcher/recovery должны сопоставить её с existing Scene по prompt, обновить occupied slots и не создавать новый Scene ID, если mapping однозначен. Текущий пример: «Песня Маши 9» `117b9d976d2c4a54945256e79fc64639` = existing Scene 20, шестой active slot.


## Scene Reference Pack automation — 07.10.2026


**Reference-first rule.** For every new or materially changed scene, determine the minimum reference set *before* final prompt preparation or a Topview submit: character identity sheets, exact location/environment, props, first/last continuity frames, and scene-specific pose/composition stills when they materially reduce ambiguity. Reuse approved assets first; do not regenerate a good approved still without a creative reason.


**One-image QC loop.** Generate scene-specific stills one at a time. After every result, inspect identity, age, hair/fur, wardrobe, body proportions, character count, left/right geography, exact location geometry, lighting state and requested pose. If the result drifts, merges faces, duplicates characters, changes anatomy/costume/location or misses the pose, reject it and continue with an adjusted method. For multi-character scenes prefer verified small subgroups and then a final group; individual model sheets always outrank composition helpers for identity.


**Save-before-next invariant.** The instant a still is accepted as useful, persist it *before* starting the next image: same Scene ID folder in Google Drive `Scene Reference Packs/Scene N — Reference Pack` (Scene 28 keeps its existing same-ID pack), Library recovery mirror `/AI Film/Scene Reference Packs/Scene N`, and GitHub/site when the still is actually used by the scene. The site must show used refs as compact thumbnails linking to the full file; never embed them full-size in a way that changes page scale.


**Existing Topview scenes.** Do not ask the owner to re-upload inputs already available from Topview. Recover the exact task input images from live Board task metadata/S3 through the authorized Reference Bridge, record provenance in the scene pack manifest, and propose only additive replacements/improvements. Topview remains generation telemetry/provenance, not story authority.


**Launch command contract.** `запускай сцену N` means: fresh-read canonical master/status -> resolve Scene N pack and prompt -> verify or create any genuinely required missing refs -> update reference mapping if necessary -> live Topview preflight (model/input mode, six-slot slow lock, unlimited-vs-credit path) -> submit the requested generation. Do not ask the user to re-send an already recoverable reference. Do not silently spend credits on helper-image generation: use a route verified as unlimited/zero-credit for that submit, or stop before submit and report the limitation. Technical success never means editorial approval.


**Checkpoint rule for long work.** Treat `pack structure -> source recovery -> new reference generation/QC -> site publication -> canonical instructions/handoff/sync verification` as separate checkpoints. Persist every completed checkpoint before starting the next. If a chat/Work run ends, the successor reads the handoff and `scene-reference-plan` and resumes from the first incomplete checkpoint rather than restarting.


**Reference-pack publication cycle.** For an accepted scene ref: save Drive first -> write/update scene manifest -> Library recovery -> GitHub binary under `references/scenes/scene-N/` -> add compact thumbnail/link in the same Scene section of canonical master -> `SYNC-TRIGGER` -> verify master hash/project-status/Pages. A full-size image appearing directly in the scene is a regression. Do not publish rejected/duplicate/face-mixed previews as approved refs.


## Claude Code bootstrap adapter — 07.10.2026


- Repository-root `CLAUDE.md` is a non-canonical Claude Code bootstrap pointer only. It does not increase the seven-document canonical takeover set and is excluded from `instruction-sync-status.json` 7/7 certification.
- Claude Code must use it to start the normal takeover, then read the seven fresh Drive canonical docs, fresh exact Drive master, and live status JSON before substantive work.
- `CLAUDE.md` never overrides Drive authority and must not become a duplicated handoff/recovery body.
- Instruction verification and repair remain seven-doc Drive → GitHub exact mirror only; `CLAUDE.md` is verified separately as a repository adapter.

## 09.10.2026 — Control Center и синхронизация: действующие контракты

- **Сигналы статуса сайта.** `health` красный — только при проверенной проблеме канона (`project-status.health` ≠ ok, несовпадение SHA загруженного master со статусом, ошибка 7/7). Жёлтый (`.health.warn`) — канон в порядке, но `topview-status.json.checked_at` или `automation-monitor-status.json.last_scheduled_cycle.completed_at` старше 120 мин, отсутствует, некорректен или более чем на 10 мин в будущем, либо `last_scheduled_cycle.health` ≠ ok. Отсутствие файла монитора не окрашивает статус (обратная совместимость).
- **`ci-status.json`** (публикует `sync-from-drive.yml`, шаг «Publish CI state change»): `last_conclusion`, `last_failure_at`, `last_failure_run_url`, `last_success_at`. Пишется только при смене результата. Сайт не обращается к `api.github.com`.
- **Пульс синхронизации.** `project-status.json` коммитится сразу при любом изменении содержимого; если отличаются только `synced_at`/`age_hours`/`age_hours_at_status_build`, коммит не чаще раза в 45 мин (сообщение «Sync heartbeat…»). Лимит свежести master-sync 100 мин не меняется.
- **Миниатюры.** `build-thumbnails.yml` при push в `references/**` (кроме `references/thumbs/**`) запускает `scripts/build_thumbnails.py`: WebP ≤640 px в `references/thumbs/<путь>.webp`, манифест `references/thumbs/manifest.json` с SHA-256 источника. Сайт подменяет `src` в галереях на миниатюру; ссылки ведут на оригинал; при ошибке загрузки — откат на оригинал. `--check` показывает устаревшие миниатюры.
- **Реестр персонажей** хранит пути к файлам вместо data URI.
- **Master — только LF без BOM.** Проверки `canonical_master_lf_line_endings` и `canonical_master_blank_spacing_compact` (с учётом CRLF) блокирующие. После каждой записи master проверять отсутствие `\r`.
- **`marked`** — локальный `vendor/marked-15.0.12.min.js`, без CDN; HTML master проходит `safeHtml()` (удаляет script/iframe/object/embed/form, on*-атрибуты, javascript:-ссылки).
