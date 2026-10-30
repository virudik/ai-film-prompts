# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-30T08:33:59+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Опубликованы7 состояний инструментов и вариант публики с вуки;14 промтов,348 тестов, CI/public readback подтверждены
Следующий шаг: Свежие очередь/слоты: продолжать разрешённые готовые части. Штурмовики и смешанный вариант отдельно блокированы Topview; не повторять автоматически.

## Контрольная точка

# Референсы рок-финала и варианты публики · 30.10.2026

work_id: SEREGIUS-PLAN-20261023
work_id: TOPVIEW-SLOT-PRIORITY-20261024

Семь недостающих состояний:51A–F результат разрушения,51G замах с целыми инструментами. Исправлена лишняя кисть промежуточного51G; ошибочный черновик не опубликован.14 автономных промтов различают начало/контакт/конец;7 ожидающих items обновлены без смены порядка и разрешений. Новых видео нет.

Nano Banana Pro: три разрешённых платных попытки, вуки готовы; штурмовики и смешанная толпа отклонены провайдером7000/35561575,1,6 возвращено, чистый расход0,8, баланс5,57. Последняя команда вновь разрешила вариант вуки напротив; прежняя отмена ниже историческая. Новый вариант — только галерея до выбора; действующий50A/B и их выбранные входы прежние. Два отсутствующих PNG не выдавать за готовые; не тормозить из-за них независимую очередь.

Следом: свежие очередь/слоты/разрешения, продолжать готовые части без дублей и платных видео. Оценить будущие ролики по фактически отправленным промтам. Доказательства: `reports/final-music-reference-states-2026-10-30.json`. Контент8cb8a8692f3e9f243b56650a890a09645919f536:348 тестов и GitHub CI прошли; публичные master/status,8 PNG и8 миниатюр проверены. Замок освобождён финальной квитанцией.

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
- `references/scenes/scene-51/manifest.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 46

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
