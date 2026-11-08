# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-08T07:26:23+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Сохранено новое поручение; общий аудит отсортирован по приоритету и готовности без повторных задач. Выполнение сайт/TLS/HONOR остаётся открытым.
Следующий шаг: Проверить живые слоты; при наличии места только готовый разрешённый item Unlimited0/CAS. Выполнить A-32 (порядок видео), A-20 (Pages/TLS), A-09/A-08 (конкурс и референсы HONOR), A-07 (RESOURCE QC), A-21/A-31 (Rutube/YouTube). Перед удалением MP4 подтвердить воспроизведение и сохранность исходника. Keep на паузе; готовые файлы/инструкции не дублировать.

## Контрольная точка

# 08.11.2026 — новые срочные поручения и точный порядок видео

work_id: TOPVIEW-SLOT-PRIORITY-20261024

- Новое поручение владельца 08.11: отсортировать планы, отметить выполненное, точный порядок шести видео; срочно Youtube→Rutube, HTTPS, HONOR/конкурс. Это начальная точка, не отчёт о завершении.
- Сохранены IDs A-01…A-30, добавлены A-31/A-32; оригинальные решения и пауза Keep сохранены.
- Доказательство: reports/owner-followup-2026-11-08.json.
- Следующий шаг: Проверить живые слоты; при наличии места только готовый разрешённый item Unlimited0/CAS. Выполнить A-32 (порядок видео), A-20 (Pages/TLS), A-09/A-08 (конкурс и референсы HONOR), A-07 (RESOURCE QC), A-21/A-31 (Rutube/YouTube). Перед удалением MP4 подтвердить воспроизведение и сохранность исходника. Keep на паузе; готовые файлы/инструкции не дублировать.

checked_at: 2026-11-08T07:26:23+00:00

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
- `ops/FUTURE-PLANS.md`
- `projects/raznoe/HANDOFF.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 55
- S49B: reconcile_without_resubmitting

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
