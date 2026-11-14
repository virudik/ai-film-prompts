# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-14T21:31:00+00:00
Задача: SEREGIUS-SHIFT-20261113-T611U — Смена 13.11 t611u: очередь 48.4 и 89, отзыв по версиям Grok

Последний подтверждённый этап: Вход Topview подтверждён на свежей странице с аккаунтом владельца. Промпт S89A-WAN30 и все пять локальных исходников совпали по SHA с каноном. Выбраны Wan 3.0 / 30с / 720p / 16:9 / 1 / «Безлимитный режим — бесплатно». Загрузка первого референса прервана; вкладка затем недоступна. claim/intent/Create=0, видео не отправлено.
Следующий шаг: Продолжить S89A-WAN30: проверить сохранение входа в свежей вкладке Topview и состояние импорта; прежний вызов загрузки прерван, Create никогда не вызывался. Взять точные исходники из канона/Drive (локальный кэш /workspace/shared/seregius-89a использовать только после повторной SHA-проверки), загрузить пять файлов по порядку и полный промпт. Затем fresh main/owner_decisions, полный свежий скан всех досок, свой замок, UI Unlimited0/720p/16:9/1, CAS-claim+intent/readback и один Create. Не повторять уже submitted S48-P4-R2 и S51E/F/G. При свободной ёмкости продолжать живую очередь.

## Контрольная точка

# 14.11.2026 — Work: вход подтверждён, загрузка 89A прервана до Create

work_id: SEREGIUS-SHIFT-20261113-T611U

- Команда владельца сохраняется: «Продолжай. Запускай по согласованной очереди»; затем «Дай форму ввода пароля».
- Последний подтверждённый этап: Вход Topview подтверждён на свежей странице с аккаунтом владельца. Промпт S89A-WAN30 и все пять локальных исходников совпали по SHA с каноном. Выбраны Wan 3.0 / 30с / 720p / 16:9 / 1 / «Безлимитный режим — бесплатно». Загрузка первого референса прервана; вкладка затем недоступна. claim/intent/Create=0, видео не отправлено.
- Полный скан 21:02:24Z: 14 досок, 19 страниц, 675 видео, занято 5/6. Это исторический снимок, перед отправкой скан обязателен заново.
- Внешняя lease ordinary была соблюдена; очередь, budgets, task IDs и foreground не изменялись. Робот остаётся primary; monitor_role=skip, heartbeat не писался.
- Импорт @Image1 документированным filechooser завершился «aborted by user»; последующее чтение вкладки 9 — Tab not found. Успешная загрузка не подтверждена. Нельзя выдавать подготовленную форму за запущенный ролик.
- Доказательства: reports/topview-queue-2026-10-16/auth-upload-20261114-work-5aa51c3f.json. Промпт и исходники не изменены.
- Причина прежнего несовпадения recovery SHA проверена по diff: Relay #678 обновил свой блок внутри прежнего checkpoint. Текущий этап привязан к отдельному новому верхнему разделу; правила D7 и скрипты не менялись.
- Следующий шаг: Продолжить S89A-WAN30: проверить сохранение входа в свежей вкладке Topview и состояние импорта; прежний вызов загрузки прерван, Create никогда не вызывался. Взять точные исходники из канона/Drive (локальный кэш /workspace/shared/seregius-89a использовать только после повторной SHA-проверки), загрузить пять файлов по порядку и полный промпт. Затем fresh main/owner_decisions, полный свежий скан всех досок, свой замок, UI Unlimited0/720p/16:9/1, CAS-claim+intent/readback и один Create. Не повторять уже submitted S48-P4-R2 и S51E/F/G. При свободной ёмкости продолжать живую очередь.

checked_at: 2026-11-14T21:23:52+00:00

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
Задач с сохранённым task ID: 90

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
