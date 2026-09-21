# SYNC-RUNBOOK v4.0 — AI Film Project

**Дата актуализации:** 20.09.2026  
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
9. проверить `project-status.json` не содержит `instruction_sync_stale/error`;
10. обновить Notion operational pointer, если меняется будущий workflow;
11. обновить Library recovery copies.

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
- Library recovery mirror не refreshed.

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
- `success` не снимает slow-lock.

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

После материальных instruction/handoff changes обновлять Library copies:
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
- Library recovery current.

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
- Library recovery copies marked recovery-only and not misleadingly newer/authoritative.

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

## Canonical rule — Scene ID ≠ Topview render attempt

Это обязательное правило для master, Topview watcher и recovery:

- **Scene ID** идентифицирует саму творческую сцену/сюжетный beat. Он не меняется только потому, что сцену снова отправили в генерацию.
- **Topview task ID** идентифицирует одну конкретную попытку рендера. У одной Scene ID может быть **сколько угодно последовательных или параллельных render attempts**.
- Повторный запуск уже существующей сцены — с тем же prompt, исправленным prompt или другим допустимым вариантом этой же сцены — **не создаёт новый Scene ID**, если связь с существующей сценой доказана по prompt lineage, refs/story beat, предыдущему mapping или explicit provenance.
- Новый неизвестный Topview task для существующей сцены должен быть **добавлен как новая attempt этой Scene ID**, а не заменять историю старой попытки. В telemetry/task-map нужно сохранять history известных task IDs и отдельно указывать текущую/активную попытку.
- Если новая attempt имеет Topview state `init`, `queued`, `running` или `processing`, существующая Scene ID должна быть **добавлена/возвращена в canonical slow-list**, даже если эта сцена уже когда-то генерировалась, завершалась или ранее была вручную снята с slow.
- Несколько одновременно активных attempts одной сцены всё равно означают один slow Scene ID; при этом должны сохраняться все активные task IDs.
- Завершение одной attempt (`success`, `fail`, `cancelled`) не означает `APPROVED`, не создаёт новую сцену и не стирает другие attempts. `success` — только техническое завершение конкретного рендера.
- Автоматика **не снимает slow автоматически только из-за success**. Пользовательское решение о результате/slow-lock имеет приоритет; новая последующая active attempt снова обязана вернуть сцену в slow.
- Новый Scene ID создаётся только для **действительно новой творческой сцены**, а не для нового рендера, retry, rerender или prompt-variant существующей сцены.
- Если нельзя надёжно решить, является task новой сценой или новой attempt существующей — no write / no new Scene ID; пометить ambiguous и уведомить пользователя.

Ключевая модель данных: **Scene 1 → N Topview attempts**. Scene lifecycle и render-attempt lifecycle — разные сущности.

## Slow table: compact UI, full internal render-attempt telemetry

Control Center intentionally keeps the slow table visually compact:

- the main slow table shows exactly **one row per canonical Scene ID**;
- no attempt counters, expandable attempt rows, or duplicate Scene rows are shown in the ordinary graphical interface;
- the row displays only the current/primary telemetry snapshot for that Scene ID so the original table proportions and readability remain stable;
- repeated and parallel Topview attempts are still preserved internally in `topview-task-map.json` and `topview-status.json` and remain available to automations, audits and statistics;
- canonical `slow_scenes` contains the Scene ID once regardless of the number of active attempts;
- if several attempts are active simultaneously, automation must still query and preserve all of them internally; the simplified UI must never be treated as evidence that only one attempt exists;
- queue/ETA values from different task IDs must never be merged into a fabricated value;
- technical `success` never equals approval and does not automatically clear canonical slow.

This is a deliberate UX choice: **full fidelity in machine state, minimal noise in the owner-facing interface**.