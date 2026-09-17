# Как пользоваться проектом AI Film Prompts — v2

Короткая памятка владельцу проекта.

## Неизменяемые правила v2

- Рабочий master только один: Google Drive `AI Film Prompts Master/video-prompts.md`.
- GitHub — публичное read-only зеркало и источник GitHub Pages.
- Routine sync: свежий Drive master → правка того же файла → `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → validation → GitHub mirror + `project-status.json` → Pages → verification.
- Library, Notion и Drive HTML — резерв/documentation, не обязательны после каждой сцены.
- Полный обход всех зеркал — только по команде **«полная ручная синхронизация всего и везде»**, при backup/checkpoint или изменении архитектуры.
- Scene ID после удаления не перенумеровывать; пропуски нормальны.
- Slow-status `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ` обновляется в четырёх местах: global status, dedicated slow table, TOC, scene section.
- Даты для человека — `DD.MM.YYYY`.
- На сайте `Инструкция для ИИ` и `Для владельца` стоят рядом; монтажный разбор открывается как rendered GitHub Pages HTML.
- `ГОТОВО` — только после проверки workflow/health/Pages для выбранного режима.

## Обычная команда

`Измени сцену N: ... и синхронизируй проект.`

ChatGPT должен сам:
1. прочитать свежий Drive master;
2. изменить только нужную сцену;
3. сохранить тот же файл;
4. обновить `SYNC-TRIGGER.txt`;
5. проверить health и Pages.

## Если ты сам изменил Drive

Напиши: `Я изменил Drive — синхронизируй проект.`

Свежий Drive имеет приоритет; старой копией его не затирать.

## Если Work изменил Drive

Напиши: `Work обновил master — синхронизируй проект.`

## Slow generation

Старт: `Сцена N запущена в медленную генерацию.`

Результат: `Сцена N закончила генерацию: готово / ошибка / нужен новый дубль.`

Редактор обновляет все четыре места slow-status.

## Если ролик готов окончательно

`Удали сцену N из активного master: ролик готов.`

ID остальных сцен не перенумеровывать.

## Когда нужен Work

Work — для многосценового анализа, continuity, film-analysis/backlog и большого аудита. Один небольшой prompt обычно быстрее делать в обычном чате.

## Другие ИИ

Claude/Gemini/DeepSeek/Grok по умолчанию дают review. Передавай им `AI-PROJECT-GUIDE.md`, актуальный raw master и реальные references нужной сцены.

Если ChatGPT недоступен: `Ты временно основной редактор. Прочитай CLAUDE-TAKEOVER-RUNBOOK.md, затем SYNC-RUNBOOK.md, AI-PROJECT-GUIDE.md и свежий Drive master.`

## Полный checkpoint

Команда: `Полная ручная синхронизация всего и везде.`

Тогда обновляются Drive HTML/instructions, Library, GitHub/Pages и Notion; затем выполняется end-to-end check.

## Если всё забылось

1. `NEW-CHAT-HANDOFF.md`.
2. `SYNC-RUNBOOK.md`.
3. `AI-PROJECT-GUIDE.md`.
4. Fresh Drive `video-prompts.md`.
