# Актуальные видео-сцены и промты


Рабочий мастер-файл. Здесь хранятся только актуальные промты, которые ещё нужны для генерации или доработки. Когда ролик готов и промт больше не нужен, соответствующая сцена удаляется из файла и из оглавления.


**Канонический источник:** `video-prompts.md`. Это единственный редактируемый мастер; `video-prompts.html` генерируется из него автоматически и вручную не редактируется.


## 📌 РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС


**21.09.2026 · 12 сцен к генерации/доработке · 24 полных текста промтов**


- **🛠️ 3** сцены в раннем блоке **«Сцены в работе»**: W5, W7, W8.
- **⏳ 6** сцен сейчас в медленной генерации: **2, 3, 4, 5, 13, 19** — повторно не запускать до результата/ошибки или отдельного решения пользователя.
- **Последние оформленные активные сцены:** 19–20.
- **Последняя полная синхронизация:** **17.09.2026 · 20:42 (+03:00)**.


**Статусы V3.5 для обсуждения правок:** `NEEDS_FIX` означает, что сцену/промт нужно отдельно обсудить и решить, требуется ли изменение; это не разрешение автоматически переписывать промт или запускать новый рендер. `NEEDS_RERENDER` означает, что предыдущий результат уже признан кандидатом на повторную генерацию, но для slow-сцен повторный запуск всё равно запрещён до результата/ошибки или отдельного решения пользователя.


**Синхронизация контекста:** **21.09.2026**. Точное техническое время зеркала хранится в `project-status.json` и здесь не дублируется. Фактическая карта — `film-analysis.md`, статусы и зависимости — `film-backlog.md`. Новые решения пользователя имеют приоритет над старым Notion. В active master остаются 12 актуальных сцен и 24 полных текста. Сцены 6, 7, 9, 12, 14, 15 и 18 удалены из active master по прямому решению пользователя как уже отработанные/больше не актуальные; их Scene ID остаются зарезервированы и не переиспользуются. Canonical slow-list сейчас: **2, 3, 4, 5, 13, 19**. Сцены 3, 4, 5 и 13 были повторно запущены в Topview и привязаны к существующим Scene ID, поэтому новые Scene ID для этих задач не создаются. Сцена 20 «Маша-Лагуна: рок-припев у озера» остаётся READY и не slow; внутри неё теперь 11 отдельных 30-секундных частей «Песня Маши 1–11». Никакие старые промты Notion сюда автоматически не добавлены. Непрерывный аудиовизуальный контроль не выполнялся.


## ⏳ Сейчас в медленной генерации


| Сцена | Статус | Действие |
|---|---|---|
| 2 — Джедаи на крыше: триумфальный марш без мечей | ⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ | Не запускать повторно |
| 3 — Космическая погоня: экстерьер | ⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ | Не запускать повторно |
| 4 — Космическая погоня: интерьер кабины | ⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ | Не запускать повторно |
| 5 — Космическая погоня: единый дубль через стекло | ⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ | Не запускать повторно |
| 13 — Совет джедаев: говорящий кот | ⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ | Не запускать повторно |
| 19 — Рыбалка и Маша-Лагуна | ⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ | Не запускать повторно |


Статус снимается только после результата/ошибки или отдельного решения пользователя о новом запуске.


| # | Сцена | Референсы | Что происходит |
|---|-------|-----------|-----------------|
| 1 | [Джедаи на крыше — проход с зажжёнными мечами](#scene-1) | @image1 = окружение/строй/позы с мечами; @image2, @image3, @image5, @image6, @image4, @image7 = персонажи | Шесть джедаев синхронно идут на камеру по мокрой крыше Корусанта с уже зажжёнными мечами. Два актуальных варианта: кинематографичный и максимально стабильный. |
| 2 | [Джедаи на крыше — триумфальный марш без мечей](#scene-2)<br>**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ** | @image1 = окружение/строй; @image2, @image3, @image5, @image6, @image4, @image7 = персонажи | Та же шестёрка идёт на камеру без оружия под эпическую оркестровую музыку. Два актуальных варианта: кинематографичный и максимально стабильный. |
| 3 | [Космическая погоня — экстерьер](#scene-3)<br>**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ** | @image1 = стартовый космический кадр; @image2 = дизайн корабля | Транспорт уже находится в разгаре боя, уклоняется от истребителей; камера сближается с кабиной и заканчивает сцену вспышкой у стекла. |
| 4 | [Космическая погоня — интерьер кабины](#scene-4)<br>**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ** | @image3 = первый кадр/экипаж; @image4 = точный последний кадр/пилот | Прямое продолжение боя внутри кабины: камера постепенно приближается к пилоту и приходит к точной композиции @image4. |
| 5 | [Космическая погоня — единый дубль через стекло](#scene-5)<br>**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ** | @image1 = первый кадр; @image2 = корабль; @image3 = интерьер; @image4 = последний кадр | Альтернатива сценам 3–4: внешний космический бой → непрерывный пролёт камеры через стекло → интерьер кабины → точный финальный кадр. |
| 10 | [Кантина — допрос про товар, часть 1](#scene-10) | @Image1 = композиция/Чубакка; @Image2 = Han; @Image3 = Jedi | Джедай спрашивает Хана про товар, Хан делает вид, что не понимает, и ссылается на Чубакку. |
| 11 | [Кантина — допрос про товар, часть 2](#scene-11) | те же @Image1/@Image2/@Image3 | Прямое продолжение: шутка про Чубакку, вопрос про плёнку и финальная растерянность Хана. |
| 13 | [Совет джедаев — говорящий кот](#scene-13)<br>**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ** | @image1 = композиция/локация; @image2 = кот; @image4 = Black; @image5 = Purple | После решения Совета кот на коленях у Purple спокойно человеческим голосом подтверждает решение. Black с кальяном и Purple воспринимают это как совершенно нормальное событие. |
| 16 | [Татуин — гигантский пустынный червь и бой на руинах](#scene-16) | @video1 = локация/герои Татуина | Огромный червь в духе Dune вырывается из песка в локации @video1 и разносит всё вокруг, пока герои сражаются на его фоне и уворачиваются от атак. |
| 17 | [Пещера — передышка после монстра и разговор о карте](#scene-17) | @video1/@video2/@video3 = продолжение пещеры/монстр | Прямое продолжение после боя: трое измотаны, сидят на отрубленных частях чудовища и начинают разговор о карте. |
| 19 | [Рыбалка и Маша-Лагуна](#scene-19)<br>**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ** | @Image1 = стартовый кадр/рыбалка; @Image2 = финальный кадр/бег; @Image3 = Маша-Лагуна; @Image4 = Sasha; @Image5 = Pasha | Саша и Паша спокойно рыбачат у озера, из воды появляется Маша-Лагуна, Саша успевает сказать «Маша?..», получает пощёчину и слышит упрёк. Паша молча реагирует мимикой, Саша вспоминает про важное поручение, после чего оба срываются в бег к финальному кадру. |
| 20 | [Маша-Лагуна — рок-припев у озера](#scene-20) | @Image1 = локация/берег озера; @Image2 = Маша-Лагуна | Маша-Лагуна одна стоит у воды и исполняет оригинальный эмоциональный англоязычный рок-припев. Один стабильный непрерывный план плавно приближается от общего/среднего к более интимному кадру; точная локация и identity Маши сохраняются. |


---


## Сцены в работе


Это не финальные промты, а рабочий блок: сцены уже взяты в разработку, контекст и базовые референсы понятны, но формулировки ещё будут уточняться по ходу работы.


| ID | Сцена в работе | Базовые референсы | Что уже понятно |
|---|---|---|---|
| W5 | Канцлер и Warcraft 3 | референс Канцлера | Сквозная мотивация: Канцлер хочет сесть играть/успеть на турнир по Warcraft 3, а джедаи всё время его отвлекают и мешают. Рекомендуемая драматургическая привязка: ранняя мотивация этой линии и её завершение у компьютера; это ориентир для разработки, а не утверждённая точка резки. |
| W7 | Переходы между группами | конечные и начальные кадры соседних блоков | Переходы между крупными блоками: сначала определить смысл перехода и проверить существующий материал; ключевые места — выход из Татуина к Набу, после монстра к лесной группе, после захвата карты к компьютеру. Полный перечень T1–T5/M4 — в film-backlog.md. Это рекомендации для разработки/монтажа, а не утверждённые точки резки. |
| W8 | Недоделанные гонки и транспорт | референсы конкретного корабля/машины и экипажа | Рабочая зона — недоделанные гонки и транспорт. Для космической погони выбрать сцены 3+4 либо 5; татуинскую гонку согласовать со сценой 16 (бывшая W6), чтобы машина не появлялась после уничтожения. Уточнить, какие конкретные дубли ещё нужны; не генерировать все перемещения заново. Это рекомендация для разработки, а не утверждённая точка резки. |


### Ближайшие направления


Это рабочие направления для последующего разбора. Они не являются автоматическим разрешением менять существующие промты, снимать slow-lock или запускать новые генерации без отдельного решения пользователя.


1. **Закрыть сюжетную логику карты и Warcraft.** Определить, зачем Канцлеру карта, что дают её части и как это связано с Warcraft 3 / турниром, чтобы уже существующий компьютерный финал стал понятным payoff, а не случайным эпизодом.
2. **Закрыть последствия боя с монстром.** Для сцены 17 / линии W1 определить владельца набусского фрагмента, причину временного перемирия Канцлера и джедаев и понятный выход к следующей сюжетной линии.
3. **Разобраться с Татуином и транспортом.** Согласовать W6/W8 с уже существующей погоней: какую часть материала заменяет эпизод с гигантским червём, когда окончательно исчезает/разрушается машина и у кого остаётся фрагмент карты.
4. **Доделать переходы W7.** Проверить Татуин → Набу, последствия монстра → лесную группу, лесной финал → компьютер и другие слабые стыки. Генерировать новый переход только там, где функцию нельзя закрыть существующим планом, звуком или короткой репликой.
5. **Разбирать существующие NEEDS_FIX / NEEDS_RERENDER по одной сцене.** Текущие кандидаты: 3, 4, 10, 11, 13, 17. Сцены 3, 4 и 13 сейчас дополнительно находятся под slow-lock из-за активных Topview-задач; не запускать их повторно до результата/ошибки или отдельного решения пользователя. Не переписывать их массово и не считать production status разрешением на новый render.
6. **После закрытия новых сцен перейти к финальному монтажному проходу.** Выбрать сокращения повторных боёв, танцев, гиперпрыжков и лесных проходов, пересчитать хронометраж и затем вручную проверить склейки, звук, музыку, continuity и краткие артефакты.
#### Сюжетные идеи-кандидаты для детального разбора

Это предложения соавтора, а не утверждённые сцены и не разрешение на генерацию. Их задача — закрыть уже найденные сюжетные пробелы минимальным количеством нового материала.

- **Три ключа турнира.** Три фрагмента могут складываться не просто в карту сокровищ, а в древний игровой/турнирный ключ: на CRT кратко проявляются пустыня, вода и лес, затем Warcraft. Это связывает реплику про «источник контроля» с уже существующим игровым финалом без отдельной длинной сцены.
- **Долг после монстра.** Продолжить сцену 17 коротким моральным последствием: один джедай признаёт, что Канцлер помог выжить, другой подчёркивает, что это не даёт права забрать карту. Так временное перемирие получает причину.
- **Кто сдал маршрут на Татуине.** Короткий payoff через контакт/бармена/коммуникатор: координаты были проданы или переданы Канцлеру. Его появление становится следствием предыдущей сцены, а не случайностью.
- **Карта в обмен на друга на Кашиике.** Рассмотреть вариант, где фрагмент отдаётся сознательно ради спасения товарища, вместо чистого Force pull. Это делает захват последнего ключа поступком персонажа.
- **Хлеб и молоко в финале.** После запуска Warcraft вернуть бытовую просьбу из начала — «Ты хлеб и молоко купил?». Использовать только если callback усиливает финал и не ломает уже выбранную W5-логику.


#### Идеи от Саши

Распознано с четырёх рукописных листов. Это идеи, монтажные замечания и варианты сюжетной логики от Саши, а не утверждённые сцены и не разрешение автоматически менять master-промты или запускать генерации. Места, которые по фотографии нельзя уверенно разобрать, оставлены как `[неразборчиво]` вместо догадки.

- **Маша / рыбалка / возврат к миссии.** Маша в виде «Лава-лагуны» появляется во время сцены на рыбалке, «лицом к лицу» `[формулировка частично неразборчива]`. Реплика/идея: «Когда наконец сможешь уделять внимание мне, а не своим увлечениям?» → «Ой, у нас же важное поручение» → сцена бегущих ног.
- **13:37 — смена кадров.** Сделать конечный кадр с ~13:47 и начальный с ~13:36; использовать движение/новое видео для перехода к теме. Во время видео — диалог о посещении планеты для поиска карты; рядом есть пометка про кадры с Землёй/картой `[частично неразборчиво]`.
- **14:49 — переход.** Склейка ухода от карты к переходу в коридор.
- **15:18.** «Пилота сверху».
- **16:11.** «Обрезать чуть-чуть Артёма?»
- **16:0x.** Попробовать переозвучить в Wan кадры третьей сцены с `[неразборчиво]`.
- **22:30.** «Мат перезвучить стоит».
- **27:31 — корабль / интерьер.** Начало с корабля и переход к планам Ильи и Артёма внутри.
- **Warcraft → хлеб и молоко.** Отдельно отмечен возврат к шутке/мотиву «хлеб и молоко» рядом с линией Warcraft.
- **Кадр с Землёй на карте.** Отмечен как отдельный переход/вставка; продолжение записи `[неразборчиво]`.
- **29:46.** Моменты Тёмы перед `[неразборчиво]` — попробовать в Wan.
- **30:01 — после монстров.** Переход к танцам после монстров; рядом пометка, что дополнительный переход между кадрами/эпизодами, возможно, не нужен `[частично неразборчиво]`.
- **32:51 — карта.** Меч гасится → карта левитирует/летит в руку к Канцлеру.
- **32:52.** Конечный кадр — момент, когда Серёгиус почти отвернулся.
- **37:30 — полёт к планете.** Полёт к планете Саши/Паши: камера вылетает из корабля, мы видим планету и летим к ней.
- **38:41.** «Закат → рассвет → закат» — ускорить.
- **39:36.** Скрыть пару рук / кадрировать.
- **41:53 — появление Маши.** Вставка на рассвете → появление Маши → «Ой, у нас же важная миссия» → побежали.
- **42:02.** Песня `[неразборчиво]` после исчезновения/погружения в воде.
- **42:07.** После «Лава-лагуны» — кадры погружения.
- **43:07.** Диалог заменить `[продолжение неразборчиво]`.
- **44:47.** Драка после `[неразборчиво]`; рядом пометка «2 Паши».
- **45:20.** «2 Саши из-под воды» — до подводной сцены.
- **45:22.** Связать сцену под водой.
- **45:34.** Кадр со скрещёнными мечами переходит в кадр с `[неразборчиво]` → в кадр 45:44.
- **48:22 — продолжение после монстра.** Вторая сцена с `[неразборчиво]` над/после монстра продолжается. Предложенные реплики: «Спасибо, что не оставил нас сражаться в одиночку против этого гада»; «Вы бы и не справились без меня»; «Помнишь, когда мы в детстве мечтали вместе стать джедаями?» `[дальше часть фразы неразборчива]`; «А зачем тебе эта карта?»; «Почему отдал?» / «Там было…» `[продолжение неразборчиво]`.
- **49:26.** Поставить эпизод с `[неразборчиво]` при отделении/отдалении камеры.
- **50:31 — уход в лес.** Уход Лёхи и Виталика в лес → первый кадр → камера вращается между ними → показ окрестностей с подлётом к лесу (новый кадр).
- **50:44.** Олень с кораблём → `[неразборчиво]` эвоков → приветствует Олега и берёт за руку.
- **52:25.** Вставить речь джедая на озвучке, сделать её эпичной.
- **53:16.** Показ спуска на землю.

**Отдельная сюжетная логика от Саши:**
- Продумать связную логику происходящего **от кантины до попадания в комнату с Канцлером**.
- **Три карты → три артефакта древности.** Рядом пометки: «диск / провод к розетке / мышь» `[частично неразборчиво]`.
- Реплика/смысл: **«Вы получили доступ к запретному знанию»**.
- Предусмотреть заключительный кадр с джедаями, которые потеряли карту `[часть формулировки неразборчива]`.
- Карты/артефакты дают доступ к **координатам заброшенного объекта в космосе** `[точное определение объекта неразборчиво]`; в связанной комнате/объекте есть компьютер/терминал, после чего появляется голограмма/карта с координатами `[частично неразборчиво]`.


---


<a id="scene-1"></a>


## Сцена 1 — Джедаи на крыше: проход с зажжёнными мечами


<!-- scene-meta: {"duration_s":30,"dialogue":{"enabled":false,"language":null},"tags":["ensemble","continuous_take","manual_review"]} -->


**Контекст использования:** Сверка: наличие именно этого прохода шестёрки в готовой сборке не подтверждено. Варианты A/B — на выбор; место и необходимость сверить перед генерацией (P1 в film-backlog.md).


**Референсы:** @image1 = окружение, общий строй и позы с мечами · @image2 = персонаж 1 · @image3 = персонаж 2 · @image5 = персонаж 3 · @image6 = персонаж 4 · @image4 = персонаж 5 · @image7 = персонаж 6


**Что происходит:** Шесть джедаев идут плечом к плечу прямо на камеру по мокрой платформе на крыше Корусанта. Все мечи зажжены с первого кадра, цвета и позиции персонажей должны оставаться фиксированными. Сохранены два актуальных варианта одной сцены.


### Вариант A — максимально кинематографичный


```text
Mode: reference-to-video | Duration: 30s | Resolution: 720p | Aspect ratio: 21:9 | FPS: 24 | Native audio: on


References:
@image1 — environment / heroic group pose / lightsaber pose reference only: six Jedi Masters in a heroic rooftop lineup at dusk with ignited lightsabers. Use this image only for overall formation, rooftop mood, dusk lighting, skyline atmosphere, and general saber pose energy.
@image2 — Character 1 identity reference: beige tunic, tan robe, light-brown hair, beard.
@image3 — Character 2 identity reference: navy-blue robes, clean-shaven, short brown hair.
@image5 — Character 3 identity reference: olive tunic, flowing red hooded cloak, mustache.
@image6 — Character 4 identity reference: round glasses, beard, maroon robe over cream tunic.
@image4 — Character 5 identity reference: purple tunic, grey hooded cloak, mustache.
@image7 — Character 6 identity reference: black leather Jedi armor, short hair.


IMPORTANT REFERENCE RULE:
Use @image2, @image3, @image5, @image6, @image4, and @image7 as the PRIMARY identity and costume references for the six individual characters.
Use @image1 only as the environment, formation, rooftop mood, and lightsaber-pose reference.
Do not let @image1 override or average the individual faces, costumes, or identities from the character sheets.


Scene:
Six Jedi Masters advance shoulder-to-shoulder across a rain-slicked metal platform atop a Coruscant skyscraper at dusk, walking directly toward the camera in a slow, powerful, synchronized stride.
They feel heroic, calm, unhurried, triumphant, and unstoppable.
All lightsabers are already ignited from the very first frame and remain stable and fully visible for the entire shot.
No saber ignition animation.
No combat.
No dialogue.


Fixed lineup left-to-right — identities, costumes, and blade colors must remain locked:
1. @image2 — beige tunic, tan robe — ignited GREEN lightsaber, held raised high.
2. @image3 — navy-blue robes — ignited BLUE lightsaber, held raised.
3. @image5 — olive tunic, flowing red hooded cloak, mustache — ignited pale CYAN-BLUE lightsaber, held diagonally across the chest.
4. @image6 — round glasses, beard, maroon robe over cream tunic — ignited GREEN lightsaber, held raised.
5. @image4 — purple tunic, grey hooded cloak, mustache — ignited PURPLE lightsaber, angled low.
6. @image7 — black leather Jedi armor — ignited pale BLUE-WHITE lightsaber, held raised.


Formation lock:
All six remain in one clear horizontal heroic formation for the full 30 seconds.
No one changes places.
No one crosses in front of another.
No one falls behind.
All six stay fully visible in frame from head to toe throughout the shot.


Camera:
Single continuous low-angle ultra-wide tracking shot.
The camera retreats backward at exactly the same speed as the group walks forward.
Keep all six characters framed shoulder-to-shoulder for the full 30 seconds.
Use subtle cinematic parallax and slight lateral drift for grandeur, but never lose the full six-person formation.
No cuts. No jump cuts. No reframing into singles.


Atmosphere:
Overcast dusk sky above Coruscant.
Dense futuristic spired skyline in the background.
A few distant air-speeders drifting past.
Warm city bokeh far below.
Steady wind pushes cloaks, robes, and hair backward naturally.
Wet floor tiles catch reflections from the skyline and the glowing lightsabers.


Lightsaber realism:
Each blade emits a strong, stable glow with realistic colored rim light and reflections on the wet floor and nearby clothing.
Glow stays primarily associated with its own character.
Only subtle natural spill light may touch the nearest surfaces.
Do not let one character's blade color contaminate the identity of neighboring characters.
Blades must not flicker, bend unnaturally, vanish, or change color mid-shot.


Style:
Photoreal cinematic sci-fi fantasy.
Epic big-budget production feel.
Anamorphic lens flare.
Subtle cinematic lens flare on the brightest blades and distant city lights.
Moderate depth of field so all six faces remain readable while the background falls slightly soft.
Subtle film grain.
Natural cloth simulation.
Stable facial identity throughout.


Performance:
The group walks with deliberate, synchronized confidence.
Serious, focused expressions.
No exaggerated gestures.
The red cloak of Character 3 flows dramatically in the wind.
Character 4 feels grounded and dignified.
Character 5's low purple blade adds visual contrast.
Character 6 feels especially solid and imposing.


Audio (native):
Rhythmic footsteps on wet metal.
Low ambient wind.
Six distinct lightsaber hums, each with slightly different pitch and character.
Distant city hum.
Occasional faint engine passes overhead.
No dialogue.
No music.


Negative prompt: face swapping between characters, identity drift, duplicated or merged faces, extra people, missing people, distorted hands, extra fingers, costume swapping, blade color changing mid-shot, flickering blades, disappearing blades, warped or melted sabers, blade glow overwhelming faces, skyline warping, platform warping, camera jitter, cuts, jump cuts, cartoon look, video-game rendering, text, logos, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


### Вариант B — максимально стабильный


```text
Mode: reference-to-video | Duration: 30s | Resolution: 720p | Aspect ratio: 21:9 | FPS: 24 | Native audio: on


References:
@image1 — environment / group arrangement / saber-pose reference only: rooftop platform at dusk, six-person formation, ignited lightsabers, heroic overall mood.
@image2 — Character 1 identity reference: beige tunic, tan robe, light-brown hair, beard.
@image3 — Character 2 identity reference: navy-blue robes, clean-shaven, short brown hair.
@image5 — Character 3 identity reference: olive tunic, red hooded cloak, mustache.
@image6 — Character 4 identity reference: round glasses, beard, maroon robe over cream tunic.
@image4 — Character 5 identity reference: purple tunic, grey hooded cloak, mustache.
@image7 — Character 6 identity reference: black leather Jedi armor, short hair.


IMPORTANT REFERENCE RULE:
Use @image2, @image3, @image5, @image6, @image4, and @image7 as the PRIMARY character identity references.
Use @image1 only for rooftop environment, dusk skyline, formation, and general lightsaber pose arrangement.
Do not replace or average the individual faces using @image1.


Scene:
Six Jedi Masters walk shoulder-to-shoulder toward the camera on a rooftop platform high above Coruscant at dusk.
They move slowly, evenly, and in perfect formation.
The tone is heroic, calm, and powerful.
All lightsabers are already ignited from frame one and remain stable for the entire 30 seconds.
No ignition animation.
No combat.
No dialogue.


Fixed lineup left-to-right — absolutely locked:
1. @image2 — beige tunic, tan robe — GREEN lightsaber raised high.
2. @image3 — navy-blue robes — BLUE lightsaber raised.
3. @image5 — olive tunic, red hooded cloak, mustache — pale CYAN-BLUE lightsaber across chest.
4. @image6 — round glasses, beard, maroon robe over cream tunic — GREEN lightsaber raised.
5. @image4 — purple tunic, grey hooded cloak, mustache — PURPLE lightsaber angled low.
6. @image7 — black leather Jedi armor — pale BLUE-WHITE lightsaber raised.


Strict formation lock:
All six characters remain in the same order for the full 30 seconds.
No one changes places.
No one moves ahead.
No one falls behind.
No one crosses in front of another.
Keep equal spacing between all characters.
Keep all six full-body figures visible the entire time.


Camera:
Single continuous shot.
Low-angle wide tracking shot.
The camera moves backward at exactly the same speed as the group.
Keep framing stable and centered.
Do not push in.
Do not orbit.
Do not crop the leftmost or rightmost characters.
Do not reframe to singles or close-ups.
Only minimal camera sway is allowed.
No cuts. No jump cuts.


Atmosphere:
Coruscant skyline at dusk.
Tall futuristic towers in the distance.
A few small distant air-speeders.
Wet metal floor with subtle reflections.
Soft evening sky.
Gentle wind only.
The environment remains stable and consistent.


Lightsaber behavior:
All blades remain continuously visible and fully ignited.
Blade lengths remain constant.
Blade colors remain constant.
No flicker, no disappearance, no color swapping.
Each blade casts realistic glow mainly on its owner and the nearby floor.
Only subtle natural light spill on adjacent surfaces.
Do not let glow confuse neighboring costume colors or faces.


Style:
Photoreal cinematic look.
Realistic live-action feel.
Moderate depth of field so all six faces stay clear.
Minimal lens flare.
Subtle film grain.
Natural cloth movement.
Stable facial identity and costume details throughout.


Performance:
All six walk with restrained confidence.
Expressions are serious and focused.
No exaggerated acting.
No talking.
No gestures beyond natural walking and stable saber carry.
No saber swinging.


Audio (native):
Steady footsteps on wet metal.
Gentle wind.
Six stable lightsaber hums with slightly varied tone.
Distant city ambience.
No dialogue.
No music.


Negative prompt: face swap, face duplication, merged characters, missing characters, extra people, costume color swapping, identity drift, flickering blades, disappearing blades, changing blade colors, unstable saber length, warped sabers, glowing blades covering faces, distorted hands, extra fingers, warped platform, skyline warping, camera shake, cuts, jump cuts, cartoon, game-render look, text, captions, logos, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-2"></a>


## Сцена 2 — Джедаи на крыше: триумфальный марш без мечей


<!-- scene-meta: {"duration_s":30,"dialogue":{"enabled":false,"language":null},"tags":["ensemble","continuous_take","manual_review"],"target_engine":"Seedance 2.5"} -->


**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**


**Контекст использования:** Сверка: варианты A/B — на выбор. Согласовать использование со сценой 1, чтобы не добавлять два одинаковых по функции марша (P2).


**Референсы:** @image1 = окружение и строй · @image2 = персонаж 1 · @image3 = персонаж 2 · @image5 = персонаж 3 · @image6 = персонаж 4 · @image4 = персонаж 5 · @image7 = персонаж 6


**Что происходит:** Те же шесть джедаев медленно и синхронно идут прямо на камеру без обнажённого оружия. Плащи и волосы двигаются от ветра, играет эпическая оркестровая музыка. Сохранены два актуальных варианта одной сцены.


### Вариант A — максимально кинематографичный


```text
Mode: reference-to-video | Duration: 30s | Resolution: 720p | Aspect ratio: 21:9 | FPS: 24 | Native audio: on


References:
@image1 — environment / group mood / rooftop lineup reference only: six Jedi Masters standing in a heroic lineup on a Coruscant rooftop at dusk. Use this image only for overall mood, skyline atmosphere, rooftop scale, and heroic ensemble feeling.
@image2 — Character 1 identity reference: beige tunic, tan robe, light-brown hair, beard.
@image3 — Character 2 identity reference: navy-blue robes, clean-shaven, short brown hair.
@image5 — Character 3 identity reference: olive tunic, flowing red hooded cloak, mustache.
@image6 — Character 4 identity reference: round glasses, beard, maroon robe over cream tunic.
@image4 — Character 5 identity reference: purple tunic, grey hooded cloak, mustache.
@image7 — Character 6 identity reference: black leather Jedi armor, short hair.


IMPORTANT REFERENCE RULE:
Use @image2, @image3, @image5, @image6, @image4, and @image7 as the primary identity references for the six individual characters.
Use @image1 only for the rooftop environment, heroic dusk mood, skyline composition, and lineup energy.
Do not let @image1 override the specific faces, costumes, or identities from the individual character sheets.


Scene:
Six Jedi Masters walk shoulder-to-shoulder across a rain-slicked metal platform atop a Coruscant skyscraper at dusk, advancing directly toward camera in a slow, powerful, synchronized heroic stride.
They feel triumphant, iconic, calm, and unstoppable.
Hands remain empty throughout. No lightsabers ignited. No weapons drawn. No blades in hand.


Fixed lineup left-to-right — do not swap:
1. @image2 — beige tunic, tan robe.
2. @image3 — navy-blue robes.
3. @image5 — olive tunic, red hooded cloak, mustache.
4. @image6 — round glasses, beard, maroon robe over cream tunic.
5. @image4 — purple tunic, grey hooded cloak, mustache.
6. @image7 — black leather Jedi armor.


Formation lock:
All six remain in one clear horizontal heroic lineup for the full shot.
No one changes places.
No one crosses in front of another.
No one falls behind.
All six stay fully visible in frame throughout.


Camera:
Single continuous low-angle ultra-wide tracking shot.
The camera retreats backward at exactly the same speed as the group walks forward.
Keep the entire six-person lineup visible for the full 30 seconds.
Use subtle cinematic lateral drift and parallax only.
Occasionally let foreground perspective shift slightly for grandeur, but never lose the full formation.
No cuts. No jump cuts. No sudden reframing.


Atmosphere:
Coruscant rooftop at dusk.
Vast futuristic skyline filled with tall spires and distant flying traffic.
Wet reflective metal platform with puddle sheen and subtle reflections underfoot.
Overcast blue-violet evening sky with fading warm light at the horizon.
A few distant air-speeders drift behind the group.
A steady wind pushes robes, cloaks, and hair backward naturally.
The mood is mythic, heroic, and triumphant.


Style:
Photoreal cinematic sci-fi fantasy.
Big-budget epic production look.
Anamorphic lens flare.
Subtle cinematic lens flares on distant city lights.
Soft atmospheric haze.
Shallow depth of field, but all six faces must remain readable.
Subtle film grain.
Natural cloth simulation.
Stable identity throughout.


Motion rhythm:
The group walks with calm, heavy confidence.
Each step feels deliberate and synchronized.
The red cloak of Character 3 flows dramatically in the wind.
The maroon robe of Character 4 moves with dignified weight.
The grey cloak of Character 5 flutters lightly.
Character 6 in black armor feels especially solid and imposing.
No exaggerated gestures.


Audio (native):
Sweeping triumphant orchestral score with brass fanfare, rising strings, and epic percussion building gradually through the full 30 seconds.
Low wind ambience.
Clear synchronized footsteps on wet metal audible beneath the music.
No dialogue.
No vocals.


Negative prompt: ignited lightsabers, glowing blades, weapons in hands, face swaps, costume swaps, duplicated people, merged bodies, missing people, distorted hands, extra fingers, warped skyline, melting geometry, camera jitter, fast shaky movement, cuts, jump cuts, cartoon look, video-game look, text, captions, logos, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


### Вариант B — максимально стабильный


```text
Mode: reference-to-video | Duration: 30s | Resolution: 720p | Aspect ratio: 21:9 | FPS: 24 | Native audio: on


References:
@image1 — environment / formation reference only: rooftop platform at dusk, heroic six-person lineup, Coruscant skyline.
@image2 — Character 1 identity reference: beige tunic, tan robe, light-brown hair, beard.
@image3 — Character 2 identity reference: navy-blue robes, clean-shaven, short brown hair.
@image5 — Character 3 identity reference: olive tunic, red hooded cloak, mustache.
@image6 — Character 4 identity reference: round glasses, beard, maroon robe over cream tunic.
@image4 — Character 5 identity reference: purple tunic, grey hooded cloak, mustache.
@image7 — Character 6 identity reference: black leather Jedi armor, short hair.


IMPORTANT REFERENCE RULE:
Use @image2, @image3, @image5, @image6, @image4, and @image7 as the primary character identity references.
Use @image1 only for rooftop environment, dusk skyline, and group arrangement.
Do not replace or average the individual faces using @image1.


Scene:
Six Jedi Masters walk shoulder-to-shoulder toward the camera on a rooftop platform high above Coruscant at dusk.
They move slowly, evenly, and in perfect formation.
The tone is heroic and calm.
Hands remain empty throughout.
No lightsabers ignited.
No weapons drawn.
No blades in hand.


Fixed lineup left-to-right — absolutely locked:
1. @image2 — beige tunic, tan robe.
2. @image3 — navy-blue robes.
3. @image5 — olive tunic, red hooded cloak, mustache.
4. @image6 — round glasses, beard, maroon robe over cream tunic.
5. @image4 — purple tunic, grey hooded cloak, mustache.
6. @image7 — black leather Jedi armor.


Strict formation lock:
All six characters remain in the same order for the full 30 seconds.
No one changes places.
No one moves ahead.
No one falls behind.
No one crosses in front of another.
Keep equal spacing between all characters.
Keep all six full-body figures visible the entire time.


Camera:
Single continuous shot.
Low-angle wide tracking shot.
The camera moves backward at the exact same speed as the group.
Keep framing stable and centered.
Do not push in.
Do not orbit.
Do not crop the leftmost or rightmost characters.
Do not reframe to singles or close-ups.
Only minimal camera sway is allowed.
No cuts. No jump cuts.


Atmosphere:
Coruscant skyline at dusk.
Tall futuristic towers in the distance.
A few tiny distant air-speeders.
Wet metal floor with subtle reflections.
Soft evening sky.
Gentle wind only.
The environment stays stable and consistent.


Style:
Photoreal cinematic look.
Realistic live-action feel.
Moderate depth of field so all six faces stay clear.
Minimal lens flare.
Subtle film grain.
Natural cloth movement.
Stable facial identity and costume details throughout.


Performance:
All six walk with restrained confidence.
Expressions are serious and focused.
No exaggerated acting.
No talking.
No gestures.
Only subtle natural head and body motion while walking.


Audio (native):
Epic but restrained orchestral music.
Steady heroic rhythm.
Footsteps on wet metal.
Light wind.
No dialogue.
No vocals.


Negative prompt: ignited lightsabers, glowing blades, weapons in hands, face swap, face duplication, merged characters, missing characters, costume color swapping, identity drift, extra people, distorted hands, extra fingers, warped platform, skyline warping, camera shake, cuts, jump cuts, cartoon, stylized game-render look, text, captions, logos, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-3"></a>


## Сцена 3 — Космическая погоня: экстерьер


<!-- scene-meta: {"production_state":"NEEDS_FIX","duration_s":30,"dialogue":{"enabled":false,"language":null},"tags":["action","needs_fix","continuity"]} -->


**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**


**Контекст использования:** Сверка: актуальная связка со сценой 4; сцена 5 — альтернатива всей связке. Космический бой уже есть в фильме, поэтому выбрать заменяемый участок части 1 / 21:10–23:55 (P3).


**Референсы:** @image1 = стартовый космический кадр · @image2 = точный дизайн транспортного корабля


**Что происходит:** Сцена сразу начинается в разгаре космического боя. Транспорт уклоняется от атак двух истребителей и отвечает огнём. Камера постепенно сближается с боковым окном кабины и заканчивает сцену яркой вспышкой/смазом у стекла для перехода к интерьеру.


```text
Mode: image-to-video (first frame: @image1) + reference image @image2 (ship design)
Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | Native audio: on


Scene: Starting on the deep-space starfield of @image1, the camera whip-pans hard and fast to the right in a sudden snap-motion — no slow reveal — immediately catching the transport ship from @image2 already in the middle of a firefight: engines glowing blue, already banking as blaster bolts streak past it through the nebula haze.


Action: Two enemy fighters flank the transport, cannons flashing; it banks hard left dodging a volley, its dorsal turret swinging and returning fire, clipping one fighter which spins off trailing smoke. A second fighter swoops in from the opposite side — the transport banks hard right, bolts sizzling past the hull, one impact sparking off the armor plating. Camera drifts alongside throughout, gradually closing the distance toward the ship's cockpit side window as the final beat — ending on a fast whip-pan/lens-flare blur exactly as it reaches the glass, whiting out the frame for the cut.


Ship: exact same hull, turret placement, engine glow color and battle-worn paint as @image2 — do not alter the design.


Audio (native): distant engine roar, blaster fire cracks, whooshing bolts, a metallic impact spark, tense rising rumble building toward the final blur. No dialogue, no music.


Style: photoreal space-opera cinematography, anamorphic flares, subtle film grain, no on-screen text, logos, or watermark.


Negative prompt: slow calm opening, static holding shot, ship geometry changing, extra or missing turrets/engines, engine glow color shifting, camera clipping through hull, fighters morphing or duplicating, warping starfield, text, logos, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-4"></a>


## Сцена 4 — Космическая погоня: интерьер кабины


<!-- scene-meta: {"production_state":"NEEDS_FIX","duration_s":17,"dialogue":{"enabled":false,"language":null},"dependencies":[{"type":"continues","scene":3}],"tags":["action","needs_fix","continuity"]} -->


**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**


**Контекст использования:** Сверка: прямое продолжение сцены 3. Перед генерацией сопоставить корабль, экипаж и конечный кадр с монтажом; не добавлять одновременно с альтернативой 5 (P4).


**Референсы:** @image3 = точный первый кадр и оба персонажа в кабине · @image4 = точный последний кадр с пилотом крупным планом


**Что происходит:** Продолжение космического боя внутри кабины. Корабль продолжает маневрировать, экипаж реагирует на бой, а камера плавно приближается к пилоту и к последнему кадру должна точно прийти в композицию @image4.


```text
Mode: first-and-last-frame (first frame: @image3, last frame: @image4)
Duration: 17s | Resolution: 1080p | Aspect ratio: 16:9 | Native audio: on


Scene: Interior cockpit exactly as in @image3 — bearded pilot in tan/cream robe at the controls in background, second crewmate in red/green robe leaning over the console in foreground. Ship is still banking from the dogfight; another vessel streaks past the windows.


Action: camera slowly pushes in and reframes over the duration, the foreground crewmate glancing at his console then out of frame, the pilot's hands working the twin throttle levers reactively with each bank. Camera settles into the exact close framing, angle, lighting, and console details of @image4 by the final frame — same "Vmax" throttle grips, same focused expression, same passing ship visible through the window.


Character identity: keep both characters' faces, hair, and robe colors fixed throughout — no face swapping or blending between the two.


Audio (native): rattling cockpit frame, muffled blaster impacts outside, engine strain, an alarm chirp, tense breathing. No dialogue.


Style: same photoreal cinematography as the companion clip, no on-screen text, logos, or watermark.


Negative prompt: face swapping between characters, identity drift, extra crew members appearing, robe colors changing, cockpit geometry morphing, camera cuts within the clip, text, logos, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-5"></a>


## Сцена 5 — Космическая погоня: единый дубль через стекло


<!-- scene-meta: {"duration_s":30,"dialogue":{"enabled":false,"language":null},"dependencies":[{"type":"alternative_to","targets":[3,4]}],"tags":["action","continuous_take","alternative","manual_review"]} -->


**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**


**Контекст использования:** Сверка: выбирать 3+4 ИЛИ 5. Этот дубль не является третьей обязательной частью погони (P5).


**Референсы:** @image1 = первый кадр космоса · @image2 = дизайн корабля · @image3 = интерьер и экипаж · @image4 = точный последний кадр


**Что происходит:** Альтернативная версия сцен 3–4 одним непрерывным дублем: космический бой снаружи → камера физически проходит через стекло кабины без склейки и разрушения стекла → оказывается внутри → приближается к пилоту → заканчивает точно на @image4.


```text
Mode: first-and-last-frame (first frame: @image1, last frame: @image4) + reference images @image2 (ship design), @image3 (interior framing reference)
Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | Native audio: on


Scene: Starting on the deep-space starfield of @image1, the camera whip-pans hard right in a sudden snap-motion to reveal the transport ship from @image2 already under fire from two enemy fighters — engines flaring, banking hard through blaster bolts, dorsal turret returning fire. Camera stays close alongside the hull as it dodges left, then right, bolts sizzling past.


As the ship banks toward camera, the camera keeps moving forward in one unbroken motion directly through the cockpit's side window glass — the glass registers as a soft blur/refraction pass, not a shatter and not a hard cut — emerging inside the cockpit exactly into the framing of @image3: bearded pilot in tan/cream robe at the controls, second crewmate in red/green robe leaning over the console in the foreground, both reacting to the battle still visible outside.


Camera continues pushing in past the foreground crewmate toward the pilot, settling into the exact close framing, angle, lighting, and console details of @image4 by the final frame — same "Vmax" throttle grips, same focused expression, same passing ship visible through the window.


Character identity: keep both characters' faces, hair, and robe colors fixed throughout — no face swapping or blending between the two. Ship keeps the exact same hull, turret placement, and engine glow color as @image2 throughout.


Audio (native): engine roar and blaster fire outside, transitioning into a muffled rattling cockpit interior as the camera passes through the glass, an alarm chirp, tense breathing near the end. No dialogue, no music.


Style: photoreal space-opera cinematography, anamorphic flares, subtle film grain, one continuous unbroken camera move, no visible cut, no on-screen text, logos, or watermark.


Negative prompt: camera cut or hard edit, glass shattering, glass vanishing instead of a see-through pass, ship geometry changing, extra or missing turrets/engines, engine glow color shifting, fighters morphing or duplicating, warping starfield, face swapping between characters, identity drift, extra crew members appearing, robe colors changing, cockpit geometry morphing, text, logos, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-10"></a>


## Сцена 10 — Кантина: допрос про товар, часть 1


<!-- scene-meta: {"target_engine":"Wan 3","production_state":"NEEDS_FIX","duration_s":30,"dialogue":{"enabled":true,"language":"ru"},"tags":["dialogue","needs_fix"]} -->


**Контекст использования:** Сверка: актуальная связка со сценой 11. В фильме уже есть контакт в кантине; наличие именно разговора Хана о товаре не подтверждено. При замене сохранить функцию эпизода с картой (P10).


**Референсы:** @Image1 = композиция кантины и Чубакка · @Image2 = Han · @Image3 = Jedi


**Что происходит:** Джедай требует от Хана обещанный товар. Хан изображает полное непонимание и в конце обращается к Чубакке как к свидетелю; Чубакка отвечает вопросительным рыком.


```text
[IMAGE REFERENCE 1: @Image1 - Cantina Composition & Chewbacca Reference] 
[IMAGE REFERENCE 2: @Image2 - Han Model Sheet] 
[IMAGE REFERENCE 3: @Image3 - The Jedi Model Sheet] 
 
Optimized for Wan 3 | Photorealistic Acting, Facial Micro-Expressions & Dialogue Focus | Duration: 30s | 4K 24fps 
 
ENVIRONMENT & ASSET LOCK: 
- THE JEDI (@Image3): Mustached man, tousled brown hair, weathered face with faint frown lines, light-green layered tunic, hooded deep-red cloak with the hood down, brown leather boots, a metal lightsaber hilt clipped to his belt. Wary, slightly bewildered expression throughout — this is clearly not going the way he expected. 
- HAN (@Image2): Sandy-brown hair, light stubble, cream shirt under an open black vest, blue trousers with a red side-stripe, holstered blaster on a leg-strap. Relaxed, faux-innocent expression, visibly playing dumb. 
- CHEWBACCA (matching @Image1): Towering bipedal Wookiee, shaggy reddish-brown fur, bandolier across his chest, expressive amber eyes. Communicates only in wookiee growls/roars — no words, no subtitles. 
- Setting: Same dim, smoke-hazed desert-cantina interior as @Image1 — stone archways, hanging amber lantern overhead, alien patrons blurred in the background, round metal table between the three. 
 
ACTING & DIALOGUE TIMELINE (00:00 - 00:30): 
 
- 00:00–00:08 (Shot 1 - The Accusation): 
Medium three-shot across the table. THE JEDI leans forward slightly, direct and serious, holding eye contact with Han: 
JEDI: «Ты добыл товар как договаривались?» 
Quick cut to Han's face — genuine-looking confusion mixed with a faint, too-innocent smile: 
HAN: «Какой ещё товар?» 
 
- 00:08–00:16 (Shot 2 - Spelling It Out): 
Close-up on THE JEDI, brow furrowed, patient but firm, spelling it out slowly and clearly: 
JEDI: «Я заплатил тебе, чтобы ты выкрал снюс у торговца спайсом.» 
Hold on his stern expression for a beat after the line. 
 
- 00:16–00:24 (Shot 3 - Playing Dumb): 
Cut to Han, shrugging with exaggerated innocence, glancing sideways toward Chewbacca as he speaks: 
HAN: «Не помню такого. Я тебя впервые вижу. Правда же, Чубака?» 
 
- 00:24–00:30 (Shot 4 - The Growl): 
Cut to CHEWBACCA — a long, questioning-sounding growl/roar, head tilting slightly. Quick reaction cut to THE JEDI's face, eyebrows raised, visibly thrown off. 
 
LIGHTING & VISUAL EFFECTS: 
Warm amber lantern light from directly overhead, soft haze/smoke drifting through the light beam, out-of-focus alien patrons in the background, shallow depth of field keeping the three main faces sharp. 
 
AUDIO: 
Clear Russian dialogue as written, one long expressive Wookiee growl in Shot 4, quiet ambient cantina chatter and distant alien music underneath — kept low enough not to compete with the dialogue, no non-diegetic score. 
 
NEGATIVE PROMPT: rushed dialogue, overlapping speech, Wookiee speaking actual words, subtitles, text on screen, expressionless faces, cartoon, anime, low quality, watermark, logo, unwanted non-diegetic music.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-11"></a>


## Сцена 11 — Кантина: допрос про товар, часть 2


<!-- scene-meta: {"target_engine":"Wan 3","production_state":"NEEDS_FIX","duration_s":30,"dialogue":{"enabled":true,"language":"ru"},"dependencies":[{"type":"continues","scene":10}],"tags":["dialogue","needs_fix","continuity"]} -->


**Контекст использования:** Сверка: продолжение сцены 10. Плёнка на стекле уже показана в части 1 / 19:05–19:36; здесь нужно уточнить смысл повторного вопроса о плёнке, не представлять сцену без пояснения как её первое получение. Реплики пока сохранены (P11).


**Референсы:** те же @Image1 = композиция/Чубакка · @Image2 = Han · @Image3 = Jedi


**Что происходит:** Прямое продолжение части 1 без скачка во времени. Джедай шутит про Чубакку, тот возмущённо рычит, затем разговор переключается на плёнку, и Хан окончательно перестаёт понимать, о чём речь.


```text
[IMAGE REFERENCE 1: @Image1 - Cantina Composition & Chewbacca Reference] 
[IMAGE REFERENCE 2: @Image2 - Han Model Sheet] 
[IMAGE REFERENCE 3: @Image3 - The Jedi Model Sheet] 
 
Optimized for Wan 3 | Photorealistic Acting, Facial Micro-Expressions & Dialogue Focus | Duration: 30s | 4K 24fps 
 
ENVIRONMENT & ASSET LOCK: 
- THE JEDI (@Image3): Mustached man, tousled brown hair, weathered face with faint frown lines, light-green layered tunic, hooded deep-red cloak with the hood down, brown leather boots, a metal lightsaber hilt clipped to his belt. 
- HAN (@Image2): Sandy-brown hair, light stubble, cream shirt under an open black vest, blue trousers with a red side-stripe, holstered blaster on a leg-strap. 
- CHEWBACCA (matching @Image1): Towering bipedal Wookiee, shaggy reddish-brown fur, bandolier across his chest, expressive amber eyes. Growls/roars only, no words. 
- Setting: Direct continuation from the previous scene — identical cantina table, seating, and lighting, no time skip. 
 
ACTING & DIALOGUE TIMELINE (00:00 - 00:30): 
 
- 00:00–00:10 (Shot 1 - The Theory): 
Medium shot on THE JEDI, gesturing dismissively toward Chewbacca, half-amused and half-exasperated. Deliver with a small natural beat/pause between the two sentences for comedic timing — unhurried: 
JEDI: «Да никто не понимает, что он говорит. Может, он просто срать хочет, а выйти не может — ты тут сидишь.» 
 
- 00:10–00:16 (Shot 2 - Offended Growl): 
Cut to CHEWBACCA — a sharper, more indignant-sounding growl/roar, visibly offended by the remark. Brief reaction cut to Han smirking slightly. 
 
- 00:16–00:22 (Shot 3 - Changing the Subject): 
Cut to THE JEDI, tone shifting, more businesslike, moving on to his next question: 
JEDI: «Так а плёнку ты принёс?» 
 
- 00:22–00:30 (Shot 4 - Final Confusion): 
Close-up on Han, throwing his hands up slightly, genuinely exasperated now: 
HAN: «Какую плёнку? Мужик, ты вообще кто?» 
Hold on his baffled expression as the shot ends. 
 
LIGHTING & VISUAL EFFECTS: 
Same warm amber lantern light and soft haze as the previous scene, shallow depth of field, out-of-focus background patrons. 
 
AUDIO: 
Clear Russian dialogue as written, one sharp indignant Wookiee growl in Shot 2, same quiet ambient cantina bed as the previous scene, no non-diegetic score. 
 
NEGATIVE PROMPT: rushed dialogue, overlapping speech, Wookiee speaking actual words, subtitles, text on screen, expressionless faces, cartoon, anime, low quality, watermark, logo, unwanted non-diegetic music.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-13"></a>


## Сцена 13 — Совет джедаев: говорящий кот


<!-- scene-meta: {"production_state":"NEEDS_FIX","duration_s":30,"dialogue":{"enabled":true,"language":"ru"},"tags":["dialogue","comedy","continuous_take","needs_fix"]} -->


**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**


**Контекст использования:** Новый активный промт на основе бывшей W4; рабочий пункт W4 получил конкретные референсы и теперь оформлен как активная сцена 13. 30-секундный deadpan-бит после того, как решение Совета уже принято; лишнее затем можно укоротить на монтаже. В кадре сидят те же Black и Purple, которые участвуют в лесной линии; их модель-шиты используются как первичные референсы идентичности.


**Референсы:** @image1 = композиция, кресла, кальяны, панорамный город и общий свет · @image2 = точная внешность кота · @image4 = Black, первичный референс лица/телосложения/костюма · @image5 = Purple, первичный референс лица/телосложения/костюма


**Что происходит:** Black спокойно сидит слева и курит кальян. Purple сидит справа с котом на коленях и неторопливо его гладит. Сначала сцена несколько секунд живёт как совершенно серьёзный спокойный финал заседания. Затем кот постепенно становится внимательнее, поднимает голову и совершенно буднично человеческим голосом говорит: «Полностью с вами согласен, коллеги. Так и поступим». После реплики выдерживается длинная сухая пауза: Black лишь переводит взгляд на кота, Purple слегка кивает и продолжает его гладить, а кот снова устраивается на коленях, будто только что высказался обычный член Совета.


```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on


REFERENCES:
@image1 — PRIMARY composition / environment reference: two seated Jedi in large armchairs inside a futuristic high-rise council lounge, panoramic golden city skyline behind them, hookahs in frame, cat resting on the right character's lap. Preserve the overall seating arrangement, camera axis, furniture placement, warm sunset lighting, and relaxed council atmosphere.
@image2 — PRIMARY CAT identity reference: exact fluffy white-and-grey long-haired cat, green eyes, grey facial markings, grey ears and crown pattern. Preserve the cat's face shape, coat pattern, eye color, fur length, and natural feline anatomy.
@image4 — PRIMARY identity reference for BLACK: heavyset man with short brown hair, black tunic with dark leather vest panels, dark glove/forearm protection, brown trousers and boots. Match face, build, hair, and costume exactly. He is seated on the LEFT.
@image5 — PRIMARY identity reference for PURPLE: leaner mustached man with brown hair, purple inner tunic under a long grey hooded outer robe, brown belt, tan boots. Match face, mustache, build, hair, and costume exactly. He is seated on the RIGHT with the cat on his lap.


REFERENCE PRIORITY:
Use @image4 and @image5 for the two men's exact identities and costumes. Use @image2 for the cat's exact identity. Use @image1 for composition, seating, hookahs, environment, lighting, and overall mood. Do not let @image1 average or alter the faces from the character model sheets.


SCENE:
A slow, completely deadpan 30-second insert at the end of a Jedi Council discussion. BLACK and PURPLE sit exactly as established in @image1. BLACK casually smokes the hookah. PURPLE has the cat resting comfortably across his lap and gently strokes its back. Nothing is rushed. For the first half of the shot the scene should feel like an ordinary, serious council pause. The humor comes only when the realistic cat calmly joins the discussion in a human voice and both Jedi accept this as routine.


TIMELINE:
[0:00–0:06]
Stable medium-wide two-shot matching @image1. Hold the composition long enough to establish the absurdly serious calm. BLACK slowly inhales from the hookah. PURPLE sits relaxed with one hand resting on the cat. The cat lies naturally across his lap, blinking once. Warm sunset light fills the room; distant air traffic glides behind the panoramic window.


[0:06–0:12]
BLACK exhales a thin, realistic cloud of smoke that drifts upward and catches the backlight. PURPLE gives the cat one slow natural stroke from shoulders toward the back. The cat's ears make a small natural adjustment, then it turns its eyes toward BLACK for a moment and back toward the room. No one speaks. Let the silence feel deliberate rather than empty.


[0:12–0:17]
The camera continues an almost imperceptible slow push-in while keeping both men and the cat clearly visible. The cat gradually lifts its head and straightens slightly on PURPLE's lap, becoming attentive as if preparing to contribute. BLACK lowers the hookah mouthpiece. PURPLE remains completely serious and does not look surprised.


[0:17–0:22]
The cat looks forward and speaks clearly in natural Russian with restrained, believable feline mouth movement synchronized to the line. It does NOT become anthropomorphic, stand up, gesture, or change anatomy.
CAT: «Полностью с вами согласен, коллеги. Так и поступим».
Deliver the line calmly, evenly and matter-of-factly, like an experienced council member concluding a discussion.


[0:22–0:26]
Hold the silence after the line. BLACK pauses with the hookah mouthpiece in hand and slowly shifts only his eyes, then his head slightly toward the cat. His expression stays serious and almost bored — no shock. PURPLE looks ahead, composed, as though the statement was expected.


[0:26–0:30]
PURPLE gives one tiny approving nod, then resumes gently stroking the cat. The cat blinks, lowers its head and settles comfortably back into his lap. BLACK calmly returns the hookah mouthpiece toward himself. End on the same relaxed council atmosphere, with the joke played completely straight. No punchline music and no exaggerated reaction.


CAMERA:
Single continuous shot. Physically stable cinematic camera, controlled inertia, no random jitter or micro-shake. Begin as the reference two-shot and use only a very slow subtle push-in over the full 30 seconds. No cuts, no sudden reframing, no close-up that removes either man from the shot. The cat must remain readable during the spoken line.


PERFORMANCE:
BLACK: relaxed, almost bored, restrained natural breathing, minimal eye/head movement, no dialogue. His reaction after the cat speaks is intentionally tiny.
PURPLE: calm, serious, gently affectionate toward the cat, no surprise, no dialogue. One subtle approving nod near the end is allowed.
CAT: remains a realistic domestic cat. Natural blinking, ear movement, head lift and settling. During speech, use only minimal realistic jaw/muzzle motion necessary for understandable lip synchronization; no human lips, no exaggerated mouth opening.


STYLE / LIGHTING:
Photorealistic live-action cinematic sci-fi. Warm golden sunset backlight, soft atmospheric haze, realistic hookah smoke, subtle reflections on metal and glass, moderate depth of field so both human faces and the cat remain readable. Preserve spatial continuity and furniture geometry throughout.


AUDIO (native):
Quiet futuristic council-room ambience, distant city traffic through the glass, soft hookah bubbling, a gentle exhale of smoke, very subtle cloth/fur movement. Preserve the long quiet beats before and after the joke. The cat speaks one clear Russian line with a calm, matter-of-fact human voice: «Полностью с вами согласен, коллеги. Так и поступим». No subtitles. No music.


NEGATIVE PROMPT:
identity drift, face swap, face duplication, costume swap, missing mustache, wrong body shape, different cat markings, changing cat eye color, anthropomorphic cat body, cat standing like a human, human lips on cat, exaggerated cartoon mouth, distorted muzzle, extra limbs, duplicated cat, warped hands, extra fingers, hookah geometry morphing, furniture moving, skyline warping, extra characters entering frame, subtitles, text, logos, watermark, exaggerated acting, slapstick reaction, camera shake, hard cuts, cartoon, anime, game-render look.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```
---


<a id="scene-16"></a>


## Сцена 16 — Татуин: гигантский пустынный червь и бой на руинах


<!-- scene-meta: {"target_engine":"Seedance 2.5","production_state":"READY","duration_s":30,"dialogue":{"enabled":false,"language":null},"tags":["action","continuous_take"]} -->


**Контекст использования:** Новый активный промт на основе бывшей W6; рабочий пункт W6 получил конкретные референсы и теперь оформлен как активная сцена 16. 30-секундная большая пустынная сцена для Seedance 2.5: двое татуинных джедаев и Канцлер сталкиваются на руинах, а из-под земли вырывается колоссальный песчаный червь. Сцена должна работать как самостоятельный мощный экшен-блок, из которого потом при желании можно отдельно собрать и более короткий фрагмент.


**Референсы:** @Video1 = пустынная локация, руины, общий масштаб и композиционный дух сцены · @Image1 = Hooded Jedi · @Image2 = Bearded Jedi · @Image3 = Chancellor


**Что происходит:** На пустынных руинах двое джедаев и Канцлер находятся в напряжённом противостоянии. Внезапно земля начинает дрожать, и из песка вырывается колоссальный пустынный червь масштаба «гигантское стихийное бедствие». Он рушит окружающие конструкции, вздымает песчаные волны, делает несколько агрессивных заходов и кружит вокруг героев. На протяжении всей сцены герои остаются в кадре на фоне катастрофы, продолжают сражаться и вынуждены постоянно уклоняться от атак чудовища и обрушений.


```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on


REFERENCES:
@Video1 — PRIMARY environment and staging reference: a desert ruins location with open sandy space, broken structures, weathered stone or metal debris, and a composition suitable for a large-scale action scene. Use it for the location feel, scale, terrain, ruin placement, and general camera mood.
@Image1 — PRIMARY identity reference for the Hooded Jedi: mustached man, tousled brown hair, weathered face, light-green layered tunic, deep-red hooded cloak, brown boots, lightsaber hilt on belt. Preserve face, costume, proportions and overall identity exactly.
@Image2 — PRIMARY identity reference for the Bearded Jedi: heavier build, short beard, cream tunic under a brown Jedi over-robe, wide brown belt, brown boots, lightsaber hilt on belt. Preserve face, build, costume and identity exactly.
@Image3 — PRIMARY identity reference for the Chancellor: pale man with thinning hair / bald crown and deep purple robes. Preserve face, body type, robe silhouette and identity exactly.


REFERENCE PRIORITY:
Use @Image1, @Image2 and @Image3 as the absolute identity lock for the three characters. Use @Video1 for the desert ruins environment, spatial layout and action scale. Do not let the environment reference overwrite the character identities.


SCENE OVERVIEW:
A photorealistic cinematic desert action scene on ruined Tatooine-like wasteland terrain. The Hooded Jedi and the Bearded Jedi are confronting the Chancellor among weathered ruins when a colossal subterranean sandworm erupts from beneath the ground and turns the entire location into chaos. The worm is gigantic on the scale of a natural disaster — towering, segmented, immense, powerful, with a massive circular maw and rows of terrifying teeth. It is not a small monster; it feels like an unstoppable force of nature. Throughout the scene, the three characters stay grounded in the same battle space and must keep fighting and dodging while the worm attacks the environment around them.


ACTION TIMELINE — SINGLE CONTINUOUS 30-SECOND TAKE:
[0:00–0:05]
Begin with a tense standoff on the ruined desert location. The Hooded Jedi and the Bearded Jedi face the Chancellor at medium distance. Wind moves robes and loose sand. The camera glides laterally through the ruins, keeping all three readable in the same frame. Small grains of sand begin to tremble across the ground and a low subterranean rumble builds beneath the dialogue-free tension.


[0:05–0:09]
The rumble intensifies violently. Sand ripples outward in fast concentric waves. Broken beams, rocks and debris start to shake loose. All three characters instinctively shift their stance and glance toward the source of the vibration. Then the ground splits open behind and slightly to the side of them. A colossal sandworm bursts out of the earth in an explosive eruption of sand and debris, instantly dominating the background.


[0:09–0:14]
The worm rises to full terrifying scale, rearing high above the ruins with its gigantic circular mouth open. Sand cascades off its ridged body. The shockwave throws dust through the air and knocks loose pieces of the surrounding structures. The heroes break their positions and sprint in different directions to avoid the collapse and the worm's initial surge. The camera keeps moving fluidly, holding spatial continuity so the audience clearly understands where each person is relative to the worm.


[0:14–0:20]
The Hooded Jedi and the Bearded Jedi attempt to regroup while the Chancellor uses the chaos to press his advantage. The three continue their live-action fight in short fast exchanges — evasive footwork, quick defensive movements, robe motion, physical urgency — but the worm remains the dominant threat in the background. It sweeps across the ruins, slamming its body through structures and sending dust clouds and fragments outward. Everyone is forced to interrupt combat and dodge a second aggressive pass from the worm.


[0:20–0:25]
The worm circles partially beneath the sand and surges up again from a new angle, its massive head and upper body carving through the location. One ruin wall collapses, sending debris and sand down around the fighters. The Bearded Jedi dives clear. The Hooded Jedi uses a fast sidestep and roll. The Chancellor pivots away with dangerous precision, barely avoiding the jaws. Keep the worm huge in frame and unmistakably larger than every surrounding structure.


[0:25–0:30]
Final escalation. The worm rears behind the three combatants while they continue the standoff in the foreground, battered by wind and sand. The scene ends on a powerful wide action composition: the two Jedi and the Chancellor still alive and in motion on the ruined desert ground, the colossal sandworm towering behind them amid collapsing debris and swirling dust, with the conflict still unresolved and continuing beyond the cut.


CAMERA:
Single continuous unbroken shot for the full 30 seconds. High-end cinematic motion with controlled inertia and stable spatial continuity. The camera may drift, arc and reframe to preserve all three characters and the worm, but there are no cuts, jump cuts or teleporting viewpoints. Emphasize scale through parallax, dust layers, foreground debris and wide-to-medium re-framing within the same take. No random micro-shake; only motivated impact vibration during the biggest eruptions.


MOVEMENT / STAGING RULES:
The worm's motion must feel massive and heavy, displacing huge volumes of sand. Its attacks are broad environmental threats: eruptions, surges, rears, sweeping passes, partial dives and re-emergence. The three characters must remain readable, keep their identities locked, and react believably to the danger. They are not standing still while the worm performs in the background: they are actively dodging, repositioning and trying to continue their conflict in the middle of the chaos.


STYLE / LIGHTING:
Photorealistic cinematic sci-fi/fantasy. Harsh warm desert light, dry haze, blown sand, long ruin shadows, strong scale cues, natural motion blur, realistic cloth and dust interaction. Serious blockbuster tone. No comedy.


AUDIO (native):
Powerful subterranean rumble, violent sand eruption, debris crashes, heavy impacts, rushing sand, distant wind, robe movement, footsteps on sand and stone, and huge monstrous roar / throat resonance from the worm. Optional brief exertion grunts from the characters, but no dialogue and no music.


NEGATIVE PROMPT:
small worm, tiny creature, comedic monster, cartoon, anime, stylized rendering, game-render look, floating worm, worm flying in the air without sand displacement, characters ignoring the worm, static posing, identity drift, face swap, extra characters, costume changes, missing robe colors, duplicate Chancellor, duplicate Jedi, warping ruins, popping geometry, sudden scene reset, teleporting camera, hard cuts, subtitles, on-screen text, logo, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-17"></a>


## Сцена 17 — Пещера: передышка после монстра и разговор о карте


<!-- scene-meta: {"target_engine":"Seedance 2.5","production_state":"NEEDS_FIX","duration_s":30,"dialogue":{"enabled":true,"language":"ru"},"tags":["dialogue","continuous_take","continuity","needs_fix"]} -->


**Контекст использования:** Новый активный промт на основе бывшей W1; рабочий пункт W1 получил конкретные референсы и теперь оформлен как активная сцена 17. Это прямое продолжение уже существующего боя в пещере: после тяжёлой победы над чудовищем трое бойцов наконец получают короткую передышку. Отдельный active prompt бывшей сцены 9 больше не нужен. Промт рассчитан на Seedance 2.5 и специально расширен до 30 секунд, чтобы на монтаже можно было укоротить или использовать целиком как напряжённый переход к следующему блоку.


**Референсы:** @Image1 = Jedi 1 (синий туник) · @Image2 = Jedi 2 (борода, очки, зелёный меч в прошлой сцене) · @Image3 = Chancellor · @Video1 = пещера и чудовище, прямое визуальное продолжение · @Video2 = дополнительные ракурсы монстра/пещеры при необходимости continuity


**Что происходит:** Бой окончен. В тёмной влажной пещере всё ещё поднимается пар от термических ран чудовища, вода шумит, по камням стекают брызги. Трое измотаны и садятся прямо на отрубленные части тела монстра — без крови, только обугленные/прижжённые срезы, как продолжение предыдущей сцены. Несколько секунд они просто приходят в себя, тяжело дышат. Затем начинается короткий напряжённый разговор о карте: один спрашивает «Куда вы дели карту?», в ответ звучит «Зачем она тебе?». Остальное пространство сцены держится на усталости, подозрении и тяжёлой паузе после реплик.


```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on


REFERENCES:
@Image1 — PRIMARY identity reference for Jedi 1: clean-shaven man in dark blue tunic, wet and battle-worn from the previous cavern fight. Preserve face, costume and proportions exactly.
@Image2 — PRIMARY identity reference for Jedi 2: bearded man with glasses in a brown/cream Jedi robe, wet and battle-worn from the previous cavern fight. Preserve face, beard, glasses, costume and proportions exactly.
@Image3 — PRIMARY identity reference for the Chancellor: pale man in deep purple robes, exhausted after combat. Preserve face, robe silhouette and identity exactly.
@Video1 — PRIMARY continuity reference for the cavern environment and monster remains. Use it to match the wet rocks, shallow splashing water, waterfall ambience, mist, lighting and the look of the defeated pale reptilian creature.
@Video2 — supplemental continuity reference for alternate angles of the monster and cave, if needed.


REFERENCE PRIORITY:
Use @Image1, @Image2 and @Image3 as the primary character identity lock. Use @Video1 and @Video2 for environment continuity, the placement of monster remains, lighting, scale, and the post-battle mood. This scene must feel like it starts minutes — ideally seconds — after the previous monster fight ended.


SCENE OVERVIEW:
Direct continuation after the monster battle in a dark subterranean cavern. The three survivors are exhausted, breathing hard, damp from spray and combat. They sit down on severed sections of the creature's massive body, treating the grisly situation with tired practicality. The severed creature pieces show cauterized wound edges and steam, but no red liquid blood, no gore and no exposed organs. The whole scene is a tense rest beat and dialogue exchange about the map.


ACTION TIMELINE — SINGLE CONTINUOUS 30-SECOND TAKE:
[0:00–0:06]
Open on the immediate aftermath. The camera glides through the wet cavern space, revealing steam, drifting mist, splashing shallow water and the butchered remains of the giant pale reptilian monster. The three characters enter or settle into frame, visibly drained. Jedi 1 lowers himself onto a severed section of the creature. Jedi 2 sits on another chunk, leaning forward with fatigue. The Chancellor remains standing half a beat longer, then sits with controlled irritation on a third piece nearby.


[0:06–0:11]
Hold the exhausted silence. All three are catching their breath. Water drips from rock surfaces. The cavern ambience fills the space. Jedi 2 briefly wipes moisture from his face or adjusts his posture; the Chancellor looks between the others, tense and calculating. Jedi 1 stares downward for a moment, breathing hard. No one speaks yet. Let the weight of the battle settle.


[0:11–0:16]
The Chancellor finally breaks the silence. He lifts his head toward the others and asks in Russian, tired but sharp:
CHANCELLOR: «Куда вы дели карту?»
Deliver it like a pressing, irritated question asked after a brutal fight, not shouted. The others look at him.


[0:16–0:22]
A short beat follows. Jedi 1 or Jedi 2 — whichever feels clearest in the shot while maintaining character readability — answers in Russian, guarded and suspicious:
JEDI: «Зачем она тебе?»
The answer lands flat and tense. No one is amused. The line should feel like the opening move of a longer argument rather than the end of it.


[0:22–0:30]
Play the aftermath. A heavy silence hangs after the question. The Chancellor studies them, irritated but trying to stay composed. Jedi 2 shifts slightly on the monster remains, still exhausted. Jedi 1 watches the Chancellor closely. Steam continues to rise from the cauterized wounds; water continues splashing nearby. End on the unresolved tension among the three, clearly setting up a longer conversation beyond the cut.


CAMERA:
Single continuous take, slow and controlled. Begin with a gentle establishing glide across the aftermath, then settle into a readable three-character composition that can breathe. Small push-ins or subtle lateral drift are allowed, but no cuts, jump cuts or random camera shake. The motion should support tension and exhaustion, not spectacle.


PERFORMANCE:
All three men are physically drained after a hard battle. Breathing, posture and micro-expressions should communicate fatigue, soreness and suspicion. No theatrical overacting. Dialogue should be clear in Russian with natural lip sync. Preserve character identity and costume continuity throughout.


ENVIRONMENT / EFFECTS:
Dark cavern, wet rocks, shallow water, waterfalls or water runoff, lingering mist, subtle blade-burn glow residue on cauterized creature wounds, light reflecting softly off wet stone. The monster remains must clearly match the previous scene's pale reptilian beast. No gore, no blood spray, no new monster attack.


AUDIO (native):
Cavern ambience, water splashing and dripping, distant waterfall, steam hiss from cauterized wounds, tired breathing, light rustle of robes as they sit and shift, and the two Russian lines spoken clearly as written. No music.


NEGATIVE PROMPT:
new monster attack, living monster, red liquid blood, guts, gore, comedy tone, relaxed cheerful mood, standing heroic pose for the whole scene, identity drift, missing glasses on Jedi 2, costume changes, duplicate characters, distorted hands, warped creature anatomy, dry cave, bright daylight, hard cuts, shaky camera, subtitles, on-screen text, logo, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```


---


<a id="scene-19"></a>


## Сцена 19 — Рыбалка и Маша-Лагуна


<!-- scene-meta: {"target_engine":"Wan 3.0","production_state":"READY","duration_s":30,"dialogue":{"enabled":true,"language":"ru"},"tags":["dialogue","fantasy_comedy","mission_return","continuous_take"]} -->


**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**


**Контекст использования:** Новая активная 30-секундная диалоговая сцена для Wan 3.0. Сцена основана на рукописной идее Саши и затем была отдельно утверждена пользователем: Саша и Паша рыбачат у озера, из воды появляется Маша в форме Лава-Лагуны, происходит короткий эмоциональный конфликт, после чего сюжет резко возвращается к миссии и выходит в бегущий финал. Это отдельная активная slow-сцена; автоматически не перезапускать.


**Референсы:** @Image1 = стартовый кадр / композиция рыбалки · @Image2 = финальный кадр / композиция бега · @Image3 = Маша в форме «Лава-Лагуны» · @Image4 = Sasha model sheet · @Image5 = Pasha model sheet


**Что происходит:** Саша и Паша спокойно рыбачат у озера. На воде появляется странная рябь, из воды поднимается Маша в образе Лава-Лагуны, быстро подходит к Саше лицом к лицу. Саша успевает удивлённо сказать «Маша?..», после чего получает пощёчину. Маша эмоционально упрекает его: «Опять ты пропадаешь на рыбалке! Когда наконец сможешь уделять внимание мне, а не своим увлечениям?» Паша молчит, но ярко реагирует мимикой. Саша резко вспоминает про поручение — «Ой, у нас же важное поручение!» — и вместе с Пашей срывается с места. Сцена заканчивается переходом в бег и приходит к композиции @Image2.


```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

References:
@Image1 — starting shot / fishing composition reference: Sasha and Pasha sitting by the lake and fishing. Use this image for the opening composition, lakeside environment, relaxed fishing setup, and the overall mood of the first beat.
@Image2 — ending shot / running composition reference: Sasha and Pasha running away. Use this image only for the final running composition, motion direction, and ending energy.
@Image3 — design reference for Masha in the “Lava-Laguna” form. Preserve her blue aquatic fantasy appearance, facial features, silhouette, and overall design identity.
@Image4 — PRIMARY exact identity reference for Sasha. Preserve his exact face, proportions, costume, and identity throughout the whole scene.
@Image5 — PRIMARY exact identity reference for Pasha. Preserve his exact face, proportions, costume, and identity throughout the whole scene.

IMPORTANT REFERENCE RULE:
Use @Image4 and @Image5 as the PRIMARY identity references for Sasha and Pasha.
Use @Image1 only for the starting composition, fishing environment, and staging.
Use @Image2 only for the final running composition.
Use @Image3 only for Masha’s appearance, silhouette, face design, and color palette in her Lava-Laguna form.
Do not average or replace Sasha and Pasha’s identities using the fishing or running stills.

Scene:
Create a 30-second live-action fantasy-comedy scene with clear Russian dialogue, expressive facial acting, coherent geography, stable identity, and natural physical movement. The tone starts calm and slightly comedic, becomes surprising and emotional when Masha appears, and then sharply returns to mission urgency. No horror tone. No subtitles. No on-screen text.

Story flow:
Start with Sasha and Pasha sitting by the lake in the spirit of @Image1, quietly fishing in a relaxed way. The environment is bright daytime by a peaceful lake with a large fantasy city or palace-like architecture in the background, matching the atmosphere of @Image1. Fishing rods, bottles, and small fishing details may remain present if visually consistent with @Image1.

At around 0:05, strange circular ripples begin forming on the water surface. Both men notice the disturbance. The camera should clearly show that something unusual is happening in the lake.

At around 0:07–0:09, Masha in her Lava-Laguna form rises out of the water. Her emergence should feel magical, surprising, and dramatic, but not monstrous or horror-like. She is wet, elegant, otherworldly, and visually faithful to @Image3. She quickly moves toward Sasha and stops face-to-face with him on the shore.

Sasha looks shocked and says in Russian:
«Маша?..»

Immediately after this line, Masha gives Sasha a clear slap across the face. The slap must be readable and emotionally charged, but not brutal or violent. It is an offended dramatic slap, not an assault scene. Sasha visibly reacts in surprise.

Right after the slap, Masha speaks emotionally in Russian, with clear lip sync and expressive facial acting:
«Опять ты пропадаешь на рыбалке! Когда наконец сможешь уделять внимание мне, а не своим увлечениям?»

While Masha is speaking, Pasha remains silent, but his reaction must be clearly visible. He reacts with expressive facial acting: surprise, awkwardness, discomfort, and confusion. Do not give Pasha any spoken lines.

After a short stunned beat, Sasha suddenly remembers the mission and says in Russian:
«Ой, у нас же важное поручение!»

Immediately after this line, Sasha and Pasha abruptly jump up and run away. Use a dynamic but clear transition into the running ending. The final part of the scene must visually arrive at the energy and composition of @Image2: Sasha and Pasha running fast near the lakeside with urgency, as if rushing back to the mission.

Camera:
Use cinematic live-action coverage with stable motion and clean continuity. You may use natural shot progression inside the same scene: a calm medium-wide opening for the fishing setup, a lake-focused view for the ripples, a dramatic medium shot for Masha emerging, a tighter face-to-face shot for «Маша?..» and the slap, a visible reaction shot of Pasha, and then a dynamic wider motion transition into the running ending. Do not make the scene feel like random montage. All transitions should feel motivated and coherent.

Performance:
Sasha should feel distracted, caught off guard, and then suddenly alarmed when he remembers the mission. Masha should feel emotionally upset, offended, and demanding attention, but still believable and expressive rather than hysterical. Pasha should remain silent and react with strong readable facial expressions. All facial animation and lip sync must be natural.

Dialogue rules:
All spoken dialogue must be in natural Russian. Use clear Russian pronunciation and believable emotional delivery. No subtitles.

Audio:
Use natural environment sound: light wind, water movement, fishing ambience. Add clear splash and water movement when Masha emerges. The slap should have a natural audible impact. Keep spoken dialogue clearly understandable. No background music, or only extremely subtle cinematic underscore if needed, but dialogue clarity is the priority.

Style:
Photoreal live-action fantasy-comedy. Natural skin, cloth, and water simulation. Good facial consistency throughout. Readable staging. No exaggerated cartoon motion.

Negative prompt:
bad Russian lip sync, incorrect dialogue speaker, subtitles, captions, text on screen, black bars, side bars, decorative borders, identity drift, face swapping, merged faces, duplicated people, extra characters, distorted hands, extra fingers, broken slap motion, stiff facial acting, horror monster look, random teleportation, confusing geography, unstable water, broken reflections, abrupt incoherent cuts, low-detail faces, watermark, logo.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

---


<a id="scene-20"></a>


## Сцена 20 — Маша-Лагуна: рок-припев у озера

<!-- scene-meta: {"target_engine":"Seedance 2.5","production_state":"READY","duration_s":30,"dialogue":{"enabled":true,"language":"en"},"tags":["music_performance","vocal_performance","multi_part_sequence","lakeshore"]} -->

**Контекст использования:** Сцена 20 теперь оформлена как единый музыкальный номер из **11 отдельных 30-секундных генераций Seedance 2.5** — «Песня Маши 1–11». Это не 11 новых Scene ID: все части остаются внутри Scene 20 и собираются в монтаже в один клип/мюзикловый эпизод. @Image1 задаёт точную локацию берега озера, @Image2 — точный образ Маши-Лагуны. Во всех 11 частях обязателен единый continuity: одна внешность, одежда, причёска, световая логика, локация, цветокоррекция, направление движения вдоль берега и одинаковый характер камеры.

**Референсы:** @Image1 = локация / берег озера / окружение · @Image2 = Маша-Лагуна, PRIMARY exact identity reference

**Что происходит:** Маша одна исполняет у озера длинный кинематографичный рок-номер как сочетание серьёзного музыкального клипа и мюзикла. Номер начинается с тихой меланхолии, постепенно усиливается через два куплетно-припевных подъёма, выходит на эмоциональную кульминацию и заканчивается спокойным визуальным аутро у воды. Каждая часть длится 30 секунд и генерируется отдельно, но должна ощущаться продолжением одной и той же съёмки.

**Таймкоды:** это точные границы **11 монтажных генерационных блоков по 30 секунд**. Без приложенного исходного аудиофайла они не заявляются как проверенные таймкоды конкретной фонограммы; финальную подгонку слов к выбранной записи делать по waveform в монтаже. Все слова ниже взяты **дословно из текста, предоставленного пользователем в чате**, без самостоятельного исправления формулировок.

### Песня Маши 1 — 0:00–0:30 · тихое вступление и первый вокальный вход

**Музыкальный таймкод блока:** 0:00–0:30

**Точный вокальный текст этой части:**

> Another head hangs lowly,
> Child is slowly taken

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 1 (0:00–0:30 OF THE EDITED 11-PART SEQUENCE):
Тихое вступление и первый вокальный вход. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: restrained melancholy, emotional distance, the feeling that the song is only beginning.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“Another head hangs lowly,
Child is slowly taken”

TIMELINE / STORY FLOW:
[0:00–0:10]
Instrumental opening. Begin on a calm wide shot of the exact lakeshore. Masha stands alone near the water, not singing yet. She breathes naturally and looks across the lake while the camera starts a slow controlled push-in.

[0:10–0:18]
The camera reaches a medium-wide framing. Masha turns her attention gradually toward camera. Wind moves only small strands of hair and loose fabric; no exaggerated motion.

[0:18–0:30]
Masha begins singing the exact lyric segment below, sung, not spoken. Her delivery is quiet, wounded and intimate. Keep clear mouth shapes and realistic breathing; finish on a stable medium shot that can cut naturally into Part 2.

CAMERA / LENS / CONTINUITY:
Start wide and execute a slow forward dolly along the same shoreline axis, ending medium. No orbit yet. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 2 — 0:30–1:00 · первый куплет — нарастание

**Музыкальный таймкод блока:** 0:30–1:00

**Точный вокальный текст этой части:**

> And the violence caused such silence
> Who are we mistaken
> But You see it's not me, It's not my family

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 2 (0:30–1:00 OF THE EDITED 11-PART SEQUENCE):
Первый куплет — нарастание. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: melancholy becoming personal and accusatory without melodrama.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“And the violence caused such silence
Who are we mistaken
But You see it's not me, It's not my family”

TIMELINE / STORY FLOW:
[0:00–0:05]
Continue from the previous medium composition. Masha takes one slow step along the shore while keeping the lake readable behind her.

[0:05–0:24]
She sings the exact lyric segment below. The vocal becomes more direct. She alternates a distant gaze with brief eye contact toward camera; gestures remain small and natural.

[0:24–0:30]
Let the final phrase breathe. Camera makes a gentle lateral drift in the established left-to-right shoreline direction and settles for the next cut.

CAMERA / LENS / CONTINUITY:
Medium tracking shot with a subtle left-to-right move, then a mild push toward medium-close. Preserve screen direction. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 3 — 1:00–1:30 · первое напряжение перед припевом

**Музыкальный таймкод блока:** 1:00–1:30

**Точный вокальный текст этой части:**

> In your head,
> in your head they are fighting
> With their tanks, and their bombs
> And their bombs, and their guns

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 3 (1:00–1:30 OF THE EDITED 11-PART SEQUENCE):
Первое напряжение перед припевом. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: contained anger, rising urgency, still grounded and human.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“In your head,
in your head they are fighting
With their tanks, and their bombs
And their bombs, and their guns”

TIMELINE / STORY FLOW:
[0:00–0:04]
Start medium-close, matching Part 2 energy. Masha steadies her stance and inhales before the next phrase.

[0:04–0:25]
She sings the exact lyric segment below with growing force. Her jaw, breath and mouth shapes remain physically believable. On the references to fighting, tanks, bombs and guns, do not literalize the lyrics with war imagery; keep the visual world at the lake.

[0:25–0:30]
The camera begins the first gentle clockwise arc around her, building toward the chorus while keeping the shoreline geometry coherent.

CAMERA / LENS / CONTINUITY:
Controlled medium-close push plus the beginning of a slow clockwise arc; no reverse direction. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 4 — 1:30–2:00 · первый припев — эмоциональное раскрытие

**Музыкальный таймкод блока:** 1:30–2:00

**Точный вокальный текст этой части:**

> In your head,
> In your head they are cryin'
> In your head, In your head
> Zombie Zombie
> Zombie ie ie

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 4 (1:30–2:00 OF THE EDITED 11-PART SEQUENCE):
Первый припев — эмоциональное раскрытие. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: first release: grief, anger and strength breaking through together.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“In your head,
In your head they are cryin'
In your head, In your head
Zombie Zombie
Zombie ie ie”

TIMELINE / STORY FLOW:
[0:00–0:04]
Continue the clockwise arc. Masha lifts her gaze fully to camera; the emotional pressure is now visible.

[0:04–0:25]
She sings the exact lyric segment below. The repeated words receive stronger projection and sustained vowels, but the performance remains cinematic rather than theatrical. Hair and fabric move slightly more in the wind.

[0:25–0:30]
End on a strong medium-close composition with the lake still visible over one shoulder. Hold just long enough for a clean musical cut.

CAMERA / LENS / CONTINUITY:
Smooth clockwise orbit of roughly 20–30 degrees, never a full spin; combine with a restrained push-in. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 5 — 2:00–2:30 · пост-припев и вокализ

**Музыкальный таймкод блока:** 2:00–2:30

**Точный вокальный текст этой части:**

> What's in your head, in your head
> Zombie Zombie Zombie ie ie ie ou
> tu tu tu tu tu tu tu tu tu tu tu tu tu tu tu tu

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 5 (2:00–2:30 OF THE EDITED 11-PART SEQUENCE):
Пост-припев и вокализ. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: aftershock of the first chorus, haunted but temporarily less confrontational.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“What's in your head, in your head
Zombie Zombie Zombie ie ie ie ou
tu tu tu tu tu tu tu tu tu tu tu tu tu tu tu tu”

TIMELINE / STORY FLOW:
[0:00–0:04]
Start from the same side of Masha as Part 4. She releases the intensity with one breath and lets her shoulders settle.

[0:04–0:19]
She sings the exact words below with accurate lip sync; the final 'ou' opens into the vocalized section.

[0:19–0:30]
Continue the exact 'tu' vocalization rhythmically. Masha turns slightly toward the lake and walks two or three slow steps along the waterline. Keep the face visible often enough for believable vocal mouth movement.

CAMERA / LENS / CONTINUITY:
Medium tracking parallel to the shore, same left-to-right direction; slight pull-back to give more environment. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 6 — 2:30–3:00 · второй куплет — новая волна

**Музыкальный таймкод блока:** 2:30–3:00

**Точный вокальный текст этой части:**

> Another mother's breakin'
> Heart is taking over
> When the violence causes silence
> We must be mistaken

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 6 (2:30–3:00 OF THE EDITED 11-PART SEQUENCE):
Второй куплет — новая волна. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: weariness, grief and frustration returning in a deeper form.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“Another mother's breakin'
Heart is taking over
When the violence causes silence
We must be mistaken”

TIMELINE / STORY FLOW:
[0:00–0:05]
Masha slows and stops near the water. Camera settles into a medium shot from a three-quarter angle.

[0:05–0:25]
She sings the exact lyric segment below. The performance is more emotionally tired than in Part 2, as if the story is repeating. Use subtle hand tension and a brief downward glance.

[0:25–0:30]
She raises her eyes again and holds the final phrase with controlled intensity, preparing the next build.

CAMERA / LENS / CONTINUITY:
Slow diagonal dolly-in from medium to medium-close, no orbit reversal and no abrupt reframing. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 7 — 3:00–3:30 · второй подъём — историческая тяжесть

**Музыкальный таймкод блока:** 3:00–3:30

**Точный вокальный текст этой части:**

> It's the same old theme since nineteen sixteen
> In your head
> In your head they're still fightin'

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 7 (3:00–3:30 OF THE EDITED 11-PART SEQUENCE):
Второй подъём — историческая тяжесть. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: historical exhaustion turning into focused anger.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“It's the same old theme since nineteen sixteen
In your head
In your head they're still fightin'”

TIMELINE / STORY FLOW:
[0:00–0:05]
Hold a quiet medium-close for one breath. Masha is nearly still except for natural breathing and wind.

[0:05–0:23]
She sings the exact lyric segment below. Emphasize the weight of 'nineteen sixteen' through acting only; do not insert text, dates, archival footage or literal battlefield visions.

[0:23–0:30]
Camera resumes the established clockwise arc very gently. Her gaze becomes firmer as the second chorus approaches.

CAMERA / LENS / CONTINUITY:
Minimal movement at first, then continue the same clockwise arc established earlier; keep horizon stable. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 8 — 3:30–4:00 · второй пред-припев — максимум напряжения

**Музыкальный таймкод блока:** 3:30–4:00

**Точный вокальный текст этой части:**

> With their tanks, and their bombs
> And their bombs, and their guns
> In your head In your head
> they are dying

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 8 (3:30–4:00 OF THE EDITED 11-PART SEQUENCE):
Второй пред-припев — максимум напряжения. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: the most compressed tension before the final vocal release.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“With their tanks, and their bombs
And their bombs, and their guns
In your head In your head
they are dying”

TIMELINE / STORY FLOW:
[0:00–0:04]
Begin already in a tense medium-close. Masha takes a visible but natural breath.

[0:04–0:24]
She sings the exact lyric segment below with stronger projection. Keep her grounded at the lake; do not create tanks, bombs, guns, explosions or battle imagery.

[0:24–0:30]
She steps half a pace toward camera and ends on direct eye contact, ready for the chorus.

CAMERA / LENS / CONTINUITY:
Slow push-in layered over the clockwise drift; stop before extreme close-up so lip sync and environment remain readable. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 9 — 4:00–4:30 · финальный припев — первая половина

**Музыкальный таймкод блока:** 4:00–4:30

**Точный вокальный текст этой части:**

> In your head, in your head
> Zombie Zombie
> Zombie ie ie

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 9 (4:00–4:30 OF THE EDITED 11-PART SEQUENCE):
Финальный припев — первая половина. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: full rock-performance release, wounded but defiant.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“In your head, in your head
Zombie Zombie
Zombie ie ie”

TIMELINE / STORY FLOW:
[0:00–0:03]
Masha holds direct eye contact as the chorus hits.

[0:03–0:24]
She sings the exact lyric segment below powerfully, sung not shouted. Sustained vowels are visible in realistic mouth shapes; chest and shoulder breathing are physically plausible.

[0:24–0:30]
Camera eases outward by a small amount, revealing more lake while keeping her dominant in frame.

CAMERA / LENS / CONTINUITY:
Strong medium-close with a controlled micro-orbit clockwise, then a small dolly-out for scale. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 10 — 4:30–5:00 · финальный припев — кульминация

**Музыкальный таймкод блока:** 4:30–5:00

**Точный вокальный текст этой части:**

> What's in your head, in your head
> Zombie Zombie Zombie
> ie ie ie

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 10 (4:30–5:00 OF THE EDITED 11-PART SEQUENCE):
Финальный припев — кульминация. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: maximum intensity: grief, anger, vulnerability and strength together.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“What's in your head, in your head
Zombie Zombie Zombie
ie ie ie”

TIMELINE / STORY FLOW:
[0:00–0:04]
Continue from Part 9 with the same screen direction and visual intensity.

[0:04–0:24]
Masha sings the exact lyric segment below at the emotional peak of the sequence. A small opening of the arms or one forward step is allowed, but no stage choreography.

[0:24–0:30]
The camera completes the strongest but still smooth portion of the clockwise arc and opens to a heroic medium-wide composition against the lake.

CAMERA / LENS / CONTINUITY:
Controlled clockwise arc plus gentle widening; cinematic inertia, stable horizon, no fast spin. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### Песня Маши 11 — 5:00–5:30 · финальный вокализ и визуальный аутро

**Музыкальный таймкод блока:** 5:00–5:30

**Точный вокальный текст этой части:**

> ou ou ou ou ou ou ou ou
> yea

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, horizon, surrounding landscape, background geography, natural color relationships and spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette and identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna. @Image1 controls only environment and geography. Do not average the character with the location reference. Do not redesign, beautify, age-shift or restyle Masha. Do not change her wardrobe between parts. Do not redesign the lake or invent large structures absent from @Image1.

SEQUENCE CONTINUITY LOCK — APPLIES TO ALL 11 PARTS:
This is one continuous music-video sequence assembled from eleven separately generated 30-second clips. Every part must feel photographed on the same day in the same place with the same actress. Keep identical Masha identity, costume, hairstyle, makeup, body proportions, lake geography, weather family, natural color grade and lens character. Preserve the established shoreline screen direction: lateral movement stays left-to-right. Whenever the camera arcs around Masha, continue the same slow clockwise direction; never reverse into a random counter-orbit. Each part is internally continuous and must finish in a composition that can cut naturally into the next part. No unexplained time-of-day jump, costume change, wet/dry reset, new props, new people or environment redesign.

STYLE GOAL:
Photorealistic live-action cinematic alternative-rock music video at a real lakeshore. Serious, melancholic, raw and intimate, with emotionally controlled performance and understated 1990s rock-video texture, but without naming or visually imitating a specific artist, band, music video or recording. No glossy pop staging. No stage show. No fantasy set. The lake and Masha remain the visual anchors.

SCENE — MASHA SONG PART 11 (5:00–5:30 OF THE EDITED 11-PART SEQUENCE):
Финальный вокализ и визуальный аутро. Masha-Laguna remains alone at the exact lakeshore from @Image1. The scene must work as a standalone 30-second clip and as a direct continuation of the previous part. Emotional target: silence after the emotional storm; exhausted, sad, released.

DIALOGUE / VOCALS / LIP SYNC:
Language: English. Masha-Laguna is the only singer. The following user-provided words are sung, not spoken. Sing exactly these words in exactly this order. Do not paraphrase, correct, substitute, add or omit lyric words. Natural English pronunciation, realistic phrasing, visible inhalations, believable jaw / lips / tongue motion and accurate sung lip sync. No subtitles or on-screen lyrics.

EXACT LYRICS FOR THIS 30-SECOND PART:
“ou ou ou ou ou ou ou ou
yea”

TIMELINE / STORY FLOW:
[0:00–0:06]
Masha sings the exact final vocalization and 'yea' below. The delivery is exhausted but still musical and clear.

[0:06–0:14]
Her mouth closes naturally after the last sound. She exhales, lowers her gaze slightly and lets the performance fall into silence.

[0:14–0:24]
She turns toward the lake without changing identity, costume or location. The camera begins a slow pull-back.

[0:24–0:30]
Finish on a wide, quiet lakeshore composition. Masha remains small but clearly recognizable. No fade, no title card, no text; leave a clean visual tail for editing.

CAMERA / LENS / CONTINUITY:
Start medium, then slow stable pull-back to wide along the same axis; no new orbit direction. Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia. Preserve one coherent 3D space. Shoreline, water, horizon and distant objects stay geometrically stable. No random jitter, micro-shake, teleporting camera, hard cut or jump cut inside the 30-second clip. Use natural 35–50mm-equivalent perspective unless a closer portrait moment is explicitly required; avoid extreme wide-angle facial distortion.

PERFORMANCE / ACTING:
Masha performs the song seriously and truthfully, never as parody. Use natural blinking, breathing, eye focus, facial micro-expressions, neck/jaw motion and subtle weight transfer. Emotion can intensify, but avoid hysterical overacting. Gestures must remain motivated and small enough to preserve a believable film performance. Maintain exact identity, hairstyle, costume and proportions in every frame.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve natural outdoor light consistent with @Image1. Keep the same weather family and color grade across the sequence. Realistic skin texture, cloth weave, wind response, natural motion blur, believable water reflections and physically plausible depth of field. Water has small natural ripples; shoreline material and distant background do not morph. No concert lighting, neon wash, fantasy glow or magical aura unless intrinsically present in the approved Masha design.

AUDIO (native):
Clear expressive female lead vocal, exact English lyric segment above, sung rather than spoken, with tight lip sync. Use a melancholic alternative-rock backing built from electric guitar, bass and drums with a steady cinematic pulse. Do not imitate or reproduce a specific existing recording, singer or melody; the generated backing is only a timing/performance guide and may be replaced by the user's chosen track in final editing. Keep soft lake ambience underneath: water, light wind and distant outdoor atmosphere. No crowd, applause, spoken dialogue or competing vocals.

NEGATIVE PROMPT:
identity drift, different face, age shift, hairstyle change, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, invented extra lyrics, omitted required words, reordered lyrics, subtitles, captions, karaoke text, lyrics on screen, title cards, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, literal tanks, bombs, guns, explosions or battlefield visions, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, hard cuts inside the clip, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```
