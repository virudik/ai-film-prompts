# AI Film Prompts — Claude Takeover Runbook

Эта инструкция нужна Claude как аварийному/резервному редактору, если ChatGPT временно недоступен. Она рассчитана на восстановление проекта без памяти старых чатов.

## 1. Когда Claude становится редактором

По умолчанию Claude работает **review-only**.

Только если пользователь явно говорит, что ChatGPT недоступен и назначает Claude временным основным редактором, Claude может изменять канонический master в пределах подключённых пользователем разрешений.

При takeover нельзя создавать параллельные `v2`, `final`, `copy`, `final-final`, менять несвязанные сцены или считать память чата источником истины.

## 2. Единственный источник истины

**Google Drive → `AI Film Prompts Master/video-prompts.md` — единственный канонический редактируемый master.**

Постоянные ссылки:
- Drive folder: `https://drive.google.com/drive/folders/1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`
- Drive master: `https://drive.google.com/file/d/1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj/view?usp=drivesdk`
- Viewer: `https://virudik.github.io/ai-film-prompts/`
- Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
- AI guide: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/AI-PROJECT-GUIDE.md`
- ChatGPT runbook: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/SYNC-RUNBOOK.md`
- This runbook: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/CLAUDE-TAKEOVER-RUNBOOK.md`
- Machine status: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/project-status.json`

## 3. Что читать перед работой

Перед **каждой фактической записью** в master:
1. fresh-read Drive `video-prompts.md`;
2. найти целевую сцену и верхний status block;
3. при continuity/story дополнительно открыть `film-analysis.md` и `film-backlog.md`.

После долгого перерыва, при рассинхронизации или изменении сайта/workflow заново прочитать:
1. этот файл;
2. `SYNC-RUNBOOK.md`;
3. `AI-PROJECT-GUIDE.md`;
4. свежий Drive master.

## 4. Упрощённая автоматическая схема

Штатный путь:

**Drive master → `SYNC-TRIGGER.txt` → GitHub Action → validation → GitHub mirror + `project-status.json` → GitHub Pages.**

`project-status.json` автоматически содержит counts, work-items, slow-scenes и health checks. Его нельзя редактировать вручную.

Notion, ChatGPT Library и Drive HTML — резерв/documentation, а не обязательные точки каждой правки сцены.

Если Claude не имеет GitHub write, это не мешает редактировать Drive master: страховочный workflow периодически подтянет Drive. Но для немедленного trigger или изменения `index.html` нужен GitHub write в среде Claude.

## 5. Как изменить сцену

При команде пользователя `измени сцену N ... и синхронизируй проект`:
1. прочитать свежий Drive master;
2. изменить только утверждённый блок;
3. сохранить тот же Drive file ID;
4. одновременно обновить TOC/status/counts, если изменение их затрагивает;
5. если GitHub write доступен — обновить `SYNC-TRIGGER.txt`;
6. проверить `project-status.json` → `health: ok`;
7. проверить успешный Pages deployment и публичную версию.

Если GitHub write недоступен, честно сообщить: Drive изменён, немедленный trigger недоступен; scheduled workflow должен подтянуть изменение. Не заявлять, что Pages уже обновлён, пока это не проверено.

## 6. Инварианты master

При добавлении активной сцены:
- следующий свободный номер;
- строка в верхней таблице;
- полный `## Сцена N` section;
- counts в revision/status block;
- убрать соответствующий W-item, если он стал полноценной сценой;
- не оставлять дубль старой версии;
- A/B-варианты одной смысловой сцены хранить внутри одной сцены.

Когда ролик окончательно принят и промт больше не нужен — удалить его из активного master и TOC.

## 7. Slow-generation protection

Точная видимая надпись:

`⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`

Она должна совпадать в:
- верхнем status block;
- dedicated slow-generation table/block;
- TOC row;
- full scene section.

В TOC сначала название, затем следующей строкой status; без тире и без `⏳` перед названием. Сам status не переносить внутри себя.

Slow-scene нельзя запускать повторно без явного решения пользователя или подтверждённой ошибки прошлого запуска.

## 8. Сайт

`index.html` — только viewer. Он должен:
- dynamically fetch `video-prompts.md`;
- fetch `project-status.json`;
- показывать health/status;
- держать `Инструкция для ИИ` одной строкой;
- держать slow-status целиком;
- открывать `Монтажный разбор фильма` как rendered GitHub Pages HTML: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`.

Сценовый текст не hard-code в HTML.

## 9. Доступы

Наличие этой инструкции не выдаёт Claude OAuth-доступ автоматически.

Если у пользователя в Claude уже подключены тот же Google Drive/Notion, Claude работает в пределах этих прав. Для прямого GitHub write нужен GitHub connector/разрешение внутри Claude.

Не просить и не использовать API keys/PAT, отправленные в чат, если есть нормальный connector/UI способ подключения.

## 10. Notion и резервные копии

Notion `AI Video Prompts — Master Hub` — documentation/navigation hub, не второй master. Не переписывать live counts/timestamp после каждой сцены; оперативный machine status — `project-status.json`.

Library/Drive HTML/Notion обновлять при архитектурных изменениях, крупных milestones или явной просьбе пользователя обновить резервные копии.

## 11. Передача проекта обратно ChatGPT

После временного takeover сообщить:
- какие сцены/Drive files изменены;
- был ли запущен GitHub sync;
- `project-status.json` health;
- проверен ли Pages;
- менялись ли architecture/Notion/backups;
- что осталось недоступно.

Рекомендуемая фраза:

`Claude временно обслуживал проект. Изменены сцены N..., Drive master обновлён, GitHub sync [статус], project-status health [статус], Pages [статус]. Сначала прочитай свежие CLAUDE-TAKEOVER-RUNBOOK.md, SYNC-RUNBOOK.md и Drive video-prompts.md.`

## 12. Восстановление без памяти

Если история полностью потеряна:
1. открыть этот runbook;
2. открыть `SYNC-RUNBOOK.md`;
3. открыть `AI-PROJECT-GUIDE.md`;
4. fresh-read Drive `video-prompts.md`;
5. проверить `project-status.json`/viewer;
6. при сюжетной задаче открыть `film-analysis.md` + `film-backlog.md`;
7. выполнить задачу по протоколу выше.
