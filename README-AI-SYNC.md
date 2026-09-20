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

## Topview auto-intake flow

Для genuinely new Topview video task:

`Topview new video task`
→ duplicate/retry guard
→ actual task prompt/model/reference metadata
→ next stable Scene ID
→ SAME Drive master write
→ canonical slow if running / `RESULT_RECEIVED` if already success
→ `SYNC-TRIGGER.txt`
→ `sync-from-drive.yml`
→ validation
→ GitHub mirror / `project-status.json`
→ Pages
→ task↔Scene mapping / telemetry refresh.

Actual Topview prompt сохраняется verbatim как фактически использованный source prompt. Автоимпорт не может превращать технический `success` в user approval.

## Service-files UI

`index.html` → `Служебные файлы` показывает все seven canonical/recovery docs русскими названиями, а также master, film-analysis и backlog.

## Recovery cadence

`AI Film Recovery Sync` = **hourly light + daily deep in one automation**.

Hourly light:
`seven docs / instruction status / master-status integrity / key site-context checks / security baseline`.

Daily deep (when `deep-audit-status.json.last_deep_audit_at` is missing or >=24h old):
`full master + prompt-style + characters + montage + Notion + Library + site + Supabase + Actions/Pages + recovery test`
→ update `deep-audit-status.json`.

The separate `Topview Scene Intake & Slow Watch` continues to own Topview task intake, task mapping, queue/ETA and auto-creation of genuinely new Topview video scenes. Recovery Sync must not duplicate that work.

## Service-files grouping

Control Center `Служебные файлы` имеет две логические группы:
- `Инструкции — читать по порядку`: ровно 7 canonical docs, вертикально 1→7;
- `Рабочие файлы проекта`: `video-prompts.md`, `film-analysis.md`, `film-backlog.md`, также вертикально один под другим в порядке master → analysis → backlog.

Machine/recovery logic должна считать instruction set размером 7 независимо от количества project-data links в UI.
