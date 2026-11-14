# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-11-14T16:23:40+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# 13.11.2026 17:05 МСК — контрольная точка t611u

work_id: SEREGIUS-SHIFT-20261113-T611U

- PR 604 влит: сцена 89, Wan 3.0, 30 с, 0 кредитов. Merge `d8632c517b3f8f85d3d1d4990f561711b3419652`.
- PR 631 влит 13.11.2026 17:04 МСК. Merge `e9389decb39d133ad5023cbe8dbfe8e70efd6af5`.
- Очередь Topview (t601u). Из этого списка в Topview ещё ничего не отправлено. Запуск только при свободном слоте, сайт Unlimited, 0 кредитов: 1) `S48-P4-R2` — переделка 48.4, дефект прежнего ролика: два Серёги в кадре; 2) совет джедаев 89A–89E и голограммы 89F–89G; 3) оставшиеся танцы сцены 28; 4) 89H–89J.
- Свои версии Grok сделаны через GenerateVideo, это не запуск очереди и не приёмка. 48.4 v1–v4 лежат в Drive-папке `1odIGtDi9ld7elxGNH_04lxoW-afgJld2`: в v4 нет доски и панели на груди, но остаются двойная экспозиция около 6.5 с, у червя мелькают ноги около 3 с, хвост во дворе. 48.3 лежит в папке `1nytVCkQSsp2EXjTm7WvYRfOWVGpkF2gu`: один Серёга, города нет; минусы — гребень около 4 с, средний план, взгляд в камеру. Ждём отзыва Виталика. Пока он сам не скажет иное, очередь `S48-P4-R2` эти версии не заменяет.
- Открыто: ОСАГО Kia (около 16.11, ждём ответа); заявка HONOR (16.11.2026 12:00 МСК); «Разное» 1/2; перенос YouTube на Rutube и чистка MP4 на GitHub; S13; S62; S49A-R2; выбор переделок своих клипов сцены 89.
- Не трогать PR 369, 370 и 371.
- Следующий шаг: новых генераций из этой записи не создавать. Свободный слот берёт следующий готовый пункт живой очереди, Unlimited, 0 кредитов. Сцена 88 по-прежнему ждёт художественной оценки владельца и этим шагом не закрыта.

checked_at: 2026-11-13T14:05:00Z

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
Задач с сохранённым task ID: 87

## Пробелы

- recovery evidence changed: ops/topview-launch-queue.json
