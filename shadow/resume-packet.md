# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-13T04:34:00+00:00
Задача: SEREGIUS-SASHA-PHOTOGRAPHER-20261110 — Сцена88: отдельная реклама фотографа Саши

Последний подтверждённый этап: Проверка публикации завершена: 4 оригинала, 4 превью, исходный референс Саши, мастер, manifest и галерея скачаны с сайта; все 12 SHA256 совпали. Пять устаревших/ошибочных тестовых проверок исправлены, полный набор: 538 тестов, 0 сбоев, 0 ошибок, 0 пропусков. Тексты сцен, изображения, очереди, приёмка и семь инструкций не изменены; видео и расходы 0.
Следующий шаг: Техническая публикация сцены88 завершена и проверена; не создавать сцену, фотографии и промпты повторно. Художественная приёмка владельца отдельно. Видео не запускать без отдельного разрешения; Seedance P2 ждёт настоящий конец P1. Остальные исторические задачи этим этапом не закрыты.

## Контрольная точка

# 10.11.2026 — Сцена 88: Саша. Даже слишком красиво

work_id: SEREGIUS-SASHA-PHOTOGRAPHER-20261110

- Проверка публикации завершена: 4 оригинала, 4 превью, исходный референс Саши, мастер, manifest и галерея скачаны с сайта; все 12 SHA256 совпали. Пять устаревших/ошибочных тестовых проверок исправлены, полный набор: 538 тестов, 0 сбоев, 0 ошибок, 0 пропусков. Тексты сцен, изображения, очереди, приёмка и семь инструкций не изменены; видео и расходы 0.
- Доказательство: reports/scene88-technical-verification-2026-11-10.json; run 42892845673.
- Следующий шаг: Техническая публикация сцены88 завершена и проверена; не создавать сцену, фотографии и промпты повторно. Художественная приёмка владельца отдельно. Видео не запускать без отдельного разрешения; Seedance P2 ждёт настоящий конец P1. Остальные исторические задачи этим этапом не закрыты.

checked_at: 2026-11-10T20:12:54+00:00

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

- `reports/scene88-technical-verification-2026-11-10.json`
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
