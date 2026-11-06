# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-06T11:36:56+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Принята Work-смена epoch4;6/6 и15submittedIDs подтверждены; HH:55 восстановлен, Relay refreshed,3prompts точно перечитаны, оба маршрута робота сохранены.
Следующий шаг: При6/6 готовить существующие реальные стыки: закончить непрерывный просмотр S52-R2-P1→P2 со звуком, затем подготовить S60-P2/S61-P2 из проверенных архивных оригиналов. При настоящем свободном слоте — fresh main/owner decisions, полный all-board scan, claims/task IDs, первая фактически готовая разрешённая сцена по priority (сейчас S49B1.21), собственная lease/CAS и UI Unlimited0. Сохранённые submittedIDs не повторять; S59-P3/S62-P2 ждут решений по QC.

## Контрольная точка

# 06.11.2026 — приём Work, сверка доставки робота и восстановление продолжения

work_id: TOPVIEW-SLOT-PRIORITY-20261024

- Прямое поручение владельца: принять смену, параллельно продолжать Keep и работу хендофа/Topview; робот должен уведомлять ChatGPT также, сохранив Grok. Keep ведётся отдельной контрольной точкой; личные заметки в канон фильма не копируются.
- Полный приём: 7 инструкций, CONTINUE-PROTOCOL и весь master прочитаны совместно; master SHA 8ad272ade568b6cd13f946a61bf5d0bfcfb12259fcdb34620207c757020facf9. Исходная ошибка recovery: текущий next_action от06.11 расходился с привязанным next_action от04.11; обновление выполнено по фактическому сегодняшнему скану.
- Полный read-only scan: 14 досок, 18 страниц, 630 уникальных видео (601 success,6 init,23 fail),6/6 слотов. Все15submitted ID найдены; claimed/submitting/unknown=0. Новых Create/claim/расходов=0.
- Робот уже имеет два маршрута: assigned GitHub issue для Grok и Relay DM chatgpt@cloud-239644772681871360. Настоящее событие S72/issue372 обработано ChatGPT06.11 05:55UTC; завершённый дубль не повторяется. Доставка именно в этот интерактивный чат отдельно не подтверждена.
- HH:55 восстановлен (тот же ID6acae6ab…), существующий Relay6adc585e… обновлён с тем же relay.message; ordinaryHH:00 сохранён. Точные prompt/schedule/enablement перечитаны. Во все3 существующих задания добавлено соблюдение атомарного recovery-capture; исходные инструкции сохранены. Одна активная Relay-подписка; новый фоновый цикл после восстановления пока не наблюдался. Робот primary; monitor_role=skip, телеметрия не подменялась.
- Собственная Work-смена session work-continue-bd1397c6-535b-4ed1-8d8f-771cb7efd03d, epoch4, route_generation3; preferred_executor не изменён. Actual chat ID инструментами не раскрыт.
- Доказательства: reports/work-continue-2026-11-06.json.

Следующий шаг: При6/6 готовить существующие реальные стыки: закончить непрерывный просмотр S52-R2-P1→P2 со звуком, затем подготовить S60-P2/S61-P2 из проверенных архивных оригиналов. При настоящем свободном слоте — fresh main/owner decisions, полный all-board scan, claims/task IDs, первая фактически готовая разрешённая сцена по priority (сейчас S49B1.21), собственная lease/CAS и UI Unlimited0. Сохранённые submittedIDs не повторять; S59-P3/S62-P2 ждут решений по QC.

checked_at: 2026-11-06T11:26:41+00:00

<!-- relay-current-start -->
Текущий Relay: 2026-11-06T05:55:16.981Z, issue #372, result:22dbd25cdd9f47cd9e44300e55f5e44f; no_update. Полный скан 14 досок / 20 страниц / 1014 задач: 6/6 видео-слотов заняты. S72 success, S49A 101221814fd5430697f697f95a3f4252 init/Unlimited0; 15 submitted IDs сверены. Новых Create/claim: 0. Следующий шаг: наблюдать существующие задачи, повторить полный скан при следующем wake/hourly.
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

- `ops/LAUNCHER-COORDINATION.md`
- `ops/TOPVIEW-EVENT-WAKE.md`
- `ops/topview-launch-queue.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 54

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
