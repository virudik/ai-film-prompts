# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project raznoe`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-05T19:23:53+00:00
Задача: MISC-S1-S2-REFERENCES — 59 отдельных референсов сцен 1 и 2 из GPT-TASK.md

Последний подтверждённый этап: Пять листов со светлой кожей на месте, описания и SHA обновлены; цены сайта Topview записаны, клиентские цены не снижены.
Следующий шаг: Художественный просмотр пяти новых листов Лены, Нины и Дарьи на сайте проекта raznoe. Видео не запускать. Цены клиенту 59 000 / 145 000 / 265 000 ₽ не менять.

## Контрольная точка

# Кожа Лены, Нины и Дарьи и web-цены · 02.11.2026

work_id: MISC-S1-S2-REFERENCES
Проверено: 2026-11-02T22:50:00Z

Пять одобренных владельцем листов со светлой кожей стоят на прежних путях, 1536×1024: `mama-lena.png`, `mama-lena-expressions.png`, `nina.png`, `nina-expressions.png`, `darya.png`. В описаниях кожи — «светлая кожа, славянская/русская внешность»; волосы и одежда не менялись. Мама Вера и остальные референсы не трогались. SHA-256 и миниатюры обновлены. Все референсы по-прежнему `not_approved` как набор; видео не запускались.

Цены пересчитаны по ценам сайта Topview (не iOS), с резервом на повторы и переделки. Цены клиенту те же: **59 000 / 145 000 / 265 000 ₽**. Клиентские PDF лежат на Google Drive в папке «AI Film — сметы и презентации для клиента».

Следующее действие: художественный просмотр новых листов на сайте. Видео не запускать.

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

Нет ошибок локальной проверки. Живые проверки выше обязательны.
