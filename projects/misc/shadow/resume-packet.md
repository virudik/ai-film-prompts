# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project misc`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-11-02T11:51:27+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# Разное — смета платных генераций и оценка заказов · 2026-11-02T11:03:44.342Z

work_id: MISC-S1-S2-REFERENCES
Проект: misc («Разное»). Основа: пользовательский Instagram Reel Db5KV8ZNQjP (загруженный MP4, 125,18 с, 1440×2560, 9:16), две самостоятельные сцены по 120 секунд (всего 240 с), 24 исходных промпта. Референсы 59/59 сохранены и доступны; все not_approved. Видеозапусков нет.
Проверено Topview (quote, не submit) 02.11.2026, image_to_video и text_to_video, 720p 9:16: Wan 3.0 12 кредитов/30 с; Seedance 2.0 15 кредитов/15 с; Seedance 2.5 36 кредитов/30 с. Один фильм: 48/120/144 кредитов; два фильма: 96/240/288. Условная цена $0,10/кредит по Ultra Annual и курс ЦБ 80,5573 ₽/USD: за обе истории приблизительно 773/1933/2320 ₽ до переделок; дополнительно ×2–3 на попытки. Не смешивать стоимость кредитов со стоимостью готового заказа.
Коммерческий ориентир Москвы: упрощённый 45–60 с — 20–35 тыс. ₽ (цена предложения 29 тыс.); один ≈120 с — 40–70 тыс. ₽ (49 тыс.); оба ≈120 с — 75–120 тыс. ₽ (89 тыс.). Полная смета с первоисточниками: `projects/misc/reports/commission-pricing-2026-11-02.md`, краткая таблица — в `projects/misc/video-prompts.md` раздел «Смета видеогенераций и цена заказа».
Безопасные границы: никаких платных генераций, новых сцен, одобрений или перезапусков; все изображения not_approved, видео DRAFT. Исходный чужой ролик нельзя повторно публиковать как свой.
Ближайшее открытое действие: владелец/клиент выбирает одну или обе истории и сокращённый 45–60 с или полный ≈120 с формат; далее художественный QC референсов и согласование брифа. После согласования — только подготовка финальных сценариев и производственного плана, не Create без отдельной команды.

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
Задач с сохранённым task ID: 0

## Пробелы

- recovery evidence changed: projects/misc/reports/commission-pricing-2026-11-02.md
