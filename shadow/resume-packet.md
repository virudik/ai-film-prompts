# Продолжай — пакет восстановления Серёгиуса

Производный навигатор. Сначала свежий main и `scripts/continue_preflight.py`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-27T14:04:37+00:00
Задача: CONTINUE-MULTIPROJECT-20261027 — Продолжай: все проекты и квитанция приёма

Последний подтверждённый этап: Прочитаны состояния пяти проектов и получены замки
Следующий шаг: Реализовать проектные пакеты и квитанцию приёма, затем проверить все пять проектов.

## Контрольная точка

# Продолжай — ДО: все проекты и квитанция приёма · 27.10.2026

work_id: CONTINUE-MULTIPROJECT-20261027
Время: 2026-10-27T14:03:47.252Z. Команда владельца: распространить механизм на остальные проекты; добавить квитанцию — какой чат принял, что проверил, с какого действия продолжил.
Проверено: Серёгиус имеет пакет; у четырёх остальных его нет. Котмонавты и Кот детектив ждут выбора владельца, Разное пустое. Роскосмос: видео на паузе, подготовка референсов ЦПК остаётся отдельной задачей открытого Work-чата. Все пять замков взяты для этой инфраструктурной работы. Новых видеозапусков нет.
План: обособленные фокус/idle, checkpoint и пакет каждого проекта; проверка изоляции и пауз; квитанция реального приёма с идентичностью чата, проверками и первым выполненным действием; сайт, существующий workflow, тесты, main/readback, снятие замков. Нельзя выдавать миграцию файлов за приём смены пятью чатами.
Следующий шаг: реализовать проектные пути и квитанцию, затем проверить все пять проектов.

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
- `projects/README.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 39

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
