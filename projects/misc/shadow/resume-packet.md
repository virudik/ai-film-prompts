# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project misc`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-02T13:25:02+00:00
Задача: MISC-S1-S2-REFERENCES — 59 отдельных референсов сцен 1 и 2 из GPT-TASK.md

Последний подтверждённый этап: Смета прямой покупки кредитов в рублях обновлена и сохранена в master, проектном отчёте и отдельном отчёте Серёгиуса; 59/59 референсов сохранены, видео по misc не запущены.
Следующий шаг: Владелец: открыть оба новых PDF с покупными RUB-кредитами, провести художественный QC 59 референсов, согласовать с клиентом лайт 59 тыс./один 120 с 145 тыс./два 120 с 265 тыс. ₽, права, озвучку, итоговое ТЗ и реальные доступные пакеты пополнения Topview. Текущий проект остаётся DRAFT; до новой прямой команды владельца видео не генерировать и кредиты не покупать.

## Контрольная точка

# Разное — платный режим по отдельно купленным рублёвым кредитам · 2026-11-02T12:28:10.760Z

work_id: MISC-S1-S2-REFERENCES
Владелец 02.11.2026 поручил исключить стоимость подписки и пересчитать все видеогенерации как платные за отдельно купленные за рубли токены. Публичная основа: RU App Store TOPVIEW PTE. LTD., 25/100/250/500/1000 кредитов за 1190/4490/9990/19990/24990 ₽. Не подтверждена переносимость кредитов iOS в topview.ai и реальная доступность оплаты в аккаунте: закупка и видеосоздание не выполнялись.
Модельные базовые кредитные ставки 720p БЕЗ скидок Ultra: WAN 0,5 кр./с, Seedance 2.0 1 кр./с, Seedance 2.5 1,5 кр./с. Один 120-секундный фильм: 60/120/180 кр. в один проход. С резервом WAN 4–6, Seedance 2.0/2.5 2–4 прохода, закупка обычных целых пакетов: WAN 9990–15670 ₽, Seedance 2.0 9990–19980 ₽, Seedance 2.5 15670–29970 ₽. Для двух историй: WAN 19980–29970 ₽; Seedance 2.0 19980–39960 ₽; Seedance 2.5 29970–58930 ₽. Опциональный пакет 1000 за 24990 ₽ может сократить расходы, если реально доступен.
Предложение заказчику на полный цикл: лайт 45–60 с 59000 ₽, один 120 с с готовой базой 145000 ₽, два 120 с 265000 ₽, один 120 с с нуля от 195000 ₽, бизнес от 230000 ₽. При 145000 ₽ внутренний бюджет до налогов 112300 ₽, условный налог 6% 8700 ₽, остаток 24000 ₽. Исправления технических дефектов в утверждённом ТЗ без отдельного счёта; творческие изменения объёма только после нового письменного согласования и ценового лимита.
«Серёгиус» My First Board: read-only 459 задач, 430 success, 23 fail, 6 init, recorded 443 кр. по 36 платным записям. Если все успешные видео WAN/Seedance рендерить платно без скидки: 7740,5 кр., закупка обычных пакетов 7750 кр. за 309690 ₽; при подтверждённом пакете 1000 — 8000 кр. за 199920 ₽. Это условный платный эквивалент, не реально уплаченные рубли.
Проверенные исходники: projects/misc/reports/commission-pricing-2026-11-02.md, reports/seregius-topview-production-audit-2026-11-02.md, projects/misc/video-prompts.md; новые PDF raznoe-smeta-pokupnye-kredity-rub-2026-11-02.pdf (7 стр.) и seregius-topview-platnye-kredity-rub-2026-11-02.pdf (4 стр.) — файлы чата.
Состояние производства: 59/59 PNG, 24 видеопромпта, две сцены DRAFT/not_approved, очередь проекта misc пуста. Не запускать ни платные, ни другие видео по этому документу. Следующий шаг — художественный QC и отдельное согласование заказа по новому пакету/срокам.

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
- `projects/misc/HANDOFF.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 0

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
