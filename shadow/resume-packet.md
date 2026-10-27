# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-27T22:07:44+00:00
Задача: OPEN-WORK-REFS-RELAY-20261027 — 18 референсов, персонажи по фото, повтор Relay и открытые Work-задачи

Последний подтверждённый этап: Все18 референсных ролей обеспечены: существующий кадр подключён как Стич; отдельная генерация снята
Следующий шаг: Опубликовать повторное использование Стича, проверить сайт и закрыть исходную задачу и текущую работу

## Контрольная точка

# Референсы, Relay и Продолжай — открытый Work · 27.10.2026

work_id: OPEN-WORK-REFS-RELAY-20261027
Проверено: 2026-10-27T22:07:17Z. Канон — GitHub main. Полный отчёт и история попыток: reports/open-work-refs-relay-2026-10-27.json.

Уточнение владельца28.10: «Есть же фото Стича с девочками, её недостаточно? из этой фотки сделать нельзя ?». Существующий references/scenes/scene-66/S66-street-outrage.png (SHA256 548388e01ccdd1b98f89284ed23fb5c00718656d655732a65308c7886b70218b) проверен визуально: Стич целиком в переднем плане, лицо, голубая шерсть, уши и красная шлейка различимы. Этот неизменённый кадр используется как референс внешности Стича; отдельная генерация больше не нужна. Файл S66-alien-dog.png не создан и не объявлен существующим. История четырёх отказов imagegen сохранена; закрывается требование отдельного файла, не заявляется исправление генератора.

Все18 требуемых референсных ролей обеспечены:10 ЦПК и8 Серёгиуса, из них17 исходных отдельных PNG и повторное использование готовой улицы для роли Стича. Всего25 разных проверенных изображений с учётом развёрток и дополнительных композиций. В предыдущем этапе созданы5 кадров: улица66, бригада68 с точной надписью, световая метла, уборка68 и мастер-класс Маши69; оригиналы, миниатюры и галереи опубликованы и проверены. Задача68–69 уже закрыта.

Привязка Стича: в52P7 @Image3 — существующий уличный кадр, внешность девочек — по отдельным sheets. В66 тот же кадр один раз в @Image3 задаёт Стича и улицу; @Image1 Алина, @Image2 Даша, @Image4 прилавок, @Image5 Маша. Обновлены все соответствующие версии промптов, маппинги, SHA и галереи. Реальные @Video1 и QC будущих стыков остаются обязательными; новых элементов очереди, видео, платных действий и художественных одобрений нет.

Relay retry и «Продолжай» в открытом Work завершены ранее и не менялись: повтор доступа к браузеру1–2 раза около минуты до Create, сохранение причины и продолжение при настоящем следующем wake; Work-only задачи исключены из фоновых handlers. Прежняя единственная подписка и часовой монитор сохранены. Настройки Project UI и будущий реальный browser retry отдельно не подтверждались.348 тестов и сайт прошли предыдущую полную проверку; текущая минимальная привязка проверяется отдельно.

Текущий этап: повторное использование применено локально. Следующий шаг — commit/readback, точная проверка сайта, закрытие исходной claude-202610271320-cpk-refs и перенос текущей работы в завершённые с возвратом фокуса на SEREGIUS-PLAN-20261023. Возврат фокуса не означает запуска видео в этом поручении.

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
