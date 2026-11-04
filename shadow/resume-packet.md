# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-04T07:00:30+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: 08:55 MSK: complete Topview scan 6/6, 627 videos; all 12 submitted IDs found, no unresolved claims, no Create/retry/spend. Queue/readiness hashes match. Ordinary last_run/latest_result/finished receipt match.
Следующий шаг: При следующем настоящем освобождении слота: fresh main, owner decisions, полный all-board scan и сверка claims/task IDs; первая независимая готовая S63-WAN30 (0.8) под собственной lease/CAS и видимым Unlimited0. S52-P2 требует непрерывной проверки видео со звуком; S59-P3 и S62-P2 ждут решения по стыку. S56-P2 не повторять.

## Контрольная точка

# 04.11.2026 — Продолжай: Work принял очередь, 6/6 слотов

work_id: TOPVIEW-SLOT-PRIORITY-20261024

- По прямому «Продолжай» принят существующий фокус; короткий приём D7 прошёл: 8 точных источников, 15 якорей, checkpoint/evidence согласованы. Новый Work session_id `work-continue-49196c1c-8dae-4af0-95c0-127b4003163a`; реальный ID чата среда не раскрывает.
- Фактический первый шаг: полный Topview scan завершён 2026-11-03T21:46:33.084Z (04.11, 00:46 МСК): 14 досок, 18 страниц, 627 видео; 598 success, 6 init, 23 fail. Все 6/6 физических слотов заняты прежними задачами: 56 P2, 48 P2, 71, 72, 61 P1, 60 P1. Все Unlimited0, 720p, 16:9.
- Все 14 submitted task IDs найдены; claimed/submitting/submission_unknown нет. Следующий независимый готовый пункт — S63-WAN30, priority 0.8. Новых запусков, retries, списаний и изменений очереди нет.
- Owner inbox: open/taken 0; новых pending/in_progress owner_decisions нет, отдельная Grok needs_owner сохранена. Оба часовых задания включены; фактические last_run.id совпали с соответствующими каноническими квитанциями. Расписания, роли, route_generation=3 и телеметрия не менялись.
- Стыки S52-P2, S59-P3, S62-P2 остаются заблокированы по прежним доказательствам; новый QC/прослушивание не заявляются. GUI/квота этой среды в текущем приёме не проверялись: свободного слота нет.
- Доказательства: `reports/work-continue-2026-11-04-49196c1c.json`; квитанция `continue-work-20261104-49196c1c` в `reports/handoff-receipts.json`.
- Следующий шаг: При следующем настоящем освобождении слота: свежий main, решения владельца, полный скан и сверка отправок; первая независимая готовая S63-WAN30 (0.8) под собственной lease/CAS и видимым Unlimited0. S52-P2 требует непрерывной проверки видео со звуком; S59-P3 и S62-P2 ждут решения по стыку. S56-P2 повторно не отправлять.

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
Задач с сохранённым task ID: 51

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
