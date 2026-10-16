# Перелёты и посадки Серёги + ревизия «Сцен в работе» — предложение владельцу

> **Ответы владельца 16.10.2026:** 1 — да; 2 — да; 3 — финальный компьютер на борту у окна в космос, тот же ПК из храма, нужна Scene 41 (Сила несёт блок и монитор); 4 — Канцлер забирает татуинский фрагмент после драки на фоне червя, сцену продолжить (Scene 42); 5 — да; 6 — да (W9, W10, W12, W15 сняты); 7 — да (корзинка в 40 и 41). Всё внесено в master; актуальные тексты Scenes 39–42 — только там.
>
> **Статус 16.10.2026 (до ответов).** По команде владельца Scenes 39 и 40 внесены в `video-prompts.md` как DRAFT. Актуальный текст сцен — только в мастере: при внесении видеовход корабля заменён фактическими кадрами ч. 1 09:03 / 09:25 из пака Scene 37, а в 40 вид лесной планеты — созданным референсом Scene 37 (как в 37). Ревизия таблицы W внесена; W9, W10, W12, W15 помечены «ПРЕДЛОЖЕНО СНЯТЬ» до ответа владельца. Scene 41 не внесена — ждёт решения о финальном компьютере (вопрос 3). Вопросы 1–7 ниже остаются открытыми. Файл восстановлен 16.10 из журнала сессии 13.10 (сессия оборвалась на лимите до коммита); ниже — исходный текст разбора без изменений.

Проверено по `main` @ `a68be0d` (решение владельца 14.10 по сценам 36–37 уже внесено). В репозитории ничего не менялось, Topview не трогался.

**Источники и обозначения:**

- **[Р1]** — `Seregius_montazhny_razbor.html`, разбор 1: сборка 58:48,789 из двух частей. Таймкоды в нём локальные, «ч.1 / ч.2».
- **[Р2]** — `Seregius_montazhny_razbor-2.html`, разбор 2 от 24.09: новая сборка 01:03:42,848, сквозной таймкод, 78 участков. **Он свежее.** Все стыки ниже даны по его шкале.
- **[FA]** — `film-analysis.md`, 16.09. Это выжимка разбора 1, таймкоды в нём тоже локальные.
- Прочее: `video-prompts.md`, `NEW-CHAT-HANDOFF.md`, `reports/montage-plan-v3-draft.md`, `reports/prompt-drafts-2026-10.md`, `reports/scenes-36-37-proposal-2026-10-14.md`, `review-ledger.json`, `project-status.json`, тексты сцен 17, 20, 21, 26 из git (`0ca107d^`, `db010cf^`). Notion «Кино» (только чтение): «Перелёты между планетами», «Мостик крейсера», «Титры и пролёт к планет», «Финал», «Кашиик и вуки». Supabase `owner_decisions`: открытых задач про перелёты нет; есть только 16 (`needs_owner`), 17, 34, 36, 37.

**Важная оговорка о шкале.** После 24.09 в фильм вставлены сцены 10, 11, 17, 20, 21, 22, 23, 26 и 29. Их точные таймкоды в `review-ledger.json` не записаны (`insert_timecode: null`). Поэтому все стыки ниже привязаны к соседним кадрам [Р2], а не к абсолютной секунде нынешнего монтажа.

**Расхождения между [FA]/[Р1] и [Р2]:**

- Шкалы разные. Пример: появление Канцлера на Набу — ч.2 16:40 в [Р1]/[FA] (≈44:11 сквозного времени старой сборки) против 47:35 в [Р2].
- Грибы (57:45–58:10) есть только в [Р2]. [FA] начинает лесной эпизод Канцлера прямо с моста (ч.2 25:25).
- Порядок миров (Татуин → Набу → Кашиик) совпадает во всех источниках.
- Везде, где источники расходятся, ниже указаны оба. Опора — на [Р2] как более свежий.

---

## 1. Маршрут Серёги по фильму

| № | Где | Таймкод [Р2] (сквозной) | Таймкод [Р1]/[FA] (локальный) | Как он туда попадает | Источник |
|---|---|---|---|---|---|
| 1 | **Корусант, кабинет**: голограмма с Юлей («хлеб и молоко»), арест, «Я и есть Сенат» | 01:20–06:00 (участки 03–06) | ч.1 01:20–06:00 | Начало фильма | [Р2] §5; [Р1] §3; [FA] |
| 2 | **Корусант, побег**: бой в кабинете → окно → прыжок на летящий корабль → волны противников на крыше | 06:00–09:20 (07–10) | ч.1 06:00–09:20; прыжок 06:55–07:13 | **Показано** (прыжок и приземление на крышу) | [Р2]; [Р1] §13 |
| 3 | **Корабль Канцлера**: люк, кабина, перелёт, прибытие в ангар | 09:20–09:55 (11) | ч.1 09:20–10:05; по [Р1] §13 «09:22–09:55 Люк/крыша, кабина, **гиперпереход**, корабль, ангар» | **Единственный полностью показанный перелёт Серёги** (отлёт, полёт, прибытие). Notion: «Прорубает люк. Захватывает корабль» → «Корабль стыкуется с крейсером». Этот корабль — транспорт Канцлера в 37 и в новых сценах ниже | [Р2] 11; [Р1] §13; Notion |
| 4 | **Крейсер Империи**: ангар, лифт, эскалатор, уборщица, зеркало, офицер, Вейдер-Юля и танец, разговор у карты, станция | 09:55–16:05 (12–18) | ч.1 10:05–15:35 (зеркала в [Р1] нет) | Прибытие показано (п. 3) | [Р2]; [Р1] |
| 5 | **Мостик во время космического боя**: мостик → окно → космос (Scene 21 уже в фильме, Серёга и Юля), сверхоружие, корова, разрушитель | 25:10–28:55 (33–37) | ч.1 23:55–27:31 | **Отлёт показан**: «Разрушитель, мостик, гиперпереходы» (37). По [Р1] §13 «в конце первой части мы остаёмся с кораблём канцлера». Куда он летит, не обозначено | [Р2] 33–37; [Р1] §3, §13; `review-ledger` 21 |
| 6 | **Татуин**: приход в кантину, бой внутри и снаружи, «Канцлер уезжает», гонка, бой на крыше машины, мечи-тормоза | 33:50–39:25 (43–49) | ч.2 03:50–09:30 | **Возникает в кантине «из ниоткуда»**: прилёт и корабль не показаны. [Р1] §4: «Желательно, чтобы он появился по понятному следу». [Р2] 43: «Установить его цель». Отлёт с Татуина **не показан**. Scene 16 (червь: Илюша, Артём, Серёга) — кандидат развязки W6. В сборке [Р2] её нет. Кнопки «Принять» и «Переделать» конфликтуют (`needs_owner`). Татуинский фрагмент к Серёге **не переходит** (M1/D6 открыты; в 16 «do not add a map exchange») | [Р2] 43–49, §8; [Р1] §4; master Scene 16 |
| 7 | **Набу**: подводный город, дуэль, затопление, бой снаружи, на морском существе, в пещере, общий бой с монстром | 47:35–51:52 (61–64) | ч.2 16:40–20:55 | **Возникает в подводном городе «из ниоткуда»**. Прилёт не показан. [Р2] §9: «Это параллельная линия, пока Канцлер снова не появится в ней». После боя — **Scene 17 (в фильме)**: передышка, шёпот, Паша отдаёт модуль. Затем **36 (DRAFT)**: уход к водяной завесе. Затем **37 (DRAFT)**: взлёт с луга у озера, космос, без посадки. ⚠ 37 начинается с корабля, **стоящего на лугу у озера**, но как этот корабль там оказался, фильм не показывает | [Р2] 61–64, §9, §3; ledger 17; master 36–37 |
| 8 | **Лесная планета (Кашиик)**: грибы, адвокат, дуэль, силовой захват фрагмента, вмешательство вуки | 57:45–01:02:45 (73–77) | ч.2 25:25–30:19 (грибов нет) | **Первое появление — грибы, 57:45**. По решению владельца 14.10 посадки нет, сюрприз с корзинкой сохраняется. Фрагмент оказывается в его руке около 01:02:00–01:02:05. Отлёт **не показан**. [Р2] §10: «Можно закончить лес его исчезновением с предметом… Не требуется отдельный взлёт, перелёт и посадка» | [Р2] 73–77, §10, §11; [Р1] §4; NEW-CHAT-HANDOFF «Что открыто» п. 6 |
| 9 | **Планета ситхов** (новая ветка, её нет ни в [Р1], ни в [Р2]): коты-магистры обращаются к Серёге (Scene 26 — **в фильме**, место вставки не записано; Серёга за кадром) → бой 27, 30–32 (slow) → руины 33 → храм 34 → находка ПК 35 → осмотр ПК 38 | — | — | **Прибытие не показано ни в одной сцене.** Монтажный план v3 §3: дыры 10–11 («зачем Серёге планета ситхов»). Место ветки не решено (D1). По плану v3 рекомендован вариант A: после Кашиика, перед компьютером. Подсказка — реплика Рыжика из 26: «…разобрался с этими [грубость] и алкашами…». Исход боя (D2) не определён | `review-ledger` 26; master 27, 30–35, 38; montage-plan-v3 §2.3, §3 |
| 10 | **Финал: CRT и Warcraft** | 01:02:45–01:03:42,848 (78) | ч.2 30:19–31:17,522 | Как он туда попадает, **не показано**. [Р2] §10: «Сейчас переход к компьютеру очень быстрый». Обстановка по [Р1] §1: «Warcraft на старом мониторе **в космическом окружении**»; §8 вариант Б: «огромное космическое окно; на столе старый монитор». Значит, финальный компьютер стоит **на борту, у окна в космос**, а не в храме. Сверить по кадру 01:02:45 | [Р2] 78; [Р1] §1, §8 |
| 11 | Титры: имперский танец (Scene 28) | после финала | — | Внесюжетная кода | master 28 |

**Порядок (однозначно для 1–8, 10; для 9 — рекомендация плана v3):** Корусант → его корабль → крейсер → мостик в космосе → Татуин → Набу → Кашиик → *[планета ситхов]* → компьютер/Warcraft → титры.

Сцены 23–25 — перелёт **котов**, а не Серёги: 23 — шестеро джедаев на крыше Корусанта превращаются в котов; 24 — запуск; 25 — космический бой. Серёги там нет. Его прибытие на планету ситхов не закрывает ни одна существующая сцена.

---

## 2. Пробелы и решения по каждому переходу

Правило проекта (W7; [Р2] §10; [Р1] §10): генерировать только недостающую функцию. Без пакета одинаковых «взлёт — полёт — посадка».

| Переход | Отлёт | Прилёт | Решение |
|---|---|---|---|
| Корусант → крейсер | показан (09:20) | показан (09:55) | **Ничего не нужно.** [Р2] 11: «Не удлинять процедурой посадки»; [Р1] §13: «Не удалять все перемещения подряд» |
| Крейсер/бой → Татуин | показан: гиперпереходы разрушителя (28:55) | **не показан**; появление в кантине 33:50 | **Без генерации, монтажная задача.** Оставить один ясный уход корабля Канцлера в гиперпространство как отлёт: [Р2] 37 «Оставить один ясный выход из блока», [Р1] §13 «Можно закончить первую часть одним уходом корабля канцлера». Причину появления в кантине закрывает **W11** (реплика или сигнал), а не посадка: [Р1] N4 «маяк под стойкой», [Р2] §6 «источник координат». Посадка сама по себе причину появления не объясняет |
| Татуин → Набу | **не показан** | **не показан**; Серёга возникает в подводном городе 47:35, а 37 начинается с корабля на лугу | **Новая Scene 39 «Прибытие на Набу»** — стык около **45:05** [Р2]: после «Бег и прыжок в воду» (57, 44:45–45:05), перед «Подводный путь и город» (58). Отлёт с Татуина не генерировать: [Р2] §9 «параллельная линия» |
| Набу → Кашиик | 36 + 37 (решение 14.10) | **посадки нет — решение владельца 14.10** | **Новых сцен нет.** Монтаж: 36 → 37 (10–15 с, финал в космосе) → существующий участок «корабль другой пары» 51:52 [Р2] 65. Не выдавать корабль пары за корабль Серёги: [Р2] 65 «не выдавать её за отлёт троих из пещеры». Первый кадр Серёги на Кашиике — грибы, 57:45 [Р2] 73: «Защитить внезапный бытовой контраст» |
| Кашиик → планета ситхов | **не показан** | **не показан**; 26 (в фильме) начинается с котов, которые говорят с невидимым Серёгой | **Новая Scene 40 «Прибытие на планету ситхов»**: начинается сразу в космосе, без взлёта с лесной планеты ([Р2] §10 «Не требуется отдельный взлёт»). Заканчивается посадкой у руин и взглядом за кадр. Затем склейка на 26 |
| Коты 25 → 26 | — | — | Линия котов, не Серёги. Монтажная склейка, вариант (а) из `prompt-drafts` §3.2. Новых сцен не нужно |
| Планета ситхов (ПК 35/38) → финальный CRT | — | — | **Зависит от D4.** Если финальный компьютер — тот же ПК и стоит на борту (по [Р1] §1, сверить), нужна **Scene 41 «Серёга увозит древний ПК»** (кандидат, текст ниже). Если финал переносится в храм или это другой компьютер — 41 не нужна, хватит монтажной склейки |
| Татуин внутри блока (погоня → червь 16) | — | — | Не перелёт. Сначала решения по 16 и D6, затем W6/W8 |

**Проверка в первую очередь, как просили:**

- **Посадка на лесную планету перед грибами (57:45)** — по источникам не нужна:
  - владелец 14.10 выбрал вариант A «без посадки»;
  - [Р2] 73 защищает «внезапный бытовой контраст»;
  - готовый кадр посадки (51:52) принадлежит другой паре.
  - Отдельную посадку генерировать не предлагаю. Если владелец передумает (вариант B из `reports/scenes-36-37-proposal-2026-10-14.md`), текст пишется по шаблону Scene 39.
- **Прибытие на планету ситхов** — нужно обязательно. Без него вся новая ветка (26 в фильме, 27, 30–38) начинается «из ниоткуда». Решение — Scene 40.

---

## 3. Новые сцены

Свободные ID: 39, 40, 41. Зарезервированы 1–7, 9–12, 14, 15, 17–23, 26, 29 (`project-status.json`). Все три сцены: Wan 3.0, 30 с, без речи. Транспорт везде один и тот же: корабль Канцлера из ч.1 (09:20–09:55). Серёга всегда один. `dependencies: []`: соседние 36, 37, 38 активны, но хронологически стоят после или в другой ветке, а 17 и 26 зарезервированы. Связи описаны в «Контексте».

**После утверждения (детерминированно, делает агент):**

- вставить блоки в master (порядок по ID, после 38) и строки в индексную таблицу;
- добавить в `character-references.json` Серёге сцены 39, 40, 41;
- создать манифесты `references/scenes/scene-39…41` с `remaining`;
- валидатор → Pages.

Запуск — только по команде владельца, через сайт Topview, в безлимите.

<a id="scene-39"></a>

## Сцена 39 — Серёга прибывает на Набу: посадка у брошенной стоянки рыбаков

<!-- scene-meta: {"target_engine":"Wan 3","production_state":"DRAFT","duration_s":30,"dialogue":{"enabled":false,"language":null},"dependencies":[],"tags":["serega","travel","landing","naboo","lake","continuity"]} -->

**Контекст использования:**

- **Стык:** около **45:05** по сборке 01:03:42 [Р2], между участками 57 «Бег и прыжок в воду» (44:45–45:05) и 58 «Подводный путь и город». Если владелец решит иначе, допустим стык перед 47:35 (участок 61 «Канцлер, дуэль»). Но тогда сцена разорвёт передачу модуля правителем Саше и вход Канцлера, поэтому этот вариант не рекомендую.
- **Функции:**
  - (1) объяснить, как Канцлер оказался на Набу: по [Р2] §9 и 61 он возникает в подводном городе без прибытия; [Р1] §10: «один канцлер не должен необъяснимо находиться… Его маршрут необходимо обозначить»;
  - (2) **поставить на луг у озера тот самый корабль, с которого он взлетает в утверждённой Scene 37** — сейчас его посадка нигде не показана;
  - (3) показать, что он идёт по следу пары: брошенная стоянка, круги на воде.
- **Корабль** — собственный корабль Канцлера из начала фильма (ч.1 09:20–09:55), тот же, что в 37. Не корабль Паши и Саши и не их водная машина.
- **Модуля карты в кадре нет.** Татуинский фрагмент к Серёге не перешёл (M1/D6 открыты), набусский он получит только в Scene 17.
- **Свет** — как в кадре бега и прыжка пары (участок 57). [Р2] отмечает там закатный свет при дневной сцене Маши.
- **Комедийный контраст:** пара в панике бежала и прыгала, а Серёга спокойно входит в воду в мантии. Персонажи под водой без снаряжения — это правило мира фильма ([FA]: «персонажи под водой в своей одежде»).
- В монтаж достаточно 10–15 с.
- **До READY выгрузить из монтажа:**
  - @Video1 — корабль и кабина Канцлера (ч.1 09:20–09:55, те же кадры, что для 37);
  - @Video2 — берег со стоянкой сразу после прыжка пары (около 44:45–45:05 [Р2]; ящики с рыбой — участки 53–55).
- Без них DRAFT. Запуск — только по команде владельца.

**Референсы:**

- @Image1 — <a href="references/full/serega.jpg">Серёга</a>;
- @Image2 — <a href="references/scenes/scene-19/S19-Image1-topview-source.png">пейзаж Набу: озеро, луг, дворец на дальнем берегу</a> (только пейзаж; рыбаков с кадра не переносить);
- @Video1 — корабль Канцлера из ч.1, 09:20–09:55 (выгрузить перед запуском);
- @Video2 — брошенная стоянка у озера после прыжка пары, около 44:45–45:05 (выгрузить перед запуском).

<div class="scene-ref-gallery">
<figure><a href="references/full/serega.jpg" target="_blank" rel="noopener"><img src="references/full/serega.jpg" alt="@Image1 — Серёга"></a><figcaption>@Image1 — Серёга</figcaption></figure>
<figure><a href="references/scenes/scene-19/S19-Image1-topview-source.png" target="_blank" rel="noopener"><img src="references/scenes/scene-19/S19-Image1-topview-source.png" alt="@Image2 — озеро Набу"></a><figcaption>@Image2 — озеро Набу</figcaption></figure></div>

**Что происходит:** Вечером корабль Канцлера опускается над озером Набу и садится на луг недалеко от брошенной стоянки рыбаков. Серёга выходит один, проходит мимо брошенных удочек и ящиков, переполненных рыбой, и смотрит на них с каменным неодобрением. На воде ещё расходятся круги от прыжка джедаев. Он не спеша входит в озеро прямо в мантии и погружается. На берегу остаются стоящий корабль и пустая стоянка.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal live-action space-opera cinema | Serega alone lands his own craft beside an abandoned Naboo fishing camp and calmly follows the Jedi into the lake

REFERENCES / AUTHORITY ORDER:
@Video1 — Serega's own craft exactly as already shown earlier in the film: hull shape, colour, proportions, engines, landing gear and hatch. It is the only authority for the vehicle; do not design a new ship.
@Video2 — the exact Naboo lakeshore fishing spot as already established in the film, moments after two fishermen ran off and jumped into the lake: shoreline shape, meadow, camp leftovers, light direction and time of day. It controls the location layout and light; no person from it appears in this shot.
@Image2 — Naboo landscape look: calm blue lake, bright green lakeshore meadow, rounded trees, a pale domed palace on the far shore. Landscape and architecture only; the two fishermen in this image are NOT part of the shot.
@Image1 — absolute identity of SEREGA.
Priority: @Video1 controls the vehicle; @Video2 controls the location layout and light; @Image2 fills in landscape detail where @Video2 is ambiguous; @Image1 controls Serega's face and costume.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image1 is the absolute visual authority for SEREGA (the Chancellor): pale older man, sparse light hair with a bald crown, mature serious face, long deep dark-purple robe with the hood lowered, dry at the start of the scene. He is the only person in the entire scene. No fishermen, no Jedi, no Gungans, no droids, no cats.

VEHICLE / LANDING LOCK — CRITICAL:
One and the same craft from @Video1 in every shot: same silhouette, colour, engine glow and scale. Realistic, unhurried landing: smooth descent, a short flare, touchdown on its landing gear, engines spooling down. After touchdown the craft stays parked on the meadow for the rest of the scene. No second ship, no water vehicle driving, no crash, no hovering speeder.

CAMP / PROP LOCK:
The abandoned camp is exactly what @Video2 shows: fishing rods dropped on the grass, crates overflowing with caught fish, a few empty brown bottles, a cold fire spot. Do not add tents, tables, people or extra vehicles. No map, glowing module, hologram or any glowing object exists in this scene.

START STATE:
Evening over the Naboo lake as in @Video2: the calm water still rippling where the fishermen jumped in, the camp abandoned on the shore, the meadow empty. Serega's craft is a small shape descending from the sky above the far end of the lake.

TIMELINE:
[0:00–0:06] — DESCENT OVER THE LAKE
Wide exterior. The craft descends in a smooth curve over the calm lake toward the near shore; the pale palace domes stand on the far bank; the craft's reflection slides across the water; the engine whine grows.

[0:06–0:12] — TOUCHDOWN ON THE MEADOW
The craft flares and settles on its landing gear on the green meadow a short walk from the camp. Grass flattens in a ring, the shallow water near the bank ripples under the engine wash, the engines spool down to silence.

[0:12–0:18] — STEPPING OUT
Closer angle: the hatch opens exactly as on @Video1. Serega steps down alone onto the grass, straightens his robe once and surveys the shore with a cold, appraising look.

[0:18–0:24] — THE ABANDONED CAMP
The camera tracks with him at walking pace past the camp: the dropped rods, the overflowing fish crates, the empty bottles. He stops at the crates for one beat and looks down at the absurd pile of fish with completely deadpan disapproval, then lifts his eyes to the lake, where the last rings of the fishermen's dive are still spreading.

[0:24–0:30] — INTO THE LAKE
Without hurry and without hesitation he walks straight into the lake in his robe: ankles, knees, waist, chest; the dark-purple fabric darkens and spreads on the surface. He takes one calm breath and goes under. The surface closes over him and rings spread; the parked craft and the abandoned camp remain on the empty shore.

END STATE:
An empty evening lake with spreading rings where Serega went under; his craft parked on the meadow; the abandoned camp on the shore; nobody visible. A clean cut point to the existing underwater journey.

CAMERA / SPACE:
Wide establishing shots for the descent and the landing; one clean time-compression cut between [0:06–0:12] and [0:12–0:18]; after it, a steady tracking shot following Serega at walking pace to the water's edge, ending as a static wide on the lake for the submersion. Stable geography: lake on one side of frame, parked craft on the other, camp between them. Real human scale; the walk is a few dozen metres. No orbiting, no shake, no zoom jumps.

PERFORMANCE:
Serega is calm, cold and purposeful. The contrast with the fishermen's frantic run lies in his total lack of hurry. His disapproval of the fish is a tiny movement of the eyes, not a gesture to the camera. No speech, no smile.

LIGHTING / MATERIALS:
Warm low evening sun matching @Video2, long shadows across the meadow, soft reflections on the lake. Engine heat shimmer fading after touchdown. Glistening fish scales, wet grass, dry robe fabric turning dark and heavy as it soaks.

AUDIO:
Engine whine and wash, grass rustling, landing-gear servo whir, hatch hiss, footsteps on grass, flies buzzing over the fish crates, distant birdsong, gentle lapping water, the robe dragging through the water, one calm inhale, the water closing overhead. No dialogue, narrator or music.

NEGATIVE PROMPT:
fishermen, Jedi, any other person, Gungans, new or different ship design, second ship, crash landing, speeder or water vehicle in motion, map module, glowing object, hologram, scuba gear, diving mask, breathing apparatus, running, jumping, diving splash, swimming strokes, night sky, rain, comedy mugging, speaking, changed face or robe, cartoon CGI, subtitles, text, logo, watermark, black bars.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

---

<a id="scene-40"></a>

## Сцена 40 — Серёга прилетает на планету ситхов: посадка у руин

<!-- scene-meta: {"target_engine":"Wan 3","production_state":"DRAFT","duration_s":30,"dialogue":{"enabled":false,"language":null},"dependencies":[],"tags":["serega","travel","landing","sith_planet","map","bread_and_milk","continuity"]} -->

**Контекст использования:**

- **Стык:** после конца лесного блока (участок 77, 01:02:15–01:02:45 [Р2]: «Герои на земле, вмешательство вуки»; Канцлер уходит с фрагментом), перед **Scene 26** (уже в фильме): коты-магистры на террасе обращаются к Серёге за кадром. Всё это при условии, что ветка планеты ситхов стоит после Кашиика (D1, вариант A монтажного плана v3; реплика Рыжика «разобрался с этими… и алкашами» это поддерживает).
- **Функции:**
  - (1) Серёга появляется на планете ситхов не «из ниоткуда» — сейчас ни одна сцена его прибытие не показывает;
  - (2) причина полёта читается тем же приёмом, который владелец утвердил для 37 14.10: модуль светится ярче, когда направлен на цель. Это согласуется с идеей Саши «карты → координаты заброшенного объекта» (master, «Идеи от Саши»);
  - (3) финал — он слышит зажигание мечей и смотрит за кадр. Так невидимый адресат реплик в 26 становится им.
- **Без взлёта с лесной планеты:** [Р2] §10 — «не требуется отдельный взлёт, перелёт и посадка». Отлёт обозначен удаляющейся лесной планетой в боковом окне.
- **В кадре ровно один модуль** — лесной, только что отнятый ([Р2]: в руке Канцлера около 01:02:00–01:02:05). Счёт фрагментов не заявляется: татуинский — D6.
- Кабина и стикер «хлеб и молоко» — continuity с 37. Это не новый гэг.
- Корабль — тот же, что в 37 и 39.
- Направление взгляда в финале сверить с готовым результатом 26 в монтаже; при необходимости кадр зеркалится.
- Если владелец поставит 33 (руины) раньше котов, END этой сцены всё равно стыкуется: Серёга стоит у лестницы храма.
- В монтаж 12–20 с.
- **До READY выгрузить:**
  - @Video1 — корабль и кабина Канцлера (ч.1 09:20–09:55);
  - @Video2 — лесная планета из космоса (51:52–52:40 [Р2], только планета; тот же клип, что для 37);
  - сверить, что модуль в лесном захвате (01:02:00–01:02:05) того же дизайна, что @Image2. Если нет — заменить @Image2 кадром из монтажа.
- Запуск — только по команде владельца.

**Референсы:**

- @Image1 — <a href="references/full/serega.jpg">Серёга</a>;
- @Image2 — <a href="references/scenes/scene-17/S17-Image4-topview-source.png">модуль карты (дизайн-класс фрагментов)</a>;
- @Image3 — <a href="references/scenes/scene-27/S27-Image5-topview-source.png">точные руины планеты ситхов</a>;
- @Video1 — корабль и кабина Канцлера из ч.1, 09:20–09:55 (выгрузить перед запуском);
- @Video2 — лесная планета из космоса, 51:52–52:40 (выгрузить; только планета, корабль пары не использовать).

<div class="scene-ref-gallery">
<figure><a href="references/full/serega.jpg" target="_blank" rel="noopener"><img src="references/full/serega.jpg" alt="@Image1 — Серёга"></a><figcaption>@Image1 — Серёга</figcaption></figure>
<figure><a href="references/scenes/scene-17/S17-Image4-topview-source.png" target="_blank" rel="noopener"><img src="references/scenes/scene-17/S17-Image4-topview-source.png" alt="@Image2 — модуль карты"></a><figcaption>@Image2 — модуль карты</figcaption></figure>
<figure><a href="references/scenes/scene-27/S27-Image5-topview-source.png" target="_blank" rel="noopener"><img src="references/scenes/scene-27/S27-Image5-topview-source.png" alt="@Image3 — руины планеты ситхов"></a><figcaption>@Image3 — руины планеты ситхов</figcaption></figure></div>

**Что происходит:** Серёга один в кабине своего корабля, в открытом космосе. Лесная планета позади уменьшается. Он достаёт модуль, и тот светится ярче, когда Серёга направляет его на далёкую пыльную охристо-красную планету. Корабль снижается сквозь пыльную закатную дымку, пролетает мимо колоссальных статуй в капюшонах и садится на каменную площадь у лестницы храма. Серёга выходит, делает несколько шагов — и замирает: за кадром впереди загудел зажжённый световой меч. Он настороженно смотрит вперёд; кто там, не показывается.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal live-action dark space-fantasy | Serega alone flies on from the forest world, lands among ancient Sith ruins at sunset and senses he is not alone

REFERENCES / AUTHORITY ORDER:
@Video1 — Serega's own craft and cockpit exactly as already shown earlier in the film: hull shape, colour, proportions, engines, landing gear, hatch, cockpit layout, seats, windows and controls. It is the only authority for the vehicle and the cockpit; do not design a new ship.
@Image3 — the exact ancient ruin city of the destination planet: ochre-red and rust-brown carved stone, colossal hooded statues, a stepped temple facade with a wide central stair, broken pillars and a fallen colonnade, tall red rock spires, low golden-orange sunset, drifting dust haze. Absolute authority for the architecture, materials, palette and light of the landing site.
@Video2 — the green forest planet seen from space exactly as already established in the film. Use the planet only; any ship in that footage must not appear.
@Image2 — the exact map module prop design.
@Image1 — absolute identity of SEREGA.
Priority: @Video1 controls the vehicle and cockpit; @Image3 controls the destination world; @Video2 controls the receding forest planet; @Image2 controls the prop; @Image1 controls Serega's face and costume.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image1 is the absolute visual authority for SEREGA (the Chancellor): pale older man, sparse light hair with a bald crown, mature serious face, long deep dark-purple robe, dusty and creased after a recent fight but intact; a lightsaber hilt hangs at his belt. He is the only person in the entire scene. No cats, no Jedi, no Sith, no pilots, no droids.

PROP LOCK — CRITICAL:
Exactly ONE small rigid palm-sized rectangular map module from @Image2 is ever visible: rounded grey metal frame, dark-grey face, two vertical warm-amber glowing segmented panels. It comes out of the inner fold of his robe and goes back there. When its face is turned toward the destination planet the two amber panels brighten and pulse slowly and steadily; turned away, they dim to a soft glow. It never folds, multiplies, projects a hologram, shows a map image or becomes a screen.
COCKPIT NOTE: the same small square paper sticky note with a simple hand-drawn doodle of a loaf of bread and a milk bottle stays stuck on the console beside the controls — pictures only, no letters, words or numbers.

VEHICLE / LANDING LOCK — CRITICAL:
One and the same craft from @Video1 in every exterior shot: same silhouette, colour, engine glow and scale. Realistic, restrained travel: one approach, one atmospheric descent, one landing on its landing gear. No take-off from the forest world, no hyperspace tunnel, no other ships, no space battle, no crash.

LOCATION LOCK:
The destination is a dry, dusty canyon world with the ruin city of @Image3. No lava, no black basalt, no volcanic glow, no green vegetation, no open water. Fine dry dust and ash with rare ember-like sparks drift in the air near the ground.

START STATE:
Serega is already seated alone at the controls inside the cockpit from @Video1, in open space. Through the side window the small green forest planet from @Video2 is receding. The module is hidden in his robe. The bread-and-milk note is on the console.

TIMELINE:
[0:00–0:06] — THE MODULE POINTS ONWARD
Medium shot inside the cockpit. Serega takes the module from his robe. As he turns its face toward the front window, where a small dusty ochre-red planet hangs far ahead, the two amber panels brighten and pulse steadily. He glances once at the forest planet shrinking in the side window, slides the module back into his robe and corrects the heading with one hand.

[0:06–0:12] — APPROACH
Exterior from behind: the same craft flies toward the ochre-red planet; a thin golden band of sunset light runs along the edge of its hazy, dusty atmosphere. Steady left-to-right travel.

[0:12–0:18] — DOWN THROUGH THE DUST
The craft descends through orange dust haze. Red rock spires and deep canyons rise out of the haze, and the ruin city of @Image3 appears below in low sunset light.

[0:18–0:24] — LANDING AMONG THE STATUES
After one clean time-compression cut: a low wide shot. The craft glides past the colossal hooded statues and settles on its landing gear on a flat, dusty stone plaza at the foot of the wide temple stair. Dust billows outward in a ring and slowly settles; the engines spool down.

[0:24–0:30] — NOT ALONE
The hatch opens. Serega steps down onto the gritty stone and takes three unhurried steps toward the stair, then stops dead: a low lightsaber ignition hum sounds off-screen ahead. He narrows his eyes and looks steadily ahead past the camera toward the top of the steps; his hand moves to the hilt at his belt without drawing it. Hold.

END STATE:
Serega stands alone on the dusty plaza in front of his parked craft, looking ahead off-screen toward the top of the temple stair, his hand on the unlit hilt at his belt, dust drifting in the sunset light. Nobody else is visible. A clean cut point to the next scene, where his opponents are revealed.

CAMERA / SPACE:
Cockpit and exterior angles of one continuous journey; exactly one time-compression cut, into [0:18–0:24]; every other transition is a motivated camera move. Smooth inertial camera, credible ship scale against the planet, canyons and statues, a stable left-to-right travel direction in space. Low wide lens at the landing to show the scale of the statues. The final shot is a steady medium-wide frontal on Serega with the parked craft behind him. Never reveal what he is looking at.

PERFORMANCE:
Calm, tired and completely sure of himself; at the saber hum a sudden alert stillness, not fear. Small precise movements, no speech, no smile, no look into the lens.

LIGHTING / MATERIALS:
Cockpit: soft instrument glow and the module's warm amber light on his fingers. Space: hard sunlight and deep black. Planet: low golden-orange sunset through dusty air, long statue shadows across warm weathered stone, fine drifting dust and ash with rare ember-like sparks. Restrained colour grade matching the neighbouring ruin scenes.

AUDIO:
Cockpit switches, a faint soft electronic pulse from the module, a deep engine hum, the roar of atmospheric entry and wind through dust, the landing-gear servo, engines spooling down, the hiss of settling dust, wind across stone, footsteps on gritty stone, then one low lightsaber ignition hum off-screen ahead. No dialogue, narrator or music.

NEGATIVE PROMPT:
cats, Jedi, Sith, any other person, revealing the source of the saber hum, ignited saber in Serega's hand, second ship, other ships, take-off from the forest planet, forest floor, hyperspace tunnel, space battle, explosions, lava, volcanic glow, black basalt, green vegetation, water, temple interior, ancient computer, CRT monitor, Warcraft screen, two or three modules, hologram map, projected map, folded paper map, readable text on the note, new ship design, changed face or robe, cartoon CGI, subtitles, text, logo, watermark, black bars.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

---

<a id="scene-41"></a>

## Сцена 41 — Серёга увозит древний ПК с планеты ситхов (кандидат, по решению D4)

<!-- scene-meta: {"target_engine":"Wan 3","production_state":"DRAFT","duration_s":30,"dialogue":{"enabled":false,"language":null},"dependencies":[],"tags":["serega","travel","sith_planet","ancient_computer","depart","bread_and_milk","continuity"]} -->

**Контекст использования:**

- **Сцена-кандидат.** Нужна, только если владелец подтвердит, что существующий финальный компьютер (участок 78, 01:02:45 [Р2]) — это тот же ПК, найденный в храме (35/38), и стоит он **на борту**. По [Р1] §1 и §8 финал идёт «на старом мониторе в космическом окружении», у «огромного космического окна».
- **Сначала сверить по кадрам монтажа**, что финальный CRT и системный блок совпадают с находкой 35/38 (бежевый блок 1990-х, массивный CRT, клавиатура). Если не совпадают или финал переносится в храм — сцена не нужна, хватает склейки.
- **Стык:** после Scene 38 (и исхода боя D2), перед 01:02:45.
- **Функция** — физически связать находку в храме с уже существующим финалом: Серёга забирает ПК и улетает к флагману.
- **ПК несёт Сила** — бытовая левитация, как в любимом гэге фильма с уборщицей и мокрым полом ([Р1] §2, §16). Это творческая деталь: если владелец против, ПК несут руками, и в тексте меняется один бит.
- ПК **не включается**, Warcraft не показывается: это payoff существующего финала. Модули не показываются: их активация — W5/D5.
- Котов нет: в 33–38 Серёга один.
- В монтаж 12–20 с.
- **До READY выгрузить:**
  - @Video1 — выбранный конечный кадр Scene 38 (результата ещё нет: сцена в slow);
  - @Video2 — корабль и кабина Канцлера (ч.1 09:20–09:55);
  - @Video3 — внешний вид крейсера из фильма (ч.1 [Р1] 10:50–11:30 «корабль снаружи», ≈11:20–11:50 [Р2]).
- Запуск — только по команде владельца.

**Референсы:**

- @Image1 — <a href="references/full/serega.jpg">Серёга</a>;
- @Image2 — <a href="references/scenes/scene-27/S27-Image5-topview-source.png">руины планеты ситхов</a>;
- @Video1 — конечный кадр Scene 38 с ПК (выгрузить после результата 38);
- @Video2 — корабль и кабина Канцлера, ч.1 09:20–09:55 (выгрузить);
- @Video3 — крейсер Канцлера снаружи, ч.1 (выгрузить).

<div class="scene-ref-gallery">
<figure><a href="references/full/serega.jpg" target="_blank" rel="noopener"><img src="references/full/serega.jpg" alt="@Image1 — Серёга"></a><figcaption>@Image1 — Серёга</figcaption></figure>
<figure><a href="references/scenes/scene-27/S27-Image5-topview-source.png" target="_blank" rel="noopener"><img src="references/scenes/scene-27/S27-Image5-topview-source.png" alt="@Image2 — руины планеты ситхов"></a><figcaption>@Image2 — руины планеты ситхов</figcaption></figure></div>

**Что происходит:** На закате Серёга выходит из арки храма. Перед ним, поднятые Силой, плывут бежевый системный блок и массивный CRT-монитор; клавиатура у него под мышкой, провод болтается. Он заводит всё по рампе в кабину и пристёгивает монитор ремнём к пассажирскому креслу, рядом со стикером «хлеб и молоко». Корабль взлетает с пыльной площади, уходит от охристой планеты и летит к огромному крейсеру Канцлера, к освещённому проёму ангара.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal live-action space-fantasy, deadpan | Serega carries the ancient 1990s computer out of the Sith temple by the Force, straps it into his craft and flies it back to his flagship

REFERENCES / AUTHORITY ORDER:
@Video1 — the genuine final moment of the previous scene: the exact beige 1990s system unit, the heavy CRT monitor and the keyboard as found in the temple niche. It is the absolute authority for the shape, colour, wear and dust of these three objects.
@Image2 — the exact ancient ruin city outside the temple: ochre-red carved stone, colossal hooded statues, the wide temple stair, golden-orange sunset, drifting dust haze.
@Video2 — Serega's own craft and cockpit exactly as already shown earlier in the film; the only authority for the vehicle and the cockpit.
@Video3 — Serega's huge imperial flagship exactly as already shown earlier in the film: silhouette, colour, scale and hangar. Use the flagship only.
@Image1 — absolute identity of SEREGA.
Priority: @Video1 controls the computer objects; @Image2 controls the ruins; @Video2 controls the craft and cockpit; @Video3 controls the flagship; @Image1 controls Serega's face and costume.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image1 is the absolute visual authority for SEREGA (the Chancellor): pale older man, sparse light hair with a bald crown, mature serious face, long deep dark-purple robe, dusty from the temple. He is the only person in the entire scene. No cats, no Jedi, no Sith, no droids, no crew.

PROP LOCK — CRITICAL:
Exactly one beige 1990s desktop system unit, exactly one heavy CRT monitor and exactly one keyboard, identical to @Video1 in every shot: same scratches, dust and dangling cables. The computer stays switched OFF for the whole scene: dark screen, no lights, no game, no text. No map modules, holograms or glowing artifacts are shown.
COCKPIT NOTE: the same small square paper sticky note with a simple hand-drawn doodle of a loaf of bread and a milk bottle stays stuck on the console — pictures only, no letters, words or numbers.

VEHICLE / TRAVEL LOCK — CRITICAL:
One and the same craft from @Video2 in every shot: parked on the dusty stone plaza at the foot of the temple stair at the start, then one lift-off, one climb out of the atmosphere, one approach to the flagship from @Video3. No docking interior, no second small ship, no space battle, no hyperspace tunnel.

START STATE:
Sunset outside the temple from @Image2. Serega's craft stands parked on the dusty plaza at the foot of the stair, hatch open. Serega appears in the dark temple arch at the top of the stair.

TIMELINE:
[0:00–0:06] — OUT OF THE TEMPLE
Serega walks out of the temple arch and down the wide stair. In front of him, floating steadily at chest height by the Force, glide the beige system unit and the CRT monitor; the keyboard is tucked under his arm, its cable swinging. Two raised fingers guide them with calm, practised control.

[0:06–0:12] — LOADING THE CRAFT
At the craft he floats both objects up the ramp into the cockpit and lowers them onto the passenger seat. With dry, careful precision he pulls the seat strap across the CRT and clicks it shut, then sets the keyboard on top. The bread-and-milk note sits on the console beside him.

[0:12–0:18] — LIFT-OFF FROM THE RUINS
Exterior wide: the craft lifts off the plaza; dust swirls around the hooded statues and the broken pillars; it climbs into the orange sky.

[0:18–0:24] — LEAVING THE DUST WORLD
Cockpit: Serega at the controls, the strapped dark CRT on the seat beside him, the ochre-red planet curving away below through the window into black space.

[0:24–0:30] — TOWARD THE FLAGSHIP
After one clean time-compression cut: exterior from behind; the small craft approaches the huge flagship from @Video3 and heads for its brightly lit hangar opening. Hold this composition; the craft is still outside.

END STATE:
The small craft flying toward the lit hangar opening of the huge flagship; inside it, the switched-off computer strapped to the passenger seat. A clean cut point to the existing scene where Serega sits down at the old computer.

CAMERA / SPACE:
Steady medium-wide shot on the stair and plaza, then a controlled move into the cockpit, then exterior and cockpit angles of one continuous journey. Exactly one time-compression cut, into [0:24–0:30]. Smooth inertial camera, credible scale of the statues, the craft and the flagship, a stable left-to-right travel direction in space. No orbit, no shake, no zoom jumps.

PERFORMANCE:
Completely serious, like a museum curator moving a priceless relic. The comedy lies in the care he gives to an old beige computer and in the click of the seat strap. No smile, no look into the lens, no speech.

LIGHTING / MATERIALS:
Golden-orange low sunset through drifting fine dust and ash with rare ember-like sparks; warm weathered stone; the dull plastic of the yellowed system unit and the curved dark glass of the CRT catch the sunset. Cockpit instrument glow. Hard sunlight and deep black in space; the flagship's hangar is a bright rectangle of light.

AUDIO:
Wind across stone, footsteps on the gritty stair, a faint low Force hum while the objects float, the soft knock of plastic set down, the click of the seat strap, the hatch hiss, engine spin-up, dust roar at lift-off, wind fading to a deep hum in space. No dialogue, narrator, music, computer start-up sounds or game sounds.

NEGATIVE PROMPT:
computer switched on, glowing screen, game footage, Warcraft logo, text on screen, map modules, hologram, cats, Jedi, any other person, crew, droids, new ship design, second ship, space battle, hyperspace tunnel, docking interior, lava, volcanic glow, green vegetation, modern gaming PC, laptop, RGB lights, duplicated monitor or keyboard, objects morphing, readable text on the note, changed face or robe, cartoon CGI, subtitles, text, logo, watermark, black bars.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

---

## 4. Ревизия «Сцен в работе» (W5–W15)

Обозначения в столбце «Вердикт»: **ЗАКРЫТО** — функция выполнена существующими сценами; **ЧАСТИЧНО** — часть закрыта, остаток указан; **НЕАКТУАЛЬНО** — предлагается снять с очереди (снимает владелец); **НУЖНА ДЛЯ СВЯЗНОСТИ** — открыта и важна.

| ID | Вердикт | Новый «Статус» | Новый текст «Что уже понятно» |
|---|---|---|---|
| W9 | **ЗАКРЫТО** сценой 17 (в фильме) + 36 (DRAFT, вариант A от 14.10) | ЗАКРЫТО СЦЕНАМИ 17/36 · МОНТАЖНАЯ ПРОВЕРКА | Перемирие и передача набусского фрагмента — Scene 17 в фильме: «Как в старые добрые времена. Куда вы дели карту?», шёпот, Паша отдаёт модуль. Уход Серёги с модулем — Scene 36 (DRAFT). Заметка Саши 48:22 реализована в 17. **Монтажная задача без генерации:** модуль принял Саша (около 47:17–47:22, [Р2] §9), а в 17 отдаёт Паша. Проверить, читается ли переход от одного к другому; если нет — короткий взгляд или жест из уже снятого материала 17. Новую сцену не создавать. |
| W10 | **НЕАКТУАЛЬНО как отдельная сцена** — закрыто связкой 37 → существующий участок 51:52 | МОНТАЖ, БЕЗ ГЕНЕРАЦИИ | Лёша и Виталик на Набу не были; лесная пара — параллельная линия ([Р2] 65: «не выдавать её за отлёт троих из пещеры»). Связка: 36 → 37 (10–15 с, финал в космосе, лесная планета впереди) → существующий «корабль другой пары, лесная планета, посадка» (51:52–52:40). Идея Саши 50:31 (камера облетает героев, подлёт к лесу) уже выполнена этим участком. При необходимости — подпись места. |
| W6 | **ЧАСТИЧНО** — червь есть в Scene 16 (результат получен) | ЖДЁТ РЕШЕНИЯ ПО SCENE 16 И D6 | Червь, руины и противостояние — Scene 16, исход не разрешён, обмена картой нет. Открыто: (1) одна кнопка по 16 (сейчас «Принять» и «Переделать» конфликтуют); (2) судьба татуинского фрагмента (D6/M1); (3) какую часть погони 46–49 [Р2] заменяет 16; (4) машина: не показывать после разрушения. Отлёт Серёги с Татуина генерировать не нужно — его прибытие на Набу закроет Scene 39. Возможное решение D6 из заметок Саши — 32:51: «меч гасится → карта левитирует в руку Канцлера». |
| W5 | **НУЖНА ДЛЯ СВЯЗНОСТИ**; продвинута 35/38 (ПК), 37 и предложенной 40 | В РАЗРАБОТКЕ (D4/D5) | Путь фрагментов к цели виден через приём «модуль светится к цели» (37, решение 14.10; продолжение — 40): Набу → лес → планета ситхов → храм → древний ПК (35/38). Открыто: (1) как соединяются фрагменты и что открывают (D5; рекомендация [Р2] — «А + Д»: доступ, затем бытовой возврат); (2) тот ли это ПК, что в существующем финале, и где тот стоит (D4; по [Р1] §1 — «в космическом окружении», тогда нужна 41). «Диск / провод / мышь» по-прежнему идея. |
| W11 | **НУЖНА ДЛЯ СВЯЗНОСТИ** (прибытие Канцлера на Татуин) | В РАЗРАБОТКЕ · КОРОТКАЯ РЕПЛИКА / ЗВУК | Прибытие Канцлера на Татуин не показано, он появляется в кантине 33:50 [Р2]. Посадку не генерировать: отлёт уже есть (уход корабля в гиперпространство, 27:50–28:55 [Р2]), а причину появления даёт только «след». Варианты без новой сцены: реплика у карты 14:05–15:20 «Координаты прислал наш контакт на Татуине» ([Р2] §13) или сигнал/маяк в кантине ([Р1] N4). Бармен отдал модуль герою (31:51–31:52, [Р2] §3) — не противоречить этому. |
| W12 | **НЕАКТУАЛЬНО** (предлагаю снять) | НЕ НУЖНА (рекомендация [Р2]) | Добровольная передача уже есть на Набу (Scene 17). Силовой захват в лесу показан ясно (01:01:35–01:02:15 [Р2]). [Р2] §10: «Мне практичнее сохранить существующее притягивание, а важное человеческое решение дать Набу». Альтернатива [Р1] N8 «Вещь или человек» старше; [Р2] её не рекомендует. |
| W7 | **НУЖНА ДЛЯ СВЯЗНОСТИ** — разложена на конкретные сцены | В РАБОТЕ: 37 (DRAFT), 39/40/41 (предложены) + монтаж | Линия Серёги: Корусант → крейсер показан (09:20–09:55); крейсер → Татуин — монтаж + W11; Татуин → Набу — **Scene 39** (стык ~45:05); Набу → лес — **36 + 37** (решение 14.10, без посадки); лес → планета ситхов — **Scene 40** (стык после 01:02:45 → Scene 26); ПК → финальный CRT — **Scene 41** или монтаж (D4). Смена групп: T2 и Татуин → Набу — существующая посадка пары (39:25–40:30); идея Саши 37:30 уже есть в этом участке. Корабль везде один — из ч.1 09:20–09:55. |
| W13 | **ЧАСТИЧНО** — установка в кабине уже есть (37), финальный callback после W5 | В РАЗРАБОТКЕ ПОСЛЕ W5 | Просьба «хлеб и молоко» есть в начале ([FA] ч.1 01:40–02:30). Промежуточное напоминание — стикер на пульте в 37 (решение 14.10); тот же стикер как continuity в 40/41. Финальный удар («А молоко?» и взгляд на корзинку — [Р2] §12, вариант Д) — 6–10 с после W5. Отдельный эпизод не нужен. |
| W8 | **ЧАСТИЧНО** | В РАЗРАБОТКЕ / СВЕРИТЬ (Татуин) | Космическая погоня решена (Scene 5); сцены 3 и 4 не возвращать. Транспорт Канцлера между планетами зафиксирован: один корабль из ч.1 09:20–09:55 (37, 39, 40, 41). Открыто: татуинская машина и Scene 16 — машина не появляется после уничтожения; один узнаваемый дизайн машины Канцлера ([Р1] §16, [Р2] §8). |
| W14 | **ОБДУМАТЬ** (без изменений по сути) | ОБДУМАТЬ, НЕ НОВАЯ СЦЕНА | Пункты Саши разбирать по одному при монтаже. Уточнения: 53:16 («показ спуска на землю») — посадка лесной пары, уже есть (51:52–52:40 [Р2]); 37:30 — прилёт пары на Набу, уже есть (39:25–40:30); 30:01 и 49:26 — сверить с вставленными 17 и 23. |
| W15 | **НЕАКТУАЛЬНО** (предлагаю снять) | ЗАКРЫТО: 19 и 20 В ФИЛЬМЕ | Scene 19 (Маша, пощёчина, «важное поручение», бег) и Scene 20 (песня) отмечены «в фильме» (`review-ledger`, коммит `db010cf`). [Р2] §3: «Старый диагноз „внезапно побежали“ снимается». Остаток — монтаж: дневной свет Маши против закатного бега (44:30–45:05, [Р2] §16). |

**Устаревшее рядом с таблицей:**

- «Ближайшие направления», п. 5: «Scene 17 остаётся активной…» — неверно, 17 уже в фильме.
- П. 2 там же: «продолжение бывшей Scene 17 / W1» — по сути закрыт 17 и 36.
- «Сюжетные идеи-кандидаты»:
  - «Долг после монстра» → закрыто 17;
  - «Карта в обмен на друга» → см. W12;
  - «Хлеб и молоко» → W13, установка уже в 37.
- «Рабочая сюжетная очередь» после ревизии: **W5 → W11 → W6 → W7 (39/40/41) → W13**. W9, W10, W12, W15 снимаются. W8 ведётся параллельно, W14 — пул.

---

## 5. Однозначное и творческое

**Следует из источников (делается без вопросов):**

- маршрут и порядок пунктов 1–8 и 10;
- что показано, а что нет;
- без отдельной посадки на Кашиике (решение 14.10);
- без генерации прилёта на Татуин (монтаж + W11);
- один корабль Канцлера;
- ровно один модуль в 39 (ноль) и в 40 (один);
- 23–25 — линия котов;
- вердикты по W9, W10, W12, W15.

**Творческие выборы (за владельцем):**

- место кошачьей ветки (D1) и, следовательно, стык 40 → 26;
- приём «модуль светится к цели» для планеты ситхов;
- нужна ли 39;
- сценарий финала (D4/D5) и нужна ли 41;
- левитация ПК;
- судьба татуинского фрагмента (D6).

## 6. Вопросы владельцу

1. **Scene 40.** Ставим ветку планеты ситхов после Кашиика, перед котами (Scene 26), и показываем прибытие Серёги так же, как в 37: модуль светится к цели, затем посадка у руин? (Рекомендую — да.)
2. **Scene 39 (прибытие на Набу).** Делаем? Место — около 45:05, после прыжка пары в воду (рекомендую), или перед 47:35?
3. **Где стоит существующий финальный компьютер (01:02:45):** на борту у окна в космос (так по разбору 1) — и это тот же ПК, что найден в храме? Если да — нужна Scene 41 (увозит ПК, Сила несёт блок и монитор). Если нет — 41 не делаем.
4. **Татуинский фрагмент (D6):** остаётся у пары или Канцлер его забирает (идея Саши 32:51 «карта левитирует в руку Канцлера»)? От этого зависит, сколько модулей можно показывать дальше.
5. **Подтвердить без генерации:** прилёт на Татуин (вместо него реплика или «след» W11) и посадку на Кашиике (решение 14.10). Верно?
6. **Снять из очереди W9, W10, W12, W15** (закрыты 17/36, 37, рекомендацией [Р2] и сценами 19–20)?
7. **Корзинка с грибами** в кабине в 40/41 — подготовка финального «А молоко?» → взгляд на корзинку? По умолчанию её нет в текстах.

**Перед запуском любых из 39–41 выгрузить из монтажа:**

- корабль и кабину Канцлера (ч.1 09:20–09:55) — общий вход для 37, 39, 40, 41;
- стоянку у озера после прыжка (44:45–45:05) — для 39;
- лесную планету из космоса (51:52–52:40) — для 40;
- конечный кадр 38 и крейсер снаружи — для 41.

Модуль в лесном захвате (01:02:00–01:02:05) сверить с `S17-Image4`.
