# AI Film Prompts — NEW CHAT HANDOFF v3.5

**Назначение:** аварийная/операционная передача проекта новому чату или другому основному ИИ без опоры на память предыдущей сессии.

**Последнее обновление handoff:** 18.09.2026.

Этот файл должен оставаться коротким путеводителем по проекту, но достаточно полным, чтобы новый основной редактор мог безопасно восстановить контекст, найти канонические источники и продолжить работу без создания второго master.

---

## 0. Самое важное за 60 секунд

- **Единственный редактируемый канонический master:** Google Drive `AI Film Prompts Master/video-prompts.md`.
- **Drive master file ID:** `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
- **Не создавать** `v2`, `final`, `copy`, `final-final` и т. п.
- Перед любой записью в master сначала **заново прочитать свежий Drive `video-prompts.md`**.
- Текущее состояние master: **17 активных сцен · 20 полных текстов промтов · 3 work items (W5, W7, W8) · 6 slow-сцен (2, 6, 12, 14, 15, 18)**.
- Scene IDs стабильны и могут иметь пропуски. **После удаления готовой сцены остальные не перенумеровывать.**
- Сцена **8 «Кашиик — спор на мосту»** завершена и удалена из active master.
- Slow-сцены **2, 6, 12, 14, 15, 18 повторно не запускать** до результата/явной ошибки или отдельного разрешения пользователя.
- `project-status.json` сейчас: **schema v3 · health = ok · canonical master SHA-256 = `a739d6890382e54c443958c1e1d124a147aa29fed50a321328c22a5dd2060520`**; все обязательные integrity/scene-meta checks = true.
- `audit_fingerprint` — обязательная проверка свежести перед внешним аудитом: revision/hash, scene/prompt counts, scene IDs, W-items, slow list, health и instruction-sync health.
- `instruction_sync.health = unverified` — ожидаемое честное состояние: приватные Drive-инструкции вручную выровнены с зеркалами в checkpoint, но автоматической authenticated hash-проверки из GitHub Actions пока нет.
- На момент этого refresh проверенный GitHub Actions master-sync: **run #85 — success**; проверенный Pages deployment: **#121 — success**. Точные более новые номера всегда перепроверять live в Actions.
- Если другой файл, старый чат, Library, Notion или старый backlog противоречат свежему Drive master по активным сценам/slow-status — **свежий Drive master имеет приоритет**.

---

## 1. Приоритет источников и правила разрешения конфликтов

Использовать этот порядок:

1. **Текущая явная команда пользователя**.
2. **Свежий Google Drive `video-prompts.md`** — текущее состояние prompt master, scene IDs, active/work/slow statuses.
3. **`film-analysis.md`** — фактическая карта текущей сборки фильма и ограничения достоверности.
4. **`film-backlog.md`** — задачи, зависимости, рекомендации и исторические производственные заметки.
5. **Старые Notion notes** — источник старого замысла/архива, не второй master.
6. Память чата, Library-копии, старые экспорты и исторические файлы.

### Важное предупреждение о backlog

`film-backlog.md` синхронизирован 16.09.2026 и в некоторых operational-строках уже устарел. Например, там исторически встречается старый набор slow-сцен. Для **текущего списка active/slow/work** всегда использовать свежий `video-prompts.md` / `project-status.json`.

Активные W-items на 17.09.2026 — **только W5, W7, W8**. Старые W1/W2/W3/W4/W6 в backlog могут оставаться как история задач/зависимостей и не означают, что они снова активны как W-items master.

---

## 2. Текущее подтверждённое состояние master

**Ревизия master:** 17.09.2026  
**Последняя полная синхронизация, заявленная master:** 17.09.2026 · 20:42 (+03:00)

- Active scenes: **17**
- Full prompt texts: **20**
- Work items: **W5, W7, W8**
- Slow scenes: **2, 6, 12, 14, 15, 18**
- Scene IDs: **1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18**
- Latest scene ID: **18**
- `project-status.json`: **schema v3 · health: ok · audit fingerprint активен · instruction_sync: unverified**

### Активные сцены — быстрый индекс

1. **Джедаи на крыше — проход с зажжёнными мечами**
2. **Джедаи на крыше — триумфальный марш без мечей** — `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`
3. **Космическая погоня — экстерьер**
4. **Космическая погоня — интерьер кабины**
5. **Космическая погоня — единый дубль через стекло**
6. **Подводный рынок — странный фрукт** — `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`
7. **Канцлер — зеркало в туалете**
9. **Пещера — бой с монстром**
10. **Кантина — допрос про товар, часть 1**
11. **Кантина — допрос про товар, часть 2**
12. **Кантина — вход двух джедаев**
13. **Совет джедаев — говорящий кот**
14. **Канцлер — сбор грибов в гигантском лесу** — `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`
15. **Кашиик — сверхбыстрые прыжки между гигантскими деревьями** — `⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`
16. **Татуин — гигантский пустынный червь и бой на руинах**
17. **Пещера — передышка после монстра и разговор о карте**
18. **Имперский крейсер — Канцлер и офицер в коридоре**

### Кандидаты на отдельное обсуждение правок

- **NEEDS_FIX:** 3, 4, 6, 10, 11, 13, 17.
- **NEEDS_RERENDER:** 18.
- Это очередь для обсуждения с пользователем. Нельзя автоматически переписывать prompt только из-за статуса.
- Для 6 и 18 одновременно действует slow-lock: текущий render не трогать и не дублировать.

### Текущие work items

- **W5 — Канцлер и Warcraft 3.** Сквозная мотивация: Канцлер хочет сесть играть/успеть на турнир по Warcraft 3, а джедаи мешают. Ключевой незакрытый вопрос — что конкретно даёт карта и как это связано с существующим игровым финалом.
- **W7 — Переходы между группами.** Сначала проверять существующий материал и звуковые/визуальные мосты. Ключевые места: выход из Татуина к Набу, после монстра к лесной группе, после захвата карты к компьютеру. Не генерировать длинные одинаковые перелёты без необходимости.
- **W8 — Недоделанные гонки и транспорт.** Для космической погони выбрать **сцены 3+4 ИЛИ сцену 5**. Для татуинского транспорта/погони сначала сверить, какие дубли действительно недоделаны и как они связаны со сценой 16; не регенерировать всё движение транспорта целиком.

---

## 3. Slow-generation — критическое правило

Точная видимая метка:

`⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ`

Текущий список: **2, 6, 14, 15**.

Не запускать повторно без:
- готового результата;
- явной ошибки/failed generation;
- или отдельного решения пользователя на новый запуск.

Slow-status должен совпадать в **4 местах master**:
1. верхний global status block;
2. dedicated slow-generation table/block;
3. TOC row;
4. full scene section.

---

## 4. Текущее состояние самого фильма

- Рабочая длительность анализировавшейся сборки: **58:48,789**.
- Это большой уже собранный фильм в CapCut, близкий к завершению, а не набор несвязанных тестов.
- Текущая подтверждённая последовательность миров после космического блока: **Татуин → Набу → Кашиик**.
- В существующем монтаже уже есть значительные транспортные, боевые и переходные блоки. **Не считать, что всё перемещение между сценами нужно генерировать заново.**
- Warcraft-финал у компьютера уже существует; новая мотивация «турнир / Warcraft 3» должна аккуратно подвести к нему, а не дублировать финал.
- Линия трёх фрагментов карты остаётся одним из главных сюжетных мест, где нужна ясность: кто владеет конкретным фрагментом, что он даёт и как результат поиска связан с финалом.
- После победы над пещерным монстром нужен понятный смысловой выход к следующей линии; сцена 17 предназначена для передышки/разговора о карте.
- Переходы между крупными группами и мирами лучше закрывать минимально необходимой функцией: существующий план, короткая вставка, реплика, звук или небольшой новый ролик — **не автоматически длинный новый перелёт**.

### Ограничение достоверности анализа

Не утверждать, что весь 58:48 фильм был непрерывно просмотрен и прослушан в реальном времени, если этого фактически не произошло. `film-analysis.md` основан на структурном анализе, сохранённых кадрах/контактных листах, HTML/CSV/архиве свидетельств и ASR. Точные склейки, говорящие и мелкие AV-детали при необходимости требуют ручного воспроизведения.

---

## 5. Рабочий стиль промтов и референсов

- Пользователь предпочитает **отдельные сцены и готовые production prompts**, а не расплывчатые идеи.
- Для видеомоделей финальные промты обычно удобнее на **английском**, а русские реплики оставлять на русском, если сцена требует диалога.
- Сохранять между сценами консистентность внешности, одежды, окружения, цветокоррекции, света и направления движения камеры.
- Камера: физически стабильное кинематографичное движение, контролируемая инерция, без случайного jitter/micro-shake.
- Пространство должно оставаться единым и понятным: не создавать внезапно новую геометрию; объекты лучше открывать движением камеры.
- `@image1`, `@video1` и т. п. **локальны для конкретной сцены**.
- Реальный character/model reference имеет приоритет для лица и одежды; environment/group ref не должен усреднять/подменять индивидуальные лица.
- Если задан **single continuous take**, не смешивать его с hard cuts, shot/reverse-shot и insert cuts без явной причины.
- A/B-варианты одной смысловой сцены хранить **внутри одного scene ID**, а не создавать параллельные scene IDs без необходимости.
- Готовый текст промта ≠ готовый ролик. Не объявлять сцену завершённой, пока пользователь не подтвердил результат.
- После принятого ролика удалить сцену/промт из active master, **если он больше не нужен для доработки**.

---

## 6. Архитектура v3.5 — как всё синхронизируется

### Единственный editable master

Google Drive:
`AI Film Prompts Master/video-prompts.md`

File ID:
`1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`

### Routine workflow

**fresh-read Drive master → edit same Drive file ID → update `SYNC-TRIGGER.txt` → `sync-from-drive.yml` → validation → GitHub `video-prompts.md` + `project-status.json` → GitHub Pages → verification**

`sync-from-drive.yml` дополнительно выполняет страховочную проверку примерно каждые 30 минут. Он автоматически читает Drive master. Пять приватных Drive-инструкций сейчас не скачиваются Actions анонимно: их канонические Drive-версии зеркалируются в GitHub/Library/Notion через authenticated checkpoint-путь.

`project-status.json` schema v3 сохраняет старые поля и добавляет `canonical_master_sha256`, `audit_fingerprint`, optional validated `scene_meta`, generated `render_state` и `instruction_sync`. Для slow-сцен `render_state = SLOW_PENDING` вычисляется из существующего slow-list — отдельное пятое ручное поле не создаётся.

Пять Drive-инструкций (`AI-PROJECT-GUIDE.md`, `SYNC-RUNBOOK.md`, `USER-GUIDE.md`, `README-AI-SYNC.md`, `CLAUDE-TAKEOVER-RUNBOOK.md`) канонические для своих GitHub/Library/Notion-копий. Полный нормативный operational block находится в `SYNC-RUNBOOK.md`; остальные entry-point документы держат короткий safety-summary.

### Что НЕ является gate обычной правки сцены

- ChatGPT Library
- Notion
- Drive `video-prompts.html`

Это backup/documentation layers.

### Когда нужен полный checkpoint всех зеркал

Только при:
- explicit backup/checkpoint;
- изменении архитектуры/инструкций;
- восстановлении после desync;
- или команде пользователя **«полная ручная синхронизация всего и везде»**.

---

## 7. Integrity rules master

Перед записью/публикацией проверить:

- declared scene count = количество `## Сцена N`;
- declared scene count = количество TOC rows;
- TOC IDs = section IDs;
- IDs уникальны и возрастают; **непрерывность не требуется**;
- declared prompt count = фактическое число fenced prompt blocks;
- W-count = реальное число W-items;
- slow-count/list совпадает с dedicated slow table, TOC и sections;
- нет второй старой версии изменяемой сцены в другом месте файла.

`project-status.json` schema v3 генерируется автоматически. **Не редактировать его вручную.** Если `scene-meta` присутствует, невалидный JSON/state/duration/dependency target должен валить validation. `instruction_sync: unverified` не считать ошибкой master и не подменять на `ok` без фактической authenticated проверки.

Нельзя писать пользователю `ГОТОВО`, пока обязательная для выбранного режима проверка реального результата не выполнена.

---

## 8. Постоянные Drive точки

Главная папка `AI Film Prompts Master`:
`1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`

- `video-prompts.md` — `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- `video-prompts.html` — `1AZK6XafZng4M_I7ciqdhEjfgfkf3CA01`
- `NEW-CHAT-HANDOFF.md` — `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- `SYNC-RUNBOOK.md` — `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `AI-PROJECT-GUIDE.md` — `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `USER-GUIDE.md` — `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` — `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `CLAUDE-TAKEOVER-RUNBOOK.md` — `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`
- `film-analysis.md` — `1O3bsGGivBktRSbeg-9JWeMLK4J_JYu0M`
- `film-backlog.md` — `1YixC7zQFY7z3Bn1XGXxeQIMema3inCT9`
- `Seregius_montazhny_razbor.html` — `1SVXdiYVrBuEw0Zogo-gLZ2pdym2P3GYw`
- `EDIT_PLAN_V2.csv` — `1Qyh8qQNVwESWzNt8DeweJQS0jSYvGJvb`
- `PROGRESS.md` — `1zy6CE3ypHWUlCT75AGHzJeVCYG5PIHg3`

Notion Hub:
`3ddfe763-7762-81c0-b8fd-e7c61895df4a`

---

## 9. Публичные точки

- Viewer: `https://virudik.github.io/ai-film-prompts/`
- GitHub repo: `https://github.com/virudik/ai-film-prompts`
- Raw master: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/video-prompts.md`
- Film map: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-analysis.md`
- Backlog: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/film-backlog.md`
- Sync runbook: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/SYNC-RUNBOOK.md`
- Claude takeover: `https://raw.githubusercontent.com/virudik/ai-film-prompts/main/CLAUDE-TAKEOVER-RUNBOOK.md`
- Rendered montage review: `https://virudik.github.io/ai-film-prompts/Seregius_montazhny_razbor.html`

### Control Center / русские подписи

`index.html` — read-only Control Center. Пользовательские подписи и статусы должны отображаться по-русски (`Медленная генерация`, `В работе`, `Ревизия`, `Синхронизация`, `Инструкции: НЕ ПРОВЕРЕНЫ`, `Контрольный отпечаток`). Machine enum-значения schema v3 сохраняются без переименования.

Фильтры/чипы строятся только из `project-status.json`/`scene_meta`; нельзя hard-code scene/status list в HTML.

### Site invariants

- `index.html` — viewer, **не master**.
- Он читает root `video-prompts.md` + `project-status.json` с `cache: no-store`.
- `Инструкция для ИИ` и `Для владельца` — две соседние half-width buttons.
- `Инструкция для ИИ` не должна переноситься (`white-space: nowrap`).
- `Монтажный разбор фильма` открывает rendered Pages HTML.
- Legacy `_source/part-*` + `build-master.yml` не использовать.
- Obsolete one-time instruction finalizer отключён/manual-only и не должен снова становиться частью обычного pipeline.

---

## 10. Последний подтверждённый технический health

`project-status.json`:

- schema_version: **3**
- canonical_master_sha256: **`a739d6890382e54c443958c1e1d124a147aa29fed50a321328c22a5dd2060520`**
- scenes: **17**
- prompt_texts: **20**
- work_items: **W5, W7, W8**
- slow_scenes: **2, 6, 12, 14, 15, 18**
- generated slow render_state: **SLOW_PENDING = 2, 6, 12, 14, 15, 18**
- instruction_sync: **unverified** (automatic authenticated Drive instruction verification not configured)
- health: **ok**
- все обязательные integrity/scene-meta checks: **true**
- текущие slow-render engines подтверждены Topview read-only сверкой: **2/6/14 = Seedance 2.5; 12/15/18 = Wan 3.0**

GitHub Actions / Pages:

- checkpoint master-sync: **run #91 = success**;
- checkpoint Pages deployment: **#131 = success**;
- более новые номера всегда сверять live; номера run/deployment не являются вечным каноническим статусом.

### Известное ограничение независимой HTTP-проверки

Управление репозиторием/Actions/Pages работает. Отдельная «visitor-style» HTTP-проверка сайта из некоторых изолированных инструментов может не сработать из-за DNS/network/safe-browsing ограничений среды. Это **не означает автоматически**, что сайт упал или недоступен пользователю. Не путать внешний fetch-инструмент с правами управления GitHub Pages.

---

## 11. Что читать новому основному редактору

Минимальный порядок восстановления:

1. **этот `NEW-CHAT-HANDOFF.md`**;
2. `SYNC-RUNBOOK.md`;
3. `AI-PROJECT-GUIDE.md`;
4. **fresh Drive `video-prompts.md`**;
5. если задача касается сюжета/монтажа/continuity — `film-analysis.md` + `film-backlog.md`;
6. для глубокого монтажа — `Seregius_montazhny_razbor.html`, `EDIT_PLAN_V2.csv`, `PROGRESS.md`.

После чтения handoff **не считать цифры внутри него вечными**: перед реальной работой всё равно сверить fresh master и `project-status.json`.

---

## 12. Роли ИИ

- **ChatGPT** — основной редактор по умолчанию.
- **Work** — для больших многосценовых/монтажных/audit-задач; при записи в master тот же Drive file ID.
- **Claude** — review-only по умолчанию; если явно назначен временным основным редактором, читать `CLAUDE-TAKEOVER-RUNBOOK.md`.
- **Gemini** — независимая проверка prompt + visual references.
- **DeepSeek** — технический аудит конфликтов, камеры, timing, overload, continuity.
- **Grok** — creative/comedy/pacing second opinion.
- Другие ИИ — review-only, пока пользователь явно не передал им роль основного редактора.

Советы внешних ИИ возвращать как patch/replacement/recommendation. Канон меняет один текущий основной редактор.

---

### Topview как дополнительный production evidence

Подключённый Topview доступен основному редактору для read-only сверки boards/tasks: status, model, prompt, timestamps и наличие результата. Его можно использовать для проверки актуальности конкретной генерации **после однозначного сопоставления со сценой**.

Topview не заменяет Drive master. `status=success` означает технически завершённую генерацию, но не user approval; неоднозначные tasks не меняют canonical scene state автоматически.

## 13. Library / Notion / исторические копии

- Library — резерв ChatGPT, не источник истины.
- Notion — navigation/documentation/старые идеи, не второй master.
- Drive `video-prompts.html` — производный viewer/backup, не editable master.
- Исторический Library `video-prompts(1).md` — старая отдельная compilation, **не canonical master mirror**; не перезаписывать его как master и не считать актуальным master.
- Старые Library/HTML копии можно обновлять при полном checkpoint, но routine scene edit от них не зависит.

---

## 14. Когда и как обновлять этот handoff

Этот файл нужно актуализировать:

- после **существенного изменения состава active/work/slow сцен**;
- после смены архитектуры синхронизации, путей, file IDs или репозитория;
- после крупного монтажного решения, которое меняет film-analysis/backlog;
- после полного checkpoint;
- периодически как страховочную контрольную точку, даже если архитектура не менялась.

При каждом обновлении:

1. fresh-read `video-prompts.md`;
2. проверить `project-status.json`;
3. при story/continuity изменениях сверить `film-analysis.md` и `film-backlog.md`;
4. обновить **этот же Drive file ID** `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`;
5. не создавать `NEW-CHAT-HANDOFF-v2/v3/final/copy` как отдельные файлы;
6. если handoff зеркалируется в GitHub/Library — обновлять зеркала из этой версии, но **Drive остаётся основной копией handoff**.

---

## 15. Готовая команда новому ChatGPT

> Мы продолжаем AI-film project. Сначала прочитай свежие Google Drive `NEW-CHAT-HANDOFF.md`, `SYNC-RUNBOOK.md`, `AI-PROJECT-GUIDE.md` и `video-prompts.md`, затем повтори `audit_fingerprint` из `project-status.json`. Единственный editable prompt master — Drive `video-prompts.md` с file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`. Не создавай второй master. Перед любой записью fresh-read master. Scene IDs стабильны и могут иметь gaps. Текущий active/work/slow status бери из fresh master / `project-status.json`, даже если `film-backlog.md` содержит более старый operational status. Slow-сцены нельзя перезапускать без результата/ошибки или моего разрешения; machine `render_state` вычисляется из slow-list. Для story/continuity используй `film-analysis.md` и `film-backlog.md`, но не утверждай непрерывный просмотр всего фильма, если его не было. Routine sync: Drive → trigger → validation → GitHub/status → Pages. `instruction_sync: unverified` означает отсутствие автоматической authenticated проверки приватных инструкций, а не поломку master. Library/Notion/Drive HTML — backup/documentation layers. Перед `ГОТОВО` проверь обязательный фактический результат.

---

**Принцип этого файла:** он нужен не для замены master/runbook/analysis, а чтобы следующий чат за несколько минут понял, **где истина, что сейчас происходит, что нельзя случайно сломать и что читать дальше**.
