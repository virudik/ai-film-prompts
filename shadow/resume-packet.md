# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-07T00:24:17+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Проверен общий ChatGPT Images и снят прежний UI-блокер; завершённая работа перенесена с сохранением истории. Подтверждён linkfix существующего руководства Саше по трём Drive ID и SHA readback. Квитанции CONTINUE-001 уточнены без закрытия issue; основной фокус и текущие блокеры сохранены. Дополнительно подтверждены success восьми Pages deployments и корректные AAAA/CAA; происхождение HTTPS 503 на origin не установлено.
Следующий шаг: При свободном слоте выполнить свежий полный preflight и взять готовый разрешённый item по priority; submitted не повторять. S52/S60/S61 ждут полного QC со звуком. Keep продолжать по приватному checkpoint. RESOURCE/HONOR доделывать под замком Разного. Проверить сертификаты/Pages восьми семейных поддоменов. Восемь файлов Саше доставлены; не дублировать.

## Контрольная точка

# 06.11.2026 — общий Images проверен, ссылка руководства Саше исправлена

work_id: TOPVIEW-SLOT-PRIORITY-20261024

- Общий ChatGPT Images проверен через авторизованный sidebar: открылась /images, загружены Images, My images и 34 видимых элемента сохранённых изображений. Это не полный счёт аккаунта. Генераций, правок, удаления или приёмки нет; прежний UI-блокер снят. TOPVIEW-FRESHNESS перенесён из active_work в completed_work; история сохранена.
- В существующих MD/DOCX/PDF Саши исправлена ссылка на RESOURCE. Три Drive ID сохранены, raw readback SHA совпадает; новых файлов/дубликатов нет. Все восемь страниц свежего PDF проверены. Linkfix сохранён отдельным событием после первоначальной доставки восьми файлов.
- CONTINUE-001: реальные приёмы и первые действия подтверждены двумя квитанциями. Локальные UUID при неизвестном conversation ID не доказывают отдельный физический чат; issue №9 остаётся открыт, комментариев нет. Реализация не повторялась.
- Дополнение HTTPS 06.11 14:00 UTC: все восемь Pages deployments success, SHA совпадают с main; AAAA соответствует Pages, CAA допускает letsencrypt.org. Наблюдавшийся 503 получен через envoy среды; причина на origin и состояние сертификата не доказаны. Точные run URL/SHA и DNS сохранены отдельным событием followup_audit.https.deployment_dns_followup.
- Делегированный аудит не менял очередь, роли, автоматику, телеметрию, инструкции или проектные файлы. Основной фокус и уже известные незавершённые работы сохранены.
- Доказательства: reports/chatgpt-images-ui-check-2026-11-06.json; reports/work-continue-linked-chat-2026-11-06.json → followup_audit.

Следующий шаг: При свободном слоте выполнить свежий полный preflight и взять готовый разрешённый item по priority; submitted не повторять. S52/S60/S61 ждут полного QC со звуком. Keep продолжать по приватному checkpoint. RESOURCE/HONOR доделывать под замком Разного. Проверить сертификаты/Pages восьми семейных поддоменов. Восемь файлов Саше доставлены; не дублировать.

checked_at: 2026-11-06T14:05:13.373171+00:00

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
- `projects/raznoe/HANDOFF.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 54

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
