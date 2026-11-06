# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-06T12:14:12+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Прочитан linked-chat, повторно проверены14досок/630видео/6слотов и15submitted; фактический HH:55 после включения подтверждён, подготовлен план восстановления несохранённых стыков.
Следующий шаг: Сохранить проверенные материалы S60/S61 из предыдущего Work; затем закрыть доступные задачи linked-chat: параллельные инструкции/план, кнопка и HTTPS, технические правки HONOR/RESOURCE. Keep продолжить после защищённого входа Google. При свободном слоте — свежий полный preflight, первая готовая разрешённая сцена по priority; submitted/unknown не повторять.

## Контрольная точка

# 06.11.2026 — продолжение связанного Work-чата и сохранение стыков

work_id: TOPVIEW-SLOT-PRIORITY-20261024

- Команда владельца: продолжить канон, после доделать share6aedc24c. Ссылка прочитана, задания сверены с main.
- Короткий D7 приём: valid15/15, ready_for_resume=true; owner_decisions без pending/in_progress, открытых/взятых owner tasks нет. Для изменения общих инструкций выполняется полное командное чтение7документов.
- Собственный свежий read-only скан:14досок/18страниц/630видео,6/6, все15submittedID найдены, unresolved claims0, новых Create0. Монитор skip; телеметрия робота не переписывалась.
- HH:55 после восстановления действительно выполнился: run5875bfa9…, завершён06.11 12:01UTC,6/6; собственная квитанция того фонового цикла не сохранена из-за чужого lock. Причина прежнего отключения не установлена.
- Несохранённые S60/S61 найдены и проверены технически; это ещё план переноса в main, не объявленный опубликованный результат.
- Keep: защищённый вход Google требуется, заметки в этом чате не изменялись, существующий checkpoint обновлён доv44.
- Исходный план и факты: reports/work-continue-linked-chat-2026-11-06.json.

Следующий шаг: Сохранить проверенные материалы S60/S61 из предыдущего Work; затем закрыть доступные задачи linked-chat: параллельные инструкции/план, кнопка и HTTPS, технические правки HONOR/RESOURCE. Keep продолжить после защищённого входа Google. При свободном слоте — свежий полный preflight, первая готовая разрешённая сцена по priority; submitted/unknown не повторять.

checked_at: 2026-11-06T12:14:12+00:00

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

- `ops/LAUNCHER-COORDINATION.md`
- `ops/TOPVIEW-FREE-LAUNCH.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 54

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
