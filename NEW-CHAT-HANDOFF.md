# NEW CHAT HANDOFF — AI Film Project
**Checkpoint: 20.09.2026**

Этот файл — **первый current-state entrypoint** для нового чата. Он должен оставаться коротким, актуальным и непротиворечивым. Не накапливать здесь старые competing snapshots; исторические инциденты — только как явно помеченная справка в runbook.

## 1. Перед вступлением в роль — обязательный полный reading gate

Новый чат **не считается принявшим проект и не начинает редактирование**, пока не прочитал все семь project/recovery instructions:

1. этот `NEW-CHAT-HANDOFF.md`;
2. `SYNC-RUNBOOK.md`;
3. `AI-PROJECT-GUIDE.md`;
4. `PROMPT-STYLE-GUIDE.md`;
5. `USER-GUIDE.md`;
6. `README-AI-SYNC.md`;
7. `BACKUP-AI-RUNBOOK.md`.

После этого обязательно:
8. fresh-read exact Google Drive `video-prompts.md`;
9. read live GitHub `project-status.json`;
10. read live `topview-status.json`;
11. read live `instruction-sync-status.json`;
12. при сюжетной/монтажной задаче — `film-analysis.md`, `film-backlog.md`, при необходимости `PROGRESS.md`, `Seregius_montazhny_razbor.html`, затем релевантные страницы Notion `Кино`.

Перед **каждой записью** в master — ещё один fresh-read exact Drive master.

Если инструкция/файлы уже дают однозначный ответ, **не задавать пользователю повторный уточняющий вопрос**. В частности, Scene ID вычисляется самостоятельно по stable-ID rules.

## 2. Capability preflight

Main editor должен уметь:
- read exact Drive master;
- write back to same Drive file ID;
- edit/mirror GitHub;
- trigger/verify sync workflow;
- update canonical instruction docs when проект меняется;
- verify status + Pages.

Если same-ID Drive write недоступен — текущий агент review-only.

## 3. Source-of-truth map

- Drive folder: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
- Editable prompt master: `video-prompts.md`
- Master ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- Handoff ID: `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- Prompt style guide ID: `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`
- GitHub repo: `virudik/ai-film-prompts`
- Control Center: `https://virudik.github.io/ai-film-prompts/`
- Notion operational pointer: `AI Film — Актуальная инструкция / Handoff`, ID `3e1fe763-7762-81d5-8c4e-dce504d7c5ec`

Roles:
- **Drive** = master + canonical instructions;
- **GitHub** = mirror + site + generated status;
- **Notion** = story/idea/history bank, not prompt master;
- **Library** = recovery mirror/cache, not authority;
- **Topview** = telemetry only;
- **Supabase** = comments only.

## 4. Current live checkpoint

На момент этого handoff:
- 16 active scenes;
- 19 prompt texts;
- work items: W5, W7, W8;
- active IDs: `1,2,3,4,5,10,11,12,13,14,15,16,17,18,19,20`;
- canonical slow: `2,12,14,15,18,19`;
- `latest_scene = 20`;
- deleted/retired IDs `6,7,9` не переиспользовать;
- Scene 20 `Маша-Лагуна: рок-припев у озера` = Seedance 2.5, 30s, READY, not slow;
- Scene 19 `Рыбалка и Маша-Лагуна` = Wan 3.0, active+slow;
- current master SHA и health **не считать постоянными**: читать live `project-status.json`.

Topview technical completion for scenes 14,15,18 does not equal approval; пока они остаются canonical slow, решение пользователя всё ещё требуется.

## 5. Prompt-writing rule — обязательно

Все новые и существенно перерабатываемые prompts пишутся по **полному** `PROMPT-STYLE-GUIDE.md`, не по краткому пересказу из чата.

Перед prompt:
1. fresh prompt guide;
2. fresh master;
3. 1–2 релевантные current master scenes;
4. затем master-level prompt.

Expected depth, где применимо: technical line, exact references roles, identity/reference priority, story/timeline, camera/continuity, performance, dialogue/vocals/lip sync, lighting/material realism, native audio, scene-specific negative prompt, `FRAME FILL / NO BARS`.

Новый Scene ID = следующий новый stable ID, если project state однозначен. Удалённые IDs не reuse. Пользователя номером не нагружать.

## 6. Routine master write

`fresh Drive master → minimal same-ID edit → SYNC-TRIGGER → sync-from-drive.yml → validation → exact Drive/GitHub compare → project-status → Pages → report`

Не говорить `ГОТОВО` до verification.

## 7. Control Center — что уже реализовано

- русский UI;
- active scene map + full prompts;
- merged `⏳ Сейчас в медленной генерации — Topview`;
- model/status/start/elapsed/queue/ETA;
- three-state sync lightsaber;
- character references;
- theme switch `☀ Светлая сторона` / `🌙 Тёмная сторона`, `localStorage = ai-film-theme`;
- раскрывающийся `Контрольный отпечаток`;
- **сразу под ним отдельная раскрывающаяся шторка `💬 Комментарии, идеи и предложения`**;
- отдельной кнопки `Архив GitHub` больше нет.

Native comments already live:
- Supabase org `Vint`;
- project `ai-film-comments`, ref `vzohfatqzyioydtgjiyd`;
- Edge Function `submit-comment`;
- public read + anonymous post + threaded replies;
- RLS;
- honeypot;
- rate limit 5 сообщений / 10 минут / IP;
- public frontend содержит только publishable key, **никогда service_role/admin secret**;
- comments backend не может менять master, Scene IDs, slow-lock, approval или generation tasks.

Site-only edit → GitHub `index.html` → JS syntax + duplicate IDs + Pages verification. Scene/prompt data не hard-code.

## 8. Documentation maintenance — новая обязательная обязанность редактора

Любое material нововведение должно быть зафиксировано **в том же рабочем цикле**, а не оставлено только в чате/коде.

После новой функции сайта, backend, workflow, prompt rule, new authority/source, status type или другого process change:
1. обновить все релевантные canonical Drive docs;
2. обновить этот SAME-ID `NEW-CHAT-HANDOFF.md`;
3. обновить `PROMPT-STYLE-GUIDE.md`, если изменились prompt rules;
4. exact-mirror docs Drive → GitHub;
5. refresh `instruction-sync-status.json`;
6. rebuild/check `project-status.json` + Pages;
7. refresh Notion operational pointer;
8. refresh Library recovery copies/state files.

Не накапливать contradictory append-only current snapshots. Переписывать current-state section до одного актуального состояния.

## 9. Seven-document instruction/recovery set

- `NEW-CHAT-HANDOFF.md` — `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- `AI-PROJECT-GUIDE.md` — `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `SYNC-RUNBOOK.md` — `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `USER-GUIDE.md` — `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` — `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `BACKUP-AI-RUNBOOK.md` — `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`
- `PROMPT-STYLE-GUIDE.md` — `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`

`AI Film Recovery Sync` должен exact-compare/mirror all seven Drive → GitHub and keep `instruction-sync-status.json` fresh. GitHub → Drive auto-write запрещён.

## 10. Notion and Library

Notion database `Кино` remains a story/idea/history source. Page `Важные промты` now marked as legacy prompt bank; current standard points to Drive `PROMPT-STYLE-GUIDE.md`.

Library recovery mirror should be refreshed after material changes with seven instruction docs plus:
- `READ-FIRST.txt`;
- `SHIFT-HANDOFF.md`;
- `SITE-STATUS.md`;
- `CURRENT-STATE.json`;
- handoff ZIP when maintained.

Library copies never override Drive.

## 11. Current story/work priorities

Главный сюжетный пробел: логика карты/трёх фрагментов/артефактов и payoff Warcraft 3.

Current work areas:
- W5 — Канцлер и Warcraft 3 / motivation;
- W7 — переходы между группами;
- W8 — транспорт/гонки;
- Scene 17 — последствия боя с монстром и разговор о карте.

Не mass-rewrite `NEEDS_FIX` / `NEEDS_RERENDER`; разбирать по одной сцене.

## 12. Known resilience rules

- concurrent writer race: current sync refetch/rebuild/retry;
- master UTF-8 without BOM;
- current backup filename only `BACKUP-AI-RUNBOOK.md`;
- historical counts/SHA/task estimates = evidence, not live invariant;
- old `Run failed` email does not prove current failure if a newer successful sync/status exists;
- Topview mapping проверять against fresh canonical scene body, not stale handoff text.

## 13. One-line takeover command

> Прими AI Film project только после полного reading gate из семи инструкций, fresh Drive master и live status JSON. Сохраняй Drive как единственный prompt master, пиши prompts только по full `PROMPT-STYLE-GUIDE.md`, сам определяй следующий stable Scene ID, синхронизируй same-ID edits через GitHub workflow, а любое material нововведение сразу фиксируй в relevant Drive docs + SAME handoff + GitHub + Notion pointer + Library recovery. Не задавай повторных вопросов, если ответ уже есть в канонических источниках.
