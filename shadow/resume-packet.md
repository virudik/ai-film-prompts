# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-11-14T18:43:46+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# 14.11.2026 — D7 ordinary: проверка очереди и передача смены

work_id: SEREGIUS-SHIFT-20261113-T611U

- Полный приём D7 из свежего GitHub main: 15/15 якорей и SHA256 всех 8 канонических источников совпали; после изменения очереди относительно старого recovery выбран полный приём. Resume focus сохранён (SEREGIUS-SHIFT-20261113-T611U); 7 инструкций прочитаны, master байты проверены через blob.
- Живые источники: проект health=ok, монитор primary=robot, Topview снимок 2026-11-14T18:10:27Z: занято 5/6, свободно 1; очередь t601u: S48-P4-R2 и S51E/F/G уже submitted, в работе. S89A-WAN30 — следующий разрешённый waiting_for_slot/authorized_inputs_available, пять референсов; текущий чат не создавал новые задачи, не менял очереди и не тратил кредиты.
- Capability preflight текущего обычного чата: Browser.list_tabs требует originating browser context; соединение с авторизованной формой Topview, проверка native file upload и Unlimited0/price0 здесь невозможны. Последний независимый полный скан Relay #674 (2026-11-14T18:10:27Z) также blocked_browser. claim/intent/Create=0; неизвестные отправки и уже выданные task_id сохраняются.
- Проверены живые GitHub owner-tasks: open/taken/needs_owner=0; Supabase owner_decisions: новых pending/in_progress нет, историческая needs_owner to:grok отдельно. Scene 88 ждёт художественную оценку; PR 369–371 не трогать.
- Принята foreground ordinary-смена epoch 5→6 (session_id локальный, реальный conversation ID недоступен). Work/Grok, расписания, route_generation и старые claims не менялись. Следующий шаг: только в новом реально авторизованном браузерном исполнении снова полный скан, точные исходники и UI Unlimited0, затем собственный замок/CAS, один Create для следующего ещё не отправленного item. Без этих доказательств — никакого Create.

checked_at: 2026-11-14T18:43:19.304Z

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
Задач с сохранённым task ID: 90

## Пробелы

- selected checkpoint hash mismatch
