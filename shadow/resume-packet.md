# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-27T18:14:24+00:00
Задача: SEREGIUS-PLAN-20261023 — Завершить Серёгиус по сохранённому плану, оценить готовые ролики

Последний подтверждённый этап: Сцена52: семь частей, промпты, референсы и очередь подготовлены. Механизм «Продолжай» и квитанции внедрены во всех пяти проектах; исходящая смена сохранена. Реальная приёмка новым чатом остаётся открытой.
Следующий шаг: Принять смену по свежему main и сохранить собственную квитанцию; затем проверить результаты/QC, решения владельца и общие live-слоты. Продолжить разрешённую очередь Серёгиуса: новая S52-R2-P1 при свободном слоте, P2–P7 после реального результата и QC предшественника. Существующие task ID не отправлять повторно. Новая конкретная команда владельца приоритетнее этого фокуса.

## Контрольная точка

# Передача смены по просьбе владельца · 27.10.2026

work_id: SEREGIUS-PLAN-20261023
Сохранено: 2026-10-27T14:46:23+00:00. Канон: GitHub virudik/ai-film-prompts:main. Это исходящая контрольная точка текущего Work-чата, не квитанция будущего сменщика. Точный conversation ID среда не раскрыла; локальная сессия work-dbcaa6ee-3f43-40ac-bc62-acb19d667f43 не является ID чата.

Завершено и не требует повторного выполнения:
- «Продолжай» распространён на все пять проектов; у каждого свои focus/idle, checkpoint, пакет и журнал квитанций. Проверены изоляция проектов, UI пяти проектов, CI и точный readback опубликованных файлов. Коммиты 76bac689, 5589ee78, итог 1749b960. Подробности и проверки: reports/continue-multiproject-2026-10-27.json (347 тестов полного прогона; 43 проверки окончательных изменений).
- Квитанция принятия текущей задачи записана в reports/handoff-receipts.json: continue-multi-20261027-current-work. Сохраняются 20 актуальных квитанций, старые архивируются; незавершённые и idle checkpoints защищены от чистки. Новому чату нужна собственная квитанция после фактических проверок и первого действия. Реальная приёмка новым чатом ещё не выполнена: issue #9 остаётся открытым.
- Сцена 52 подготовлена: семь частей, промпты, референсы и очередь R2P1–P7. Начало — выбранный конец ремонта крыла из Scene44 Seedance2.5. Это готовность материалов, не готовность семи видео; подробности reports/scene52-seven-parts-handoff-2026-10-27.md. В инфраструктурной работе и сохранении этой точки новых видео не запускали.

Текущее состояние и ограничения:
- Явный фокус остаётся SEREGIUS-PLAN-20261023. Последний прочитанный topview-status.json: 2026-10-27T14:00:20Z, занято 6/6; robot-status — 14:30:19Z. Это сохранённая телеметрия, не новый live scan и не основание для запуска.
- Котмонавты и Кот детектив ждут решения владельца; Разное (misc) ждёт материалов. Роскосмос (raznoe): видео на паузе. Во входящих claude-202610271320-cpk-refs — 10 референсов ЦПК для сцен21–25; задача только для открытого ChatGPT Work по передаче владельца, не для часового/Relay. Здесь она не взята и не выполнена.
- Последний запрос владельца также касается возможностей разбора заметок. Прямых Keep/Evernote подключений не обнаружено; доступны разбор экспорта Keep (Takeout) и Evernote (ENEX/HTML), работа через Notion и подтверждённое подключение OneNote. Pocket закрыт, возможен разбор ранее сохранённого экспорта. Содержимое заметок не читали и не меняли; сервис и объём чистки ещё не выбраны. Это не разрешение на массовое удаление и не новая задача очереди фильма.

Дальнейшие действия сменщика:
1. Получить свежий main, выполнить ops/CONTINUE-PROTOCOL.md и continue_preflight.py; для другого проекта указать --project ID. При несовпадении — полный приём семи инструкций. Проверить текущие решения владельца, входящие, замок и состояние внешних задач; сохранить собственную честную квитанцию приёма по фактически выполненным проверкам/первому действию.
2. Если владелец не дал новую приоритетную задачу, продолжить разрешённое производство Серёгиуса: свежие результаты/QC и общий live scan слотов; первая готовая новая S52-R2-SEED20-P1 — только при свободном слоте и выполненном preflight. P2–P7 требуют реального результата и QC предшественника. Сохранённые task IDs и неоднозначные submission не отправлять повторно; брать следующий действительно готовый разрешённый пункт очереди по правилам.
3. Зафиксировать фактический приём новым чатом в issue #9 после проверки; не объявлять его состоявшимся по зелёному индикатору или тестам. Подготовку сцены52 и многопроектного механизма заново не делать.
4. Разбор заметок начинать по следующей конкретной команде владельца: актуальные задачи, справочное, архив, дубликаты, спорные. Возраст сам по себе не доказывает ненужность. Не смешивать заметки и канон фильма.

Замок этой записи освобождается в том же итоговом коммите. Следующий чат не должен повторно брать завершённую CONTINUE-MULTIPROJECT-20261027 как активную работу.

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

Нет ошибок локальной проверки. Живые проверки выше обязательны.
