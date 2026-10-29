# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-29T08:44:21+00:00
Задача: SEREGIUS-PLAN-20261023 — Завершить Серёгиус по сохранённому плану, оценить готовые ролики

Последний подтверждённый этап: Owner authorized exactly one new S62-P1 attempt first at the next free slot; old unknown claim preserved in history. Full scan:6/6 active; no new submission.
Следующий шаг: First next video slot: S62-SEED20-P1; exactly one new owner-authorized Unlimited0 attempt. Fresh full reconciliation first: adopt any actual existing S62 task instead of duplicating. Unknown old claim retained in history. New CAS claim and allowance consumption before Create; no further automatic retry. Other items ready-skip; Stitch closed; Roscosmos paused.

## Контрольная точка

# Сцена 62 — следующая попытка по решению владельца · 29.10.2026

work_id: SEREGIUS-PLAN-20261023
work_id: TOPVIEW-SLOT-PRIORITY-20261024

Записано: 2026-10-29T08:41:44.413Z. Владелец: «Тогда следующей попробуем 62». Для S62-SEED20-P1 разрешена ровно одна новая бесплатная попытка, первой при следующем свободном видеослоте (priority -0.5). Это явное новое разрешение после неизвестного исхода; не утверждение, что первая попытка не была отправлена. Прежние claim и receipt сохранены в submission_history, активный claim снят по этому решению. При свежем обнаружении настоящей задачи62 принять её вместо дубля. Иначе новый CAS-claim и расход единственного allowance ДО Create; следующий таймаут или fail не разрешает ещё попытку.

Скан 2026-10-29T08:38:26.439Z: 13 досок, 19 страниц, 943 задачи, 6 активных видео, свободных слотов0; после старой попытки62 найдены только две известные отправки59. В этом изменении Create/новых видео0.

Татуинская связка: 52ч7→66→67→68→69→70→65. Перед её началом ещё пять новых частей52 (2–6), часть1 уже в очереди сервиса. До66 нужен также результат52ч7. По живым priorities перед66 стоят18 ещё неотправленных частей из9 сцен (52,56,48,62,59,60,61,63,64); это не18 обязательных ожиданий: независимые ветки идут по готовности. 63→64 расположены перед66, музыкальные49–51 и танцы после связки.

Следующее действие: First next video slot: S62-SEED20-P1, one newly owner-authorized Unlimited0 attempt. Fresh main/owner decisions/lock/full account scan; if actual S62 task is found adopt it and do not duplicate. Unknown old claim preserved in submission_history; it is not an active lock for the new allowance. Before Create persist a new CAS claim and consume allowance; any new timeout/failed attempt gets no automatic repeat. Other items keep ready-skip. Stitch trials closed; Roscosmos paused.

Квитанция: reports/topview-queue-2026-10-16/S62-SEED20-P1-20261029-owner-next.json. Эта запись заменяет прежний запрет новой попытки62 и указание «следующая60»; остальные ограничения сохранены.

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

- `ops/topview-launch-queue.json`
- `ops/TOPVIEW-FREE-LAUNCH.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 44

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
