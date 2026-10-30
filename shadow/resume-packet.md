# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-30T00:22:59+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Scene28: all23 prompts and12 pending SHA revised for animated lighting and sustained motion; GitHub/Pages verified,348 tests passed; zero generations.
Следующий шаг: Fresh main/owner decisions/inbox/lock and full slot scan; continue next ready authorized queue item under ops/TOPVIEW-RETRY.md. At Scene28 use revised SHA, inspect animated lights/floor, sustained middle motion and clean face gestures. A3 requires clean new A2; A12 requires real A11 ending. Old slot counts are not a fresh scan.

## Контрольная точка

# Танцы28: светомузыка и непрерывное движение · 30.10.2026

work_id: SEREGIUS-PLAN-20261023
work_id: TOPVIEW-SLOT-PRIORITY-20261024

По прямой команде владельца опубликованы правки всех23 промптов A1–A12/B1–B11: меняющиеся цвет/яркость лучей, волна по световым линиям пола и отражения; постоянный нейтральный свет на лицах. Непрерывное движение в середине и при сближении/расхождении; финальная поза только последние0,5с. A1/B1 сближаются танцуя в последние2с; A2/B2 — один короткий обмен, две внешние щеки, лицо не перекрывать, согласованный кадр до колен. Опоры, хват, лица, костюмы и кошачья анатомия сохранены.

Коммит:2797025754b0506e9798706c97e06bb1c6151660. Отчёт:reports/scene28-light-motion-2026-10-30.json. У12 неотправленных выбранных items обновлены SHA; порядок, разрешения, реальные входы и зависимости прежние. Старые A1/A2 отправлены23.10; готовые видео не менялись и новая редакция ещё не проверена рендером. Удачные фрагменты A1 сохранять для монтажа. Новых картинок/запусков/пунктов очереди0.

Проверено:348 тестов, site validator, master health=ok, canon-health0 предупреждений;8 файлов прочитаны обратно по blob SHA. Канонический workflow и Pages успешны; публичный master содержит23 новых световых блока, его SHA совпадает с project-status. Правило света в PROMPT-STYLE-GUIDE.md §5.I, handoff обновлён.

Дальше: свежий main/решения/входящие/замок и полный скан слотов, затем следующая готовая разрешённая сцена по живой очереди; технические отказы — ops/TOPVIEW-RETRY.md. Достигнув28, использовать новые SHA и проверять реальную смену света/пол, энергию в середине, лица и контакты. A3 ждёт чистый новый A2, A12 — настоящий конец A11; правка текста эти зависимости не снимает. В этой редакционной задаче повторный живой скан слотов не выполнялся: старые числа занятости не считать свежими.

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
- `reports/scene28-light-motion-2026-10-30.json`
- `ops/TOPVIEW-RETRY.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 46

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
