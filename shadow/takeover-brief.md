# AI Film — takeover brief (d7-1.0) — короткий приём смены (D7, решение владельца 14.10.2026)

> **Порядок короткого приёма:** (1) `git pull` в `main`; (2) этот файл: «Валиден при генерации» = True и все 15 правил ✓ — иначе полное чтение 7 инструкций; (3) `shadow/current-checkpoint.md` целиком (верхние блоки NEW-CHAT-HANDOFF.md дословно); (4) живые статусы и открытые `owner_decisions`; (5) под задачу — разделы из «Что читать под задачу». Полное чтение обязательно при любом триггере в конце файла. Бриф — навигатор, не authority: свежий `main` всегда важнее.

Сгенерирован 2026-10-22T22:14:07+00:00. Валиден при генерации: **True**
Brief — навигатор. При любом триггере ниже — полный fresh-read канона.

## Authority
GitHub main (master + 7 instructions, status, site/Pages) → Topview telemetry → Notion story/pointer; backups (Drive, Notion pointer, Library, Project files) never override main

## Источники (sha256)
- NEW-CHAT-HANDOFF.md · копия на Drive `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD` · 34663 B · `4e154519ae852fe0`
- SYNC-RUNBOOK.md · копия на Drive `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4` · 120834 B · `b04f0e15a5cea6d0`
- AI-PROJECT-GUIDE.md · копия на Drive `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u` · 32722 B · `39ebed74e4a6bcd1`
- PROMPT-STYLE-GUIDE.md · копия на Drive `14VzE8DwjKIquGJWENci6rYWj_1xEn34d` · 64497 B · `e1511aa020ae4f3e`
- USER-GUIDE.md · копия на Drive `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO` · 74055 B · `8294130ab6664f70`
- README-AI-SYNC.md · копия на Drive `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX` · 15350 B · `b5ac5af59fb86b69`
- BACKUP-AI-RUNBOOK.md · копия на Drive `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1` · 17707 B · `2167ce1ba9077c14`
- video-prompts.md · копия на Drive `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj` · 914628 B · `7ba6bd01abda44b4`

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
- **INV-NO-CREDITS** — No paid generation or credit spending without the canonical workflow and owner permission; launches only on owner command. → `SYNC-RUNBOOK.md` ✓
- **INV-LIBRARY-NONBLOCKING** — Library is best-effort, never a completion gate. → `SYNC-RUNBOOK.md` ✓
- **INV-DONE** — Never say «готово» before the relevant read-back/verification passed. → `SYNC-RUNBOOK.md` ✓

## Runtime
- health ok; сцен 21 ([13, 16, 28, 33, 36, 37, 39, 40, 41, 42, 44, 47, 48, 49, 50, 51, 52, 53, 56, 57, 58]); промтов 89; последний ID 58; зарезервированы [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 34, 35, 38, 43, 45, 46, 54, 55]
- Слоты, slow, ETA, монитор — только из живых project-status.json, topview-status.json, instruction-sync-status.json, automation-monitor-status.json. Slots, slow, ETA and monitor state: read the live JSON. checked_at older than 2 h, missing or in the future = unverified.

## Индекс сцен
| ID | Название | Промт-движок | Состояние | Промтов | Refs | Зависит | sha |
|---|---|---|---|---|---|---|---|
| 13 | Совет джедаев: говорящий кот Лучик | Wan 3 | NEEDS_RERENDER/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 53146e9d1886 |
| 16 | Татуин: гигантский пустынный червь и бой на руинах | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 85cacbf36444 |
| 28 | Финальные титры: имперский строевой танец | Seedance 2.0 | READY/IDLE | 23 | @Image1 @Image2 @Image3 @Image4 | [] | 32d9ec7ccfb1 |
| 33 | Серёга исследует руины на планете ситхов | Wan 3 | READY/IDLE | 3 | @Image1 @Image2 | [] | 9ed4ad5f905c |
| 36 | После пещеры: Серёга уходит с фрагментом карты | Wan 3 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 1bcbb827821d |
| 37 | Отлёт Серёги с Набу к лесной планете | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [36] | 991188fcb733 |
| 39 | Серёга прибывает на Набу: посадка у брошенной стоянки рыбако | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 9d730b647bb8 |
| 40 | Серёга прилетает на планету ситхов: посадка у руин | Seedance 2.0 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 4edcb12c25e4 |
| 41 | Серёга увозит древний ПК с планеты ситхов | Wan 3 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | d9a46173a72c |
| 42 | Татуин: бой на фоне червя — червь им не интересен | Seedance 2.0 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [16] | 8f29749a1858 |
| 44 | Ангар крейсера: ремонт крыла, и оно отваливается | Wan 3 | DRAFT/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 | [] | e564279271c2 |
| 47 | Красная точка: Серёга уходит от котов хитростью | Seedance 2.0 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 3be8f42e38a1 |
| 48 | Татуин: после боя Канцлер забирает фрагмент карты | Seedance 2.0 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [56] | 562af2732315 |
| 49 | Финальные титры: все играют космический рок на инопланетных  | Seedance 2.0 | READY/IDLE | 9 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 @Image8 @Image9 | [28] | 05ff816dde03 |
| 50 | Финальные титры: вуки-фанаты слэмятся и трясут гривами | Seedance 2.0 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image8 | [28, 49] | a88ff3c303f6 |
| 51 | Финальные титры: рок-финал с разбиванием инопланетных инстру | Seedance 2.0 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 @Image8 | [28, 49, 50] | dd53d5db138f |
| 52 | Серёга пересаживается на свой корабль и прилетает на Татуин | Seedance 2.0 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 | [44] | 49ca73f4fd9d |
| 53 | Взлёт Серёги с Татуина: курс на Набу | Seedance 2.0 | DRAFT/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 | [48, 39] | bcec38b443fb |
| 56 | Татуин: бой в движении — червь требует внимания | Seedance 2.0 | DRAFT/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 | [42] | 1acd2327c68d |
| 57 | РосКОТмос: аварийная посадка котов на планете ситхов | Seedance 2.0 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 1dc8ecac6141 |
| 58 | РосКОТмос: коты выбегают из горящего корабля | Seedance 2.0 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 @Image8 | [57] | d18fef031798 |

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

См. `current-checkpoint.md` (22704 симв., sha `33b6739b4d4b`). Дополнительно действующие разделы: ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ; ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ
