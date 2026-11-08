# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-08T15:08:37+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Опубликованы точный порядок6роликов и6проверенных Rutube-плееров. ОСД/ЗВ сохранены наDrive с обратным SHAreadback и удалены только из текущего сайта (161912522B); история сохранена. Сцена5HONORсинхронизирована с правилами90с/безмузыки, заявка не отправлена. Инвентарь13YouTubeID готов; Pages403 блокирует сертификаты. Готовое помечено OK.
Следующий шаг: Сначала живые слоты/очередь и антидубли; при свободном месте только разрешённый READY Unlimited0/CAS. Не повторять A-32/A-21/конкурсную редактуру, инструкцииСаше или визитки. Продолжить A-08 продуктовые PNGHONOR, A-07 RESOURCE и видеостыки QC. A-20 требует административного Pages-доступа; A-31 — авторизованной Студии Rutube/прав; A-09 — настоящий город и согласование участия/реальная съёмка. Keep/Роскосмос на паузе.

## Контрольная точка

# 08.11.2026 — порядок, шесть Rutube-плееров и конкурсный мастер опубликованы

work_id: TOPVIEW-SLOT-PRIORITY-20261024

- Опубликованы точный порядок6роликов и6проверенных Rutube-плееров. ОСД/ЗВ сохранены наDrive с обратным SHAreadback и удалены только из текущего сайта (161912522B); история сохранена. Сцена5HONORсинхронизирована с правилами90с/безмузыки, заявка не отправлена. Инвентарь13YouTubeID готов; Pages403 блокирует сертификаты. Готовое помечено OK.
- Прямая публикация js и мастера проверена по SHA; подробные доказательства и границы: reports/owner-followup-2026-11-08.json.
- Открытые стадии не закрывались: продуктовые PNGHONOR, QCRESOURCE/стыков,8сертификатов, YouTubeимпорт, VKзаявка/съёмка, физическая/художественная приёмка визитки.
- Следующий шаг: Сначала живые слоты/очередь и антидубли; при свободном месте только разрешённый READY Unlimited0/CAS. Не повторять A-32/A-21/конкурсную редактуру, инструкцииСаше или визитки. Продолжить A-08 продуктовые PNGHONOR, A-07 RESOURCE и видеостыки QC. A-20 требует административного Pages-доступа; A-31 — авторизованной Студии Rutube/прав; A-09 — настоящий город и согласование участия/реальная съёмка. Keep/Роскосмос на паузе.

checked_at: 2026-11-08T08:05:31+00:00

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
- `ops/FUTURE-PLANS.md`
- `projects/raznoe/HANDOFF.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 55
- S49B: reconcile_without_resubmitting
- S49D: reconcile_without_resubmitting

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
