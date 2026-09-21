# PROMPT-STYLE-GUIDE — единый стандарт видео-промтов

**Версия:** 1.2  
**Дата:** 20.09.2026  
**Назначение:** обязательная специализированная инструкция для текущего редактора и любого следующего чата/сменщика AI Film Project.

## 1. Зачем существует этот файл

Все новые видео-промты проекта должны сохранять тот же общий уровень структуры, сложности, режиссёрской конкретики и технической управляемости, что и лучшие актуальные сцены `video-prompts.md`.

Это **не шаблон для буквального копирования** старых текстов. Это стандарт качества: новый промт может иметь другие разделы, другой ритм и другую длину, если этого требует сцена, но он не должен скатываться к короткому общему описанию вида «герой стоит у озера, камера приближается, красиво и атмосферно».

Главная цель — заранее закрывать риски генерации: identity drift, смешивание референсов, нелогичную геометрию, случайную камеру, сломанный тайминг, неверный lip sync, мультяшность, лишние объекты, неправильное аудио и прочие типовые ошибки.

## 2. Когда читать

Этот файл является частью обязательного seven-document takeover set. Новый чат сначала читает `NEW-CHAT-HANDOFF.md`, `SYNC-RUNBOOK.md`, `AI-PROJECT-GUIDE.md`, этот `PROMPT-STYLE-GUIDE.md`, `USER-GUIDE.md`, `README-AI-SYNC.md`, `BACKUP-AI-RUNBOOK.md`, а затем fresh master и live status JSON.

Перед написанием **любого нового prompt** или существенной переработкой существующего prompt текущий чат/сменщик обязан:

1. fresh-read этот `PROMPT-STYLE-GUIDE.md`;
2. fresh-read exact Drive `video-prompts.md`;
3. открыть минимум 1–2 актуальные сцены master, наиболее близкие к задаче;
4. проверить current Scene ID / engine / reference assignment;
5. только затем писать новый prompt.

Нельзя заменять этот full guide кратким пересказом из переписки или памятью предыдущего чата.

Для добавления новой сцены не спрашивать номер, если его можно определить из проекта. Scene IDs стабильны; удалённые номера не переиспользуются. Новый ID = следующий ещё не использованный стабильный Scene ID после последнего известного ID проекта. На checkpoint 20.09.2026 после Scene 19 следующая новая сцена получила ID 20.

## 3. Источник истины и приоритеты

- Единственный editable prompt master: Google Drive `video-prompts.md`.
- Сначала выполняется fresh-read Drive master, затем правка.
- Старые вложения, Library-копии и GitHub mirror не являются editable master.
- Текущая явная команда пользователя сильнее старых заметок и исторических snapshot-ов.
- Approved model sheet сильнее визуального сходства случайного frame reference.
- Не придумывать отсутствующие референсы, костюмы, имена файлов или номера сцен.

## 4. Как должен выглядеть scene block в master

Обычная новая сцена оформляется на двух уровнях.

### 4.1. Человеческая обвязка сцены

```md
<a id="scene-N"></a>

## Сцена N — Короткое понятное название

<!-- scene-meta: {"target_engine":"Seedance 2.5","production_state":"READY","duration_s":30,"dialogue":{"enabled":true,"language":"ru"},"tags":["..."]} -->

**Контекст использования:** зачем сцена нужна, её функция, важные решения пользователя, ограничения.

**Референсы:** @Image1 = ... · @Image2 = ...

**Что происходит:** короткий человеческий пересказ результата без технической перегрузки.

```text
...полный prompt...
```
```

Если сцена slow, marker `**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**` добавляется только когда генерация реально запущена / scene входит в canonical slow-list. Статус `READY` сам по себе не означает slow.

### 4.2. Полный prompt

Сам prompt должен быть достаточно подробным, чтобы модель понимала не только сюжет, но и **что считать неизменяемым, как двигаться во времени, как вести камеру, как играть персонажей, какой звук нужен и чего категорически избегать**.

## 5. Базовая структура полного prompt

Не каждый prompt обязан иметь абсолютно одинаковые заголовки, но обычно master-level prompt включает следующие блоки.

### A. Техническая строка

В начале явно задавать режим и технические параметры, например:

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
```

Не копировать 1080p/16:9 механически, если пользователь или движок требуют другое.

### B. REFERENCES

Каждому референсу назначить **одну ясную роль**:

- PRIMARY exact identity reference;
- location / environment only;
- starting composition only;
- ending composition only;
- costume / transformed form only;
- prop / vehicle design only.

Плохой вариант: `@Image1 — reference`.  
Хороший вариант: объяснить, **что брать и что не брать** из изображения.

### C. IMPORTANT REFERENCE RULE / REFERENCE PRIORITY

При двух и более референсах почти всегда нужен явный приоритет.

Нужно писать, например:

- лицо/возраст/пропорции берутся только из model sheet;
- локационный кадр не имеет права переопределять персонажа;
- стартовый/финальный кадр отвечает за композицию, а не identity;
- запрещено усреднять лица между изображениями;
- approved character sheet является identity lock.

### D. STYLE GOAL / SCENE / ENVIRONMENT

Нужно описывать не набор эпитетов, а конкретную постановочную цель:

- live-action или стилизация;
- жанр;
- настроение;
- физический характер мира;
- уровень серьёзности/комедии;
- production design;
- что должно ощущаться как реальная съёмка.

Формулировки «cinematic, beautiful, epic» сами по себе недостаточны.

### E. TIMELINE / STORY FLOW / SCENE STRUCTURE

Для 20–30 секунд с несколькими beats обычно нужна временная разметка.

Пример логики:

```text
[0:00–0:05] setup
[0:05–0:11] first action / first line
[0:11–0:18] escalation
[0:18–0:25] consequence
[0:25–0:30] final composition
```

Тайминг должен быть **реалистичным**: длинную реплику нельзя запихивать в 2 секунды, а сложное физическое действие не должно происходить одновременно с пятью другими ключевыми событиями.

Если точные секунды мешают модели, использовать `Story flow:` и последовательные beats, но порядок всё равно должен быть однозначным.

### F. CAMERA / LENS / CONTINUITY

Почти всегда нужен отдельный блок камеры.

Глобальные правила проекта:

- physically stable cinematic motion;
- controlled inertia;
- no random jitter / micro-shake;
- coherent 3D space;
- камера не телепортируется;
- новые объекты не возникают из ничего, а раскрываются движением камеры;
- направление движения и пространственная логика не ломаются между beats.

Если нужен continuous take — написать это явно. Если допустима shot progression — описать её как мотивированную последовательность, а не случайный монтаж.

### G. PERFORMANCE / ACTING

Для людей и антропоморфных персонажей описывать:

- исходное эмоциональное состояние;
- изменение состояния;
- уровень мимики и жестов;
- natural blinking / breathing / weight transfer;
- что нельзя переигрывать;
- как сохраняется identity и costume.

Комедия проекта часто лучше работает, когда персонажи играют происходящее **серьёзно**, а юмор возникает из ситуации, а не из гротескной актёрской игры.

### H. DIALOGUE / VOCALS / LIP SYNC

Если есть речь или пение:

- язык указывать явно;
- точный текст помещать отдельно;
- назначать конкретного говорящего;
- требовать natural pronunciation и accurate lip sync;
- описывать интонацию;
- запрещать subtitles/captions, если они не нужны.

Для русского диалога по умолчанию — естественная русская речь без акцента, если пользователь не задал другое.

Для пения явно писать `sung, not spoken`, breathing, phrasing, mouth shapes и роль музыкального сопровождения.

Если пользователь хочет существующую песню, но точные защищённые lyrics не были предоставлены пользователем, не вставлять их самостоятельно: использовать оригинальный текст, предоставленный пользователем текст или нейтральный placeholder/описание вокала в зависимости от задачи.

### I. LIGHTING / MATERIAL REALISM / PRODUCTION DESIGN

Нужно конкретизировать:

- источник и направление света;
- характер теней;
- material response кожи, ткани, металла, воды и т. п.;
- глубину/дымку/рефлексы;
- что должно оставаться физически правдоподобным.

Для live-action полезны отдельные realism locks: pores, fabric weave, practical-light falloff, natural motion blur, believable reflections.

### J. AUDIO (native)

Если `Native audio: on`, описывать звук так же конкретно, как изображение:

- dialogue/vocal priority;
- шаги;
- ветер;
- вода;
- одежда;
- engine hum / room tone;
- музыка и её громкость;
- что не должно заглушать речь.

### K. NEGATIVE PROMPT

Negative prompt должен быть **сценоспецифичным**, а не универсальным хвостом из пяти слов.

Обычно проверять риски:

- identity drift / face morphing;
- costume drift;
- duplicated / missing people;
- distorted hands / fingers;
- broken physical interaction;
- lip desync;
- wrong speaker;
- cartoon / anime / game-render look, если нужен live-action;
- plastic/wax skin;
- warped environment;
- changing geometry;
- camera jitter;
- hard cuts / random montage;
- accidental subtitles/text/logo/watermark;
- типичные ошибки конкретной сцены: неправильный slap, неверное оружие, лишний микрофон, магические грибы и т. д.

### L. FRAME FILL / NO BARS

Для всех текущих и будущих prompts действует глобальное правило, если пользователь явно не отменил его:

```text
FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

## 6. Уровень подробности

Ориентир — не количество слов, а **плотность полезных ограничений**.

Master-level prompt:

- однозначно распределяет роли референсов;
- фиксирует protagonist/identity;
- содержит понятную драматургию по времени;
- задаёт физически правдоподобную камеру;
- описывает performance;
- описывает environment/light/materials;
- управляет audio;
- содержит сценоспецифичный negative prompt;
- не противоречит сам себе.

Простая сцена может быть короче сложной, но не должна терять ключевые блоки только потому, что исходная идея пользователя сформулирована одной строкой.

## 7. Адаптация под движок

### Seedance 2.5

Обычно хорошо работает подробная режиссёрская структура, точное распределение референсов, ясная временная последовательность, controlled camera motion и native audio instructions.

Не перегружать одновременными независимыми действиями. Если 30 секунд — распределять beats по времени.

### Wan 3.0

Особенно внимательно контролировать live-action realism, identity stability, mouth/lip sync, материальность и отсутствие мультяшного/глянцевого CG look, если предыдущий результат имел такой дефект.

### Veo / другие движки

Сохранять ту же master-level режиссёрскую структуру, но учитывать ограничения конкретной модели по длительности, native audio, reference count и moderation. Не тащить технические параметры Seedance в другой движок механически.

## 8. Continuity между сценами

Если сцена является продолжением:

- явно назвать связь с предыдущей;
- сохранить одежду, свет, погоду, повреждения, реквизит;
- сохранить направление движения;
- определить стартовую и конечную композицию;
- не менять геометрию пространства без мотивированного перехода.

Если есть starting/ending frame references, указать, что именно они фиксируют и что они **не имеют права переопределять**.

## 9. Правила для нового Scene ID

- Scene IDs никогда не перенумеровываются ради «красивой» последовательности.
- Удалённые IDs не переиспользуются.
- Не спрашивать пользователя «какой номер дать?», если project status/master однозначно позволяет определить следующий стабильный ID.
- Перед присвоением номера fresh-check `video-prompts.md` и `project-status.json.latest_scene` / known history.
- После добавления обновить scene map / counts / status metadata, а не только вставить prompt в конец файла.

## 10. Что запрещено считать готовым prompt

Не оставлять как финальный master prompt текст уровня:

> A woman stands by a lake and sings emotionally. Cinematic camera slowly moves closer. Beautiful lighting, realistic style.

В нём нет identity lock, роли локационного референса, тайминга, performance, vocal rules, spatial continuity, audio design и negative prompt.

Также нельзя:

- автоматически переписывать все NEEDS_FIX разом;
- подменять точный model sheet «похожим» лицом;
- добавлять в prompt выдуманный reference;
- превращать continuous scene в хаотичный montage без причины;
- снимать slow после `success` одной попытки, если у той же сцены ещё есть другие active Topview tasks;
- создавать `video-prompts-v2/final/copy` вместо same-ID edit.

## 11. Финальный чек-лист перед сохранением нового prompt

Перед записью в master проверить:

- [ ] Scene ID определён по стабильным правилам и не переиспользован.
- [ ] `scene-meta` соответствует движку, длительности, языку и production state.
- [ ] Есть `Контекст использования`.
- [ ] Есть `Референсы`.
- [ ] Есть `Что происходит`.
- [ ] В prompt есть техническая строка.
- [ ] Каждому reference назначена конкретная роль.
- [ ] При нескольких reference есть priority rule.
- [ ] Сюжет разбит на последовательные beats / timeline, если это полезно.
- [ ] Камера физически понятна и стабильна.
- [ ] Performance прописан.
- [ ] Dialogue/vocal + lip sync прописаны, если нужны.
- [ ] Environment / lighting / material realism описаны.
- [ ] Audio описан при Native audio on.
- [ ] Negative prompt привязан к рискам конкретной сцены.
- [ ] `FRAME FILL / NO BARS` присутствует.
- [ ] Нет внутренних противоречий.
- [ ] После записи обновлены map/counts и выполнена стандартная Drive→GitHub→Pages проверка.

## 12. Эталонные live-сцены в текущем master

При написании нового prompt сначала выбрать ближайший по задаче эталон и прочитать его **в свежем master**, потому что master может измениться.

- **Scene 2** — сложный ensemble, multiple identity references, formation lock, camera tracking.
- **Scene 14** — одиночный герой, подробный timeline, dry comedy, environment/material logic.
- **Scene 18** — walk-and-talk dialogue, live-action realism lock, production design, lip sync.
- **Scene 19** — multiple references, fantasy event, dialogue beats, physical interaction, transition to running ending.
- **Scene 20** — музыкальный performance, location reference + identity reference, sung lip sync, continuous camera.

Ниже приложены несколько полных **snapshot-примеров из master**. Они нужны как ориентир по плотности и структуре. Это не второй master: если пример ниже расходится с более свежим `video-prompts.md`, всегда использовать свежий master.

---

# Пример A — Scene 14 snapshot

<a id="scene-14"></a>


## Сцена 14 — Канцлер: сбор грибов в гигантском лесу


<!-- scene-meta: {"production_state":"READY","duration_s":30,"dialogue":{"enabled":false,"language":null},"tags":["comedy"],"target_engine":"Seedance 2.5"} -->


**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**


Повторно не запускать до результата/ошибки или отдельного решения пользователя.


**Контекст использования:** Новый активный промт на основе бывшей W2; рабочий пункт W2 получил конкретный референс Канцлера и теперь оформлен как активная сцена 14. 30-секундная серьёзно снятая комедийная вставка перед/внутри лесной линии: пока другие персонажи ищут опасного Канцлера, он с неожиданным искренним энтузиазмом занят грибами. Излишки затем можно сократить на монтаже.


**Референсы:** @image3 = Chancellor, точный модель-шит лица, телосложения и тёмно-фиолетовой мантии. Лес задаётся текстом: огромные древние деревья, густой влажный подлесок, масштаб почти монументальный.


**Что происходит:** Канцлер один идёт по колоссальному лесу с небольшой корзиной, внимательно изучает землю, замечает первую группу грибов у гигантского корня, почти научно осматривает их и бережно собирает. Затем он замечает ещё более интересный гриб глубже между корнями, быстро, но всё ещё серьёзно перебирается к нему, сравнивает находки, складывает добычу в корзину и в конце снова видит что-то перспективное впереди и уходит глубже в лес.


```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on


REFERENCE:
@image3 — PRIMARY exact character identity reference for THE CHANCELLOR: pale middle-aged-to-older man, bald on top with thin pale blond hair around the sides and back, pale blue-grey eyes, heavy facial structure, wearing a long deep-purple / black-purple hooded robe with layered dark fabric. Preserve his exact face, age, build, hair pattern, robe design, robe color, and proportions throughout.


SCENE:
A vast ancient forest on a giant-tree world. Tree trunks are enormous, wider than buildings, rising far beyond the upper frame. Massive exposed roots form natural ridges across the damp forest floor. Dense moss, ferns, fallen leaves, small plants, drifting mist, and shafts of warm filtered sunlight create a rich photorealistic environment. The Chancellor is completely alone.


The scene is intentionally funny but must be performed and photographed with absolute seriousness. The Chancellor is not behaving like a clown. He is genuinely, almost scholarly, delighted by mushroom hunting and gives the task the same focused importance he would give to a strategic military operation.


TIMELINE:
[0:00–0:06]
Wide cinematic tracking shot. The Chancellor walks slowly through the colossal forest carrying a small simple woven basket in his left hand. He studies the ground with intense concentration, occasionally moving aside a fern with his free hand. His purple robe brushes naturally against moss and low vegetation. The giant trees establish an overwhelming sense of scale.


[0:06–0:11]
He suddenly notices a small cluster of unusual but realistic forest mushrooms growing beside an enormous moss-covered root. His expression changes subtly: eyebrows lift, eyes sharpen with genuine interest, and a restrained pleased smile appears. He changes direction immediately and steps over a low root toward them with surprising but controlled enthusiasm.


[0:11–0:17]
Camera lowers into a medium three-quarter shot as he crouches beside the root. He carefully examines two mushrooms from several angles without damaging them, gently brushes away a leaf, checks the underside of one cap, then cleanly picks the best specimen at the stem. He studies it in his hand with almost scientific fascination.


[0:17–0:21]
He places the first mushroom carefully into the basket, then picks a second smaller one. Before standing, he compares the two for a beat, visibly satisfied with the selection. The comedy stays completely dry and understated.


[0:21–0:26]
While still crouched, he notices another larger but biologically plausible mushroom growing several meters away in a pocket between two gigantic roots. His eyes widen slightly. He rises faster than before, steps over the root ridge and moves toward it with renewed purpose, keeping the basket steady.


[0:26–0:30]
He reaches the second patch, kneels briefly, gently lifts the larger mushroom to inspect it without immediately picking it, then looks deeper into the forest and notices yet another promising area off-screen. A small satisfied smile returns. He stands and continues deeper between the colossal trunks as the camera follows, ending with him fully absorbed in the hunt.


CAMERA:
One continuous physically stable cinematic shot. Smooth controlled glide following and gently arcing around the Chancellor. The camera may lower with him when he crouches and rise naturally when he stands, but never teleports or cuts. Maintain one coherent 3D forest space; every root, tree and mushroom must already exist in the environment and be revealed naturally by camera movement.


CHARACTER PERFORMANCE:
Restrained live-action acting. Small facial micro-expressions only. He is focused, curious and sincerely pleased, not manic or goofy. Keep the same face, age, bald pattern, body shape and robe from @image3 in every frame. Natural crouching, hand contact, stepping over roots and weight transfer. His growing enthusiasm is shown through slightly quicker movement and attentive eyes, not exaggerated gestures.


FOREST / LIGHTING:
Photorealistic giant ancient forest. Monumental trunks, deep layered canopy, warm dappled sunlight, soft volumetric rays, cool green ambient bounce, damp moss, subtle atmospheric mist, natural insects and distant birds. Mushrooms should look biologically plausible and varied, not neon fantasy props. No modern objects.


AUDIO (native):
Deep quiet forest ambience, distant birds, faint insects, soft wind high in the canopy, footsteps compressing damp moss, robe brushing vegetation, slight basket creak, tiny natural sounds as mushrooms are handled and picked. No dialogue. No music.


NEGATIVE PROMPT:
identity drift, different face, different age, full head of hair, robe color change, costume change, duplicate Chancellor, extra people, modern hiking equipment, plastic basket, magical glowing mushrooms, giant comedy mushroom, psychedelic neon colors, slapstick acting, exaggerated grin, distorted hands, extra fingers, mushroom growing or morphing on contact, trees appearing from nowhere, changing forest geometry, floating roots, camera shake, hard cuts, cartoon, anime, game-render look, text, subtitles, logos, watermark.

FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```
---


<a id="scene-15"></a>

---

# Пример B — Scene 19 snapshot

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

---

# Пример C — Scene 20 snapshot

<a id="scene-20"></a>


## Сцена 20 — Маша-Лагуна: рок-припев у озера


<!-- scene-meta: {"target_engine":"Seedance 2.5","production_state":"READY","duration_s":30,"dialogue":{"enabled":true,"language":"en"},"tags":["music_performance","vocal_performance","continuous_take","lakeshore"]} -->


**Контекст использования:** Новая активная 30-секундная музыкальная сцена для Seedance 2.5. @Image1 задаёт точную локацию берега озера, @Image2 — точный образ Маши-Лагуны. Сцена строится как цельный live-action музыкальный перформанс: Маша стоит у воды и исполняет эмоциональный англоязычный рок-припев. В prompt не упоминаются конкретные существующие группа или песня. Текст припева ниже оригинальный и используется как точный вокальный текст для lip sync.


**Референсы:** @Image1 = локация / берег озера / окружение · @Image2 = Маша-Лагуна, PRIMARY exact identity reference


**Что происходит:** Маша-Лагуна одна стоит на берегу озера из @Image1 и поёт эмоциональный меланхоличный рок-припев. Камера начинает с более широкого плана, затем медленно и физически стабильно приближается. Лёгкий ветер естественно двигает волосы и одежду, вода остаётся спокойной и реалистичной. Вокал постепенно усиливается, но актёрская игра остаётся живой и сдержанной; финал приходит к более близкому эмоциональному кадру Маши без смены локации и без монтажной дробности.


```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on


REFERENCES:
@Image1 — LOCATION / ENVIRONMENT reference only: the exact lakeshore location, shoreline shape, water placement, surrounding landscape, background geography, natural color relationships, and overall spatial mood. Preserve the recognizable location and do not redesign it into a different lake or fantasy set.
@Image2 — PRIMARY exact identity reference for MASHA-LAGUNA: preserve her exact face, age, hairstyle, body proportions, clothing / character design, silhouette, and overall identity throughout the full 30-second performance.


IMPORTANT REFERENCE RULE:
@Image2 is the absolute identity lock for Masha-Laguna.
@Image1 controls only the location, geography, shoreline, water, and environmental composition.
Do not average Masha's face or body with anything from @Image1.
Do not replace, beautify, restyle, age-shift, or redesign Masha.
Do not alter the lake into another environment and do not invent large new structures that are absent from the location reference.


STYLE GOAL:
Photorealistic live-action cinematic music performance at a real lakeshore. Emotional, melancholic, raw, and intimate alternative-rock energy with a restrained 1990s feeling, but no reference to any specific existing band or song. The scene must feel like a serious film/music-video performance photographed with a real actress in a real outdoor location, not a stage show, not glossy pop choreography, not animation, and not a synthetic game cutscene.


SCENE — ONE CONTINUOUS 30-SECOND PERFORMANCE:
Masha-Laguna stands alone close to the water's edge in the exact lakeside environment established by @Image1. She faces slightly toward camera while remaining naturally connected to the landscape. The lake is clearly visible in the composition. There is no audience, no band visible in frame, no stage, no microphone stand, and no extra foreground characters.

She sings the following ORIGINAL English chorus with clear articulation and accurate lip sync. These are the only required lyrics; do not replace them with lines from any existing song:

“Hear the silence, hear it calling,
Through the dark, the echoes falling,
In my heart the fire is rising,
Still I stand, no more disguising.”

If musical timing requires additional vocal time, the same four-line chorus may repeat once naturally. Do not invent unrelated extra lyrics and do not substitute recognizable lyrics from another song.


TIMELINE:
[0:00–0:04]
Open in a medium-wide establishing shot. Masha-Laguna stands at the lakeshore from @Image1 with the water and recognizable background geography clearly readable. She takes a natural breath before the vocal entry. A light breeze moves individual strands of hair and the loose parts of her clothing. The camera is already in gentle motion, beginning a very slow controlled push toward her.

[0:04–0:11]
Masha begins singing:
“Hear the silence, hear it calling,
Through the dark, the echoes falling,”
Her delivery starts controlled and melancholic, then grows in emotional weight. Keep natural breathing, realistic mouth shapes, subtle jaw movement and exact sung lip sync. The camera continues its slow push-in without changing direction abruptly.

[0:11–0:18]
She continues:
“In my heart the fire is rising,
Still I stand, no more disguising.”
Her vocal intensity opens up. Her eyes become more focused and emotionally charged, but the performance remains believable and grounded. No broad theatrical hand gestures. One small natural hand movement or a slight shift of weight is acceptable if motivated by the performance.

[0:18–0:25]
Let the musical phrase breathe. Masha may repeat the chorus from the beginning or sustain and resolve the final musical phrase, depending on natural timing, while keeping the exact same lyrical material. Camera reaches a clean medium shot. The lake remains visible behind or beside her and the environment stays spatially continuous.

[0:25–0:30]
The camera makes only a very subtle final arc or lateral drift while staying close enough to read her eyes and mouth clearly. Masha finishes the phrase with a strong but controlled emotional release. End on a stable cinematic medium / medium-close composition with the same lake and shoreline still coherent in the background. No freeze frame, no fade to a different location, no sudden pose.


CAMERA / CONTINUITY:
One continuous unbroken shot for the full 30 seconds.
Physically stable cinematic dolly / precision-gimbal behavior with controlled inertia.
Start medium-wide and slowly push toward medium / medium-close framing.
A subtle motivated arc near the end is allowed, but there must be no sudden lateral jump, no teleporting camera, no random reframing, no hard cuts, no jump cuts, and no montage.
Maintain one coherent 3D space. Shoreline, horizon, water, and background objects must remain geometrically stable and reveal themselves naturally through camera motion.
No random jitter or micro-shake.


PERFORMANCE / VOCAL DELIVERY:
Masha-Laguna performs with sincere melancholy, restrained anger, vulnerability, and growing strength. She is emotionally intense without becoming hysterical or theatrical.
Natural blinking, breathing, eye focus, facial micro-expressions, neck and jaw motion, and subtle body weight transfer.
The singing must look physically believable: realistic inhalation before phrases, mouth opening appropriate to sustained vowels, natural chest / shoulder breathing, and no frozen face between lines.
Do not make her smile broadly or perform cheerful pop choreography.
Identity, hairstyle, costume and proportions must remain stable in every frame.


LIGHTING / ENVIRONMENT:
Preserve the environmental identity of @Image1. Use natural outdoor light consistent with the reference image. If the source is soft daylight / overcast light, keep it soft and cinematic rather than replacing it with golden-hour or concert lighting.
Water should have small physically plausible ripples and realistic reflections. Wind affects hair and fabric lightly and consistently. Plants, shoreline material and distant background must not morph or appear/disappear.
Natural skin tone, realistic cloth texture, believable contact with the ground, and physically plausible depth of field.
No fantasy glow, no magical aura, no neon color wash unless already present in @Image2 as an intrinsic part of Masha-Laguna's approved design.


AUDIO (native):
Clear expressive female singing voice with accurate English pronunciation and tight sung lip sync.
Vocal is the dominant element in the mix.
Backing track: restrained melancholic alternative-rock arrangement with electric guitar, bass and drums, emotionally building without overpowering the voice. Do not imitate or reproduce a specific existing recording or melody.
Natural lake ambience remains quietly audible underneath: soft water movement, light wind and distant outdoor atmosphere.
No crowd noise, no applause, no spoken dialogue, no subtitles.


NEGATIVE PROMPT:
identity drift, different face, different age, different hairstyle, costume change, body-shape drift, beauty-filter face, wax skin, over-smoothed skin, face morphing, bad lip sync, spoken delivery instead of singing, frozen mouth, random or recognizable lyrics from an existing song, subtitles, captions, karaoke text, lyrics on screen, extra people, audience, visible band, backup dancers, concert stage, handheld microphone, microphone stand, exaggerated choreography, broad theatrical gestures, cheerful pop performance, cartoon, anime, stylized CGI, game cutscene, plastic skin, distorted hands, extra fingers, warped body, unstable horizon, changing shoreline, moving geography, lake morphing, broken water reflections, objects appearing from nowhere, surreal water behavior, hard cuts, jump cuts, random montage, sudden zoom, camera jitter, micro-shake, oversaturated neon lighting, black bars, side bars, decorative borders, empty margins, logo, watermark.


FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

---

## 13. Правило для следующего чата / сменщика

Если новый prompt заметно беднее по структуре, чем свежие Scenes 2 / 14 / 18 / 19 / 20, он **не готов** и должен быть доработан до master-level.

Сменщик не должен просить пользователя заново объяснять уже известные project rules. Если задача однозначно выводится из fresh master + handoff + этого guide, нужно продолжать работу по установленному workflow.


## 14. Documentation / handoff maintenance for prompt changes

Prompt-writing standard — не отдельная статичная памятка. Если в ходе работы появляется новое повторяемое правило, которое должно действовать для будущих сцен (новый обязательный block, новый reference-priority rule, новое continuity/audio/camera правило, новая engine-specific практика), текущий редактор обязан в том же цикле:

1. обновить **этот SAME Drive `PROMPT-STYLE-GUIDE.md`**;
2. обновить relevant `AI-PROJECT-GUIDE.md`, `USER-GUIDE.md`, `BACKUP-AI-RUNBOOK.md`;
3. обновить `NEW-CHAT-HANDOFF.md`, если правило важно для takeover/current workflow;
4. exact-mirror Drive → GitHub;
5. refresh `instruction-sync-status.json`;
6. refresh Library recovery copy;
7. update Notion operational pointer if rule changes how future chats should work.

Не создавать `PROMPT-STYLE-GUIDE-v2/final/copy`. Правится тот же canonical Drive file ID `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`.

Snapshot examples ниже/выше — эталоны **сложности и структуры**, а не eternal current scene truth. Перед копированием решения всегда смотреть fresh master.


## 15. Definition of Done для prompt-work и передачи следующему чату

Обычная новая/изменённая сцена считается записанной только после:
1. fresh guide + fresh master;
2. master-level prompt;
3. SAME-ID Drive write;
4. TOC/count/meta consistency;
5. Drive → GitHub sync;
6. validator/status verification;
7. Pages verification, если сцена отображается на Control Center.

Если во время prompt-work появилось **новое повторяемое правило**, которое должно действовать для будущих сцен, это уже material workflow change. Тогда до завершения задачи требуется:
- обновить SAME `PROMPT-STYLE-GUIDE.md`;
- обновить релевантные файлы seven-document takeover set;
- обновить SAME `NEW-CHAT-HANDOFF.md`;
- exact-mirror Drive → GitHub;
- refresh `instruction-sync-status.json`;
- обновить Notion operational pointer;
- обновить Library recovery copies.

Следующий чат обязан знать: prompt style не хранится «в памяти прошлого чата». Он хранится здесь и в живом master. Если пользователь формулирует новую сцену кратко, задача редактора — самостоятельно развернуть её до принятого master-level формата, не заставляя пользователя повторно диктовать техническую структуру.

## 16. Имена персонажей → exact identity в prompt

Перед написанием новой сцены редактор обязан разрешить имена через `character-references.json` + current `video-prompts.md`. Пользователь может задавать сцену человеческим языком — например, «Паша говорит Саше, затем заходит Серёжа» — и не обязан каждый раз повторять внешность.

Для каждого известного персонажа в prompt:
- использовать canonical name;
- назначить exact attached model sheet как PRIMARY identity reference, если он доступен в этой generation task;
- кратко зафиксировать отличительные черты лица/телосложения/прически/костюма из approved model sheet/current scene variant;
- не переносить одежду из другой сцены, если current scene требует иной approved variant;
- не позволять environment/group reference переопределять индивидуальную identity.

Global registry на текущем checkpoint: **Серёга (Канцлер/The Chancellor), Юля, Паша (JEDI-A/Navy Jedi), Артём (Bearded Jedi), Илюша (Hooded Jedi), Саша (JEDI-B/Glasses Jedi), Лёша (PURPLE), Виталик (BLACK)**. В однозначном контексте `Серёжа` resolve → `Серёга`.

Персонажи, существующие только в конкретных current prompts (например Маша-Лагуна или Imperial Officer), разрешаются через fresh scene references/master. Не выдумывать global model sheet для персонажа, которого там нет.

Если user name/alias реально может относиться к двум разным людям и current sources не снимают неоднозначность, задать один точный вопрос. В остальных случаях resolve самостоятельно.

## 17. Связь prompt с монтажным контекстом

Перед созданием сцены следующий чат уже должен быть ознакомлен с `Seregius_montazhny_razbor.html`, `film-analysis.md` и `film-backlog.md`. При разработке новой сцены учитывать её монтажную функцию: что было до неё, что должно стать понятнее после неё, какие сюжетные/диалоговые проблемы она закрывает и не дублирует ли уже существующий beat.

Монтажный анализ — context/recommendation layer, не второй prompt master. Новый explicit user decision и current master имеют приоритет над старой рекомендацией.

## 18. Imported Topview prompt: fidelity rule

Когда новая сцена создана автоматикой из уже запущенной/готовой Topview video task, есть особое правило происхождения prompt:

- **actual prompt, реально отправленный в Topview, сохраняется verbatim** как source prompt этой imported scene;
- нельзя автоматически переписать его в более красивый master-style и затем утверждать, что именно эта новая версия использовалась при генерации;
- master-style wrapper (`Контекст использования`, `Референсы`, `Что происходит`, корректный `scene-meta`) может быть добавлен вокруг source prompt;
- если позже пользователь просит улучшенный rerender prompt, это уже отдельная новая редакционная версия внутри той же scene по обычным правилам, при этом происхождение исходного Topview prompt не теряется;
- known characters при import resolve через global registry/current master, но неизвестные детали не выдумываются.

Это исключение существует ради provenance: guide определяет качество новых prompts, но не должен переписывать историю уже совершённой генерации.

## 19. Prompt-quality проверки в daily deep audit

Раз в 24 часа `AI Film Recovery Sync` внутри своего daily deep audit может **проверять** активные/new prompts на явный regression относительно этого guide: reference priority, identity handling, timeline/story flow, camera/continuity, audio, negative prompt, `FRAME FILL / NO BARS` и другие обязательные элементы.

Это audit, а не разрешение автоматически переписывать творческий prompt. Автоматически допустимы только однозначные механические/documentation fixes. Содержательное изменение сцены, диалога, режиссуры или approval требует обычного editor/user workflow. Deep-audit result записывается в `deep-audit-status.json`; Topview auto-intake остаётся отдельной automation.

## 20. Место этой инструкции в takeover order

На Control Center этот файл отображается как **№4 «Стандарт написания промтов»** в вертикальном seven-document списке. До него новый чат читает HANDOFF, Sync Runbook и Project Guide; после него — User Guide, README AI Sync и Backup AI Runbook.

Master/film-analysis/backlog, находящиеся в той же общей шторке, относятся к рабочим файлам проекта и не являются дополнительными prompt-инструкциями. В UI они вынесены в отдельный блок и также идут вертикально один под другим.

## Canonical Topview state — minimal operational model

This is the permanent Topview rule for the master, watcher, recovery and Control Center:

- **Scene ID** identifies the creative scene. **Topview task ID** identifies one render attempt.
- A rerun/rerender/revised prompt for the same creative scene keeps the same Scene ID.
- Persistent Topview state is intentionally minimal:
  - `topview-task-map.json.active_by_scene` stores only currently active task IDs per Scene ID;
  - `topview-task-map.json.processed_tasks` stores only a bounded recent dedup/statistics journal: `task_id`, `scene_id`, `final_status`, `finished_at`;
  - keep at most the most recent 200 processed tasks and do not persist queue/ETA history or permanent `attempts[]` / `active_attempts[]` trees.
- `SLOW` / `SLOW_PENDING` means that a Topview-managed scene currently has at least one active task in `init`, `queued`, `running` or `processing`.
- A new active task for an existing scene adds/returns that same Scene ID to canonical slow.
- If several tasks of one scene are active, canonical slow still contains the Scene ID once; all active task IDs remain in `active_by_scene`.
- When one task becomes terminal (`success`, `fail`, `failed`, `cancelled`), remove that task ID from active state and append/update the minimal processed journal.
- When the **last Topview-managed active task** for that scene becomes terminal, remove the Scene ID from canonical slow automatically. This changes only render state: **never auto-approve, never auto-rerun, and do not change editorial/production state because rendering ended**.
- Never auto-clear a canonical slow scene when there is no proven Topview active mapping; unknown/manual slow state is not cleared by guess.
- `topview-status.json` stays compact but exposes transient `active_tasks[]`: one telemetry object for every task that is active **right now**. It also keeps the backward-compatible current/primary scene snapshot plus `active_task_ids`. No terminal task history, queue history or ETA history is stored there.
- Control Center slow table deliberately shows **one row per active Topview task / occupied slot**. Therefore the same Scene ID may appear in several rows when it has several simultaneous renders. This is a slot view, not a duplicate-scene model.
- A new Scene ID is created only for a genuinely new creative scene. Ambiguous classification means no master write and user notification.

Principle: **keep only the state required for correctness and deduplication; detailed render history is not a permanent project entity**.

### Точное ТЗ — Topview slow slots, capacity = 6

Это постоянный UI/automation contract:

1. **Ёмкость:** Topview допускает максимум **6 одновременно активных slow-generation tasks**. `slot_capacity = 6`.
2. **Что занимает слот:** каждый отдельный Topview `task_id` в состоянии `init`, `queued`, `running` или `processing` занимает **ровно 1 слот**.
3. **Scene ID и слоты — разные счётчики:** canonical `slow_scenes` остаётся множеством уникальных Scene ID без дублей. Число slow Scene ID **нельзя** использовать как число занятых слотов.
4. **Повторный запуск той же сцены:** если одна Scene ID одновременно запущена 2–3 раза, она остаётся одной canonical scene, но занимает 2–3 Topview slot и должна появляться 2–3 отдельными строками в slow-таблице сайта.
5. **Заголовок сайта:** справа от `⏳ Сейчас в медленной генерации — Topview` всегда показывать динамический текст точно в формате:
   - `занято X из 6 · свободно Y`
   - `X` = количество реально активных `task_id`;
   - `Y = max(0, 6 - X)`.
   При текущих шести active tasks ожидаемый вид: **`занято 6 из 6 · свободно 0`**.
6. **Таблица:** одна строка = один active `task_id` = один занятый slot. Сохраняются прежние 8 колонок и их базовые пропорции: `#`, `Сцена`, `Модель`, `Статус`, `Запуск`, `Прошло`, `Очередь`, `Оценка времени`. Новую колонку `Attempt`/`Task ID` не добавлять. Если Scene ID повторяется, номер и название сцены повторяются в нескольких строках.
7. **Telemetry:** `topview-status.json` должен содержать:
   - `slot_capacity`;
   - `occupied_slots`;
   - `free_slots`;
   - transient `active_tasks[]`, где на каждый активный task есть как минимум `scene_id`, `task_id`, `model/model_id`, `topview_status`, `started_at`, `checked_at`, `queue_count`, provider wait/process estimates и verification/mapping confidence, если известны.
8. **Точность строки:** queue/ETA/status/start time каждой строки берутся **только из того task_id, которому принадлежит эта строка**. Не усреднять и не переносить очередь/ETA между параллельными попытками одной сцены.
9. **Primary scene snapshot:** scene-level поля в `topview-status.json` можно сохранять для обратной совместимости/других частей сайта, но они **не являются источником slot-count** и не заменяют `active_tasks[]`.
10. **Завершение:** terminal task (`success`, `fail`, `failed`, `cancelled`) немедленно перестаёт занимать slot и удаляется из `active_tasks[]`/`active_by_scene`. В minimal `processed_tasks` можно оставить только дедуп-факт.
11. **Slow lifecycle:** если у Scene ID остаётся хотя бы один active task, Scene ID остаётся canonical slow. Если завершается последний Topview-managed active task, watcher снимает только render slow-state; approval/editorial/production state не меняются автоматически.
12. **Over-capacity guard:** если из-за race/provider anomaly `occupied_slots > 6`, не скрывать проблему: показывать фактическое `занято X из 6 · свободно 0`, считать это warning и уведомлять пользователя/аудит.
13. **Никакой тяжёлой истории:** это правило не возвращает старую permanent `attempts[]` модель. `active_tasks[]` содержит только текущие активные задачи; после terminal state подробная telemetry не хранится бессрочно.
14. **Recovery/audit:** при проверке сайта и Topview state отдельно сверять `occupied_slots == len(active_tasks[]) == sum(len(active_by_scene[scene]))` и `free_slots == max(0, 6 - occupied_slots)`. Не сравнивать `occupied_slots` с количеством уникальных `slow_scenes`.
