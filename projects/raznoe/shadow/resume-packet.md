# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project raznoe`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-06T13:25:45+00:00
Задача: RAZNOE-RESOURCE-HONOR-SASHA-20261106 — Доработка RESOURCE/HONOR, референсы Magic9 Pro Max и руководство Саше

Последний подтверждённый этап: Сохранено 2/4 новых референсов RESOURCE с промптами и визуальным QC; PROP-polymer-gripper-mounted-open.png.
Следующий шаг: Завершить точные правки RESOURCE/HONOR и план недостающих кадров; получить официальные изображения Magic9 Pro Max, затем по одному создавать, проверять и сразу сохранять референсы. Подготовить и проверить руководство Саше, загрузить в подтверждённую папку Drive. Видео не запускать.

## Контрольная точка

# 06.11.2026 — доработка RESOURCE/HONOR и руководство Саше

work_id: RAZNOE-RESOURCE-HONOR-SASHA-20261106

- Референсы RESOURCE: 2/4 сохранены с промптами, SHA и визуальным QC; последний PROP-polymer-gripper-mounted-open.png. Новые ролики не запускались.
- Новое прямое поручение владельца получено; улучшения промтов и недостающие референсы разрешены.
- Последний флагман HONOR Magic9 Pro Max подтверждён первичными релизами HONOR и ARRI от 28.09.2026; изображения продукта собираются.
- RESOURCE: выявлена несовместимость жёсткой рамной детали с командами «раскрыть захват»; готовится единая механика без морфа корпуса.
- Папка Саша найдена, содержит существующие MP4; руководство готовится, существующие файлы и доступ сохраняются.
- Предупреждение сайта: фактические health/automation/continue зелёные, жёлтая плашка показывает действующий общий замок.
- Предыдущий этап опубликован bd80507f9 и проверен по HTTPS; новая работа не объявлена завершённой.

Следующий шаг: Завершить точные правки RESOURCE/HONOR и план недостающих кадров; получить официальные изображения Magic9 Pro Max, затем по одному создавать, проверять и сразу сохранять референсы. Подготовить и проверить руководство Саше, загрузить в подтверждённую папку Drive. Видео не запускать.

checked_at: 2026-11-06T12:46:46+00:00

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

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 0

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
