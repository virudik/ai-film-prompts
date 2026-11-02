# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project misc`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-02T12:01:18+00:00
Задача: MISC-S1-S2-REFERENCES — 59 отдельных референсов сцен 1 и 2 из GPT-TASK.md

Последний подтверждённый этап: Публичный мастер и отчёт обновлены рыночной и производственной сметой 45/109/189 тыс. ₽, договорные условия уточнены; отдельный отчёт «Серёгиуса» основан на 459 реальных задачах доски. 59 PNG сохранены, видео не запускались.
Следующий шаг: Показать владельцу обновлённые PDF/сметы и 59 референсов (все not_approved), согласовать с клиентом один упрощённый ролик 45–60 с за ориентир 45 тыс. ₽, полный 120 с за ориентир 109 тыс. ₽ или оба за ориентир 189 тыс. ₽; уточнить голос, материалы, права и сроки. Без прямого разрешения владельца видео не генерировать.

## Контрольная точка

# Разное — проверка Grok, исправленная коммерческая смета и аудит Topview · 2026-11-02T11:57:00.027Z

work_id: MISC-S1-S2-REFERENCES
Проект «Разное» (misc), 02.11.2026: выполнен повторный пересчёт исходного файла «Памятка: сколько стоит ИИ-ролик ~2 минуты» (2 стр.) по реальным Topview quote, рыночным предложениям и истории фактического производства. Подготовлен обновлённый PDF на 9 страниц для заказчика, отдельно — PDF-аудит «Серёгиуса» на 4 страницах, переданы владельцу в этом чате.
Референсы: 59/59 (26 по сцене 1, 33 по сцене 2) находятся в GitHub и на сайте; все not_approved, две сцены DRAFT, видео в misc не запускались. Исходный Reel 125,18 с, 9:16; две наши сцены — две альтернативные самостоятельные истории по 120 с каждая, 24 промпта.
Исправлены цены для заказчика: упрощённый 45–60 с 45 000 ₽; один полноценный 120 с с существующей визуальной базой 109 000 ₽; две истории по 120 с 189 000 ₽; новая история 120 с с нуля 169 000 ₽; бизнес-реклама от 199 000 ₽. В цену закладываются труд, отбор и технические переделки, звук, накладные и резерв. Исправление брака внутри утверждённого ТЗ за счёт исполнителя, творческие изменения ТЗ отдельно после согласования; предварительная оплата 50/30/20.
Подробный аудит/смета «Разного»: projects/misc/reports/commission-pricing-2026-11-02.md. Публичная таблица и условия: projects/misc/video-prompts.md, раздел «Стоимость AI-мультфильма, переделки и условия заказа». История «Серёгиуса»: reports/seregius-topview-production-audit-2026-11-02.md; реальные 459 видеозадач My First Board, 430 success, 23 fail, 6 init, 443 кредита по 36 платным задачам. Все эти задачи не равны художественно принятым роликам готового фильма. Условная полная кредитная стоимость — не фактический платёж.
Запрещено делать видео submit без отдельного прямого решения владельца. Следующий шаг: художественное QC 59 изображений и согласование с клиентом объёма, прав, голоса/текста и итоговой сметы. Никакие рендеры или approval не производились.

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

- `projects/misc/reports/commission-pricing-2026-11-02.md`
- `reports/seregius-topview-production-audit-2026-11-02.md`
- `projects/misc/references/generation-progress.json`
- `projects/misc/video-prompts.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 0

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
