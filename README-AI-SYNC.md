# AI Film — sync architecture v3.5


## Source of truth


Editable:
Google Drive `AI Film Prompts Master/video-prompts.md`
ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`


Public mirror:
GitHub `virudik/ai-film-prompts`


Viewer:
`https://virudik.github.io/ai-film-prompts/`


## Data flow


Drive master
→ `SYNC-TRIGGER.txt`
→ `sync-from-drive.yml`
→ validation
→ GitHub `video-prompts.md`
→ generated `project-status.json`
→ GitHub Pages


Instruction mirror / recovery:
private Drive instructions (canonical)
→ hourly `AI Film Recovery Sync` exact-text compare
→ automatic repair only Drive → GitHub when mirror differs
→ semantic consistency check
→ `instruction-sync-status.json`
→ project-status rebuild

`Topview Slow Watch` continues hourly Topview telemetry and authorized instruction-health verification; it does not make production approval decisions.


Topview telemetry:
mapped task per slow Scene ID
→ per-task queue/status/ETA
→ `topview-status.json`
→ site


## Never do


- do not edit `project-status.json` by hand
- do not treat GitHub master mirror as editable source
- do not create duplicate master versions
- do not rerun slow scene because of audit/UI suggestion
- do not reuse one Topview queue snapshot for every task
- do not replace user-confirmed character model sheets from similarity


## Current viewer conventions


- Russian UI
- technical detail in `Контрольный отпечаток`
- service links in `Служебные файлы`
- clickable counters
- W-items remain a normal table
- Topview status localized
- queue label = `Очередь`
- time estimate remains current one-line combined form
- sync health uses three-state lightsaber: green `✓ СИНХРОНИЗАЦИЯ В ПОРЯДКЕ`, yellow `! БЫЛИ ОШИБКИ` during recovery observation, red for unresolved/stale error
- slow UI объединён: одна видимая canonical+Topview таблица; raw master slow-table скрыта только в presentation layer


## Reference architecture


`character-references.json` = identity registry
`references.html` = viewer
960px preview = lightweight web display
`reference-originals.zip` = Drive original archive


Verified 19.09.2026: all 8 confirmed entries have existing `references/full/*.jpg` paths and `references.html` opens `model_sheet.full_image` in the lightbox.


## Recovery


Start from:
1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. fresh Drive master
5. current status JSON files




## Write-race resilience


Direct Topview/instruction telemetry commits can advance `main` during a Drive sync. Since 19.09.2026 the sync workflow refetches the newest `origin/main`, rebuilds status on that head and retries non-fast-forward pushes instead of failing immediately. The site health indicator also applies freshness/latest-workflow checks rather than trusting an indefinitely old green JSON.


## Encoding normalization

Since 19.09.2026 the Drive sync normalizes an optional UTF-8 BOM before validating the Markdown header. The canonical raw master is kept UTF-8 without BOM. This prevents invisible encoding markers from producing false sync failures.

## Verified recovery 19.09.2026

Race retry and BOM normalization are now verified by multiple successful Drive-sync runs. Current verified fingerprint: revision `19.09.2026`, SHA-256 `861c19e4749ac35dc50c17cf18d8d7f1430bcdb45c99e7311fd65a65202a3cb6`, Drive/GitHub master exact match, project health `ok`, instruction sync `ok`.


## Recovery-warning UI

The Control Center keeps a recovered error visible in yellow until three consecutive successful sync workflow runs have followed the latest detected failure. Current unresolved failure or stale/unhealthy state is red; stable healthy state is green. Exact sync time is shown without a redundant relative `N minutes ago`. A Topview-success task that remains in the canonical slow list is labeled as waiting for user decision.
