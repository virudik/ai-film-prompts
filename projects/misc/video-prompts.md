# 🎲 Разное — актуальные видео-сцены и промты

Канонический мастер: `projects/misc/video-prompts.md`, GitHub main. Новые независимые ролики. Правила: `projects/README.md` и `projects/misc/INSTRUCTIONS.md`.

## 📌 РЕВИЗИЯ / ТЕКУЩИЙ СТАТУС

**01.11.2026 · 1 сцена к генерации/доработке · 12 полных текстов промта (4 × 30 с + 8 × 15 с)**

- **🛠️ 0** рабочих направлений W.
- **⏳ 0** сцен сейчас в медленной генерации: **нет**.
- **Последняя полная синхронизация:** **01.11.2026 · сцена 1 «Тихий маяк» (DRAFT): две версии — 4 ролика B1–B4 по 30 с (Wan 3.0 / Seedance 2.5, русская озвучка Ярика в промте) и 8 подсцен A1–A8 по 15 с (Seedance 2.0), формат 9:16 вертикаль, без картинок и запусков; картинки и видео пока не делаем по решению владельца**.

## Оглавление сцен

| ID | Сцена | Персонажи | Что происходит |
|---|---|---|---|
| 1 | [Тихий маяк — история Ярика](#scene-1) | Ярик, мама Лена, Соня, Анна Сергеевна, пёс Бублик, Варя | Мальчик с особенностями развития рассказывает о громком внутреннем мире и о людях, которые становятся его маяком. 4 ролика по 30 с (B1–B4) или 8 подсцен по 15 с (A1–A8) |

## Сцены в работе

Сцена 1 — черновик: референсов и запусков ещё нет. Старые космические сцены находятся в проекте Роскосмос.

<a id="scene-1"></a>
## Сцена 1 — Тихий маяк (история Ярика)

<!-- scene-meta: {"target_engine":"Wan 3.0","production_state":"DRAFT","duration_s":120,"dialogue":{"enabled":true,"language":"ru"},"dependencies":[],"tags":["owner_requested","draft","original_story","voiceover_ru","vertical_9x16","two_engine_versions","reference_first","misc_scene_1","eight_subscenes"]} -->

**Контекст использования:** оригинальный ролик около 2 минут о мальчике Ярике (7 лет) с особенностями развития, рассказ от первого лица детским голосом по-русски. От громкого внутреннего мира и страхов к поддержке и надежде. Вдохновлён общим настроением чужого рилса, но все герои, места и сюжет собственные; текст, герои и сбор средств оригинала не используются.

**Что происходит:** Ярику семь лет, и обычные звуки для него слишком громкие. Во дворе он прячется в тень и выкладывает морские стёклышки, внутри него — штормовое море, где слова уплывают, как лодки. Тяжёлое утро заканчивается слезами, но ночью старшая сестра Соня приносит маяк-ночник и жёлтые наушники, а пёс Бублик ложится ему на ноги. Анна Сергеевна терпеливо ждёт, и Ярик впервые выкладывает три картинки: «я — хочу — тихо». Во дворе рядом садится Варя. На закате семья обнимает его на берегу у настоящего маяка.

**Готовность:** DRAFT. Решение владельца 01.11.2026: картинки и видео пока не делаем, только сцена и промты на сайте. Референсов ещё нет (18 картинок в плане, список — в `projects/misc/character-references.json`, поле `provenance.planned_reference_images`); промты ссылаются на них как на плановые @Image. Запусков не было, Topview-очередь пуста. Техническая проверка изображения не является одобрением владельца.
**Формат кадра:** вертикаль 9:16 (720×1280), как в оригинальном рилсе — решение владельца 01.11.2026. Во всех 12 промтах `Aspect ratio: 9:16`, `FRAME FILL` для портретного кадра, вертикальная композиция и запрет горизонтальных/letterbox-кадров. **Запуск в Topview — только с форматом 9:16** (очередь и общие инструкции репозитория по умолчанию 16:9: при создании пункта очереди и на сайте Topview выставить 9:16 отдельно). Референсы локаций, реквизита и ключевые кадры K1–K8 — вертикальные 9:16; листы персонажей — горизонтальные листы-развёртки (как во всём репозитории), они задают только внешность.

**Монтажная роль:** целый короткий фильм; порядок B1→B4 (30 с) или A1→A8 (15 с), B1 = A1 + A2, B2 = A3 + A4, B3 = A5 + A6, B4 = A7 + A8. В 30-секундной версии русский закадровый голос Ярика внутри промта (Wan 3.0); в 15-секундной клипы тихие, текст записывается отдельно и кладётся по таймингам. Музыка и титры добавляются в редакторе.

**Закадровый текст целиком (RU, для озвучки; ~20 слов на 15 с, детский голос, спокойно):**

- **A1** [0:01–0:05] «Меня зовут Ярик. Мне семь лет.»
- **A1** [0:06–0:15] «Чайник свистит, как поезд. Часы стучат, как молотки. Мир у меня внутри — очень громкий.»
- **A2** [0:01–0:07] «Во дворе все смеются и кричат. Для меня это — как огромная волна.»
- **A2** [0:08–0:15] «Я не злюсь. Я выкладываю стёклышки в ряд. Они тихие.»
- **A3** [0:01–0:07] «Внутри у меня море. Когда начинается шторм, слова уплывают, как лодки.»
- **A3** [0:08–0:15] «Я знаю, что хочу сказать. Но слова не слушаются.»
- **A4** [0:01–0:06] «Иногда у меня внутри всё взрывается. Новые ботинки колются, а время бежит.»
- **A4** [0:07–0:15] «Я плачу — по-другому не умею. Мама устала. Мне так жалко её. И себя.»
- **A5** [0:01–0:07] «Ночью пришла Соня. Она принесла маяк и жёлтые наушники.»
- **A5** [0:08–0:15] «Она сказала: „Чтобы море стало тише“. Бублик лёг рядом — тёплый и тяжёлый.»
- **A6** [0:01–0:06] «Анна Сергеевна никогда не торопит. Она умеет ждать.»
- **A6** [0:07–0:15] «Сегодня я выложил три картинки: „я“, „хочу“, „тихо“. И меня поняли.»
- **A7** [0:01–0:07] «Во дворе всё так же шумно. Но теперь у меня есть наушники.»
- **A7** [0:08–0:15] «Одна девочка села рядом. Я дал ей самое красивое стёклышко.»
- **A8** [0:01–0:05] «Мой мир всё ещё громкий.»
- **A8** [0:06–0:10] «Но у меня есть маяк — это те, кто рядом.»
- **A8** [0:11–0:15] «Просто побудьте рядом. Этого достаточно.»

_Всего ≈ 169 слов за 120 с: оставлено время на паузы и музыку._

**Две версии одной сцены:** **30 с · Wan 3.0 / Seedance 2.5** — четыре ролика B1–B4 (основная вкладка: речь по-русски идёт на Wan) и **Seedance 2.0 · 15 с** — восемь роликов A1–A8. Обе версии рассказывают одну историю с теми же репликами; ключевые кадры и референсы по подсценам A1–A8 годятся для обеих. Вкладка — выбор владельца, не разрешение на запуск.

<div class="engine-tabs" data-scene="1">
<div class="engine-pane" data-engine="wan30" data-main="1">

### 30 с · Wan 3.0 / Seedance 2.5 — четыре ролика B1–B4 с русской озвучкой Ярика

Один текст на оба движка (PROMPT-STYLE-GUIDE §7А); основной движок — Wan 3.0, потому что в промте русская речь. Ролик = две подсцены: B1 = A1 + A2, B2 = A3 + A4, B3 = A5 + A6, B4 = A7 + A8. Реплики Ярика идут закадровым голосом внутри промта (тайминг сдвинут на +15 с для второй половины). Входов на ролик 5–6, у B3–B4 часть реквизита и двор описаны текстом. Порядок для монтажа B1→B4. Запусков не было.

#### B1 · Wan 3.0 · 30 с · Громкий мир (A1 + A2)

**Что происходит:** Утро на кухне. Обычные звуки (ложка, часы, чайник) для Ярика видны как цветные звуковые формы и становятся слишком громкими. Он закрывает уши, мама мягко приглушает плиту и кладёт руку ему на спину. Затем: Двор с площадкой. Смех и крики детей накатывают на Ярика волной. Он отступает в тень горки и тихо выкладывает в ряд морские стёклышки.

**Закадровый текст Ярика (внутри промта, русский, голос ребёнка):**
- [0:01–0:05] «Меня зовут Ярик. Мне семь лет.»
- [0:06–0:15] «Чайник свистит, как поезд. Часы стучат, как молотки. Мир у меня внутри — очень громкий.»
- [0:16–0:22] «Во дворе все смеются и кричат. Для меня это — как огромная волна.»
- [0:23–0:30] «Я не злюсь. Я выкладываю стёклышки в ряд. Они тихие.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Мама Лена — основной лист · @Image3 = Кухня · @Image4 = Двор с площадкой · @Image5 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (лицо, волосы, пропорции); одежда меняется по таймлайну.
- @Image2 — Мама Лена: PRIMARY exact identity.
- @Image3 — кухня: только архитектура, мебель, свет.
- @Image4 — двор: только локация (горка, песочница, берёзы, дом).
- @Image5 — лист реквизита: только внешний вид мешочка и морских стёклышек.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Мама Лена — основной лист · id `mama-lena`
- @Image3 — Кухня · id `loc-kitchen`
- @Image4 — Двор с площадкой · id `loc-courtyard`
- @Image5 — Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки · id `props-sheet`

```text
Mode: reference-to-video (omni-reference) | Duration: 30s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Wan 3.0 / Seedance 2.5 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. Russian child voice-over narration in the first person.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (face, hair, proportions); clothing changes only as written in the timeline.
@Image2: PRIMARY exact identity of MAMA LENA.
@Image3: kitchen layout, furniture and morning light only; it never overrides the characters.
@Image4: courtyard location only (blue slide, sandbox, birch trees, brick building).
@Image5: prop sheet, use only the look of the small cloth bag and the sea-glass pieces.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
MAMA LENA: 34-year-old woman, tan skin, dark-brown curly hair in a high loose bun with a few strands free, warm dark eyes, soft laugh lines, no glasses; light-blue denim shirt with rolled sleeves over a white tee, dark jeans.

SPECIAL LOCKS:
Sound is shown only as soft glowing abstract shapes (dots, wavy rings, a sharp teal-white ribbon for the kettle); no letters, no symbols. One round wall clock, one whistling kettle on the stove, one bowl of cereal. Other children are blurred, generic background figures without close-ups; their noise is shown as translucent blue ripples travelling through the air. Exactly five sea-glass pieces end up in a straight line. The kitchen half and the courtyard half are one continuous day: same hoodie, same hair, no new characters in the courtyard close-ups.

START STATE:
Yarik sits at the kitchen table in front of a bowl of cereal, mama stands at the stove three-quarters to camera, kettle on the flame, sunny morning.

TIMELINE:
[0:00–0:05] CRUNCH AND TICK. Close on the spoon in the cereal; each small sound appears as warm yellow sparks; the wall clock ticks out soft orange rings that drift toward Yarik's ears; his eyes flick to the clock.

[0:05–0:10] KETTLE. The kettle starts to whistle; its sound grows into a sharp spiky teal-white ribbon that coils through the room; Yarik flinches and presses both palms over his ears; mama turns, lowers the flame and steps toward him.

[0:10–0:15] HAND ON THE BACK. Mama kneels and rests one hand on his back; the ribbon shrinks into a faint ripple; slow push-in on Yarik's face, eyes closed, one slow breath, then he opens his eyes and looks at the clock.

[0:15–0:20] MATCH CUT TO THE COURTYARD. On Yarik's lowered hands the kitchen light turns to cool autumn daylight: cut to the courtyard, where he now stands at the edge of the playground in the same brick-red hoodie holding a small cloth bag; mama is no longer in frame. TOO MUCH. Tall establishing frame, playground in the lower two thirds and birch crowns above: children run, scream-laugh and chase on the playground; translucent blue ripples build from them toward Yarik, who stands at the edge, shoulders rising.

[0:20–0:25] THE WAVE. The ripples swell into a visible wave-like distortion of the air; Yarik steps back, presses his hands to his ears and slips backward into the shadow under the blue slide.

[0:25–0:30] STILL GLASS. In the quiet shade he kneels, takes sea-glass pieces from the bag and lays them one by one in a perfectly straight line on the concrete; the ripples recede; close on the glass catching a soft glint; his breathing slows.

END STATE:
Yarik kneeling in the shade of the slide, a straight line of five sea-glass pieces in front of him, hands resting beside it, playground noise now distant.

CAMERA / SPACE:
First half: Three setups: close insert on the spoon, medium two-shot as the kettle sounds, slow push-in on Yarik's face. Motivated moves only, eye level of a child, no whip pans. Second half: Tall establishing, then medium portrait framing following his retreat, then a low close-up at ground level on the glass and his hands. Smooth and slow. One clean transition at 0:15; no whip pans, no hand-held feel. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Yarik: tense, inward, small precise reactions, no theatrics. Mama: instantly attentive, gentle, unhurried. Yarik: overwhelmed but not aggressive; the glass ritual is calm and exact, almost meditative.

LIGHTING / MATERIALS:
Warm amber morning window light, pale-mint cabinets, wooden table; cool teal only for the kettle sound. Then: Soft autumn sunlight outside, cooler shade under the slide, warm glints on the glass. Stylized 3D materials with believable softness, readable faces at all times.

DIALOGUE / VOICEOVER:
Language: Russian. Speaker: YARIK as the first-person narrator, the voice of a calm, sensitive 7-year-old boy, soft, unhurried, natural Russian pronunciation without accent. Off-screen voice-over: Yarik's lips do not move on screen and no other character speaks. Exact lines, spoken once each, finishing before the next one begins, with natural breaths and short pauses:
[0:01–0:05] YARIK (V.O.): «Меня зовут Ярик. Мне семь лет.»
[0:06–0:15] YARIK (V.O.): «Чайник свистит, как поезд. Часы стучат, как молотки. Мир у меня внутри — очень громкий.»
[0:16–0:22] YARIK (V.O.): «Во дворе все смеются и кричат. Для меня это — как огромная волна.»
[0:23–0:30] YARIK (V.O.): «Я не злюсь. Я выкладываю стёклышки в ряд. Они тихие.»
Voice sits in the mix above the effects; no subtitles, no captions.

AUDIO:
Sound effects follow the action: Spoon on bowl, clock ticks, kettle whistle, soft room tone; then Distant children's laughter and shouts (non-verbal, muffled as he retreats), light wind, tiny clicks of glass on concrete. The only voice is Yarik's voice-over above; non-verbal crying and children's shouts stay wordless. No music, no sung words.

NEGATIVE PROMPT:
Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, speech from on-screen characters, lip-synced dialogue, singing, generated music score, subtitles, captions, on-screen text, a different voice, a robotic or accented voice, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### B2 · Wan 3.0 · 30 с · Море и слёзы (A3 + A4)

**Что происходит:** Внутренний мир: тёмное штормовое море. Ярик в маленькой лодке, его слова — светящиеся бумажные кораблики, которые уносят волны. Маяк на горизонте не горит. Затем: Прихожая, утро, все опаздывают. Новые ботинки колются, Ярик кричит и плачет на полу. Мама устала, Соня молча смотрит. Он видит мамино лицо и чувствует вину.

**Закадровый текст Ярика (внутри промта, русский, голос ребёнка):**
- [0:01–0:07] «Внутри у меня море. Когда начинается шторм, слова уплывают, как лодки.»
- [0:08–0:15] «Я знаю, что хочу сказать. Но слова не слушаются.»
- [0:16–0:21] «Иногда у меня внутри всё взрывается. Новые ботинки колются, а время бежит.»
- [0:22–0:30] «Я плачу — по-другому не умею. Мама устала. Мне так жалко её. И себя.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Мама Лена — основной лист · @Image3 = Соня — основной лист · @Image4 = Внутреннее море — шторм · @Image5 = Прихожая

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (лицо, волосы, пропорции); одежда меняется по таймлайну.
- @Image2 — Мама Лена: PRIMARY exact identity.
- @Image3 — Соня: PRIMARY exact identity.
- @Image4 — внутреннее море в шторм: только мир, палитра, форма волн и далёкий тёмный маяк.
- @Image5 — прихожая: только планировка, вешалка, обувница, зеркало, свет.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Мама Лена — основной лист · id `mama-lena`
- @Image3 — Соня — основной лист · id `sonya`
- @Image4 — Внутреннее море — шторм · id `loc-inner-sea-storm`
- @Image5 — Прихожая · id `loc-hallway`

```text
Mode: reference-to-video (omni-reference) | Duration: 30s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Wan 3.0 / Seedance 2.5 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. Russian child voice-over narration in the first person.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (face, hair, proportions); clothing changes only as written in the timeline.
@Image2: PRIMARY exact identity of MAMA LENA.
@Image3: PRIMARY exact identity of SONYA.
@Image4: inner-sea storm world, palette, wave shapes and the distant dark lighthouse only.
@Image5: hallway layout, coat hooks, shoe rack, round mirror and lamp only.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
MAMA LENA: 34-year-old woman, tan skin, dark-brown curly hair in a high loose bun with a few strands free, warm dark eyes, soft laugh lines, no glasses; light-blue denim shirt with rolled sleeves over a white tee, dark jeans.
SONYA: 12-year-old girl, fair skin with rosy cheeks, long straight light-brown hair in a side braid, round blue-grey eyes, lilac windbreaker with a small cluster of enamel pins on the pocket, jeans, white sneakers.

SPECIAL LOCKS:
One small wooden rowboat with two oars, Yarik alone in it. His words are small glowing paper boats made of pale light; they leave his mouth silently and are swept away. The distant lighthouse stays dark during the entire clip. One pair of stiff new brown leather boots with stiff laces. Distress shown by crying and body language only, no hitting, no harm, no shouting of words. Mama never raises her voice or hand. The inner sea is a visualisation of Yarik's mind, not a real place; the hallway half is real life. In the sea half Yarik wears the brick-red hoodie and sits alone in the boat; the lighthouse stays dark. The prop look of the lighthouse comes from this text only.

START STATE:
Yarik, small in a wooden rowboat on a dark teal storm sea under a purple sky, gripping both oars; far on the horizon a dark lighthouse.

TIMELINE:
[0:00–0:05] STORM. Tall frame, stacked layers: towering waves made of swirling sound-shapes; the little boat climbs a swell; Yarik grips the oars; the dark lighthouse is tiny on the horizon.

[0:05–0:10] LOST WORDS. Close on Yarik: he opens his mouth to speak, no sound; small glowing paper boats drift out of it and are carried away by the wind in different directions; he reaches after one and misses.

[0:10–0:15] BIG WAVE. A huge wave rises over the stern; he ducks and holds on; camera rises and pulls back to show the boat tilting on the crest, tiny against the sea; lighthouse still dark.

[0:15–0:20] WAVE TO HALLWAY. The huge wave breaks over the camera and washes the frame out in swirling orange-red sound-shapes that settle into the narrow apartment hallway. ITCHY. Mama tries to slide the boot on; Yarik pulls his foot away with a grimace as if the leather burns; short spiky orange-red sound-shapes flicker around his foot.

[0:20–0:25] MELTDOWN. Yarik slides to the floor, pushes the boots away and cries loudly with tears; mama closes her eyes, breathes, sits back on her heels, shoulders heavy; Sonya stays still at the door.

[0:25–0:30] GUILT. Close on Yarik's wet cheeks: his eyes find mama's tired face and his expression turns from anger to guilt; Sonya quietly lowers her bag.

END STATE:
Yarik on the hallway floor, mama sitting beside him not yet touching, Sonya watching from the door, boots pushed aside.

CAMERA / SPACE:
First half: Tall establishing, close-up, then a rising vertical crane. Camera moves with the swell but stays readable; no chaotic shake. Second half: Medium two-shot at child height, close-up on his foot, close-up on his face, final slow push-in. Hand-held feel is not allowed; keep it steady. One clean transition at 0:15; no whip pans, no hand-held feel. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Yarik: concentrated effort and quiet sadness, not terror; his mouth shapes words that do not come out. Real childlike distress, not villain-like. Mama: exhausted love. Sonya: silent understanding.

LIGHTING / MATERIALS:
Moody teal-blue storm light, purple clouds, small warm glow only from his paper-boat words. Then: Warm lamp light in a narrow hallway, grey morning from the door window, no harsh contrast. Stylized 3D materials with believable softness, readable faces at all times.

DIALOGUE / VOICEOVER:
Language: Russian. Speaker: YARIK as the first-person narrator, the voice of a calm, sensitive 7-year-old boy, soft, unhurried, natural Russian pronunciation without accent. Off-screen voice-over: Yarik's lips do not move on screen and no other character speaks. Exact lines, spoken once each, finishing before the next one begins, with natural breaths and short pauses:
[0:01–0:07] YARIK (V.O.): «Внутри у меня море. Когда начинается шторм, слова уплывают, как лодки.»
[0:08–0:15] YARIK (V.O.): «Я знаю, что хочу сказать. Но слова не слушаются.»
[0:16–0:21] YARIK (V.O.): «Иногда у меня внутри всё взрывается. Новые ботинки колются, а время бежит.»
[0:22–0:30] YARIK (V.O.): «Я плачу — по-другому не умею. Мама устала. Мне так жалко её. И себя.»
Voice sits in the mix above the effects; no subtitles, no captions.

AUDIO:
Sound effects follow the action: Sea, wind and wave rumble, soft creak of the boat; words make no sound; then Crying (non-verbal), boot scuff, jacket rustle, muffled street through the door. No spoken words, no music. The only voice is Yarik's voice-over above; non-verbal crying and children's shouts stay wordless. No music, no sung words.

NEGATIVE PROMPT:
Realistic sea documentary look, drowning peril, blood, gore, Violence, hitting, throwing boots at people, mocking expression, Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, speech from on-screen characters, lip-synced dialogue, singing, generated music score, subtitles, captions, on-screen text, a different voice, a robotic or accented voice, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### B3 · Wan 3.0 · 30 с · Маяк и слова (A5 + A6)

**Что происходит:** Ночью Соня приносит Ярику маяк-ночник и жёлтые наушники со своими наклейками. Луч маяка скользит по стене, Бублик ложится ему на ноги. Первое облегчение. Затем: Занятие у Анны Сергеевны: она терпеливо ждёт, Ярик выкладывает ряд карточек-пиктограмм «я — хочу — тихо». Его впервые поняли, и он слегка улыбается.

**Закадровый текст Ярика (внутри промта, русский, голос ребёнка):**
- [0:01–0:07] «Ночью пришла Соня. Она принесла маяк и жёлтые наушники.»
- [0:08–0:15] «Она сказала: „Чтобы море стало тише“. Бублик лёг рядом — тёплый и тяжёлый.»
- [0:16–0:21] «Анна Сергеевна никогда не торопит. Она умеет ждать.»
- [0:22–0:30] «Сегодня я выложил три картинки: „я“, „хочу“, „тихо“. И меня поняли.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Соня — основной лист · @Image3 = Бублик — лист (ракурсы + эмоции) · @Image4 = Анна Сергеевна — лист (ракурсы + эмоции) · @Image5 = Комната Ярика ночью · @Image6 = Кабинет занятий

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (лицо, волосы, пропорции); одежда меняется по таймлайну.
- @Image2 — Соня: PRIMARY exact identity.
- @Image3 — Бублик: PRIMARY exact identity.
- @Image4 — Анна Сергеевна: PRIMARY exact identity.
- @Image5 — комната ночью: только планировка, кровать, полка, окно.
- @Image6 — кабинет: только планировка, круглый стол, ковёр с волнами, свет.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Соня — основной лист · id `sonya`
- @Image3 — Бублик — лист (ракурсы + эмоции) · id `bublik`
- @Image4 — Анна Сергеевна — лист (ракурсы + эмоции) · id `anna-sergeevna`
- @Image5 — Комната Ярика ночью · id `loc-yarik-room`
- @Image6 — Кабинет занятий · id `loc-therapy-room`

```text
Mode: reference-to-video (omni-reference) | Duration: 30s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Wan 3.0 / Seedance 2.5 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. Russian child voice-over narration in the first person.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (face, hair, proportions); clothing changes only as written in the timeline.
@Image2: PRIMARY exact identity of SONYA.
@Image3: PRIMARY exact identity of BUBLIK.
@Image4: PRIMARY exact identity of ANNA SERGEEVNA.
@Image5: night bedroom layout, bed, shelf and window only.
@Image6: therapy room layout, round table, wave-pattern rug and light only.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
SONYA: 12-year-old girl, fair skin with rosy cheeks, long straight light-brown hair in a side braid, round blue-grey eyes, lilac windbreaker with a small cluster of enamel pins on the pocket, jeans, white sneakers.
BUBLIK: medium-large fluffy cream-and-apricot mixed-breed dog with floppy ears, dark brown nose, kind dark eyes and a sky-blue bandana.
ANNA SERGEEVNA: woman of about 48, tall, pale-beige skin, short silver-grey bob, warm brown eyes, deep smile lines, no glasses; plum linen tunic, wooden bead necklace, soft flat shoes.

SPECIAL LOCKS:
Exactly one lighthouse night-light with a slowly rotating warm beam, and one pair of yellow headphones with small hand-placed blue wave stickers. Beam on the wall sweeps slowly, never flashes fast. Exactly three large soft picture cards end in a row: a figure pointing to itself (I), a reaching hand (want), an ear with a small soft cloud (quiet). Pictograms only, no letters or words on cards. Clothing: navy pyjamas with small yellow stars in the night-room half; brick-red hoodie with the yellow headphones around the neck in the therapy-room half. Prop looks (yellow headphones with blue wave stickers, lighthouse night-light, soft picture cards) come from this text only.

START STATE:
Night, a small bedroom lit only by the city glow in the window; Yarik in pyjamas sits on the bed hugging his knees; the door is opening softly.

TIMELINE:
[0:00–0:05] VISITOR. Sonya slips in carrying the lighthouse night-light and the yellow headphones; Yarik watches without moving.

[0:05–0:10] LIGHT. She sets the night-light on the shelf; it glows and a soft beam begins to sweep slowly across the ceiling and wall; she gently places the headphones on his head; his shoulders drop.

[0:10–0:15] WARM WEIGHT. Bublik hops quietly onto the bed and lies across Yarik's feet; Yarik rests a hand in the dog's fur; the sweeping beam on the wall briefly forms a calm blue wave pattern.

[0:15–0:20] DISSOLVE TO DAY. A slow dissolve from the dark night room, with the beam still sweeping, to the bright therapy room where Yarik, now in the brick-red hoodie with the yellow headphones around his neck, sits at the round table opposite Anna. WAITING. Long calm hold: Anna does not hurry, soft smile, relaxed hands; Yarik studies the cards; sunlight slowly moves across the wave-pattern rug.

[0:20–0:25] THREE CARDS. Yarik's hand hovers, picks the 'I' card, sets it down; then 'want'; then 'quiet', lining them in a row exactly like his sea glass.

[0:25–0:30] UNDERSTOOD. Anna nods slowly, eyes shining, a hand over her heart; Yarik looks up at her for the first time and a tiny smile appears; a soft blue-gold shimmer crosses the rug's waves.

END STATE:
Three cards in a row on the table, Anna smiling softly with a hand on her heart, Yarik's small shy smile.

CAMERA / SPACE:
First half: Slow dolly-in from the doorway, medium close two-shot of the headphone moment, low angle on the bed for the dog. Steady, intimate. Second half: Slow medium two-shot across the table, close insert on the hand placing cards, gentle push-in on the final faces. No cuts faster than 3 seconds. One clean transition at 0:15; no whip pans, no hand-held feel. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Sonya: shy, tender, no speech. Yarik: cautious trust. Bublik: calm, heavy settling. Anna: infinite patience, quiet warmth. Yarik: concentration, then a brief fragile joy.

LIGHTING / MATERIALS:
Dark blue night, one warm moving lighthouse beam, faint city glow; skin stays warm and readable. Then: Bright soft daylight through sheer curtains, warm wood, light blue accents from the rug. Stylized 3D materials with believable softness, readable faces at all times.

DIALOGUE / VOICEOVER:
Language: Russian. Speaker: YARIK as the first-person narrator, the voice of a calm, sensitive 7-year-old boy, soft, unhurried, natural Russian pronunciation without accent. Off-screen voice-over: Yarik's lips do not move on screen and no other character speaks. Exact lines, spoken once each, finishing before the next one begins, with natural breaths and short pauses:
[0:01–0:07] YARIK (V.O.): «Ночью пришла Соня. Она принесла маяк и жёлтые наушники.»
[0:08–0:15] YARIK (V.O.): «Она сказала: „Чтобы море стало тише“. Бублик лёг рядом — тёплый и тяжёлый.»
[0:16–0:21] YARIK (V.O.): «Анна Сергеевна никогда не торопит. Она умеет ждать.»
[0:22–0:30] YARIK (V.O.): «Сегодня я выложил три картинки: „я“, „хочу“, „тихо“. И меня поняли.»
Voice sits in the mix above the effects; no subtitles, no captions.

AUDIO:
Sound effects follow the action: Room tone, soft door creak, fabric, the dog's settling sigh; then Quiet room tone, soft card taps on wood, a distant clock. The only voice is Yarik's voice-over above; non-verbal crying and children's shouts stay wordless. No music, no sung words.

NEGATIVE PROMPT:
Bright overhead light, fast flashing beam, Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, speech from on-screen characters, lip-synced dialogue, singing, generated music score, subtitles, captions, on-screen text, a different voice, a robotic or accented voice, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### B4 · Wan 3.0 · 30 с · Друг и берег (A7 + A8)

**Что происходит:** Тот же двор, но теперь у Ярика наушники и Бублик рядом. Девочка Варя осторожно садится рядом и кладёт ракушку; Ярик отдаёт ей самое красивое стёклышко. Первый друг. Затем: Закат на берегу, полосатый маяк. Ярик снимает наушники и слушает море; звуки теперь тёплые золотые волны. Мама, Соня и Бублик обнимают его, луч маяка зажигается над всеми.

**Закадровый текст Ярика (внутри промта, русский, голос ребёнка):**
- [0:01–0:07] «Во дворе всё так же шумно. Но теперь у меня есть наушники.»
- [0:08–0:15] «Одна девочка села рядом. Я дал ей самое красивое стёклышко.»
- [0:16–0:20] «Мой мир всё ещё громкий.»
- [0:21–0:25] «Но у меня есть маяк — это те, кто рядом.»
- [0:26–0:30] «Просто побудьте рядом. Этого достаточно.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Варя — лист (ракурсы + эмоции) · @Image3 = Бублик — лист (ракурсы + эмоции) · @Image4 = Мама Лена — основной лист · @Image5 = Соня — основной лист · @Image6 = Берег и маяк на закате

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (лицо, волосы, пропорции); одежда меняется по таймлайну.
- @Image2 — Варя: PRIMARY exact identity.
- @Image3 — Бублик: PRIMARY exact identity.
- @Image4 — Мама Лена: PRIMARY exact identity.
- @Image5 — Соня: PRIMARY exact identity.
- @Image6 — берег и маяк: только пляж, море, полосатый маяк.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Варя — лист (ракурсы + эмоции) · id `varya`
- @Image3 — Бублик — лист (ракурсы + эмоции) · id `bublik`
- @Image4 — Мама Лена — основной лист · id `mama-lena`
- @Image5 — Соня — основной лист · id `sonya`
- @Image6 — Берег и маяк на закате · id `loc-seaside-lighthouse`

```text
Mode: reference-to-video (omni-reference) | Duration: 30s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Wan 3.0 / Seedance 2.5 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. Russian child voice-over narration in the first person.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (face, hair, proportions); clothing changes only as written in the timeline.
@Image2: PRIMARY exact identity of VARYA.
@Image3: PRIMARY exact identity of BUBLIK.
@Image4: PRIMARY exact identity of MAMA LENA.
@Image5: PRIMARY exact identity of SONYA.
@Image6: seaside and red-and-white lighthouse location only.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
BUBLIK: medium-large fluffy cream-and-apricot mixed-breed dog with floppy ears, dark brown nose, kind dark eyes and a sky-blue bandana.
VARYA: 6-year-old girl, light skin with freckles, two short dark-brown pigtails with orange hair ties, gap-toothed smile; light-blue dungarees over a striped tee.
MAMA LENA: 34-year-old woman, tan skin, dark-brown curly hair in a high loose bun with a few strands free, warm dark eyes, soft laugh lines, no glasses; light-blue denim shirt with rolled sleeves over a white tee, dark jeans.
SONYA: 12-year-old girl, fair skin with rosy cheeks, long straight light-brown hair in a side braid, round blue-grey eyes, lilac windbreaker with a small cluster of enamel pins on the pocket, jeans, white sneakers.

SPECIAL LOCKS:
Background children are blurred and generic. Around Yarik the sound ripples are tiny, soft and held at a distance, as if by a gentle bubble. One small spiral seashell from Varya; one bright blue sea-glass piece given to her. Yarik carries the yellow headphones in his hand, then takes them off. The lighthouse beam turns on only in the last five seconds. Sound-shapes appear as soft golden ripples that blend with the sea. The courtyard half has no location image: an autumn courtyard with a blue slide, a sandbox with a wooden edge, yellow birch trees and a five-storey brick building, exactly as in the first clip of the scene (B1). In the courtyard half Yarik wears the brick-red hoodie with the yellow headphones on his head.

START STATE:
Autumn courtyard; Yarik sits on the edge of the sandbox with the yellow headphones on, Bublik lying beside him, a line of sea glass on the ground in front of him; other children play noisily far behind.

TIMELINE:
[0:00–0:05] A BUBBLE OF QUIET. Camera on Yarik and Bublik; the noisy playground behind is soft and blurred; tiny gentle ripples flutter and stop at an invisible bubble around him.

[0:05–0:10] VARYA. Varya approaches slowly, stops at a respectful distance, crouches and places a small spiral shell next to his line of glass; Yarik watches her; Bublik's tail wags.

[0:10–0:15] THE GIFT. Yarik picks the brightest blue sea-glass piece and puts it in her palm; she smiles gap-toothed; the two sit side by side adding pieces to the line while the camera slowly pulls back.

[0:15–0:20] SOFT DISSOLVE TO THE SEA. The courtyard dissolves into a pebble beach at dusk; Varya is no longer in frame and the family now walks on the pebbles toward the sea. SHORE. Tall low tracking beside and behind the family, pebbles below and sea and sky stacked above: the family walking on the pebbles; gentle waves, golden hour; Yarik looks at the water.

[0:20–0:25] LISTENING. Yarik stops, takes off the headphones and listens to the sea; soft golden ripples of sound blend with the waves; mama kneels and hugs him, Sonya joins, Bublik leans in.

[0:25–0:30] BEACON. The lighthouse beam lights up and sweeps across the family and the sea; slow crane up and back until the hugging group is small under the sweeping beam in a golden-teal sea.

END STATE:
Tall frame: the family hugging on the pebble beach, Bublik pressed against them, the lighthouse beam sweeping over the calm sea.

CAMERA / SPACE:
First half: Medium at child height, a slow reveal of Varya's approach from the depth of the frame, then a gentle pull-back. No fast moves. Second half: Tall tracking, medium on Yarik's face, then a slow crane up and back. Calm, steady, emotional. One clean transition at 0:15; no whip pans, no hand-held feel. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Yarik: wary curiosity turning into trust; Varya: patient, no touching; Bublik: calm. Yarik: quiet wonder and safety. Mama: eyes wet, soft smile. Sonya: relieved, proud. Bublik: pressing close.

LIGHTING / MATERIALS:
Warm autumn light, gentle golden rim light on the glass; the colour palette is warmer than in A2. Then: Golden-hour glow with teal sea; the lighthouse beam as the warm key in the final five seconds. Stylized 3D materials with believable softness, readable faces at all times.

DIALOGUE / VOICEOVER:
Language: Russian. Speaker: YARIK as the first-person narrator, the voice of a calm, sensitive 7-year-old boy, soft, unhurried, natural Russian pronunciation without accent. Off-screen voice-over: Yarik's lips do not move on screen and no other character speaks. Exact lines, spoken once each, finishing before the next one begins, with natural breaths and short pauses:
[0:01–0:07] YARIK (V.O.): «Во дворе всё так же шумно. Но теперь у меня есть наушники.»
[0:08–0:15] YARIK (V.O.): «Одна девочка села рядом. Я дал ей самое красивое стёклышко.»
[0:16–0:20] YARIK (V.O.): «Мой мир всё ещё громкий.»
[0:21–0:25] YARIK (V.O.): «Но у меня есть маяк — это те, кто рядом.»
[0:26–0:30] YARIK (V.O.): «Просто побудьте рядом. Этого достаточно.»
Voice sits in the mix above the effects; no subtitles, no captions.

AUDIO:
Sound effects follow the action: Muffled playground noise far away, light wind, soft clink of glass; then Gentle waves, pebbles, soft wind, a faint distant gull. The only voice is Yarik's voice-over above; non-verbal crying and children's shouts stay wordless. No music, no sung words.

NEGATIVE PROMPT:
Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, speech from on-screen characters, lip-synced dialogue, singing, generated music score, subtitles, captions, on-screen text, a different voice, a robotic or accented voice, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

</div>
<div class="engine-pane" data-engine="sd20">

### 15 с · Seedance 2.0 — восемь роликов A1–A8 (тихие клипы, озвучка Ярика накладывается на монтаже)

#### A1 · Seedance 2.0 · 15 с · Громко

**Что происходит:** Утро на кухне. Обычные звуки (ложка, часы, чайник) для Ярика видны как цветные звуковые формы и становятся слишком громкими. Он закрывает уши, мама мягко приглушает плиту и кладёт руку ему на спину.

**Закадровый текст (не генерируется, озвучка на монтаже):**
- [0:01–0:05] «Меня зовут Ярик. Мне семь лет.»
- [0:06–0:15] «Чайник свистит, как поезд. Часы стучат, как молотки. Мир у меня внутри — очень громкий.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Мама Лена — основной лист · @Image3 = Кухня

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (лицо, причёска, одежда).
- @Image2 — Мама Лена: PRIMARY exact identity.
- @Image3 — кухня: только архитектура, мебель, свет.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Мама Лена — основной лист · id `mama-lena`
- @Image3 — Кухня · id `loc-kitchen`

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. No speech in this clip.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (face, hair, proportions, clothing).
@Image2: PRIMARY exact identity of MAMA LENA.
@Image3: kitchen layout, furniture and morning light only; it never overrides the characters.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
MAMA LENA: 34-year-old woman, tan skin, dark-brown curly hair in a high loose bun with a few strands free, warm dark eyes, soft laugh lines, no glasses; light-blue denim shirt with rolled sleeves over a white tee, dark jeans.

SPECIAL LOCKS:
Sound is shown only as soft glowing abstract shapes (dots, wavy rings, a sharp teal-white ribbon for the kettle); no letters, no symbols. One round wall clock, one whistling kettle on the stove, one bowl of cereal.

START STATE:
Yarik sits at the kitchen table in front of a bowl of cereal, mama stands at the stove three-quarters to camera, kettle on the flame, sunny morning.

TIMELINE:
[0:00–0:05] CRUNCH AND TICK. Close on the spoon in the cereal; each small sound appears as warm yellow sparks; the wall clock ticks out soft orange rings that drift toward Yarik's ears; his eyes flick to the clock.

[0:05–0:10] KETTLE. The kettle starts to whistle; its sound grows into a sharp spiky teal-white ribbon that coils through the room; Yarik flinches and presses both palms over his ears; mama turns, lowers the flame and steps toward him.

[0:10–0:15] HAND ON THE BACK. Mama kneels and rests one hand on his back; the ribbon shrinks into a faint ripple; slow push-in on Yarik's face, eyes closed, one slow breath, then he opens his eyes and looks at the clock.

END STATE:
Yarik at the table with hands lowered from his ears, mama kneeling beside him with a hand on his back, kettle off, ripple fading.

CAMERA / SPACE:
Three setups: close insert on the spoon, medium two-shot as the kettle sounds, slow push-in on Yarik's face. Motivated moves only, eye level of a child, no whip pans. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Yarik: tense, inward, small precise reactions, no theatrics. Mama: instantly attentive, gentle, unhurried.

LIGHTING / MATERIALS:
Warm amber morning window light, pale-mint cabinets, wooden table; cool teal only for the kettle sound. Stylized 3D materials with believable softness, readable faces at all times.

AUDIO:
Spoon on bowl, clock ticks, kettle whistle, soft room tone. No speech, no music.

NEGATIVE PROMPT:
Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, generated speech, narration, singing, generated music score, subtitles, captions, on-screen text, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### A2 · Seedance 2.0 · 15 с · Двор

**Что происходит:** Двор с площадкой. Смех и крики детей накатывают на Ярика волной. Он отступает в тень горки и тихо выкладывает в ряд морские стёклышки.

**Закадровый текст (не генерируется, озвучка на монтаже):**
- [0:01–0:07] «Во дворе все смеются и кричат. Для меня это — как огромная волна.»
- [0:08–0:15] «Я не злюсь. Я выкладываю стёклышки в ряд. Они тихие.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Двор с площадкой · @Image3 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity.
- @Image2 — двор: только локация (горка, песочница, берёзы, дом).
- @Image3 — лист реквизита: только внешний вид банки/мешочка и морских стёклышек (зелёные, синие, белые).

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Двор с площадкой · id `loc-courtyard`
- @Image3 — Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки · id `props-sheet`

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. No speech in this clip.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK.
@Image2: courtyard location only (blue slide, sandbox, birch trees, brick building).
@Image3: prop sheet, use only the look of the small cloth bag and the sea-glass pieces (green, blue, white).
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.

SPECIAL LOCKS:
Other children are blurred, generic background figures without close-ups; their noise is shown as translucent blue ripples travelling through the air. Exactly five sea-glass pieces end up in a straight line.

START STATE:
Yarik stands at the edge of the playground in autumn light holding a small cloth bag; children run and shout in the background.

TIMELINE:
[0:00–0:05] TOO MUCH. Tall establishing frame, playground in the lower two thirds and birch crowns above: children run, scream-laugh and chase on the playground; translucent blue ripples build from them toward Yarik, who stands at the edge, shoulders rising.

[0:05–0:10] THE WAVE. The ripples swell into a visible wave-like distortion of the air; Yarik steps back, presses his hands to his ears and slips backward into the shadow under the blue slide.

[0:10–0:15] STILL GLASS. In the quiet shade he kneels, takes sea-glass pieces from the bag and lays them one by one in a perfectly straight line on the concrete; the ripples recede; close on the glass catching a soft glint; his breathing slows.

END STATE:
Yarik kneeling in the shade of the slide, a straight line of five sea-glass pieces in front of him, hands resting beside it, playground noise now distant.

CAMERA / SPACE:
Tall establishing, then medium portrait framing following his retreat, then a low close-up at ground level on the glass and his hands. Smooth and slow. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Yarik: overwhelmed but not aggressive; the glass ritual is calm and exact, almost meditative.

LIGHTING / MATERIALS:
Soft autumn sunlight outside, cooler shade under the slide, warm glints on the glass. Stylized 3D materials with believable softness, readable faces at all times.

AUDIO:
Distant children's laughter and shouts (non-verbal, muffled as he retreats), light wind, tiny clicks of glass on concrete. No speech, no music.

NEGATIVE PROMPT:
Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, generated speech, narration, singing, generated music score, subtitles, captions, on-screen text, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### A3 · Seedance 2.0 · 15 с · Внутреннее море

**Что происходит:** Внутренний мир: тёмное штормовое море. Ярик в маленькой лодке, его слова — светящиеся бумажные кораблики, которые уносят волны. Маяк на горизонте не горит.

**Закадровый текст (не генерируется, озвучка на монтаже):**
- [0:01–0:07] «Внутри у меня море. Когда начинается шторм, слова уплывают, как лодки.»
- [0:08–0:15] «Я знаю, что хочу сказать. Но слова не слушаются.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Внутреннее море — шторм · @Image3 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (красная толстовка, те же лицо и волосы).
- @Image2 — внутреннее море в шторм: только мир, палитра, форма волн и далёкий тёмный маяк.
- @Image3 — лист реквизита: только вид маяка (не горит).

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Внутреннее море — шторм · id `loc-inner-sea-storm`
- @Image3 — Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки · id `props-sheet`

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. No speech in this clip.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (brick-red hoodie, same face and hair).
@Image2: inner-sea storm world, palette, wave shapes and distant dark lighthouse only.
@Image3: prop sheet, use only the look of the lighthouse (unlit).
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.

SPECIAL LOCKS:
One small wooden rowboat with two oars, Yarik alone in it. His words are small glowing paper boats made of pale light; they leave his mouth silently and are swept away. The distant lighthouse stays dark during the entire clip.

START STATE:
Yarik, small in a wooden rowboat on a dark teal storm sea under a purple sky, gripping both oars; far on the horizon a dark lighthouse.

TIMELINE:
[0:00–0:05] STORM. Tall frame, stacked layers: towering waves made of swirling sound-shapes; the little boat climbs a swell; Yarik grips the oars; the dark lighthouse is tiny on the horizon.

[0:05–0:10] LOST WORDS. Close on Yarik: he opens his mouth to speak, no sound; small glowing paper boats drift out of it and are carried away by the wind in different directions; he reaches after one and misses.

[0:10–0:15] BIG WAVE. A huge wave rises over the stern; he ducks and holds on; camera rises and pulls back to show the boat tilting on the crest, tiny against the sea; lighthouse still dark.

END STATE:
The rowboat tilting on a wave crest, Yarik tiny and holding on, the unlit lighthouse far in the distance.

CAMERA / SPACE:
Tall establishing, close-up, then a rising vertical crane. Camera moves with the swell but stays readable; no chaotic shake. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Yarik: concentrated effort and quiet sadness, not terror; his mouth shapes words that do not come out.

LIGHTING / MATERIALS:
Moody teal-blue storm light, purple clouds, small warm glow only from his paper-boat words. Stylized 3D materials with believable softness, readable faces at all times.

AUDIO:
Sea, wind and wave rumble, soft creak of the boat; words make no sound. No speech, no music.

NEGATIVE PROMPT:
Realistic sea documentary look, drowning peril, blood, gore, Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, generated speech, narration, singing, generated music score, subtitles, captions, on-screen text, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### A4 · Seedance 2.0 · 15 с · Ботинки

**Что происходит:** Прихожая, утро, все опаздывают. Новые ботинки колются, Ярик кричит и плачет на полу. Мама устала, Соня молча смотрит. Он видит мамино лицо и чувствует вину.

**Закадровый текст (не генерируется, озвучка на монтаже):**
- [0:01–0:06] «Иногда у меня внутри всё взрывается. Новые ботинки колются, а время бежит.»
- [0:07–0:15] «Я плачу — по-другому не умею. Мама устала. Мне так жалко её. И себя.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Мама Лена — основной лист · @Image3 = Соня — основной лист · @Image4 = Прихожая

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity.
- @Image2 — Мама Лена: PRIMARY exact identity.
- @Image3 — Соня: PRIMARY exact identity.
- @Image4 — прихожая: только планировка, вешалка, обувница, зеркало, свет.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Мама Лена — основной лист · id `mama-lena`
- @Image3 — Соня — основной лист · id `sonya`
- @Image4 — Прихожая · id `loc-hallway`

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. No speech in this clip.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK.
@Image2: PRIMARY exact identity of MAMA LENA.
@Image3: PRIMARY exact identity of SONYA.
@Image4: hallway layout, coat hooks, shoe rack, round mirror and lamp only.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
MAMA LENA: 34-year-old woman, tan skin, dark-brown curly hair in a high loose bun with a few strands free, warm dark eyes, soft laugh lines, no glasses; light-blue denim shirt with rolled sleeves over a white tee, dark jeans.
SONYA: 12-year-old girl, fair skin with rosy cheeks, long straight light-brown hair in a side braid, round blue-grey eyes, lilac windbreaker with a small cluster of enamel pins on the pocket, jeans, white sneakers.

SPECIAL LOCKS:
One pair of stiff new brown leather boots with stiff laces. Distress shown by crying and body language only, no hitting, no harm, no shouting of words. Mama never raises her voice or hand.

START STATE:
Mama crouches on the hallway floor holding one new brown boot, coat half on, glancing at her watch; Sonya waits at the door with her school bag; Yarik sits on the shoe bench.

TIMELINE:
[0:00–0:05] ITCHY. Mama tries to slide the boot on; Yarik pulls his foot away with a grimace as if the leather burns; short spiky orange-red sound-shapes flicker around his foot.

[0:05–0:10] MELTDOWN. Yarik slides to the floor, pushes the boots away and cries loudly with tears; mama closes her eyes, breathes, sits back on her heels, shoulders heavy; Sonya stays still at the door.

[0:10–0:15] GUILT. Close on Yarik's wet cheeks: his eyes find mama's tired face and his expression turns from anger to guilt; Sonya quietly lowers her bag.

END STATE:
Yarik on the hallway floor, mama sitting beside him not yet touching, Sonya watching from the door, boots pushed aside.

CAMERA / SPACE:
Medium two-shot at child height, close-up on his foot, close-up on his face, final slow push-in. Hand-held feel is not allowed; keep it steady. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Real childlike distress, not villain-like. Mama: exhausted love. Sonya: silent understanding.

LIGHTING / MATERIALS:
Warm lamp light in a narrow hallway, grey morning from the door window, no harsh contrast. Stylized 3D materials with believable softness, readable faces at all times.

AUDIO:
Crying (non-verbal), boot scuff, jacket rustle, muffled street through the door. No spoken words, no music.

NEGATIVE PROMPT:
Violence, hitting, throwing boots at people, mocking expression, Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, generated speech, narration, singing, generated music score, subtitles, captions, on-screen text, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### A5 · Seedance 2.0 · 15 с · Маяк

**Что происходит:** Ночью Соня приносит Ярику маяк-ночник и жёлтые наушники со своими наклейками. Луч маяка скользит по стене, Бублик ложится ему на ноги. Первое облегчение.

**Закадровый текст (не генерируется, озвучка на монтаже):**
- [0:01–0:07] «Ночью пришла Соня. Она принесла маяк и жёлтые наушники.»
- [0:08–0:15] «Она сказала: „Чтобы море стало тише“. Бублик лёг рядом — тёплый и тяжёлый.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Соня — основной лист · @Image3 = Бублик — лист (ракурсы + эмоции) · @Image4 = Комната Ярика ночью · @Image5 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (лицо, волосы; сейчас в тёмно-синей пижаме со звёздочками вместо толстовки).
- @Image2 — Соня: PRIMARY exact identity (сиреневая ветровка/кофта).
- @Image3 — Бублик: PRIMARY exact identity.
- @Image4 — комната ночью: только планировка, кровать, полка, окно.
- @Image5 — лист реквизита: только внешний вид жёлтых наушников и маяка-ночника.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Соня — основной лист · id `sonya`
- @Image3 — Бублик — лист (ракурсы + эмоции) · id `bublik`
- @Image4 — Комната Ярика ночью · id `loc-yarik-room`
- @Image5 — Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки · id `props-sheet`

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. No speech in this clip.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (face, hair; now in navy pyjamas with small yellow stars instead of the hoodie).
@Image2: PRIMARY exact identity of SONYA (lilac windbreaker).
@Image3: PRIMARY exact identity of BUBLIK.
@Image4: night bedroom layout, bed, shelf and window only.
@Image5: prop sheet, use only the look of the yellow headphones and the lighthouse night-light.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
SONYA: 12-year-old girl, fair skin with rosy cheeks, long straight light-brown hair in a side braid, round blue-grey eyes, lilac windbreaker with a small cluster of enamel pins on the pocket, jeans, white sneakers.
BUBLIK: medium-large fluffy cream-and-apricot mixed-breed dog with floppy ears, dark brown nose, kind dark eyes and a sky-blue bandana.

SPECIAL LOCKS:
Exactly one lighthouse night-light with a slowly rotating warm beam, and one pair of yellow headphones with small hand-placed blue wave stickers. Beam on the wall sweeps slowly, never flashes fast.

START STATE:
Night, a small bedroom lit only by the city glow in the window; Yarik in pyjamas sits on the bed hugging his knees; the door is opening softly.

TIMELINE:
[0:00–0:05] VISITOR. Sonya slips in carrying the lighthouse night-light and the yellow headphones; Yarik watches without moving.

[0:05–0:10] LIGHT. She sets the night-light on the shelf; it glows and a soft beam begins to sweep slowly across the ceiling and wall; she gently places the headphones on his head; his shoulders drop.

[0:10–0:15] WARM WEIGHT. Bublik hops quietly onto the bed and lies across Yarik's feet; Yarik rests a hand in the dog's fur; the sweeping beam on the wall briefly forms a calm blue wave pattern.

END STATE:
Yarik lying back with headphones on, Bublik on his feet, Sonya sitting on the bed edge, lighthouse beam sweeping slowly over the wall.

CAMERA / SPACE:
Slow dolly-in from the doorway, medium close two-shot of the headphone moment, low angle on the bed for the dog. Steady, intimate. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Sonya: shy, tender, no speech. Yarik: cautious trust. Bublik: calm, heavy settling.

LIGHTING / MATERIALS:
Dark blue night, one warm moving lighthouse beam, faint city glow; skin stays warm and readable. Stylized 3D materials with believable softness, readable faces at all times.

AUDIO:
Room tone, soft door creak, fabric, the dog's settling sigh. No speech, no music.

NEGATIVE PROMPT:
Bright overhead light, fast flashing beam, Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, generated speech, narration, singing, generated music score, subtitles, captions, on-screen text, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### A6 · Seedance 2.0 · 15 с · Три картинки

**Что происходит:** Занятие у Анны Сергеевны: она терпеливо ждёт, Ярик выкладывает ряд карточек-пиктограмм «я — хочу — тихо». Его впервые поняли, и он слегка улыбается.

**Закадровый текст (не генерируется, озвучка на монтаже):**
- [0:01–0:06] «Анна Сергеевна никогда не торопит. Она умеет ждать.»
- [0:07–0:15] «Сегодня я выложил три картинки: „я“, „хочу“, „тихо“. И меня поняли.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Анна Сергеевна — лист (ракурсы + эмоции) · @Image3 = Кабинет занятий · @Image4 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (красная толстовка, наушники на шее).
- @Image2 — Анна Сергеевна: PRIMARY exact identity.
- @Image3 — кабинет: только планировка, круглый стол, ковёр с волнами, свет.
- @Image4 — лист реквизита: только вид карточек-пиктограмм (без текста) и жёлтых наушников.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Анна Сергеевна — лист (ракурсы + эмоции) · id `anna-sergeevna`
- @Image3 — Кабинет занятий · id `loc-therapy-room`
- @Image4 — Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки · id `props-sheet`

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. No speech in this clip.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (brick-red hoodie, yellow headphones around his neck).
@Image2: PRIMARY exact identity of ANNA SERGEEVNA.
@Image3: therapy room layout, round table, wave-pattern rug and light only.
@Image4: prop sheet, use only the look of the pictogram cards (no text) and the yellow headphones.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
ANNA SERGEEVNA: woman of about 48, tall, pale-beige skin, short silver-grey bob, warm brown eyes, deep smile lines, no glasses; plum linen tunic, wooden bead necklace, soft flat shoes.

SPECIAL LOCKS:
Exactly three large soft picture cards end in a row: a figure pointing to itself (I), a reaching hand (want), an ear with a small soft cloud (quiet). Pictograms only, no letters or words on cards.

START STATE:
Anna sits low at the round table opposite Yarik, large picture cards spread on it; she waits with open calm hands; Yarik, headphones around his neck, looks at the cards.

TIMELINE:
[0:00–0:05] WAITING. Long calm hold: Anna does not hurry, soft smile, relaxed hands; Yarik studies the cards; sunlight slowly moves across the wave-pattern rug.

[0:05–0:10] THREE CARDS. Yarik's hand hovers, picks the 'I' card, sets it down; then 'want'; then 'quiet', lining them in a row exactly like his sea glass.

[0:10–0:15] UNDERSTOOD. Anna nods slowly, eyes shining, a hand over her heart; Yarik looks up at her for the first time and a tiny smile appears; a soft blue-gold shimmer crosses the rug's waves.

END STATE:
Three cards in a row on the table, Anna smiling softly with a hand on her heart, Yarik's small shy smile.

CAMERA / SPACE:
Slow medium two-shot across the table, close insert on the hand placing cards, gentle push-in on the final faces. No cuts faster than 3 seconds. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Anna: infinite patience, quiet warmth. Yarik: concentration, then a brief fragile joy.

LIGHTING / MATERIALS:
Bright soft daylight through sheer curtains, warm wood, light blue accents from the rug. Stylized 3D materials with believable softness, readable faces at all times.

AUDIO:
Quiet room tone, soft card taps on wood, a distant clock. No speech, no music.

NEGATIVE PROMPT:
Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, generated speech, narration, singing, generated music score, subtitles, captions, on-screen text, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### A7 · Seedance 2.0 · 15 с · Стёклышко

**Что происходит:** Тот же двор, но теперь у Ярика наушники и Бублик рядом. Девочка Варя осторожно садится рядом и кладёт ракушку; Ярик отдаёт ей самое красивое стёклышко. Первый друг.

**Закадровый текст (не генерируется, озвучка на монтаже):**
- [0:01–0:07] «Во дворе всё так же шумно. Но теперь у меня есть наушники.»
- [0:08–0:15] «Одна девочка села рядом. Я дал ей самое красивое стёклышко.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Бублик — лист (ракурсы + эмоции) · @Image3 = Варя — лист (ракурсы + эмоции) · @Image4 = Двор с площадкой · @Image5 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (красная толстовка, жёлтые наушники на голове).
- @Image2 — Бублик: PRIMARY exact identity.
- @Image3 — Варя: PRIMARY exact identity.
- @Image4 — двор: только локация (песочница, горка, берёзы).
- @Image5 — лист реквизита: только вид стёклышек и жёлтых наушников.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Бублик — лист (ракурсы + эмоции) · id `bublik`
- @Image3 — Варя — лист (ракурсы + эмоции) · id `varya`
- @Image4 — Двор с площадкой · id `loc-courtyard`
- @Image5 — Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки · id `props-sheet`

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. No speech in this clip.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (brick-red hoodie, yellow headphones on his head).
@Image2: PRIMARY exact identity of BUBLIK.
@Image3: PRIMARY exact identity of VARYA.
@Image4: courtyard location only (sandbox, slide, birch trees).
@Image5: prop sheet, use only the look of the sea-glass pieces and the yellow headphones.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
BUBLIK: medium-large fluffy cream-and-apricot mixed-breed dog with floppy ears, dark brown nose, kind dark eyes and a sky-blue bandana.
VARYA: 6-year-old girl, light skin with freckles, two short dark-brown pigtails with orange hair ties, gap-toothed smile; light-blue dungarees over a striped tee.

SPECIAL LOCKS:
Background children are blurred and generic. Around Yarik the sound ripples are tiny, soft and held at a distance, as if by a gentle bubble. One small spiral seashell from Varya; one bright blue sea-glass piece given to her.

START STATE:
Autumn courtyard; Yarik sits on the edge of the sandbox with the yellow headphones on, Bublik lying beside him, a line of sea glass on the ground in front of him; other children play noisily far behind.

TIMELINE:
[0:00–0:05] A BUBBLE OF QUIET. Camera on Yarik and Bublik; the noisy playground behind is soft and blurred; tiny gentle ripples flutter and stop at an invisible bubble around him.

[0:05–0:10] VARYA. Varya approaches slowly, stops at a respectful distance, crouches and places a small spiral shell next to his line of glass; Yarik watches her; Bublik's tail wags.

[0:10–0:15] THE GIFT. Yarik picks the brightest blue sea-glass piece and puts it in her palm; she smiles gap-toothed; the two sit side by side adding pieces to the line while the camera slowly pulls back.

END STATE:
Yarik and Varya side by side at the sandbox with sea glass and the shell in a shared line, Bublik beside them, playground blurred behind.

CAMERA / SPACE:
Medium at child height, a slow reveal of Varya's approach from the depth of the frame, then a gentle pull-back. No fast moves. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Yarik: wary curiosity turning into trust; Varya: patient, no touching; Bublik: calm.

LIGHTING / MATERIALS:
Warm autumn light, gentle golden rim light on the glass; the colour palette is warmer than in A2. Stylized 3D materials with believable softness, readable faces at all times.

AUDIO:
Muffled playground noise far away, light wind, soft clink of glass. No speech, no music.

NEGATIVE PROMPT:
Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, generated speech, narration, singing, generated music score, subtitles, captions, on-screen text, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

#### A8 · Seedance 2.0 · 15 с · Побудьте рядом

**Что происходит:** Закат на берегу, полосатый маяк. Ярик снимает наушники и слушает море; звуки теперь тёплые золотые волны. Мама, Соня и Бублик обнимают его, луч маяка зажигается над всеми.

**Закадровый текст (не генерируется, озвучка на монтаже):**
- [0:01–0:05] «Мой мир всё ещё громкий.»
- [0:06–0:10] «Но у меня есть маяк — это те, кто рядом.»
- [0:11–0:15] «Просто побудьте рядом. Этого достаточно.»

**Референсы (план):** @Image1 = Ярик — основной лист (4 ракурса) · @Image2 = Мама Лена — основной лист · @Image3 = Соня — основной лист · @Image4 = Бублик — лист (ракурсы + эмоции) · @Image5 = Берег и маяк на закате

**Роли входов:**
- @Image1 — Ярик: PRIMARY exact identity (красная толстовка).
- @Image2 — Мама Лена: PRIMARY exact identity.
- @Image3 — Соня: PRIMARY exact identity.
- @Image4 — Бублик: PRIMARY exact identity.
- @Image5 — берег и маяк: только локация, палитра и вид маяка.

**Планируемые референсы (картинок пока нет, будут сгенерированы позже; пути не заданы):**
- @Image1 — Ярик — основной лист (4 ракурса) · id `yarik`
- @Image2 — Мама Лена — основной лист · id `mama-lena`
- @Image3 — Соня — основной лист · id `sonya`
- @Image4 — Бублик — лист (ракурсы + эмоции) · id `bublik`
- @Image5 — Берег и маяк на закате · id `loc-seaside-lighthouse`

```text
Mode: reference-to-video (omni-reference) | Duration: 15s | Resolution: 720p | Aspect ratio: 9:16 (vertical portrait) | FPS: 24 | Native audio: on
Optimized for Seedance 2.0 | High-end 3D animated family-feature look: stylized but physically grounded characters with soft rounded forms, expressive eyes, subtle skin subsurface scattering, detailed hair and fabric, soft volumetric light, shallow depth of field, tender emotional tone. Warm, moving, quiet. No speech in this clip.

REFERENCES / AUTHORITY ORDER:
@Image1: PRIMARY exact identity of YARIK (brick-red hoodie).
@Image2: PRIMARY exact identity of MAMA LENA.
@Image3: PRIMARY exact identity of SONYA.
@Image4: PRIMARY exact identity of BUBLIK.
@Image5: seaside and red-and-white lighthouse location, palette and lighthouse design only.
Priority: the individual character sheets (horizontal turnaround sheets, used for identity only) control faces, hair, ages, proportions and clothing; location and prop images (vertical 9:16 frames) control only their named elements, recomposed for a vertical frame; never blend faces; do not import incidental people or props from location images.

CHARACTER APPEARANCE / IDENTITY LOCK:
YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
MAMA LENA: 34-year-old woman, tan skin, dark-brown curly hair in a high loose bun with a few strands free, warm dark eyes, soft laugh lines, no glasses; light-blue denim shirt with rolled sleeves over a white tee, dark jeans.
SONYA: 12-year-old girl, fair skin with rosy cheeks, long straight light-brown hair in a side braid, round blue-grey eyes, lilac windbreaker with a small cluster of enamel pins on the pocket, jeans, white sneakers.
BUBLIK: medium-large fluffy cream-and-apricot mixed-breed dog with floppy ears, dark brown nose, kind dark eyes and a sky-blue bandana.

SPECIAL LOCKS:
Yarik carries the yellow headphones in his hand, then takes them off. The lighthouse beam turns on only in the last five seconds. Sound-shapes appear as soft golden ripples that blend with the sea.

START STATE:
Dusk on a pebble beach; the family walks toward the sea, Yarik holding mama's hand with headphones around his neck, Sonya beside them, Bublik ahead; a striped red-and-white lighthouse stands in the distance.

TIMELINE:
[0:00–0:05] SHORE. Tall low tracking beside and behind the family, pebbles below and sea and sky stacked above: the family walking on the pebbles; gentle waves, golden hour; Yarik looks at the water.

[0:05–0:10] LISTENING. Yarik stops, takes off the headphones and listens to the sea; soft golden ripples of sound blend with the waves; mama kneels and hugs him, Sonya joins, Bublik leans in.

[0:10–0:15] BEACON. The lighthouse beam lights up and sweeps across the family and the sea; slow crane up and back until the hugging group is small under the sweeping beam in a golden-teal sea.

END STATE:
Tall frame: the family hugging on the pebble beach, Bublik pressed against them, the lighthouse beam sweeping over the calm sea.

CAMERA / SPACE:
Tall tracking, medium on Yarik's face, then a slow crane up and back. Calm, steady, emotional. Vertical 9:16 composition: main subject centred in the middle third, characters stacked high-to-low or front-to-back rather than side by side, tall depth layers (foreground, subject, background), faces large enough to read on a phone, phone-UI safe margins, no wide horizontal panoramas.

PERFORMANCE:
Yarik: quiet wonder and safety. Mama: eyes wet, soft smile. Sonya: relieved, proud. Bublik: pressing close.

LIGHTING / MATERIALS:
Golden-hour glow with teal sea; the lighthouse beam as the warm key in the final five seconds. Stylized 3D materials with believable softness, readable faces at all times.

AUDIO:
Gentle waves, pebbles, soft wind, a faint distant gull. No speech, no music.

NEGATIVE PROMPT:
Identity drift between shots, extra people, altered clothing colours, scary or distorted faces, exaggerated slapstick, photoreal live-action look, uncanny teeth, extra fingers or limbs, camera shake, generated speech, narration, singing, generated music score, subtitles, captions, on-screen text, logos, watermark, split screen, poster layout, horizontal landscape framing, letterbox, pillarbox, black bars, tiny subject lost in a wide frame, cropped heads.

FRAME FILL / NO BARS:
Fill the entire generated vertical 9:16 portrait frame edge to edge, 720×1280. No letterbox, pillarbox, black bars, borders or empty margins; no horizontal landscape picture inside the frame.
```

</div>
</div>
