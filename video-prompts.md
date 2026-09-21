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








**Синхронизация контекста:** **21.09.2026**. Точное техническое время зеркала хранится в `project-status.json` и здесь не дублируется. Фактическая карта — `film-analysis.md`, статусы и зависимости — `film-backlog.md`. Новые решения пользователя имеют приоритет над старым Notion. В active master остаются 12 актуальных сцен и 24 полных текста промтов. Сцены 6, 7, 9, 12, 14, 15 и 18 удалены из active master по прямому решению пользователя как уже отработанные/больше не актуальные; их Scene ID остаются зарезервированы и не переиспользуются. Canonical slow-list сейчас: **2, 3, 4, 5, 13, 19**. Сцены 3, 4, 5 и 13 были повторно запущены в Topview и привязаны к существующим Scene ID, поэтому новые Scene ID для этих задач не создаются. Сцена 20 «Маша-Лагуна: рок-припев у озера» остаётся READY и не slow. Никакие старые промты Notion сюда автоматически не добавлены. Непрерывный аудиовизуальный контроль не выполнялся.








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
| 20 | [Маша-Лагуна — рок-припев у озера](#scene-20) | @Image1 = локация/берег озера; @Image2 = Маша-Лагуна | Полный музыкальный номер разбит на 11 взаимосвязанных 30-секундных Seedance 2.5 фрагментов «Песня Маши 1–11» с точным пользовательским вокальным текстом, единым образом Маши, одной локацией и кинематографичной эскалацией от вступления к финальному аутро. |








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
 

REFERENCE PRIORITY / IDENTITY LOCK:
@Image2 is the absolute identity authority for HAN. @Image3 is the absolute identity authority for THE JEDI. @Image1 controls the cantina composition, Chewbacca, table placement, background atmosphere and lighting only.
Do not average Han or the Jedi with faces visible in @Image1. Keep all three characters in their established seats/positions and preserve costume, face, hair, body proportions and left-right geography throughout.

START / END STATE:
Start as an already-established conversation at the same table, with the Jedi focused on Han and Chewbacca present as a silent witness.
End with Chewbacca's questioning growl and the Jedi visibly thrown off, while Han remains committed to playing dumb. Preserve this exact emotional and spatial state for Scene 11.

CAMERA / CONTINUITY:
Use motivated cinematic dialogue coverage only: readable medium three-shot for geography, then restrained singles/reaction shots that preserve eyelines and screen direction.
No arbitrary side swaps, no 180-degree axis break, no teleporting between seats, no random montage, and no camera move that obscures the speaking face during a line.
Keep camera motion physically stable with controlled inertia; subtle dolly or locked-off coverage is preferred over handheld movement.

PERFORMANCE / LIP SYNC:
All Russian dialogue must be spoken exactly by the assigned character with natural Russian pronunciation, no accent unless present in the reference performance, and accurate lip sync.
Jedi is serious and increasingly puzzled; Han performs believable faux innocence rather than broad comedy; Chewbacca reacts only through natural head/eye/body motion and Wookiee vocalization.
Allow natural blinking, breathing, small posture shifts and reaction pauses. Do not overlap key dialogue lines.

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
 
NEGATIVE PROMPT: identity drift, face averaging, face swapping, costume drift, seat swapping, broken eyelines, 180-degree axis flip, random camera cuts, rushed dialogue, overlapping speech, wrong speaker, bad Russian pronunciation, lip desync, Wookiee speaking actual words, subtitles, captions, text on screen, duplicated characters, extra foreground characters, distorted hands, expressionless faces, exaggerated slapstick acting, warped table or cantina geometry, camera jitter, cartoon, anime, game-render look, plastic skin, low-detail faces, watermark, logo, unwanted non-diegetic music.




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
 

REFERENCE PRIORITY / IDENTITY LOCK:
@Image2 is the absolute identity authority for HAN. @Image3 is the absolute identity authority for THE JEDI. @Image1 controls Chewbacca, the cantina composition, table placement, background atmosphere and lighting only.
Do not average Han or the Jedi with faces visible in @Image1. Preserve the same costumes, seats, left-right geography, table layout, eyelines and lighting established in Scene 10.

CONTINUITY FROM SCENE 10 / START STATE:
This begins immediately after Chewbacca's questioning growl at the end of Scene 10. No time skip, no reset of posture, no new entrance and no changed seating.
The Jedi is still thrown off but tries to recover; Han is still playing dumb; Chewbacca is attentive after his previous growl.

END STATE:
End on Han's baffled close reaction after «Какую плёнку? Мужик, ты вообще кто?» with the Jedi and Chewbacca remaining in the same established space, leaving a clean reaction beat for the next edit.

CAMERA / CONTINUITY:
Maintain the same dialogue axis and screen direction as Scene 10. Use restrained motivated coverage: medium shot, reaction shot, then close framing only when it serves the line.
No arbitrary side swaps, no 180-degree axis break, no teleporting between seats, no random montage, and no camera movement that hides the active speaker's mouth.
Physically stable cinematic motion with controlled inertia; subtle dolly or locked-off coverage is preferred.

PERFORMANCE / LIP SYNC:
All Russian dialogue must be spoken exactly by the assigned character with natural Russian pronunciation and accurate lip sync.
The Jedi delivers the crude joke dryly rather than theatrically, then shifts back to business. Chewbacca's offended reaction is readable but still physically natural. Han's final confusion feels genuine and increasingly exasperated.
Allow natural blinking, breathing, restrained gestures and short reaction pauses. Do not overlap key lines.

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
 
NEGATIVE PROMPT: identity drift, face averaging, face swapping, costume drift, changed seating, broken eyelines, 180-degree axis flip, time-skip look, random camera cuts, rushed dialogue, overlapping speech, wrong speaker, bad Russian pronunciation, lip desync, Wookiee speaking actual words, subtitles, captions, text on screen, duplicated characters, extra foreground characters, distorted hands, expressionless faces, exaggerated slapstick acting, warped table or cantina geometry, camera jitter, cartoon, anime, game-render look, plastic skin, low-detail faces, watermark, logo, unwanted non-diegetic music.




FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```








---








<a id="scene-13"></a>








## Сцена 13 — Совет джедаев: говорящий кот








<!-- scene-meta: {"target_engine":"Wan 3","production_state":"NEEDS_FIX","duration_s":30,"dialogue":{"enabled":true,"language":"ru"},"tags":["dialogue","comedy","continuous_take","needs_fix"]} -->








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

<!-- scene-meta: {"target_engine":"Wan 3","production_state":"READY","duration_s":30,"dialogue":{"enabled":true,"language":"ru"},"tags":["dialogue","continuous_take","continuity","deadpan_comedy","map"]} -->

**Контекст использования:** Прямое продолжение уже существующего боя в пещере. Главная комедийная конструкция сцены — трое совершенно серьёзно и буднично разговаривают после тяжёлого боя, при этом всё это время сидят на трёх крупных отрубленных частях тела только что побеждённого монстра. Персонажи не считают ситуацию смешной и никак специально её не комментируют: юмор возникает только из абсурдного визуального контраста. Серёга вспоминает старые времена, спрашивает о карте; Паша сначала не понимает, зачем она ему, затем Серёга тихо говорит Паше что-то на ухо, после чего Паша без колебаний отдаёт карту Серёге. Содержание шёпота не раскрывается.

**Референсы:** @Image1 = Паша / Jedi 1, тёмно-синий туник · @Image2 = Саша / Jedi 2, борода и очки · @Image3 = Серёга / Канцлер, глубокая тёмно-фиолетовая мантия · @Image4 = фото локации пещеры, точный environment reference · @Image5 = фото карты, точный prop reference · @Video1 = пещера, чудовище и прямое визуальное продолжение предыдущего боя · @Video2 = дополнительные ракурсы монстра/пещеры при необходимости continuity

**Что происходит:** Бой окончен. В тёмной влажной пещере трое измотанных героев сидят каждый на отдельной массивной отрубленной части тела чудовища с прижжёнными срезами без крови и органов. Несколько секунд они молча приходят в себя. Серёга с усталой ностальгией говорит: «Как в старые добрые времена. Куда вы дели карту?» Паша отвечает: «Да зачем она вообще тебе?» Серёга наклоняется и тихо шепчет Паше что-то на ухо — слов зритель не слышит. Паша сразу, совершенно без раздумий и без дальнейших вопросов, достаёт карту и отдаёт её Серёге. Саша наблюдает за этим с усталой сдержанной реакцией. Все продолжают сидеть на частях монстра, будто это самое обычное место для разговора.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — PRIMARY exact identity reference for PASHA / Jedi 1: clean-shaven man in a dark navy-blue Jedi tunic, wet and battle-worn from the previous cavern fight. Preserve his exact face, age, hairstyle, costume, body proportions and identity.
@Image2 — PRIMARY exact identity reference for SASHA / Jedi 2: bearded man with glasses in a brown-and-cream Jedi robe, wet and battle-worn from the previous cavern fight. Preserve his exact face, beard, glasses, hairstyle, costume, body proportions and identity.
@Image3 — PRIMARY exact identity reference for SEREGA / the Chancellor: pale man in a long deep dark-purple robe, exhausted after combat. Preserve his exact face, hairstyle, robe silhouette, proportions and identity.
@Video1 — PRIMARY continuity reference for the cavern environment, defeated monster remains and immediate post-battle geography. Match the wet rocks, shallow splashing water, waterfall ambience, mist, lighting, scale and the pale reptilian creature.
@Video2 — supplemental continuity reference for alternate angles of the same monster and cavern only.

REFERENCE PRIORITY / IDENTITY LOCK:
@Image1, @Image2 and @Image3 are the absolute identity and costume authority for Pasha, Sasha and Serega. @Image4 is the exact location/environment authority. @Image5 is the exact map-prop authority. @Video1 and @Video2 provide motion, monster anatomy and immediate post-battle continuity. Environment references must never override or average the three character identities, and the map must not be redesigned from the video references. Keep all three men visually distinct and stable for the entire take.

COMEDY / TONE LOCK:
The comedy is entirely deadpan and situational. The central visual joke is that three exhausted men conduct a serious, almost ordinary conversation while each of them is sitting on a different severed body section of the monster they have just defeated. They do NOT laugh, grin, wink at the camera, make jokes about the body parts, act goofy, or acknowledge how absurd the seating is. Play the dialogue sincerely and naturally. The stranger and more matter-of-fact their behavior feels against the bizarre seating arrangement, the better the comedy works.

START STATE:
The battle has just ended. The same cavern, monster, wet clothing, lighting and physical aftermath continue directly from the preceding footage. Three large separated sections of the defeated creature are already lying naturally in the cavern. Their cut surfaces are fully cauterized and darkened, with faint steam but no liquid blood, exposed organs or graphic gore. Pasha, Sasha and Serega are exhausted and remain close together in one readable conversational area.

SCENE OVERVIEW:
Direct continuation after the monster battle in a dark subterranean cavern. Pasha, Sasha and Serega settle onto three separate large severed sections of the defeated pale reptilian creature as improvised seats. They stay seated there through the conversation. Serega nostalgically remarks that it feels like old times, asks where the map is, and Pasha questions why he needs it. Serega then leans close and whispers something privately into Pasha's ear. The whisper content is deliberately inaudible and never revealed. Immediately afterward Pasha gives Serega the map without hesitation, argument or explanation. Sasha witnesses the strange exchange with restrained exhausted curiosity.

ACTION TIMELINE — SINGLE CONTINUOUS 30-SECOND TAKE:
[0:00–0:05]
Open in the immediate aftermath of the fight. A slow controlled camera glide reveals the wet cavern, drifting mist, shallow water, steam and the defeated monster's massive separated body sections. Reveal Pasha, Sasha and Serega already lowering themselves onto or settling on three different monster sections. Make the bizarre improvised seating visually unmistakable without framing it as a gag. They are simply exhausted and need somewhere to sit.

[0:05–0:10]
Hold a quiet recovery beat. All three remain seated on the monster pieces, breathing heavily. Pasha leans forward slightly from fatigue. Sasha adjusts his posture and glasses. Serega looks from one old companion to the other. Nobody comments on what they are sitting on. Their complete seriousness is essential.

[0:10–0:16]
Serega looks at Pasha and Sasha with a faint trace of tired nostalgia, not a smile, and says clearly in natural Russian:
SEREGA: «Как в старые добрые времена. Куда вы дели карту?»
He delivers both sentences as one natural thought: first a weary recollection, then a direct practical question. Pasha and Sasha look toward him.

[0:16–0:20]
Pasha answers Serega directly, guarded and genuinely puzzled, in natural Russian:
PASHA: «Да зачем она вообще тебе?»
No one else speaks over him. Accurate Russian lip sync. Sasha remains silent and watches.

[0:20–0:24]
Serega calmly leans sideways toward Pasha without standing up and whispers something very quietly into Pasha's ear. The actual words must NOT be intelligible to the audience: only a soft indistinct whisper/murmur is heard. Do not invent audible dialogue, subtitles or captions. Sasha notices the whisper and watches them with restrained curiosity.

[0:24–0:28]
The instant Serega finishes whispering, Pasha reacts with a tiny matter-of-fact acknowledgement and, without hesitation, without asking another question and without looking conflicted, takes out the map and hands it directly to Serega. The handoff must be clear and physically readable: one map, Pasha releases it, Serega receives it securely. No Force pull, no magical levitation, no struggle.

[0:28–0:30]
Serega looks down at the map in his hand with quiet satisfaction while remaining seated on the monster section. Pasha settles back as if the matter is completely resolved. Sasha gives them a brief tired, slightly puzzled look but says nothing. End with all three still seated on the grotesquely inappropriate monster-body seats, preserving the deadpan visual joke and setting up the next story beat.

CAMERA / CONTINUITY:
One physically stable continuous take. Begin with a gentle low-to-medium establishing glide that clearly reveals all three separate monster-body seats and the cavern geography, then settle into a readable three-shot. During dialogue use only a subtle controlled push-in and small lateral adjustment so the speaker and listener remain readable without cuts. For the whisper, allow a modest natural move closer to Serega and Pasha while Sasha remains visible or spatially understandable. For the map handoff, frame both hands clearly without turning the scene into an insert shot. No cuts, jump cuts, teleporting camera, random orbiting or micro-shake. Maintain coherent left/right screen positions and the same cavern axis throughout.

PERFORMANCE:
All three are genuinely exhausted after a brutal fight: heavy breathing, sore posture, damp clothes, restrained movements and small natural facial reactions. Play everything straight. Serega is calm, tired, slightly nostalgic and purposeful. Pasha is initially suspicious/puzzled, then after the whisper changes instantly to uncomplicated cooperation and hands over the map as though the whispered explanation completely settles the issue. Sasha remains a silent observer with a restrained "what was that?" reaction, never broad or cartoonish. No theatrical comedy acting.

DIALOGUE / LIP SYNC:
Spoken language: Russian, natural native pronunciation, no foreign accent.
Only these two public lines are audible:
SEREGA: «Как в старые добрые времена. Куда вы дели карту?»
PASHA: «Да зачем она вообще тебе?»
Then Serega whispers privately into Pasha's ear. The whisper must remain unintelligible; do not generate additional understandable words. Accurate lip sync for the two audible lines. No subtitles, captions or on-screen text.

MAP PROP / HANDOFF:
Use the exact physical map from @Image5. Preserve its recognizable design, proportions, material and markings; do not redesign, simplify or substitute it. It must not appear from nowhere: Pasha retrieves it naturally from his clothing, belt pouch or an already plausible carried place. Keep the same prop shape throughout the handoff. Pasha physically gives it to Serega. Serega ends the scene holding the map. No duplicate map, no disappearing prop, no morphing object.

ENVIRONMENT / MATERIAL REALISM:
Dark wet cavern, slick rock, shallow water, runoff or distant waterfall, lingering mist and subtle steam from cauterized monster wounds. Soft reflected light on wet stone and damp fabric. The defeated creature remains must clearly belong to the same massive pale reptilian monster from the previous fight. Body sections have sealed, charred/cauterized cut surfaces only — no liquid red blood, no exposed organs, no graphic gore. Preserve believable weight: the monster sections compress or support the seated characters naturally and do not wobble like rubber.

AUDIO (native):
Natural cavern ambience, dripping and splashing water, distant waterfall, faint steam hiss, tired breathing and subtle robe movement. The two Russian lines are clear and foregrounded. During the private whisper, lower the voice to an indistinct close murmur that the audience cannot decipher. No music. No comedic sting or sound effect when Pasha hands over the map.

NEGATIVE PROMPT:
wrong speaker, Sasha speaking either dialogue line, Pasha saying Serega's line, Serega saying Pasha's line, intelligible whispered words, invented extra dialogue, subtitles, captions, on-screen text, characters laughing or smiling at the situation, slapstick acting, exaggerated comedy faces, characters commenting on the monster seats, anyone standing up during the core conversation, ordinary chairs or rocks replacing the monster-body seats, characters sitting on the same body section, living monster, new monster attack, red liquid blood, blood spray, exposed organs, graphic gore, duplicate characters, missing character, identity drift, face swapping, missing Sasha's glasses, costume changes, map appearing from nowhere, duplicate map, map levitation, Force pull, refusal or hesitation after the whisper, broken hand interaction, extra fingers, warped anatomy, dry cave, bright daylight, random camera shake, micro-jitter, hard cuts, jump cuts, cartoon look, glossy video-game render, logo, watermark.

END STATE:
Serega is seated and clearly holds the map. Pasha has willingly surrendered it and remains seated. Sasha remains seated and silently observes. All three are still resting on separate severed monster sections in the same cavern, ready for a clean continuation into the next story beat.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
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

<!-- scene-meta: {"target_engine":"Seedance 2.5","production_state":"READY","duration_s":30,"dialogue":{"enabled":true,"language":"en"},"tags":["music_performance","vocal_performance","11_part_sequence","lakeshore","cinematic_music_video","musical"]} -->

**Контекст использования:** Полный музыкальный номер Маши-Лагуны разбит на **11 самостоятельных 30-секундных генераций Seedance 2.5**, которые затем собираются в единый клип / музыкальную сцену. Это не 11 новых Scene ID: весь номер остаётся **Scene 20**. @Image1 задаёт точный берег озера, @Image2 — точную identity Маши-Лагуны. Все части используют одинаковую внешность, одежду, причёску, локацию, погоду, световую логику и цветокоррекцию. Вокальный текст внутри prompts взят **только из текста, напрямую предоставленного пользователем**, и должен исполняться дословно с sung lip sync.

**Референсы:** @Image1 = LOCATION / берег озера / окружение · @Image2 = MASHA-LAGUNA / PRIMARY exact identity reference

**Режиссёрская формула всей Scene 20:** основа всегда — берег озера; Маша почти всё время остаётся в кадре и является эмоциональным центром. Клип не должен быть статичным: по ходу номера она то стоит, то медленно идёт вдоль воды, то поворачивается к камере, то смотрит вдаль, то поёт прямо в объектив. Камера сознательно чередует **wide establishing shot, slow dolly-in, side tracking, gentle orbit / partial orbit, backward tracking, medium performance framing, expressive close-up и slow final pull-back**. Общая эстетика — **меланхоличный, драматичный и красивый cinematic music video, соединённый с эмоциональной ясностью мюзикла**. Никакой концертной сцены, танцоров, случайного клипового хаоса или одиннадцати одинаковых статичных кадров.

**Что происходит:** номер развивается как единая драматургическая дуга: тихое одиночное вступление → нарастающее внутреннее напряжение → первый припевный выброс → музыкальная передышка с движением вдоль воды → более тяжёлый второй куплет → финальное нарастание → главный эмоциональный пик → спокойный широкий аутро. Каждая часть — один устойчивый 30-секундный кинематографичный фрагмент; монтаж между частями формирует единый клип.

**Монтажная сетка / camera-blocking map:**

| Часть | Музыкальный диапазон | Драматургия | Маша / камера |
|---:|---:|---|---|
| 1 | 0:00–0:30 | вступление и начало первого куплета | стоит → slow dolly-in → medium |
| 2 | 0:30–1:00 | первый куплет — движение вдоль воды | медленно идёт вдоль воды → боковой tracking |
| 3 | 1:00–1:30 | первый куплет — война в голове | стоит / поворот плеч → gentle orbit |
| 4 | 1:30–2:00 | первый припев — первый эмоциональный выброс | шаг к камере → dolly-in → close-up |
| 5 | 2:00–2:30 | первый припев — кульминация и вопрос | пол-оборота к озеру и обратно → half-orbit |
| 6 | 2:30–3:00 | вокализ / инструментальная передышка | идёт вдоль воды → wide side tracking |
| 7 | 3:00–3:30 | второй куплет — новая волна | 1–2 шага к воде → diagonal dolly-in |
| 8 | 3:30–4:00 | второй куплет — историческая тема и нарастание | почти стоит → поворот к камере → near-frontal orbit |
| 9 | 4:00–4:30 | финальный подъём — война продолжается | идёт к камере по диагонали → backward tracking |
| 10 | 4:30–5:00 | финальный припев — вершина | почти стоит, максимум эмоции → close-up + partial orbit |
| 11 | 5:00–5:30 | финальный вокализ и визуальный аутро | остаётся у воды → slow pull-back → wide outro |

**Важно о таймингах:** интервалы 0:00–5:30 — рабочая сетка 11 генерационных блоков по 30 секунд. Порядок вокального текста фиксирован. Если фактический аудиотрек имеет иные внутренние длительности пауз/инструментальных мест, финальная синхронизация выполняется по реальной waveform в монтаже без изменения порядка слов.

### GLOBAL DIRECTING BIBLE — Scene 20

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.



### CHARACTER APPEARANCE / IDENTITY LOCK — MASHA-LAGUNA

This appearance lock applies unchanged to **all 11 parts** of Scene 20.

- **@Image2 is the absolute visual authority for Masha-Laguna.** If any written description conflicts with @Image2, follow @Image2.
- Masha-Laguna is an adult woman with a smooth pale aquatic-blue complexion and a human feminine face with soft, balanced features.
- Her silhouette is tall, slender and elegant. Preserve the exact body proportions and overall figure from @Image2.
- Instead of ordinary human hair, she has long, thick, light-blue tentacle-like head strands descending along both sides and behind the head. Preserve their number, placement, length, thickness and natural movement as closely as the reference allows.
- A glossy black organic ornamental structure frames the crown / upper head and continues into a high black neck-chest collar with a matching elongated decorative element over the upper back. Preserve this black ornamentation as part of the approved design.
- Her main body silhouette is a sleek, floor-length, form-fitting light-blue gown-like / aquatic fantasy design matching @Image2. Preserve the exact approved design rather than inventing a new costume.
- Keep the same face, blue skin tone, head shape, head strands, black ornamental elements, body proportions and silhouette in every shot and every camera angle.
- Do not replace the head strands with ordinary hair, do not add a mermaid tail, fins, horns or extra tentacles, do not redesign the black ornamentation, do not change skin color, and do not turn her into a monster or a different fantasy species.
- Wide shots, profile views, side tracking, orbit shots and close-ups must all preserve the same identity and design. Natural motion, wind and body movement are allowed; design drift is not.

### Песня Маши 1 — вступление и начало первого куплета

**Музыкальный таймкод:** 0:00–0:30

**Функция фрагмента:** Открыть весь музыкальный номер: сначала озеро и одиночество Маши, затем первое очень личное вокальное вступление.

**Пластика Маши:** Маша начинает почти неподвижно у самой воды. После первого вдоха медленно переводит взгляд с озера к камере, но ещё не идёт.

**Камера:** Start in a wide establishing shot that clearly shows Masha and the lake, then perform one very slow controlled dolly-in toward a medium-wide / medium framing. No orbit yet.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 1 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 1 / GLOBAL MUSIC TIMECODE 0:00–0:30:
Open the full musical number with the lake and Masha's solitude, then move into the first deeply personal vocal entrance.
BLOCKING / PHYSICAL ACTION:
Masha begins almost motionless at the water's edge. After the first breath, she slowly shifts her gaze from the lake toward the camera, but does not walk yet.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

Another head hangs lowly,
Child is slowly taken

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:06]
Wide establishing image of the exact lakeshore. Masha is already present near the water, almost still. One natural preparatory breath; wind moves only loose hair and fabric.
[0:06–0:15]
Sing the first exact lyric line. Masha looks mostly toward the distance across the lake, not directly at camera.
[0:15–0:24]
Sing the second exact lyric line. Her gaze slowly returns toward camera; emotion becomes more personal.
[0:24–0:30]
No new words. Let the final syllable resolve naturally into the music while the dolly-in settles into a clean medium composition.

CAMERA / LENS / CONTINUITY:
Start in a wide establishing shot that clearly shows Masha and the lake, then perform one very slow controlled dolly-in toward a medium-wide / medium framing. No orbit yet.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
quiet melancholy, contained grief, intimate vulnerability.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 2.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 2 — первый куплет — движение вдоль воды

**Музыкальный таймкод:** 0:30–1:00

**Функция фрагмента:** Сделать номер визуально живым: Маша начинает медленно идти вдоль воды и впервые вступает с камерой в более прямой эмоциональный контакт.

**Пластика Маши:** Два-три медленных шага параллельно береговой линии; короткий взгляд в камеру, затем снова вдаль; к концу она останавливается и разворачивает корпус к объективу.

**Камера:** A smooth side-tracking move parallel to the shoreline, gradually curving only slightly toward a three-quarter front view. End in medium framing.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 2 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 2 / GLOBAL MUSIC TIMECODE 0:30–1:00:
Make the performance visually more alive: Masha begins walking slowly along the water and establishes a more direct emotional connection with the camera for the first time.
BLOCKING / PHYSICAL ACTION:
She takes two or three slow steps parallel to the shoreline, gives the camera a brief look, then looks into the distance again; by the end she stops and turns her torso toward the lens.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

And the violence caused such silence
Who are we mistaken
But You see it's not me,
It's not my family

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:07]
Sing the first exact line while beginning a slow walk along the waterline.
[0:07–0:13]
Sing the second exact line. Briefly slow the walk so the question lands.
[0:13–0:20]
Sing the third exact line. Masha looks directly toward camera for the first time with more intensity.
[0:20–0:27]
Sing the fourth exact line. She stops and turns her upper body slightly more toward camera.
[0:27–0:30]
No new words. Hold the breath and expression as a transition into the next part.

CAMERA / LENS / CONTINUITY:
A smooth side-tracking move parallel to the shoreline, gradually curving only slightly toward a three-quarter front view. End in medium framing.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
growing tension, restrained pain, questioning.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 3.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 3 — первый куплет — война в голове

**Музыкальный таймкод:** 1:00–1:30

**Функция фрагмента:** Перевести песню из личной печали в более масштабное, тревожное высказывание и впервые использовать мягкое круговое движение камеры.

**Пластика Маши:** Маша остаётся на месте, но тело становится выразительнее: небольшой поворот плеч, сдержанный жест рукой, взгляд то в объектив, то поверх камеры.

**Камера:** Begin medium. Use a gentle partial orbit around Masha, never faster than a slow walking pace, moving toward medium-close framing by the end.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 3 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 3 / GLOBAL MUSIC TIMECODE 1:00–1:30:
Shift the song from personal sadness into a broader, more unsettling statement and introduce the first gentle orbiting camera move.
BLOCKING / PHYSICAL ACTION:
Masha remains in place, but her body language becomes more expressive: a slight shoulder turn, one restrained hand gesture, and a gaze alternating between the lens and just beyond the camera.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

In your head,
in your head they are fighting
With their tanks, and their bombs
And their bombs, and their guns

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:05]
Sing exactly “In your head,” in a controlled medium shot.
[0:05–0:12]
Sing the second exact line as the slow orbit begins.
[0:12–0:20]
Sing the third exact line. Her face becomes more focused; one small motivated hand gesture is allowed.
[0:20–0:27]
Sing the fourth exact line. Orbit continues smoothly, keeping the lake readable behind her.
[0:27–0:30]
No new words. Hold the final expression while the camera finishes the partial arc.

CAMERA / LENS / CONTINUITY:
Begin medium. Use a gentle partial orbit around Masha, never faster than a slow walking pace, moving toward medium-close framing by the end.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
melancholy turning into restrained anger and urgency.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 4.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 4 — первый припев — первый эмоциональный выброс

**Музыкальный таймкод:** 1:30–2:00

**Функция фрагмента:** Дать первый настоящий припевный подъём: Маша сильнее обращается прямо к камере, но остаётся кинематографичной, без концертной истерики.

**Пластика Маши:** Она делает один небольшой шаг к камере, потом остаётся на месте; плечи и руки раскрываются немного сильнее, чем в куплете.

**Камера:** Start medium-close. Use a slow frontal dolly-in with a very subtle lateral arc, ending on an expressive close-up without cutting.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 4 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 4 / GLOBAL MUSIC TIMECODE 1:30–2:00:
Deliver the first true chorus lift: Masha addresses the camera more directly and intensely while remaining cinematic, with no concert-style hysteria.
BLOCKING / PHYSICAL ACTION:
She takes one small step toward the camera, then stays in place; her shoulders and arms open slightly more than during the verse.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

In your head,
In your head they are cryin'
In your head, In your head

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:07]
Sing the first exact line while taking one small step forward.
[0:07–0:17]
Sing the second exact line with stronger projection and direct eye contact.
[0:17–0:26]
Sing the third exact line. Let the camera arrive at a close but natural framing; preserve facial realism.
[0:26–0:30]
No new words. Let the phrase breathe while the close-up holds her emotional reaction.

CAMERA / LENS / CONTINUITY:
Start medium-close. Use a slow frontal dolly-in with a very subtle lateral arc, ending on an expressive close-up without cutting.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
first emotional release, grief becoming force.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 5.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 5 — первый припев — кульминация и вопрос

**Музыкальный таймкод:** 2:00–2:30

**Функция фрагмента:** Закрыть первый припев мощным, клиповым, но не хаотичным блоком и сделать первый большой зрительский payoff.

**Пластика Маши:** Маша поёт прямо в камеру, затем на одной фразе поворачивается на пол-оборота к озеру и снова возвращается в объектив; движения рук редкие и мотивированные.

**Камера:** A controlled half-orbit that starts medium-close, briefly opens to a medium-wide view showing the lake, then returns toward medium. No cuts.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 5 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 5 / GLOBAL MUSIC TIMECODE 2:00–2:30:
Close the first chorus with a powerful music-video passage that feels dynamic but never chaotic, delivering the sequence's first major visual payoff.
BLOCKING / PHYSICAL ACTION:
Masha sings directly to camera, turns halfway toward the lake during one phrase, then returns her gaze to the lens; hand gestures remain sparse and motivated.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

Zombie Zombie
Zombie ie ie
What's in your head, in your head
Zombie Zombie Zombie ie ie ie ou

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:06]
Sing exactly “Zombie Zombie”. Strong direct gaze.
[0:06–0:11]
Sing exactly “Zombie ie ie”. Keep the mouth shapes and breathing clearly sung, not spoken.
[0:11–0:19]
Sing the exact question line while Masha turns partly toward the lake.
[0:19–0:28]
Sing the final exact lyric line of this part as she turns back toward camera; the half-orbit reveals more of the shoreline.
[0:28–0:30]
No additional words. Let the final “ou” resolve naturally into the instrumental transition.

CAMERA / LENS / CONTINUITY:
A controlled half-orbit that starts medium-close, briefly opens to a medium-wide view showing the lake, then returns toward medium. No cuts.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
dramatic, wounded, strong, musically expansive.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 6.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 6 — вокализ / инструментальная передышка

**Музыкальный таймкод:** 2:30–3:00

**Функция фрагмента:** Дать клипу дыхание между куплетами: меньше фронтального пения, больше красивого движения Маши и пейзажа, сохраняя её почти постоянно в кадре.

**Пластика Маши:** Маша медленно идёт вдоль воды, иногда смотрит на горизонт; вокализ исполняет свободнее, как часть музыкального номера, но не танцует.

**Камера:** Begin with a wide side-tracking shot. Gradually move to a medium profile / three-quarter view while keeping Masha and the waterline in one coherent composition.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 6 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 6 / GLOBAL MUSIC TIMECODE 2:30–3:00:
Give the clip breathing room between verses: less frontal singing and more graceful movement through the lakeside environment, while keeping Masha visible almost continuously.
BLOCKING / PHYSICAL ACTION:
Masha walks slowly along the water, occasionally looking toward the horizon; she performs the vocalization more freely as part of the musical number, but does not dance.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

tu tu tu tu tu tu tu tu tu tu tu tu tu tu tu tu

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:08]
Masha begins the exact provided “tu” vocalise while walking slowly parallel to the shore. Keep the rhythm musical and natural.
[0:08–0:16]
Continue only the remaining provided “tu” syllables in exact order. She looks out over the lake rather than into camera.
[0:16–0:23]
No new lyric words. Continue instrumental backing; camera tracks beside her and lets the landscape breathe.
[0:23–0:30]
She slows to a stop and turns slightly back toward camera, preparing the second verse. No invented lyrics.

CAMERA / LENS / CONTINUITY:
Begin with a wide side-tracking shot. Gradually move to a medium profile / three-quarter view while keeping Masha and the waterline in one coherent composition.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
melancholic afterglow, suspended beauty, quiet movement.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 7.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 7 — второй куплет — новая волна

**Музыкальный таймкод:** 3:00–3:30

**Функция фрагмента:** Вернуть текст после интерлюдии, но уже с более зрелым и тяжёлым эмоциональным состоянием Маши.

**Пластика Маши:** Она стоит под углом к камере, затем делает один-два медленных шага в сторону воды; периодически взгляд опускается и снова поднимается.

**Камера:** A diagonal slow dolly-in from medium-wide to medium-close, with a slight side drift to keep the frame alive.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 7 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 7 / GLOBAL MUSIC TIMECODE 3:00–3:30:
Bring the lyrics back after the interlude with Masha now carrying a more mature, heavier emotional state.
BLOCKING / PHYSICAL ACTION:
She stands at an angle to the camera, then takes one or two slow steps toward the water; her gaze occasionally drops and then rises again.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

Another mother's breakin'
Heart is taking over
When the violence causes silence
We must be mistaken

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:07]
Sing the first exact line, starting from a quiet three-quarter profile.
[0:07–0:13]
Sing the second exact line. One small step toward the water; eyes briefly lower.
[0:13–0:21]
Sing the third exact line as the diagonal dolly-in continues.
[0:21–0:27]
Sing the fourth exact line. Masha lifts her gaze back toward camera.
[0:27–0:30]
No new words. Hold a natural breath and transition.

CAMERA / LENS / CONTINUITY:
A diagonal slow dolly-in from medium-wide to medium-close, with a slight side drift to keep the frame alive.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
weariness, sorrow, deeper internal pressure.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 8.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 8 — второй куплет — историческая тема и нарастание

**Музыкальный таймкод:** 3:30–4:00

**Функция фрагмента:** Сделать сильный драматический мост к финальному припевному блоку; камера становится ближе, а Маша — собраннее и жёстче.

**Пластика Маши:** Маша почти неподвижна в начале, затем разворачивается к камере и делает один уверенный шаг; на последней строке смотрит прямо в объектив.

**Камера:** Begin medium-wide with a slow push-in. Transition into a gentle near-frontal orbit of only a few degrees, ending medium-close.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 8 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 8 / GLOBAL MUSIC TIMECODE 3:30–4:00:
Create a strong dramatic bridge into the final chorus section; the camera moves closer while Masha becomes more focused and emotionally firm.
BLOCKING / PHYSICAL ACTION:
Masha is almost motionless at first, then turns toward the camera and takes one confident step; on the final line she looks directly into the lens.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

It's the same old theme since nineteen sixteen
In your head
In your head they're still fightin'

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:11]
Sing the first exact line slowly enough for natural articulation; Masha begins still and grounded.
[0:11–0:16]
Sing exactly “In your head”. She turns more directly toward camera.
[0:16–0:25]
Sing the third exact line as the camera makes a subtle near-frontal arc.
[0:25–0:30]
No new words. Let the musical tension build visibly in her face and breathing.

CAMERA / LENS / CONTINUITY:
Begin medium-wide with a slow push-in. Transition into a gentle near-frontal orbit of only a few degrees, ending medium-close.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
historical weight, restrained anger, gathering force.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 9.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 9 — финальный подъём — война продолжается

**Музыкальный таймкод:** 4:00–4:30

**Функция фрагмента:** Максимально приблизить номер к финальной кульминации: быстрых склеек нет, но движения камеры и Маши ощущаются мощнее.

**Пластика Маши:** Маша медленно идёт к камере по диагонали вдоль берега, затем останавливается; на последних строках удерживает прямой взгляд.

**Камера:** A smooth backward tracking move as Masha advances slowly, then settle into a medium-close framing when she stops. No handheld feel.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 9 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 9 / GLOBAL MUSIC TIMECODE 4:00–4:30:
Drive the number decisively toward its final climax: there are no rapid cuts, but both Masha's movement and the camera movement feel more powerful.
BLOCKING / PHYSICAL ACTION:
Masha slowly approaches the camera on a diagonal path along the shoreline, then stops; during the final lines she holds direct eye contact.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

With their tanks, and their bombs
And their bombs, and their guns
In your head In your head
they are dying
In your head, in your head

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:06]
Sing the first exact line while beginning the slow approach.
[0:06–0:12]
Sing the second exact line. Camera retreats at the same measured pace.
[0:12–0:18]
Sing the third exact line as Masha slows.
[0:18–0:23]
Sing exactly “they are dying”. She stops and the camera also settles.
[0:23–0:29]
Sing the final exact line with direct eye contact.
[0:29–0:30]
No extra words; take one breath into the final chorus.

CAMERA / LENS / CONTINUITY:
A smooth backward tracking move as Masha advances slowly, then settle into a medium-close framing when she stops. No handheld feel.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
urgent, tragic, increasingly forceful.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 10.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 10 — финальный припев — вершина

**Музыкальный таймкод:** 4:30–5:00

**Функция фрагмента:** Дать главный эмоциональный пик всего номера: наиболее сильная актёрская подача, самый выразительный close-up и затем расширение кадра перед аутро.

**Пластика Маши:** Маша почти не ходит: энергия теперь в лице, дыхании, корпусе и нескольких точных жестах. На середине припева может слегка раскрыть руки, затем снова собрать их.

**Камера:** Start medium-close, continue into an expressive close-up, then complete a graceful partial orbit and ease slightly wider by the end. One continuous shot.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 10 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 10 / GLOBAL MUSIC TIMECODE 4:30–5:00:
Deliver the main emotional peak of the entire number: the strongest performance, the most expressive close-up, then widen the framing in preparation for the outro.
BLOCKING / PHYSICAL ACTION:
Masha barely walks here; the energy is carried by her face, breathing, torso, and a few precise gestures. Midway through the chorus she may open her arms slightly, then bring them back in.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

Zombie Zombie
Zombie ie ie
What's in your head, in your head
Zombie Zombie Zombie
ie ie ie

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:05]
Sing exactly “Zombie Zombie” with the strongest direct performance of the sequence.
[0:05–0:10]
Sing exactly “Zombie ie ie”. Camera reaches the closest natural framing of the whole clip.
[0:10–0:18]
Sing the exact question line; begin a graceful partial orbit.
[0:18–0:24]
Sing exactly “Zombie Zombie Zombie”. Her posture opens slightly.
[0:24–0:28]
Sing exactly “ie ie ie”. Sustain only these provided syllables.
[0:28–0:30]
No additional words. Ease slightly wider, preparing the final vocal tail and outro.

CAMERA / LENS / CONTINUITY:
Start medium-close, continue into an expressive close-up, then complete a graceful partial orbit and ease slightly wider by the end. One continuous shot.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
catharsis, tragic power, emotional apex.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 11.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```


### Песня Маши 11 — финальный вокализ и визуальный аутро

**Музыкальный таймкод:** 5:00–5:30

**Функция фрагмента:** Закончить песню и дать красивое кинематографичное послевкусие: после последних звуков Маша остаётся у воды одна, а камера медленно отступает.

**Пластика Маши:** Первые секунды — финальный вокализ; затем Маша перестаёт петь, выдыхает, переводит взгляд на озеро и остаётся почти неподвижной.

**Камера:** Start medium-close, then perform one slow stable pull-back to a wide final lakeside composition with Masha small but clearly readable in frame.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on

REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: preserve the exact lakeshore, shoreline shape, water placement, background geography, natural color relationships, horizon, and overall spatial mood.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, aquatic-blue skin tone, head shape, long light-blue tentacle-like head strands, black ornamental head / neck / upper-back elements, body proportions, approved light-blue full-length character design, silhouette, and overall identity.

IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only location, geography, shoreline, water, environmental composition, and natural lighting logic.
Do not average Masha's face or body with anything from @Image1.
Do not beautify, restyle, age-shift, redesign, change costume, or alter body proportions.
Do not redesign the lake or introduce large new structures absent from the location reference.

CHARACTER APPEARANCE / IDENTITY LOCK:
@Image2 is the absolute visual authority for Masha-Laguna. Preserve her exact face and body proportions, pale aquatic-blue skin, long thick light-blue tentacle-like head strands, glossy black ornamental crown / neck / upper-back elements, and the same sleek light-blue full-length aquatic-fantasy silhouette. Do not replace the head strands with ordinary hair, redesign the black ornamentation, change skin color, alter body proportions, or change her approved design.

SEQUENCE CONTINUITY LOCK:
This is MASHA SONG PART 11 of 11.
Keep the same Masha, same exact approved character design, same aquatic-blue skin tone, same head strands and black ornamental elements, same lake, same shoreline, same weather, same time-of-day logic, same color grade, same overall screen-direction logic, and the same grounded live-action visual language established across the sequence.
Treat all eleven parts as one continuous music-video / musical performance assembled in editing.
Do not reset the character, wardrobe, location or visual style between parts.
Do not introduce an audience, band, stage, microphone stand, backup dancers, costume change, or new location.

GLOBAL DIRECTING BIBLE — APPLY TO ALL 11 PARTS:
- The lakeshore from @Image1 is the permanent visual foundation of the entire number. Every part remains in this same real location; only camera position and Masha's position along the shoreline may evolve naturally.
- Masha from @Image2 is the emotional and visual protagonist and must remain visible for almost the entire sequence. Do not cut away to empty landscapes for long periods.
- The clip must NEVER feel like eleven static clips of a woman standing still. Across the sequence Masha alternates naturally between: standing still, slowly walking along the waterline, turning toward camera, turning partly toward the lake, looking into the distance, and singing directly to lens.
- Performance is music-video cinematic but also has the emotional clarity of a musical: the song feels physically performed in the space, while camera movement and blocking create cinematic progression.
- Camera vocabulary across the eleven parts intentionally varies: wide establishing shot, slow dolly-in, side tracking move, gentle orbit / partial orbit, backward tracking while Masha approaches, medium performance shot, expressive close-up, and slow final pull-back.
- Camera motion must always be physically stable, smooth and motivated, with controlled inertia. No random jitter, no micro-shake, no teleporting, no arbitrary reversal of screen direction.
- Visual tone remains melancholic, dramatic and beautiful from beginning to end. Do not turn the sequence into glossy pop, concert coverage, cheerful choreography or fashion advertising.
- Emotional arc: quiet melancholy → growing tension → first release → lyrical breathing space → heavier second verse → rising anger/urgency → final catharsis → exhausted quiet outro.
- Identity, costume, hairstyle, lake geography, lighting logic, weather family, color grade and physical realism stay consistent across all eleven generations.
- Adjacent parts must end/start in compatible emotional and spatial states so the eleven renders can be assembled into one coherent clip.

STYLE GOAL:
Photorealistic live-action cinematic rock music video at a real lakeshore, staged with the emotional clarity and physical presence of a musical performance.
Melancholic, dramatic, beautiful, raw and intimate; emotionally serious rather than glossy or fashionable.
Masha is not merely posing for a camera: she is physically performing the song inside the landscape.
The scene must feel photographed with a real actress in a real outdoor location, not a stage show, not concert coverage, not animation, and not a synthetic game cutscene.

SCENE — MASHA SONG PART 11 / GLOBAL MUSIC TIMECODE 5:00–5:30:
Finish the song with a cinematic afterglow: after the final sounds, Masha remains alone by the water as the camera slowly pulls away.
BLOCKING / PHYSICAL ACTION:
The opening seconds contain the final vocalization; then Masha stops singing, exhales, turns her gaze toward the lake, and remains almost motionless.

VOCALS / EXACT USER-PROVIDED LYRICS / LIP SYNC:
Masha sings in English. This is SUNG performance, not spoken dialogue.
Use natural breathing, phrasing, consonant articulation, sustained-vowel mouth shapes and tight musical lip sync.
She must sing ONLY the exact user-provided lyric material below, in this exact order:

ou ou ou ou ou ou ou ou
yea

Do not add, remove, reorder, paraphrase, translate, censor, correct, replace, or invent any lyric words.
Do not substitute generic filler words or a different chorus.
Where the timeline says “no new words”, use only instrumental music, breath, or the natural sustained ending of the immediately preceding provided syllable.
Do not display lyrics as subtitles, captions, karaoke text, or typography on screen.

TIMELINE / STORY FLOW:
[0:00–0:05]
Sing the exact eight “ou” syllables rhythmically and naturally, without adding any extra sounds.
[0:05–0:07]
Sing exactly “yea” as the final vocal word/sound.
[0:07–0:16]
No lyrics. Masha exhales, lowers her intensity and turns her gaze toward the lake.
[0:16–0:24]
Camera begins a slow controlled pull-back; Masha remains still or makes one small natural shift of weight.
[0:24–0:30]
End in a stable wide composition of the exact lakeshore with Masha alone against the water. No fade to another location, no text, no freeze frame.

CAMERA / LENS / CONTINUITY:
Start medium-close, then perform one slow stable pull-back to a wide final lakeside composition with Masha small but clearly readable in frame.
Use physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Use natural cinematic perspective approximately equivalent to a 40–65 mm full-frame lens depending on framing.
Maintain one coherent 3D space. Horizon, shoreline, waterline and background objects remain geometrically stable.
Objects are revealed by camera movement; they do not teleport, morph or appear from nowhere.
No hard cuts, no jump cuts and no random montage inside this 30-second part.
Keep movement direction compatible with adjacent parts; do not arbitrarily flip screen direction.
No random jitter or micro-shake.

PERFORMANCE / ACTING:
Masha performs as a real person singing an emotionally heavy rock song.
Natural blinking, inhalation, jaw movement, sustained-vowel mouth shapes, throat/neck motion, chest and shoulder breathing, subtle weight transfer and precise eye focus.
Her body language changes with the music: sometimes quiet and almost still, sometimes walking slowly, sometimes turning toward camera, sometimes looking over the lake, sometimes giving direct eye contact.
Every gesture must be motivated by the phrase; avoid repetitive generic “music video” arm movements.
Emotion may grow from melancholy into grief, restrained anger and strength, but never into uncontrolled theatrical screaming or cheerful pop choreography.
Identity, face, hair, costume and proportions remain stable every frame.

PART-SPECIFIC EMOTIONAL TARGET:
release, exhaustion, melancholy after catharsis.
The emotional state must visibly evolve inside the part rather than staying as one frozen expression.

LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN:
Preserve the environmental and lighting identity of @Image1. Keep one continuous time-of-day and weather family across all eleven parts.
Natural skin texture and pores, realistic individual hair strands, cloth weave, physically plausible wind response and natural motion blur.
Water has small believable ripples and consistent reflections; shoreline material, vegetation and background geometry do not morph.
Use cinematic depth of field only when physically plausible; never blur the environment so aggressively that location continuity is lost.
No fantasy aura, magical glow, neon concert wash, impossible reflections, changing sky state, or sudden weather transition unless already intrinsic to @Image1.

AUDIO (native):
Lead vocal: clear expressive female singing voice, accurate English articulation, exact provided lyrics, tight SUNG lip sync.
Backing: melancholic alternative-rock instrumentation with electric guitar, bass and drums, supporting the vocal without overpowering it.
Keep tempo, vocal timbre, arrangement character and musical energy compatible from one 30-second part to the next so the eleven renders can be assembled as one song sequence.
Natural lake ambience remains subtle underneath: soft water, light wind and distant outdoor atmosphere.
No spoken dialogue, no crowd, no applause, no narrator, no subtitles.

TRANSITION / EDITING HANDOFF:
End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 11.
Do not fade to black, do not freeze-frame, and do not jump to a different location.
The final few frames should preserve the same lake, wardrobe, weather and screen-direction logic so the next 30-second render can continue seamlessly.

NEGATIVE PROMPT:
identity drift, different face, face morphing, changed age, changed hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, plastic skin, over-smoothed skin, bad sung lip sync, spoken delivery instead of singing, wrong lyric order, invented lyrics, omitted lyrics, translated lyrics, extra lyric words, subtitles, captions, karaoke text, lyrics on screen, visible band, audience, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, repetitive generic arm waving, cheerful pop performance, fashion-ad posing, long empty landscape cutaways without Masha, duplicated Masha, extra foreground characters, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, sudden weather shift, objects appearing from nowhere, hard cuts inside a part, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, cartoon, anime, stylized CGI, game cutscene, oversaturated neon lighting, logo, watermark, black bars, side bars, decorative borders, empty margins.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.

```
