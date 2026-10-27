# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-27T21:35:14+00:00
Задача: OPEN-WORK-REFS-RELAY-20261027 — 18 референсов, персонажи по фото, повтор Relay и открытые Work-задачи

Последний подтверждённый этап: Пять новых кадров сохранены;25 файлов проверены; входы52P7/64–69 и правила Relay/Work-only согласованы
Следующий шаг: Проверить публикацию Pages и закрыть выполненную задачу68–69; исходная задача17/18 остаётся с blocked imagegen отдельного Стича

## Контрольная точка

# Референсы, Relay и Продолжай — открытый Work · 27.10.2026

work_id: OPEN-WORK-REFS-RELAY-20261027
Проверено: 2026-10-27T21:34:40Z. Открытый Work c8084d939274; локальный session_id не является ID чата. Канон — GitHub main; точные SHA и доказательства — reports/open-work-refs-relay-2026-10-27.json.

Завершено: пять новых PNG16:9 — улица66 с Алиной, Дашей и Стичем; бригада68 с точной надписью «ГБУ ЖИЛИЩНИК» / «РАЙОНА ТАТУИНА»; световая метла; композиция уборки68; мастер-класс Маши69. Каждый оригинал, миниатюра, манифест, галерея и checkpoint сохранены отдельным коммитом с точным readback до следующего принятого кадра. Новые файлы перечислены в отчёте с коммитами. Развёртки Алины/Даши/Маши и спор Маши уже существовали; повторно не создавались. Всего проверено25 разных файлов; исходная задача17/18 (ЦПК10/10, Серёгиус64–67:7/8); новая задача68–69:5/5. Роскосмос не переписывался, его пауза сохраняется.

Интеграция: слоты и SHA привязаны в существующих семи пунктах52P7/64–69; старые ожидания фотографий сняты, собака в52P7/66 заменена на Стича, Маша закреплена в финале66 как @Image6. Композиции68/69 — только галереи/helpers, без новых входов. Настоящие @Video1 по-прежнему требуют реальных результатов и QC; отсутствующий отдельный Стич не отмечен доступным. Очередь не расширялась, видео и платные инструменты не запускались, художественная приёмка не выставлялась. Состояния64/65 не повышены до запуска.

Relay6adc585e обновлён и прочитан обратно дословно: при временном сбое браузера до Create —1–2 повтора чтения/доступа с паузой около минуты; далее честный retryable blocked_browser, checkpoint и свежая проверка в следующем wake/часовом цикле. Неизвестный Create никогда не повторять. Сохранены прежняя единственная подписка relay.message/{} и часовое задание6acae6ab. Правило открытого Work добавлено в CONTINUE/OWNER-TASKS и канонический шаблон: «Продолжай» включает открытые Work-only задачи, фоновые handlers их не берут. Фактические настройки Project UI не проверялись; будущий browser retry не имитировался и пока не подтверждён реальным run.

Проверки: 348 unit tests, site contract, canon health ok/warnings0, сертификат7/7, live instruction consistency;16 инвариантов интеграции и независимый read-only review. Квитанция реального приёма текущим Work уже сохранена в reports/handoff-receipts.json (seregius-open-work-20261027-c8084d939274). Проверка нового будущего чата отдельно не подменяется этой записью.

Единственный блокер: references/scenes/scene-66/S66-alien-dog.png отсутствует. Три попытки отдельного портрета Стича отклонены builtin imagegen, output moderation category other, без конкретной причины; request IDs сохранены в отчёте. Улица со Стичем успешно создана, но не подставляется как ложный отдельный референс. В этом проходе повторных попыток больше нет.

Следующий шаг: завершить публикацию/Pages и закрыть только полностью выполненную задачу claude-202610272340-s68-69-refs с result_commit. Исходную claude-202610271320-cpk-refs оставить незавершённой из-за отдельного Стича. Далее открытый Work продолжает с этого конкретного блокера после восстановления доступного способа генерации;25 сохранённых файлов, интеграцию и Relay повторно не делать. Фокус сохраняется на текущей незавершённой работе.

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

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 39

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
