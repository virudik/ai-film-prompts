# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-31T11:09:10+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: D7 принят по свежему main; полный scan подтвердил 5/6 активных видео, S72 следующая без дублей; правильная UI-доска и Unlimited0 выбраны. Входы/полный промт ещё проверяются, Create не выполнялся.
Следующий шаг: Завершить получение и SHA256-проверку четырёх точных входов S72, загрузить их по порядку @Image1–4 и полный промт из master. Затем свежие main/слоты/отмены/Unlimited0, CAS-claim S72, один Create, сверка фактического task ID и receipt; после запуска пересчитать слоты. S71 следующая по живому priority.

## Контрольная точка

# Продолжай: приём D7 и подготовка S72 · 31.10.2026

work_id: TOPVIEW-SLOT-PRIORITY-20261024

Исходная контрольная точка перед запуском. Команда владельца: «Продолжай»; действующее решение 31.10 01:02 МСК ставит S72-WAN30, затем S71-WAN30 в начало очереди. Границы: выбранные канонические входы и промт, Wan 3.0 · 30 с · 720p · 16:9 · 1 ролик · Unlimited0; технический успех не означает приёмку.

Подтверждено: свежий main `cbe44aa326381a80d081ad7dba07d63c448f4832`, D7 short/preflight ready, 15/15 инвариантов и хеши мастера/семи инструкций совпали. Полный scan 2026-10-31T10:52:34Z: 14 досок, 18 страниц, 623 видео, ошибок 0; занято 5/6, свободен 1 слот. Все пять активных task IDs перепроверены напрямую; новых технических fail и дублей S71/S72 нет. S48-P1 завершилась success, без редакционной приёмки. Открытых owner tasks и owner_decisions нет. Робот остаётся основным писателем телеметрии; задание HH:55 включено, последний no_update сам по себе не доказывает запуск.

Первый фактический шаг выполнен: скан и сверка приоритетов; в авторизованном браузере открыта My First Board `1a6244cf1ae747ef847d949a80d6133c`, выбраны Wan 3.0/30s/720p/16:9/qty1 и «Безлимитный режим — бесплатно». Получение/проверка SHA четырёх файлов, их загрузка и сверка полного промта ещё не закончены. Create 0, claim нет, task ID нет, расходы 0. Собственный замок взят и прочитан обратно: `8ab8088e694cc53809506040c9a743bed8db9a9f`.

Следующий шаг: Завершить получение и SHA256-проверку четырёх точных входов S72, загрузить их по порядку @Image1–4 и полный промт из master. Затем свежие main/слоты/отмены/Unlimited0, CAS-claim S72, один Create, сверка фактического task ID и receipt; после запуска пересчитать слоты. S71 следующая по живому priority.

Доказательства: `reports/topview-queue-2026-10-16/S72-WAN30-preflight-20261031.json`. Историческая запись «6/6» ниже не является текущим состоянием.

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
- `references/scenes/scene-72/manifest.json`
- `ops/TOPVIEW-FREE-LAUNCH.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 47
- S72-WAN30: reconcile_without_resubmitting

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
