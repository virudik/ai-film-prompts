# AI Film Project — Start Here

This file explains how ChatGPT, Work, Claude, Gemini, and other AI tools should use the shared prompt master and project context.

## 1. Canonical source of truth

The only editable prompt master is:

- Google Drive → `AI Film Prompts Master/video-prompts.md`

Google Drive folder:
https://drive.google.com/drive/folders/1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6

The public GitHub copy is a read-only mirror for external AI review:

- Viewer: https://virudik.github.io/ai-film-prompts/
- Raw master: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md
- Repository: https://github.com/virudik/ai-film-prompts

Do not create parallel masters such as `video-prompts-final.md`, `video-prompts-2.md`, `final-final`, etc.

`video-prompts.html` and the GitHub Pages viewer are generated/read-only views. They are never the editing source.

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

### Claude / Gemini / other AI tools

Default mode is REVIEW ONLY.

They should:
1. open this guide;
2. read the public raw `video-prompts.md`;
3. optionally read `film-analysis.md` / `film-backlog.md` if the question needs story/continuity context;
4. inspect the actual reference images if the question is visual;
5. return suggestions tied to exact scene numbers/names;
6. not create a competing master file;
7. not change unrelated scenes.

Suggested instruction to another AI:

> Read the project guide and the current prompt master from the linked files. Work in review-only mode. For the scene I ask about, identify the exact scene number/name, explain any issue, and return either a precise patch or a full replacement prompt. Do not rewrite unrelated scenes and do not create a new master file. If your recommendation depends on character appearance, tell me which reference images you need to see.

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
