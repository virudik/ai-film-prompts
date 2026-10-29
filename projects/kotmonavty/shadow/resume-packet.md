# Продолжай — пакет восстановления: Котмонавты

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project kotmonavty`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-29T22:42:09+00:00
Задача: KM-WAIT-REVIEW-2-22 — Котмонавты — два готовых ролика ждут оценки

Последний подтверждённый этап: Оба разрешённых платных ролика Seedance 2.5 завершены success: сцены 2 и 22, 30 с, 1280×720, по 36 кредитов; параметры, полный промпт и ID сверены с квитанциями. Учёт согласован, художественная приёмка не выставлена.
Следующий шаг: Показать владельцу уже готовые трейлер (2) и событийную заставку (22); получить оценку. Новых запусков или повторов без отдельного решения не делать.

## Контрольная точка

# Котмонавты — результаты получены, ждут просмотра · 30.10.2026

work_id: KM-WAIT-REVIEW-2-22
Проверено: 2026-10-29T22:30:59Z
Разрешение владельца 29.10: два платных ролика Seedance 2.5 по 30 с на доске Котмонавты. Команда продолжения 30.10: «Продолжи этот чат».

- Трейлер, сцена 2: d92ed461dca14e83a429f3c5d8407a8e. Отправлен 29.10 12:07:16 МСК, готов 12:22:09 МСК (14 мин 53 с). Ресурс 2b8790452a3542c2ab1774ccc62b47f6.
- Событийная заставка, сцена 22: fde415b07e2049a696b94699219268fc. Отправлена 29.10 12:15:39 МСК, готова 12:39:55 МСК (24 мин 16 с). Ресурс 223e55610e0c4069ad64460350fb9bf9.
- Оба success, 30 с, 1280×720, 16:9; 36+36=72 кредита, текущий баланс 30,37. Девять входов каждого совпали с квитанциями; полные промпты совпали с каноном. Все 66 блоков промптов сохранены побайтно; референсы не редактировались.
- Квитанции: projects/kotmonavty/reports/KM02-SEED25-30-20261029.json и KM22-SEED25-30-20261029.json. Запуски опубликованы коммитами 98ccadc7e1e3b393416c9f8de0b9438de7f2dd58 и 337908247cf009e664f3383e137147f4942e8682.
- Живой owner_decisions: нет решений по проекту/этим task ID; проектный review-ledger пуст. Других открытых входящих Котмонавтов нет. Это продолжение того же чата, не новый приём смены; новая квитанция приёма не создавалась.
- Синхронизированы master, scene manifests, очередь, инструкции и HANDOFF. Платное разрешение исчерпано; оба task ID остаются защитой от дублей. Технический успех не означает приёмку.

Проверки перед публикацией: projects.py status — health=ok, 22 сцены / 66 промптов; build_resume_packet — ready; continue_preflight — ready_for_resume=true, execution_authorized=false.

Следующий шаг: Показать владельцу уже готовые трейлер (2) и событийную заставку (22); получить оценку. Новых запусков или повторов без отдельного решения не делать.
Остаётся: художественная оценка видео и звука; выбор дальнейшей работы владельцем. MP4 находятся на исходной доске Topview; в репозиторий не копировались. Роскосмос и остальные проекты не затронуты.

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
- `projects/kotmonavty/reports/KM02-SEED25-30-20261029.json`
- `projects/kotmonavty/reports/KM22-SEED25-30-20261029.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 2

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
