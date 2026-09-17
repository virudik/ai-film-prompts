# AI Film Prompts — Claude Takeover Runbook v3.5

Эта инструкция используется только когда пользователь явно назначил Claude временным основным редактором из-за недоступности ChatGPT. По умолчанию Claude остаётся review-only.

## Safety summary v3.5

Полные правила — `SYNC-RUNBOOK.md`. Минимум:

- Единственный редактируемый prompt master — существующий Google Drive `video-prompts.md` с file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
- GitHub — public read-only mirror; Library/Notion не становятся временным master.
- `project-status.json` schema v3 генерируется автоматически; вручную его не править.
- Scene IDs не перенумеровывать. Slow-сцену не перезапускать без результата/ошибки или разрешения.
- Пять Drive-инструкций канонические для своих GitHub-зеркал.
- Если `instruction_sync.health = unverified`, не выдавать это за подтверждённое совпадение инструкций.

## Перед началом takeover — capability preflight

До первой записи проверить доступные инструменты.

Claude может принять editor-role только если доступный Drive action умеет **заменить raw contents существующего canonical file по тому же file ID**, а не только читать/переименовывать/перемещать или создавать новый файл.

Если такой операции нет:
- не создавать `video-prompts-copy`, `final`, `v2` и т. п.;
- не объявлять себя фактическим editor;
- подготовить точный patch/replacement text;
- попросить пользователя/ChatGPT применить patch к существующему file ID;
- продолжать как review-only.

## Что прочитать

1. этот файл;
2. `SYNC-RUNBOOK.md`;
3. `AI-PROJECT-GUIDE.md`;
4. fresh Drive `video-prompts.md`;
5. current `project-status.json` fingerprint;
6. `film-analysis.md` / `film-backlog.md`, если задача зависит от сюжета/continuity.

Перед выводами повторить fingerprint: revision, master SHA, scene IDs, W-items, slow scenes, health, instruction sync health. Если snapshot старый — обновить источники.

## Работа с master

- редактировать существующий Drive master в том же file ID;
- менять только approved scene/status;
- обновлять TOC/counts/W/slow invariants;
- scene IDs после удаления не перенумеровывать;
- не создавать параллельный master;
- actual references нужны для визуальной проверки;
- optional `scene-meta` добавлять только валидным блоком; `render_state` вручную не задавать.

## Production status / сайт

- `NEEDS_FIX` = кандидат на отдельное обсуждение правки; не переписывать prompt автоматически.
- `NEEDS_RERENDER` = известна необходимость нового дубля, но новый запуск требует соблюдения slow-lock/решения пользователя.
- `SLOW_PENDING` вычисляется из canonical slow-list, не редактируется вручную.
- Пользовательские подписи Control Center — русские; machine enum schema v3 не переименовывать.
- Не hard-code slow/status/scene content в `index.html`.

## Sync

Если GitHub write доступен:
1. update `SYNC-TRIGGER.txt`;
2. дождаться `sync-from-drive.yml`;
3. проверить Actions success;
4. проверить `project-status.json` health + fingerprint;
5. проверить Pages.

Если GitHub write недоступен:
- Drive edit можно выполнять только если capability preflight пройден;
- немедленный trigger может быть недоступен;
- scheduled workflow позже подтянет master;
- не заявлять, что GitHub/Pages обновлены, пока это не подтверждено.

## Instruction changes

Если takeover затрагивает одну из пяти Drive-инструкций:
- изменять тот же Drive file ID;
- считать Drive authoritative;
- GitHub mirror обновлять отдельно через доступный authenticated path;
- не менять privacy Drive-файла ради Actions;
- `instruction_sync: unverified` не считать ошибкой master, но явно сообщать, что automatic instruction verification не настроена.

## Topview evidence

Если Topview подключён, его board/task metadata можно читать для сверки фактического запуска, модели, prompt и технического результата. Не считать Topview вторым master; неоднозначный task не привязывать к scene ID автоматически, а `success` не означает user approval.

## Сайт

`index.html` — viewer. Scene text меняется через master. Прямой UI/site-code edit требует GitHub write. `Монтажный разбор фильма` должен вести на rendered Pages HTML.

## Notion/Library

Не обновлять их после каждой сцены. Обновлять при architecture changes, milestones, explicit backup/full checkpoint.

## Возврат управления ChatGPT

Сообщить:
- какие Drive files/scenes изменены;
- capability preflight result;
- был ли trigger/workflow;
- Actions health;
- project fingerprint;
- Pages;
- менялись ли instructions/Notion/Library;
- что осталось `unverified`.

## Recovery

Если память потеряна: этот файл → `SYNC-RUNBOOK.md` → `AI-PROJECT-GUIDE.md` → fresh Drive master → `project-status.json` fingerprint → film context при необходимости.
