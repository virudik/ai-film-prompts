# NEW CHAT HANDOFF — AI Film Project
**Checkpoint: 20.09.2026**

Этот файл — текущая точка передачи следующему чату. Он намеренно очищен от накопившихся исторических противоречий. Исторические коммиты/старые snapshot-и не являются текущей властью.

## 1. Что читать первым

1. Этот `NEW-CHAT-HANDOFF.md`.
2. `SYNC-RUNBOOK.md`.
3. `AI-PROJECT-GUIDE.md`.
4. Fresh-read Google Drive `video-prompts.md`, file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
5. Live GitHub `project-status.json`.
6. Live `topview-status.json`.
7. Live `instruction-sync-status.json`.
8. Для сюжета/монтажа: `film-analysis.md`, `film-backlog.md`, при необходимости `PROGRESS.md` и `Seregius_montazhny_razbor.html`.
9. Перед любой записью в master — ещё один fresh-read exact Drive master.

## 2. Источник истины и архитектура

- Drive folder: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
- Единственный editable prompt master: `video-prompts.md`
- Drive master ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- GitHub repo: `virudik/ai-film-prompts`
- Control Center: `https://virudik.github.io/ai-film-prompts/`
- Handoff Drive ID: `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- GitHub — зеркало + Pages, не второй prompt master.
- `project-status.json` генерируется автоматически и вручную не редактируется.
- Scene IDs стабильны. Удалённые IDs 6, 7, 9 не переиспользовать.
- Не создавать `video-prompts-v2`, `final`, `copy`, `final-final` и т. п.

## 3. Текущий live fingerprint

Проверено 20.09.2026 перед передачей:
- 15 active scenes
- 18 prompt texts
- W5, W7, W8
- active Scene IDs: `1,2,3,4,5,10,11,12,13,14,15,16,17,18,19`
- canonical slow: `2,12,14,15,18,19`
- current master SHA-256: `3dab6fa527063fa8e6174c620c76e17fe9d3ade07aab504ef8cbeb45952543bf`
- `project-status.json.health = ok`
- `instruction_sync = ok`
- warnings: none
- Drive master == GitHub mirror: verified

Эти значения — checkpoint. На следующем чате всё равно fresh-check live JSON.

## 4. Current scene decisions

- Scene 2 `Джедаи на крыше — триумфальный марш без мечей` снова находится в canonical slow по прямому решению пользователя. Это новый rerun, а не историческая completed task.
- Scene 19 `Рыбалка и Маша-Лагуна` — active + slow, Wan 3.0, 30s, русский диалог.
- Scenes 6, 7, 9 удалены как неактуальные и не должны автоматически возвращаться.
- Scene 17 остаётся active как пост-монстр продолжение; machine dependency на удалённую Scene 9 снята.
- Topview `success` = техническое завершение, не user approval.
- Нельзя автоматически перезапускать slow scene или снимать slow-lock по одной telemetry.

## 5. Scene 19 — Рыбалка и Маша-Лагуна

Утверждённый сюжет:
- стартовый кадр: Саша и Паша рыбачат у озера;
- вода начинает рябить;
- Маша в форме Лава-Лагуны выходит из воды;
- подходит к Саше лицом к лицу;
- Саша: `«Маша?..»`;
- сразу пощёчина;
- Маша эмоционально: `«Опять ты пропадаешь на рыбалке! Когда наконец сможешь уделять внимание мне, а не своим увлечениям?»`;
- Паша молчит, но ярко реагирует мимикой;
- Саша: `«Ой, у нас же важное поручение!»`;
- Саша и Паша срываются с места;
- финал приходит к референсу бегущих ног/бега.

Референсы в scene prompt:
- Image1 — старт рыбалки;
- Image2 — финальный бег;
- Image3/Image4 — Sasha/Pasha model sheets в фактической Topview task;
- Image5 — Masha-Laguna.

## 6. Topview — текущая проверенная привязка

На 20.09.2026 `topview-status.json` содержит все шесть canonical slow scenes и verified high-confidence mappings.

Exact current tasks:
- Scene 2 → `d28b2481a8b344439fa175c3ef0b7f5b` — Seedance 2.5, init
- Scene 12 → `8d2103753bb145b7990014bf83a6f652` — Wan 3.0, init
- Scene 14 → `1fd5e89e6cd64b41af6a007a88d0939f` — Seedance 2.5, init
- Scene 15 → `86d84863bf5e4b97b2ea9423ca514f84` — Wan 3.0, init
- Scene 18 → `cd7c476566d84076aaa330274093ea15` — Wan 3.0, init
- Scene 19 → `6ef310d646ca4605b5b10c12752b6ab7` — Wan 3.0, init

ВАЖНО: ранее automation ошибочно назвала Scene 19 task mismatch. Это был false positive. Повторная проверка полного prompt task показала точное соответствие сцене 19: рыбалка Саши/Паши → выход Маши из воды → `Маша?..` → пощёчина → русские реплики → бег. Текущий mapping Scene 19 валиден.

`Topview Slow Watch` должен сначала читать fresh Drive master и current `project-status.json`, затем сопоставлять exact task по полному содержанию сцены. Не сравнивать новую task со старым/кэшированным описанием Scene ID.

## 7. Почему в последние дни было много красных/жёлтых состояний

Добавление/удаление сцен само по себе не является проблемой и система должна это выдерживать. Ошибки возникали из четырёх отдельных классов:
1. concurrent GitHub writers → non-fast-forward race;
2. UTF-8 BOM → strict header validation fail;
3. старое имя backup-runbook осталось в validator после rename;
4. дублирование current-state фактов в нескольких инструкциях/handoff + stale Topview mapping logic → semantic false positives.

Первые три технически исправлены. Четвёртый класс теперь должен предотвращаться правилами:
- dynamic current facts (`counts`, `slow IDs`, current SHA, current Topview tasks) считаются live-authority только из fresh master + `project-status.json` + `topview-status.json`;
- инструкции описывают правила, а не пытаются быть второй базой статуса;
- checkpoint/historical sections не сравнивать как current invariant;
- handoff содержит один явный current-state блок, исторические противоречивые слои удалены;
- Topview task mapping проверять против current scene prompt, не против памяти/старого snapshot.

На момент передачи система снова green/healthy.

## 8. Control Center — что уже реализовано

- русский UI;
- объединённая slow/Topview таблица;
- model/status/start/elapsed/queue/ETA;
- трёхсостоянийный sync lightsaber;
- active scene map + full prompts;
- characters/references;
- comments reader через GitHub Issue #8;
- `FRAME FILL / NO BARS` во всех 18 текущих prompt blocks;
- theme switch в верхней строке между `РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС` и health lightsaber:
  - `☀ Светлая сторона`
  - `🌙 Тёмная сторона`
  - выбор сохраняется в `localStorage` (`ai-film-theme`).

Тема — presentation-only. Она не должна влиять на master/status/sync health.

## 9. НОВЫЙ план сайта: комментарии прямо на сайте без GitHub

Пользователь явно хочет, чтобы посетитель мог **читать, писать и отвечать прямо на Control Center без GitHub-аккаунта**.

Текущий GitHub Issue #8 reader остаётся существующей реализацией до миграции, но это уже не целевой UX.

Рекомендуемая архитектура следующего шага:
- отдельный lightweight backend для comments; предпочтительный кандидат — Supabase;
- публичное чтение опубликованных комментариев;
- anonymous posting с отображаемым именем (без обязательного аккаунта);
- threaded replies (`parent_id`);
- timestamps;
- HTML escaping/sanitization;
- rate limit / anti-spam / CAPTCHA или honeypot;
- moderation status (`pending`/`published`/`hidden`) при необходимости;
- НИКОГДА не давать comment backend право менять Drive master, Scene IDs, slow-lock или approval;
- service-role/admin key никогда не класть в клиентский `index.html`; только public anon key + RLS policies либо server-side endpoint.

Перед реализацией новый чат должен проверить доступный Supabase project/credentials и согласовать минимальную схему. Не удалять GitHub Issue #8 до успешной миграции; можно оставить как архив/резерв.

## 10. Другие pending UI / infrastructure планы

- `Сейчас` view — будущий дополнительный режим, не реализован. Не внедрять без отдельного явного запроса.
- personal domain `рудик.рф/промты` — не реализован; нужен реальный hosting/router access.
- independent video playback без YouTube — будущая задача.
- local deterministic `sync-master.ps1/.py` — будущий resilience helper, не реализован.
- generated `workflow-status.json` — optional future hardening, пока не обязателен.

## 11. Film/story priorities

Главный сюжетный пробел: логика карты/трёх фрагментов/артефактов и payoff Warcraft 3.

Актуальные направления:
- W5 — Канцлер и Warcraft 3 / мотивация;
- W7 — переходы между группами;
- W8 — транспорт/гонки;
- Scene 17 — последствия боя с монстром и разговор о карте;
- Sasha ideas — теперь источник конкретных монтажных/сюжетных предложений; Scene 19 уже выросла из одной такой идеи.

Не массово переписывать NEEDS_FIX/NEEDS_RERENDER. Разбирать по одной сцене.

## 12. Global prompt rules

- единый стиль/цветокоррекция/свет/окружение/дизайн персонажей;
- physically stable cinematic camera motion; no random jitter;
- coherent 3D space; no sudden geometry;
- русская речь без акцента, если не оговорено иначе;
- exact approved character model sheets важнее similarity;
- global `FRAME FILL / NO BARS` во всех текущих и будущих prompts, если пользователь явно не отменит.

## 13. Routine write procedure

Для scene/prompt change:
1. fresh-read exact Drive master;
2. минимально изменить нужный Scene ID/TOC/count/slow markers;
3. сохранить SAME Drive file ID;
4. update GitHub `SYNC-TRIGGER.txt`;
5. дождаться `sync-from-drive.yml`;
6. verify validation;
7. verify GitHub `video-prompts.md` == Drive;
8. verify `project-status.json`;
9. verify Pages;
10. только потом говорить `ГОТОВО`.

Для site-only UI:
- меняется GitHub `index.html`;
- после правки: JS syntax check + duplicate IDs + Pages verification;
- scene/prompt content не hard-code в HTML.

## 14. Canonical instruction files

Drive authority:
- `AI-PROJECT-GUIDE.md` — `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `SYNC-RUNBOOK.md` — `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `USER-GUIDE.md` — `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` — `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `BACKUP-AI-RUNBOOK.md` — `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`

Hourly `AI Film Recovery Sync` may repair only Drive → GitHub instruction mirrors. Never GitHub → Drive automatically.

## 15. Ready-to-paste command for the next chat

> Продолжаем AI Film project. Сначала fresh-read Google Drive `NEW-CHAT-HANDOFF.md` (same ID `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`), `SYNC-RUNBOOK.md`, `AI-PROJECT-GUIDE.md`, затем exact Drive `video-prompts.md` file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`. После этого проверь live GitHub `project-status.json`, `topview-status.json`, `instruction-sync-status.json` и повтори current fingerprint. Не используй старые Library/GitHub copies как editable master. Не переиспользуй Scene IDs 6/7/9. Current checkpoint: 15 active scenes, 18 prompts, W5/W7/W8, canonical slow 2,12,14,15,18,19; Scene 19 «Рыбалка и Маша-Лагуна» = Wan 3.0 30s Russian dialogue; exact Topview task `6ef310d646ca4605b5b10c12752b6ab7`; Scene 2 current rerun task `d28b2481a8b344439fa175c3ef0b7f5b`. Theme switch `Светлая сторона / Тёмная сторона` уже реализован в header. Следующий сайт-приоритет по последнему решению пользователя — комментарии прямо на сайте без GitHub-аккаунта: спроектировать/подключить безопасный backend (предпочтительно Supabase), anonymous posting + replies + anti-spam, без доступа к prompt master. Также перепроверь стабильность sync/Topview mapping; не считать historical checkpoint current invariant и не выдавать false red из-за старых секций. Перед `ГОТОВО` проверить Drive→GitHub sync, validation, Topview telemetry и Pages.
