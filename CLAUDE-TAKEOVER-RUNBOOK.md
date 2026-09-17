# AI Film Prompts — Claude Takeover Runbook

Эта инструкция нужна Claude как аварийному/резервному редактору проекта на случай, если ChatGPT временно недоступен. Она рассчитана на работу без памяти старых чатов: сначала прочитать этот файл, затем свежий `AI-PROJECT-GUIDE.md`, затем канонический `video-prompts.md` на Google Drive.

## 1. Роль Claude при подмене ChatGPT

По умолчанию Claude в проекте работает review-only. Но если пользователь прямо говорит, что ChatGPT недоступен и Claude временно назначен основным редактором, Claude может взять на себя обслуживание мастера и проекта по правилам этого файла.

При подмене ChatGPT Claude должен вести себя как один текущий редактор канона: не создавать параллельные master-файлы, не плодить `v2`, `final`, `copy`, `final-final`, не переписывать несвязанные сцены и не считать память чата источником истины.

После возвращения ChatGPT Claude должен сообщить пользователю, что именно изменил в каноническом Drive-мастере и какие зеркала/хабы были обновлены или не были обновлены.

## 2. Единственный источник истины

**Google Drive → `AI Film Prompts Master/video-prompts.md` — единственный канонический редактируемый мастер промтов.**

## Обязательный статус ревизии и времени синхронизации

В верхней части канонического `video-prompts.md` всегда должен быть **заметный статусный блок**, а не незаметная строка. Он обязан показывать актуальные значения:

- количество **сцен к генерации/доработке**;
- количество **полных текстов промтов**;
- количество сцен в раннем блоке **«Сцены в работе»**;
- количество и номера сцен **⏳ в медленной генерации**;
- точное время **последней полной синхронизации** с датой, часами, минутами и UTC-смещением.

Текущий контрольный снимок проекта: **18 сцен к генерации/доработке · 21 полный текст промтов · 🛠️ 3 в раннем блоке (W5, W7, W8) · ⏳ 5 в медленной генерации (2, 6, 8, 14, 15)**.

Текущее зафиксированное время полной синхронизации: **2026-09-17 · 16:52 (+03:00)**.

При каждой **полной синхронизации** строка/пункт `Последняя полная синхронизация` и абзац `Синхронизация` в master-файле должны быть обновлены на фактическое время завершения синхронизации, в формате `YYYY-MM-DD · HH:MM (UTC offset)`, например `2026-09-17 · 16:38 (+03:00)`. Нельзя оставлять только дату без времени. Если меняются число сцен, prompt-текстов, work-items или slow-generation status, обновить этот статус одновременно во всех зеркалах и инструкциях.

## Обязательные правила отображения сайта и статусов

Эти правила считаются частью постоянной архитектуры проекта и должны сохраняться при любых будущих правках сайта, мастера, синхронизации или takeover:

1. **Монтажный разбор фильма для просмотра человеком** на публичном сайте должен открываться как отрендеренная HTML-страница GitHub Pages:  
   `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`  
   Не использовать Google Drive preview этого `.html` как основную кликабельную ссылку на сайте: Drive может показывать исходный HTML-код. Drive-файл остаётся проектной копией/контекстом для ИИ, но не основным human-viewer URL.
2. Кнопка **`Инструкция для ИИ`** в боковой панели сайта должна всегда помещаться **в одну строку**. Не разрешать перенос слов/строк; для неё сохранять `white-space: nowrap` и при необходимости компактный размер шрифта/отступов.
3. Для сцен в медленной генерации использовать **одинаковую видимую надпись везде**: `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`.
   - В строке сцены в оглавлении сначала показывается название сцены, **на следующей строке** — `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`.
   - Не ставить `⏳` перед названием сцены.
   - Не ставить тире перед статусом.
   - Саму фразу `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` не переносить внутри себя; в веб-viewer она должна помещаться целиком (`white-space: nowrap`).
   - В отдельной таблице slow-generation использовать ту же точную формулировку.
   - В полном разделе сцены статус также должен визуально стоять отдельной строкой той же формулировкой; пояснение `уже запущено / не запускать повторно` давать отдельным текстом, а не частью другой версии статуса.
4. Статус медленной генерации по-прежнему является инвариантом: при добавлении/снятии его нужно синхронно обновлять в верхнем статусном блоке, отдельном slow-generation блоке, строке оглавления и полном разделе сцены.

Постоянные точки:

- Google Drive folder `AI Film Prompts Master`
  - folder ID: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
  - folder URL: https://drive.google.com/drive/folders/1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6
- Canonical Drive master `video-prompts.md`
  - file ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
  - URL: https://drive.google.com/file/d/1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj/view?usp=drivesdk
- Drive viewer `video-prompts.html`
  - file ID: `1AZK6XafZng4M_I7ciqdhEjfgfkf3CA01`
- `AI-PROJECT-GUIDE.md`
  - file ID: `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `USER-GUIDE.md`
  - file ID: `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md`
  - file ID: `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `SYNC-RUNBOOK.md`
  - file ID: `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `CLAUDE-TAKEOVER-RUNBOOK.md`
  - file ID: `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`
- `film-analysis.md`
  - file ID: `1O3bsGGivBktRSbeg-9JWeMLK4J_JYu0M`
- `film-backlog.md`
  - file ID: `1YixC7zQFY7z3Bn1XGXxeQIMema3inCT9`
- Notion Hub page ID: `3ddfe763-7762-81c0-b8fd-e7c61895df4a`
- GitHub repo: `virudik/ai-film-prompts`
- Public viewer: https://virudik.github.io/ai-film-prompts/
- Public raw master: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md
- Public general guide: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/AI-PROJECT-GUIDE.md
- ChatGPT full sync runbook: https://raw.githubusercontent.com/virudik/ai-film-prompts/main/SYNC-RUNBOOK.md

If sources disagree, use this priority:
1. current explicit user decision;
2. freshest canonical Google Drive `video-prompts.md` for prompt-master state;
3. factual evidence in current film analysis;
4. `film-backlog.md` recommendations/statuses;
5. old Notion scenario notes;
6. old chat memory or stale copies.

## 3. Что читать и как часто

Claude must not rely on remembered instructions when doing writes.

Before every actual edit of the canonical master:
1. re-read the fresh Google Drive `video-prompts.md`;
2. inspect the exact scene(s) being changed;
3. check the top slow-generation/status block;
4. read `film-analysis.md` / `film-backlog.md` if the edit depends on story, placement, continuity, character assignment, scene order, map fragments, or whether the scene is needed at all.

Before full synchronization, site maintenance, workflow repair, Notion maintenance, or recovery after a long gap:
1. re-read this `CLAUDE-TAKEOVER-RUNBOOK.md`;
2. re-read `SYNC-RUNBOOK.md`;
3. re-read `AI-PROJECT-GUIDE.md`;
4. fetch the newest Drive master.

For casual brainstorming/review-only discussion, there is no need to reload the whole runbook on every message. The mandatory fresh read happens before writes and whenever project state is uncertain.

## 4. Как обслуживать мастер

When adding a new active scene:
1. read fresh Drive master first;
2. choose the next free scene number;
3. add one row to the top contents table;
4. add one full section with anchor `<a id="scene-N"></a>` and `## Сцена N — ...`;
5. update the revision line counts;
6. remove the matching W-item from `Сцены в работе` if it became a full scene;
7. preserve unrelated scenes exactly;
8. check for stale duplicates;
9. keep intentional A/B alternatives inside one numbered scene where practical.

When editing an existing scene:
- replace only the target section/phrasing;
- do not duplicate it elsewhere;
- preserve exact reference-label meanings local to that scene;
- if appearance matters, ask for/inspect the real image/video references because `@image1` text labels alone do not show appearance.

When a generated clip is accepted and the prompt is no longer needed:
- remove that scene from the active master and top contents table;
- update counts and references;
- do not keep a separate archive copy unless the user explicitly asks for one.

## 5. Slow-generation protection

A scene marked `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` must not be submitted again unless the user explicitly says the previous run failed, completed, or authorizes a new run.

The slow-generation state must agree in all required places:
1. top global status block;
2. dedicated slow-generation block/table;
3. the scene row in the contents table;
4. the scene's own section.

When status is removed, remove it from all these places in one edit.

## 6. Project context

For ordinary prompt editing, the current `video-prompts.md` is primary.

Use `film-analysis.md` for factual map/current cut context. Use `film-backlog.md` for unresolved tasks, dependencies and recommendations. For deep structural decisions, use `Seregius_montazhny_razbor.html`, `EDIT_PLAN_V2.csv`, and `PROGRESS.md` when needed.

Do not claim the full film was continuously watched/listened to in real time. The large Work analysis is structural and evidence-based; manual audiovisual playback remains the final authority for tiny timing, sound and continuity questions.

## 7. Google Drive write protocol

If Claude has the user's Google Drive connector/access:
- edit the existing `video-prompts.md` in place, preserving its same file ID;
- never upload a replacement named `video-prompts-final.md` or `video-prompts-2.md`;
- if the user manually edited Drive, treat that fresh Drive version as authoritative and merge nothing from stale copies over it;
- if instructions themselves are updated, update the existing instruction files in place where possible.

If Claude cannot write Google Drive:
- do not pretend the canonical master was updated;
- produce an exact patch/full replacement section for the user;
- use the public GitHub copy only for reading;
- ask the user to reconnect Drive or return the patch to an editor with Drive write access.

## 8. GitHub and site architecture

Repo: `virudik/ai-film-prompts`.

The site at https://virudik.github.io/ai-film-prompts/ is a read-only viewer. Root `index.html` dynamically fetches root `video-prompts.md`; scene content should therefore be changed in the master, not hard-coded into the HTML.

Preferred master flow:
`Google Drive video-prompts.md` → GitHub root `video-prompts.md` → GitHub Pages viewer.

There is a workflow `.github/workflows/sync-from-drive.yml` used as a safety sync for the canonical master. It is expected to pull the Drive master and update GitHub. `SYNC-TRIGGER.txt` can trigger a sync, and there is also a schedule.

The old `_source/part-*.md` + `build-master.yml` mechanism is obsolete and must not be treated as a source of truth or manually run to rebuild the master. If it still exists, it should remain disabled.

If Claude has GitHub write access:
- it may update root `video-prompts.md` only after Drive has been updated/verified;
- it may update `index.html` only for site/UI changes, not for scene text;
- after a site/master commit, verify GitHub Pages deployment success before claiming the site is updated.

If Claude does not have GitHub write access:
- updating Drive master is still useful because the Drive→GitHub workflow is designed to sync the root master automatically;
- do not claim a structural site/UI change was made if `index.html` could not be edited;
- record any needed site-structure change for later in Notion or report it to the user.

Permanent site rules Claude must preserve:
- Montage review button/link → `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`, not Drive preview.
- `Инструкция для ИИ` button stays on one line.
- Slow-generation visible label is exactly `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`, on its own next line in TOC cells, with no leading dash and no internal wrapping.

## 9. End-to-end sync checklist

When the user says `синхронизируй всё`, `обнови мастер везде`, or equivalent, Claude should execute this checklist if it is the active editor:

1. Fresh-read canonical Drive `video-prompts.md`.
2. Apply only approved edits.
3. Integrity-check counts, contents table, anchors, W-block, duplicates and slow-generation state.
4. Save back to the same Drive master file ID.
5. Update Drive `video-prompts.html` only as a derived viewer if Claude has the same workflow/tooling; never treat it as source.
6. Update GitHub root mirror directly if GitHub write access exists; otherwise rely on/trigger the Drive→GitHub workflow and verify after it runs.
7. Update instruction mirrors if rules changed.
8. Update Notion Hub and instruction copies if available.
9. Verify public GitHub raw and Pages viewer after deployment.
10. Report clearly what succeeded and what could not be updated due to permissions/tool availability.

Never report `готово / fully synchronized` before external verification.

## 10. Notion

Notion page `AI Video Prompts — Master Hub` is a navigation/status hub, not a separate prompt master.

If Claude has Notion edit access:
- update Hub status/timestamp when full synchronization changes them;
- keep copies of all five instruction documents current:
  - `SYNC-RUNBOOK.md`
  - `USER-GUIDE.md`
  - `AI-PROJECT-GUIDE.md`
  - `README-AI-SYNC.md`
  - `CLAUDE-TAKEOVER-RUNBOOK.md`
- never create an independent editable copy of `video-prompts.md` in Notion.

## 11. Taking over after memory loss

If Claude starts with no previous-chat memory:
1. read this takeover runbook;
2. read `SYNC-RUNBOOK.md`;
3. read `AI-PROJECT-GUIDE.md`;
4. read fresh Drive `video-prompts.md`;
5. read `film-analysis.md` / `film-backlog.md` if needed;
6. inspect GitHub/Pages/Notion when synchronization state matters;
7. perform the requested change using the write/sync protocol above.

The project is intentionally file-based so that losing model memory or old chats does not destroy the workflow.
