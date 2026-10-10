# AI Film — takeover brief (pilot-1.0) — ПИЛОТ 09.10–16.10, НЕ КАНОН

> Приёмка смены по-прежнему — полное чтение по NEW-CHAT-HANDOFF.md. Этот файл только измеряет, хватило бы brief.

Сгенерирован 2026-10-10T13:52:12+00:00. Валиден при генерации: **True**
Brief — навигатор. При любом триггере ниже — полный fresh-read канона.

## Authority
Drive canon/master → GitHub mirrors/status/Pages → Topview telemetry → Notion story/pointer → Library cache

## Источники (sha256)
- NEW-CHAT-HANDOFF.md · Drive `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD` · 241104 B · `808ac50e2a8247d2`
- SYNC-RUNBOOK.md · Drive `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4` · 113609 B · `2f51fc5662953395`
- AI-PROJECT-GUIDE.md · Drive `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u` · 102619 B · `a7b69c2e8a7b9c21`
- PROMPT-STYLE-GUIDE.md · Drive `14VzE8DwjKIquGJWENci6rYWj_1xEn34d` · 70332 B · `28542cedf06c07c3`
- USER-GUIDE.md · Drive `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO` · 96986 B · `e95b0a79d958ac4c`
- README-AI-SYNC.md · Drive `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX` · 74734 B · `f647c4e1e4613a35`
- BACKUP-AI-RUNBOOK.md · Drive `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1` · 83484 B · `91a0ed90d9a48627`
- video-prompts.md · Drive `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj` · 592123 B · `ec8d8d23965432c7`

## Обязательные инварианты
- **INV-AUTH** — Drive = editable master + 7 canonical docs; GitHub = mirror/status/site; Topview = telemetry; Notion = story/pointer; Library = recovery cache. → `AI-PROJECT-GUIDE.md` ✓
- **INV-ONE-MASTER** — One SAME-ID master; no v2/final/copy. → `AI-PROJECT-GUIDE.md` ✓
- **INV-FRESH-WRITE** — Before any master write: second fresh read of the exact Drive master; minimal same-ID edit → SYNC-TRIGGER → validation → mirror/status → Pages → verification. → `SYNC-RUNBOOK.md` ✓
- **INV-SERIAL-DOCS** — Canonical instruction writes are serial: fresh read/version → same-ID write → read-back → exact mirror → verify; never replay a stale write. → `SYNC-RUNBOOK.md` ✓
- **INV-SCENE-ID** — Scene IDs stable; retired IDs never reused; rerender keeps the same Scene ID. → `AI-PROJECT-GUIDE.md` ✓
- **INV-SUCCESS-NOT-APPROVAL** — Topview technical success ≠ editorial approval; never auto approve/rerun/delete/close. → `SYNC-RUNBOOK.md` ✓
- **INV-SLOTS** — Slot capacity 6; one active task = one slot; Scene stays slow until its last active task is terminal. → `SYNC-RUNBOOK.md` ✓
- **INV-ONE-MONITOR** — Exactly one automation «AI Film — единый монитор» (ID 6aac794245e481919ee7155c461cc77e, HH:00 MSK); archived 6aac3e4d…/6ac358bf… stay off; no duplicates; never disable it. If found disabled without an explicit owner decision to stop it: re-enable THAT task (is_enabled:true), record the incident, then verify a real publication (fresh topview-status/checkpoint + Pages). A disabled task cannot re-enable itself. → `SYNC-RUNBOOK.md` ✓
- **INV-NO-FAKE-TIME** — Never fake checked_at/queue/ETA; partial phases keep last confirmed timestamps. → `SYNC-RUNBOOK.md` ✓
- **INV-OWNER-BOUNDARY** — Owner decides only creative/editorial choices, ambiguous task↔Scene mapping, approval, rerender, deletion/closing; deterministic work is done by the agent; never ask for info already in sources. → `AI-PROJECT-GUIDE.md` ✓
- **INV-PROMPT-AUTONOMY** — Every copyable prompt is self-contained: identity lock, reference roles/priority, camera/space, timeline, native audio, negatives, FRAME FILL. → `PROMPT-STYLE-GUIDE.md` ✓
- **INV-MATERIAL-CHANGE** — Material workflow/site/authority/recovery change → relevant canonical docs + SAME handoff → mirrors → 7/7 certificate → Notion pointer → Library (best-effort). → `SYNC-RUNBOOK.md` ✓
- **INV-NO-CREDITS** — No paid generation or credit spending without the canonical workflow and owner permission; launches only on owner command. → `SYNC-RUNBOOK.md` ✓
- **INV-LIBRARY-NONBLOCKING** — Library is best-effort, never a completion gate. → `SYNC-RUNBOOK.md` ✓
- **INV-DONE** — Never say «готово» before the relevant read-back/verification passed. → `SYNC-RUNBOOK.md` ✓

## Runtime
- health ok; сцен 21 ([10, 11, 13, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]); промтов 54; последний ID 34; зарезервированы [1, 2, 3, 4, 5, 6, 7, 9, 12, 14, 15, 18]
- Слоты, slow, ETA, монитор — только из живых project-status.json, topview-status.json, instruction-sync-status.json, automation-monitor-status.json. Slots, slow, ETA and monitor state: read the live JSON. checked_at older than 2 h, missing or in the future = unverified.

## Индекс сцен
| ID | Название | Промт-движок | Состояние | Промтов | Refs | Зависит | sha |
|---|---|---|---|---|---|---|---|
| 10 | Кантина: допрос про товар, часть 1 | Wan 3 | NEEDS_FIX/IDLE | 1 | @Image1 @Image2 @Image3 | [] | 4bcf7357b408 |
| 11 | Кантина: допрос про товар, часть 2 | Wan 3 | NEEDS_FIX/IDLE | 1 | @Image1 @Image2 @Image3 | [10] | cc7a847ac011 |
| 13 | Совет джедаев: говорящий кот Лучик | Wan 3 | NEEDS_RERENDER/IDLE | 1 |  | [] | cf5b524e491f |
| 16 | Татуин: гигантский пустынный червь и бой на руинах | Seedance 2.5 | READY/SLOW_PENDING | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [] | 17f27d6e4cb0 |
| 17 | Пещера: передышка после монстра и разговор о карте | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 | [] | 611dc54063c4 |
| 19 | Рыбалка и Маша-Лагуна | Wan 3.0 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 | [] | a0b923994ec4 |
| 20 | Маша-Лагуна: рок-припев у озера | Seedance 2.5 | READY/SLOW_PENDING | 13 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 @Image7 | [] | 6320c046e5f5 |
| 21 | Мостик → космическая битва: бесшовный пролёт через окно | Seedance 2.5 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 | [] | 53eb9b26374f |
| 22 | Разрушенная станция → внутренний коридор: бесшовный пролёт ч | Seedance 2.5 | READY/IDLE | 1 | @Image1 @Image2 | [] | ac8ea0da407a |
| 23 | Люди → коты-джедаи: бесшовное раскрытие второго плана | Seedance 2.5 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 | [] | 7c7acf98efda |
| 24 | Коты в кабине: запуск корабля и взлёт | Seedance 2.5 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 | [23] | 86d19bea3cb2 |
| 25 | Коты в кабине: космическое сражение | Seedance 2.5 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 | [24] | 0951b58b93f8 |
| 26 | Коты-магистры на планете ситхов: ультиматум Серёге | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 | [25] | e1a8783cfe9f |
| 27 | Серёга против котов-магистров: бой на световых мечах | Seedance 2.5 | READY/IDLE | 3 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [26] | 74f9f994f645 |
| 28 | Финальные титры: имперский строевой танец | Seedance 2.0 | READY/IDLE | 20 | @Image1 @Image2 @Image3 @Image4 | [] | c0a156267d76 |
| 29 | Кантина: Илюха о плёнке на «Тысячелетнем соколе», часть 3 | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 @Image3 | [11] | a1b98e0c7420 |
| 30 | Коты против Серёги: разрушение колоннады | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [27] | 15792ffc960a |
| 31 | Коты против Серёги: лестница и телекинетические обломки | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [30] | e63eaa1e0ebc |
| 32 | Коты против Серёги: обрушение древней арки | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 @Image3 @Image4 @Image5 @Image6 | [31] | aaa2050e2dfd |
| 33 | Серёга исследует руины на планете ситхов | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 | [] | c434640420c2 |
| 34 | Серёга входит в полуразрушенный храм ситхов | Wan 3 | READY/IDLE | 1 | @Image1 @Image2 | [33] | 2f5bc485bf9d |

## Полный fresh-read обязателен, если
- any source sha256 in the brief ≠ live mirror / instruction certificate
- instruction-sync health ≠ ok or certificate older than its freshness limit
- project-status health ≠ ok or canonical_master_sha256 ≠ brief master sha
- task touches authority, sync, recovery, schedule, slot semantics or ≥2 scenes' shared rules
- agent cannot answer a mandatory takeover question from the brief + read set
- brief generator version or schema unknown

## Текущий checkpoint (дословно из NEW-CHAT-HANDOFF.md, до пометки «Предыдущая история»)

См. `current-checkpoint.md` (79499 симв., sha `3bea4725308c`). Дополнительно действующие разделы: ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ; ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ; ## ТЕКУЩЕЕ ДОПОЛНЕНИЕ
