# AI Film Project — Start Here v2

Эта инструкция задаёт правила для ChatGPT, Work, Claude, Gemini, DeepSeek, Grok и других ИИ, работающих с проектом.

## Неизменяемые правила v2

- Единственный редактируемый master: Google Drive `AI Film Prompts Master/video-prompts.md`, file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
- GitHub `virudik/ai-film-prompts` — публичное read-only зеркало и источник GitHub Pages.
- `project-status.json` — automatically generated machine-status; вручную не редактировать.
- Routine sync: **fresh-read Drive master → edit same Drive file ID → `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → validation → GitHub mirror + `project-status.json` → Pages → verification**.
- Library, Notion и Drive HTML — backup/documentation, не gate routine edit.
- Полный обход всех зеркал выполняется только при explicit backup/checkpoint, architecture/instruction change или команде **«полная ручная синхронизация всего и везде»**.
- Scene ID стабилен: после удаления готовой сцены остальные сцены не перенумеровывать; пропуски допустимы, IDs уникальны и возрастают.
- Slow-status `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` должен совпадать в четырёх местах: global status, dedicated slow table, TOC row, full scene section.
- Человекочитаемые даты — `DD.MM.YYYY`.
- `index.html` — viewer, читает `video-prompts.md` и `project-status.json` с `cache: no-store`; scene content не hard-code.
- `Инструкция для ИИ` + `Для владельца` — две половинные кнопки; первая не переносится.
- `Монтажный разбор фильма` ведёт на rendered GitHub Pages `Seregius_montazhny_razbor.html`.
- Legacy `_source/part-*` builder не использовать.
- `ГОТОВО` — только после обязательной проверки фактического результата.

## Источник истины и контекст

Канонический prompt master — только Drive `video-prompts.md`.

Для обычной правки одного prompt достаточно fresh master + реальные references нужной сцены.

Для story/continuity/placement дополнительно читать `film-analysis.md` и `film-backlog.md`. Для глубокой структуры при необходимости — `Seregius_montazhny_razbor.html`, `EDIT_PLAN_V2.csv`, `PROGRESS.md`.

Не утверждать, что весь фильм был непрерывно просмотрен со звуком в реальном времени, если это не было фактически выполнено.

## Reference rules

- `@image1`, `@video1` и т. п. локальны для конкретной сцены.
- Для проверки внешности нужны реальные references.
- Character/model sheet имеет приоритет для внешности/одежды; environment/group refs вторичны.
- Continuous take не смешивать с hard cuts/shot-reverse-shot/inserts без явной причины.

## Роли ИИ

### ChatGPT — основной редактор по умолчанию
1. fresh-read Drive master;
2. изменить только approved block;
3. сохранить same Drive file ID;
4. обновить TOC/count/status при необходимости;
5. обновить `SYNC-TRIGGER.txt`;
6. проверить workflow → health → Pages.

### Work
Для многосценового, монтажного, backlog/analysis и широкого аудита. При записи — тот же Drive master, без второго master.

### Claude
Review-only по умолчанию. При явном назначении временным основным редактором переходит на `CLAUDE-TAKEOVER-RUNBOOK.md`.

### Gemini
Независимая проверка prompt + visual references.

### DeepSeek
Технический аудит: contradictions, timing, camera/action conflicts, overload, reference priority, negative constraints, continuity.

### Grok
Creative/comedy/pacing second opinion при сохранении continuity.

### Другие ИИ
Review-only по умолчанию. Рекомендации привязывать к точным scene IDs/names.

## Передача советов между ИИ

Внешний ИИ возвращает patch/replacement/recommendation. Канон меняет только один текущий редактор. Не создавать `video-prompts-final`, `v2`, `copy`, `final-final`.

## Conflict priority

1. текущая явная команда пользователя;
2. свежий Drive master;
3. factual `film-analysis.md`;
4. `film-backlog.md`;
5. старые Notion notes;
6. память чата/старые копии.

## Публичные ссылки

- Viewer: `https://virudik.github.io/ai-film-prompts/`
- Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
- Repo: `https://github.com/virudik/ai-film-prompts`
- Film map: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-analysis.md`
- Backlog: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-backlog.md`
- Montage review: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`
- Sync runbook: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/SYNC-RUNBOOK.md`
- Claude takeover: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/CLAUDE-TAKEOVER-RUNBOOK.md`
