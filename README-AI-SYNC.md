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
- new active Topview task returns the same Scene ID to slow; when the last tracked active task becomes terminal, Topview-managed slow clears automatically without approval/editorial change;
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
