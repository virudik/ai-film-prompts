# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-28T08:42:42+00:00
Задача: SUCCESSOR-AUDIT-20261028 — Проверка завершённой работы сменщика: референсы, Relay, Продолжай

Последний подтверждённый этап: Прочитан отчёт сменщика и свежий main; найдены два подтверждённых несоответствия.
Следующий шаг: Проверить артефакты и связи, исправить подтверждённые ошибки, выполнить проверки и вернуть основной фокус.

## Контрольная точка

# Проверка работы сменщика · 28.10.2026

work_id: SUCCESSOR-AUDIT-20261028. Проверено: 2026-10-28T08:41:28+00:00.

Владелец поручил сверить работу другого чата, исправить только недоделки и не повторять готовое. Исходный main: 67798296b6c697332ba9f44a49a6f57ed3d1b48a. Отчёт: reports/successor-audit-2026-10-28.json. Прочитаны доступный общий чат, актуальные правила и живые настройки Relay; повторное рисование/видеозапуски не выполняются.

Найдены устаревший технический blocker S64 и рассогласование next_action/recovery в основном плане. Дальше: проверить байты всех изображений, manifests/registry/галереи/очередь/публичный сайт, исправить подтверждённые ошибки и обновить доказательства восстановления. Ранее сохранённый основной фокус будет восстановлен после аудита.

---

<!-- relay-current-status -->
## Текущее Relay-событие
Проверено: 2026-10-28T06:55:12.326724Z. work_id: TOPVIEW-SLOT-PRIORITY-20261024.
slots:6bc77dbe:2 / issue98: отправлена ровно одна S52-R2-SEED20-P1, task `c65c30d8cbe14e9eadec886276e62471`, Seedance2.0/15с/720p/16:9,5изображений+настоящие3с S44, Unlimited0,0кредитов. Полный текст и входные SHA проверены; отдельный CAS claim. После отправки полный скан13досок/19страниц/938задач подтвердил6занятых/0свободных. Квитанции: reports/topview-event-wake.json и reports/topview-queue-2026-10-16/S52-R2-SEED20-P1-receipt-20261028.json. Художественная приёмка не выполнялась.
Далее: ждать реальный результат этого task, сохранить оригинал, выполнить QC корабля/личности/входа и настоящий стык для R2P2; при следующем свободном слоте свежая общая очередь без резервирования. Уже отправленное не повторять. Собственный замок освобождён в том же коммите.
Поздняя проверка 2026-10-28T07:42:40.844Z: восстановленные result:4b7b972870a44dfbb29bd6c5e330a633 (issue95) и slots:6bc77dbe:1 (issue96) подтверждены и завершены stale: исходные сигналы старше30мин. Новых Create/claim/расходов нет; квитанция slots:6bc77dbe:2 и существующий task сохранены. Новый live-скан в этой проверке не выполнялся.
<!-- /relay-current-status -->

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
- `ops/TOPVIEW-FREE-LAUNCH.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 40

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
