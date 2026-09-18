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
- `CLAUDE-TAKEOVER-RUNBOOK.md` — `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`

После изменения инструкций:
1. обновить Drive originals;
2. обновить GitHub mirrors exact-text;
3. выполнить авторизованную сверку;
4. обновить `instruction-sync-status.json`;
5. дождаться rebuild `project-status.json`;
6. проверить `instruction_sync.health`.

States:
- `ok` exact match + fresh
- `stale` snapshot >3h
- `error` mismatch/read failure
- `unverified` missing/invalid snapshot

При `error` ничего не перезаписывать автоматически.

## 4. Current integrity checkpoint

На момент handoff:
- 17 scenes
- 20 prompt texts
- W5/W7/W8
- slow: 2,6,12,14,15,18

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

На момент handoff scene 6 наблюдалась как `success`, но master всё ещё содержит её в slow list. Это intentional safety state до пользовательского решения.

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
- Technical detail → `Контрольный отпечаток`
- current health green lightsaber: `✓ СИНХРОНИЗАЦИЯ В ПОРЯДКЕ`
- health error red lightsaber: `✕ ОШИБКА СИНХРОНИЗАЦИИ`
- Topview `running` → `Выполняется`
- Topview `init/queued` → `В очереди`
- queue header → `Очередь`
- Topview sync timestamp in header
- active scene map remains separate
- `Сцены в работе` remains scalable table
- time estimate stays in current one-line combined display

Open UX question:
Topview monitor and canonical slow table duplicate some rows. Do not merge until user approves a concrete design.

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

Before claiming full-res click is live for all 8, verify actual public paths and lightbox behavior.

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
