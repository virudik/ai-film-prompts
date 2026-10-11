# reports/ — отчёты Claude Code (облачная сессия 11.10.2026)

Это **не канон и не телеметрия**. Здесь лежат только новые файлы-отчёты; `video-prompts.md`, 7 инструкций, `NEW-CHAT-HANDOFF.md`, `topview-*.json`, `review-ledger.json`, `project-status.json`, `automation-monitor-status.json`, `monitor-role.json` в этой сессии **не менялись** (писатель канона — ChatGPT, `monitor-role.json`). Автор: Claude Code; технический success Topview ≠ approval; в Topview ничего не запускалось, ключи не запрашивались.

| Файл | Что внутри | Кому |
|---|---|---|
| [`topview-unknown-mapping-2026-10-11.md`](topview-unknown-mapping-2026-10-11.md) | Сопоставление 6 новых задач Wan 3.0 (05:09–05:13Z 11.10) со сценами: предварительно по 200-символьным заголовкам (21, 24, 25, 27 — высокая уверенность; две задачи — из 30/31/32), как получить точный ответ одним запуском workflow, что применить писателю | ChatGPT, владелец |
| [`prompt-audit-2026-10.md`](prompt-audit-2026-10.md) | Аудит всех 51 промтов по `PROMPT-STYLE-GUIDE`: таблица сцена → оценка → находки → предложенные diff (текстом, не применены), стыки соседних сцен, топ-10 исправлений | ChatGPT (механические правки), владелец (решения) |
| [`references-audit-2026-10.md`](references-audit-2026-10.md) | Сверка `character-references.json` и манифестов `references/scenes/*` с master: что исправлено, что спорно, файлы вне манифестов, входы вне репозитория | ChatGPT |
| [`montage-plan-v3-draft.md`](montage-plan-v3-draft.md) | Черновик монтажного плана v3 для владельца: порядок сцен, что уже есть, дыры сюжета, хронометраж, приоритет следующих генераций, решения D1–D11 с вариантами | владелец |
| [`prompt-drafts-2026-10.md`](prompt-drafts-2026-10.md) | **Только предложения:** автономные черновики v2 для Scenes 35–38 (с пометками `[ВЫБОР]` на творческих развилках) и каркасы для сцен, которых ещё нет в master (исход дуэли, стык 25→26, активация комплекта, захват на Татуине, вариант разделения 37) | владелец, затем писатель канона |
| [`tools/prompt_lint.py`](tools/prompt_lint.py) | Read-only эвристическая проверка структуры промтов master (ничего не пишет); вывод — зацепки для человека | справочно |

## Что изменено вне `reports/` (отдельные небольшие коммиты в ветке `claude/adoring-wright-hkj8va`)

| Что | Файлы | Зачем |
|---|---|---|
| Скрипт и workflow сопоставления промтов Topview (только `GET`, только аннотация) | `scripts/topview_prompt_match.py`, `.github/workflows/topview-prompt-match.yml`, `tests/test_topview_prompt_match.py`, `.github/workflows/test-recovery-integration.yml` (добавлен тест) | пункт 1; **запуск возможен после попадания файлов в `main`** (GitHub запускает `workflow_dispatch` только из default-ветки) |
| Реестр персонажей | `character-references.json` (`id` для Лучика/Рыжика; алиас «Лёха») | пункт 3, детерминированно |
| Манифесты референсов | `references/scenes/scene-35…38/manifest.json` (новые), `references/scenes/scene-20/manifest.json` (привязки частей 12–13) | пункт 3, детерминированно |

Проверки: `python3 -m unittest discover -s tests` — OK (93 теста); `python3 scripts/validate_site.py .` — site contract ok.

## Что решает не Claude

Всё, что в отчётах помечено «решение владельца» (D1–D11 в плане v3; топ-10 п. 1 и раздел 6 аудита). Принятие правок master и применение сопоставления Topview — за писателем канона по `monitor_role.py`.
