# AI Film — takeover brief (d7-1.0) — короткий приём смены (D7, решение владельца 14.10.2026)

> **Порядок короткого приёма:** (1) `git pull` в `main`; (2) этот файл: «Валиден при генерации» = True и все 15 правил ✓ — иначе полное чтение 7 инструкций; (3) `shadow/current-checkpoint.md` целиком (верхние блоки NEW-CHAT-HANDOFF.md дословно); (4) живые статусы и открытые `owner_decisions`; (5) под задачу — разделы из «Что читать под задачу». Полное чтение обязательно при любом триггере в конце файла. Бриф — навигатор, не authority: свежий `main` всегда важнее.

Сгенерирован 2026-10-27T19:10:40+00:00. Валиден при генерации: **True**
Brief — навигатор. При любом триггере ниже — полный fresh-read канона.

## Authority
GitHub main (master + 7 instructions, status, site/Pages) → Topview telemetry → Notion story/pointer; backups (Drive, Notion pointer, Library, Project files) never override main

## Источники (sha256)
- NEW-CHAT-HANDOFF.md · копия на Drive `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD` · 34911 B · `d49bdd4283a196da`
- SYNC-RUNBOOK.md · копия на Drive `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4` · 125587 B · `fd2c8389816df3e0`
- AI-PROJECT-GUIDE.md · копия на Drive `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u` · 34298 B · `e4b282b861e67590`
- PROMPT-STYLE-GUIDE.md · копия на Drive `14VzE8DwjKIquGJWENci6rYWj_1xEn34d` · 72372 B · `a5813bc631df9432`
- USER-GUIDE.md · копия на Drive `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO` · 80102 B · `1429253208039887`
- README-AI-SYNC.md · копия на Drive `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX` · 16692 B · `353e9e8fee391b9d`
- BACKUP-AI-RUNBOOK.md · копия на Drive `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1` · 18925 B · `a6bf924b43892379`
- video-prompts.md · копия на Drive `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj` · 1004026 B · `7edc8947d751763d`

## Обязательные инварианты
- **INV-AUTH** — Since 11.10.2026: GitHub main = canon (master + 7 docs, status, site); Drive / Notion / Library / Project files = read-only backups; Topview = telemetry; Notion = story. → `NEW-CHAT-HANDOFF.md` ✓
- **INV-ONE-MASTER** — One master: video-prompts.md in GitHub main; no v2/final/copy. → `AI-PROJECT-GUIDE.md` ✓
- **INV-FRESH-WRITE** — Before any master write: fresh git pull of main; minimal commit → SYNC-TRIGGER → validator health=ok → Pages → verification; rejected push = another writer, redo from scratch. → `NEW-CHAT-HANDOFF.md` ✓
- **INV-SERIAL-DOCS** — Instruction edits: fresh pull → minimal commit → scripts/cert_github.py → push → verify; never replay a stale write. → `NEW-CHAT-HANDOFF.md` ✓
- **INV-SCENE-ID** — Scene IDs stable; retired IDs never reused; rerender keeps the same Scene ID. → `AI-PROJECT-GUIDE.md` ✓
- **INV-SUCCESS-NOT-APPROVAL** — Topview technical success ≠ editorial approval; never auto approve/rerun/delete/close. → `SYNC-RUNBOOK.md` ✓
- **INV-SLOTS** — Slot capacity 6; one active task = one slot; a terminal task frees its slot at once; canonical slow is cleared only by an explicit owner button (11.10.2026), never by a technical terminal. → `SYNC-RUNBOOK.md` ✓
- **INV-ONE-MONITOR** — One writer, decided by monitor-role.json + scripts/monitor_role.py: since 13.10.2026 the GitHub robot (topview-robot.yml → robot_telemetry.py, every 10 min via Supabase pg_cron) is primary, ChatGPT is standby and takes over only after 180 min without a verified healthy robot cycle; the Claude monitor is off; kill switch ROBOT_TELEMETRY=shadow. Old ChatGPT HH:00 monitor and archived Recovery/slot-watcher stay off. → `NEW-CHAT-HANDOFF.md` ✓
- **INV-NO-FAKE-TIME** — Never fake checked_at/queue/ETA; partial phases keep last confirmed timestamps. → `SYNC-RUNBOOK.md` ✓
- **INV-OWNER-BOUNDARY** — Owner decides only creative/editorial choices, ambiguous task↔Scene mapping, approval, rerender, deletion/closing; deterministic work is done by the agent; never ask for info already in sources. → `AI-PROJECT-GUIDE.md` ✓
- **INV-PROMPT-AUTONOMY** — Every copyable prompt is self-contained: identity lock, reference roles/priority, camera/space, timeline, native audio, negatives, FRAME FILL. → `PROMPT-STYLE-GUIDE.md` ✓
- **INV-MATERIAL-CHANGE** — Material workflow/site/authority/recovery change → relevant canonical docs + SAME handoff → cert_github.py certificate → push to main → Notion pointer → backup copies (best-effort). → `SYNC-RUNBOOK.md` ✓
- **INV-NO-CREDITS** — Agents may launch only owner-authorized queue items via the website in Unlimited mode at zero credits. Paid Topview launches are performed only by the owner. → `SYNC-RUNBOOK.md` ✓
- **INV-LIBRARY-NONBLOCKING** — Library is best-effort, never a completion gate. → `SYNC-RUNBOOK.md` ✓
- **INV-DONE** — Never say «готово» before the relevant read-back/verification passed. → `SYNC-RUNBOOK.md` ✓

## Runtime
- health ok; сцен 24 ([13, 16, 28, 33, 36, 41, 42, 48, 49, 50, 51, 52, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]); промтов 119; последний ID 67; зарезервированы [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40, 43, 44, 45, 46, 47, 53, 54, 55]
- Слоты, slow, ETA, монитор — только из живых project-status.json, topview-status.json, instruction-sync-status.json, automation-monitor-status.json. Slots, slow, ETA and monitor state: read the live JSON. checked_at older than 2 h, missing or in the future = unverified.

## Индекс сцен
| ID | Название | Промт-движок | Состояние | Промтов | Refs | Зависит | sha |
|---|---|---|---|---|---|---|---|
| 13 | Совет джедаев: говорящий кот Лучик | Wan 3 | NEEDS_RERENDER/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 53146e9d1886 |
| 16 | Татуин: гигантский пустынный червь и бой на руинах | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 1cb49f8adfc7 |
| 28 | Финальные титры: имперский строевой танец | Seedance 2.0 | NEEDS_RERENDER/SLOW_PENDING | 23 | @Image1 @Image2 @Image3 @Image4 @Image5 | [] | d913dff42477 |
| 33 | Серёга исследует руины на планете ситхов | Wan 3 | READY/IDLE | 3 | @Image1 @Image2 | [] | 9ed4ad5f905c |
| 36 | После пещеры: Серёга уходит с фрагментом карты | Wan 3 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | ee119b556282 |
| 41 | Серёга увозит древний ПК с планеты ситхов | Wan 3 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 809d46f72e41 |
| 42 | Татуин: бой на фоне червя — червь им не интересен | Seedance 2.0 | DRAFT/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [16] | e13906f96ded |
| 48 | Татуин: после боя Канцлер забирает фрагмент карты | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [56] | 8e8632aff462 |
| 49 | Финальные титры: все играют космический рок на инопланетных  | Seedance 2.0 | READY/IDLE | 9 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 @Image8 @Image9 | [28] | 17eb4aa1f7b0 |
| 50 | Финальные титры: вуки-фанаты слэмятся и трясут гривами | Seedance 2.0 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image8 | [28, 49] | 6ac559c15d25 |
| 51 | Финальные титры: каждый разбивает свой инструмент | Seedance 2.0 | READY/IDLE | 12 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [28, 49, 50] | f3bfb2c4c6d1 |
| 52 | Серёга пересаживается на свой корабль и прилетает на Татуин | Seedance 2.0 | DRAFT/SLOW_PENDING | 14 | @Image1 @Image2 @Image3 @Image4 @Image5 | [] | 7ec0a934d336 |
| 56 | Татуин: бой в движении — червь требует внимания | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 | [42] | be481db171a4 |
| 57 | РосКОТмос: аварийная посадка котов на планете ситхов | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | c12ca1c3d38d |
| 58 | РосКОТмос: коты выбегают из горящего корабля | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 @Image8 | [57] | a2719cef0c5c |
| 59 | Кашиик: динамичное прибытие и предвкушение грибной прогулки | Seedance 2.0 | READY/IDLE | 4 | @Image1 @Image2 @Image3 @Image4 @Image5 | [] | 23df59b3344e |
| 60 | Кашиик: Серёга уходит после боя и взлетает | Seedance 2.0 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | a68354642ec8 |
| 61 | Кашиик: ковбойское сближение перед дуэлью | Seedance 2.0 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 | [] | 3c9040f5ef19 |
| 62 | Татуин: после погони — обратно к противостоянию | Seedance 2.0 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 7b405dfdc4b9 |
| 63 | Храм ситхов: великие люди все на одно лицо | Wan 3 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 | [] | 44a6503cbd40 |
| 64 | Звёздный разрушитель: Серёга пританцовывает по коридору | Wan 3 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 | [] | a7573f3dcf7b |
| 65 | Татуин: Серёга молча выпивает в баре с Бобой Феттом и компан | Wan 3 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 | [] | b688c16a3b5b |
| 66 | Татуин: две девочки и инопланетная собака | Wan 3 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 | [52] | b4072ceb7a7d |
| 67 | Татуин: девушка яростно ругается с продавцом фруктов | Wan 3 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 | [66] | 5a4112e7c5dc |

## Что читать под задачу (сверх брифа)
- **takeover** — документы: —; master: index_only (D7 (owner 14.10.2026): short takeover = this read set; open full sections per task; any fallback trigger → full 7+master+status read.)
- **prompt_edit** — документы: PROMPT-STYLE-GUIDE.md целиком; master: target_scene_full + neighbours_full; ещё: character-references.json (target identities)
- **new_scene** — документы: PROMPT-STYLE-GUIDE.md целиком; SYNC-RUNBOOK.md — разделы «4. Routine: добавить новую scene», «18. Topview task intake»; master: last_two_scenes_full + header; ещё: character-references.json
- **story_edit** — документы: —; master: relevant_scenes_full; ещё: film-analysis.md, film-backlog.md, montage v2, Notion «Кино»
- **topview_check** — документы: SYNC-RUNBOOK.md — разделы «Порядок фаз цикла монитора», «Точное ТЗ — Topview slow slots», «Publish gate»; master: none_unless_slow_change; ещё: topview-status.json, topview-task-map.json, topview-checkpoint.json
- **instruction_change** — документы: все 7 инструкций целиком; master: none (material change: full current cycle)
- **recovery** — документы: все 7 инструкций целиком; master: full (always full)

## Полное чтение 7 инструкций обязательно, если
- any source sha256 in the brief ≠ live mirror / instruction certificate
- instruction-sync health ≠ ok or certificate older than its freshness limit
- project-status health ≠ ok or canonical_master_sha256 ≠ brief master sha
- task touches authority, sync, recovery, schedule, slot semantics or ≥2 scenes' shared rules
- agent cannot answer a mandatory takeover question from the brief + read set
- brief generator version or schema unknown
- brief «valid» ≠ True or any invariant shows ✕ ANCHOR MISSING
- the task edits any of the 7 instructions or is a material workflow / site / authority / recovery change
- recovery after an incident, or the owner asks for a full takeover

## Текущий checkpoint (дословно из NEW-CHAT-HANDOFF.md, до пометки «Предыдущая история»)

См. `current-checkpoint.md` (22865 симв., sha `686232b3f9ed`). Дополнительно действующие разделы: ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ; ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ
