# AI Film Prompts Master

Canonical repository of the AI Film project «Серёгиус»: prompt master, the 7 instructions, machine status, the Control Center site and robots (GitHub Actions).

## Canonical source

**Canon = this repository, branch `main`** (owner decision 11.10.2026): `video-prompts.md` (the only prompt master) and exactly seven instruction documents. Google Drive, Notion, Claude Project, ChatGPT Project and Library are read-only backup copies that are refreshed automatically (`BACKUP-AI-RUNBOOK.md`) and never override `main`. Topview is generation telemetry; Notion holds story, ideas and history.

## New-chat / takeover reading order

Before editing the project, `git pull` and read the full instruction set in order:

1. [`NEW-CHAT-HANDOFF.md`](./NEW-CHAT-HANDOFF.md) (top blocks = live state)
2. [`SYNC-RUNBOOK.md`](./SYNC-RUNBOOK.md)
3. [`AI-PROJECT-GUIDE.md`](./AI-PROJECT-GUIDE.md)
4. [`PROMPT-STYLE-GUIDE.md`](./PROMPT-STYLE-GUIDE.md)
5. [`USER-GUIDE.md`](./USER-GUIDE.md)
6. [`README-AI-SYNC.md`](./README-AI-SYNC.md)
7. [`BACKUP-AI-RUNBOOK.md`](./BACKUP-AI-RUNBOOK.md)

Then read the fresh `video-prompts.md` and the live `project-status.json`, `topview-status.json`, `instruction-sync-status.json`, `monitor-role.json` and the open owner tasks in Supabase `owner_decisions`. `CLAUDE.md` is only a bootstrap pointer for Claude Code, not an eighth instruction.

## Prompt standard

All new or substantially reworked prompts follow the full `PROMPT-STYLE-GUIDE.md` and are checked against 1–2 current master scenes. Do not replace it with a short generic prompt or a chat summary.

## Writing to the canon

Minimal commit → (`SYNC-TRIGGER.txt` for the master) → validator `project-status.health=ok` → Pages → verification; for instructions: minimal commit → `python3 scripts/cert_github.py .` → tests → push → verification. One writer at a time (`monitor-role.json`, `scripts/monitor_role.py`); a rejected push means another writer: re-read and redo from scratch.

Checks: `python3 -m unittest discover -s tests`, `python3 scripts/validate_site.py`, `node tests/site_status_check.js` (with `python3 -m http.server 8765`), `python3 scripts/build_takeover_brief.py . shadow` (derived, non-canonical brief).

## Control Center

Viewer (GitHub Pages, read-only): `https://virudik.github.io/ai-film-prompts/`

The site includes active-scene navigation, full prompts, merged slow/Topview telemetry (live status of each slow scene), sync health indicator, character references, light/dark theme, owner buttons, links to the private Drive copies of finished videos, and native anonymous comments/replies through Supabase in a collapsible `💬 Комментарии, идеи и предложения` section directly below `Контрольный отпечаток`.

## Robots (GitHub Actions)

Full map: `README-AI-SYNC.md` («Компоненты и workflow»).

- `topview-robot.yml` — Topview telemetry writer: `scripts/topview_api_scan.py` (read-only GET) → `scripts/robot_telemetry.py`, minimal slow-row master edits via `scripts/master_slow_edit.py`. Since 13.10.2026 `monitor-role.json` has `primary=robot`, `standby=chatgpt` (ChatGPT takes over by itself after 180 minutes without a verified healthy robot cycle); the Claude monitor is off. Kill switch: GitHub Variable `ROBOT_TELEMETRY=shadow`. Details: `ops/ROBOT-TELEMETRY.md`.
- `sync-from-drive.yml` (historical name; it no longer pulls the master from Drive) — builds `project-status.json` from `main` and applies owner buttons from Supabase `owner_decisions` (`scripts/process_owner_decisions.py`, `scripts/robot_master_actions.py`).
- `topview-video-archive.yml` + `scripts/topview_video_archive.py` — copies finished MP4s of active scenes into a private Drive folder through pre-created owner slots; only metadata (`topview-video-archive.json`) goes to git (`ops/TOPVIEW-VIDEO-ARCHIVE.md`).
- `drive-write.yml` + `scripts/drive_write.py` — daily refresh of the read-only Drive copies.
- GitHub `schedule:` is unreliable, so Supabase pg_cron + pg_net start the robots via `workflow_dispatch` (`ops/ROBOT-TRIGGER.md`, SQL in `ops/supabase/`).
- `scripts/monitor_role.py` — one-writer guard (`claude` / `chatgpt` / `robot`).

Robots never start, approve, rerun or delete Topview generations and never remove a scene from canonical slow (only the owner's button does). Topview generations run only on the owner's command, in unlimited mode through the Topview site; paid MCP/Canvas generation is forbidden.

## Other stores

- **Notion `Кино`** — story/idea/history bank; not prompt authority.
- **Topview** — render telemetry; technical success is not approval.
- **Supabase** — comments backend and owner decisions (`owner_decisions`); no master mutation rights.
- **Backups** (Drive, Library, Project files) — read-only copies, see `BACKUP-AI-RUNBOOK.md`.

## Material-change rule

A material site/workflow/prompt-standard/authority change is not complete until the relevant instructions and `NEW-CHAT-HANDOFF.md` are updated, the certificate is refreshed (`scripts/cert_github.py`), verification passes, and the Notion pointer is updated where applicable; backup copies are best-effort.

## New-chat takeover

Before acting as the project editor, a new chat must read all seven instructions, the fresh master and the live status JSON. It must also review:
- [Characters / references](./references.html) + `character-references.json` to map canonical names/aliases to approved model sheets and current prompt usage;
- [Montage analysis](./Seregius_montazhny_razbor.html) (and the [second version](./Seregius_montazhny_razbor-2.html)) together with `film-analysis.md` and `film-backlog.md`.

Only after a cross-layer audit of main ↔ site ↔ references ↔ montage context ↔ Notion should the new chat report that it is ready to continue the predecessor's work.

Natural-language character shorthand is expected: requests such as «Паша говорит Саше, потом заходит Серёжа» should be resolved from the approved character registry/current master without asking the user to repeat known appearance.
