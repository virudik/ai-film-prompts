# AI Film — takeover brief (pilot-1.0) — ПИЛОТ 09.10–16.10, НЕ КАНОН

> Приёмка смены по-прежнему — полное чтение по NEW-CHAT-HANDOFF.md. Этот файл только измеряет, хватило бы brief.

Сгенерирован 2026-10-13T20:52:56+00:00. Валиден при генерации: **True**
Brief — навигатор. При любом триггере ниже — полный fresh-read канона.

## Authority
Drive canon/master → GitHub mirrors/status/Pages → Topview telemetry → Notion story/pointer → Library cache

## Источники (sha256)
- NEW-CHAT-HANDOFF.md · Drive `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD` · 323200 B · `3b15893b2e9f07b6`
- SYNC-RUNBOOK.md · Drive `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4` · 131923 B · `7a62d26ee37068f8`
- AI-PROJECT-GUIDE.md · Drive `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u` · 121567 B · `97e9043d652a7e0e`
- PROMPT-STYLE-GUIDE.md · Drive `14VzE8DwjKIquGJWENci6rYWj_1xEn34d` · 77435 B · `dd9361be260d87ce`
- USER-GUIDE.md · Drive `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO` · 129419 B · `546d7ae233aec9ed`
- README-AI-SYNC.md · Drive `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX` · 78428 B · `ede04db6473583c0`
- BACKUP-AI-RUNBOOK.md · Drive `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1` · 98035 B · `8124c33b1836c3a9`
- video-prompts.md · Drive `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj` · 348180 B · `253a20f50c46bc7b`

## Обязательные инварианты
- **INV-AUTH** — Since 11.10.2026: GitHub main = canon (master + 7 docs, status, site); Drive / Notion / Library / Project files = read-only backups; Topview = telemetry; Notion = story. → `NEW-CHAT-HANDOFF.md` ✓
- **INV-ONE-MASTER** — One master: video-prompts.md in GitHub main; no v2/final/copy. → `AI-PROJECT-GUIDE.md` ✓
- **INV-FRESH-WRITE** — Before any master write: fresh git pull of main; minimal commit → SYNC-TRIGGER → validator health=ok → Pages → verification; rejected push = another writer, redo from scratch. → `NEW-CHAT-HANDOFF.md` ✓
- **INV-SERIAL-DOCS** — Instruction edits: fresh pull → minimal commit → scripts/cert_github.py → push → verify; never replay a stale write. → `NEW-CHAT-HANDOFF.md` ✓
- **INV-SCENE-ID** — Scene IDs stable; retired IDs never reused; rerender keeps the same Scene ID. → `AI-PROJECT-GUIDE.md` ✓
- **INV-SUCCESS-NOT-APPROVAL** — Topview technical success ≠ editorial approval; never auto approve/rerun/delete/close. → `SYNC-RUNBOOK.md` ✓
- **INV-SLOTS** — Slot capacity 6; one active task = one slot; Scene stays slow until its last active task is terminal. → `SYNC-RUNBOOK.md` ✓
- **INV-ONE-MONITOR** — One writer: the Claude monitor (HH:10) is the only writer; ChatGPT «резервный контроль» (6acae6ab…, HH:40) is read-only and may not take over until monitor-role.json migration_state allows it; old ChatGPT HH:00 monitor and archived Recovery/slot-watcher stay off. Claude monitor silent >3 h → issue monitor-alert, restore it; a disabled task cannot re-enable itself. → `NEW-CHAT-HANDOFF.md` ✓
- **INV-NO-FAKE-TIME** — Never fake checked_at/queue/ETA; partial phases keep last confirmed timestamps. → `SYNC-RUNBOOK.md` ✓
- **INV-OWNER-BOUNDARY** — Owner decides only creative/editorial choices, ambiguous task↔Scene mapping, approval, rerender, deletion/closing; deterministic work is done by the agent; never ask for info already in sources. → `AI-PROJECT-GUIDE.md` ✓
- **INV-PROMPT-AUTONOMY** — Every copyable prompt is self-contained: identity lock, reference roles/priority, camera/space, timeline, native audio, negatives, FRAME FILL. → `PROMPT-STYLE-GUIDE.md` ✓
- **INV-MATERIAL-CHANGE** — Material workflow/site/authority/recovery change → relevant canonical docs + SAME handoff → mirrors → 7/7 certificate → Notion pointer → Library (best-effort). → `SYNC-RUNBOOK.md` ✓
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
| 24 | Коты в кабине: запуск корабля и взлёт | Seedance 2.5 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 | [] | 31483dfb97b1 |
| 25 | Коты в кабине: космическое сражение | Seedance 2.5 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 | [24] | 88cc39ae51c9 |
| 27 | Серёга против котов-магистров: бой на световых мечах | Seedance 2.5 | READY/SLOW_PENDING | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | b8f60f7db58e |
| 28 | Финальные титры: имперский строевой танец | Seedance 2.0 | READY/IDLE | 20 | @Image1 @Image2 @Image3 @Image4 | [] | dcd69af7849d |
| 30 | Коты против Серёги: разрушение колоннады | Wan 3 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [27] | 98807b4f7026 |
| 31 | Коты против Серёги: лестница и телекинетические обломки | Wan 3 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [30] | 9ff63ee430c6 |
| 32 | Коты против Серёги: обрушение древней арки | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [31] | aaa2050e2dfd |
| 33 | Серёга исследует руины на планете ситхов | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 | [] | c434640420c2 |
| 34 | Серёга входит в полуразрушенный храм ситхов | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 | [33] | 2359ffefb996 |
| 35 | Древний ПК в руинах храма: находка Серёги | Wan 3 | DRAFT/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 | [34] | c438bf9bc64f |
| 36 | После пещеры: Серёга с картой направляется к кораблю | Wan 3 | DRAFT/IDLE | 1 | @Image1 @Image2 @Image3 | [] | da50cffb5d16 |
| 37 | Полёт Серёги к лесной планете и стык с отдельной группой | Wan 3 | DRAFT/IDLE | 1 | @Image1 @Image2 @Image3 | [36] | f81fe6c5166e |
| 38 | Серёга рассматривает древний компьютер в заброшенном храме | Wan 3 | DRAFT/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 | [35] | 7fcc8220229a |

## Полный fresh-read обязателен, если
- any source sha256 in the brief ≠ live mirror / instruction certificate
- instruction-sync health ≠ ok or certificate older than its freshness limit
- project-status health ≠ ok or canonical_master_sha256 ≠ brief master sha
- task touches authority, sync, recovery, schedule, slot semantics or ≥2 scenes' shared rules
- agent cannot answer a mandatory takeover question from the brief + read set
- brief generator version or schema unknown

## Текущий checkpoint (дословно из NEW-CHAT-HANDOFF.md, до пометки «Предыдущая история»)

См. `current-checkpoint.md` (133468 симв., sha `88039af558d6`). Дополнительно действующие разделы: ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ; ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ; ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ
