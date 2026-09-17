# AI Film Project — Start Here

This file explains how ChatGPT, Work, Claude, Gemini, DeepSeek, Grok, and other AI tools should use the shared prompt master and project context.

## 1. Canonical source of truth

The only editable prompt master is:

- Google Drive → `AI Film Prompts Master/video-prompts.md`

Google Drive folder:
https://drive.google.com/drive/folders/1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6

The public GitHub copy is a read-only mirror for external AI review:

- Viewer: https://virudik.github.io/ai-film-prompts/
- Raw master: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md
- Repository: https://github.com/virudik/ai-film-prompts
- Claude takeover runbook: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/CLAUDE-TAKEOVER-RUNBOOK.md

Do not create parallel masters such as `video-prompts-final.md`, `video-prompts-2.md`, `final-final`, etc.

`video-prompts.html` and the GitHub Pages viewer are generated/read-only views. They are never the editing source.

## Mandatory live status and automatic synchronization

Live project counts and the exact last automation timestamp are **not duplicated in this instruction anymore**. Operational status has three sources:

- canonical Google Drive `video-prompts.md` — editable content and human project status;
- GitHub `project-status.json` — generated counts, slow-scene list, health checks, and exact last successful Drive → GitHub synchronization time;
- the public viewer — displays `project-status.json` in its top status bar.

The prominent `REVISION / CURRENT STATUS` block remains in `video-prompts.md`, but instruction copies, Notion, and Library no longer need their live counts/timestamps manually rewritten after every prompt edit. This deliberately removes synchronization points.

**Normal path:** edit the single canonical Drive master → update `SYNC-TRIGGER.txt` → `sync-from-drive.yml` downloads the Drive master, runs `scripts/build_project_status.py`, validates invariants, updates GitHub `video-prompts.md` + `project-status.json` → GitHub Pages publishes the site.

If the health check fails, the workflow must fail instead of publishing a known-inconsistent master.
## Mandatory public-view and status-display rules

These rules are permanent project architecture and must survive future site edits, master synchronization, maintenance, or takeover:

1. **The human-facing “Montage review” link** on the public site must open the rendered GitHub Pages HTML page:  
   `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`  
   Do not use the Google Drive preview of that `.html` as the main clickable site link because Drive can display the HTML source code. The Drive file remains a project/deep-context copy, not the primary human-viewer URL.
2. The sidebar button **`Инструкция для ИИ`** must remain **on one line**. Do not allow the label to wrap; keep `white-space: nowrap` and use compact font/padding if needed.
3. Every visible slow-generation marker must use the exact same label: `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`.
   - In a TOC scene cell, show the scene title first and put `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` on the **next line**.
   - Do not put `⏳` before the scene title.
   - Do not put a dash before the status.
   - Do not wrap the status phrase internally; the web viewer should keep that label whole (`white-space: nowrap`).
   - The dedicated slow-generation table must use the same exact wording.
   - The full scene section must also show the same status wording on its own visible line; explanatory text such as “already running / do not relaunch” goes separately.
4. Slow-generation status remains a synchronization invariant: adding/removing it must update the top status block, dedicated slow-generation block, TOC row, and full scene section together.

Before suggesting or starting a generation, check the top status section in `video-prompts.md`. Any scene marked **⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ / DO NOT RELAUNCH** is already running and must not be submitted again unless the user explicitly says the previous run failed or authorizes a rerun.

## 2. Project-context files

For ordinary work on one prompt, read `video-prompts.md` first.

For decisions that depend on the film structure, characters, locations, map fragments, continuity, scene order, or whether a new scene is actually needed, also read:

- `film-analysis.md` — compact factual map of the current 58:48.789 cut and known limitations.
- `film-backlog.md` — active/possible changes, dependencies, transitions, cuts, and statuses.

Public review copies:

- https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-analysis.md
- https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-backlog.md

Deep reference, when needed: `Seregius_montazhny_razbor.html` is the long structural/editorial report created by Work (22 sections, ~14.5k words). It is useful for large structural questions but is overkill for routine prompt polishing.

Important limitation: Work did not perform a continuous real-time audiovisual watch of the full film. `film-analysis.md` explicitly marks what is factual, inferred, recommended, or requires manual playback verification.

## 3. Reference images are scene-local

`@image1`, `@image2`, etc. are local labels inside a specific prompt. Never assume that `@image1` means the same character in another scene.

When reviewing or rewriting a prompt that depends on appearance, the AI should receive the actual reference images used for that scene. The text master describes their role, but an AI cannot reliably judge facial/costume match without seeing the images.

For a scene-specific visual review, use:
1. the current scene block from `video-prompts.md`;
2. the exact reference images/videos named in that block;
3. `film-analysis.md` only if placement/continuity matters.

## 4. Editing roles

### Default editor: ChatGPT in the main project chat

When the user says things like:
- "добавь в мастер"
- "измени сцену 15"
- "удали готовый промт"
- "обнови мастер"

ChatGPT should:
1. read the newest Google Drive `video-prompts.md` first;
2. preserve all unrelated scenes;
3. apply only the approved change;
4. update the table of contents / scene-in-work section if needed;
5. keep the same canonical filename;
6. update `SYNC-TRIGGER.txt` so the automated Drive → GitHub validation/sync runs immediately; Library refresh is optional and reserved for explicit backups or major milestones;
7. ensure the web viewer continues to read the current public mirror.

If the user manually edited the Drive master, the user can say:

`Синхронизируй мастер с Google Drive.`

ChatGPT must fetch Drive first and treat the user's Drive edit as authoritative before updating mirrors.

### Work

Work is primarily the project-level analyst/editor, not the default writer for small prompt edits.

Before any film/project task, Work should read:
- latest `video-prompts.md` from Google Drive;
- `film-analysis.md`;
- `film-backlog.md`;
- relevant Notion pages when needed.

Use Work for:
- comparing many scenes at once;
- structural/continuity decisions;
- checking proposed scenes against the film map and backlog;
- updating film-analysis/backlog after major project decisions;
- broad audits.

For a small single-prompt rewrite or reference-image adjustment, normal ChatGPT is usually faster.

By default Work should propose changes to `video-prompts.md`, not create a second master. If Work is explicitly told to edit the Drive master, it must edit that same file in place and report exactly what changed. After a Work-side edit, the public GitHub mirror may need resynchronization by ChatGPT; the user can simply say: `Work обновил мастер — синхронизируй зеркала.` No file attachment is required.

### Claude / Gemini / DeepSeek / Grok / other AI tools

Default mode for every external AI is **REVIEW ONLY** unless the user explicitly appoints that AI as the current editor. All of them must read this guide and the current raw `video-prompts.md` before giving project-specific advice.

Project roles:
- **Claude — editorial/coherence reviewer.** Check long prompt structure, scene logic, clarity, consistency, pacing, and whether a rewrite preserves the user's intent. Return concrete edits, not a competing master. If the user explicitly appoints Claude as the temporary primary editor because ChatGPT is unavailable, Claude must switch to the takeover protocol in `CLAUDE-TAKEOVER-RUNBOOK.md` and may then edit the canonical Drive master within the user-authorized connected accounts.
- **Gemini — independent prompt + visual-reference reviewer.** Review the requested scene against the provided images/video references, prompt instructions, and film context when supplied. Do not build a website/app just because a project URL was provided; first read the linked guide/master and answer the user's actual review request.
- **DeepSeek — technical prompt auditor.** Look specifically for contradictions, impossible timing, camera/action conflicts, reference-priority mistakes, model-unfriendly overload, continuity gaps, negative-prompt problems, and opportunities to make constraints more explicit. Return a precise patch or replacement block.
- **Grok — creative/comedy/pacing reviewer.** Act as a second opinion on punchlines, deadpan timing, scene energy, dialogue rhythm, cinematic escalation, and alternative ideas while respecting established characters and continuity. Do not replace the canonical story with unrelated improvisation.
- **Other AI tools — general review role.** Read the same files, state what you are reviewing, and return suggestions tied to exact scene numbers/names.

All external AIs should:
1. open this guide;
2. read the public raw `video-prompts.md`;
3. optionally read `film-analysis.md` / `film-backlog.md` if the question needs story/continuity context;
4. inspect the actual reference images if the question is visual;
5. return suggestions tied to exact scene numbers/names;
6. not create a competing master file;
7. not change unrelated scenes;
8. never assume a project URL means “build a new site” — follow the user's explicit task first.

Suggested instruction to another AI:

> Read the project guide and the current prompt master from the linked files. Find the section that defines your role (Claude, Gemini, DeepSeek, Grok, or general reviewer) and follow it. Work in review-only mode. For the scene I ask about, identify the exact scene number/name, explain any issue, and return either a precise patch or a full replacement prompt. Do not rewrite unrelated scenes and do not create a new master file. If your recommendation depends on character appearance, tell me which reference images you need to see.

## 5. How much context to give another AI

### Quick prompt polish
Give:
- this guide link;
- `video-prompts.md` raw link;
- the scene's actual reference images.

### Continuity / story / placement question
Give:
- this guide;
- `video-prompts.md`;
- `film-analysis.md`;
- `film-backlog.md`;
- scene reference images if appearance matters.

### Deep film-structure review
Additionally provide/open:
- `Seregius_montazhny_razbor.html`;
- `EDIT_PLAN_V2.csv` if timing/cuts are relevant;
- manual notes or exact problem timecodes from real playback.

Do not dump every file into every AI chat by default. Use the smallest context set that answers the question.

## 6. Manual editing by the user

Manual editing is allowed, but edit only the canonical Google Drive `video-prompts.md`.

Recommended workflow: usually tell ChatGPT what to change instead of editing the Markdown manually. That keeps the table of contents, mirrors, and viewer synchronized automatically during the same task.

Never manually edit the HTML viewer as a source.

## 7. Conflict resolution

If sources disagree, use this priority unless the user explicitly overrides it:

1. current user decision;
2. factual evidence from the current film analysis;
3. current Google Drive `video-prompts.md`;
4. `film-backlog.md` recommendations/statuses;
5. old Notion scenario notes;
6. stale chat/file copies.

For the master file itself, the newest Google Drive `video-prompts.md` is authoritative.

## 8. Memory / old chats

Do not rely on an AI remembering this workflow from an old conversation. Read this guide and the current files again whenever there is uncertainty. The system is intentionally file-based so that losing chat history does not lose the project workflow.

## 9. Current public links

- Guide: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/AI-PROJECT-GUIDE.md
- Viewer: https://virudik.github.io/ai-film-prompts/
- Prompt master: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md
- Film map: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-analysis.md
- Backlog: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-backlog.md
- Montage review (rendered): https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html
- Repository: https://github.com/virudik/ai-film-prompts
- Claude takeover runbook: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/CLAUDE-TAKEOVER-RUNBOOK.md


## 10. Automated synchronization protocol

For normal prompt edits, a synchronization is complete when:
1. the newest Drive `video-prompts.md` was read and edited in place;
2. `SYNC-TRIGGER.txt` was updated to request immediate sync;
3. GitHub Actions completed successfully;
4. generated `project-status.json` reports `health: ok`;
5. GitHub Pages successfully deployed and the public viewer shows the new content/status.

`project-status.json` is generated and must never be hand-edited as a second source of truth.

ChatGPT Library, Drive `video-prompts.html`, and Notion are **backup/documentation layers, not per-edit synchronization gates**. Refresh them when the user explicitly asks for a backup, at major milestones, or whenever architecture/instructions change.

Technical runbook: `SYNC-RUNBOOK.md`.