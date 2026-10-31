# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-31T11:17:06+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: S72-WAN30 отправлена одним бесплатным веб-Create; подтверждён task22dbd25cdd9f47cd9e44300e55f5e44f и полный prompt/settings/input preflight. Полный postscan14 досок/18 страниц/624 видео:6/6 активны, дублей нет.
Следующий шаг: При следующем цикле заново проверить свежий main, решения/замок, существующие task IDs и полную глобальную ёмкость Topview. Если есть свободный слот, первой готовой S71-WAN30 (Wan 3.0,30с,Unlimited0), затем S56-SEED20-P2 по живому priority и входам. S72 наблюдать по task22dbd25cdd9f47cd9e44300e55f5e44f, не повторять. Ожидающее реальный результат продолжение пропускать без резервирования слота; свободные слоты заполнить разрешёнными готовыми items.

## Контрольная точка

# Продолжай: S72 запущена, 6/6 слотов · 31.10.2026

work_id: TOPVIEW-SLOT-PRIORITY-20261024

По команде «Продолжай» выполнен приём D7 и продолжена выбранная разрешённая очередь. Исходный checkpoint опубликован `4335361422df924b4c905be6375ba4695becd1fa`; перед отправкой сохранён и прочитан обратно CAS-claim `6a44f5af81b1b961296c258fe814e51994cbb832`.

31.10.2026 в 14:08:48 МСК (11:08:48Z) ровно один Create отправил **S72-WAN30**, пролог «Всем привет». Подтверждён task `22dbd25cdd9f47cd9e44300e55f5e44f`, My First Board `1a6244cf1ae747ef847d949a80d6133c`: Wan 3.0 · 30 с · 720p · 16:9 · 1 ролик · native audio on · Unlimited=true · credits=0, статус `init`. Четыре канонических изображения загружены в порядке @Image1–4; канонический текст 7136 символов совпал с UI, нормализованный backend-текст совпал полностью (SHA256 `157f5a30640f72712001d5ff40efbb181e6ad42ccbcc75cf179fb337ca7366f1`). Расходы 0. Это подтверждение отправки, не готовый ролик и не редакционная приёмка.

Повторный полный scan 2026-10-31T11:09:40Z: 14 досок, 18 страниц видео, 624 уникальные задачи, ошибок 0; активны 6/6, свободных слотов 0. Единственная новая видеозадача — указанная S72; дублей нет. Остальные активные: S61-P1, S60-P1, S62-P1, S59-P2 и S52-R2-P1. S48-P1 ранее завершилась технически; её приёмка/повтор не выполнялись. Телеметрию продолжает писать GitHub-робот, старые результаты не подменяются текущим снимком.

Следующий шаг: При следующем цикле заново проверить свежий main, решения/замок, существующие task IDs и полную глобальную ёмкость Topview. Если есть свободный слот, первой готовой S71-WAN30 (Wan 3.0,30с,Unlimited0), затем S56-SEED20-P2 по живому priority и входам. S72 наблюдать по task22dbd25cdd9f47cd9e44300e55f5e44f, не повторять. Ожидающее реальный результат продолжение пропускать без резервирования слота; свободные слоты заполнить разрешёнными готовыми items.

Доказательства: `reports/topview-queue-2026-10-16/S72-WAN30-20261031T110848Z.json` и `reports/topview-queue-2026-10-16/S72-WAN30-postscan-20261031.json`. Нижняя исходная точка «Create 0» и прежние снимки сохранены как история этапов, а не текущее состояние.

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
- `references/scenes/scene-71/manifest.json`
- `references/scenes/scene-56/manifest.json`
- `ops/TOPVIEW-FREE-LAUNCH.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 48

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
