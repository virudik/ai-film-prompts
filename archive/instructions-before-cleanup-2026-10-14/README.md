# AI Film Prompts Master

Canonical repository (prompt master, instructions, statuses), recovery documentation and Control Center for the AI Film project.

## Canonical source

Since 11.10.2026 the **only editable canon is this repository, branch `main`**: `video-prompts.md` (prompt master) and the seven instruction documents listed below. Google Drive (`AI Film Prompts Master`), Notion, ChatGPT Library and Project files are read-only backup copies, refreshed automatically; they never override `main`. Edits are minimal commits to `main` followed by validation, status and Pages checks (see `CLAUDE.md` and `SYNC-RUNBOOK.md`).

## New-chat / takeover reading order

Before editing the project, read the full instruction/recovery set:

1. [`NEW-CHAT-HANDOFF.md`](./NEW-CHAT-HANDOFF.md)
2. [`SYNC-RUNBOOK.md`](./SYNC-RUNBOOK.md)
3. [`AI-PROJECT-GUIDE.md`](./AI-PROJECT-GUIDE.md)
4. [`PROMPT-STYLE-GUIDE.md`](./PROMPT-STYLE-GUIDE.md)
5. [`USER-GUIDE.md`](./USER-GUIDE.md)
6. [`README-AI-SYNC.md`](./README-AI-SYNC.md)
7. [`BACKUP-AI-RUNBOOK.md`](./BACKUP-AI-RUNBOOK.md)

Then read `video-prompts.md` from fresh `main` plus live `project-status.json`, `topview-status.json`, `instruction-sync-status.json`, `monitor-role.json` and open owner tasks.

## Prompt standard

All new or substantially reworked prompts must follow the full `PROMPT-STYLE-GUIDE.md` and be checked against 1–2 current master scenes. Do not replace it with a short generic prompt or chat summary.

## Control Center

Viewer: `https://virudik.github.io/ai-film-prompts/`

Current site includes active-scene navigation, full prompts, merged slow/Topview telemetry, sync health indicator, character references, light/dark theme, and native anonymous comments/replies through Supabase in a collapsible `💬 Комментарии, идеи и предложения` section directly below `Контрольный отпечаток`.

## Other stores

- **Notion `Кино`** — story/idea/history bank; not prompt authority.
- **ChatGPT Library** — recovery mirror/cache; not prompt authority.
- **Topview** — render telemetry; technical success is not approval.
- **Supabase** — comments backend only; no master mutation rights.

## Material-change rule

A material site/workflow/prompt-standard/authority change is not complete until the relevant instructions and `NEW-CHAT-HANDOFF.md` are updated in `main`, `python3 scripts/cert_github.py .` and the tests pass, and the Pages deployment is verified. Backup copies (Drive, Notion pointer, Library) are refreshed best-effort afterwards.

## New-chat takeover
Before acting as the project editor, a new chat must read all seven canonical project/recovery documents in this repository, then `video-prompts.md` and the live status JSON from fresh `main`. It must also review:
- [Characters / references](./references.html) + `character-references.json` to map canonical names/aliases to approved model sheets and current prompt usage;
- [Montage analysis](./Seregius_montazhny_razbor.html) together with `film-analysis.md` and `film-backlog.md`.

Only after a cross-layer audit of `main` ↔ site/Pages ↔ references ↔ montage context ↔ Notion (backup copies are checked best-effort) should the new chat report that it is ready to continue the predecessor's work.

Natural-language character shorthand is expected: requests such as “Паша говорит Саше, потом заходит Серёжа” should be resolved from the approved character registry/current master without asking the user to repeat known appearance.

