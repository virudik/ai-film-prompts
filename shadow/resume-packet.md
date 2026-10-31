# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-10-31T17:14:08+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# Обычный ChatGPT — основной; Work — резерв · 31.10.2026

work_id: TOPVIEW-SLOT-PRIORITY-20261024

Прямая команда владельца: Work-лимит исчерпан; обычный исполнитель основной, Work резервный; оба независимы, но отправка только под общим замком/claim. После доказанного восстановления Work вернуть предпочтение ему. «Продолжай» передаёт ответственность сменщику.

Стадия: code_and_documents_validated; automation_and_GUI_acceptance_separate. Время фактической записи: 2026-10-31T16:58:22Z. Технический план: общий реестр ролей, уникальная lease, одноразовый submitting intent, foreground epoch, согласованные инструкции/хендоф, cert и тесты. Очередь/мастер/видео не меняются.

Подтверждено до смены ролей: реальный обычный runtime 52f01b43-0358-8330-9c19-fb332e6dcb03 проверил 14 досок/18 страниц/624 видео, 6/6 занято; GUI-проба вернула originating_browser_context_required. Это не подтверждение Create или отдельной квоты. S72 от 11:08:48Z сохраняется как исторический подтверждённый запуск.

Следующий шаг: проверить реальную настройку трёх существующих задач и новый обычный runtime после сообщения владельца о лимите; при 6/6 только read-only GUI-проба, при свободном слоте полный preflight и первый готовый разрешённый пункт. Не повторять S72/unknown. Не объявлять страховку полностью принятой без browser/task evidence.

Источники: ops/slot-backup.json; ops/LAUNCHER-COORDINATION.md; reports/launcher-coordination-2026-10-31.json.
<!-- /launcher-policy -->

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
Задач с сохранённым task ID: 48

## Пробелы

- selected checkpoint hash mismatch
