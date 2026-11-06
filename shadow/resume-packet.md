# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-06T13:31:48+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Сверены обе share-ветки; работа HH:55 подтверждена совпавшими runtime/result/канонической квитанцией. Выполнена повторная HTTPS-проверка с честным остатком8поддоменов. Подтверждена доставка8файлов Саше. Keep, полный QC стыков и доработка RESOURCE/HONOR остаются незавершёнными.
Следующий шаг: При свободном слоте выполнить свежий полный preflight и взять готовый разрешённый item по priority; submitted не повторять. S52/S60/S61 ждут полного QC со звуком. Keep продолжать по приватному checkpoint. RESOURCE/HONOR доделывать под замком Разного. Проверить сертификаты/Pages восьми семейных поддоменов. Восемь файлов Саше доставлены; не дублировать.

## Контрольная точка

# 06.11.2026 — повторная сверка связанных чатов, HTTPS и доставки Саше

work_id: TOPVIEW-SLOT-PRIORITY-20261024

- Два переданных share прочитаны: 6aedd10a прямо продолжает 6aedc24c; новых отдельных поручений второй чат не добавляет. Общий ответ «всё готово» не подтверждён.
- HH:55 включено. Реальный цикл 15:55–16:02 МСК имеет совпадающие runtime/result/canonical receipt; 14 досок, 18 страниц, 630 видео, 6/6 занято, Create0. Это проверенный прошлый цикл, не новый скан; автоматика не менялась.
- HTTPS16:19–16:23МСК: root/www/промты/ии доступны; восемь семейных поддоменов возвращают HTTPS503 при HTTP200. Origin сертификат не прочитан из-за DNS, Pages UI требует входа; точная причина не доказана, настроек не меняли.
- Саше доставлены8файлов, включая8-страничное руководство PDF/DOCX/MD, шаблон/примеры и две инструкции; имена, размеры и папка проверены. Прежние15видео и доступ сохранены.
- Keep остаётся в работе, нового пересчёта нет. У S52/S60/S61 всё ещё нет подтверждённого непрерывного просмотра со звуком. RESOURCE/HONOR — черновики/референсы/QC в проектном продолжении, не completed.
- Доказательства с точными ссылками и границами проверок: reports/work-continue-linked-chat-2026-11-06.json → followup_audit. Исторические сканы и результаты сохранены.

Следующий шаг: При свободном слоте выполнить свежий полный preflight и взять готовый разрешённый item по priority; submitted не повторять. S52/S60/S61 ждут полного QC со звуком. Keep продолжать по приватному checkpoint. RESOURCE/HONOR доделывать под замком Разного. Проверить сертификаты/Pages восьми семейных поддоменов. Восемь файлов Саше доставлены; не дублировать.

checked_at: 2026-11-06T13:30:20+00:00

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
