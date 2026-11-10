# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-11-10T15:14:12+00:00
Задача: SEREGIUS-PARODIES-20261110 — Пародии 74–87: заметки t540u и кадры t548u–t550u

Последний подтверждённый этап: Кадры t548u–t550u положены по слотам и подключены в промпты, манифесты и parodies.html; в 81A Алексей отвечает «Я сам решу».
Следующий шаг: Пародии 74–87 опубликованы как DRAFT, все кадры t540u подключены (t550u). Видео 74–87 не запускать без отдельной команды владельца, очередь не менять. Открытых слотов без файлов нет.

## Контрольная точка

# 10.11.2026 — пародии 74–87 опубликованы, t540u внесён в промпты

work_id: SEREGIUS-PARODIES-20261110

- Свежий факт: сцены 74–87 есть в `video-prompts.md` как DRAFT. Кадры Грока лежат в `references/scenes/scene-74` … `scene-87` и в манифестах. Утверждения от 09.11, что дополнительные кадры не получены и что пародии — это только 7 PNG и 21 промпт, устарели и не должны запускать переделку.
- Не откатывать принятое: рыбка в 75 и основной кадр `S75-fishing-start.png`; оба кадра 79 и оба кадра 80; единственный кадр комнаты жениха в 82; гонг в 74 не входит; 77 — мем «Яблоневый сад» без майонеза.
- t540u сделано в текстах: 76A–C отдельные подсцены; 81A→82A→83A одна история, причина выбора Артёма посеяна фразой про пальто; 84A–C показывают панель, ракель и результат; 85A–C одна новость про гравитацию и тапочки; 86A–C открытие, ничтожная находка, восторг без зацикленного припева.
- Сделано t548u–t550u (10.11, ~14:55 МСК): все 17 файлов положены по слотам и подключены в промпты и манифесты. Сябитова — два портрета одного лица: `references/full/hostess-syabitova.jpg` (анфас, главный, @Image5) и `references/full/hostess-syabitova-34.jpg` (вполоборота, @Image6). В 81A на реплику Гузеевой «…Ей же с вами скучно будет!» Алексей отвечает «Я сам решу». Видео не запускалось. Строка ниже — историческая.
- Не сделано, потому что файлов нет и их нельзя выдумывать: портреты `references/full/hostess-guzeeva.jpg` (Лариса Гузеева), `hostess-syabitova.jpg` (Роза Сябитова), `star-gosling.jpg` (Райан Гослинг), `star-dicaprio.jpg` (Леонардо Ди Каприо), `star-pitt.jpg` (Брэд Питт) и отдельные кадры подсцен из `reports/parody-frames-to-draw-2026-11-10.md`. Картинки не генерировать из этого чата: их рисует владелец.
- Следующий шаг: не пересоздавать опубликованные кадры и не запускать видео. Очередь генераций не менять. Когда владелец положит файл точно по имени слота, подключить его как вход подсцены.

checked_at: 2026-11-10T11:20:00+00:00

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

- `reports/current-work-checkpoint.md`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 86

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
