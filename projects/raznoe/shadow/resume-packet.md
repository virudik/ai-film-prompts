# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project raznoe`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-06T12:23:49+00:00
Задача: RAZNOE-SCENE3-RESOURCE — Сцена 3 RESOURCE на сайте, без видео

Последний подтверждённый этап: Техническая обвязка RESOURCE согласована с19/114 и8v2 без смены промтов/очереди; HONOR36блоков и3moodPNG разобраны, творческие предложения сохранены.
Следующий шаг: До отправки RESOURCE продолжать художественный motion/audioQC существующих попыток; для HONOR выбрать озвучку и точное изделие по решению владельца. Генерации, приёмка и перерисовка без нового разрешения не выполняются.

## Контрольная точка

# 06.11.2026 — RESOURCE: согласование пакета; HONOR: предложения

work_id: RAZNOE-SCENE3-RESOURCE

Основание: продолжить задания share6aedc24c, включая «посмотри как можно улучшить сцены с Хонор и бутылками».

- Исправлена техническая обвязка RESOURCE по существующим v2: active-cut.json19/114,8v2, START/END C02–C05 и уже раскрытые панели C01. Промты, requests, изображения, очередь и approval не менялись.
- Аудит HONOR36блоков и3moodPNG сохранён:4пропущенные реплики и8глобальных AUDIO окон. Перенос озвучки в общую дорожку — предложение, masterHONOR не менялся.
- Исторический пакет19/116 сохранён; новая карта не является разрешением на отправку.
- Доказательство: reports/scene3-scene4-audit-2026-11-06.md. Итог проверки/публикации — корневой reports/work-continue-linked-chat-2026-11-06.json.

Следующий шаг: До отправки RESOURCE продолжать художественный motion/audioQC существующих попыток; для HONOR выбрать озвучку и точное изделие по решению владельца. Генерации, приёмка и перерисовка без нового разрешения не выполняются.

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
