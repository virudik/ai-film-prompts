# Как пользоваться проектом AI Film Prompts — v3.5

Короткая памятка владельцу проекта. Полные технические правила находятся в `SYNC-RUNBOOK.md`.

## Самое главное

- Рабочий prompt master только один: Google Drive `AI Film Prompts Master/video-prompts.md`.
- GitHub — зеркало и сайт, не место, где вручную ведётся второй master.
- Пять Drive-инструкций также считаются каноническими для своих GitHub-копий.
- `project-status.json` генерируется автоматически; вручную его не править.
- Slow-сцену нельзя запускать повторно, пока нет результата/ошибки или отдельного разрешения.

Обычно достаточно написать:
`Измени сцену N: ... и синхронизируй проект.`

ChatGPT должен сам:
1. прочитать свежий Drive master;
2. изменить только нужную сцену;
3. сохранить тот же файл;
4. запустить sync через `SYNC-TRIGGER.txt`;
5. проверить Actions, `project-status.json` и Pages.

## Что появилось в v3.5

`project-status.json` теперь schema v3 и содержит:
- SHA-256 актуального master;
- `audit_fingerprint`;
- машинный `render_state`;
- optional `scene_meta`;
- `instruction_sync`.

Для slow-сцен `render_state = SLOW_PENDING` вычисляется автоматически из уже существующего slow-list. Отдельно вручную его заполнять не нужно.

Пока приватные Drive-инструкции не проверяются GitHub Actions через authenticated access, `instruction_sync.health = unverified` — нормальная честная отметка. Она не означает, что prompt master сломан.

## Если ты сам изменил Drive

Напиши:
`Я изменил Drive — синхронизируй проект.`

Свежий Drive имеет приоритет; старой копией его не затирать.

## Если Work изменил Drive

Напиши:
`Work обновил master — синхронизируй проект.`

## Если сцена ушла в slow generation

Напиши:
`Сцена N запущена в медленную генерацию.`

После результата:
`Сцена N закончила генерацию: готово / ошибка / нужен новый дубль.`

Редактор обновляет четыре существующих места slow-status в master. Machine `render_state` пересчитается автоматически.

## Если ролик готов окончательно

Напиши:
`Удали сцену N из активного master: ролик готов.`

ID остальных сцен не перенумеровывать.

## Если нужно понять, свежий ли контекст у другого ИИ

Попроси его перед аудитом повторить `audit_fingerprint` из `project-status.json`: revision, master hash, scene IDs, slow list, W-items и health.

Если fingerprint не совпадает — сначала обновить материалы, потом слушать рекомендации.

## Когда нужен Work

Work — для многосценового анализа, continuity, film-analysis/backlog и большого аудита. Один небольшой prompt обычно быстрее делать в обычном чате.

## Другие ИИ

Claude/Gemini/DeepSeek/Grok по умолчанию дают review. Передавай им `AI-PROJECT-GUIDE.md`, актуальный master/status и реальные references нужной сцены.

Если ChatGPT недоступен и нужно временно дать запись Claude:
`Ты временно основной редактор. Прочитай CLAUDE-TAKEOVER-RUNBOOK.md, затем SYNC-RUNBOOK.md, AI-PROJECT-GUIDE.md и свежий Drive master.`

Claude сначала должен проверить, способен ли его Drive-инструмент **заменять содержимое существующего файла по тому же ID**. Если нет — он остаётся review/patch-only и не создаёт новый master.

## Полный checkpoint

Для обновления резервов и инструкций скажи:
`Полная ручная синхронизация всего и везде.`

Это нужно после архитектурных/инструкционных изменений, milestone или когда хочешь обновить все резервные слои.

## Если всё забылось

1. Открыть `NEW-CHAT-HANDOFF.md`.
2. Открыть `SYNC-RUNBOOK.md`.
3. Открыть `AI-PROJECT-GUIDE.md`.
4. Открыть свежий Drive `video-prompts.md`.
5. Проверить `project-status.json` fingerprint.
