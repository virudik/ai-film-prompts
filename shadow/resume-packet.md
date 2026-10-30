# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-10-30T00:54:55+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: All47 finale prompts and26 pending hashes validated;348 tests passed. Empty reverse hangar saved; audience B blocked by image generator including edit attempt. Publication readback pending.
Следующий шаг: Finish publication readback; then fresh main/inbox/lock/full slot scan and next ready authorized item. Inspect updated light/motion/camera. Obtain audience B image before owner placement choice; keep existing production reference until then.

## Контрольная точка

# Финальный музыкально-танцевальный номер · 30.10.2026

work_id: SEREGIUS-PLAN-20261023
work_id: TOPVIEW-SLOT-PRIORITY-20261024

По команде владельца обновлены все47 промтов28/49/50/51 и26 неотправленных пунктов очереди: меняющийся свет/пол, непрерывное исполнение и подходящие действию дуги/наезды/отъезды камеры. Старые13 отправок28 связаны с нынешними редакциями в reports/final-music-number-2026-10-30.json; их фактические payload/SHA/результаты не изменены. Очередь, выбранные движки, обязательные референсы и зависимости сохранены. Видео и платные операции не запускались. 348 тестов, site contract и master health=ok, canon health без предупреждений. Публикационный readback ещё выполняется.

Пустой обратный вид H28B создан и визуально проверен как предложение. ВариантА — существующий выбранный кадр вуки на площадке. ВариантБ — зрители напротив: генератор отклонил кадр, PNG нет; точный промт references/scenes/scene-50/S50-option-B-opposite-audience.image-prompt.txt сохранён. Не выдавать пустой ангар за готовую толпу, не выбирать вариант за владельца и не заменять текущий @Image5. Не повторять уже готовую работу.

Дальше: завершить проверку/публикацию; продолжать согласованную очередь после свежего чтения main/входящих/замка и живой проверки всех слотов. У28A3 требуется чистый конец новогоA2, уA12 — настоящий конецA11. КадрБ остаётся отдельным незавершённым визуальным заданием и не блокирует видеоочередь. После его получения владелец выбирает расстановку; тогда согласованно обновить версии50 и их входы. Проверять будущие видео по отправленным редакциям, особенно середину движения, смену света, лица/контакты и географию. Старые числа слотов не считать свежей проверкой.

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
- `video-prompts.md`
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
