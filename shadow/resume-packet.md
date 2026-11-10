# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-10T18:33:57+00:00
Задача: SEREGIUS-SASHA-PHOTOGRAPHER-20261110 — Сцена88: отдельная реклама фотографа Саши

Последний подтверждённый этап: Сцена88 оформлена:4 существующих PNG + исходный лист Саши,3 автономных промпта. Проверки master/site/инструкций прошли; общий набор тестов не получил новых ошибок, прежние сбои отражены в отчёте; оригиналы с Drive проверены обратным скачиванием. Сцена87 и остальные сцены не изменены; видео и расходы0.
Следующий шаг: Проверить фактическую публикацию сцены88,галереи,4 PNG/4 превью на Pages; до проверки не объявлять сайт готовым. Фото повторно не генерировать. P2 ждёт реальный конецP1; видеозапуск отдельно.

## Контрольная точка

# 10.11.2026 — Сцена 88: Саша. Даже слишком красиво

work_id: SEREGIUS-SASHA-PHOTOGRAPHER-20261110

- Создана отдельная сцена88: 4 оригинальных PNG + исходный референс лица Саши, 3 автономных промпта, галерея. Сцена87 и все прежние сцены неизменны; очередь, approval, видео и кредиты не тронуты.
- Проверка: reports/sasha-photographer-scene-88-2026-11-10.json.
- Следующий шаг: Проверить публикацию именно сцены88 и её4 оригиналов/4превью на сайте, затем отметить этап публикации. Не генерировать фотографии повторно. Видеозапуск не разрешён; P2 ждёт настоящий конецP1. Старые задачи этим этапом не закрыты.

checked_at: 2026-11-10T16:06:56+00:00

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

- `video-prompts.md`
- `parodies.html`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 86

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
