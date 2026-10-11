# Черновики промтов для следующих сцен — ПРЕДЛОЖЕНИЯ (11.10.2026)

> Черновики Claude Code. **Это не правка master и не разрешение на генерацию.** `video-prompts.md` не менялся; ничего не запускалось в Topview. Все творческие решения остаются за владельцем: там, где выбор творческий, он помечен **`[ВЫБОР n]`** и по умолчанию стоит тот вариант, который уже написан в текущем master (то есть я ничего сюжетного не придумывал и не заменял). Применять — только по вашему решению, через писателя канона (`monitor_role.py`), с `PROMPT-STYLE-GUIDE` §11 и обновлением манифестов.
>
> Основа: текущие тексты Scenes 35–38 в master, `prompt-audit-2026-10.md` (находки по этим сценам), листы Серёги/Паши/Саши (внешность сверена визуально), манифесты `references/scenes/scene-35…38`.

## 0. Что исправляют черновики 35–38 (относительно master)

| Находка аудита | Что сделано в черновике |
|---|---|
| Нет стандартного `FRAME FILL / NO BARS` (35, 36, 37, 38) | Добавлен блок гайда дословно. |
| Нет явных `START STATE` / `END STATE` | Добавлены; END каждой сцены совместим со START следующей (35→38, 36→37). |
| Операторские/редакторские фразы в копируемом блоке («Warcraft/CRT story», «No generation authorized by this draft», «as Scenes 33–35») | Убраны; требования к входам вынесены **за блок** (раздел «Входы перед запуском»). |
| Нет `CHARACTER APPEARANCE / IDENTITY LOCK` по листам | Добавлен короткий lock по реальным признакам с листов (капюшон мантии Серёги; щетина и наручи Паши; очки/борода Саши). |
| Scene 36: Паша и Саша в кадре без identity-референса | Предложен выбор `[ВЫБОР 36-1]`: приложить листы или опереться на кадр Scene 17. |
| Scene 37: перегруз 30 с | Предложен сокращённый вариант (4 бита); альтернатива — разделить (каркас в §3). |
| Scenes 35 и 38 повторяют бит «стирает пыль с CRT» | `[ВЫБОР 35/38-1]`: по умолчанию бит остаётся в 35, а в 38 заменён осмотром шильдиков/портов (можно вернуть как в master). |

Дополнительно: в каждом блоке нет ссылок вида «выше/ниже», упоминаний других сцен по номеру и путей репозитория; внутри — только то, что нужно модели.

## 1. Входы перед запуском (вне промтов)

| Сцена | Обязательно приложить | Откуда | Сейчас |
|---|---|---|---|
| 35 | `@Image1` лист Серёги; `@Image2` внешняя архитектура; `@Image3` **последний кадр результата Scene 34** | `references/full/serega.jpg`; `references/scenes/scene-27/S27-Image5-topview-source.png`; кадр 34 — из Topview/монтажа | кадра 34 в репозитории нет (результат 34 принят «в монтаж») |
| 36 | `@Image1` лист Серёги; `@Image2` пещера; `@Image3` карта; `@Image4`/`@Image5` листы Паши/Саши (если `[ВЫБОР 36-1]` = листы); `@Image6` кадр Scene 17 (последний, из фильма); `@Image7` кадр транспорта на Набу | `serega.jpg`; `S17-cave-Video1-frame-003s.png`; `S17-Image4-topview-source.png`; `pasha.jpg`/`sasha.jpg`; кадры из монтажа | кадры из монтажа не выгружены; транспорт не подобран |
| 37 | `@Image1` лист Серёги; `@Image2` последний кадр результата Scene 36; `@Image3` кадр корабля/планеты из монтажа | кадры из монтажа/результата 36 | ни один не существует |
| 38 | `@Image1` лист Серёги; `@Image2` архитектура; `@Image3` последний кадр результата Scene 35 | как в 35 | сцена 35 не сгенерирована |

Выбор стоит между кадрами (`@Image`) и видео (`@Video`): в черновиках везде **кадры**, потому что кадр однозначнее для first-frame continuity; если Topview/Wan принимает видео-вход и вы хотите именно его — замена механическая (`@Image3` → `@Video1` в двух строках). Лимит числа входов у Wan 3.0 не проверялся — до запуска сверить в Topview.

Нумерация `@Image` **локальна для каждого промта**. Метки в квадратных скобках внутри блоков (`[только при (а)]`, `[ВЫБОР …]`) — пометки для вас: **перед запуском удалить**; копируемый блок должен быть чистым.

## 2. Черновики

### 2.1. Scene 35 — Древний ПК в руинах храма: находка Серёги (DRAFT v2)

**Что решено вами ранее и сохранено:** прямое продолжение Scene 34; находка бежевого системного блока, CRT и клавиатуры; ничего не включается; сухая серьёзная реакция; открытый конец без Warcraft-развязки.

**Выборы:**
- `[ВЫБОР 35/38-1]` — какой из двух сцен принадлежит бит «стирает пыль с CRT»: по умолчанию **35** (как в master); 38 тогда получает другой бит (см. 2.4).
- `[ВЫБОР 35-2]` — как заканчивается кадр: по умолчанию как в master (тянется к клавиатуре, питание **не** нажимает).

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal live-action archaeological adventure with a deadpan find | Continuous physical take

REFERENCES:
@Image1 — PRIMARY exact identity reference for SEREGA. It owns his face, age, proportions and robe only.
@Image2 — EXTERIOR WORLD reference only: red-ochre ancient weathered masonry, eroded stone, warm orange sunset, modest dry dust. Exterior design may be glimpsed through the existing entrance; it never overrides the interior of @Image3.
@Image3 — START FRAME and INTERIOR CONTINUITY: the actual final frame of the preceding temple-entry shot. It owns the first interior hall, the carved corridor entrance, the real door position, camera side, sunlight direction and physical geometry. Do not replace it with fantasy statues, a vast new cathedral or a generic cave.
REFERENCE PRIORITY: @Image1 outranks every other image for the face and costume of Serega. @Image3 outranks @Image2 for everything inside the building.

CHARACTER APPEARANCE / IDENTITY LOCK:
SEREGA: pale older man with a rounded face, bald crown and sparse light-blond hair only at the sides and back, calm heavy-lidded expression; long dark-purple hooded robe (hood down) over black fitted sleeves, dark boots. Preserve exact face, age, proportions and robe silhouette. No younger face, beautification, new jewellery or accessory. His hands hold nothing at the start.

STORY FUNCTION:
A serious archaeological adventure with a deadpan absurd find. Serega is alone and searching with intent, never looking into the camera. The find is an ordinary tangible object, not a magical interface: a bulky late-20th-century beige desktop case, a grey-beige CRT monitor with convex glass, a simple keyboard, coiled dusty cables. No flat monitor, no RGB, no hologram. Nothing powers on.

START STATE:
Directly continues @Image3. Serega stands in the first interior chamber at the carved masonry, facing the narrower side passage; exterior light lies geometrically consistent behind him. Same robe, empty hands, no new prop visible.

TIMELINE:
[0:00–0:05] Medium-wide, stable. Serega pauses at the carved masonry and notices a narrow recess behind fallen stone. Restrained, observant expression. The camera glides laterally only as much as needed to reveal the recess naturally.
[0:05–0:11] He approaches along the same floor, slow deliberate boots over ancient grit; tracking at shoulder height passes one broken support. A thin sunlight shaft from the known wall opening rakes through floating dust.
[0:11–0:17] Over the same shoulder he carefully moves one small loose flat stone aside with both hands, uncovering the corner of a rectangular beige object under cloth and dust. A mechanical, physically plausible reveal, not a glowing portal.
[0:17–0:23] Smooth three-quarter view, still spatially linked: he lifts the cloth and brushes dust from a bulky CRT monitor on a stone shelf; below it a beige case and a keyboard become visible in the same composition, cables attached. Objects never morph between angles.
[0:23–0:27] Close medium on Serega: intense explorer's concentration shifts into a tiny, utterly serious bewilderment. He looks from the monitor to the keyboard, never laughs or winks. One dry stone scrape, quiet shoe movement.
[0:27–0:30] The camera drifts back to a readable archaeological composition: Serega, the dusty PC, the CRT and the keyboard in one consistent shot. He reaches toward the keyboard but does NOT press anything.

END STATE:
Serega stands at the shelf with one hand extended toward the keyboard, not touching it; the computer is dormant in the same niche; same sunlight shaft, same camera side. A clean continuation point for the next shot.

CAMERA / SPACE:
Physically stable cinema, natural 35 mm perspective, smooth inertia, no jitter. No cut that moves objects or changes the hallway topology. If coverage is needed keep the same axis and a motivated viewpoint. Preserve the real size of a desktop system and of Serega's hands.

LIGHT / MATERIALS:
Matte etched stone; airborne dust lit by warm side shafts; dim bounce-lit chamber; greyed ABS plastic with age-yellowing and scratches; realistic convex CRT glass reflecting only faint room light, screen inert and black; no LEDs, no backlit text.

AUDIO (native):
Dry wind fading into reverberant temple room tone, grit under boots, soft robe movement, one stone scrape, dust brushing, faint plastic contact. No dialogue, voiceover, song, score or machine startup sound.

NEGATIVE PROMPT:
different man or robe, younger face, new location, impossible hall, weightless objects, morphing CRT, flat screen, magic sigils, neon, glowing screen, hologram, powered-on gameplay, modern laptop, extra characters, cats, cartoon comedy, giggling, subtitles, text added to the image, flicker, handheld shake, wrong shadows, logo, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### 2.2. Scene 36 — После пещеры: Серёга с картой направляется к кораблю (DRAFT v2)

**Сохранено из master:** продолжение Scene 17; Серёга встаёт, прощается жестом, прячет единственную карту и уходит; Паша и Саша остаются; без диалога и без взлёта.

**Выборы:**
- `[ВЫБОР 36-1]` — как удержать лица Паши и Саши: **(а)** приложить их листы (`@Image4`, `@Image5`); **(б)** считать их лица принадлежащими последнему кадру Scene 17 (`@Image6`) без листов. В черновике написан вариант (а); для (б) удалить два абзаца помеченные `[только при (а)]` и фразу в `REFERENCE PRIORITY`.
- `[ВЫБОР 36-2]` — каким кадром задаётся транспорт: кадр из монтажа (`@Image7`) — нужен до запуска; без него сцена не готова (так и сказано в master).
- Карту в руках/под одеждой оставляю как в master («складывает по существующему сгибу и прячет в ту же мантию»).

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal live-action restrained adventure | One continuous follow take

REFERENCES:
@Image1 — PRIMARY exact identity reference for SEREGA.
@Image2 — CAVERN reference: the humid post-battle cavern with wet layered rock, shallow water, cool bounce light, the monster-remains seating and the real exit direction.
@Image3 — PRIMARY PROP reference for the single map: folded edges, markings, size, surface, material. Never substitute a disk, book, glowing tablet or a second map.
@Image4 — PRIMARY exact identity reference for PASHA. [только при (а)]
@Image5 — PRIMARY exact identity reference for SASHA. [только при (а)]
@Image6 — START FRAME: the final frame of the preceding cave shot. It owns positions, who sits where and which hand holds the map.
@Image7 — TRANSPORT reference: the existing craft in its real Naboo parking place — exact shape, exterior geography and approach direction.
REFERENCE PRIORITY: @Image1, @Image4 and @Image5 own the faces of their characters; @Image6 owns positions and the map hand; @Image2 owns the cave only; @Image7 owns the transport and the exterior only. Never borrow faces or costumes from scenery images.

CHARACTER APPEARANCE / IDENTITY LOCK:
SEREGA: pale older man, rounded face, bald crown with sparse light-blond hair at the sides, long dark-purple hooded robe (hood down) over black sleeves, hem still wet from the cave.
PASHA: short brown hair with receding temples, light stubble, no full beard; dark navy Jedi tunic and trousers, dark leather forearm bracers, brown belt with pouches, tall dark boots. [только при (а)]
SASHA: round wire glasses, full dark beard, receding dark hair; cream inner tunic under a dark burgundy hooded robe, brown belt with pouches, brown boots. [только при (а)]
Do not blend the faces; the attached images outrank this text. Wet clothing and exhausted faces continue without reset.

START STATE:
Matches @Image6. Serega sits and holds the one map; Pasha and Sasha sit on separate sections of the inert monster remains, exhausted; the monster stays inert. The handoff of the map has already happened: do not replay it, no whispering, no dialogue.

STORY:
After the fight Serega decides to leave. Pasha and Sasha stay on Naboo and do not follow him. No reconciliation speech, no new villain. A slight farewell gesture is enough.

TIMELINE:
[0:00–0:06] Close to the established three-shot. Serega glances at the map, folds it only along its existing crease and secures it inside the same robe, visibly. Pasha and Sasha watch silently.
[0:06–0:12] Serega plants his feet on firm wet stone and rises carefully with a coherent weight shift. Pasha and Sasha stay seated. Serega gives one small, serious nod; they answer with minimal eye movement only.
[0:12–0:18] The camera follows from behind, three-quarter, as he walks at his own pace along the established water edge toward the real exit; the seating area stays in believable perspective. No new stairs, the waterfall does not move.
[0:18–0:24] One motivated camera travel crosses the real cave opening; damp rock gives way to the existing Naboo exterior light and terrain. His hem stays wet. Exposure adapts gradually; the cave opening remains visible behind him.
[0:24–0:30] The same walking vector brings him toward the transport of @Image7, parked consistently with the existing footage. A clear, unhurried composition: he is still approaching the boarding point, the map is secured, the craft is motionless. No takeoff and no planet cut.

END STATE:
Serega walks toward the parked transport, map concealed in his robe, the craft motionless in its original Naboo exterior; the last frame is matchable for the next shot.

CAMERA / GEOGRAPHY:
One smooth controlled 35 mm follow without arbitrary cuts; physical 3D space; no abrupt change of screen direction; stable left/right identities; no digital zoom or micro-shake; a believable cave-to-exterior light gradient.

PERFORMANCE:
Adult, restrained, tired movement after a hard battle. No swagger, no parody, no extra gesticulation.

AUDIO (native):
Wet steps and faint dripping, distant waterfall, fabric rustle, then natural outdoor wind; the sound bed changes gradually as he emerges. No dialogue, narrator, music or audible coordinates.

NEGATIVE PROMPT:
double map, missing map, flying map, extra characters, Pasha or Sasha following, changed man or robe, face blending between the three men, magical portal, wrong vehicle, invented landing platform, duplicated seats, resurrected monster, new combat, inconsistent lighting, fake CG look, jump cuts, subtitles, text, watermark, camera jitter.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### 2.3. Scene 37 — Перелёт Серёги к лесной планете (DRAFT v2, сокращённый)

**Сохранено из master:** корабль Серёги уходит с Набу, короткий космический переход, подход к лесной планете; встреча с лесной группой **не** инсценируется; карта одна и остаётся в робе.

**Что изменено ради исполнимости:** четыре бита вместо шести; убраны «time-compression edit» и бит «подход к конкретному первому кадру леса» (кадр остаётся ориентиром только для света/растительности, стык делается монтажом). Если нужен именно подход к посадке — это второй самостоятельный ролик (каркас в §3.5).

**Выборы:**
- `[ВЫБОР 37-1]` — оставить 37 одним роликом (этот черновик), разделить на «отлёт / прибытие» (§3.5) или оставить как в master.
- `[ВЫБОР 37-2]` — показывать ли лесную пару (Виталик, Лёша): по умолчанию **нет** (как в master они допускаются только если реально видны); поэтому их листы в черновик не включены.

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | Photoreal live-action physically plausible planetary transfer | Continuous camera path

REFERENCES:
@Image1 — PRIMARY exact identity reference for SEREGA.
@Image2 — START FRAME: the final frame of the preceding Naboo shot. It owns the exact transport craft model, hatch, parking environment, camera side and Serega's approach vector.
@Image3 — SHIP / PLANET design reference from the existing film: the same craft in flight and a believable planet view. It owns hull shape, scale, exhaust behaviour and the look of space; it never licenses a new vehicle design.
REFERENCE PRIORITY: @Image1 owns the face and robe; @Image2 owns the craft and the departure site; @Image3 owns the craft in flight and the space look.

CHARACTER APPEARANCE / IDENTITY LOCK:
SEREGA: pale older man, rounded face, bald crown with sparse light-blond hair at the sides, long dark-purple hooded robe (hood down) over black sleeves. He is alone. The one physical map stays concealed inside his robe, never multiplied, never floating, never a hologram.

START STATE:
Matches @Image2. Serega stands at the hatch of the real transport in the Naboo exterior; map concealed; daylight.

TIMELINE:
[0:00–0:05] Serega takes two steps, boards through a visible, mechanically plausible entry and the hatch closes. Identity, robe, distance and screen direction stay coherent.
[0:05–0:12] One motivated exterior wide view: the same full craft makes a realistic vertical or shallow forward departure; dust, water and local vegetation react as appropriate. No redesign, no instant switch from shuttle to fighter.
[0:12–0:20] A stable forward-following shot as the craft climbs through atmospheric layers into open space on one continuous navigable path; real cloud haze, parallax and a starfield.
[0:20–0:30] The same craft in a restrained, short space beat. A new planet becomes readable ahead — cloud deck, wooded continental landforms, horizon — and the camera glides from behind the ship along its approach vector. Hold on the planet with the craft small in frame; no landing, no meeting.

END STATE:
The craft flies toward a cloud-wrapped wooded planet, still in space or the upper atmosphere; ship orientation and light direction are clear so the next shot can be matched in editing.

CAMERA / PHYSICS:
Stable 3D continuity, smooth inertial cinema, accurate perceived ship size, no jump discontinuity on the craft, no random flight-direction flips. Natural daylight turning to space light and then believable planetary lighting; muted clean grade.

AUDIO (native):
Recognisable hatch servo and closing, engine ignition, air movement and low-frequency ascent vibration, low travel ambience, subtle atmospheric wind near the destination. No songs, narrator, speech or crowd.

NEGATIVE PROMPT:
wrong face, a new craft, mismatch with the reference craft, teleporting or extra map, other characters on board, impossible instant landing, made-up planet landmarks, fleets, laser battle, explosion, magic warp doorway, shiny game CGI, random direction flips, hard geometry morph, jitter, subtitles, text, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

### 2.4. Scene 38 — Серёга рассматривает древний компьютер (DRAFT v2)

**Сохранено из master:** самостоятельный осмотр; ПК уже найден; ничего не включается, нет Warcraft/карт/новых артефактов; сухая ирония в реакции; один тихий щелчок клавиши.

**Выбор `[ВЫБОР 35/38-1]` (по умолчанию в черновике — бит заменён):** в master бит `[00:05–00:10]` («вытирает полосу пыли с рамки CRT») повторяет Scene 35. В черновике он заменён осмотром шильдиков/портов корпуса; если хотите оставить как в master — вернуть исходную строку и убрать «brushes dust» из 35 (§2.1).

```text
Mode: reference-to-video | Duration: 30s | Resolution: 1080p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on
Optimized for Wan 3.0 | High-end photoreal live-action cinema | Dry deadpan inspection

REFERENCES:
@Image1 — PRIMARY exact identity reference for SEREGA; it alone owns his face.
@Image2 — EXTERIOR WORLD reference only: red-ochre ancient masonry, dry dusty air, warm sunset light. It never overrides the interior of @Image3.
@Image3 — START FRAME: the actual final frame of the preceding find shot. It defines the first frame, Serega's position and gaze, the dust layers, the arrangement of the computer, monitor, keyboard and stone shelf, the nearest support, the passage, the light direction and the camera axis. Start from it; do not recreate a different temple.
REFERENCE PRIORITY: @Image1 > @Image3 > @Image2.

CHARACTER APPEARANCE / IDENTITY LOCK:
SEREGA: pale older man, rounded face, bald crown with sparse light-blond hair at the sides, natural age and skin structure; long dark-purple hooded robe (hood down) over black sleeves; same height and proportions as in the start frame. No younger face, duplicate, costume change, weapon or accessory in his hands.

OBJECT LOCK / PHYSICS:
One plausible late-1990s beige desktop case, one bulky grey-beige CRT monitor with convex glass and one simple dusty wired keyboard, in the EXACT positions and orientation of the start frame. Cables, yellowed plastic, dull buttons, scuffs and dust stay stable. He may gently touch dust and one key but must not unplug, carry, replace, shrink or levitate anything. No flat screen, no second machine, no glowing interface, no power-on. The black CRT glass reflects only faint room light; no image, no glyphs.

START STATE:
The computer has already been found and partly uncovered. Serega stands at the stone niche, one hand near the keyboard, alone. No re-entry, no second reveal, no time jump.

TIMELINE:
[0:00–0:05] Medium-wide, geometrically matching the start frame: Serega by the shelf with the black CRT, the keyboard and the beige case fully readable. He freezes at the incongruous find, eyes tracing the monitor's bulky outline; a stabilised dolly nudges closer without crossing the axis.
[0:05–0:10] Mid over-shoulder follows his small lean toward the case. He reads its details: scuffs, a faded label plate, a row of old ports; he runs a fingertip over the plate and looks at the dust on it. The screen stays black. [ВЫБОР 35/38-1: master has here «wipes a strip of dust from the lower bezel of the CRT»]
[0:10–0:16] Same profile and spatial frame. He leans lower and reads the keyboard: a slow glance from cable to raised keys, then one ordinary key pressed with the index finger. It depresses and springs back with one tiny mechanical tick. No chime, boot tone, text or response.
[0:16–0:22] A short continuous shoulder-level drift without a new corridor or camera-side inversion: he examines the rough side panel of the system unit and its dust-caked vents without reaching for power, with a subtle dawning recognition of an ordinary old machine, then checks the impossible ancient stone around it. Everything stays where it was.
[0:22–0:27] Medium reaction: his eyes return from the stone relief to the lifeless CRT; a tiny raised eyebrow and a restrained incredulous exhale reveal dry humour. He glances once toward the passage he came from, then back at the computer, still alone. No speech, laughter or extra characters.
[0:27–0:30] A smooth slow ease-out to a clear three-quarter composition containing his recognisable face, the inert monitor, the case, the keyboard and the same cracked niche, under the same warm light shaft. His fingertips rest near, not on, the power control.

END STATE:
Serega still examines the same dormant computer in the same niche; nothing has changed except that he has studied it; a clean continuation point.

CAMERA / CONTINUITY:
One plausible 3D set; natural 35 mm perspective with restrained short 50 mm inspection accents; fluid dolly and focus pulls without perspective warping; the doorway, shelf, wall cracks, broken stone and sun shaft stay absolutely consistent; prefer uninterrupted motivated motion; no shake or micro-jitter; no scale drift of hands, computer or temple.

LIGHT / GRADE:
Aged red-ochre masonry and dry particulate air, low warm dusty sun beams from the established side, soft dark chamber fill, matte scratch detail on old plastic, dusty convex CRT glass catching only plausible inert reflections. Photochemical cinematic contrast, no blue sci-fi light, no horror jump effects.

AUDIO (native):
Subdued dry temple ambience and faint far wind, cloth and feet, fine dust brush, a soft fingertip on old plastic and ONE tactile key click, a small involuntary breath. No music, narrator, dialogue, machine fan, power-on sound, magic hum or synthetic UI beeps.

NEGATIVE PROMPT:
finding the computer again, teleporting to a second room, wrong face or robe, new location, moved or rearranged or duplicated computer, floating keyboard, laptop, modern RGB gaming PC, LED text, CRT switched on or glowing, game footage on screen, extra person, cats, giant hands, morphing close-up, shifted camera axis, random jump cuts, shaky camera, cartoon acting, subtitles, captions, titles, logos, watermark.

FRAME FILL / NO BARS:
Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.
```

## 3. Каркасы для сцен, которых ещё нет в master (только структура, без решений)

Здесь **нет готовых промтов**: каждая сцена зависит от вашего решения (D-номера из `montage-plan-v3-draft.md`). Для каждой — неизменные ограничения канона, слоты выбора и бит-схемы вариантов. Когда решение принято, из каркаса разворачивается полноценный промт по тому же шаблону, что в §2.

**Общие неизменные факты** (из master/реестра): Серёга — бледный пожилой мужчина, лысая макушка, редкие светлые волосы по бокам, тёмно-пурпурная мантия с капюшоном; Лучик — бело-серый длинношёрстный кот, синий меч; Рыжик — рыжий табби, зелёный меч; меч Серёги — красный; коты обычного домашнего размера (голова стоящего кота — около колена Серёги); локация планеты ситхов — каменный город-руина охристо-красно-коричневого камня на оранжево-золотом закате с тонкой сухой пылью/пеплом; никаких лавы, чёрного базальта, вулканического свечения. Русская речь → Wan 3.

### 3.1. Исход дуэли (после Scene 32) — решение D2

Вход: END Scene 32 («кот-дуэт доминирует, Серёга жив и борется; арка частично обрушена; заблокированный проход»). Ролик 30 с, Wan 3.0. Слот `[ВЫБОР D2]`:

| Вариант | Бит-схема (по секундам, ориентир) | Фиксирует для следующих сцен |
|---|---|---|
| (а) коты побеждают, Серёга отступает/уходит | 0–8 коты давят; 8–18 Серёга находит выход через завал/укрытие; 18–26 коты не преследуют (почему — **творческий** слот); 26–30 Серёга остаётся один | Scene 33 естественно следует (один в руинах) |
| (б) Серёга выживает неожиданным приёмом, не побеждая | 0–10 прорыв обороны; 10–20 приём (какой — **слот**); 20–30 коты отброшены/отвлечены, бой остановлен | нужно объяснение отсутствия котов в 33–38 |
| (в) бой прерывает внешнее событие (обрушение, находка, свет храма) | 0–12 нарастание; 12–22 событие (какое — **слот**); 22–30 все трое смотрят на новое | событие должно вести к храму 34 |
| (г) бой не разрешается в сцене | не снимается; решается монтажом | Scene 33 остаётся хронологически свободной |

Идентичность: листы Серёги, Лучика, Рыжика; локация — `S27-Image5`. Каждый из трёх драфтов — отдельный автономный блок с START STATE = END 32.

### 3.2. Стык 25 → 26 (космос → планета ситхов) — решение D1/D3

Варианты: **(а)** без новой сцены — монтажная склейка, правок нет; **(б)** короткий переход 10–15 с (корабль заходит на посадку над руинами, коты выходят на террасу — **творческий слот**: как именно); **(в)** изменить END Scene 25: бой заканчивается подлётом к планете. Если (б): входы — `@Image4` кабина Scene 24 (интерьер), `S27-Image5` (руины), листы котов; START = END 25; END = «коты на террасе лицом к off-camera Серёге» (для Scene 26: сторона off-camera — **слот**, в аудите предложено кадр-право).

### 3.3. Активация комплекта (три фрагмента → доступ) — решение D5

Ролик 18–30 с. Что фиксируется независимо от варианта: три модуля — один дизайн-язык, у каждого свой знак; три индикатора загораются поочерёдно; число «три» читается по изображению, не по надписям; питание компьютера **не** включается, пока вы не решите иначе. Слот `[ВЫБОР D5]` — что именно открывается: **А** игровое преимущество (рекомендация v2), **Б** доступ к турниру, **В** знание есть, пользоваться не умеет, **Г** друзья уже в лобби, **Е** новое бытовое ограничение. Бит-схема (общая): 0–8 первый–второй–третий модуль; 8–15 реакция Серёги; 15–30 — разветвляется по выбору. Место действия: тот же храм (если D4 = «ПК из 35/38») или существующий финальный CRT-эпизод (иначе). Идентичность: лист Серёги; для модулей нужен референс предмета — в репозитории есть только референс единственной карты (`S17-Image4-topview-source.png`); три фрагмента как отдельные объекты не существуют (потребуются кадры из фильма: бармен/Татуин, правитель/Набу, Чубакка/лес).

### 3.4. Захват карты на Татуине — решение D6

Ролик 20–30 с; прилагает кадры Scene 16 (локация, червь) либо кантины (`S10-Image1-cantina-source`). Слот `[ВЫБОР D6]`: **кража в суматохе**, **силовое отбирание**, **иной исход** (в т. ч. «герои сохраняют фрагмент» — тогда новой сцены не нужно). Неизменное из Scene 16: червь — крупная стихия; в ней **нет обмена картой**, поэтому захват должен стоять до или после червя; судьба машины решается W6/W8. Идентичность: Ильюша, Артём, Серёга (листы).

### 3.5. Если Scene 37 разделить (по `[ВЫБОР 37-1]`)

- **37A «Отлёт» (30 с):** биты 0:00–0:05 посадка и люк; 0:05–0:12 отлёт; 0:12–0:22 подъём через атмосферу; 0:22–0:30 открытый космос, планета вдали. Входы: `@Image1`, `@Image2` (END 36), `@Image3` (корабль/космос). END: корабль уходит в сторону планеты.
- **37B «Прибытие» (30 с):** 0:00–0:08 корабль у планеты; 0:08–0:20 вход в атмосферу, облака, лесные массивы; 0:20–0:30 снижение до опушки/подхода к известному первому кадру леса. Входы: кадр корабля, **первый кадр лесной группы** (обязателен), без персонажей. END = первый кадр леса (для монтажного стыка).

## 4. Что отсюда нельзя считать решённым

- Все `[ВЫБОР …]` и все слоты каркасов §3 — ваше решение; без них я не разворачиваю промты.
- Черновики §2 **не проверены генерацией**; проверка качества — только на реальном рендере (и редакционное решение — после просмотра).
- Лимит входов и допустимость кадров вместо видео у Wan 3.0 в Topview не проверялись.
- Внешность Паши и Саши в локах — по листам (просмотр 11.10); Серёги — по листу; `character-references.json` в этой части не менялся.
- Порядок внедрения, если будете применять: сначала механические правки из `prompt-audit-2026-10.md` §4, затем (по вашему решению) замена блоков 35–38 этими черновиками, затем обновление манифестов `references/scenes/scene-35…38` (слоты и `launch_readiness`).
