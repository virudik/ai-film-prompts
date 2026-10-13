# Сцены 36–37: предложение правки на утверждение владельцу

Задача владельца в `owner_decisions` (id `08644768…`, `4e4f6814…` по сцене 36 и `f3f13a3f…` по сцене 37, статус `in_progress`): «надо продумать тщательней 36 и 37. согласовать с текущим сюжетом и действующими сценами фильма».

Проверено по `main` @ `93ca112`, 14.10.2026. Использованы: `NEW-CHAT-HANDOFF.md` (верхние блоки), `video-prompts.md` (сцены 33–38), текст Scene 17 из git (`0ca107d^`), `film-analysis.md`, `film-backlog.md`, `Seregius_montazhny_razbor-2.html` (монтажная карта v2 из 78 участков, 24.09), `reports/montage-plan-v3-draft.md`, `reports/prompt-audit-2026-10.md`, `reports/prompt-drafts-2026-10.md`, `character-references.json`, манифесты `references/scenes/scene-17|35|36|37|38`, `review-ledger.json`, `project-status.json`, `scripts/build_project_status.py` и Notion «Кино» (только чтение: «Набу», «Кашиик и вуки», «Перелёты между планетами», «Мостик крейсера», «Крыша корабля и мандалорцы», «Финал»).

Ничего в репозитории не менялось, Topview не трогался.

---

## 1. Несостыковки

### 1.1. Что подтверждается источниками (это не ошибки)

- **Место действия 36: пещера на Набу (Scene 17), а не храм.** Scene 17 — «Пещера: передышка после монстра и разговор о карте» (git `0ca107d^:video-prompts.md`). Карта переходит от Паши к Серёге. Храм и древний ПК (33→34→35→38) — отдельная цепочка на планете ситхов: `scene-meta` там `continues 33/34/35`, а 36–37 с ней не связаны.
- **Хронология: 36–37 идут раньше 33–38, а не после 38 и не параллельно.** В монтаже v2 после боя с монстром «около 51:47–51:51 трое стоят, примерно в 51:52 начинается лесной корабль» (`Seregius_montazhny_razbor-2.html`, «Передышка после монстра»). Scene 17 вставлена в этот стык (`review-ledger.json`: 17 `inserted_into_film=true`). Значит, 36–37 стоят на 51:52 перед лесным блоком (W7/T4), а храм и ПК — ближе к финалу (`montage-plan-v3-draft.md` §2.2 и вариант A в §2.3).
- **Карта не происходит от ПК.** В 35/38 карты прямо запрещены: в 38 «premature maps/artifacts» стоит в NEGATIVE, в 33 — «no map». В 36 Серёга несёт набусский фрагмент. Путь фрагмента: «Правитель → Саша, около 47:17–47:22, Саша убирает под одежду» (razbor-2 §11) → Scene 17, где его отдаёт Паша.
- **Куда он летит, тоже согласовано.** Порядок миров в фильме: «Татуин → Набу → Кашиик» (`film-analysis.md`, «Текущий порядок крупных сцен»). На Кашиике Канцлер появляется сам: «57:45–58:15 Канцлер с грибами» и «58:15 История спидера, адвоката» (razbor-2, участки 73–74). Старый Notion «Мостик крейсера»: «Сам берёт все три планеты последовательно».
- **Паша и Саша остаются на Набу.** В фильме их линия на Набу и заканчивается. Это совпадает с 36.

### 1.2. Реальные несостыковки DRAFT 36–37

| # | Что не так | Источник |
|---|---|---|
| 1 | **Реквизит «карта» описан как бумажная складная карта, а в фильме это жёсткий светящийся модуль.** Промт 36: «folds it only along its existing crease», «including folded edges». На референсе `S17-Image4-topview-source.png` — небольшая прямоугольная пластина в серой рамке с двумя янтарными светящимися панелями. В разборе: «светящийся прямоугольник», «правитель отдаёт модуль Саше». Сложить её нельзя, и модель начнёт перерисовывать предмет. | `video-prompts.md` §Сцена 36 (STORY/START, @Image3); `references/scenes/scene-17/S17-Image4-topview-source.png`; razbor-2 §11, «Карта Татуина» |
| 2 | **Транспорта Серёги на Набу в фильме нет.** Сцена 36 требует «@Video2 = существующий кадр доступного на Набу транспорта Серёги, подобрать из монтажа». По монтажной карте v2 Канцлер на Набу просто появляется в подводном городе («61 · 47:35–48:50 Канцлер, дуэль, трещина и затопление»). Прибытие и его корабль не показаны: на 39:25–41:10 видна только машина Паши и Саши. Подобрать @Video2 не из чего, поэтому промт в нынешнем виде запустить нельзя. Сцена 37 строится на том же несуществующем корабле. | razbor-2, участки 50, 51, 61; `references/scenes/scene-36/manifest.json` → `remaining` |
| 3 | **Выход из пещеры «на знакомую местность Набу к транспорту» придуман.** В пещеру попадают по воде («63 · Бой на существе/рыбе, затем пещера»). На кадрах Scene 17 (`S17-post-battle-seated.png`, `S17-map-handoff.png`) за героями водяная завеса или водопад, яркий туман и плавник морского существа в воде. Сухой тропы к стоянке нет. Промт 17 даже запрещал «dry cave, bright daylight». | razbor-2, участок 63; текст Scene 17 (NEGATIVE); helpers `S17-*` |
| 4 | **Референс локации в 36 показывает живого монстра в разгар боя.** @Image2 = `S17-cave-Video1-frame-003s.png`: монстр стоит, Паша и Саша с мечами. Это противоречит собственному правилу 36 «the defeated monster remains inert» и провоцирует «resurrected monster». Для пещеры после боя подходит `S17-post-battle-seated.png`. | `video-prompts.md` §Сцена 36, «Референсы»; сам файл кадра |
| 5 | **Конец 37 смешивает полёт Серёги с прилётом лесной пары.** Промт 37 стыкует финал с «@Video3 — FIRST FOREST SHOT of the Kashyyyk / forest group». В фильме этот кадр — «65 · 51:52–52:40 Корабль другой пары, лесная планета, посадка». Разбор прямо требует: «Обозначить параллельную линию, не выдавать её за отлёт троих из пещеры» и «Это не транспорт, на котором трое победителей только что улетели с Набу». При стыке «в точный кадр» зритель решит, что это корабль Серёги или что он прилетел вместе с Виталиком и Лёшей. Свой первый кадр на Кашиике у Серёги — грибы (57:45), а не прилёт пары. | razbor-2, участок 65 и раздел «51:52–54:25. Ясно сменить людей и планету»; `video-prompts.md` §Сцена 37 (@Video3, END STATE) |
| 6 | **Виталик и Лёша в 37 лишние.** Их референсы (@Image2, @Image3) стоят по условию «если видны». Кабина с ними в открывающем кадре леса видна всегда (razbor-2: «короткая кабина с Виталиком и Лёхой»), поэтому условие на деле подтянет их в сцену Серёги. Реестр уже числит 37 за ними (`character-references.json`: `vitalik.scenes`, `lesha.scenes` = [13, 28, 37]). Каноническое имя — **Лёша** (алиас «Лёха»), в 37 написано «Лёха». | `character-references.json`; `video-prompts.md` §Сцена 37 |
| 7 | **Паша и Саша в 36 без identity-референсов.** Первые ~12 с они в кадре, но их лица описаны только через «@Video1 последний кадр 17», а этого входа в репозитории нет. В реестре их сцены — [20, 28], без 36. | `NEW-CHAT-HANDOFF.md` «Промты»; `character-references.json`; `reports/prompt-audit-2026-10.md` (Scene 36, оценка D) |
| 8 | **37 перегружена и противоречит духу W7/W8.** В 30 с уложено шесть событий: посадка, люк, взлёт, атмосфера, космос, подход к планете. В TIMELINE разрешена одна склейка-сжатие времени, а в CAMERA — «two motivated transitions». В источниках: «Генерировать только недостающую функцию, не пакет одинаковых перелётов» (W7); «Не требуется отдельный взлёт, перелёт и посадка: такую процедуру фильм уже многократно показал» (razbor-2, «Вмешательство вуки…»); «Несколько гиперпереходов подряд мало добавляют» (razbor-2 §7). Старый Notion «Перелёты между планетами»: корабль в космосе ~5 с. | `film-backlog.md` W7; razbor-2; Notion; `reports/prompt-audit-2026-10.md` |
| 9 | **Причина полёта (W5) нигде не названа.** Ни 36, ни 37 не показывают, зачем Серёга летит именно на лесную планету и как это связано с Warcraft. Шёпот Паше в Scene 17 намеренно неслышен. W5 требует «завязка, промежуточное напоминание, финал». 36–37 — естественное место для напоминания, но содержание напоминания — творческий выбор. | `film-backlog.md` W5; `film-analysis.md` «Warcraft и ближайшие решения»; Scene 17 (шёпот) |
| 10 | **Счёт фрагментов.** Сейчас никакая сцена не мешает модели показать у Серёги два или три модуля. Татуинский фрагмент к нему не перешёл: M1/D6 открыты, в Scene 16 «do not add a map exchange». В 36–37 должен быть ровно один модуль — набусский. | `film-backlog.md` M1, M4; `montage-plan-v3-draft.md` §3, дыра 1 |
| 11 | **Мелочи в `scene-meta`.** В 36 тег `nabu` (опечатка, правильно `naboo`). В 36 `dependencies: []` при тексте «продолжение 17». Это **правильно**: валидатор принимает зависимость только на активную сцену (`build_project_status.py`, `normalize_dependencies`: `target not in active_scene_ids` → health ≠ ok), а 17 зарезервирована. Связь с 17 описывается только в «Контексте». | `video-prompts.md`; `scripts/build_project_status.py` |

---

## 2. Варианты и рекомендация

Общее для всех вариантов (вытекает из источников, творческого выбора не требует):

- 36 начинается с конца Scene 17 в пещере Набу. Модуль-фрагмент один, это реквизит `S17-Image4`. Паша и Саша остаются.
- `S17-cave-Video1-frame-003s.png` заменить на `S17-post-battle-seated.png`. Добавить листы `pasha.jpg` и `sasha.jpg`.
- Из 37 убрать Виталика и Лёшу, а также стык «в первый кадр лесной группы».
- В 36–37 только один модуль. Без ПК, храма, котов, Warcraft-экрана.
- 36 — без диалога, Wan 3.0, 30 с. 36 `dependencies: []`, 37 `continues 36`.

### Вариант A — «Уход и отлёт, без посадки» (рекомендую)

- **36:** Серёга прячет модуль под робу, встаёт, коротко кивает, уходит в глубь пещеры к светлой водяной завесе. Камера остаётся у сидящих Паши и Саши. Финал — его силуэт на фоне светлой завесы, Паша и Саша на переднем плане. Ни транспорта, ни внешней местности. Всё пространство уже есть в кадрах 17.
- **37:** кабина собственного корабля Канцлера — того, что уже есть в фильме (ч. 1, 09:20–09:55 «Люк, кабина, прибытие»). Подъём с Набу через облака, выход в космос, короткий разгон. Финал: корабль вдали от зелёной лесной планеты, вид которой взят из уже существующего установочного плана 51:52–52:40 (только планета, без корабля пары). Без входа в атмосферу и посадки, без лесной пары.
- **Монтаж:** 17 → 36 (20–30 с) → 37 (взять ~10–15 с) → существующий «корабль другой пары» 51:52. Зритель знает, что Канцлер летит туда же; payoff — его внезапное появление с грибами (57:45).
- **@Image/@Video:** см. §4. Из обязательных внешних входов остаются два кадра из монтажа для 37 и конец Scene 17 для 36. Для 36 есть запасной вариант из репозитория (`S17-post-battle-seated.png`).
- **Почему A:**
  - закрывает обе функции, которые просил владелец («уходит с картой» и «улетает к лесной планете»);
  - не требует несуществующего транспорта на Набу;
  - не выдаёт корабль пары за корабль Серёги;
  - не плодит лишнюю посадку;
  - сохраняет сюрприз «Канцлер с корзинкой».

### Вариант B — «Отлёт и отдельное прибытие перед грибами»

- **36** — как в A.
- **37** — только отлёт и уход в космос, финал без планеты.
- **Новая сцена (новый Scene ID, только по решению владельца)** — посадка корабля Серёги в лесу. Её финал стыкуется с **первым кадром грибного эпизода** (57:45), а не с прилётом пары.
- **Плюс:** географически самый ясный.
- **Минус:** ещё одна генерация, и прямо против рекомендации разбора не показывать «взлёт, перелёт и посадку». Сюрприз с грибами теряется.

### Вариант C — «Только 36»

- 36 как в A, 37 — кнопка «Не нужна». Появление Канцлера на Кашиике остаётся неожиданностью.
- Минимум генераций, полностью в духе W7.
- Минус: противоречит прямой просьбе владельца о сцене перелёта (контекст 37 в master).

---

## 3. Вопросы владельцу (решает только он)

1. **Вариант:** A (рекомендую), B или C?
2. **На чём летает Серёга:** тот же корабль, на котором он ушёл с крыши в начале фильма (ч. 1, 09:20–09:55; рекомендую), или другой транспорт из фильма — какой?
3. **Откуда взлёт в 37:** зелёный луговой берег озера Набу, как в Scene 19 (`S19-Image1`; в готовом тексте так), или не показывать землю и начать сразу в облаках?
4. **Напоминание W5 в кабине 37** (Warcraft / турнир / «хлеб и молоко»): нужно ли и какое конкретно? По умолчанию в тексте ничего такого нет — нельзя выдумывать реквизит, которого нет в фильме.
5. **«Указывает» ли модуль на лесную планету** (например, усиливает свечение, когда планета в кадре)? По умолчанию нет: причина полёта остаётся тайной шёпота из Scene 17.

**После решения (детерминированно, делает агент):**

- правка master тем же Scene ID (тексты ниже);
- обновить манифесты `scene-36`/`scene-37`;
- в `character-references.json`: Паша и Саша +36, Виталик и Лёша −37;
- валидатор и Pages.

**Перед запуском нужны кадры из монтажа:**

- конец Scene 17;
- кадр корабля и кабины из ч. 1 (09:20–09:55);
- установочный план лесной планеты (51:52–52:40).

Запуск Topview — только по отдельной команде владельца.

---

## 4. Готовые тексты для варианта A

### Сцена 36 — После пещеры: Серёга уходит с фрагментом карты

`scene-meta`: `{"target_engine":"Wan 3","production_state":"DRAFT","duration_s":30,"dialogue":{"enabled":false,"language":null},"dependencies":[],"tags":["serega","naboo","cave","map","depart","continuity"]}`

**Контекст использования:** Прямое продолжение Scene 17, которая уже в фильме (её Scene ID зарезервирован, поэтому в `dependencies` связь не пишется). Место в монтаже — стык около 51:52 после боя с монстром, перед блоком лесной пары (W1/W7/T4). Сцена закрывает «расхождение» после вынужденного союза: Серёга молча уходит с единственным набусским фрагментом, Паша и Саша остаются на Набу. Реквизит «карта» — жёсткий светящийся модуль с `S17-Image4`, не бумага. Ни транспорта, ни внешней местности: в фильме нет кадров корабля Канцлера на Набу, а выход из пещеры — водяная завеса. Перелёт — Scene 37. До READY: выгрузить из монтажа фактический конец Scene 17 (@Video1) и сверить сторону кадра и руку с модулем; без него сцена остаётся DRAFT. Технический результат не равен одобрению. Запуск — только по команде владельца.

**Референсы:**

- @Image1 — Серёга (`references/full/serega.jpg`);
- @Image2 — Паша (`references/full/pasha.jpg`);
- @Image3 — Саша (`references/full/sasha.jpg`);
- @Image4 — фрагмент карты, светящийся модуль (`references/scenes/scene-17/S17-Image4-topview-source.png`);
- @Image5 — пещера после боя, рассадка троих (`references/scenes/scene-17/S17-post-battle-seated.png`);
- @Video1 — фактический конец Scene 17 из монтажа (выгрузить перед запуском).

**Что происходит:** Серёга прячет полученный модуль под робу, молча кивает Паше и Саше и уходит по мокрым камням в глубь пещеры, к светлой водяной завесе. Паша и Саша остаются сидеть на останках монстра и провожают его взглядом.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal live-action cinema | Deadpan quiet departure: Serega leaves the post-battle cavern with the single map module

REFERENCES / AUTHORITY ORDER:
@Video1 — the genuine final seconds of the finished previous scene in this same cavern. Its last frame is the absolute start authority: positions of the three seated men, which hand holds the map module, camera side, water level, light and the inert monster remains.
@Image5 — the same post-battle cavern and seating arrangement: Pasha seated screen-left, Serega centre, Sasha screen-right, each on a separate severed pale section of the dead monster; wet black rocks and shallow water in front; the huge inert monster carcass lying behind on the right; a bright misty curtain of falling water at the back of the cave. It controls location geometry and composition if @Video1 is ambiguous.
@Image4 — the exact map module prop.
@Image1, @Image2, @Image3 — identity sheets for Serega, Pasha and Sasha.
Priority: @Video1 controls the first frame and positions; @Image5 controls cave geometry; @Image4 controls the prop; @Image1–@Image3 control faces and costumes only. No reference may add a fourth person or revive the monster.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image1 is the absolute visual authority for SEREGA (the Chancellor): pale older man, sparse light hair with a bald crown, mature serious face, long deep dark-purple robe with hood lowered, soaked and darkened by water.
@Image2 is the absolute visual authority for PASHA: clean-shaven man, dark navy-blue Jedi tunic, brown belt, dark trousers, high boots, leather bracer, soaked and battle-worn.
@Image3 is the absolute visual authority for SASHA: bearded man with round glasses, cream inner tunic, dark burgundy-brown robe, brown boots, soaked and battle-worn.
Three clearly different men; no face blending, no costume swaps, no added armour or jewellery.

PROP LOCK — CRITICAL:
The map is ONE small rigid palm-sized rectangular module from @Image4: rounded grey metal frame, dark-grey face, two vertical warm-amber glowing segmented panels in the upper middle, a black central stripe with a tiny lock-like mark, small dark markings at the corners. It never folds, bends, unrolls, duplicates, becomes paper, a disk or a hologram. Exactly one module exists in this scene.

CAVE / CONTINUITY LOCK:
The monster is dead and stays completely inert; its cut surfaces are dark and cauterized, no fresh blood. Pasha and Sasha stay seated on their own sections for the whole take and do not follow. No exterior landscape, vehicle or sky is revealed: the cave exit is only the bright misty water curtain at the back.

START STATE:
Exact last frame of @Video1: all three seated and exhausted, Serega in the centre holding the single module in his hand, Pasha on the left, Sasha on the right, wet clothes, shallow water, mist.

TIMELINE:
[0:00–0:06] — THE MODULE SECURED
Hold the established three-shot. Serega looks down at the module; its amber panels glow softly on his wet fingers. He slides it calmly into an inner fold of his robe at the chest; the glow disappears under the cloth. Pasha and Sasha watch silently.

[0:06–0:12] — SEREGA RISES
Serega plants his boots on the wet stone and stands up from his monster section with tired, careful weight. He gives Pasha a small serious nod, then Sasha the same. Pasha answers with a minimal nod; Sasha glances at Pasha with a restrained "what was that about?" look. No words.

[0:12–0:20] — WALKING AWAY
Serega turns his back to the camera and walks upstage between the two seated men, along the wet rocky edge of the shallow water, past the dead carcass. The camera stays low behind Pasha and Sasha and slowly pushes in between them, keeping both seated in the foreground.

[0:20–0:26] — TOWARD THE LIGHT
Serega reaches the back of the cave; the bright curtain of falling water fills the background with cool misty light. His dark-purple silhouette becomes smaller and backlit; spray drifts around him.

[0:26–0:30] — THE PARTING IMAGE
Serega stops for one beat at the edge of the water curtain, a dark silhouette in the glow, then steps forward into the bright mist. In the foreground Pasha and Sasha remain seated on the monster sections, looking after him.

END STATE:
Serega is a backlit silhouette entering the bright water curtain at the back of the cave, the single module hidden in his robe; Pasha and Sasha remain seated in the foreground on separate monster sections; the monster stays dead. Clean cut point to a departure scene.

CAMERA / SPACE:
One continuous take, 35 mm natural perspective, slow low push-in from behind the two seated men; no cuts, no orbit, no camera shake. Stable screen positions: Pasha left, Sasha right, the water curtain at the back. Real cave scale; the walk is a few dozen metres, no new tunnels or staircases.

PERFORMANCE:
Adult, restrained, physically tired after a hard fight. Serega is calm and purposeful, almost formal; Pasha is resigned; Sasha is quietly puzzled. Play it completely straight: nobody comments on sitting on monster pieces, nobody laughs or looks into the camera.

LIGHTING / MATERIALS:
Cool humid bounce light, glistening wet rock and soaked fabric, pale cauterized monster skin, drifting spray and mist. The water curtain is the brightest area of the frame and gradually rims Serega's silhouette. The module's amber glow is small and warm and is visible only before he hides it.

AUDIO:
Steady roar of falling water growing louder as Serega approaches it, dripping, wet footsteps on stone, soft heavy robe rustle, tired breathing. No dialogue, whisper, narrator or music.

NEGATIVE PROMPT:
folded paper map, scroll, second module, glowing hologram, map floating, Pasha or Sasha standing up or following, extra people, cats, resurrected or moving monster, fresh blood, gore, new combat, lightsabers ignited, spaceship, vehicle, exterior landscape, sunny sky, staircase, teleport, jump cut, changed faces, missing glasses on Sasha, dry clothes, comedy mugging, subtitles, text, logo, watermark, black bars.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

---

### Сцена 37 — Отлёт Серёги с Набу к лесной планете

`scene-meta`: `{"target_engine":"Wan 3","production_state":"DRAFT","duration_s":30,"dialogue":{"enabled":false,"language":null},"dependencies":[{"type":"continues","scene":36}],"tags":["serega","travel","naboo","forest_planet","map","continuity"]}`

**Контекст использования:** Следует за Scene 36 через монтажную склейку (не непрерывный дубль). Функция — показать, что Канцлер с одним набусским фрагментом летит на лесную планету. Это стык W7/T4 перед существующим блоком «корабль другой пары, лесная планета, посадка» (около 51:52). Сцена **не** стыкуется с кадрами лесной пары и не показывает посадку: на Кашиике Серёга впервые появляется в уже готовом эпизоде с грибами (57:45). Корабль — собственный транспорт Канцлера, уже показанный в начале фильма (ч. 1, 09:20–09:55 «Люк, кабина, прибытие»), а не корабль Виталика и Лёши. Вид лесной планеты берётся из существующего установочного плана 51:52–52:40, только сама планета. Причина полёта (W5) не раскрывается до решения владельца. В монтаж достаточно ~10–15 с. До READY: выгрузить из монтажа @Video1 и @Video2. Запуск — только по команде владельца.

**Референсы:**

- @Image1 — Серёга (`references/full/serega.jpg`);
- @Image2 — фрагмент карты, светящийся модуль (`references/scenes/scene-17/S17-Image4-topview-source.png`);
- @Image3 — пейзаж Набу: озеро, луга, деревья (`references/scenes/scene-19/S19-Image1-topview-source.png`; только палитра и тип местности, люди с кадра не переносятся);
- @Video1 — корабль и кабина Канцлера из ч. 1 фильма, 09:20–09:55 (выгрузить перед запуском);
- @Video2 — установочный план лесной планеты из космоса, 51:52–52:40 (выгрузить перед запуском; только планета, корабль пары не использовать).

**Что происходит:** Серёга один в кабине своего корабля коротко проверяет спрятанный модуль и берётся за управление. Корабль поднимается над зелёными озёрами Набу, проходит облака, выходит в космос и уходит к далёкой лесной планете. Сцена заканчивается в космосе, до входа в атмосферу.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal live-action space-opera cinema | Serega alone departs Naboo in his own craft and heads for a distant forest planet

REFERENCES / AUTHORITY ORDER:
@Video1 — Serega's own craft and cockpit exactly as already shown earlier in the film: hull shape, colour, proportions, engines, cockpit layout, seats, windows and controls. It is the only authority for the vehicle; do not design a new ship.
@Image1 — absolute identity of SEREGA.
@Image2 — the exact map module prop.
@Image3 — Naboo landscape palette only: calm blue lakes, bright green meadows, rounded trees, soft clear daylight. People and buildings in this image are not part of the shot.
@Video2 — the destination planet's appearance from space exactly as already established in the film: colour, cloud cover, dense green forested continents. Use the planet only; any other ship in that footage must not appear.
Priority: @Video1 controls the vehicle and cockpit; @Image1 controls Serega's face and costume; @Image2 controls the prop; @Image3 controls the Naboo look; @Video2 controls the destination planet.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image1 is the absolute visual authority for SEREGA (the Chancellor): pale older man, sparse light hair with a bald crown, mature serious face, long deep dark-purple robe, still damp and darker at the hem after the cave. He is the only person in the film frame. No pilot droid, co-pilot, cats or other Jedi.

PROP LOCK — CRITICAL:
Exactly ONE small rigid palm-sized rectangular map module from @Image2: rounded grey metal frame, dark-grey face, two vertical warm-amber glowing segmented panels. It comes out of the inner fold of his robe and goes back there. It never folds, multiplies, projects a hologram or becomes a screen.

VEHICLE / TRAVEL LOCK — CRITICAL:
One and the same craft from @Video1 in every exterior shot: same silhouette, colour, engine glow and scale. Realistic, restrained travel: one take-off, one climb, one short burst of acceleration in space. No landing, no atmospheric entry at the destination, no forest ground, no other ships, no space battle.

START STATE:
Serega is already seated alone at the controls inside the cockpit from @Video1, map module hidden in his robe, the craft resting on a green Naboo lakeshore meadow visible through the window.

TIMELINE:
[0:00–0:06] — COCKPIT CHECK
Medium shot inside the cockpit. Serega takes the module from his robe and looks at its soft amber glow for one quiet beat, then slides it back into the same fold. He places both hands on the controls; the instrument lights come on.

[0:06–0:12] — LIFT-OFF FROM NABOO
Exterior wide: the same craft rises steadily from the green lakeshore meadow; grass flattens and the lake surface ripples under the engine wash; trees and calm water stretch to the horizon in soft daylight.

[0:12–0:18] — THROUGH THE CLOUDS
Following shot from behind and slightly below: the craft climbs through a white cloud layer; Naboo's lakes and green land shrink below and the sky darkens toward space.

[0:18–0:24] — LEAVING NABOO
Space: the blue-green curve of Naboo fills the lower frame. The craft banks onto a new heading, engines flare once, and it accelerates smoothly away from the planet.

[0:24–0:30] — THE FOREST PLANET AHEAD
After one clean time-compression cut: deep space, the same small craft seen from behind, heading toward a distant planet with dense green forested continents and white cloud bands that match @Video2. Hold this composition; the craft is still far from the planet.

END STATE:
The craft travels through open space toward the distant forest planet; no arrival, no other ship, no characters visible. A clean cut point to the existing footage of the other Jedi pair, which follows separately.

CAMERA / SPACE:
Exactly one time-compression cut (between [0:18–0:24] and [0:24–0:30]); every other transition is a motivated continuous camera move. Smooth inertial camera, credible ship scale against clouds and planets, stable direction of travel left-to-right throughout, no warp tunnel, no shake, no zoom jumps.

PERFORMANCE:
Serega is calm, focused and alone; small precise movements, no gestures to the camera, no smile, no speech.

LIGHTING / MATERIALS:
Cockpit: soft instrument glow and daylight through the window on his face and damp robe. Exterior: natural Naboo daylight, real volumetric clouds, then the hard sunlight and black of space, believable planet atmosphere glow. Restrained colour grade matching the neighbouring scenes.

AUDIO:
Cockpit switches and soft servo clicks, engine spin-up, low rumble of the climb, wind roar through the clouds fading to a quiet deep hum in space. No dialogue, narrator, music or radio voices.

NEGATIVE PROMPT:
new or different ship design, second ship, the other Jedi pair, Vitalik, Lesha, Pasha, Sasha, pilot droid, cats, extra passengers, landing, forest floor, entering the forest planet's atmosphere, Sith ruins, temple, ancient computer, Warcraft screen, hologram map, two or three modules, folded paper map, space battle, explosions, hyperspace tunnel, flipping travel direction, changed face or robe, cartoon CGI, subtitles, text, logo, watermark, black bars.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Примечания к текстам

- В 36 шесть входов (5 изображений и 1 видео), в 37 — пять (3 и 2). В прежней 37 их было шесть. Лимит Wan 3.0 по числу входов в репозитории не зафиксирован — проверить на сайте Topview при запуске.
- Если владелец по вопросу 3 выберет «без земли», в 37 убрать @Image3, START STATE начинать «in the cockpit already climbing through clouds», а бит LIFT-OFF объединить с CLOUDS.
- Если по вопросу 4 будет выбрано напоминание W5, оно встаёт в бит COCKPIT CHECK вместо паузы с модулем, после утверждения конкретного реквизита.
- Заголовки сцен в master меняются только по тексту. Якоря `#scene-36`/`#scene-37` и Scene ID остаются прежними.
