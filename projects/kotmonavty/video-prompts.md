# Котмонавты — актуальные видео-сцены и промты

Канонический мастер проекта: `projects/kotmonavty/video-prompts.md`, GitHub main. Номера сцен независимы от других проектов. Общие правила — `projects/README.md` и 7 инструкций; своё — `INSTRUCTIONS.md`.

## 📌 РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС

**20.10.2026 · 2 сцен к генерации/доработке · 6 полных текстов промта**

- **🛠️ 0** рабочих направлений W: сюжетные предложения вынесены в `story-development.md` и не являются утверждёнными сценами.
- **⏳ 0** сцен сейчас в медленной генерации: **нет**.
- **Последняя оформленная активная сцена:** 2 — черновик, без запуска и без очереди.
- **Последняя полная синхронизация:** **20.10.2026 · сюжет, трейлер и референсы по команде владельца**.

**Все сцены DRAFT. Очередь оставлена без изменений.** [Сюжет и визуальный пакет](projects/kotmonavty/story-development.md). История и контрольные точки — `HANDOFF.md`.

## Оглавление сцен

| ID | Сцена | Персонажи и референсы | Что происходит |
|---|---|---|---|
| 1 | [Самый серьёзный заказ](#scene-1) | Лучик, Рыжик, бар | Брутальные коты лакают молоко |
| 2 | [Трейлер — Не тот груз](#scene-2) | Коты, корабль, кабина, компас, архив | Авантюрная галактическая погоня |

## Сцены в работе

Новых W-пунктов нет. Предложения эпизодов — в `story-development.md`; они не резервируют номера сцен и не попадают в очередь.

<a id="scene-1"></a>
## Сцена 1 — Самый серьёзный заказ

<!-- scene-meta: {"target_engine":"Seedance 2.0","production_state":"DRAFT","duration_s":30,"dialogue":{"enabled":false,"language":null},"dependencies":[],"tags":["owner_requested","draft","not_queued","two_engine_versions","reference_first"]} -->

**Черновик по задаче владельца 20.10.2026. В очередь не добавлять. Генерации не запускались.**

**Что происходит:** Лучик и Рыжик сидят за стойкой инопланетного бара и лакают языками молоко из рюмок. Чем грознее их лица и окружающие посетители, тем смешнее маленькие кошачьи действия.

**Готовность:** Все три статичных входа существуют и визуально проверены; сюжет сцены соответствует прямой команде владельца. Готов текст, но видеорезультата ещё нет. Техническая проверка изображения не является одобрением владельца.

**Второй ракурс и вариант завязки:** `projects/kotmonavty/references/development/KM-bar-compass.png`. Компас используется только в предложенном трейлере/сюжете; в самостоятельном барном промте он не появляется.

**Входные изображения и их роли:**
<div class="scene-ref-gallery">
<figure><a href="projects/kotmonavty/references/luchik.jpg" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/luchik.jpg" alt="Лучик — абсолютная идентичность" loading="lazy"></a><figcaption>@Image1 — Лучик — абсолютная идентичность</figcaption></figure>
<figure><a href="projects/kotmonavty/references/ryzhik.jpg" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/ryzhik.jpg" alt="Рыжик — абсолютная идентичность" loading="lazy"></a><figcaption>@Image2 — Рыжик — абсолютная идентичность</figcaption></figure>
<figure><a href="projects/kotmonavty/references/scenes/scene-1/KM01-bar-milk.png" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/scenes/scene-1/KM01-bar-milk.png" alt="Бар, расстановка, рюмки молока и серьёзные морды" loading="lazy"></a><figcaption>@Image3 — Бар, расстановка, рюмки молока и серьёзные морды</figcaption></figure>
</div>

**Две версии одной сцены:** Wan 3.0 — 30 с; Seedance 2.0 — 2 × 15 с. Для части 2 требуется настоящий результат части 1 как @Video1; его пока нет. Первая часть должна закончиться указанным переходным состоянием. Референсы загружаются в указанном порядке. Запуск возможен только по последующей команде, через безлимитный режим с ценой 0 кредитов.

<div class="engine-tabs" data-scene="1">
<div class="engine-pane" data-engine="wan30" data-main="1">

### Wan 3.0 · 30 секунд

```text
Mode: reference-to-video (omni-reference) | Duration: 30s | Resolution: 720p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal epic space-adventure deadpan comedy; serious cats in an alien bar

REFERENCES / AUTHORITY ORDER:
@Image1 — Лучик — абсолютная идентичность; file: projects/kotmonavty/references/luchik.jpg.
@Image2 — Рыжик — абсолютная идентичность; file: projects/kotmonavty/references/ryzhik.jpg.
@Image3 — Бар, расстановка, рюмки молока и серьёзные морды; file: projects/kotmonavty/references/scenes/scene-1/KM01-bar-milk.png.
Priority: original individual identities first; environment references control only their named locations; action keyframes control staging, never replace identity. Do not import incidental props or people from original references.

CHARACTER APPEARANCE / IDENTITY LOCK:
LUCHIK: exact grey-white long-haired domestic cat from @Image1, white muzzle/chest/paws, grey forehead and nose markings, serious light green-grey eyes. RYZHIK: exact ginger long-haired tabby from @Image2, dark orange stripes, pale chin, serious amber-green eyes. Real domestic-cat scale and anatomy, furred paws and tails, no clothes, no human hands. No identity blending. In cockpit Ryzhik is screen-left navigator and Luchik screen-right pilot; outside cockpit follow shot staging.

START STATE:
Both cats sit on separate high stools at the same brass bar, Luchik left and Ryzhik right. Exactly two short wide shot glasses of white milk rest on the counter, one in front of each cat. Large reptilian bartender behind. No compass in this standalone scene.

TIMELINE:
[0:00–0:04] Low travelling reveal along the bar brings both serious cats and their two milk shots into view; background aliens turn toward the pair.

[0:04–0:09] Cut to clear low close-up: both cats lean down and repeatedly lap milk with visible pink tongues. Tiny concentric ripples, paws braced beside glasses.

[0:09–0:14] Widen to their faces: Luchik stops first and gives the room a hard stare; Ryzhik continues two brisk laps, then raises his head with a small milk drop on whisker.

[0:14–0:20] The massive bartender stops polishing a glass and studies them. Cats turn only their eyes toward him, then forward. Short purposeful reaction, no smile.

[0:20–0:25] Ryzhik presses his glass a few centimetres forward with one furry paw; Luchik pins his own glass steadily with a paw. Quiet glass clink, controlled physical contact.

[0:25–0:30] Both lean in for one decisive last lap, sit up sternly in synchrony. Pull back to the intimidating bar and absurdly small milk shots; end on the milk drop, no mugging.

END STATE:
Both cats remain at the counter, glasses set down, look straight ahead with absolute hardened seriousness; a tiny milk drop clings to Ryzhik's whisker.

CAMERA / SPACE:
Maintain left/right identities and counter geography. Low eye-level two-shot, motivated cut to tongues and glasses, reaction two-shot, final gentle pullback. Real-time movement; no slow-motion. No teleportation between stools.

PERFORMANCE:
Dry absolute seriousness, narrowed attentive eyes, ears tracking bar sounds. Repeated clear feline tongue lapping with tiny head and jaw motion; natural lively micro-actions, not frozen posing. Cats never lift or toast glasses with hands. The pause before the final lap is an intentional short comic beat.

LIGHTING / MATERIALS:
Warm amber lamps, cyan spaceport window rim, photoreal individual fur strands, worn brass, transparent thick glass, opaque white milk with physically plausible ripples.

AUDIO:
Quiet alien bar murmur, soft engine bass, distinct tiny lap-lap sounds, one glass clink. Original restrained brass swagger and pizzicato pulse; music briefly drops for the final audible lap. No dialogue, no narration, no sung words. Original music only, no recognizable existing melodies.

NEGATIVE PROMPT:
Human hands, human faces on cats, dressed cats, altered fur markings, giant cats, duplicate cats, extra limbs, broken tongues, fused glasses, drinking alcohol, floating props without physical cause, arbitrary ship redesign, franchise characters, subtitles, text overlays, logos added as titles, watermark, static slideshow, unmotivated idle holds.

FRAME FILL / NO BARS:
Fill the entire generated 16:9 frame edge to edge. No letterbox, pillarbox, black bars, embedded borders, split screens or poster layouts.
```

</div>
<div class="engine-pane" data-engine="sd20x2">

### Seedance 2.0 · часть 1 · 15 секунд

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | Photoreal epic space-adventure deadpan comedy; serious cats in an alien bar

REFERENCES / AUTHORITY ORDER:
@Image1 — Лучик — абсолютная идентичность; file: projects/kotmonavty/references/luchik.jpg.
@Image2 — Рыжик — абсолютная идентичность; file: projects/kotmonavty/references/ryzhik.jpg.
@Image3 — Бар, расстановка, рюмки молока и серьёзные морды; file: projects/kotmonavty/references/scenes/scene-1/KM01-bar-milk.png.
Priority: original individual identities first; environment references control only their named locations; action keyframes control staging, never replace identity. Do not import incidental props or people from original references.

CHARACTER APPEARANCE / IDENTITY LOCK:
LUCHIK: exact grey-white long-haired domestic cat from @Image1, white muzzle/chest/paws, grey forehead and nose markings, serious light green-grey eyes. RYZHIK: exact ginger long-haired tabby from @Image2, dark orange stripes, pale chin, serious amber-green eyes. Real domestic-cat scale and anatomy, furred paws and tails, no clothes, no human hands. No identity blending. In cockpit Ryzhik is screen-left navigator and Luchik screen-right pilot; outside cockpit follow shot staging.

START STATE:
Both cats sit on separate high stools at the same brass bar, Luchik left and Ryzhik right. Exactly two short wide shot glasses of white milk rest on the counter, one in front of each cat. Large reptilian bartender behind. No compass in this standalone scene.

TIMELINE:
[0:00–0:04] Low travelling reveal along the bar brings both serious cats and their two milk shots into view; background aliens turn toward the pair.

[0:04–0:10] Cut to clear low close-up: both cats lean down and repeatedly lap milk with visible pink tongues. Tiny concentric ripples, paws braced beside glasses.

[0:10–0:15] Widen to their faces: Luchik stops first and gives the room a hard stare; Ryzhik continues two brisk laps, then raises his head with a small milk drop on whisker. End exactly in the close two-shot described in END STATE.

END STATE:
Close two-shot: cats have just lifted their heads from the milk. Ryzhik has one small milk drop on his whisker. Two glasses remain on the counter in their original positions; bartender pauses behind.

CAMERA / SPACE:
Maintain left/right identities and counter geography. Low eye-level two-shot, motivated cut to tongues and glasses, reaction two-shot, final gentle pullback. Real-time movement; no slow-motion. No teleportation between stools.

PERFORMANCE:
Dry absolute seriousness, narrowed attentive eyes, ears tracking bar sounds. Repeated clear feline tongue lapping with tiny head and jaw motion; natural lively micro-actions, not frozen posing. Cats never lift or toast glasses with hands. The pause before the final lap is an intentional short comic beat.

LIGHTING / MATERIALS:
Warm amber lamps, cyan spaceport window rim, photoreal individual fur strands, worn brass, transparent thick glass, opaque white milk with physically plausible ripples.

AUDIO:
Quiet alien bar murmur, soft engine bass, distinct tiny lap-lap sounds, one glass clink. Original restrained brass swagger and pizzicato pulse; music briefly drops for the final audible lap. No dialogue, no narration, no sung words. Original music only, no recognizable existing melodies.

NEGATIVE PROMPT:
Human hands, human faces on cats, dressed cats, altered fur markings, giant cats, duplicate cats, extra limbs, broken tongues, fused glasses, drinking alcohol, floating props without physical cause, arbitrary ship redesign, franchise characters, subtitles, text overlays, logos added as titles, watermark, static slideshow, unmotivated idle holds.

FRAME FILL / NO BARS:
Fill the entire generated 16:9 frame edge to edge. No letterbox, pillarbox, black bars, embedded borders, split screens or poster layouts.
```

### Seedance 2.0 · часть 2 · 15 секунд

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | Photoreal epic space-adventure deadpan comedy; serious cats in an alien bar

REFERENCES / AUTHORITY ORDER:
@Video1 — the actual completed Part 1 of THIS scene, final frame, positions, motion and lighting; begin on that exact ending, not on a recreated still.
@Image1 — Лучик — абсолютная идентичность; file: projects/kotmonavty/references/luchik.jpg.
@Image2 — Рыжик — абсолютная идентичность; file: projects/kotmonavty/references/ryzhik.jpg.
@Image3 — Бар, расстановка, рюмки молока и серьёзные морды; file: projects/kotmonavty/references/scenes/scene-1/KM01-bar-milk.png.
Priority: original individual identities first; environment references control only their named locations; action keyframes control staging, never replace identity. Do not import incidental props or people from original references.

CHARACTER APPEARANCE / IDENTITY LOCK:
LUCHIK: exact grey-white long-haired domestic cat from @Image1, white muzzle/chest/paws, grey forehead and nose markings, serious light green-grey eyes. RYZHIK: exact ginger long-haired tabby from @Image2, dark orange stripes, pale chin, serious amber-green eyes. Real domestic-cat scale and anatomy, furred paws and tails, no clothes, no human hands. No identity blending. In cockpit Ryzhik is screen-left navigator and Luchik screen-right pilot; outside cockpit follow shot staging.

START STATE:
Continue @Video1 exactly: Close two-shot: cats have just lifted their heads from the milk. Ryzhik has one small milk drop on his whisker. Two glasses remain on the counter in their original positions; bartender pauses behind.

TIMELINE:
[0:00–0:01] Continue the actual final frame of Part 1 without resetting positions, milk level or whisker drop.

[0:01–0:06] The massive bartender stops polishing a glass and studies them. Cats turn only their eyes toward him, then forward. Short purposeful reaction, no smile.

[0:06–0:10] Ryzhik presses his glass a few centimetres forward with one furry paw; Luchik pins his own glass steadily with a paw. Quiet glass clink, controlled physical contact.

[0:10–0:15] Both lean in for one decisive last lap, sit up sternly in synchrony. Pull back to the intimidating bar and absurdly small milk shots; end on the milk drop, no mugging.

END STATE:
Both cats remain at the counter, glasses set down, look straight ahead with absolute hardened seriousness; a tiny milk drop clings to Ryzhik's whisker.

CAMERA / SPACE:
Maintain left/right identities and counter geography. Low eye-level two-shot, motivated cut to tongues and glasses, reaction two-shot, final gentle pullback. Real-time movement; no slow-motion. No teleportation between stools.

PERFORMANCE:
Dry absolute seriousness, narrowed attentive eyes, ears tracking bar sounds. Repeated clear feline tongue lapping with tiny head and jaw motion; natural lively micro-actions, not frozen posing. Cats never lift or toast glasses with hands. The pause before the final lap is an intentional short comic beat.

LIGHTING / MATERIALS:
Warm amber lamps, cyan spaceport window rim, photoreal individual fur strands, worn brass, transparent thick glass, opaque white milk with physically plausible ripples.

AUDIO:
Quiet alien bar murmur, soft engine bass, distinct tiny lap-lap sounds, one glass clink. Original restrained brass swagger and pizzicato pulse; music briefly drops for the final audible lap. No dialogue, no narration, no sung words. Original music only, no recognizable existing melodies.

NEGATIVE PROMPT:
Human hands, human faces on cats, dressed cats, altered fur markings, giant cats, duplicate cats, extra limbs, broken tongues, fused glasses, drinking alcohol, floating props without physical cause, arbitrary ship redesign, franchise characters, subtitles, text overlays, logos added as titles, watermark, static slideshow, unmotivated idle holds.

FRAME FILL / NO BARS:
Fill the entire generated 16:9 frame edge to edge. No letterbox, pillarbox, black bars, embedded borders, split screens or poster layouts.
```

</div>
</div>

<a id="scene-2"></a>
## Сцена 2 — Трейлер — Не тот груз

<!-- scene-meta: {"target_engine":"Seedance 2.0","production_state":"DRAFT","duration_s":30,"dialogue":{"enabled":false,"language":null},"dependencies":[],"tags":["owner_requested","draft","not_queued","two_engine_versions","reference_first"]} -->

**Черновик по задаче владельца 20.10.2026. В очередь не добавлять. Генерации не запускались.**

**Что происходит:** Молоко в баре → чужой звёздный компас → погоня на исходном корабле → активная работа в знакомой кабине → пробуждение древнего архива и бегство → невозмутимый глоток молока.

**Готовность:** Все семь статичных входов подготовлены. Трейлер остаётся DRAFT до выбора владельцем сюжетной линии; часть 2 Seedance зависит от будущего результата части 1. Техническая проверка изображения не является одобрением владельца.

**Сюжетный статус:** рабочее предложение «Не тот груз», не утверждённый финальный сюжет. Исходные коты, корабль и кабина сохранены; новые события подготовлены как концепт трейлера. Подробный монтажный план и шесть эпизодов — `story-development.md`.

**Входные изображения и их роли:**
<div class="scene-ref-gallery">
<figure><a href="projects/kotmonavty/references/luchik.jpg" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/luchik.jpg" alt="Лучик — морда и шерсть" loading="lazy"></a><figcaption>@Image1 — Лучик — морда и шерсть</figcaption></figure>
<figure><a href="projects/kotmonavty/references/ryzhik.jpg" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/ryzhik.jpg" alt="Рыжик — морда и шерсть" loading="lazy"></a><figcaption>@Image2 — Рыжик — морда и шерсть</figcaption></figure>
<figure><a href="projects/kotmonavty/references/ship-exterior-front.png" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/ship-exterior-front.png" alt="Исходный выбранный корабль — абсолютный дизайн" loading="lazy"></a><figcaption>@Image3 — Исходный выбранный корабль — абсолютный дизайн</figcaption></figure>
<figure><a href="projects/kotmonavty/references/ship-interior-cockpit.png" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/ship-interior-cockpit.png" alt="Кабина: Рыжик слева, Лучик справа" loading="lazy"></a><figcaption>@Image4 — Кабина: Рыжик слева, Лучик справа</figcaption></figure>
<figure><a href="projects/kotmonavty/references/development/KM-bar-compass.png" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/development/KM-bar-compass.png" alt="Бар, бармен и звёздный компас" loading="lazy"></a><figcaption>@Image5 — Бар, бармен и звёздный компас</figcaption></figure>
<figure><a href="projects/kotmonavty/references/development/KM-ring-chase.png" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/development/KM-ring-chase.png" alt="Погоня и орбитальное кольцо" loading="lazy"></a><figcaption>@Image6 — Погоня и орбитальное кольцо</figcaption></figure>
<figure><a href="projects/kotmonavty/references/development/KM-star-vault.png" target="_blank" rel="noopener"><img src="projects/kotmonavty/references/development/KM-star-vault.png" alt="Звёздный архив, мост и компас" loading="lazy"></a><figcaption>@Image7 — Звёздный архив, мост и компас</figcaption></figure>
</div>

**Две версии одной сцены:** Wan 3.0 — 30 с; Seedance 2.0 — 2 × 15 с. Для части 2 требуется настоящий результат части 1 как @Video1; его пока нет. Первая часть должна закончиться указанным переходным состоянием. Референсы загружаются в указанном порядке. Запуск возможен только по последующей команде, через безлимитный режим с ценой 0 кредитов.

<div class="engine-tabs" data-scene="2">
<div class="engine-pane" data-engine="wan30" data-main="1">

### Wan 3.0 · 30 секунд

```text
Mode: reference-to-video (omni-reference) | Duration: 30s | Resolution: 720p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Original epic galactic adventure comedy, photoreal cats and spacecraft, energetic cinematic trailer montage

REFERENCES / AUTHORITY ORDER:
@Image1 — Лучик — морда и шерсть; file: projects/kotmonavty/references/luchik.jpg.
@Image2 — Рыжик — морда и шерсть; file: projects/kotmonavty/references/ryzhik.jpg.
@Image3 — Исходный выбранный корабль — абсолютный дизайн; file: projects/kotmonavty/references/ship-exterior-front.png.
@Image4 — Кабина: Рыжик слева, Лучик справа; file: projects/kotmonavty/references/ship-interior-cockpit.png.
@Image5 — Бар, бармен и звёздный компас; file: projects/kotmonavty/references/development/KM-bar-compass.png.
@Image6 — Погоня и орбитальное кольцо; file: projects/kotmonavty/references/development/KM-ring-chase.png.
@Image7 — Звёздный архив, мост и компас; file: projects/kotmonavty/references/development/KM-star-vault.png.
Priority: original individual identities first; environment references control only their named locations; action keyframes control staging, never replace identity. Do not import incidental props or people from original references.

CHARACTER APPEARANCE / IDENTITY LOCK:
LUCHIK: exact grey-white long-haired domestic cat from @Image1, white muzzle/chest/paws, grey forehead and nose markings, serious light green-grey eyes. RYZHIK: exact ginger long-haired tabby from @Image2, dark orange stripes, pale chin, serious amber-green eyes. Real domestic-cat scale and anatomy, furred paws and tails, no clothes, no human hands. No identity blending. In cockpit Ryzhik is screen-left navigator and Luchik screen-right pilot; outside cockpit follow shot staging.

START STATE:
In the alien bar of @Image5, Luchik left and Ryzhik right sit on stools lapping white milk from short wide shot glasses, faces brutally serious. The brass spherical compass is initially beneath the bartender's claw.

TIMELINE:
[0:00–0:04] Bar close two-shot: both cats lap milk with deadly serious expressions. Bartender slides the brass cyan-core compass onto the counter; eyes follow it without smiling.

[0:04–0:08] Match cut from compass ring to the hero ship: it accelerates away through an orbital harbor gap, two blue rear plumes extending. Three unmanned drones swing into pursuit behind.

[0:08–0:13] Cut exterior @Image6: hero ship banks hard through a broken ring opening. Orange drone bolts strike the pillar behind; debris passes with strong parallax, ship stays intact.

[0:13–0:17] Cut cockpit @Image4: Luchik right makes a decisive control movement; Ryzhik left braces and taps one navigation pad. Their bodies lean under inertia, no human hands.

[0:17–0:25] Hard cut to @Image7: compass ignites the enormous star atlas. Rings turn, bridge behind starts breaking. Cats instantly lower their bodies and sprint together toward camera along the remaining bridge, then leap across one small crack; both land safely, identities unchanged.

[0:25–0:30] Smash cut back to the bar. The two cats sit with renewed milk shots, equally stern; one final audible lap as music drops, then the compass pulses. No explanation, no title card.

END STATE:
Back in the original alien bar, both stern cats sit with fresh milk shots. Ryzhik makes one tiny final lap; the brass compass between them pulses cyan once. The wider adventure remains unresolved.

CAMERA / SPACE:
A clear trailer montage with motivated hard cuts: milk circle to compass ring, blue flash to engine plume, star-map glow to bar glass reflection. Never morph one location into another. Exterior ship retains long ivory battered hull, red swoosh, blue stripe, front faceted amber cockpit and cylindrical rear engines from @Image3. Action has readable travel direction and real momentum.

PERFORMANCE:
Cats remain recognisably real cats. Bar comedy uses short precise lapping and stern looks. Flight uses fast evasive movement, planted paws and reactive ears; vault escape uses immediate low four-paw sprint and leap. No smiling anthropomorphic mugging, no slow idle drifting during danger.

LIGHTING / MATERIALS:
Photoreal fur, worn hull metal, amber cockpit, cyan star core, orange sparks, massive orbital structures and ancient bronze machinery. Match each reference environment; preserve exposure and identity across cuts.

AUDIO:
Original adventurous symphonic score: bold brass, agile strings, unusual mysterious percussion, escalating driving rhythm. Milk laps and glass clink lead into engine surge and debris impact, then vast mechanism resonance; brief comic music stop for final lap. No copied themes. No dialogue, no narration, no sung words. Original music only, no recognizable existing melodies.

NEGATIVE PROMPT:
Human hands, human faces on cats, dressed cats, altered fur markings, giant cats, duplicate cats, extra limbs, broken tongues, fused glasses, drinking alcohol, floating props without physical cause, arbitrary ship redesign, franchise characters, subtitles, text overlays, logos added as titles, watermark, static slideshow, unmotivated idle holds.

FRAME FILL / NO BARS:
Fill the entire generated 16:9 frame edge to edge. No letterbox, pillarbox, black bars, embedded borders, split screens or poster layouts.
```

</div>
<div class="engine-pane" data-engine="sd20x2">

### Seedance 2.0 · часть 1 · 15 секунд

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | Original epic galactic adventure comedy, photoreal cats and spacecraft, energetic cinematic trailer montage

REFERENCES / AUTHORITY ORDER:
@Image1 — Лучик — морда и шерсть; file: projects/kotmonavty/references/luchik.jpg.
@Image2 — Рыжик — морда и шерсть; file: projects/kotmonavty/references/ryzhik.jpg.
@Image3 — Исходный выбранный корабль — абсолютный дизайн; file: projects/kotmonavty/references/ship-exterior-front.png.
@Image4 — Кабина: Рыжик слева, Лучик справа; file: projects/kotmonavty/references/ship-interior-cockpit.png.
@Image5 — Бар, бармен и звёздный компас; file: projects/kotmonavty/references/development/KM-bar-compass.png.
@Image6 — Погоня и орбитальное кольцо; file: projects/kotmonavty/references/development/KM-ring-chase.png.
@Image7 — Звёздный архив, мост и компас; file: projects/kotmonavty/references/development/KM-star-vault.png.
Priority: original individual identities first; environment references control only their named locations; action keyframes control staging, never replace identity. Do not import incidental props or people from original references.

CHARACTER APPEARANCE / IDENTITY LOCK:
LUCHIK: exact grey-white long-haired domestic cat from @Image1, white muzzle/chest/paws, grey forehead and nose markings, serious light green-grey eyes. RYZHIK: exact ginger long-haired tabby from @Image2, dark orange stripes, pale chin, serious amber-green eyes. Real domestic-cat scale and anatomy, furred paws and tails, no clothes, no human hands. No identity blending. In cockpit Ryzhik is screen-left navigator and Luchik screen-right pilot; outside cockpit follow shot staging.

START STATE:
In the alien bar of @Image5, Luchik left and Ryzhik right sit on stools lapping white milk from short wide shot glasses, faces brutally serious. The brass spherical compass is initially beneath the bartender's claw.

TIMELINE:
[0:00–0:04] Bar close two-shot: both cats lap milk with deadly serious expressions. Bartender slides the brass cyan-core compass onto the counter; eyes follow it without smiling.

[0:04–0:07] Match cut from compass ring to the hero ship: it accelerates away through an orbital harbor gap, two blue rear plumes extending. Three unmanned drones swing into pursuit behind.

[0:07–0:12] Cut exterior @Image6: hero ship banks hard through a broken ring opening. Orange drone bolts strike the pillar behind; debris passes with strong parallax, ship stays intact.

[0:12–0:15] Cut cockpit @Image4: Luchik right makes a decisive control movement; Ryzhik left braces and taps one navigation pad. Their bodies lean under inertia, no human hands. End on the cockpit two-shot before the blue flash fades.

END STATE:
Cockpit medium two-shot at the end of an evasive bank: Ryzhik at screen-left has his furry paw braced over the amber navigation panel, Luchik at screen-right grips the pilot control with feline paws. Both lean left under inertia; blue emergency light flashes once.

CAMERA / SPACE:
A clear trailer montage with motivated hard cuts: milk circle to compass ring, blue flash to engine plume, star-map glow to bar glass reflection. Never morph one location into another. Exterior ship retains long ivory battered hull, red swoosh, blue stripe, front faceted amber cockpit and cylindrical rear engines from @Image3. Action has readable travel direction and real momentum.

PERFORMANCE:
Cats remain recognisably real cats. Bar comedy uses short precise lapping and stern looks. Flight uses fast evasive movement, planted paws and reactive ears; vault escape uses immediate low four-paw sprint and leap. No smiling anthropomorphic mugging, no slow idle drifting during danger.

LIGHTING / MATERIALS:
Photoreal fur, worn hull metal, amber cockpit, cyan star core, orange sparks, massive orbital structures and ancient bronze machinery. Match each reference environment; preserve exposure and identity across cuts.

AUDIO:
Original adventurous symphonic score: bold brass, agile strings, unusual mysterious percussion, escalating driving rhythm. Milk laps and glass clink lead into engine surge and debris impact, then vast mechanism resonance; brief comic music stop for final lap. No copied themes. No dialogue, no narration, no sung words. Original music only, no recognizable existing melodies.

NEGATIVE PROMPT:
Human hands, human faces on cats, dressed cats, altered fur markings, giant cats, duplicate cats, extra limbs, broken tongues, fused glasses, drinking alcohol, floating props without physical cause, arbitrary ship redesign, franchise characters, subtitles, text overlays, logos added as titles, watermark, static slideshow, unmotivated idle holds.

FRAME FILL / NO BARS:
Fill the entire generated 16:9 frame edge to edge. No letterbox, pillarbox, black bars, embedded borders, split screens or poster layouts.
```

### Seedance 2.0 · часть 2 · 15 секунд

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | Original epic galactic adventure comedy, photoreal cats and spacecraft, energetic cinematic trailer montage

REFERENCES / AUTHORITY ORDER:
@Video1 — the actual completed Part 1 of THIS scene, final frame, positions, motion and lighting; begin on that exact ending, not on a recreated still.
@Image1 — Лучик — морда и шерсть; file: projects/kotmonavty/references/luchik.jpg.
@Image2 — Рыжик — морда и шерсть; file: projects/kotmonavty/references/ryzhik.jpg.
@Image3 — Исходный выбранный корабль — абсолютный дизайн; file: projects/kotmonavty/references/ship-exterior-front.png.
@Image4 — Кабина: Рыжик слева, Лучик справа; file: projects/kotmonavty/references/ship-interior-cockpit.png.
@Image5 — Бар, бармен и звёздный компас; file: projects/kotmonavty/references/development/KM-bar-compass.png.
@Image6 — Погоня и орбитальное кольцо; file: projects/kotmonavty/references/development/KM-ring-chase.png.
@Image7 — Звёздный архив, мост и компас; file: projects/kotmonavty/references/development/KM-star-vault.png.
Priority: original individual identities first; environment references control only their named locations; action keyframes control staging, never replace identity. Do not import incidental props or people from original references.

CHARACTER APPEARANCE / IDENTITY LOCK:
LUCHIK: exact grey-white long-haired domestic cat from @Image1, white muzzle/chest/paws, grey forehead and nose markings, serious light green-grey eyes. RYZHIK: exact ginger long-haired tabby from @Image2, dark orange stripes, pale chin, serious amber-green eyes. Real domestic-cat scale and anatomy, furred paws and tails, no clothes, no human hands. No identity blending. In cockpit Ryzhik is screen-left navigator and Luchik screen-right pilot; outside cockpit follow shot staging.

START STATE:
Exact @Video1 ending: Cockpit medium two-shot at the end of an evasive bank: Ryzhik at screen-left has his furry paw braced over the amber navigation panel, Luchik at screen-right grips the pilot control with feline paws. Both lean left under inertia; blue emergency light flashes once.

TIMELINE:
[0:00–0:02] Continue actual @Video1 cockpit end frame; complete the bank and let the blue light flash fade.

[0:02–0:06] Hard cut to star vault @Image7. Compass activates overhead atlas; rings awaken with a cyan wave.

[0:06–0:11] Bridge behind fractures. Both cats react instantly, sprint on all four paws toward foreground and leap a short crack. Hold clear screen direction and show both landing, no teleportation.

[0:11–0:15] Smash cut back to the bar. The two cats sit with renewed milk shots, equally stern; one final audible lap as music drops, then the compass pulses. No explanation, no title card.

END STATE:
Back in the original alien bar, both stern cats sit with fresh milk shots. Ryzhik makes one tiny final lap; the brass compass between them pulses cyan once. The wider adventure remains unresolved.

CAMERA / SPACE:
A clear trailer montage with motivated hard cuts: milk circle to compass ring, blue flash to engine plume, star-map glow to bar glass reflection. Never morph one location into another. Exterior ship retains long ivory battered hull, red swoosh, blue stripe, front faceted amber cockpit and cylindrical rear engines from @Image3. Action has readable travel direction and real momentum.

PERFORMANCE:
Cats remain recognisably real cats. Bar comedy uses short precise lapping and stern looks. Flight uses fast evasive movement, planted paws and reactive ears; vault escape uses immediate low four-paw sprint and leap. No smiling anthropomorphic mugging, no slow idle drifting during danger.

LIGHTING / MATERIALS:
Photoreal fur, worn hull metal, amber cockpit, cyan star core, orange sparks, massive orbital structures and ancient bronze machinery. Match each reference environment; preserve exposure and identity across cuts.

AUDIO:
Original adventurous symphonic score: bold brass, agile strings, unusual mysterious percussion, escalating driving rhythm. Milk laps and glass clink lead into engine surge and debris impact, then vast mechanism resonance; brief comic music stop for final lap. No copied themes. No dialogue, no narration, no sung words. Original music only, no recognizable existing melodies.

NEGATIVE PROMPT:
Human hands, human faces on cats, dressed cats, altered fur markings, giant cats, duplicate cats, extra limbs, broken tongues, fused glasses, drinking alcohol, floating props without physical cause, arbitrary ship redesign, franchise characters, subtitles, text overlays, logos added as titles, watermark, static slideshow, unmotivated idle holds.

FRAME FILL / NO BARS:
Fill the entire generated 16:9 frame edge to edge. No letterbox, pillarbox, black bars, embedded borders, split screens or poster layouts.
```

</div>
</div>
