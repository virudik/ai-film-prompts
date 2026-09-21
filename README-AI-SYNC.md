# README-AI-SYNC v4.0

**Дата:** 20.09.2026  
**Назначение:** краткая карта архитектуры и синхронизации AI Film Project.

## Canonical data flow

`Google Drive video-prompts.md`
→ same-ID edit
→ GitHub `SYNC-TRIGGER.txt`
→ `sync-from-drive.yml`
→ validation
→ GitHub `video-prompts.md`
→ generated `project-status.json`
→ GitHub Pages / Control Center

Editable master:
`Google Drive / AI Film Prompts Master / video-prompts.md`  
ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`

GitHub `virudik/ai-film-prompts` — mirror/status/site layer, не второй master.

## Seven-document takeover / recovery set

Google Drive является authority для:

1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

Новый чат должен прочитать **все семь**, затем fresh master и live status JSON.

Instruction mirror flow:

`Drive seven docs`
→ exact compare
→ repair **Drive → GitHub only**
→ semantic consistency check
→ `instruction-sync-status.json`
→ `project-status.json` health projection

`instruction-sync-status.json` должен отслеживать все семь документов.

## Storage roles

### Drive
Canonical editable prompt master + canonical instruction/recovery docs.

### GitHub
Public mirrors, Control Center, scripts, status JSON, references, Pages.

### Notion
Story/idea/history bank. Не prompt authority.  
Operational pointer: `AI Film — Актуальная инструкция / Handoff`.

### ChatGPT Library
Recovery mirror/cache. Не authority при доступном Drive.

### Topview
Read-only generation telemetry. Technical `success` != approval.

### Supabase
Comments backend only. No prompt/master mutation rights.

## Prompt-writing flow

Перед новым/существенно изменённым prompt:

`PROMPT-STYLE-GUIDE.md`
→ fresh Drive master
→ 1–2 current example scenes
→ write master-level prompt
→ same-ID master edit
→ sync/validation/Pages

Если следующий Scene ID очевиден из fresh master, редактор выбирает следующий новый стабильный ID сам. Удалённые IDs не переиспользуются.

## Master invariants

- no duplicate master versions;
- stable Scene IDs;
- `project-status.json` generated, never manually used as second master;
- slow membership is canonical from master/status;
- slow rerun/clear requires user decision/error;
- Topview success does not approve scene;
- current runtime counts/SHA/slow come from fresh master/status, not historical docs;
- raw master UTF-8 without BOM;
- global prompt rule `FRAME FILL / NO BARS`, unless user explicitly overrides.

## Control Center baseline

Viewer:
`https://virudik.github.io/ai-film-prompts/`

Current permanent features:
- Russian UI;
- active scene map + full prompts;
- merged slow + Topview telemetry;
- status/model/start/elapsed/queue/ETA;
- three-state sync lightsaber;
- reference/character viewer;
- light/dark theme (`ai-film-theme`);
- collapsible `Контрольный отпечаток`;
- directly below it collapsible `💬 Комментарии, идеи и предложения`;
- native Supabase read/post/reply without GitHub login.

Old `Архив GitHub` comments button is no longer part of the UI.

## Supabase comments

- org `Vint`;
- project `ai-film-comments`;
- ref `vzohfatqzyioydtgjiyd`;
- Edge Function `submit-comment`;
- public read published;
- anonymous post/reply;
- RLS;
- honeypot;
- rate limit 5 / 10 min / IP;
- frontend publishable key only;
- never expose service/admin secret;
- comments never mutate master.

## Material-change propagation

A permanent change to site architecture, workflow, prompt standard, authority, recovery or status model is not complete until:

`implementation`
→ relevant Drive docs
→ SAME `NEW-CHAT-HANDOFF.md`
→ `PROMPT-STYLE-GUIDE.md` if relevant
→ exact GitHub mirrors
→ fresh `instruction-sync-status.json`
→ status/Pages verification
→ Notion operational pointer
→ Library recovery copies

Do not propagate ephemeral queue/ETA/SHA as permanent prose across all docs.

## Site-only changes

Edit GitHub `index.html`.

After edit:
- JS syntax;
- duplicate IDs;
- no secrets;
- Pages success.

If it becomes a permanent feature, also run Material-change propagation.

## Topview flow

`project-status.json.slow_scenes`
→ exact verified Topview task
→ per-task queue/status/ETA
→ `topview-status.json`
→ site

No guessed task mapping. No queue copying between tasks. No automatic rerun/approval.

## Recovery safeguards

- sync workflow refetch/rebuild/retry for concurrent GitHub writers;
- BOM normalization/guard;
- live status freshness checks;
- historical snapshot != current invariant;
- Topview mapping against fresh current scene body;
- Drive → GitHub only for instruction repair.

## Definition of Done

Prompt/master change:
same-ID Drive write + successful sync + validation + exact mirror + current status + Pages.

Instruction/material change:
all seven Drive docs current + all seven GitHub mirrors exact + fresh instruction status + Notion pointer + Library recovery current.

If any required layer is not verified, report it explicitly rather than claiming full completion.

## Character / film-context flow

Takeover context теперь включает не только instructions + master/status, но и два обязательных смысловых слоя:

`references.html` + `character-references.json`
→ canonical name / alias / model-sheet map
→ cross-check current master
→ natural-language character resolution in new prompts.

`Seregius_montazhny_razbor.html`
+ `film-analysis.md`
+ `film-backlog.md`
+ relevant Notion `Кино`
→ compact current film/story/editing map.

Это позволяет следующему чату понимать запросы вида «Паша говорит Саше, потом заходит Серёжа» без повторного описания известных персонажей и понимать монтажную функцию новой сцены.

## Takeover readiness check

До readiness report агент проверяет актуальность seven docs, master/status, site, character registry, montage sources, Notion operational pointer и Library recovery. Safe documentation drift repair допускается по существующим authority rules; creative/approval conflicts требуют user decision.

Hourly automation должна оставаться лёгкой: проверять наличие/целостность этих слоёв и предупреждать о drift, но не перечитывать/перегенерировать тяжёлый montage HTML или image payload каждый час.

## Topview task-intake flow

Для previously unknown Topview video task сначала выполняется classification:

`Topview unknown video task`
→ already-known task ID? stop as known telemetry
→ exact/normalization-equivalent active canonical prompt or explicit provenance?
   → bind to **existing Scene ID**
   → if queued/running/init/processing: add existing Scene ID to canonical slow
   → preserve editorial/production state
   → no duplicate Scene ID
→ clearly distinct from active canonical scenes?
   → genuinely new scene
   → actual task prompt/model/reference metadata
   → next stable Scene ID
   → SAME Drive master write
   → canonical slow if running / `RESULT_RECEIVED` if already success
→ ambiguous?
   → no master mutation, notify user
→ `SYNC-TRIGGER.txt`
→ `sync-from-drive.yml`
→ validation
→ GitHub mirror / `project-status.json`
→ Pages
→ task↔Scene mapping / telemetry refresh.

Normalization may ignore only non-semantic `@image`/`<<<Image>>>`, whitespace/line-ending/reference-token formatting differences. Semantic resemblance alone must never cause a new task to be silently discarded. Actual Topview prompt of a genuinely new imported scene remains verbatim. Technical `success` never equals user approval.

## Service-files UI

`index.html` → `Служебные файлы` показывает все seven canonical/recovery docs русскими названиями, а также master, film-analysis и backlog.

## Recovery cadence

`AI Film Recovery Sync` = **hourly light + daily deep in one automation**.

Hourly light:
`seven docs / instruction status / master-status integrity / key site-context checks / security baseline`.

Daily deep (when `deep-audit-status.json.last_deep_audit_at` is missing or >=24h old):
`full master + prompt-style + characters + montage + Notion + Library + site + Supabase + Actions/Pages + recovery test`
→ update `deep-audit-status.json`.

The separate `Topview Scene Intake & Slow Watch` owns Topview task intake, one-to-many Scene→attempt history/current-attempt mapping, queue/ETA, slow re-entry on every new active attempt, and auto-creation of Scene IDs only for genuinely new creative scenes. Recovery Sync must not duplicate that work.

## Service-files grouping

Control Center `Служебные файлы` имеет две логические группы:
- `Инструкции — читать по порядку`: ровно 7 canonical docs, вертикально 1→7;
- `Рабочие файлы проекта`: `video-prompts.md`, `film-analysis.md`, `film-backlog.md`, также вертикально один под другим в порядке master → analysis → backlog.

Machine/recovery logic должна считать instruction set размером 7 независимо от количества project-data links в UI.

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

## Slow table: one Scene row, many render attempts

Control Center must visualize the canonical relation **one Scene ID → many Topview render attempts** without duplicating the creative scene.

UI rule:
- the slow table has exactly **one parent row per canonical Scene ID**;
- if that Scene has more than one known or active Topview attempt, the parent row shows the attempt count and provides an expandable attempt list;
- each attempt row shows its own model, technical status, start time, elapsed time, queue and ETA when those values are available for that exact task;
- when more than one attempt is active simultaneously, the attempt rows are expanded by default so parallel renders are immediately visible;
- canonical `slow_scenes` still contains the Scene ID once, regardless of how many attempts are active;
- completed/historical attempts may remain visible in the expanded history but do not create extra Scene IDs;
- `topview-task-map.json` is the durable Scene→attempt-history mapping; `topview-status.json` provides current/active telemetry. The UI may combine both, but must never merge queue/ETA values from different task IDs;
- for full parallel-attempt telemetry, `topview-status.json` should expose per-task current data for every active attempt (for example `active_attempts[]`), while keeping backward-compatible current-attempt fields;
- technical `success` never equals approval and does not automatically clear canonical slow.

This presentation rule is part of the permanent Control Center baseline and must be checked after site/UI changes.
