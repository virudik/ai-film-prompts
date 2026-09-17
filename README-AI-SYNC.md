# AI Video Prompts — synchronization rules

## Source of truth
The only canonical editable prompt master is `video-prompts.md`.

`video-prompts.html` is a generated read-only viewer derived from the canonical Markdown file. It must never be edited as a source.


## Обязательный статус ревизии и времени синхронизации

В верхней части канонического `video-prompts.md` всегда должен быть **заметный статусный блок**, а не незаметная строка. Он обязан показывать актуальные значения:

- количество **сцен к генерации/доработке**;
- количество **полных текстов промтов**;
- количество сцен в раннем блоке **«Сцены в работе»**;
- количество и номера сцен **⏳ в медленной генерации**;
- точное время **последней полной синхронизации** с датой, часами, минутами и UTC-смещением.

Текущий контрольный снимок проекта: **18 сцен к генерации/доработке · 21 полный текст промтов · 🛠️ 3 в раннем блоке (W5, W7, W8) · ⏳ 5 в медленной генерации (2, 6, 8, 14, 15)**.

Текущее зафиксированное время полной синхронизации: **2026-09-17 · 17:01 (+03:00)**.

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

## Canonical locations
1. Google Drive folder `AI Film Prompts Master`: `video-prompts.md` — **the authoritative canonical editable master**.
2. ChatGPT Library: `/video-prompts.md` — internal mirror/reserve copy, never newer than Drive unless explicitly being staged before a confirmed Drive write.
3. GitHub root `video-prompts.md` — public read-only mirror used by the site and external AI.
4. Google Drive: `video-prompts.html` — generated viewer for easy navigation/copying.
5. Notion page `AI Video Prompts — Master Hub` — index/instructions only; it links to the Drive files and must not contain an independently edited master copy.

## Editing protocol
Before changing prompts, ALWAYS read the newest canonical `video-prompts.md` from Google Drive first. Use Library only as a fallback mirror if Drive is temporarily unavailable, and never silently overwrite newer Drive content from Library.

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


## Full-sync invariant
For the current project architecture, a full sync is complete only when the approved state has been propagated and verified in all relevant mirrors:
- local working files;
- Google Drive canonical master;
- ChatGPT Library mirror;
- GitHub root mirror;
- GitHub Pages viewer after successful deployment;
- Notion Hub status/navigation.

Read `SYNC-RUNBOOK.md` for the exact checklist. The GitHub Pages `index.html` dynamically fetches root `video-prompts.md`; the public site content therefore comes from the root Markdown mirror, not from a separately edited HTML scene copy.

Slow-generation scene status must be mirrored in three places inside `video-prompts.md`: top status block, TOC row, and scene section.


## Sanity check after every sync

Always verify scene consistency in two places:
1. the top summary table in `video-prompts.md`;
2. the full per-scene section list below.

New scenes must appear in both places. Slow-generation scenes must be reflected both in the dedicated slow-generation block and in the summary table with the `⏳` marker.


## Claude emergency takeover
If ChatGPT is unavailable and the user explicitly authorizes Claude to become the temporary editor, Claude must first read `CLAUDE-TAKEOVER-RUNBOOK.md`, then this file, `AI-PROJECT-GUIDE.md`, and the fresh Drive master. Claude may edit the existing canonical Drive file when the user's Claude account has the required connected-app permissions. Site content then follows the normal Drive → GitHub root → Pages path. Direct `index.html` changes require GitHub write access in Claude's own environment.
