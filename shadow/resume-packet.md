# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-21T16:23:52+00:00
Задача: SEREGIUS-SHIFT-20261113-T611U — Смена 13.11 t611u: очередь 48.4 и 89, отзыв по версиям Grok

Последний подтверждённый этап: S89C submitted, task 5d1f4fc1b4e548a7828892c73b672990, Unlimited0; post-scan6/6
Следующий шаг: Wait for free slot then fresh queue/anti-duplicate preflight; never repeat S89C Create

## Контрольная точка

# 16.11.2026 — dot: S89C отправлена через cloud browser, 6/6

work_id: SEREGIUS-SHIFT-20261113-T611U

- S89C-WAN30 отправлена одним Create 15:58:20Z; task `5d1f4fc1b4e548a7828892c73b672990`, init, Wan 3.0 / 30s / 720p / 16:9 / 1, пять проверенных референсов, Unlimited=true, creditsCost=0.
- Полный скан 14 досок после отправки: 678 задач, 6/6 занято. Следующий безопасный шаг: ждать свободного слота, сверить свежую разрешённую очередь и антидубли. S89C не повторять, художественная приёмка не заявлена.
- Доказательство: `reports/topview-queue-2026-10-16/S89C-WAN30-20261116T155820Z.json`. Чужая lease соблюдена; TinyFish не запускался.

checked_at: 2026-11-16T15:59:03.424Z

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

- `ops/LAUNCHER-ENTRY.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 100
- S28-A5-20261023: reconcile_without_resubmitting
- S89D-WAN30-R2: reconcile_without_resubmitting
- S89F-WAN30: reconcile_without_resubmitting
- S89F-WAN30-R2: reconcile_without_resubmitting

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
