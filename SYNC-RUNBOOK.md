# AI Film Prompts — Full Sync Runbook v3.5


Нормативный технический runbook для основного редактора проекта.


## 1. Неизменяемые правила


- Editable master только Google Drive `video-prompts.md`.
- File ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- Folder ID: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
- GitHub `virudik/ai-film-prompts` — mirror + Pages.
- `project-status.json` генерируется, вручную не менять.
- Scene IDs stable; gaps допустимы.
- Перед каждой записью — fresh-read Drive master.
- Slow-scene не перезапускать без результата/ошибки/явного решения пользователя.
- Не создавать `video-prompts-v2/final/copy/final-final`.


## 2. Routine edit одной сцены


1. Fresh-read Drive master.
2. Найти exact Scene ID.
3. Изменить только нужный scene block/TOC/count/status metadata.
4. Сохранить тот же Drive file ID.
5. Обновить `SYNC-TRIGGER.txt` в GitHub.
6. Дождаться `sync-from-drive.yml`.
7. Проверить validation.
8. Проверить GitHub `video-prompts.md`.
9. Проверить `project-status.json`.
10. Проверить Pages.


Не писать пользователю `ГОТОВО`, пока обязательная проверка не завершилась.


## 3. Full instruction checkpoint


Пять канонических Drive instruction files:
- `AI-PROJECT-GUIDE.md` — `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `SYNC-RUNBOOK.md` — `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `USER-GUIDE.md` — `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` — `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `BACKUP-AI-RUNBOOK.md` — `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`


После изменения инструкций:
1. обновить Drive originals — это канон;
2. `AI Film Recovery Sync` (hourly) сравнивает полный текст и при mismatch автоматически обновляет только GitHub mirror из Drive → GitHub; обратное направление запрещено;
3. выполнить/дождаться авторизованной exact-text сверки;
4. выполнить semantic consistency check по известным критическим правилам;
5. обновить `instruction-sync-status.json`;
6. дождаться rebuild `project-status.json`;
7. проверить `instruction_sync.health`.

Для срочного изменения основной редактор может обновить GitHub mirror сразу вручную, но источник всё равно Drive, а итог обязан пройти ту же сверку.


States:
- `ok` exact match + fresh
- `stale` snapshot >3h
- `error` mismatch/read failure
- `unverified` missing/invalid snapshot


При `error` различать два случая: exact-text mismatch GitHub mirror можно автоматически исправить только из canonical Drive → GitHub; semantic conflict, missing Drive source или неоднозначность автоматически в Drive не исправлять — сообщить точные файлы/формулировки пользователю.


## 4. Current integrity checkpoint


На момент handoff:
- 15 scenes
- 18 prompt texts
- W5/W7/W8
- slow: 2,12,14,15,18,19


Всегда fresh-check.


Validator должен подтверждать:
- declared scenes = `## Сцена N`
- declared scenes = scene map rows
- IDs unique/increasing
- prompt count = fenced prompt blocks
- W-count correct
- slow list consistent
- scene-meta valid
- dependency targets exist
- canonical SHA present


## 5. Topview telemetry workflow


Automation: `Topview Slow Watch`.


Для каждой slow scene:
1. взять exact mapped task ID;
2. query exact task;
3. сохранить status/model/start/end;
4. `queue_count` только из `estimateInfo.queueCount` этой задачи;
5. provider ETA только из `estimateInfo.estimatedWaitSeconds` этой задачи;
6. historical ETA отдельно;
7. success означает completion, не approval;
8. slow-lock в master не снимать автоматически.


Current decision 19.09.2026: scene 2 по новому прямому решению пользователя возвращена в canonical slow-list. Scenes 6, 7 and 9 удалены из active master как больше не актуальные. Не восстанавливать их автоматически. Добавлена новая active+slow scene 19 «Рыбалка и Маша-Лагуна» для Wan 3.0, 30s, русский диалог. Current canonical slow = 2,12,14,15,18,19. В active scene map generation-status badge показывается только canonical slow-сценам.


## 6. Control Center management


Основной UI: GitHub `index.html`.


Можно менять:
- layout/navigation
- labels/translations
- filters
- visual status
- table composition
- link behavior


Нельзя:
- hard-code актуальный список сцен вместо master/status;
- вручную редактировать machine `project-status.json`;
- превращать GitHub в editable master.


Текущие UI conventions:
- Service links → `Служебные файлы`
- `BACKUP-AI-RUNBOOK.md` — нейтральная инструкция для любого резервного ИИ; в UI подписывается `Инструкция для резервного ИИ`
- Technical detail → `Контрольный отпечаток`
- sync lightsaber animation family is shared across green/yellow/red: moving `saberFlow` gradient + state-specific brightness/glow pulse; do not add a separate text-position animation
- healthy stable state: green lightsaber `✓ СИНХРОНИЗАЦИЯ В ПОРЯДКЕ`
- recovered recent workflow failure with only 1–2 consecutive successful sync-runs after it: yellow lightsaber `! БЫЛИ ОШИБКИ СИНХРОНИЗАЦИИ`
- unresolved failure, unhealthy status/instructions, or stale heartbeat (>75 min): red lightsaber `✕ ОШИБКА СИНХРОНИЗАЦИИ` / `✕ СИНХРОНИЗАЦИЯ УСТАРЕЛА`
- Topview `running` → `Выполняется`
- Topview `init/queued` → `В очереди`
- queue header → `Очередь`
- Topview sync timestamp in header
- active scene map remains separate
- `Сцены в работе` remains scalable table
- time estimate stays in current one-line combined display


Current slow UI:
- объединение уже реализовано;
- на сайте видна одна таблица `⏳ Сейчас в медленной генерации — Topview`;
- canonical membership берётся из `project-status.json.slow_scenes`, а Topview только дополняет строки model/status/start/elapsed/queue/ETA;
- исходная slow-таблица master остаётся в Markdown и скрывается в presentation layer, чтобы не было двух одинаковых видимых таблиц;
- не разделять обратно без нового запроса пользователя;
- в Topview-таблице служебные колонки `Модель`, `Статус`, `Запуск`, `Прошло`, `Очередь` используют компактную content-driven ширину и не растягиваются вместе со всей таблицей; больше пространства получают название сцены и оценка времени; значения модели (`Seedance 2.5`, `Wan 3.0`), status `В очереди` и фраза `ждёт решения` не переносятся внутри себя;
- если Topview `success`, но Scene ID ещё canonical slow, Status выводится в две строки: `Завершено` / `ждёт решения`.


## 7. Character references


Repo:
- `character-references.json`
- `references.html`
- `references/*` legacy fallbacks


Rules:
- exact user-confirmed model sheet is authoritative;
- never replace based on Topview visual similarity;
- aliases are technical secondary labels;
- 960px preview is intentional for performance;
- originals archive exists on Drive as `reference-originals.zip`.


Проверено 19.09.2026: для всех 8 подтверждённых персонажей существуют public `references/full/*.jpg`, а `references.html` использует `model_sheet.full_image` для lightbox.


## 8. Recovery order


1. `NEW-CHAT-HANDOFF.md`
2. this runbook
3. `AI-PROJECT-GUIDE.md`
4. fresh Drive master
5. `project-status.json`
6. `topview-status.json`
7. `instruction-sync-status.json`
8. only then edit


## 9. Permanent links


Viewer:
`https://virudik.github.io/ai-film-prompts/`


Repo:
`https://github.com/virudik/ai-film-prompts`


Raw master:
`https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`




## 10. Concurrent-write recovery


GitHub может получать прямые telemetry-коммиты Topview/instruction verification одновременно с `sync-from-drive.yml`. Ранее это давало transient `git push ... fetch first`.


Текущий sync workflow обязан:
1. не отменять соседний sync run только из-за concurrency;
2. перед публикацией выполнить fresh `git fetch origin main`;
3. сбросить runner на свежий `origin/main`;
4. заново построить `project-status.json` поверх свежего instruction snapshot;
5. при non-fast-forward повторить цикл до 4 раз;
6. считать ошибкой только невосстановленный итог после retry.


Control Center дополнительно проверяет свежесть последнего успешного status и публичный результат последнего sync workflow, чтобы старый зелёный status не маскировал новую невосстановленную ошибку.


## 11. Encoding guard

Canonical raw `video-prompts.md` should be UTF-8 without BOM. On 19.09.2026 a write path temporarily inserted UTF-8 BOM (`EF BB BF`), causing strict `^#` header validation to fail even though the Markdown text was readable. The master was repaired in place and `sync-from-drive.yml` now strips an optional BOM before validation. When diagnosing a 4–6 second failure in the download step, inspect first bytes/encoding before blaming Drive access.

## 12. Verified recovery checkpoint

19.09.2026 после race retry + BOM normalization выполнены несколько успешных sync runs. Исторический recovery-checkpoint на тот момент: revision `19.09.2026`, SHA-256 `66c0f71841d57dd1f47b731f7f25680053e75040ac4a83962c6cf4e43e821e96`, Drive mirror exact match, health/instruction sync = `ok`. Этот SHA — снимок прошлого checkpoint, а не постоянный live-инвариант: после легитимной правки master текущий SHA может измениться. Актуальный fingerprint всегда брать из свежего `project-status.json`; historical/checkpoint SHA не считать semantic conflict только из-за отличия от live SHA. При будущих письмах `Run failed` всегда сравнивать время письма с более свежим успешным `project-status.json.synced_at`.


## 13. Hourly recovery automation

`AI Film Recovery Sync` runs hourly. It:
1. reads fresh Drive master + five canonical Drive instruction files + handoff;
2. repairs instruction mirrors only Drive → GitHub when exact text differs;
3. never writes GitHub instruction text back into Drive;
4. checks known semantic contradictions, including merged slow UI, scene 18 = Wan 3.0, Drive-only editable master, Topview success != approval, no automatic slow-lock removal, and current race/BOM recovery rules; historical/checkpoint SHA values are evidence only and must not be required to equal the current live SHA;
5. refreshes `NEW-CHAT-HANDOFF.md` only for material state changes and keeps its GitHub mirror aligned;
6. otherwise stays silent.

## 14. Backup-AI filename migration validator fix — 19.09.2026

После переименования пятого canonical instruction file с `CLAUDE-TAKEOVER-RUNBOOK.md` на `BACKUP-AI-RUNBOOK.md` validator `scripts/build_project_status.py` тоже обязан использовать новое имя в `INSTRUCTION_FILES`. Если exact-text snapshot показывает все пять файлов `match=true`, но workflow падает с `instruction_sync_error`, первым делом проверить, что validator не ожидает старое filename. 19.09.2026 этот хвост миграции был найден и исправлен; следующий sync успешно пересобрал `project-status.json` с `health=ok` и `instruction_sync=ok`.



## Stability/current-state policy — 20.09.2026

Добавление, удаление и возврат сцен в slow — нормальные операции и не должны сами по себе ломать систему. Последние сбои были связаны не с самим изменением scene list, а с race/BOM/validator migration и с тем, что current-state факты дублировались в исторических секциях и могли давать semantic false positive.

Правило с этого checkpoint:
- current counts / active IDs / slow IDs / current SHA берутся из fresh Drive master + live `project-status.json`;
- current Topview task IDs/status/queue/ETA берутся из fresh `topview-status.json` после проверки exact task against current scene prompt;
- исторические/checkpoint значения не являются live invariants;
- instruction files задают правила, а не являются параллельной базой runtime-status;
- при конфликте сначала fresh-read live sources, затем чинить documentation drift; не красить health в error только из-за явно исторического текста.

На 20.09.2026 live state: 15 active scenes, 18 prompt texts, W5/W7/W8, canonical slow `2,12,14,15,18,19`, health=ok, instruction_sync=ok, warnings=[]; current master SHA `3dab6fa527063fa8e6174c620c76e17fe9d3ade07aab504ef8cbeb45952543bf`.

Topview mapping checkpoint: Scene 2 current rerun task `d28b2481a8b344439fa175c3ef0b7f5b`; Scene 19 exact task `6ef310d646ca4605b5b10c12752b6ab7`. Scene 19 mapping проверен по полному prompt и является high-confidence; более ранний mismatch-alert был false positive.


## Topview mapping hardening — 20.09.2026

Для нового/возвращённого slow Scene ID automation обязана:
1. fresh-read Drive master scene block;
2. fresh-read `project-status.json.slow_scenes`;
3. query candidate board task;
4. сравнить task prompt/reference semantics с current scene body;
5. только после совпадения записать mapping `verified=true` / high confidence;
6. если task prompt явно соответствует сцене, не отвергать её из-за stale title/старого handoff snapshot;
7. если exact match не доказан — `unverified`, queue/ETA не подставлять.

Current exact mappings: Scene 2 → `d28b2481a8b344439fa175c3ef0b7f5b`; Scene 19 → `6ef310d646ca4605b5b10c12752b6ab7`.
