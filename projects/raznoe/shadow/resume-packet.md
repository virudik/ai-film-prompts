# Продолжай — пакет восстановления: Роскосмос

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project raznoe`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-30T09:23:42+00:00
Задача: RAZNOE-CPK-REFS-20261027 — Роскосмос — референсы ЦПК готовы, проект на паузе

Последний подтверждённый этап: Все10 существующих PNG ЦПК сохранены; в семи локально добавлены официальные эмблемы, флаги и кириллические надписи. SHA и тексты требований обновлены; лица и все пиксели вне областей правок неизменны.
Следующий шаг: Не рисовать готовые референсы заново. Ждать замечаний владельца по семи локальным правкам и отдельного явного разрешения на снятие паузы; сцены21–25 не добавлять в очередь, видео не запускать.

## Контрольная точка

# ЦПК — локальные нашивки и надписи · 28.10.2026

work_id: RAZNOE-CPK-REFS-20261027
Проверено: 2026-10-28T12:55:17+00:00

Все10 существующих PNG ЦПК сохранены; в семи локально добавлены официальные эмблемы, флаги и кириллические надписи. SHA и тексты требований обновлены; лица и все пиксели вне областей правок неизменны.

Отчёт: projects/raznoe/reports/cpk-insignia-edit-2026-10-28.json. Исходные размеры сохранены;0 изменённых пикселей вне масок. Три исключённых владельцем изображения сохранены побайтно.29 элементов очереди остаются на паузе; запусков и новых пунктов0.

Следующее действие: Не рисовать готовые референсы заново. Ждать замечаний владельца по семи локальным правкам и отдельного явного разрешения на снятие паузы; сцены21–25 не добавлять в очередь, видео не запускать.

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

- `projects/raznoe/HANDOFF.md`
- `projects/raznoe/ops/topview-launch-queue.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 0

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
