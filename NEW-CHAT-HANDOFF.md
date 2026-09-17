# AI Film Prompts — передача управления в новый чат

Дата передачи: **17.09.2026**.

Этот файл нужен на случай, если старый чат достиг лимита длины, пропала память разговора или основной редактор временно недоступен. Новый ChatGPT или Claude должен восстановить проект из файлов, а не из памяти старого чата.

## 1. Краткая аннотация текущей сессии

В этой сессии была собрана и отлажена система хранения и публикации активных AI-видеопромтов для фильма. Главная цель — иметь один канонический мастер, публичный сайт для чтения и резервные инструкции, чтобы проект можно было продолжать без старого чата.

Что сделано в ходе сессии:
- выбран единственный канонический master: Google Drive `AI Film Prompts Master/video-prompts.md`;
- GitHub `virudik/ai-film-prompts` используется как публичное read-only зеркало;
- GitHub Pages публикует сайт `https://virudik.github.io/ai-film-prompts/`;
- сайт динамически читает root `video-prompts.md`, поэтому сцены не хардкодятся в `index.html`;
- создан автоматический workflow `.github/workflows/sync-from-drive.yml`, который каждые 30 минут и по `SYNC-TRIGGER.txt` подтягивает Drive-master, проверяет его и обновляет GitHub + `project-status.json`;
- создан валидатор `scripts/build_project_status.py`;
- создан `SYNC-RUNBOOK.md` для ChatGPT и `CLAUDE-TAKEOVER-RUNBOOK.md` для аварийной подмены;
- Notion используется как хаб и резервная копия инструкций, но не как отдельный master;
- ChatGPT Library — резервное зеркало, но не обязательная точка при каждой мелкой правке;
- монтажный разбор должен открываться на сайте как отрендеренная страница `Seregius_montazhny_razbor.html`, а не через Drive preview;
- для медленной генерации используется единая надпись `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`;
- отображаемые человеку даты должны идти в порядке день → месяц → год, формат `DD.MM.YYYY`;
- обычная синхронизация упрощена до Drive → trigger → automation → GitHub Pages;
- полный ручной обход всех зеркал выполняется только по явной команде пользователя, при backup/checkpoint или изменении архитектуры.

На момент передачи пользователь дополнительно решил, что **«Кашиик — спор на мосту» завершён и больше не нужен в активном master**. Его промт должен быть удалён из активного файла; оставшиеся номера сцен не обязаны перенумеровываться только ради непрерывности ID.

## 2. Источник истины и адреса

### Google Drive — канон
Папка: `AI Film Prompts Master`
Folder ID: `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`

Главный master:
- `video-prompts.md`
- file ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`

Инструкции:
- `SYNC-RUNBOOK.md` — `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `AI-PROJECT-GUIDE.md` — `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `USER-GUIDE.md` — `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` — `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `CLAUDE-TAKEOVER-RUNBOOK.md` — `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`

Контекст фильма:
- `film-analysis.md` — `1O3bsGGivBktRSbeg-9JWeMLK4J_JYu0M`
- `film-backlog.md` — `1YixC7zQFY7z3Bn1XGXxeQIMema3inCT9`
- `Seregius_montazhny_razbor.html` — `1SVXdiYVrBuEw0Zogo-gLZ2pdym2P3GYw`

### GitHub / сайт
Repository: `virudik/ai-film-prompts`
Viewer: `https://virudik.github.io/ai-film-prompts/`
Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
Rendered montage review: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`

### Notion
Hub: `AI Video Prompts — Master Hub`
Page ID: `3ddfe763-7762-81c0-b8fd-e7c61895df4a`

Notion хранит ссылки, статус контрольной точки и полные копии инструкций. Master-промты в Notion отдельно не редактировать.

## 3. Что читать в новом чате

Новый основной редактор обязан читать в таком порядке:
1. `SYNC-RUNBOOK.md`;
2. `AI-PROJECT-GUIDE.md`;
3. свежий `video-prompts.md` с Google Drive;
4. при сюжетной/монтажной задаче — `film-analysis.md` и `film-backlog.md`;
5. для глубокого монтажа — `Seregius_montazhny_razbor.html`, `EDIT_PLAN_V2.csv`, `PROGRESS.md` при необходимости.

Не опираться на память старого чата, если она расходится с Drive.

## 4. Как теперь обслуживается master

Обычная команда пользователя вида:
`Добавь/измени/удали сцену N и синхронизируй проект.`

Штатный путь:
1. заново прочитать свежий Drive `video-prompts.md`;
2. изменить только нужную сцену/статус;
3. проверить TOC и полноценные `## Сцена N` секции;
4. проверить counts, prompt fences, work-items и slow-generation status;
5. записать изменения в тот же Drive file ID;
6. обновить GitHub `SYNC-TRIGGER.txt`;
7. дождаться успешного `sync-from-drive.yml`;
8. проверить `project-status.json` и GitHub Pages;
9. только после этого написать пользователю `ГОТОВО`.

### Что делает автоматика
`sync-from-drive.yml`:
- скачивает Drive master;
- валидирует структуру;
- генерирует `project-status.json`;
- обновляет GitHub root `video-prompts.md`;
- GitHub Pages автоматически публикует сайт;
- кроме ручного trigger, workflow выполняет страховочную проверку каждые 30 минут.

### Что НЕ надо делать после каждой мелкой правки
Не нужно каждый раз вручную переписывать:
- ChatGPT Library;
- Notion;
- Drive `video-prompts.html`;
- все пять инструкций.

Их обновлять при:
- явной команде `полная ручная синхронизация всего и везде`;
- backup/checkpoint;
- изменении архитектуры/инструкций;
- восстановлении после рассинхронизации.

## 5. Полная ручная контрольная синхронизация

При явной команде пользователя `полная ручная синхронизация всего и везде`:
1. fresh-read Drive master;
2. правка Drive master;
3. проверка целостности;
4. обновление Drive `video-prompts.html`;
5. обновление Drive-инструкций, если они менялись;
6. обновление ChatGPT Library master/HTML/instructions;
7. обновление GitHub изменённых файлов;
8. запуск/trigger автоматического workflow;
9. проверка GitHub Actions success;
10. проверка GitHub Pages success;
11. обновление Notion Hub и копий инструкций;
12. end-to-end проверка публичного сайта и raw master;
13. финальный ответ только в форме `ГОТОВО — ...`, либо `НЕ ГОТОВО — осталось ...`.

## 6. Медленная генерация

Точная надпись: `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`.

Она должна совпадать во всех местах master:
- общий статусный блок;
- dedicated slow-generation table;
- строка сцены в TOC;
- секция самой сцены.

На сайте в TOC сначала название сцены, затем с новой строки полный статус без тире. Фразу не разрывать внутри себя.

Перед повторным запуском медленной сцены нужна явная ошибка/готовый результат или отдельное решение пользователя.

## 7. Правила сайта

`index.html` — только viewer, не master.

Обязательные UI-правила:
- `Инструкция для ИИ` и `Для владельца` находятся рядом в двух половинных кнопках;
- `Монтажный разбор фильма` ведёт на `Seregius_montazhny_razbor.html` внутри GitHub Pages;
- `Claude backup / takeover` ведёт на `CLAUDE-TAKEOVER-RUNBOOK.md`;
- сайт читает `video-prompts.md` с `cache: no-store`;
- верхний статус берётся из generated `project-status.json`;
- человекочитаемые даты выводятся день → месяц → год.

## 8. Правила создания и правки промтов

- Пользователь предпочитает отдельные сцены и готовый production prompt.
- Для Seedance/Veo/Kling/Wan промты обычно на английском; русские реплики оставлять по-русски.
- Консистентность персонажей, одежды, света, окружения и направления камеры обязательна.
- Камера: физически стабильное cinematic motion, controlled inertia, без random jitter/micro-shake.
- Пространство единое; геометрия не должна внезапно появляться.
- Если continuous take — не смешивать его с hard cuts/shot-reverse-shot/inserts.
- Модель-лист персонажа имеет приоритет для внешности/одежды; environment/group refs вторичны.
- Не менять значения `@image1`, `@video1` между сценами без явного указания.
- После успешной генерации и закрытия сцены удалить её из активного master, если промт больше не нужен.
- Не создавать `v2`, `final-final`, `copy` и параллельные masters.

## 9. Claude как аварийный основной редактор

Если ChatGPT недоступен, пользователь может прямо назначить Claude временным главным редактором. Тогда Claude сначала читает `CLAUDE-TAKEOVER-RUNBOOK.md`, затем `SYNC-RUNBOOK.md`, свежий Drive master и выполняет тот же протокол.

Если у Claude подключён тот же Google Drive — он может менять master с разрешения пользователя. Если GitHub-write недоступен, Drive master всё равно может попасть в GitHub через существующий Drive→GitHub workflow.

## 10. Готовый промпт для нового ChatGPT

Скопировать целиком в новый чат:

> Мы продолжаем проект AI-фильма из предыдущего чата. Старый чат достиг лимита длины. Не пытайся восстанавливать проект по памяти или догадкам. Сначала открой и прочитай `SYNC-RUNBOOK.md`, затем `AI-PROJECT-GUIDE.md`, затем самую свежую версию `video-prompts.md` из Google Drive папки `AI Film Prompts Master`. Для сюжетного контекста при необходимости используй `film-analysis.md` и `film-backlog.md`. Канонический master только один — Drive `video-prompts.md`; не создавай v2/final/copy. Обычные правки синхронизируются по упрощённой схеме Drive → `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → GitHub root → `project-status.json` → GitHub Pages. Library/Notion/Drive HTML обновляй вручную только при explicit backup/checkpoint, изменении инструкций или моей команде «полная ручная синхронизация всего и везде». Перед каждой записью fresh-read Drive master. Перед `ГОТОВО` проверяй health/workflow/Pages. Человекочитаемые даты — DD.MM.YYYY. Статус медленной генерации — точная фраза `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`. На сайте `Инструкция для ИИ` и `Для владельца` должны быть рядом в двух половинных кнопках; монтажный разбор открывается как GitHub Pages HTML. Сцена «Кашиик — спор на мосту» уже завершена и должна отсутствовать из активного master. После чтения файлов коротко сообщи мне текущие counts, список медленных сцен и что система готова к продолжению, ничего не меняя без моей команды.

## 11. Готовый промпт для Claude при takeover

> ChatGPT сейчас недоступен. Ты временно основной редактор проекта с моего разрешения. Сначала прочитай `CLAUDE-TAKEOVER-RUNBOOK.md`, затем `SYNC-RUNBOOK.md`, `AI-PROJECT-GUIDE.md` и свежий Drive `video-prompts.md`. Работай только с каноническим master и по takeover-протоколу. Обычные prompt-изменения делай через Drive master и существующую Drive→GitHub автоматику. Полный ручной backup во все зеркала делай только по моей явной команде. Не создавай параллельных master-файлов и не заявляй `ГОТОВО`, пока не проверен фактический результат синхронизации.
