# Продолжай — пакет восстановления: Котмонавты

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project kotmonavty`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-10-30T00:15:29+00:00
Задача: KM-20261030-WAN4-9 — Wan3 30s: сцены4 и9

Последний подтверждённый этап: Сцены 4 и 9 отправлены по одному разу: Wan 3.0, 30 с, 720p, 16:9, звук; Topview подтвердил running, по 12 кредитов. Полные UI/provider-промпты совпали с каноном. Остаток 6,37; разрешение исчерпано.
Следующий шаг: Проверить статусы существующих task ID сцен 4/9; после success сохранить результат и провести просмотр видео/звука. Готовые 2/22 также ждут оценки владельца. Не нажимать Create повторно, не выставлять приёмку автоматически.

## Контрольная точка

# Котмонавты — два Wan 3.0 отправлены, контрольная точка ПОСЛЕ · 30.10.2026

work_id: KM-20261030-WAN4-9
Проверено: 2026-10-29T22:53:00Z
Сцены 4 и 9 отправлены по одному разу: Wan 3.0, 30 с, 720p, 16:9, звук; Topview подтвердил running, по 12 кредитов. Полные UI/provider-промпты совпали с каноном. Остаток 6,37; разрешение исчерпано.
- Сцена 4: 4dc7da2c6bff41b3a8161a6cc427aaa7, отправлена 30.10 01:44:32 МСК; квитанция projects/kotmonavty/reports/KM04-WAN30-20261030.json, коммит 53a46762b594e7a48d779f2366a486c952f7ab0b.
- Сцена 9: 16d53ab1a84e4091b8867b7ed5cc8f4c, отправлена 30.10 01:51:18 МСК; квитанция projects/kotmonavty/reports/KM09-WAN30-20261030.json, коммит cf2a9a641724eebc4785397c20dae21626d3c51f.
- Четыре источника каждой сцены проверены по SHA, визуально, по UI-порядку и натуральным размерам; все загрузки complete. Обратное скачивание blob для SHA не работало, проверка байтов после загрузки не заявляется. Канонические изображения и все 66 блоков промптов не менялись.
- По скриншоту Серёгиуса: набор входов соответствует старой ошибочной подготовке S59 P2 (лес 1280×240 отклонён, второй корабль попал вместо него). Задача 9b2e18c883e3401e9b13b2930b3b570c отменена, исправленная b0915b04173c414e9ac08652d34b7852 подтверждена init; S62 0de1f663432646d294f409a22e20a26e тоже init. У красной карточки на скрине нет ID, однозначная привязка не доказана; на свежей доске она не отображалась. Серёгиус не перезапускался и не правился.
- Учёт обновлён в master, manifests, queue, HANDOFF, INSTRUCTIONS и recovery. Ни одна техническая проверка не является художественной приёмкой.

Следующий шаг: Проверить статусы существующих task ID сцен 4/9; после success сохранить результат и провести просмотр видео/звука. Готовые 2/22 также ждут оценки владельца. Не нажимать Create повторно, не выставлять приёмку автоматически.
Границы: только два уже отправленных запуска; без новых изображений, изменения промптов, иных сцен, покупки кредитов и автоповтора.

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

- `projects/kotmonavty/HANDOFF.md`
- `projects/kotmonavty/INSTRUCTIONS.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 4

## Пробелы

- brief was invalid at generation
- master vs project-status sha256 mismatch
