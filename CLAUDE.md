# CLAUDE.md — AI Film Серёгиус bootstrap

> **Role:** repository bootstrap for Claude Code only.
>
> **NON-CANONICAL:** this file is not an eighth project instruction and is not a source of truth. Since 11.10.2026 (owner decision, 03:25 MSK) the canon is this repository, branch `main`: `video-prompts.md` and exactly seven instruction documents. Google Drive, Notion, ChatGPT Library and Project files are read-only backup copies. If this file conflicts with fresh `main` or live status, fresh `main` wins.

## 1. Start every substantive project task with live takeover

Do not assume local clones, old chat history, attachments, backup copies or prior summaries are current. `git pull` first.

Read the seven canonical instruction documents from `main` in this order:

1. `NEW-CHAT-HANDOFF.md` (top blocks = live state)
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

Then read from `main`:

1. `video-prompts.md` (canonical master);
2. live `project-status.json`;
3. live `topview-status.json`;
4. live `instruction-sync-status.json`;
5. `monitor-role.json` and open owner tasks in Supabase `owner_decisions`.

For prompt work, additionally follow `PROMPT-STYLE-GUIDE.md` and inspect 1–2 nearby current master scenes.

For story/editing work, additionally read `film-analysis.md`, `film-backlog.md`, and relevant Notion `Кино` context when available.

## 2. Authority

`GitHub main (master + 7 instructions, statuses, site/Pages) → Topview generation telemetry → Notion story/ideas/history`; backups (Drive, Notion pointer, Library, Project files) never override `main`.

## 3. Capability preflight

Before any write, confirm the environment can read/write this repository, run validation (`scripts/validate_site.py`, tests) and verify resulting status and Pages when relevant. Do not create `v2`, `final`, `copy` or replacement masters. Do not ask the owner to repeat information already available in canonical/project sources.

## 4. Master and instruction edits

- Before writing the master, `git pull` again and edit from fresh `main`.
- Master edit: `minimal commit → SYNC-TRIGGER.txt → validator project-status.health=ok → Pages → verification`.
- Instruction edit: `minimal commit → python3 scripts/cert_github.py . → tests → push → verification`.
- A rejected push means another writer: re-read and redo from scratch; never replay a stale prepared edit after a timeout or uncertain result.
- One writer at a time: `scripts/monitor_role.py` and `monitor-role.json` decide which monitor writes; do not edit canon concurrently with ChatGPT.
- Do not declare completion until read-back and verification pass.

## 5. Backup copies

Refreshed periodically, never edited instead of canon (table: `BACKUP-AI-RUNBOOK.md` «РЕЗЕРВНЫЕ КОПИИ КАНОНА»). A manually edited Drive copy (issue `drive-drift`) is not overwritten — port the edit into `main` or ask the owner.

## 6. Topview safety

Topview is telemetry/source-task data, not editorial authority.

- Technical success is not approval.
- Never auto-approve, auto-delete, auto-rerun, or close scenes.
- Preserve the distinction between creative Scene ID and individual Topview task/render IDs.
- Generations only on owner command, unlimited mode via the Topview site; never spend credits.

## 7. Owner decision boundary

Ask the owner only for genuinely non-deterministic decisions: creative/editorial choices, ambiguous task ↔ Scene mapping, approval/rejection, rerender, deletion or scene closing, and other choices canonical rules cannot determine safely. Deterministic maintenance, verification, recovery, formatting and status work is done with tools, not handed back.

## 8. Material workflow changes

If a change materially affects workflow, site, authority or recovery: update the relevant canonical instruction(s) and the SAME `NEW-CHAT-HANDOFF.md` in `main` → `cert_github.py` → Notion pointer when relevant → backups best-effort.

## 9. Final rule

This file is intentionally short and stable. Do not copy the evolving handoff body into `CLAUDE.md`. **Fresh `main` always wins.**
