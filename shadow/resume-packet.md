# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-10-30T00:15:29+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Bounded retry policy and both automation prompts published/read back; six slots occupied, no new submission.
Следующий шаг: Fresh main/owner decisions/full all-board scan. Confirmed technical failure: ops/TOPVIEW-RETRY.md, max2 additional free attempts with shared durable counter, otherwise next independent ready item in same cycle. Observe active S59P2/S62P1/S60P1; S61P1 is next currently ready, subject to fresh priorities/inputs; S56P2 remains QC-blocked.

## Контрольная точка

# Задача №1: технические повторы без остановки очереди · 30.10.2026

work_id: TOPVIEW-SLOT-PRIORITY-20261024
work_id: SEREGIUS-PLAN-20261023

Решение владельца: при техническом отказе пытаться восстановить запуск, затем продолжать независимую согласованную очередь Серёгиуса. Действует ops/TOPVIEW-RETRY.md: до двух дополнительных попыток на item, общий постоянный счётчик Work/hourly/Relay, пауза около минуты; неизвестный исход сначала сверять, активные задачи не дублировать. Owner holds, реальные входы/QC и Unlimited0 сохраняются.

Часовое задание 6acae6ab… и Relay 6adc585e… обновлены; точный readback обоих, расписание HH:55 Europe/Moscow и одна relay.message с прежними фильтрами подтверждены. Коммит правил: e6524f3c1465a79b97e82ca84f100b9346975530. Квитанция: reports/topview-retry-policy-2026-10-30.json. 348 тестов, site validator и canon-health прошли.

На 30.10 02:38 МСК: полный скан 14 досок/20 страниц/945 задач; 6/6 видео init, свободных0, новых запусков/повторов здесь0. S60-P1 уже отправлена Relay в02:20 (025955aad2cf494da2b4104d26c36ed5). Исправленная S59-P2 и S62-P1 активны. Ближайшая сейчас готовая независимая — S61-P1; при освобождении сначала заново проверить priority/готовность более ранних частей. S56-P2 по-прежнему блокирует дефект реального стыка P1, художественный rerender не разрешён.

Далее: на настоящем wake/часовом цикле fresh main/решения владельца/полный скан; подтверждённый технический fail обработать по общему бюджету, локальный blocker/исчерпание не удерживают слот. Неизвестный Create не повторять. Новый retry ещё не испытывался в production: текущие слоты заняты.

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
- `ops/TOPVIEW-RETRY.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 46

## Пробелы

- brief was invalid at generation
- master vs project-status sha256 mismatch
