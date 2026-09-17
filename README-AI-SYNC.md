# AI Video Prompts — synchronization rules

## Source of truth
The only canonical editable prompt master is `video-prompts.md`.

`video-prompts.html` is a generated read-only viewer derived from the canonical Markdown file. It must never be edited as a source.


## Обязательный статус и автоматическая синхронизация

Живые числа проекта и точное время последней автоматической синхронизации **не дублируются в этой инструкции**. Источники оперативного статуса:

- канонический Google Drive `video-prompts.md` — содержимое, сцены и ручной статус проекта;
- GitHub `project-status.json` — автоматически рассчитанные counts, slow-scenes, health-check и точное время последней успешной синхронизации Drive → GitHub;
- публичный сайт — показывает `project-status.json` в верхней панели.

В самом `video-prompts.md` сохраняется заметный блок `РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС`, но инструкции, Notion и Library больше не должны вручную копировать его числа/время после каждой правки. Это специально уменьшает количество точек, которые могут рассинхронизироваться.

**Новый штатный путь:** изменить один канонический Drive-master → обновить `SYNC-TRIGGER.txt` → workflow `sync-from-drive.yml` сам скачивает master, запускает `scripts/build_project_status.py`, проверяет инварианты, обновляет GitHub `video-prompts.md` + `project-status.json` → GitHub Pages публикует сайт.

Если health-check не проходит, workflow должен завершиться ошибкой и **не публиковать заведомо неконсистентный master**.
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
1. replace the existing Drive `video-prompts.md` in place;
2. update GitHub `SYNC-TRIGGER.txt`;
3. let `sync-from-drive.yml` validate and mirror the Drive master;
4. let `scripts/build_project_status.py` generate `project-status.json`;
5. verify `health: ok` and a successful GitHub Pages deployment.

Routine edits do **not** require manual refresh of ChatGPT Library, Drive `video-prompts.html`, Notion, or every instruction copy. Those are backup/documentation layers and are refreshed only on explicit backup, major milestones, or architecture/instruction changes.
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


## Automated-sync invariant

A routine prompt sync is healthy only when:
- Drive remains the single editable canonical master;
- GitHub root `video-prompts.md` matches Drive after the workflow;
- `project-status.json` exists and reports `health: ok`;
- GitHub Pages deployment succeeds.

Library, Drive HTML and Notion are no longer blockers for every prompt edit.
## Sanity check after every sync

Always verify scene consistency in two places:
1. the top summary table in `video-prompts.md`;
2. the full per-scene section list below.

New scenes must appear in both places. Slow-generation scenes must be reflected both in the dedicated slow-generation block and in the summary table with the `⏳` marker.


## Claude emergency takeover
If ChatGPT is unavailable and the user explicitly authorizes Claude to become the temporary editor, Claude must first read `CLAUDE-TAKEOVER-RUNBOOK.md`, then this file, `AI-PROJECT-GUIDE.md`, and the fresh Drive master. Claude may edit the existing canonical Drive file when the user's Claude account has the required connected-app permissions. Site content then follows the normal Drive → GitHub root → Pages path. Direct `index.html` changes require GitHub write access in Claude's own environment.
