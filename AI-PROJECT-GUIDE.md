# AI Film Project — Start Here

This file explains how ChatGPT, Work, Claude, Gemini, DeepSeek, Grok, and other AI tools should use the shared prompt master and project context.




## Mandatory revision status and synchronization timestamp

The top of canonical `video-prompts.md` must contain a **prominent project-status block**, not only a small revision line. It must show current values for:

- number of **scenes awaiting generation/refinement**;
- number of **full prompt texts**;
- number of items in the early **Scenes in work** block;
- count and scene numbers currently **⏳ in slow generation**;
- exact **last full synchronization time**, including date, hour, minute, and UTC offset.

Current control snapshot: **18 scenes awaiting generation/refinement · 21 full prompt texts · 🛠️ 3 early work items (W5, W7, W8) · ⏳ 5 slow-generation scenes (2, 6, 8, 14, 15)**.

Current recorded full-sync time: **2026-09-17 · 15:35 (+03:00)**.

After every **full synchronization**, update both the `Last full synchronization` item and the `Synchronization` paragraph in the master to the actual completion time, for example `2026-09-17 · 15:35 (+03:00)`. Never leave only the date without time. If scene counts, prompt-text counts, work items, or slow-generation status change, update this snapshot consistently across mirrors and instruction copies.

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

Before suggesting or starting a generation, check the top status section in `video-prompts.md`. Any scene marked **⏳ МЕДЛЕННАЯ ГЕНЕРАЦИЯ / DO NOT RELAUNCH** is already running and must not be submitted again unless the user explicitly says the previous run failed or authorizes a rerun.

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
6. sync the updated master to the public GitHub mirror and the ChatGPT Library mirror;
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
- Repository: https://github.com/virudik/ai-film-prompts
- Claude takeover runbook: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/CLAUDE-TAKEOVER-RUNBOOK.md


## 10. Full synchronization protocol

For any request such as **"обнови мастер везде"**, **"полная синхронизация"**, **"синхронизируй мастер и сайт"**, or equivalent, ChatGPT must read and follow `SYNC-RUNBOOK.md`.

A master edit is not complete when only a local `/mnt/data` copy changes. A full sync means verifying the same approved state across:
1. local working Markdown / derived HTML;
2. canonical Google Drive `video-prompts.md`;
3. ChatGPT Library mirror;
4. GitHub root `video-prompts.md` and changed instruction files;
5. GitHub Pages deployment / public viewer;
6. Notion Hub status/navigation.

Before reporting success, verify that the public raw master or website contains the new change.

Slow-generation status is a three-place invariant: every scene currently running slowly must be marked in the top status block, the TOC row, and the scene section itself. Removing the status requires removing it from all three places.

Technical runbook:
- Google Drive / GitHub filename: `SYNC-RUNBOOK.md`
- Public raw: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/SYNC-RUNBOOK.md
