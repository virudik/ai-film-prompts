# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project misc`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-02T04:43:32+00:00
Задача: MISC-S1-S2-REFERENCES — 59 отдельных референсов сцен 1 и 2 из GPT-TASK.md

Последний подтверждённый этап: Проверка источников и трёх неудачных результатов сохранена; новых пригодных PNG 0, ранее нарисованное не перерисовывалось.
Следующий шаг: Recover original C2-C6 and resolve C7 without redrawing; check fresh inventory. Continue only missing separate images from number 8 after a single-image generation matches its exact prompt. Save verified originals and publish actual files only; no collage substitutes.

## Контрольная точка

# Разное — проверка повторов и блокер отдельных изображений · 02.11.2026

work_id: MISC-S1-S2-REFERENCES
Проверено: 2026-11-02T03:50:22Z
Статус: blocked_repeated_output_mismatch; задача не завершена.

Владелец разрешил дорисовать недостающее заходами по 10 и затем опубликовать. Прежде нарисованное не повторять. Загруженный GPT-TASK.md побайтно соответствует каноническому git blob 90d9ecb9983f2320a898a5f75f77215105da2b85 (59 изображений). Существующие промпты и C1 не пересоздавались.

В GitHub прежний журнал подтверждает сохранение C1. В доступной истории прежнего чата сообщается о C1–C6 и объявляется C7; оригиналы C2–C7 в текущую среду не получены и визуально не проверены. Пустая выдача Library и недоступная share-ссылка не доказывают отсутствие файлов. Поэтому C1–C7 исключены из повторной генерации до восстановления оригиналов; прежнее указание «начать с №2» ниже не исполнять без этой проверки.

Попытка продолжить отсутствующие №8–17 и уточнить отдельный C8 не дала пригодных PNG: получены три обзорных коллажа. Все три отклонены по заданию, не разрезаются на фиктивные референсы и не публикуются в сценах. Новых пригодных изображений 0; десять картинок и весь комплект не объявляются готовыми. Причина обработки генератором достоверно не установлена; однотипные попытки прекращены.

Следующий шаг: восстановить оригиналы C2–C6 и выяснить состояние C7 без перерисовки; проверить текущий реестр. Продолжать с действительно отсутствующего отдельного изображения, проверив соответствие одному точному промпту до следующей партии. Публиковать только реальные проверенные файлы; обе сцены DRAFT/not_approved, мастер и очередь Topview не менялись.

Доказательства: `projects/misc/reports/reference-generation-attempts-2026-11-02.json`. Исторический generation-progress.json сохранён; его счётчики относятся к прежнему циклу. Полный успешный приём и готовность генератора не заявляются.

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

- `projects/misc/references/GPT-TASK.md`
- `projects/misc/reports/reference-generation-attempts-2026-11-02.json`
- `projects/misc/references/generation-progress.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 0

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
