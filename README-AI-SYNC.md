# AI Video Prompts — synchronization rules v3.5

Короткая техническая спецификация. Нормативный подробный процесс — в `SYNC-RUNBOOK.md`.

## Canonical locations

1. Google Drive `AI Film Prompts Master/video-prompts.md` — единственный authoritative editable prompt master.
2. Пять Drive instruction files — canonical для своих GitHub mirrors.
3. GitHub root `video-prompts.md` + instruction files — public read-only mirrors.
4. `project-status.json` — generated machine status schema v3.
5. GitHub Pages — public viewer.
6. Drive `video-prompts.html`, ChatGPT Library и Notion Hub — backup/documentation layers.

## Routine master sync

1. fresh-read Drive master;
2. edit same Drive file ID;
3. update TOC/counts/statuses as required;
4. update `SYNC-TRIGGER.txt`;
5. wait for `sync-from-drive.yml`;
6. require Actions success;
7. require `project-status.json` → `health: ok`;
8. verify fingerprint + public/raw content;
9. verify Pages;
10. report success.

Scheduled workflow также проверяет Drive master примерно каждые 30 минут.

## Schema v3

`project-status.json` сохраняет backward-compatible v2 fields и добавляет:
- `canonical_master_sha256` / bytes;
- `audit_fingerprint`;
- `scene_meta`;
- generated `render_state`;
- `instruction_sync`;
- metadata validation checks.

Slow render-state выводится из existing slow-list, поэтому нового ручного slow-поля нет.

## Control Center

`index.html` — read-only production UI. Пользовательские подписи отображаются по-русски, machine enum-значения schema v3 остаются неизменными.

- `NEEDS_FIX` = кандидат на обсуждение/корректировку, не автоматический rewrite;
- `NEEDS_RERENDER` = требуется новый дубль по отдельному решению;
- slow state берётся только из canonical slow-list → generated `render_state`;
- фильтры/чипы появляются только из подтверждённых `scene_meta`.

## Instruction freshness

Drive instruction files сейчас приватны. GitHub Actions не имеет authenticated access к ним, поэтому автоматический routine workflow **не должен** пытаться скачивать их анонимно.

Текущее ожидаемое состояние:
- `instruction_sync.health = unverified`;
- warning `instruction_sync_unverified`.

При architecture/instruction checkpoint основной редактор должен fresh-read Drive instructions и зеркально обновить GitHub через authenticated connectors/manual editor path, сохраняя те же Drive file IDs.

Нельзя делать Drive instructions публичными только ради упрощения Actions без отдельного решения пользователя.

## Topview evidence

Подключённый Topview допустим как read-only evidence layer для task status/model/prompt/result. Он не становится source of truth и не заменяет Drive master. `success` подтверждает техническое завершение генерации, но не creative acceptance.

## Validation invariant

Валидатор должен проверять:
- scene counts;
- TOC/sections;
- prompt fences;
- W-items;
- slow list + четыре slow locations;
- unique/increasing scene IDs;
- canonical master SHA presence;
- если `scene-meta` присутствует — JSON/schema/production-state/duration/dependency targets.

Scene ID gaps допустимы.

## Full checkpoint

При architecture/instruction change или explicit full-sync проверить:
- Drive master integrity;
- schema v3/fingerprint;
- five canonical Drive instructions;
- matching GitHub instruction mirrors;
- Actions;
- `project-status.json`;
- Pages;
- Drive HTML/Library/Notion according to `SYNC-RUNBOOK.md`;
- end-to-end public verification.

Legacy `_source/part-*` builder не использовать.
