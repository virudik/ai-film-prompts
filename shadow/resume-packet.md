# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-30T01:42:36+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Трио и3 референса готовы;6 промтов,348 тестов и master health пройдены; публикация далее
Следующий шаг: Проверить свежую очередь и слоты, продолжать разрешённые готовые части; отдельный PNG штурмовиков пока блокирован фильтром.

## Контрольная точка

# Трио Маши Р, Алины и Даши · 30.10.2026

work_id: SEREGIUS-PLAN-20261023
work_id: TOPVIEW-SLOT-PRIORITY-20261024

Подготовлены три новые картинки, самостоятельные28A13/49G/51G и их30с альтернативы. Инструменты: Маша Р — медно-красная гитара, Алина — бирюзовый бас, Даша — фиолетовые клавиши;51G использует повреждённый образец только для конца. Вуки50A/B остаются на центральной площадке, ненужный групповой G28 вход удалён и4 оставшихся входа перенумерованы. Старые отправки неизменны. Новые три пункта продолжают действующую бесплатную очередь музыкального номера;30с варианты не выбраны. Видео в этом цикле не отправлялись.

Штурмовики — зрители напротив по новому решению владельца; PNG генератор отклонил фильтром. Старый незавершённый вариант «вуки напротив» отменён, не восстанавливать. Блокер касается только дополнительного кадра публики. Следом: свежие очередь/слоты/разрешения; независимые готовые части не ждать из-за этой картинки. СуществующиеA3/A12 требуют своих настоящих стыков. Не повторять проваленные картинки Стича:3 отменённых пункта перенесены в архив без потери истории.

Доказательства: `reports/final-music-trio-2026-10-30.json`; публикация и тесты будут дописаны после проверки.

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
- `references/scenes/scene-50/manifest.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 46

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
