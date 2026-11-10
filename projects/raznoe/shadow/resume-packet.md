# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project raznoe`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-10T23:34:06+00:00
Задача: RAZNOE-HONOR-X9EPRO-CONTEST-20261107 — RAZNOE-HONOR-X9EPRO-CONTEST-20261107

Последний подтверждённый этап: Шесть существующих ИИ-PNG и6 превью привязаны к сценам4/5; все36+3 промпта используют реальные источники точной модели. Drive6/6 совпали. Тесты550/550; сайт ещё ждёт точного readback.
Следующий шаг: Завершить Pages и точный readback всех файлов; не пересоздавать изображения. Затем только отдельно разрешённые видео, реальные хвосты/QC и конкурсная съёмка; приёмку не подменять.

## Контрольная точка

# 11.11.2026 — реальные модели и шесть референсов HONOR4/5

work_id: RAZNOE-HONOR-X9EPRO-CONTEST-20261107

- Добавлены шесть существующих PNG без изменения байтов, 6 превью, карта реальных источников и 39 автономных привязок промптов. Новых генераций 0. 39 привязок проверены; 550 тестов и валидаторы пройдены. Проверка выдачи сайта ещё ожидается.
- Сделанное не повторять. Официальные источники не подменены ИИ-рисунками. H-GEN-PAIR только сравнение; X-GEN-MOSCOW архив без использования.
- Следующий шаг: полный набор тестов, статус проекта, публикация и точный readback сайта/Drive; отдельно остаются видео, реальные стыки, приёмка и физический конкурс.

checked_at: 2026-11-10T23:31:21+00:00

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

- `projects/raznoe/references/scenes/scene-4/reference-bindings.json`
- `projects/raznoe/references/scenes/scene-5/reference-bindings.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 0

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
