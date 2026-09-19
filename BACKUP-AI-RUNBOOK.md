# Инструкция для резервного ИИ — AI Film v3.5


Резервный ИИ работает review-only по умолчанию.


Использовать этот файл только если пользователь явно назначает конкретный резервный ИИ временным основным редактором. Техническое имя файла: `BACKUP-AI-RUNBOOK.md`.


## Preflight


Перед любой записью резервный ИИ должен доказать, что его конкретное окружение умеет:
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
- Current canonical state must be read fresh: scene 2 has been explicitly returned to canonical slow by the user; scenes 6, 7 and 9 remain removed from active master as obsolete; new Scene 19 «Рыбалка и Маша-Лагуна» is active+slow. Current slow = 2,12,14,15,18,19. Do not infer slow changes from historical Topview telemetry.
- `project-status.json` is generated
- canonical instruction semantics are not auto-rewritten; hourly `AI Film Recovery Sync` may repair only GitHub instruction mirrors from canonical Drive → GitHub and performs semantic-conflict detection


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
- three-state animated sync lightsaber: green stable, yellow recovered-error observation, red unresolved/stale error
- slow/Topview UI is already merged into one visible canonical+telemetry table
- time estimate intentionally unchanged
- Topview status labels such as `В очереди` must stay on one line; model names and `ждёт решения` also stay unbroken


## References


User-approved model sheets are authoritative.
Never substitute images based on visual similarity.
Verified 19.09.2026: public `references/full/*.jpg` paths exist for all 8 confirmed model sheets and the lightbox uses them.




## Environment-specific warning


Любой web/chat-сеанс, который умеет только читать Drive и публичный GitHub, остаётся review-only независимо от названия модели. Takeover authority определяется возможностями конкретного окружения, а не брендом ИИ. Claude Code, Gemini CLI, Grok/DeepSeek в coding-agent окружении или другой резервный агент может стать main editor только после preflight, доказавшего same-ID Drive write плюс GitHub write/verification с реально подключёнными credentials/tools.

## Verified sync recovery

As of 19.09.2026, the earlier race/BOM failures are resolved and confirmed by multiple successful sync runs. Before takeover, still fresh-check live status, but do not treat older failure emails as evidence of a current outage when a newer successful status exists.


## Current automation note — 19.09.2026

`AI Film Recovery Sync` now runs hourly. It can repair GitHub mirrors of the five canonical instruction files from Drive, but never Drive from GitHub. It also checks known semantic contradictions. This does not expand takeover authority: an external AI still needs the preflight for same-ID Drive write and GitHub write if it is to become main editor.
