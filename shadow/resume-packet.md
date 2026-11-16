# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-16T00:03:53+00:00
Задача: SEREGIUS-SHIFT-20261113-T611U — Смена 13.11 t611u: очередь 48.4 и 89, отзыв по версиям Grok

Последний подтверждённый этап: dot изучил инструкции через отдельный аудит, проверил D7 и полный read-only скан 14 досок/19 страниц/676 видео: 6/6 активных Unlimited0. 89A уже submitted, следующая 89B. Подтверждены действующие HH:00/HH:55/Relay и успешный архив. Бесплатная авторизованная форма в текущем браузере проверена до Create; отправок нет.
Следующий шаг: Повторить свежий main/решения владельца и полный глобальный скан перед запуском. Не повторять 89A. При свободном слоте следующий кандидат S89B-WAN30: точные исходники/SHA/master, полный UI-preflight Wan3/30с/720p/16:9/1/Unlimited0, собственные lease/CAS claim+intent/readback, один Create. HH:55 runtime 11:55 UTC подтверждён completed в 12:09:49 UTC. Расписания остаются в прежних чатах, перенос к dot не заявлен.

## Контрольная точка

# 15.11.2026 — dot: приём смены, инструкции изучены, очередь сверена

work_id: SEREGIUS-SHIFT-20261113-T611U

- Проверка восстановления D7: 15/15 якорей и SHA восьми канонических источников совпали; ready_for_resume=true.
- Полный скан Topview 2026-11-15T12:06:17.559Z: 14 досок, 19 страниц, 676 видео; шесть активных init, Unlimited=true, creditsCost=0. Следующая S89B-WAN30; 89A уже submitted.
- Входящие GitHub open/taken/needs_owner=0. Supabase pending/in_progress=0; историческая needs_owner 01.11 сохранена.
- HH:00 реально отработала 15.11 11:00 UTC; HH:55 включена; runtime 11:55 UTC завершился в 12:09:49 UTC, квитанция в main: no_free_slot, 6/6, Create=0. Relay включён, его прежний blocked_browser — исторический результат. Автоматизации не переносились в dot и не менялись.
- Архив run 43709625696 успешен, включая Copy and verify completed videos; Pages успешен.
- В текущем браузере dot подтверждены вход, My First Board и выбранный бесплатный Unlimited для Wan3/30с/720p; шесть видео в очереди. Create не нажат. Доступ к форме не выдаётся за доказательство отправки или возможности любого фонового runtime.
- Первая запись lock была отклонена проверкой безопасности и не попала на GitHub. Затем владелец явно разрешил служебную запись. Чужая HH:55 lease соблюдена; приём сохраняется только под собственной свежей lease.
- Сцены, промпты, очередь, task IDs, приёмка, retry budgets, расписания и роль робота не изменены. Новых видео и расходов нет.
- Инструкции: полный аудит семи канонических документов и INSTRUCTIONS/HANDOFF четырёх дополнительных проектов подтверждён корневым агентом. Master/backlog изучены по текущей задаче; полного просмотра всех промптов и референсов не заявляем. Приём квитанции относится к Серёгиусу; отдельные проектные квитанции и замки этой записью не создаются.
- Доказательства: `reports/topview-queue-2026-10-16/dot-takeover-20261115-a83fdec7.json`. Следующий шаг: Повторить свежий main/решения владельца и полный глобальный скан перед запуском. Не повторять 89A. При свободном слоте следующий кандидат S89B-WAN30: точные исходники/SHA/master, полный UI-preflight Wan3/30с/720p/16:9/1/Unlimited0, собственные lease/CAS claim+intent/readback, один Create. HH:55 runtime 11:55 UTC подтверждён completed в 12:09:49 UTC. Расписания остаются в прежних чатах, перенос к dot не заявлен.

checked_at: 2026-11-15T12:15:31+00:00

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
Задач с сохранённым task ID: 92

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
