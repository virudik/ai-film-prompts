# AI Video Prompts — synchronization rules v2

Короткая техническая спецификация синхронизации.

## Неизменяемые правила v2

- Единственный editable master: Google Drive `AI Film Prompts Master/video-prompts.md`.
- GitHub root `video-prompts.md` — public read-only mirror.
- `project-status.json` — generated machine status; вручную не редактировать.
- Routine sync: fresh-read Drive master → edit same Drive file ID → `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → validation → GitHub mirror + `project-status.json` → Pages → verification.
- Library, Drive HTML и Notion не являются обязательными точками routine edit.
- Full backup/checkpoint выполняется только по explicit request, milestone или architecture/instruction change.
- Scene IDs уникальны и возрастают; пропуски допустимы, непрерывность не требуется.
- Slow-status `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` обязан совпадать в 4 местах: global status, dedicated slow table, TOC row, full scene section.
- Человекочитаемые даты — `DD.MM.YYYY`.
- `index.html` — viewer, читает `video-prompts.md` и `project-status.json` с `cache: no-store`.
- Legacy `_source/part-*` builder не использовать.

## Canonical locations

1. Google Drive master — authoritative editable source.
2. GitHub root master — public mirror.
3. `project-status.json` — generated status.
4. GitHub Pages — public viewer.
5. Drive `video-prompts.html` — derived backup viewer.
6. ChatGPT Library — backup.
7. Notion Hub — documentation/navigation backup.

## Routine edit protocol

1. fresh-read Drive master;
2. edit same Drive file ID;
3. update TOC/counts/statuses when required;
4. update `SYNC-TRIGGER.txt`;
5. wait for `sync-from-drive.yml`;
6. require `project-status.json` → `health: ok`;
7. require successful Pages deployment;
8. verify public/raw content;
9. report success.

**Routine edit must not manually refresh Library, Drive HTML or Notion unless the user explicitly requests backup/checkpoint or architecture/instructions changed.**

## Manual Drive edit

Если пользователь сам изменил Drive, сначала fetch свежего master и считать его authoritative. Затем trigger normal sync. Не обновлять Library/HTML/Notion только потому, что edit был ручным.

## Full checkpoint protocol

При explicit full-sync обновить/проверить:
- Drive master integrity;
- Drive HTML;
- five canonical instructions;
- Library master/HTML/instructions/site reserve;
- GitHub changed files;
- Actions;
- `project-status.json`;
- Pages;
- Notion Hub + five instruction pages;
- end-to-end public verification.

## Validation invariant

Валидатор проверяет counts, TOC/sections, prompt fences, W-items, slow list и unique/increasing scene IDs. Scene ID gaps допустимы.
