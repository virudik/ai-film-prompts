# AI Film Prompts — Claude Takeover Runbook v2

Эта инструкция используется только когда пользователь явно назначил Claude временным основным редактором из-за недоступности ChatGPT. По умолчанию Claude остаётся review-only.

## Неизменяемые правила v2

- Единственный editable master: Google Drive `AI Film Prompts Master/video-prompts.md`.
- GitHub — public read-only mirror и источник Pages.
- Routine sync: fresh-read Drive master → edit same Drive file ID → `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → validation → GitHub mirror + `project-status.json` → Pages → verification.
- Library, Notion и Drive HTML — backup/documentation, не обязательны после каждой сцены.
- Full checkpoint — только по explicit request/milestone/architecture change.
- Scene IDs после удаления не перенумеровывать; gaps допустимы.
- Slow-status `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` совпадает в четырёх местах: global status, dedicated slow table, TOC row, full scene section.
- Человекочитаемые даты — `DD.MM.YYYY`.
- `index.html` — viewer, scene content не hard-code; montage review ведёт на rendered GitHub Pages HTML.
- `ГОТОВО` — только после фактической проверки требуемого результата.

## Перед началом takeover

Прочитать:
1. этот файл;
2. `SYNC-RUNBOOK.md`;
3. `AI-PROJECT-GUIDE.md`;
4. fresh Drive `video-prompts.md`;
5. `film-analysis.md` / `film-backlog.md`, если задача зависит от сюжета/continuity.

## Работа с master

- редактировать существующий Drive master в том же file ID;
- менять только approved scene/status;
- обновлять TOC/counts/W/slow invariants;
- scene IDs после удаления не перенумеровывать;
- не создавать параллельный master;
- для визуальной проверки нужны actual references.

## Sync

Если GitHub write доступен:
1. update `SYNC-TRIGGER.txt`;
2. дождаться `sync-from-drive.yml`;
3. проверить `project-status.json` health;
4. проверить Pages.

Если GitHub write недоступен:
- Drive edit можно выполнить;
- немедленный trigger может быть недоступен;
- scheduled workflow должен подтянуть Drive;
- не заявлять, что Pages обновлён, пока это фактически не подтверждено.

## Сайт

`index.html` — viewer. Scene text меняется через master. Прямой UI/site-code edit требует GitHub write. `Монтажный разбор фильма` должен вести на rendered Pages HTML.

## Notion/Library

Не обновлять после каждой сцены. Обновлять при architecture changes, milestones, explicit backup/full checkpoint.

## Возврат управления ChatGPT

Сообщить:
- какие Drive files/scenes изменены;
- был ли trigger/workflow;
- health;
- Pages;
- менялись ли Notion/Library/instructions;
- что осталось не подтверждено.

## Recovery

Если память потеряна: этот файл → `SYNC-RUNBOOK.md` → `AI-PROJECT-GUIDE.md` → fresh Drive master → status/Pages → film context при необходимости.
