# NEW CHAT HANDOFF — AI Film Project
**Checkpoint: 18.09.2026**

Этот файл — переходная точка для следующего чата. Он не заменяет fresh-read master/status.

## 1. Что новому ChatGPT проверить в первую очередь

До любых изменений:

1. Прочитать этот `NEW-CHAT-HANDOFF.md`.
2. Прочитать `SYNC-RUNBOOK.md`.
3. Прочитать `AI-PROJECT-GUIDE.md`.
4. Fresh-read Drive `video-prompts.md`, file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
5. Прочитать live GitHub `project-status.json`.
6. Прочитать live `topview-status.json`.
7. Прочитать live `instruction-sync-status.json`.
8. Повторить пользователю current fingerprint:
   - revision
   - master SHA
   - scenes/prompts
   - work items
   - slow scenes
   - health
   - instruction sync health
9. Если задача про сюжет/монтаж — `film-analysis.md` + `film-backlog.md`.
10. Только после этого писать.

## 2. Ключевые точки

Drive folder:
`1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`

Drive master:
`1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`

GitHub:
`virudik/ai-film-prompts`

Viewer:
`https://virudik.github.io/ai-film-prompts/`

Handoff Drive ID:
`1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`

## 3. Snapshot на момент передачи

- 17 active scenes
- 20 prompt texts
- W5, W7, W8
- canonical slow list: 2,6,12,14,15,18
- Scene IDs: 1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18

Всегда fresh-check.

## 4. Самое важное safety-состояние

Topview last observed:
- scene 6 task технически `success`
- canonical master всё ещё содержит scene 6 в slow list

Это intentional safety state.
Topview completion не снимает slow-lock автоматически.

Новый чат должен проверить результат scene 6 и дождаться решения пользователя:
- принять;
- доработать;
- оставить;
- перезапустить.

Только после решения обновлять master slow state.

## 5. Что сделано в этом чате

### Control Center

Сделано:
- technical links → `Служебные файлы`;
- technical explanations/status legend → `Контрольный отпечаток`;
- search helper убран;
- advanced filters свёрнуты;
- duplicated status blocks сокращены;
- `17 Сцен` кликабельно ведёт к scene map;
- `20 Промтов` ведёт к full prompts;
- slow count ведёт к slow filter;
- work count ведёт к `Сцены в работе`;
- W5/W7/W8 вернули в обычную масштабируемую таблицу;
- active scene map восстановлена;
- scene 1 navigation conflict fixed;
- dependencies показываются по-русски;
- Topview completion time находится внутри Status;
- Topview sync timestamp справа в header;
- `Очередь Topview` сокращено до `Очередь`;
- per-task queue telemetry исправлена;
- `running`/`processing` → `Выполняется`;
- `init`/`queued` → `В очереди`;
- `success` → `Завершено`;
- `fail`/`failed` → `Ошибка`;
- time estimate оставлена как согласовано: `≈ ... · Topview ... · история ...`;
- button styles/hover выровнены;
- obsolete CSS/renderer частично очищены;
- health ok = green lightsaber `✓ СИНХРОНИЗАЦИЯ В ПОРЯДКЕ`;
- error state = red lightsaber `✕ ОШИБКА СИНХРОНИЗАЦИИ`;
- рукоятка увеличена;
- анимация меча затем замедлена.

### Slow section

Пользователь запросил короткий heading:
`## ⏳ Сейчас в медленной генерации`

без суффикса `— НЕ ЗАПУСКАТЬ ПОВТОРНО`.

Safety остаётся в slow markers и логике.

### Work notes

Общий development paragraph убран.
W5/W7/W8 notes разнесены в их rows.
Historical W context перенесён ближе к соответствующим active scenes, где уместно.

### References

Сделано:
- cards упрощены;
- repeated priority text убран;
- `Основной референс` — основной label;
- legacy aliases secondary;
- repeated `Нажми на лист...` убрано;
- lightbox fixed;
- 960px previews используются для скорости;
- Drive содержит `reference-originals.zip`;
- Drive также содержит `reference-serega-original.jpg`.

## 6. Что НЕ закончено / нельзя считать законченным

1. **Не объединены две slow-таблицы.**
   Обсуждается объединение:
   - `Мониторинг медленных генераций Topview`
   - `⏳ Сейчас в медленной генерации`
   Пока НЕ менять.

2. **High-resolution references.**
   960px previews точно используются.
   Архив originals точно есть в Drive.
   Нельзя без проверки утверждать, что lightbox публично открывает отдельный original для каждого из 8.

3. **Scene 6 Topview success vs canonical slow.**
   Требует пользовательского решения.

4. **Не менять time estimate** без нового запроса.

5. После крупных instruction changes нужно заново проверить exact Drive↔GitHub instruction match и свежесть `instruction-sync-status.json`.

## 7. Как менять master

1. Fresh-read exact Drive master.
2. Не использовать старую GitHub/Library copy как source.
3. Изменить только нужный Scene ID.
4. При необходимости обновить:
   - scene map row
   - full section
   - scene-meta
   - counts
   - slow table/status
5. Save SAME Drive file ID.
6. Update GitHub `SYNC-TRIGGER.txt`.
7. Wait sync workflow.
8. Verify `project-status.json`.
9. Verify Pages.
10. Report exact change.

## 8. Как управлять сайтом

UI:
GitHub `index.html`

References UI:
GitHub `references.html`

Registry:
GitHub `character-references.json`

Site-only changes можно делать прямо в GitHub presentation layer.

После UI change:
1. update exact file;
2. JS syntax check;
3. duplicate HTML ID check;
4. wait Pages deploy;
5. verify conclusion.

Scene/prompt content всё равно меняется только в Drive master.

## 9. Topview telemetry

Automation:
`Topview Slow Watch`

Rules:
- query exact mapped task per scene;
- no global queue copied to every row;
- Topview read-only;
- success != accepted;
- no automatic slow-lock removal;
- never replace user-confirmed refs from similarity.

## 10. Instruction sync

Canonical Drive instructions:
- AI-PROJECT-GUIDE.md
- SYNC-RUNBOOK.md
- USER-GUIDE.md
- README-AI-SYNC.md
- CLAUDE-TAKEOVER-RUNBOOK.md

Authorized verification compares full text with GitHub mirrors.

Mismatch:
- `instruction-sync-status.json` → error
- no auto-copy
- report exact filename

## 11. Confirmed reference identities

- Серёга
- Паша
- Артём
- Илюша
- Саша
- Лёша
- Виталик
- Юля

Natural names should map to these identities; user should not need internal aliases.

## 12. Open UX question: combining slow tables

Current duplication:
A. Topview monitor = operational telemetry.
B. Canonical slow table = scene + canonical slow lock.

Potential combined table:
`# | Сцена | Что происходит | Модель | Статус | Запуск | Прошло | Очередь | Оценка времени`

Canonical slow-lock must remain visibly distinct from Topview status.

DO NOT implement until user approves.

## 13. Ready-to-paste command for next chat

> Продолжаем AI Film project. Сначала открой свежий Google Drive `NEW-CHAT-HANDOFF.md`, `SYNC-RUNBOOK.md`, `AI-PROJECT-GUIDE.md` и exact master `video-prompts.md` file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`. Затем прочитай live `project-status.json`, `topview-status.json`, `instruction-sync-status.json` из `virudik/ai-film-prompts` и повтори текущий audit fingerprint. Не используй старые копии как master. Не меняй Scene IDs. Не перезапускай slow scenes автоматически. Обрати особое внимание: scene 6 была замечена как Topview success, но canonical slow-lock ещё не снят — сначала проверить результат и спросить решение. Site UI меняется в GitHub `index.html`, scene/prompt content меняется только в Drive master. Перед `ГОТОВО` проверь sync workflow, validation и Pages.

## 14. Зачем этот handoff

Следующий чат должен за несколько минут понять:
- где истина;
- какие файлы редактируемые;
- как синхронизировать;
- какие UI решения уже приняты;
- какие решения ещё обсуждаются;
- что нельзя автоматически перезапускать или удалять.
