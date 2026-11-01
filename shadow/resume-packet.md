# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-01T15:13:27+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Существующий ordinary HH:00 восстановлен и точно перечитан; новая контрольная точка исправляет доказанный hash mismatch, 6/6 слотов проверены; запуск/расход0.
Следующий шаг: Next actual ordinary HH:00 must produce its own run/receipt. On a free slot, reconcile current task IDs and ready priority (currently S48-SEED20-P2), exact inputs/QC, full all-board scan and one Unlimited0 Create under lease/CAS. At full capacity prepare authorized continuity, including S52-R2-P1 only after original archive/QC.

## Контрольная точка

# 01.11.2026 — Продолжай: восстановление часового исполнителя

work_id: TOPVIEW-SLOT-PRIORITY-20261024

Выполнено 2026-11-01T13:11:25Z по «Продолжай», полный приём. Существующий ordinary6ae5e9d563f88191aa6da7c9ba1e05a0 восстановлен в enabled=true; отдельный peek подтвердил неизменность ID, prompt, HH:00 Europe/Moscow и conversation. HH:55 и Relay включены. Новых автоматизаций0. Перед изменением исходная точка сохранена/readback ed2bbfb; ordinary foreground передан новой сессии (epoch3), preferred_executor и route_generation сохранены.

Причина выключения API не раскрыта. Последний ordinary run445b644c-d2cc-8332-b542-c54e01dd47e4 завершён01.11 в08:12:11 МСК; пустой результат требует действия пользователя, пояснения нет. Этот старый флаг не скрыт. После включения нового реального runtime/receipt ещё нет. HH:55 run4051845d-b258-8332-9532-5c1c5639360e от15:59 МСК имеет no_update и не доказывает проверку Topview. Настройка восстановлена; сквозное фоновое исполнение остаётся отдельной проверкой.

Полный read-only scan15:42:45–15:43:16 МСК:14 досок,18 страниц,625 видео,6/6 активных Unlimited0. Активны71,72,61P1,60P1,62P1,59P2. S52-R2-P1 завершилась07:55:25 МСК; S71 task431180d384cc43bebe7afc702e4eb4e6 создана Grok11:29:13, простой3ч33м48с. Новых Create/расходов в ремонте0; submitted/unknown не повторять.

Восстановление исправлено после проверки причины: коммит9b4425f добавил расписание Grok внутрь связанного H1, а recovery не обновил. Исходный отчёт побайтно цел, прежняя recovery сохранена в истории; новая привязка относится к этому проверенному этапу. Восемь источников и15якорей сверены, continue_preflight проходит. Отчёт возможностей Grok прочитан, задача grok-202611010305-capabilities — «Принято»; чужая d37ea54b needs_owner сохранена.

Дальше: проверить собственные run/receipt следующего ordinary HH:00; при свободном слоте первая фактически готовая по свежей priority (сейчас48.2), полный scan/точные входы/QC/замок/CAS/Unlimited0. При6/6 — подготовка разрешённых стыков; S52-R2-P2 требует настоящего окончания завершённой P1 и QC. Включение не подтверждает GUI или Work-квоту; телеметрию продолжает робот, monitor_role=skip.

Доказательства: `reports/ordinary-launcher-recovery-2026-11-01.json`; квитанция приёма `seregius-continue-20261101-ordinary-recovery` в `reports/handoff-receipts.json`. Очередь, master, разрешения, claims и бюджеты сохранены.

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
