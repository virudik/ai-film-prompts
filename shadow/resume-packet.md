# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-15T11:26:06+00:00
Задача: SEREGIUS-SHIFT-20261113-T611U — Смена 13.11 t611u: очередь 48.4 и 89, отзыв по версиям Grok

Последний подтверждённый этап: В браузере владельца подтверждены 6 задач в очереди и существующая 89A (425108630b0e48c9a4b299fc89ad88ee). Точный промпт 89B и все пять исходников проверены по SHA и визуально. HH:55 снова включена и перечитана. Create/claim/intent в этом чате не выполнялись.
Следующий шаг: При следующей проверке начать с фактической общей ёмкости и свежего main. 89A уже submitted: не повторять. Следующий кандидат — S89B-WAN30, затем живая очередь. Перед Create заново проверить все доски, unknown/claims/task IDs, решения владельца, точные SHA пяти исходников/master, текущую форму Wan 3.0/30с/720p/16:9/1/Unlimited0, свой замок/CAS claim+intent/readback; один Create. Сейчас 6/6 занято. Проверить фактический следующий HH:55 runtime: enabled не доказывает успешную проверку или запуск.

## Контрольная точка

# 15.11.2026 — Work: 89A уже отправлена, 89B проверена, занято 6/6

work_id: SEREGIUS-SHIFT-20261113-T611U

- Полный приём смены после несовпадения первоначального брифа со свежим main; 7 инструкций и живые статусы проверены. Бриф затем сошёлся.
- В браузере владельца подтверждены 6 задач в очереди и существующая 89A (425108630b0e48c9a4b299fc89ad88ee). Точный промпт 89B и все пять исходников проверены по SHA и визуально. HH:55 снова включена и перечитана. Create/claim/intent в этом чате не выполнялись.
- Браузерный осмотр охватил доску My First Board и детали 89A, не все страницы аккаунта. Шесть видимых активных карточек подтверждают отсутствие свободного слота; снимок робота 2026-11-15T11:20:31Z также показывает 6/6 (light scan, complete=false). Нового полного скана для запуска не заявляем.
- Старый blocked_browser относится к предыдущей попытке. В этом интерактивном Work вход доступен; состояние других фоновых сред из этого не выводится.
- Существующая HH:55 6acae6ab433481919e88665c520b8ef2 включена 2026-11-15T11:21:13.909242+00:00, read-back enabled=true. Prompt/расписание сохранены, Relay и ordinary не менялись. Причина выключения неизвестна; следующий успешный runtime ещё не подтверждён.
- 89B: все пять полных канонических файлов скачаны, SHA/форматы/размеры и роли просмотрены; промпт 3724 символа, SHA совпал. Загрузка формы/Unlimited для 89B не проверялись.
- Свой foreground Work принят по прямому «Продолжай»; другие peers, route_generation, claims и очередь сохранены. Новых owner tasks/решений pending нет, историческое needs_owner Grok не изменено.
- Следующий шаг: При следующей проверке начать с фактической общей ёмкости и свежего main. 89A уже submitted: не повторять. Следующий кандидат — S89B-WAN30, затем живая очередь. Перед Create заново проверить все доски, unknown/claims/task IDs, решения владельца, точные SHA пяти исходников/master, текущую форму Wan 3.0/30с/720p/16:9/1/Unlimited0, свой замок/CAS claim+intent/readback; один Create. Сейчас 6/6 занято. Проверить фактический следующий HH:55 runtime: enabled не доказывает успешную проверку или запуск.
- Доказательства: `reports/topview-queue-2026-10-16/continue-20261115-work-248a657f.json`.

checked_at: 2026-11-15T11:26:05+00:00

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
- `ops/TOPVIEW-FREE-LAUNCH.md`
- `reports/current-work-checkpoint.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 91

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
