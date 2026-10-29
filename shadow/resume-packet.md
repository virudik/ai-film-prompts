# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-29T08:17:07+00:00
Задача: SEREGIUS-PLAN-20261023 — Завершить Серёгиус по сохранённому плану, оценить готовые ролики

Последний подтверждённый этап: Closed failed Stitch trials; scoped S62 uncertainty; corrected S59P2 task b0915b04173c414e9ac08652d34b7852 confirmed Unlimited0; six active videos.
Следующий шаг: Fresh owner decisions/main/lock/full all-board scan. Keep S62 unknown claim and reconcile without repeating; independent ready items continue. Six videos active at08:09UTC. On capacity choose minimum-priority ready authorized video, currently S60-SEED20-P1. Stitch trials closed; no retries. On actual S59P2 success perform QC and extract real continuity for P3.

## Контрольная точка

# Topview: очередь продолжена без проб Стича · 29.10.2026

work_id: SEREGIUS-PLAN-20261023
work_id: TOPVIEW-SLOT-PRIORITY-20261024

Проверено 2026-10-29T08:09:07.085Z. По команде владельца три failed пробы Стича закрыты cancelled_owner; повторов и использования в видео нет. Продолжаем с существующими референсами; шесть входов S68 сохранены.

Причина простоя: после таймаута Create S62 в06:11–06:13UTC Relay/hourly распространили неопределённость одной отправки на всю очередь. Полные сканы13досок показывали5активных видео. Исходный claim S62 и submission_unknown сохранены, повторять её нельзя; блокировка уточнена до S62 и её зависимых частей. Независимые готовые сцены заполняют проверенные свободные слоты.

S59-SEED20-P2 отправлена в08:07:31UTC (11:07МСК), task b0915b04173c414e9ac08652d34b7852. Seedance2.0/15s/720p/16:9/quantity1/Unlimited0, creditsCost0. Полный нормализованный prompt совпал; Video1=реальные3с, Image1=финальный кадр, Image2=лесной кроп, Image3=корабль. Байты исправленного Image2 повторно скачаны из принятой задачи и совпали с upload SHA. Полный финальный скан13досок/19страниц/943задач: 6активных видео, 0изображений, свободных слотов0.

Ошибка этого рабочего чата сохранена прозрачно: первая задача9b2e18c883e3401e9b13b2930b3b570c ошибочно получила корабль вместо леса; отменена до рендера (UI Отменено, provider fail, стоимость0). Причина: пропущен отказ загрузки леса1280x240 по minimum300px / maximumaspect2.50. Создана только техническая обёртка1280x720 с нейтральными серыми полями; исходный кроп целиком, без масштабирования, обрезки и AI-дорисовки. Единственная корректирующая отправка подтверждена; budget дальнейших попыток0. Это не разрешение будущих автоматических повторов.

Дальше: при новом слоте свежие owner decisions/main/замок/полный скан; S62 сверять отдельно без повтора, выбирать следующий независимый готовый item по priority (сейчас S60-SEED20-P1). Стича не возобновлять. После success S59P2 — проверить результат и подготовить настоящий стык для P3, художественную приёмку не подменять техническим success. Роскосмос на паузе.

Доказательства: reports/topview-queue-2026-10-16/S59-SEED20-P2-20261029.json и .jpg; upload_derivative — manifest59. Эта запись заменяет прежний общий запрет отправок до выяснения S62 и старый план трёх проб Стича.

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

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 44
- S62-SEED20-P1: reconcile_without_resubmitting

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
