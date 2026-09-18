# Claude Takeover Runbook — AI Film v3.5


Claude is review-only by default.


Use this file only if user explicitly asks Claude to become temporary main editor.


## Preflight


Before any write, Claude must prove it can:
1. read exact Drive master ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`;
2. write back to SAME file ID;
3. read GitHub repo `virudik/ai-film-prompts`;
4. update `SYNC-TRIGGER.txt`;
5. verify workflow/status/Pages.


If same-ID Drive write is unavailable:
remain review-only and return exact patch instructions.


## Required reading


1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. fresh Drive `video-prompts.md`
5. `project-status.json`
6. if relevant `film-analysis.md` + `film-backlog.md`


## Safety


- stable Scene IDs
- no duplicate masters
- slow list is canonical
- no slow rerun without result/error/user decision
- Topview success != approval
- Scene 6 was last observed technically complete in Topview but must not be auto-cleared from canonical slow state
- `project-status.json` is generated
- instruction drift is not auto-fixed


## Write procedure


fresh-read
→ minimal edit
→ same Drive file ID
→ sync trigger
→ workflow
→ validation
→ status
→ Pages
→ report exact change


## Site-only edits


UI/HTML changes may be made in GitHub `index.html` when explicitly requested.
Do not move scene content into HTML.


Current UI:
- Russian labels
- service and technical drawers
- clickable metric navigation
- Topview status translations
- green/red animated sync lightsaber
- slow/Topview UI is already merged into one visible canonical+telemetry table
- time estimate intentionally unchanged


## References


User-approved model sheets are authoritative.
Never substitute images based on visual similarity.
Verified 19.09.2026: public `references/full/*.jpg` paths exist for all 8 confirmed model sheets and the lightbox uses them.




## Environment-specific warning


A Claude web/chat session that can only read Drive and public GitHub remains review-only even if the Claude model itself is capable of coding. Takeover authority belongs to the environment, not the model name. Claude Code or another Claude environment may become a main editor only after the preflight proves same-ID Drive write plus GitHub write/verification with the actual connected credentials/tools.

## Verified sync recovery

As of 19.09.2026, the earlier race/BOM failures are resolved and confirmed by multiple successful sync runs. Before takeover, still fresh-check live status, but do not treat older failure emails as evidence of a current outage when a newer successful status exists.
