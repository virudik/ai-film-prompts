# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-01T13:05:55+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Полный приём и диагностика выполнены; исходный результат сохранён, подготовлен ручной ремонт ordinary без изменения очереди.
Следующий шаг: Восстановить is_enabled=true только у существующего ordinary HH:00 и перечитать; затем подтвердить настоящий следующий runtime/receipt. S71/S72 уже отправлены. При свободном слоте первая готовая по свежей priority (сейчас48.2); полный scan, точные входы и CAS/Unlimited0 обязательны.

## Контрольная точка

# 01.11.2026 — Продолжай: восстановление часового исполнителя

work_id: TOPVIEW-SLOT-PRIORITY-20261024

Исходная точка до изменения Automations, 2026-11-01T13:05:12Z. Команда владельца «Продолжай»; полный приём. Восемь источников и исходный отчёт проверены по SHA. Сбой восстановления вызван добавлением абзаца расписания Grok в связанный H1 без обновления recovery (коммит 9b4425f); исходное доказательство цело, старая recovery сохранена в истории.

Живой peek: обычное задание 6ae5e9d563f88191aa6da7c9ba1e05a0 выключено, хотя действует HH:00 МСК; HH:55 и Relay включены. Причина отключения не раскрыта. Последний ordinary run 445b644c-d2cc-8332-b542-c54e01dd47e4 завершён 08:12:11 МСК, результат пустой с requires_user_action=true без пояснения. Команды владельца остановить ordinary не найдено. Двухчасовая страховка ранее заменена HH:00, дубль не создаётся.

Полный read-only scan 15:42:45–15:43:16 МСК:14 досок,18 страниц,625 видео,6/6 активных Unlimited0. S71 task431180d384cc43bebe7afc702e4eb4e6 создана Grok в11:29:13 МСК; S52-R2-P1 завершилась07:55:25 МСК, интервал3ч33м48с. S71/S72 не повторять. Телеметрия робота, очередь, master, claims и бюджеты не изменяются.

План: сохранить эту точку и передачу ordinary foreground под точной lease; включить только существующее HH:00, перечитать настройки; записать результат и квитанцию приёма. Включение не доказывает исполнение или браузерный Create. Первый последующий настоящий runtime и его собственный receipt проверяются отдельно. При свободном слоте — живая готовая очередь (сейчас48.2), полный scan и штатный preflight.

Доказательства: `reports/ordinary-launcher-recovery-2026-11-01.json`. Автоматизация этим исходным checkpoint ещё не изменена; новых отправок/расходов0.

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

- `ops/LAUNCHER-COORDINATION.md`
- `ops/slot-backup.json`
- `ops/TOPVIEW-FREE-LAUNCH.md`
- `ops/topview-launch-queue.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 49

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
