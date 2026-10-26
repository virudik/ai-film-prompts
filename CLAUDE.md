# CLAUDE.md — AI Film Серёгиус bootstrap

> **Role:** repository bootstrap for Claude Code only.
>
> **NON-CANONICAL:** this file is not an eighth project instruction and is not a source of truth. Since 11.10.2026 (owner decision, 03:25 MSK) the canon is this repository, branch `main`: `video-prompts.md` and exactly seven instruction documents. Google Drive, Notion, ChatGPT Library and Project files are read-only backup copies. If this file conflicts with fresh `main` or live status, fresh `main` wins.

## 1. Start every substantive project task with live takeover

Do not assume local clones, old chat history, attachments, backup copies or prior summaries are current. `git pull` first.

**Short takeover (owner decision D7, 14.10.2026) — the default:**

1. `shadow/takeover-brief.md` — must say «Валиден при генерации: True» with all 15 rules ✓; otherwise do the full takeover;
2. `shadow/current-checkpoint.md` in full (verbatim top blocks of `NEW-CHAT-HANDOFF.md`);
3. live `project-status.json`, `topview-status.json`, `instruction-sync-status.json`, `automation-monitor-status.json`, `monitor-role.json`, `ops/canon-lock.json`, `ops/owner-tasks.json` and open owner tasks in Supabase `owner_decisions`;
4. the full sections your task needs («Что читать под задачу» in the brief): prompt work → `PROMPT-STYLE-GUIDE.md` + the target scene and 1–2 nearby current master scenes; story/editing → `film-analysis.md`, `film-backlog.md`, relevant Notion `Кино`.

**Full takeover** is mandatory when the brief is invalid or shows `✕ ANCHOR MISSING`; when the task edits any of the 7 instructions or materially changes workflow / site / authority / recovery; for recovery after an incident; when the task touches sync, schedules, slot semantics or rules shared by several scenes; when in doubt; or when the owner asks for a full takeover. Read the seven canonical instruction documents from `main` in this order:

1. `NEW-CHAT-HANDOFF.md` (top blocks = live state)
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

then `video-prompts.md` (canonical master) and the live status files above. Say in the readiness report which takeover (short / full) you used.

## 2. Authority

`GitHub main (master + 7 instructions, statuses, site/Pages) → Topview generation telemetry → Notion story/ideas/history`; backups (Drive, Notion pointer, Library, Project files) never override `main`.

## 3. Capability preflight

Before any write, confirm the environment can read/write this repository, run validation (`scripts/validate_site.py`, tests) and verify resulting status and Pages when relevant. Do not create `v2`, `final`, `copy` or replacement masters. Do not ask the owner to repeat information already available in canonical/project sources.

## 4. Master and instruction edits

- Before writing the master, `git pull` again and edit from fresh `main`.
- Master edit: `minimal commit → SYNC-TRIGGER.txt → validator project-status.health=ok → Pages → verification`.
- Instruction edit: `minimal commit → python3 scripts/cert_github.py . → tests → push → verification`.
- A rejected push means another writer: re-read and redo from scratch; never replay a stale prepared edit after a timeout or uncertain result.
- Canon edits require the live root or project lock from `ops/CANON-LOCK.md`; acquire, verify, then release your own lock. `monitor-role.json` only selects the telemetry writer; it does not grant or deny permission to edit canon. Inbox tasks and reference-review metadata use the explicit no-lock exceptions in that protocol.
- Agent coordination and responses to the same Claude thread follow `ops/OWNER-TASKS.md`; task state in GitHub is authoritative, Relay is the notification channel.
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
