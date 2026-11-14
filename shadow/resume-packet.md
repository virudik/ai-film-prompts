# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-14T20:04:15+00:00
Задача: SEREGIUS-SHIFT-20261113-T611U — Смена 13.11 t611u: очередь 48.4 и 89, отзыв по версиям Grok

Последний подтверждённый этап: Work выполнил короткий D7: 15/15 правил и SHA источников совпали. Полный read-only скан 14 досок/675 видеозадач в 19:59:04Z: 5/6 занято. Следующий S89A-WAN30; новых claim/intent/Create нет. Существующая часовая страховка снова включена и перечитана через Automations.
Следующий шаг: Восстановить вход Topview в открытой вкладке встроенного браузера этого Work-чата. Затем новый полный скан всех досок, свежий main/lease и проверка дублей; для S89A-WAN30 скачать точные пять исходников, сверить SHA/master и Unlimited/720p/16:9/quantity1/0 credits, CAS-claim/intent/readback и один Create. Продолжать по живой очереди при свободных слотах. Уже submitted S48-P4-R2 и S51E/F/G не повторять. Проверить следующий реальный цикл возобновлённой HH:55 страховки; enabled не доказывает вход или запуск.

## Контрольная точка

# 14.11.2026 — Work: очередь проверена, запуск ожидает входа Topview

work_id: SEREGIUS-SHIFT-20261113-T611U

- Команда владельца: «Продолжай. Запускай по согласованной очереди». Приём короткий D7; fresh main dbfceb4042d0c9caea4b9e53ae77336b4e6ad6f5, ready_for_short=true, ready_for_resume=true, 15/15 правил.
- Последний подтверждённый этап: Work выполнил короткий D7: 15/15 правил и SHA источников совпали. Полный read-only скан 14 досок/675 видеозадач в 19:59:04Z: 5/6 занято. Следующий S89A-WAN30; новых claim/intent/Create нет. Существующая часовая страховка снова включена и перечитана через Automations.
- Проверены live project/instruction/automation/monitor status, canon lock, owner-tasks (открытых нет), Supabase owner_decisions (pending/in_progress нет; историческая needs_owner to:grok не менялась). monitor_role=skip, робот здоров; телеметрия/heartbeat не переписывались.
- Точный результат скана и активные task IDs: reports/topview-queue-2026-10-16/preflight-20261114-work-33406175.json. Все 19 страниц прочитаны, одно физическое свободное место на момент скана.
- Блокер этого Work: сайт Topview показывает «Войти», форма входа остаётся открытой. Browser control доступен, авторизованная форма генерации отсутствует. Защищённый запрос входа сначала вернул locator_invalid, исправленный завершился таймаутом; секреты не читались и не вводились агентом. Claim/intent/Create=0; платный обход не применялся.
- HH:55 6acae6ab433481919e88665c520b8ef2 фактически была disabled. По действующему поручению владельца снова включена 20:01:16Z, Automations.peek подтверждает is_enabled=true, прежнее расписание и prompt сохранены. Возвращаемый next_run_time устарел; будущий успешный запуск не объявляется.
- Foreground Work epoch 6→7 передан этому session_id chatgpt-work-continue-33406175-4e23-4eca-8906-26de4724d255; ordinary/Grok, route_generation=3, очередь, task IDs и retry budgets сохранены.
- Следующий шаг: Восстановить вход Topview в открытой вкладке встроенного браузера этого Work-чата. Затем новый полный скан всех досок, свежий main/lease и проверка дублей; для S89A-WAN30 скачать точные пять исходников, сверить SHA/master и Unlimited/720p/16:9/quantity1/0 credits, CAS-claim/intent/readback и один Create. Продолжать по живой очереди при свободных слотах. Уже submitted S48-P4-R2 и S51E/F/G не повторять. Проверить следующий реальный цикл возобновлённой HH:55 страховки; enabled не доказывает вход или запуск.

checked_at: 2026-11-14T20:02:31+00:00

<!-- relay-current-start -->
Relay #676 · 2026-11-14T19:28:43.268Z · slots:a3e98072:67 · blocked_browser, retryable=true. Полный независимый скан: 14 досок / 19 страниц / 1059 задач, занято 5/6; готов S89A-WAN30. Fresh master raw/normalized SHA совпали, все 5 входов учтены. Подключённый браузер дважды, с повтором примерно через минуту, потребовал исходный контекст; точная загрузка исходников, Wan 3.0 Unlimited0 и цена0 в UI не подтверждены. claim/intent/Create=0. Следующий свежий wake/плановый цикл повторяет доступ и полный preflight. next_action/recovery активной работы сохранены. Квитанция: reports/topview-event-wake.json.
<!-- relay-current-end -->

<!-- relay-current-start -->
Relay #676 · 2026-11-14T19:28:43.268Z · slots:a3e98072:67 · blocked_browser, retryable=true. Полный независимый скан: 14 досок / 19 страниц / 1059 задач, занято 5/6; готов S89A-WAN30. Fresh master raw/normalized SHA совпали, все 5 входов учтены. Подключённый браузер дважды, с повтором примерно через минуту, потребовал исходный контекст; точная загрузка исходников, Wan 3.0 Unlimited0 и цена0 в UI не подтверждены. claim/intent/Create=0. Следующий свежий wake/плановый цикл повторяет доступ и полный preflight. next_action/recovery активной работы сохранены. Квитанция: reports/topview-event-wake.json.
<!-- relay-current-end -->

## Обязательные правила

- Since 11.10.2026: GitHub main = canon (master + 7 docs, status, site); Drive / Notion / Library / Project files = read-only backups; Topview = telemetry; Notion = story. — `NEW-CHAT-HANDOFF.md`
- One master: video-prompts.md in GitHub main; no v2/final/copy. — `AI-PROJECT-GUIDE.md`
- Before any master write: fresh git pull of main; minimal commit → SYNC-TRIGGER → validator health=ok → Pages → verification; rejected push = another writer, redo from scratch. — `NEW-CHAT-HANDOFF.md`
- Instruction edits: fresh pull → minimal commit → scripts/cert_github.py → push → verify; never replay a stale write. — `NEW-CHAT-HANDOFF.md`
- Scene IDs stable; retired IDs never reused; rerender keeps the same Scene ID. — `AI-PROJECT-GUIDE.md`
- Topview technical success ≠ editorial approval; never auto approve/rerun/delete/close. — `SYNC-RUNBOOK.md`
- Slot capacity 6; one active task = one slot; a terminal task frees its slot at once; canonical slow is cleared only by an explicit owner button (11.10.2026), never by a technical terminal. — `SYNC-RUNBOOK.md`
- One writer, decided by monitor-role.json + scripts/monitor_role.py: since 13.10.2026 the GitHub robot (topview-robot.yml → robot_telemetry.py, every 10 min via Supabase pg_cron) is primary, ChatGPT is standby and takes over only after 180 min without a verified healthy robot cycle; the Claude monitor is off; kill switch ROBOT_TELEMETRY=shadow. Old ChatGPT HH:00 monitor and archived Recovery/slot-watcher stay off. — `NEW-CHAT-HANDOFF.md`
- Never fake checked_at/queue/ETA; partial phases keep last confirmed timestamps. — `SYNC-RUNBOOK.md`
- Owner decides only creative/editorial choices, ambiguous task↔Scene mapping, approval, rerender, deletion/closing; deterministic work is done by the agent; never ask for info already in sources. — `AI-PROJECT-GUIDE.md`
- Every copyable prompt is self-contained: identity lock, reference roles/priority, camera/space, timeline, native audio, negatives, FRAME FILL. — `PROMPT-STYLE-GUIDE.md`
- Material workflow/site/authority/recovery change → relevant canonical docs + SAME handoff → cert_github.py certificate → push to main → Notion pointer → backup copies (best-effort). — `SYNC-RUNBOOK.md`
- Agents may launch only owner-authorized queue items via the website in Unlimited mode at zero credits. Paid Topview launches are performed only by the owner. — `SYNC-RUNBOOK.md`
- Library is best-effort, never a completion gate. — `SYNC-RUNBOOK.md`
- Never say «готово» before the relevant read-back/verification passed. — `SYNC-RUNBOOK.md`

## Прочитать под задачу

- `ops/topview-launch-queue.json`
- `ops/TOPVIEW-FREE-LAUNCH.md`
- `reports/current-work-checkpoint.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 90

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
