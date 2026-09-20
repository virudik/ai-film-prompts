# AI Film Project — Start Here v3.5


Короткая стартовая инструкция для нового ChatGPT/Work/Claude/Gemini/DeepSeek/Grok.


## Источник истины


- Единственный редактируемый prompt master: Google Drive `AI Film Prompts Master/video-prompts.md`
- Drive master ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- Drive folder ID: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
- GitHub `virudik/ai-film-prompts` — публичное read-only зеркало и GitHub Pages, не второй master.
- `project-status.json` — генерируемый machine-status schema v3, вручную не редактировать.
- Scene IDs стабильны и не перенумеровываются после удаления.


## Что читать новому чату


1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. этот файл
4. `PROMPT-STYLE-GUIDE.md` — полный обязательный стандарт prompt-writing, Drive ID `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`
5. fresh Drive `video-prompts.md`
6. live GitHub `project-status.json`
7. live `topview-status.json`
8. live `instruction-sync-status.json`
8. при story/continuity — `film-analysis.md` + `film-backlog.md`


Перед любой записью в master — ещё один fresh-read.


## Текущий handoff snapshot


На момент передачи:
- 16 active scenes
- 19 prompt texts
- W5, W7, W8
- canonical slow list: 2, 12, 14, 15, 18, 19
- Scene 2: по новому прямому решению пользователя возвращена в canonical slow-list; prompt остаётся active.
- Scenes 6, 7 and 9: удалены из active master как больше не актуальные.
- Scenes 2, 12, 14, 15, 18 and 19 are the current canonical slow set; Scene 19 «Рыбалка и Маша-Лагуна» — активный 30s prompt для Wan 3.0.
- Scene 20 «Маша-Лагуна: рок-припев у озера» — active READY, Seedance 2.5, 30s, not slow; @Image1 location, @Image2 Masha identity.


Topview success != user approval. Slow scene нельзя перезапускать или снимать с slow автоматически без результата/ошибки/решения пользователя.


## Routine sync


`fresh Drive master → edit same Drive file ID → update SYNC-TRIGGER.txt → sync-from-drive.yml → validation → GitHub mirror + project-status.json → GitHub Pages → verification`

## Обязательный стандарт написания промтов

Полная нормативная инструкция: `PROMPT-STYLE-GUIDE.md`, Drive ID `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`. Это **не краткая памятка**, а обязательный основной стандарт для всех новых и существенно перерабатываемых видео-промтов. Перед prompt-work редактор обязан fresh-read этот файл и затем посмотреть 1–2 актуальные master-сцены как живые примеры.

Стандарт требует, где применимо: техническую строку; точные роли references; reference priority; Scene/Style/Environment; timeline/story flow; camera/continuity; performance; dialogue/vocals/lip sync; lighting/material/production design; native audio; scene-specific negative prompt; глобальный `FRAME FILL / NO BARS`. Детали адаптируются под сцену и движок, но уровень проработки не упрощается до короткого общего описания.

Новый Scene ID определяется автоматически из fresh master: использовать следующий новый стабильный ID и не переиспользовать удалённые IDs. Если ID однозначно выводится из проекта, не спрашивать пользователя.


Приватные instruction files GitHub Actions анонимно не скачивает.


Пять канонических Drive-инструкций:
- `AI-PROJECT-GUIDE.md`
- `SYNC-RUNBOOK.md`
- `USER-GUIDE.md`
- `README-AI-SYNC.md`
- `BACKUP-AI-RUNBOOK.md`


`Topview Slow Watch` работает каждый час и отвечает только за Topview production telemetry по exact mapped tasks. Отдельная hourly automation `AI Film Recovery Sync` отвечает за пять canonical instruction files и recovery/handoff: Google Drive является каноном, при exact-text mismatch она автоматически ремонтирует только GitHub mirror из Drive → GitHub, никогда не пишет GitHub → Drive, затем выполняет semantic consistency check и обновляет recovery state. Результат проверки инструкций хранится в `instruction-sync-status.json`. Такое разделение убирает дублирующие Drive/GitHub проверки и уменьшает число concurrent writers.


## Slow / production state


Видимый slow-marker:
`⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`


`render_state` вычисляется из canonical slow-list:
- slow → `SLOW_PENDING`
- иначе → `IDLE`


`NEEDS_FIX` и `NEEDS_RERENDER` не дают автоматического разрешения на rewrite/rerun.


## Topview


Topview — read-only production telemetry:
- exact mapped task
- model/status
- started/completed timestamps
- `estimateInfo.queueCount`
- `estimateInfo.estimatedWaitSeconds`
- result availability


Каждую сцену проверять по её собственной task.
Нельзя копировать один queue/ETA на все сцены.
`queueCount` — provider telemetry, не обещание точного места пользователя в очереди.


UI:
- `init` / `queued` → `В очереди`
- `running` / `processing` → `Выполняется`
- `success` → `Завершено`
- `fail` / `failed` → `Ошибка`


## Control Center


Viewer: `https://virudik.github.io/ai-film-prompts/`


Принципы:
- русский UI;
- scene/prompt data не hard-code в HTML;
- technical detail → `Контрольный отпечаток`;
- service links → `Служебные файлы`;
- human label и техническое имя резервной инструкции: `BACKUP-AI-RUNBOOK.md` → `Инструкция для резервного ИИ`; старое Claude-specific filename больше не использовать;
- counters Сцен/Промтов/slow/work кликабельны;
- `Сцены в работе` остаются обычной таблицей;
- Topview показывает model/status/start/elapsed/queue/time estimate;
- time estimate оставлена в текущем согласованном one-line виде;
- зелёный меч `✓ СИНХРОНИЗАЦИЯ В ПОРЯДКЕ` = master/status/instructions свежие и здоровые, невосстановленной ошибки workflow нет, после последнего обнаруженного сбоя уже прошло минимум 3 последовательных успешных sync-runs либо сбой не виден в текущем окне истории;
- жёлтый меч `! БЫЛИ ОШИБКИ СИНХРОНИЗАЦИИ` = текущие master/status/instructions уже здоровы, но после недавнего сбоя прошло только 1–2 последовательных успешных sync-runs; это recovery-warning, а не текущая поломка;
- красный меч `✕ ОШИБКА СИНХРОНИЗАЦИИ` / `✕ СИНХРОНИЗАЦИЯ УСТАРЕЛА` = есть невосстановленный workflow failure, unhealthy instruction/project status либо status старше 75 минут;
- рядом с точным временем синхронизации не показывать дублирующее `N мин назад`;
- анимация меча умеренная, не быстрая; зелёный/жёлтый/красный используют общий moving-gradient `saberFlow` + цветовую pulse-анимацию, поэтому движение надписи/свечения должно ощущаться единообразно во всех трёх состояниях;
- в Topview-таблице служебные колонки модели/статуса/запуска/прошедшего времени/очереди держать компактными по содержимому, не растягивать их равномерно; `Seedance 2.5` / `Wan 3.0`, `В очереди` и фразу `ждёт решения` не разрывать переносом внутри самой фразы.


Slow/Topview UI уже объединён и проверен: на сайте видна одна таблица `⏳ Сейчас в медленной генерации — Topview`; canonical membership берётся из master/status, Topview только добавляет telemetry. Не разделять обратно без нового запроса пользователя. Завершённая Topview task, пока Scene ID остаётся в canonical slow list, должна показываться в две строки: `Завершено` и ниже `ждёт решения`.


## References


Registry: `character-references.json`.


8 подтверждённых:
Серёга, Юля, Паша, Артём, Илюша, Саша, Лёша, Виталик.


Правила:
- exact user model sheet > Topview similarity;
- legacy aliases вторичны;
- 960px preview — web preview;
- originals хранятся отдельно;
- Drive содержит `reference-originals.zip`;
- `full_image` для всех 8 подтверждённых model sheets проверен 19.09.2026: файлы `references/full/*.jpg` существуют, а `references.html` открывает `model_sheet.full_image` в lightbox.


## Conflict priority


1. текущая явная команда пользователя
2. fresh Drive master
3. `film-analysis.md`
4. `film-backlog.md`
5. старые Notion notes
6. память чата / старые копии


Consensus ИИ — evidence, not authority.




## Reliability checkpoint 19.09.2026


- Обнаружена гонка между GitHub Actions sync и прямыми telemetry-коммитами: старый workflow иногда падал на `git push` с `fetch first`.
- `.github/workflows/sync-from-drive.yml` обновлён: перед публикацией он берёт свежий `origin/main`, пересобирает status и повторяет push до 4 раз; concurrent sync runs не отменяют друг друга.
- Control Center больше не считает один старый зелёный JSON достаточным: учитывается свежесть успешного `project-status.json` и последний публичный run sync workflow; stale/новая ошибка должны снимать зелёный статус.
- Последний успешный статус всегда важнее старого письма об уже восстановившейся transient-ошибке.
- Master correction 19.09.2026: у сцены 18 служебный контекст исправлен с устаревшего `Seedance 2.5` на фактический `Wan 3.0`; scene-meta и Topview уже указывали Wan 3.0. Slow-lock сцены 18 не изменён.

- Sync encoding guard 19.09.2026: raw `video-prompts.md` must be stored without UTF-8 BOM; workflow now strips an optional BOM before strict header validation. A short-lived BOM introduced during takeover caused fast validation failures and was removed from the same Drive file ID.

## Verified recovery status 19.09.2026

После BOM/race fixes выполнены несколько успешных sync runs. Проверено: revision `19.09.2026`, canonical SHA-256 `66c0f71841d57dd1f47b731f7f25680053e75040ac4a83962c6cf4e43e821e96`, Drive master == GitHub mirror, `health=ok`, `instruction_sync=ok`. Старые failure emails до этого checkpoint не считать текущим incident без fresh-check.

## Planned feature — режим `Сейчас`

Статус: **идея на будущее, не реализована**. Не внедрять без нового явного запроса пользователя.

Цель: дать владельцу проекта короткий рабочий экран «что требует внимания сейчас», не меняя и не урезая основной Control Center. Полный режим со всеми сценами, промтами, W-items, slow/Topview, референсами и служебными файлами остаётся доступным всегда. Режим `Сейчас` — дополнительный view/filter, а не отдельный источник данных и не новый master.

Предлагаемая логика показа:
1. `Требует решения пользователя` — завершённые Topview tasks с сохранённым canonical slow-lock, ambiguous/manual-review состояния и другие элементы, где без пользовательского решения нельзя двигаться дальше.
2. `Проблемы / блокеры` — реальные error/failed states, NEEDS_FIX/NEEDS_RERENDER и подтверждённые continuity/story blockers.
3. `Уже выполняется` — canonical slow scenes и их Topview telemetry, чтобы не запускать повторно.
4. `Следующее логическое действие` — только из явно зафиксированных W-items / backlog / подтверждённого пользователем приоритета. ИИ не должен самовольно объявлять творческий приоритет новым каноническим решением.
5. Остальные сцены в режиме `Сейчас` можно не показывать, но они не удаляются, не деактивируются и остаются в полном режиме сайта.

Правила безопасности:
- `Сейчас` ничего не пишет в prompt master автоматически;
- не меняет Scene IDs, production_state, slow-lock или approval;
- не скрывает данные из полного режима навсегда;
- приоритет, выведенный из технического статуса, должен быть объяснимым и детерминированным;
- творческий/сюжетный приоритет появляется только из канонического W-item/backlog или после явного решения пользователя;
- Topview `success` остаётся техническим completion, а не approval.

Реализация в будущем: добавить кнопку/вкладку `Сейчас`, которая агрегирует существующие `project-status.json`, `topview-status.json`, W-items и production state. Не создавать отдельную параллельную базу данных, если в этом нет необходимости.



## Control Center update — generation status / comments / no-bars rule — 19.09.2026

- В таблице `🎬 Активные сцены проекта — карта и навигация` технический status из `topview-status.json` показывается только для canonical slow-сцен. Если Scene ID снят с slow-list, Topview completion badge в active map больше не показывается. Для slow: `success` → зелёный `✓ ГЕНЕРАЦИЯ ЗАВЕРШЕНА`; `init/queued` → `⏳ В ОЧЕРЕДИ`; `running/processing` → `▶ ВЫПОЛНЯЕТСЯ`; `fail/failed` → `✕ ОШИБКА ГЕНЕРАЦИИ`. Presentation-status не равен approval сам по себе.
- Current state: scene 2 снова входит в canonical slow-list по новому решению пользователя; scenes 6, 7 and 9 удалены из active master; новая scene 19 «Рыбалка и Маша-Лагуна» добавлена active+slow; current slow = 2, 12, 14, 15, 18, 19.
- Под блоком `🛠️ Сцены в работе` / `Ближайшие направления` добавлен публичный раздел `💬 Комментарии / идеи и предложения`. Хранилище обсуждения — GitHub Issue #8 `Идеи и предложения к фильму`; сайт читает его комментарии через public GitHub API. Для публикации/ответа нужен GitHub account; чтение доступно публично. Комментарии не меняют master и не запускают генерации.
- Во все 18 актуальных fenced prompt blocks canonical `video-prompts.md` добавлено единое правило заполнения кадра: `FRAME FILL / NO BARS` — output edge-to-edge, без letterboxing, pillarboxing, black/side bars, decorative borders и пустых полей. Это глобальное prompt-ограничение для текущих активных промтов.
- Email Monitor должен считать GitHub `Run failed` текущим incident только после сравнения с более свежим live `project-status.json` / instruction status / успешным sync. Старые failure-email после более нового success не обозначать как продолжающуюся поломку.


## Stability/current-state policy — 20.09.2026

Добавление, удаление и возврат сцен в slow — нормальные операции и не должны сами по себе ломать систему. Последние сбои были связаны не с самим изменением scene list, а с race/BOM/validator migration и с тем, что current-state факты дублировались в исторических секциях и могли давать semantic false positive.

Правило с этого checkpoint:
- current counts / active IDs / slow IDs / current SHA берутся из fresh Drive master + live `project-status.json`;
- current Topview task IDs/status/queue/ETA берутся из fresh `topview-status.json` после проверки exact task against current scene prompt;
- исторические/checkpoint значения не являются live invariants;
- instruction files задают правила, а не являются параллельной базой runtime-status;
- при конфликте сначала fresh-read live sources, затем чинить documentation drift; не красить health в error только из-за явно исторического текста.

На 20.09.2026 live state: 16 active scenes, 19 prompt texts, W5/W7/W8, canonical slow `2,12,14,15,18,19`, health=ok, instruction_sync=ok, warnings=[]; current master SHA `3dab6fa527063fa8e6174c620c76e17fe9d3ade07aab504ef8cbeb45952543bf`.

Topview mapping checkpoint: Scene 2 current rerun task `d28b2481a8b344439fa175c3ef0b7f5b`; Scene 19 exact task `6ef310d646ca4605b5b10c12752b6ab7`. Scene 19 mapping проверен по полному prompt и является high-confidence; более ранний mismatch-alert был false positive.


## Control Center current/pending UI — 20.09.2026

Уже реализовано:
- theme switch в header между `РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС` и lightsaber health: `☀ Светлая сторона` / `🌙 Тёмная сторона`;
- выбор темы сохраняется в `localStorage` ключ `ai-film-theme`;
- theme — presentation-only и не влияет на master/sync/telemetry.

Новый явный пользовательский план:
- посетитель должен уметь читать, писать и отвечать на комментарии прямо на сайте **без GitHub-аккаунта**;
- текущий GitHub Issue #8 reader остаётся временным/резервным до миграции;
- предпочтительная реализация — Supabase comments backend: public read, anonymous insert, replies через `parent_id`, sanitization, rate-limit/anti-spam, при необходимости moderation;
- service-role/admin secret запрещено помещать в client HTML; использовать безопасные RLS/public anon policies либо server-side endpoint;
- comments никогда не получают права менять prompt master, Scene IDs, slow-lock, approval или запускать генерации.


## Current implementation update — Scene 20 / prompt style / comments

- Current checkpoint after Scene 20: 16 active scenes, 19 prompt texts, W5/W7/W8, canonical slow `2,12,14,15,18,19`; Scene 20 READY / Seedance 2.5 / not slow. Current SHA/health are live-status facts, not duplicated authority here.
- Native comments are already implemented via Supabase organization `Vint`, project `ai-film-comments` / ref `vzohfatqzyioydtgjiyd`: public read, anonymous posting, replies, RLS, honeypot/rate limit, no master mutation rights. UI is a collapsible `💬 Комментарии, идеи и предложения` section below `Контрольный отпечаток`. Any older “next step” wording about comments is historical and superseded by this section.
- All future prompt work must follow the full `PROMPT-STYLE-GUIDE.md`; do not substitute a shortened guide.
