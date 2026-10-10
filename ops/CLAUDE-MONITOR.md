# Claude monitor — процедура одного цикла (НЕ КАНОН, рабочая инструкция)

Решение владельца 10.10.2026: роль «единого монитора» берёт на себя Claude — ежечасная scheduled task «AI Film — монитор Claude». Задача ChatGPT «AI Film — единый монитор» (`6aac794245e481919ee7155c461cc77e`) выводится из работы: владелец выключает её сам. Канон — Drive; правила — 7 инструкций. Этот файл только описывает шаги. При конфликте побеждает свежий Drive `NEW-CHAT-HANDOFF.md` / `SYNC-RUNBOOK.md`.

## Жёсткие запреты
- Ничего не одобрять, не перезапускать, не удалять и не закрывать сцены. Генерации не запускать. Кредиты Topview не тратить: только read-only инструменты `topview_list_boards`, `topview_list_board_tasks`, `topview_get_board_task`, `topview_get_credit`.
- Время честное: `checked_at` — реальный момент окончания скана. Никогда не сдвигать вперёд.
- Master — только same-ID запись на Drive через компьютер владельца, `J:\Мой диск\AI Film Prompts Master\video-prompts.md`: `device_commit_files` с `expectedMtimeMs`, затем read-back через Drive connector (`download_file_content`, ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`) и сравнение байтов. Никаких v2/copy.
- Один писатель: если за последние 50 мин в `origin/main` есть коммиты автора `virudik` (ChatGPT), этот цикл ничего не пишет, а только отчитывается.
- Не публиковать telemetry, которая расходится с master: validator требует `active Topview scenes == canonical slow`.

## Шаги
1. `cd /home/claude/ai-film-prompts` (если нет — `git clone https://github.com/virudik/ai-film-prompts`), затем `git fetch && git checkout -B work origin/main`. Запомнить `started_at` (UTC, реальное).
2. **Скан Topview.**
   - `topview_list_boards` (`mode=my-boards`, `pageSize=50`).
   - Для каждой доски с задачами — `topview_list_board_tasks` (`mediaType=video`, `pageSize=100`, все страницы; у основной доски `1a6244cf1ae747ef847d949a80d6133c` 4 страницы). Большие ответы сохраняются в файлы tool-results — это нормально.
   - Сводка: `python3 scripts/topview_scan_summary.py . <файлы страниц> --inline-total <число задач из маленьких досок, прочитанных inline>`.
   - Для каждой задачи из `active` — `topview_get_board_task`: точный статус и `estimateInfo` (`queueCount`, `estimatedWaitSeconds`).
   - Время окончания скана = `checked_at`.
3. **Классификация.**
   - `finished_known` — terminal (`success` / `fail`) у прежде активных задач.
   - `unknown_new` — новые задачи. Сцену определить по совпадению промта с fresh master (нормализованное сравнение блока промта, модель, референсы). Совпадение однозначно — задача существующей сцены, тот же Scene ID. Сомнение — ничего не менять и написать владельцу (решение «неоднозначный task↔Scene» — за ним).
   - Задачи не с доски AI Film в `active_tasks` не включать. Если такая задача активна и занимает слот, сообщить владельцу и не публиковать противоречивые счётчики.
4. **Нужно ли менять master.** Slow-набор меняется, если сцена теряет последнюю активную задачу или получает первую.
   - Fresh-read master через Drive connector (base64 → файл), убедиться, что SHA = `project-status.json.canonical_master_sha256` или новее. Если Drive новее зеркала — работать от Drive.
   - `python3 scripts/master_slow_edit.py <fresh> <new> --date DD.MM.YYYY --plan plan.json` (`add` / `finish`, формат в шапке скрипта).
   - Валидация: `python3 scripts/build_project_status.py <new> --output /tmp/ps.json --topview-status-file <будущий topview-status> ...` — нужен `health=ok`.
   - Запись на Drive (см. запреты), ожидание синхронизации Drive (3–8 мин), read-back байт-в-байт. Компьютер недоступен — master не трогать, telemetry не публиковать, цикл = `degraded`.
5. **Публикация.**
   - Собрать `cycle.json` (формат в шапке `scripts/monitor_publish.py`) и выполнить `python3 scripts/monitor_publish.py . cycle.json`. Порядок записи файлов — внутри скрипта, checkpoint последним.
   - Проверки: `python3 -m unittest tests/test_recovery_integration.py` и `python3 scripts/check_public_freshness.py --root .` (допустима только ошибка возраста сертификата 7/7, её чинит шаг 6).
   - Если master менялся — `SYNC-TRIGGER.txt` с ожидаемым SHA.
6. **Сертификат 7/7** — если `instruction-sync-status.checked_at` старше 2 ч.
   - Скачать 7 документов через Drive connector. ID: в `instruction-sync-status.json → files[].drive_file_id`.
   - Убедиться, что зеркала совпадают побайтно.
   - Обновить `checked_at` временем последнего скачивания, `all_match`, `health`. Логика — как в `cert.py` из истории Claude: обновлять только при полном совпадении 7/7. Расхождение — не чинить автоматически, а сообщить; канон правит только отдельный цикл по правилам.
7. **Решения владельца с сайта** (если в Supabase `owner_decisions` есть `status='pending'`). Применить по таблице из handoff (верхний блок 10.10) и поставить `applied` / `result_note`. Действия, требующие master (`scene_not_needed`, `tv_drop_task`), — по тому же циклу шага 4.
8. **Статус цикла** — `python3 scripts/monitor_status.py . --started … --completed <сейчас> --health ok|degraded --phase … [--missing …] --note …`.
9. Коммит одним набором (`git add` нужных файлов, сообщение `Claude monitor: …`), `git pull --rebase`, `git push origin HEAD:main`. Затем проверить CI (sync, integration tests) и `project-status.json` health.
10. **Отчёт владельцу** (`SendUserMessage`) — только если что-то произошло:
   - освободился слот;
   - сцена технически готова;
   - новая задача;
   - неоднозначность;
   - сбой или компьютер недоступен.

   Тихие циклы без изменений — без сообщения.

## Что делает каждая часть системы
- **D3:** `sync-from-drive.yml` открывает issue `monitor-alert`, если `last_scheduled_cycle.completed_at` старше 3 ч, и закрывает её после свежего цикла.
- **Сайт:** чип «Монитор» читает тот же `completed_at`.
