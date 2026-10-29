# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-29T04:43:34+00:00
Задача: SEREGIUS-PLAN-20261023 — Завершить Серёгиус по сохранённому плану, оценить готовые ролики

Последний подтверждённый этап: Возвращён @Image6 в три промпта68, manifest, registry, галерею и очередь; SHA сверены, PNG не менялись. Подтверждены три необязательные прогулки Стича и одна новая попытка IMAGE-1 после отказа; 6 видео активны, новых запусков нет.
Следующий шаг: При освобождении видеослота отправить S66-STITCH-NB-IMAGE-1 → -2 → -3 подряд по одному подготовленному промпту, Unlimited0, с отдельным claim/taskID/receipt и проверкой image-capacity после каждого клика, без ожидания результатов. IMAGE-1 заново разрешён владельцем после отказа без taskID. Новые изображения необязательны для видео: использовать существующий общий кадр по умолчанию, выбор новых — после просмотра владельцем. S68 использует @Image1–6 плюс настоящий конец67; затем прежняя готовая видеоочередь. Роскосмос на паузе.

## Контрольная точка

# Сцена 68: шесть входов; Стич: необязательная пробная тройка · 28.10.2026

work_id: SEREGIUS-PLAN-20261023
work_id: TOPVIEW-SLOT-PRIORITY-20261024

Проверено: 2026-10-28T16:32:18+00:00.

Возвращён @Image6 в три промпта68, manifest, registry, галерею и очередь; SHA сверены, PNG не менялись. Подтверждены три необязательные прогулки Стича и одна новая попытка IMAGE-1 после отказа; 6 видео активны, новых запусков нет.

Новое решение владельца заменяет прежнюю запись «композиция68 только в галерее» и прежнее ожидание разрешения IMAGE-1. @Image6 задаёт расположение и масштаб; индивидуальные листы — внешность и реквизит; настоящий @Video1 и таймлайн — старт, включение мётел и появление Маши. Никакой перерисовки.

При освобождении видеослота отправить S66-STITCH-NB-IMAGE-1 → -2 → -3 подряд по одному подготовленному промпту, Unlimited0, с отдельным claim/taskID/receipt и проверкой image-capacity после каждого клика, без ожидания результатов. IMAGE-1 заново разрешён владельцем после отказа без taskID. Новые изображения необязательны для видео: использовать существующий общий кадр по умолчанию, выбор новых — после просмотра владельцем. S68 использует @Image1–6 плюс настоящий конец67; затем прежняя готовая видеоочередь. Роскосмос на паузе. Оценка владельца около10мин не является гарантией сервиса. История отказа сохранена в receipt и архиве, attempts_used не обнулён.

Доказательства: `reports/s68-composition-and-stitch-policy-2026-10-28.json`.

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

- `ops/TOPVIEW-FREE-LAUNCH.md`
- `ops/CONTINUE-PROTOCOL.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 40

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
