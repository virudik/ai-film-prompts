# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-10-28T16:25:34+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# Татуинская связка — проверка готового и очередь прогулок Стича · 28.10.2026

work_id: SEREGIUS-PLAN-20261023

Задача claude-202610272340-s68-69-refs уже done, проверены все 5 существующих PNG и их SHA; повторного рисования нет. Композиция 68 возвращена только в галерею (из 3 промптов и очереди удалена); композиция 69 уже только вспомогательная. Тост IG-11 своей маслёнкой был в таймлайне, теперь синхронизированы описание и ограничение «не пьёт».

Владелец отдельно разрешил Topview Nano Banana: три новых разных кадра прогулки Алины и Даши со Стичем, S66-STITCH-NB-IMAGE-1 → -2 → -3, приоритеты -3/-2/-1 перед существующими видео. Все 3 исходника каждого кадра готовы, новые PNG пока не созданы. Полный живой скан: 13 досок, 19 страниц, 938 задач, 6/6 занято; Create, claim и расходов не было. После каждого submit повторить скан; если свободен только один слот, остальные изображения ждут его освобождения, без перехода на платный режим. Старые видео и проектная пауза Роскосмоса сохранены.

Следующий шаг: свежий main/решения/замок/полный скан, затем бесплатный веб-запуск следующего из трёх image-items по его prompt_source_path и SHA; в этом же цикле продолжать при наличии свободных слотов. Существующий часовой обработчик и Relay включены и читают живую очередь, новый монитор не создавался. Готовые 5 картинок не повторять, закрытую задачу не переоткрывать.

Доказательства: `reports/s68-69-followup-2026-10-28.json`.

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
Задач с сохранённым task ID: 40

## Пробелы

- recovery evidence changed: ops/topview-launch-queue.json
