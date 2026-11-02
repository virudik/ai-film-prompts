# Продолжай — пакет восстановления: Разное

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project misc`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-11-02T21:25:14+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# Разное — новая внешность Лены, Нины, Дарьи: передача в Work · 2026-11-02T16:09:03.597Z

work_id: MISC-S1-S2-REFERENCES
**Новое подтверждённое решение владельца (02.11.2026):** «Мама Лена имеется ввиду. Бабушку Нина и Дарья Андреевну тоже привести к российской белокожей внешности»; затем уточнил «значит и описание и картинуи людей меняем», подтвердил «да», после начал передачу: «так просто сохранись в контрольные точки. я это ворку поручу». **Исполнитель следующих правок — Work, это запись передачи, не отчёт об их выполнении.**

**Точные объекты правки (проект `projects/misc`, сцены 1–2):** заменить **и описания, и сами изображения** трёх персонажей, всего **5 отдельных референсов**:
- Сцена 1, **Мама Лена**, 34 года: `mama-lena.png` (C3), `mama-lena-expressions.png` (C4). Светлая кожа, русская/европейская внешность; сохранить тёмные кудри в высоком свободном пучке, тёмные глаза, голубую джинсовую рубашку над белой футболкой, тёмные джинсы, усталую доброжелательность. **Не путать с мамой Верой сцены 2 — её не менять.**
- Сцена 2, **Бабушка Нина**, 62 года: `nina.png` (S2-N1), `nina-expressions.png` (S2-N2). Светлокожая русская женщина, короткие серебристые кудри, крупные серебристые серьги, сливовая спортивная куртка с белыми полосами, серые брюки, свисток; сохранить характер бывшего тренера по плаванию.
- Сцена 2, **Дарья Андреевна**, 30 лет: `darya.png` (S2-D1). Светлокожая русская женщина с европейскими чертами, тёмные волосы в длинной косе на плече, доброжелательный спокойный взгляд; оставить зелёную льняную рубашку, кремовые брюки и образ специалиста.

**Чего Work должен добиться:** сохранить единую идентичность каждой женщины во всех ракурсах и на листах эмоций, отдельные PNG с требуемым 3:2 для персонажей, стиль 3D-мультфильма, без подписей/логотипов/посторонних персонажей. Заменить оригиналы только после проверки результата; синхронно исправить `projects/misc/character-references.json`, пять `references/*.prompt.txt`, все относящиеся к ним фразы master `video-prompts.md`, SHA256 в списках/manifest и публичные ссылки. Обновить проектный статус `health=ok` по `scripts/projects.py . status --project misc --write` и проверить Pages. Остальные **54 референса из 59 не перерисовывать**, две сцены остаются DRAFT, изображения не получают automatic approval, видео не запускать. Никакого Topview/Higgsfield/MCP-расхода без отдельного согласования стоимости.

**Фактически сделано в ЭТОМ чате (не сохранено в GitHub):** штатным ChatGPT ImageGen созданы два *предварительных* файла для Лены: C3 — `file_00000000f0448243a4552d114e489aa9` / `/mnt/data/a_high_quality_3d_cgi_character_model_sheet_in_a_c.png`; C4 — `file_00000000df6881f4bed2d817646cab79` / `/mnt/data/a_cinematic_ultra_detailed_photorealistic_cgi_st.png`. **Они не прошли художественную приёмку, не опубликованы в каноне;** Work должен проверить их пригодность, стиль и совпадение лица, не объявлять как готовые. Для Нины две попытки `file_0000000001588243ba490005540a4995` и `file_00000000d97c8210b7c18ef5957f4693` дали ошибочные общие коллажи трёх женщин с надписями; **отклонены**, не использовать как S2-N1/N2 или как три раздельные картинки. Для Дарьи отдельная правильная новая картинка не создана.

**Текущее состояние:** пять канонических PNG и старые описания всё ещё **не исправлены**; старые `mama-lena`, `nina`, `darya` в `character-references.json` и `references/*.prompt.txt` содержат tan/deep-brown skin. Переданные намерения нельзя считать завершённым изменением. В GitHub 59/59 технических оригиналов, все not_approved, видео 0. Следующий шаг — Work принимает эту точку, проверяет fresh main и свой проектный замок, затем исправляет **пять** отдельных изображений и зависимые тексты/манифесты/Pages. Никаких новых расходов.

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

- selected checkpoint hash mismatch
