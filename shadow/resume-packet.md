# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-09T20:23:11+00:00
Задача: SEREGIUS-PARODIES-20261109 — Семь пародийных сцен с изображениями по прямой команде владельца

Последний подтверждённый этап: Сохранена отдельная галерея существующих фото: 7 основных кадров и 7 ранних композиционных черновиков, 21 текст без изменений.
Следующий шаг: Не генерировать заново. Сверить parodies.html, 7 основных PNG и 7 первых композиционных черновиков; все доступные варианты — в указанной Drive-папке. Первые фото не являются исправлением лиц и не входят в видеовходы. Коррекция остальных лиц/дополнительные кадры и старые независимые поручения остаются открытыми; никакой автоприёмки или видеозапуска.

## Контрольная точка

# 09.11.2026 — сохранение существующих фото пародий на сайт и Drive

work_id: SEREGIUS-PARODIES-20261109

- Новая команда: сохранить то, что уже есть, без новых генераций.
- Семь основных PNG не менялись; семь первых фото опубликованы в отдельной архивной галерее, не как референсы лиц. Во всех сценах 74–80 есть ссылка на фотографии и Drive-папку.
- Все 21 видеопромпт сохранены без изменения текста; очередь и приёмка не изменены.
- Drive: https://drive.google.com/drive/folders/1m0kKr532uOqOzyoIZh_9ZlrWfOoQtNxu
- Доказательство: reports/parody-existing-photos-publication-2026-11-09.json. Полная доводка сцен не заявлена.
- Следующий шаг: Не генерировать заново. Сверить parodies.html, 7 основных PNG и 7 первых композиционных черновиков; все доступные варианты — в указанной Drive-папке. Первые фото не являются исправлением лиц и не входят в видеовходы. Коррекция остальных лиц/дополнительные кадры и старые независимые поручения остаются открытыми; никакой автоприёмки или видеозапуска.

checked_at: 2026-11-09T20:18:38+00:00

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

- `parodies.html`
- `reports/parody-existing-photos-publication-2026-11-09.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 84
- S66-STITCH-INDEP-WAN30: reconcile_without_resubmitting

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
