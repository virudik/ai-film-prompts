# AI Video Prompts — synchronization rules

## Source of truth
The only canonical editable prompt master is `video-prompts.md`.

`video-prompts.html` is a generated read-only viewer derived from the canonical Markdown file. It must never be edited as a source.

## Canonical locations
1. ChatGPT Library: `/video-prompts.md` — canonical ChatGPT-side copy.
2. Google Drive folder `AI Film Prompts Master`: `video-prompts.md` — canonical shared-cloud copy for Work and other AI tools.
3. Google Drive: `video-prompts.html` — generated viewer for easy navigation/copying.
4. Notion page `AI Video Prompts — Master Hub` — index/instructions only; it links to the Drive files and must not contain an independently edited master copy.

## Editing protocol
Before changing prompts, ALWAYS read the newest canonical `video-prompts.md` from Google Drive or ChatGPT Library.

Never create `video-prompts-final.md`, `video-prompts-2.md`, `final-final`, or other parallel masters.

If a prompt is changed, replace the existing scene text in the canonical file. Do not create a duplicate version unless the scene intentionally has labeled A/B alternatives.

When a generated clip is accepted and no further revision is needed, remove that prompt from the active master and update the table of contents.

After every canonical Markdown update:
1. regenerate `video-prompts.html` from the updated Markdown;
2. replace the existing Drive `video-prompts.md` in place;
3. replace the existing Drive `video-prompts.html` in place;
4. update the ChatGPT Library `/video-prompts.md` and `/video-prompts.html` copies;
5. update the Notion Hub timestamp/status if needed.

## Other AI tools
Claude, Gemini, or another AI should normally READ the Drive `video-prompts.md` and return suggestions only.
They should not directly rewrite the canonical file unless explicitly told that they are the current editor.

When asking another AI for advice, tell it:
- read the current `video-prompts.md` first;
- do not assume old chat context is current;
- identify exact scene numbers/names being discussed;
- return proposed edits as a patch/replacement block or clear recommendations;
- do not create another master file;
- do not change unrelated prompts.

The user can then bring the suggested changes to ChatGPT, which applies approved edits to the canonical master and synchronizes the derived copies.

## Work mode
Work should use the same Google Drive `video-prompts.md` as the current master, together with `film-analysis.md` and `film-backlog.md` when project-level context is needed.
Work should not use an attached stale copy if the Drive master is available.

For prompt-only micro-edits, character-reference adjustments, or drafting one scene, ordinary ChatGPT is the default editor.
Use Work when a task benefits from cross-checking the film analysis, backlog, Notion, multiple files, or many scenes at once.

## Manual edits by the user
Manual editing is allowed, but only in the canonical `video-prompts.md` on Google Drive.
If the user edits it manually, tell ChatGPT afterward: `Синхронизируй мастер с Google Drive`.
ChatGPT should first fetch the newest Drive version, treat it as authoritative, update Library/HTML/Notion Hub, and preserve the user's manual changes.

Do not manually edit `video-prompts.html`; it will be regenerated and overwritten.
