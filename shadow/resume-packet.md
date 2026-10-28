# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-10-28T09:13:28+00:00
Задача: SEREGIUS-PLAN-20261023 — Завершить Серёгиус по сохранённому плану, оценить готовые ролики

Последний подтверждённый этап: Проверены материалы и работа сменщика; восстановлена готовность S64 и согласованность плана. Relay ранее запустил52P1, S28A1 получил QC.
Следующий шаг: Прочитать свежие решения владельца и все слоты. Наблюдать существующий S52-R2-SEED20-P1 task c65c30d8cbe14e9eadec886276e62471 без повторного Create; по готовности сохранить оригинал и выполнить QC для реального стыка P2. При свободном слоте продолжить существующую авторизованную очередь по приоритету и полному Unlimited0 preflight: S64 готов, S28-A1-R2 технически разблокирован после QC предшественника. Связка52P7→66→67→68→69→70→65 требует настоящих результатов и последних3с; Роскосмос на паузе.

## Контрольная точка

# Основной план после проверки сменщика · 28.10.2026

work_id: SEREGIUS-PLAN-20261023. Проверено: 2026-10-28T09:11:19+00:00.

Аудит сменщика подтвердил28 текущих PNG,34 изображений-входов очереди и72 публичных файла (HTTP200, побайтовое совпадение). Исходная задача закрыта корректно:18 ролей референсов обеспечены17 отдельными PNG с разрешённым владельцем повторным использованием общего кадра со Стичем. Сюжет и рисунки сохранены. Отчёт: reports/successor-audit-2026-10-28.json.

Исправлены искусственный блокер S64, явные пути изображений в обеих версиях52P7, пять устаревших отметок публикации и неполная тестовая фикстура журнала. Relay включён; его live-инструкция содержит повторы браузерной проверки, checkpoint и защиту от дубля Create. Реальный запуск52P1 по slots:6bc77dbe:2 подтверждён квитанцией; испытание самого browser-retry не заявляется. Правило задач «только открытый Work» уже внесено и сохранено.

Последний прочитанный полный скан08:06UTC показывал6/6; это историческое наблюдение, не текущая доступность. S28-A1 QC: partially_usable_not_owner_approved; разрешённый R2 ждёт слота. Новых изображений, пунктов очереди, запусков и художественных одобрений при аудите нет.

Следующее действие: Прочитать свежие решения владельца и все слоты. Наблюдать существующий S52-R2-SEED20-P1 task c65c30d8cbe14e9eadec886276e62471 без повторного Create; по готовности сохранить оригинал и выполнить QC для реального стыка P2. При свободном слоте продолжить существующую авторизованную очередь по приоритету и полному Unlimited0 preflight: S64 готов, S28-A1-R2 технически разблокирован после QC предшественника. Связка52P7→66→67→68→69→70→65 требует настоящих результатов и последних3с; Роскосмос на паузе.

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

- `reports/successor-audit-2026-10-28.json`
- `ops/OWNER-TASKS.md`
- `ops/TOPVIEW-FREE-LAUNCH.md`
- `ops/topview-launch-queue.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 40

## Пробелы

- brief was invalid at generation
- master vs project-status sha256 mismatch
