# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-06T12:45:48+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Опубликованы и побайтно проверены материалы S60/S61 и RESOURCE, параллельные правила и хендоф; 475 тестов и серверные проверки прошли. Keep v46: 15 прочитано, 12 изменено, остаток442. Новое поручение RESOURCE/HONOR/Саша передано проектному продолжению.
Следующий шаг: Слоты: при настоящем освобождении выполнить свежий полный preflight и первый готовый разрешённый item по priority (S49B), не повторять submitted. Стыки S52/S60/S61 уже сохранены, остаётся непрерывный визуальный просмотр со звуком перед READY. Keep продолжать по приватному checkpoint v46: добавлять подтверждённые темы, сохранять прежние ярлыки, исключённые записи о фильме не обрабатывать. Новая доработка RESOURCE/HONOR и руководство Саше продолжаются по проектному checkpoint Разного; 8 новых поддоменов HTTPS остаются неподтверждёнными.

## Контрольная точка

# 06.11.2026 — продолжение связанного Work-чата и сохранение стыков

work_id: TOPVIEW-SLOT-PRIORITY-20261024

- Приём D7 и последующее полное командное чтение 7 инструкций; foreground Work epoch 5. Shared-чат прочитан, исходный checkpoint опубликован bd2426592.
- Свежий полный scan 14 досок / 18 страниц / 630 видео: 6/6, 15 submitted сверены, unknown 0, Create 0. Монитор skip, робот остаётся писателем телеметрии.
- Реальный HH:55 после включения завершён 06.11 в 12:01 UTC (run 5875bfa9…);6/6, blocked_lock/receipt_not_saved. Причина прежнего выключения в доступных данных не записана.
- S60/S61: сохранены настоящие последние 3 с в существующем Drive и проверенные final PNG / provenance / manifests в этой транзакции. Decode/SHA/pixel-match прошли. Полного просмотра со звуком нет, READY/очередь не менялись.
- Параллельный порядок Keep/Серёгиус/сайты закреплён в AI-PROJECT-GUIDE; Keep добавлен P-14. Хендоф сокращён ниже 35000 байт с сохранением истории.
- Рудик.рф: кнопка поднята,13 страниц, включая test, проверены; bc875408 и Pages 42216017874 success. Root/www/промты/ии HTTPS 200; 8 новых поддоменов HTTPS не подтверждён.
- Разное: RESOURCE metadata 19/114 согласованы с 8 версиями v2; HONOR аудит сохранён, способ озвучки только предложен, генераций 0.
- Keep: вход восстановлен; полностью прочитаны 15 заметок, 12 изменены и проверены. Приватный checkpoint v46 сохранён и перечитан. «На проверку» — 442; известна минимум одна заметка без ярлыков. Автоматическая проверка отклонила снятие служебного ярлыка и обработку исключённой записи о фильме; обходов нет. Личные сведения и содержимое заметок в канон не переносились.
- Публикация: bd80507f9, все 28 файлов перечитаны без расхождений; 475 локальных тестов и серверные integration/Projects/canon-health прошли. Pages 42218580707 success, пять файлов проверены побайтно по публичному HTTPS.
- Новое поручение владельца: доработать RESOURCE и HONOR с референсами последнего телефона, проверить предупреждение сайта, дать Саше руководство на Диске. Продолжение ведётся в проектном checkpoint Разного; основной слотный focus сохраняется.
- Доказательства и текущие результаты проверок: reports/work-continue-linked-chat-2026-11-06.json.

Следующий шаг: Слоты: при настоящем освобождении выполнить свежий полный preflight и первый готовый разрешённый item по priority (S49B), не повторять submitted. Стыки S52/S60/S61 уже сохранены, остаётся непрерывный визуальный просмотр со звуком перед READY. Keep продолжать по приватному checkpoint v46: добавлять подтверждённые темы, сохранять прежние ярлыки, исключённые записи о фильме не обрабатывать. Новая доработка RESOURCE/HONOR и руководство Саше продолжаются по проектному checkpoint Разного; 8 новых поддоменов HTTPS остаются неподтверждёнными.

checked_at: 2026-11-06T12:45:48+00:00

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

- `ops/TOPVIEW-FREE-LAUNCH.md`
- `projects/raznoe/HANDOFF.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 54

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
