# AI Video Prompts — synchronization rules

## Source of truth
The only canonical editable prompt master is `video-prompts.md`.

`video-prompts.html` is a generated read-only viewer derived from the canonical Markdown file. It must never be edited as a source.

## Canonical locations
1. ChatGPT Library: `/video-prompts.md` — canonical ChatGPT-side copy.
2. Google Drive folder `AI Film Prompts Master`: `video-prompts.md` — canonical shared-cloud copy for Work and other AI tools.
3. Google Drive: `video-prompts.html` — generated viewer for easy navigation/copying.
4. Notion page `AI Video Prompts — Master Hub` — index/instructions only; it links to the Drive files and must not contain an independently edited master copy.
5. GitHub root `video-prompts.md` — public read-only mirror used by the website and external AI tools.

## Editing protocol
Before changing prompts, ALWAYS read the newest canonical `video-prompts.md` from Google Drive or ChatGPT Library.

Never create `video-prompts-final.md`, `video-prompts-2.md`, `final-final`, or other parallel masters.

If a prompt is changed, replace the existing scene text in the canonical file. Do not create a duplicate version unless the scene intentionally has labeled A/B alternatives.

When a generated clip is accepted and no further revision is needed, remove that prompt from the active master and update the table of contents.

After every canonical Markdown update:
1. replace the existing Drive `video-prompts.md` in place;
2. regenerate/refresh `video-prompts.html` when maintaining the Drive viewer;
3. update the ChatGPT Library mirrors;
4. update GitHub root `video-prompts.md`;
5. wait for GitHub Pages deployment and verify the public viewer;
6. update Notion Hub status/navigation if needed.

## Other AI tools
Claude, Gemini, DeepSeek, Grok, or another AI should normally READ the current master and return suggestions only. They should not directly rewrite the canonical file unless explicitly told that they are the current editor.

When asking another AI for advice, tell it to read `AI-PROJECT-GUIDE.md`, use the role defined there, identify exact scene numbers/names, return a patch/replacement block or clear recommendations, avoid unrelated edits, and never create another master file.

## Work mode
Work should use the same Google Drive `video-prompts.md` as the current master, together with `film-analysis.md` and `film-backlog.md` when project-level context is needed. Work should not use an attached stale copy if the Drive master is available.

## Manual edits by the user
Manual editing is allowed, but only in the canonical `video-prompts.md` on Google Drive. If the user edits it manually, tell ChatGPT afterward: `Синхронизируй мастер с Google Drive`.

## Full-sync invariant
For the current project architecture, a full sync is complete only when the approved state has been propagated and verified in all relevant mirrors:
- local working files;
- Google Drive canonical master;
- ChatGPT Library mirror;
- GitHub root mirror;
- GitHub Pages viewer after successful deployment;
- Notion Hub status/navigation and instruction copies.

Read `SYNC-RUNBOOK.md` for the exact checklist. The GitHub Pages `index.html` dynamically fetches root `video-prompts.md`; the public site content therefore comes from the root Markdown mirror, not from a separately edited HTML scene copy.

Slow-generation scene status must be mirrored in three places inside `video-prompts.md`: top status block, TOC row, and scene section.

## Sanity check after every sync

Always verify scene consistency in two places:
1. the top summary table in `video-prompts.md`;
2. the full per-scene section list below.

New scenes must appear in both places. Slow-generation scenes must be reflected in the dedicated slow-generation block, in the summary table with the `⏳` marker, and in the scene section.
