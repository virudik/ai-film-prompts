# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-27T20:52:36+00:00
Задача: OPEN-WORK-REFS-RELAY-20261027 — 18 референсов, персонажи по фото, повтор Relay и открытые Work-задачи

Последний подтверждённый этап: 16/18 исходных +4 дополнительных изображения проверены по файлам/SHA; checkpoint восстановлен
Следующий шаг: Создать S66-alien-dog (Стич), затем улицу66 и4 кадра68/69, связать входы; Relay retry и Work-only продолжение

## Контрольная точка

# Референсы, Relay и Продолжай — открытый Work · 27.10.2026

work_id: OPEN-WORK-REFS-RELAY-20261027
Проверено: 2026-10-27T20:51:54+00:00. Продолжение открытым Work, session_id c8084d939274 (локальный идентификатор, не ID чата).

Команда владельца: лично завершить 18 референсов claude-202610271320-cpk-refs и развёртки/сценические кадры по фото Алины, Даши и Маши Р. Собака — Стич. Пункт2: при временном сбое браузера повторить чтение/восстановление 1–2 раза с паузой около минуты; при неудаче записать причину и следующий шаг для нового события или часового задания. Пункт3: «Продолжай» в открытом Work включает открытые задачи с меткой «ВЫПОЛНЯЕТ ТОЛЬКО ОТКРЫТЫЙ ЧАТ ChatGPT Work». Видео не запускать, новых пунктов очереди не добавлять.

Исходное состояние проверено по main 1876317fe9983cd884d2f1e5d168af1e9b0a4370: 16/18 исходных PNG уже существуют (10 ЦПК, по2 для64/65/67), также сохранены три развёртки и спор Маши с продавцом — всего20 файлов. SHA всех перечислены и сверены в reports/open-work-refs-relay-2026-10-27.json. S65-toast, S67 и развёртки НЕ рисовать повторно. Прежняя recovery-ссылка отстала от manifest65; выполнен полный приём7инструкций и восстановлена фактическая стадия. Supabase: открытых решений0; робот основной, свежая телеметрия6/6, monitor_role=skip. Художественное принятие не выставлено.

Осталось шесть уникальных изображений: Стич и улица66; бригада/метла68; дополнительные композиции68/69 (новая задача claude-202610272340-s68-69-refs по команде владельца27.10 23:37МСК). Каждый кадр: QC, manifest/галерея, commit/readback до следующего. Затем связать все существующие входы и SHA, исправить устаревшие ожидания фото и оранжевую собаку в52P7/66; @Video1 остаются настоящими будущими результатами. Дополнительные композиции68/69 — только галереи, без новых входов промпта/очереди.

После картинок: Relay retry и live prompt существующего6adc585e с сохранением одной подписки; правило открытого Work в CONTINUE/OWNER-TASKS/шаблоне; сертификат/тесты/Pages/readback, закрытие двух задач с result_commit. Следующий шаг: скорректировать .image-prompt по решению «Стич», создать S66-alien-dog.png штатным imagegen.

Блокеры: нет постоянных. Запись — GitHub connector FF/CAS под замком; исходный бриф восстановлен по проверенным фактам. Сохранённая настройка не доказывает будущий успешный browser retry. Никаких новых video submit/approval/Relay ACK.

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

- `ops/OWNER-TASKS.md`
- `ops/CONTINUE-PROTOCOL.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 39

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
