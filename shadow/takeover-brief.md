# AI Film — takeover brief (d7-1.0) — короткий приём смены (D7, решение владельца 14.10.2026)

> **Порядок короткого приёма:** (1) `git pull` в `main`; (2) этот файл: «Валиден при генерации» = True и все 15 правил ✓ — иначе полное чтение 7 инструкций; (3) `shadow/current-checkpoint.md` целиком (верхние блоки NEW-CHAT-HANDOFF.md дословно); (4) живые статусы и открытые `owner_decisions`; (5) под задачу — разделы из «Что читать под задачу». Полное чтение обязательно при любом триггере в конце файла. Бриф — навигатор, не authority: свежий `main` всегда важнее.

Сгенерирован 2026-10-13T22:15:19+00:00. Валиден при генерации: **True**
Brief — навигатор. При любом триггере ниже — полный fresh-read канона.

## Authority
GitHub main (master + 7 instructions, status, site/Pages) → Topview telemetry → Notion story/pointer; backups (Drive, Notion pointer, Library, Project files) never override main

## Источники (sha256)
- NEW-CHAT-HANDOFF.md · копия на Drive `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD` · 37690 B · `ae112a4dd25b632a`
- SYNC-RUNBOOK.md · копия на Drive `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4` · 104963 B · `8f956fffbee444ad`
- AI-PROJECT-GUIDE.md · копия на Drive `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u` · 63781 B · `9a56ac7941c01427`
- PROMPT-STYLE-GUIDE.md · копия на Drive `14VzE8DwjKIquGJWENci6rYWj_1xEn34d` · 73563 B · `b6c655aa5c74cdd5`
- USER-GUIDE.md · копия на Drive `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO` · 65328 B · `e6e53de7d5963cc9`
- README-AI-SYNC.md · копия на Drive `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX` · 26664 B · `1760add0e4eb9acc`
- BACKUP-AI-RUNBOOK.md · копия на Drive `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1` · 36043 B · `b8f5f248497a7d1a`
- video-prompts.md · копия на Drive `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj` · 348631 B · `87328c2b26aaea2d`

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
- health ok; сцен 15 ([13, 16, 24, 25, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38]); промтов 36; последний ID 38; зарезервированы [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 23, 26, 29]
- Слоты, slow, ETA, монитор — только из живых project-status.json, topview-status.json, instruction-sync-status.json, automation-monitor-status.json. Slots, slow, ETA and monitor state: read the live JSON. checked_at older than 2 h, missing or in the future = unverified.

## Индекс сцен
| ID | Название | Промт-движок | Состояние | Промтов | Refs | Зависит | sha |
|---|---|---|---|---|---|---|---|
| 13 | Совет джедаев: говорящий кот Лучик | Wan 3 | NEEDS_RERENDER/IDLE | 1 |  | [] | cf5b524e491f |
| 16 | Татуин: гигантский пустынный червь и бой на руинах | Seedance 2.5 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 75964595562a |
| 24 | Коты в кабине: запуск корабля и взлёт | Seedance 2.5 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 | [] | 353817ca7a46 |
| 25 | Коты в кабине: космическое сражение | Seedance 2.5 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 | [24] | 9889b2806cd0 |
| 27 | Серёга против котов-магистров: бой на световых мечах | Seedance 2.5 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 0ae7b2df08c0 |
| 28 | Финальные титры: имперский строевой танец | Seedance 2.0 | READY/IDLE | 20 | @Image1 @Image2 @Image3 @Image4 | [] | dcd69af7849d |
| 30 | Коты против Серёги: разрушение колоннады | Wan 3 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [27] | 92eff17cd419 |
| 31 | Коты против Серёги: лестница и телекинетические обломки | Wan 3 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [30] | 20ef82ba5808 |
| 32 | Коты против Серёги: обрушение древней арки | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [31] | aaa2050e2dfd |
| 33 | Серёга исследует руины на планете ситхов | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 | [] | c434640420c2 |
| 34 | Серёга входит в полуразрушенный храм ситхов | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 | [33] | 2359ffefb996 |
| 35 | Древний ПК в руинах храма: находка Серёги | Wan 3 | DRAFT/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 | [34] | 2dbb4299d3e9 |
| 36 | После пещеры: Серёга с картой направляется к кораблю | Wan 3 | DRAFT/IDLE | 1 | @Image1 @Image2 @Image3 | [] | da50cffb5d16 |
| 37 | Полёт Серёги к лесной планете и стык с отдельной группой | Wan 3 | DRAFT/IDLE | 1 | @Image1 @Image2 @Image3 | [36] | f81fe6c5166e |
| 38 | Серёга рассматривает древний компьютер в заброшенном храме | Wan 3 | DRAFT/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 | [35] | 7fcc8220229a |

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

См. `current-checkpoint.md` (21258 симв., sha `b49d26b952ca`). Дополнительно действующие разделы: ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ; ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ
