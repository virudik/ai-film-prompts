# Продолжай — пакет восстановления: Стахий

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project stikhiy`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-11-25T16:43:40+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# 19.11.2026 — Стахий: перенос проекта и статус работы

work_id: STIKHIY-SCENE1-20261118

Проект выделен из «Разного» по прямому поручению владельца. Сцена 1 «Ради этого стоит жить»; имя героя — Стахий. Сохранены варианты 15×15 и 10×30, все 25 промтов, 10 локаций, 9 черновых листов внешности и реконструкция дачи. Нумерация исходных эпизодов и реплики не менялись. Шура и Юлия по-прежнему не распределены по ролям. Оригинальные семейные фотографии не опубликованы.

Добавлены 11 отдельных V2-листов с ракурсами головы: 8 других персонажей и Стахий по листу на 1, 2 и 3 года. Девять прежних V1 сохранены как дополнительные. Роли Шуры и Юлии, номера и входы промтов не менялись.

Следующий шаг: Проверить с владельцем черновые референсы, уточнить роли Шуры и Юлии, затем проверить пробную озвучку ночного диалога и 188-секундный монтаж. До отдельного разрешения видео не запускать.

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


## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 0

## Пробелы

- selected checkpoint hash mismatch
