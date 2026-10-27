# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-10-27T19:05:11+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# Референсы, Relay и Продолжай — открытый Work · 27.10.2026

work_id: OPEN-WORK-REFS-RELAY-20261027
Проверено: 2026-10-27T18:59:31+00:00. Выполняет открытая сессия Work beb26cfe80f8; это локальный session_id, ID чата среда не раскрыла.

Команда владельца: лично нарисовать 18 референсов задачи claude-202610271320-cpk-refs; по новым фото также развёртки Алины (фото1), Даши (фото2–3) и Маши Р (фото4) в татуинской одежде и сценические кадры. Собака теперь Стич. Последнее уточнение отменяет старое ожидание фотографий. В очередь ничего не добавлять, видео не запускать. Починить повтор при временном сбое браузера в Relay 6adc585e; расширить Продолжай на задачи только открытого Work.

Доказано: 10/10 PNG ЦПК 21–25 опубликованы, реестр/галереи/манифесты и handoff Роскосмоса обновлены (итог 15111686b215e7e88a852a3c4f8e7046a37ce5c6). Пауза и очередь Роскосмоса сохранены. S64-коридор и офицеры опубликованы (57e8e3c2, c4501d29); S65-стол сохранён текущим согласованным коммитом, точная внешность Серёги взята из references/full/serega.jpg. Художественное принятие не выставлено.

Осталось: тост S65, Стич/улица S66, прилавок/продавец S67, три индивидуальные развёртки и сценические кадры; затем маппинг/SHA/available только существующих изображений, при этом реальные видеостыки остаются зависимостями. После изображений исправить протокол и живой prompt Relay с сохранением подписки и readback; добавить открытые Work-задачи в Продолжай; проверки, итоговый result_commit и status done. Начатые или сохранённые изображения не рисовать повторно. Следующий шаг — S65-toast-closeup.image-prompt.txt.

Блокеры: постоянных нет. CLI git push не авторизован; запись успешно выполняется GitHub-коннектором с FF/CAS и readback. Первая генерация S65 отклонена инструментом; спокойная композиция без оружия успешно получена. Созданий видео, смен расписания и фальшивых Relay ACK нет.

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


## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 39

## Пробелы

- recovery evidence changed: references/scenes/scene-65/manifest.json
