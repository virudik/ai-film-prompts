# Облачная сессия №2 — большие расчётные работы по проекту (НЕ КАНОН)

**Зачем:** бонус облачных сессий Claude Code (100 $ до 5 ноября) не тратит лимит подписки; недельный лимит Claude почти исчерпан до пт 16.10. Работа в основном аналитическая: сессия пишет отчёты и предложения, а master не правит (сейчас писатель — ChatGPT, решение владельца 11.10 13:59).

**Как запустить:** claude.ai/code → новая сессия → репозиторий `virudik/ai-film-prompts`, `main` → вставить текст ниже. Не одновременно с другой большой сессией.

---

```text
Проект «AI Film Серёгиус». Канон — этот репозиторий, ветка main. Прочитай CLAUDE.md, верхние блоки NEW-CHAT-HANDOFF.md, PROMPT-STYLE-GUIDE.md целиком, video-prompts.md, film-analysis.md, film-backlog.md, character-references.json, review-ledger.json, topview-task-map.json, shadow/topview-robot-status.json, references/ (manifest.json сцен).

ВАЖНО: сейчас единственный писатель канона и телеметрии — ChatGPT (monitor-role.json). Ты НЕ правишь video-prompts.md, 7 инструкций и файлы телеметрии (topview-*.json, review-ledger.json, project-status.json, automation-monitor-status.json, monitor-role.json). Пишешь только новые файлы в reports/ и (пункт 3) данные реестров. Технический success Topview ≠ approval. Ничего в Topview не запускать. Ключи не просить.

1. СОПОСТАВЛЕНИЕ НОВЫХ ЗАДАЧ TOPVIEW. Сканер робота нашёл 6 новых задач Wan 3.0 (05:09–05:13 UTC 11.10, unknown_new). Через публичный API (секрет TOPVIEW_API_KEY, переменная TOPVIEW_UID; GET https://api.topview.ai/boards/tasks/list?boardId=1a6244cf1ae747ef847d949a80d6133c&mediaType=video&sortField=gmtCreate&sortOrder=desc) — это можно сделать только из GitHub Actions; если из сессии сеть до API недоступна, напиши маленький workflow_dispatch-скрипт, который сравнивает parameters.positivePrompt этих задач с промтами master по точному/нормализованному совпадению и печатает в аннотацию только: task_id → Scene/часть (например 28 B1) + степень уверенности. Итог — reports/topview-unknown-mapping-2026-10-11.md. Сцены НЕ создавать и telemetry не писать: ChatGPT применит по отчёту.

2. АУДИТ ВСЕХ ПРОМТОВ ПО PROMPT-STYLE-GUIDE. Для каждой активной сцены и каждого копируемого промта: автономность (identity lock, роли и приоритет референсов, камера/пространство, таймлайн, native audio, негативы, FRAME FILL), соответствие длительности/модели, ссылки на существующие файлы референсов, continuity со смежными сценами (граничные кадры), повторы и противоречия. Итог — reports/prompt-audit-2026-10.md: таблица сцена → оценка → конкретные находки → предложенный diff (как текст, НЕ применять). Отдельно — топ-10 самых важных исправлений.

3. РЕЕСТР ПЕРСОНАЖЕЙ И МАНИФЕСТЫ РЕФЕРЕНСОВ. Сверить character-references.json с активными сценами master (известно: не хватает сцен 35–38) и manifest.json сцен с полями, требуемыми хендофом (identity_refs, location_refs, prop_refs, start_frame, end_frame, pose_composition_helpers, approved, rejected, topview_source_provenance, prompt_reference_order). Исправить только детерминированное (отсутствующие сцены/поля, битые пути) отдельными небольшими коммитами; всё спорное — списком в reports/references-audit-2026-10.md. Проверить, что все файлы, на которые ссылаются промты, реально лежат в references/.

4. МОНТАЖНЫЙ ПЛАН v3 (черновик для владельца). По film-analysis.md, film-backlog.md, review-ledger.json (в фильме / в монтаж / принято), master и монтажному разбору v2 (claude/montage-report-v2 есть в Claude Project; в репозитории — Seregius_montazhny_razbor*.html, publish-montage-report.yml): порядок сцен, что уже есть, чего не хватает для связного фильма, дыры в сюжете, приоритет следующих генераций (сначала сцены, закрывающие сюжет). Итог — reports/montage-plan-v3-draft.md. Творческие решения не принимать — только варианты для владельца.

5. ПРОВЕРКИ: python3 -m unittest discover -s tests; python3 scripts/validate_site.py . Коммиты небольшими шагами, git pull --rebase перед push; отклонённый push — перечитать и повторить. В верхний блок NEW-CHAT-HANDOFF.md НЕ писать (писатель — ChatGPT); вместо этого — reports/README.md со списком отчётов. В конце — короткий отчёт владельцу по-русски: что найдено главного, что требует его решения, что передать ChatGPT.
```
