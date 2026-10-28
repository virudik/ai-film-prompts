# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-10-28T03:11:35+00:00
Задача: SEREGIUS-PLAN-20261023 — Завершить Серёгиус по сохранённому плану, оценить готовые ролики

Последний подтверждённый этап: Татуинская цепочка52P7→66→67→68→69 согласована; все пять звеньев выбраны Wan3/30с перед49–51/28. Опубликовано и проверено по точным публичным SHA; content commit 71056a649105eb5fca6d482ce024363b559894c6.
Следующий шаг: Принять смену по свежему main и сохранить собственную квитанцию; затем проверить результаты/QC, решения владельца и общие live-слоты. Продолжить разрешённую очередь Серёгиуса: новая S52-R2-P1 при свободном слоте, P2–P7 после реального результата и QC предшественника. Существующие task ID не отправлять повторно. Новая конкретная команда владельца приоритетнее этого фокуса.

## Контрольная точка

# Татуин — связность и выбранные версии Wan 3 · 28.10.2026

work_id: SEREGIUS-PLAN-20261023
Проверено: 2026-10-27T22:30:37Z. Отчёт: reports/tatooine-chain-2026-10-28.json.

Уточнение владельца28.10: уличная цепочка52 ч.7 →66 →67 →68 →69 должна запускаться в Wan3 и иметь приоритет перед музыкальными сценами49–51 и танцами28. Выбран существующий Wan3/30с блок52P7; части52P1–P6 сохраняют Seedance2.0/15с. Стабильный ID P7 сохранён для зависимостей, модель определяется полями model/canonical_block_label.66–69 уже были Wan3/30с. Новых пунктов очереди, task IDs, claims, запусков и художественных одобрений нет.

Сюжетная связь подтверждена: Серёга уступает камеру Алине/Даше/Стичу; Стич оставляет кучку; камера передаётся Маше у фруктового прилавка; после её спора камера возвращается к тому же месту, где Жилищник метёт вокруг кучки; Маша в69 сама собирает её и песок в совок. В68 композиции кучка видна. Сохранена комедийная развязка69; отдельно уточнены голубая дыня на стыке66→67 и география возврата68.

Бесшовность задана настоящими последними3с предыдущих результатов и QC. Эти результаты ещё ожидаются; готовое видео и фактически идеальный стык не заявляются. Численные приоритеты ставят цепочку выше49–51/28; прежний ready-skip владельца остаётся: если продолжение ждёт результат, следующий готовый пункт может занять свободный слот.

Опубликовано и проверено по точным публичным SHA; content commit 71056a649105eb5fca6d482ce024363b559894c6.

Следующий шаг сохранённого плана: Принять смену по свежему main и сохранить собственную квитанцию; затем проверить результаты/QC, решения владельца и общие live-слоты. Продолжить разрешённую очередь Серёгиуса: новая S52-R2-P1 при свободном слоте, P2–P7 после реального результата и QC предшественника. Существующие task ID не отправлять повторно. Новая конкретная команда владельца приоритетнее этого фокуса.

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

- `ops/CONTINUE-PROTOCOL.md`
- `reports/handoff-receipts.json`
- `reports/scene52-seven-parts-handoff-2026-10-27.md`
- `ops/TOPVIEW-FREE-LAUNCH.md`
- `ops/OWNER-TASKS.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 39

## Пробелы

- brief was invalid at generation
- project-status health not ok
- master vs project-status sha256 mismatch
