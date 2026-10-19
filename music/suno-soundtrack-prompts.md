# «Серёгиус» — готовые промпты фонового саундтрека для Suno

Подготовлено 18.10.2026 по запросу владельца04:40МСК. **30 самостоятельных заданий** по сохранённой карте фильма. Владелец запускает их в Suno сам; агент музыку по этому файлу не генерировал. Это набор исходного музыкального материала для монтажа, а не утверждённые30 дорожек, которые обязательно должны звучать все.

## Как скопировать в Suno

1. Открой [Suno Create](https://suno.com/create), выбери **Custom** и включи **Instrumental**.
2. **Title** — скопируй название из раздела выбранного трека.
3. **Styles / Style of Music** — вставь весь английский блок этого трека. Он самодостаточный; дописывать общее описание фильма не требуется.
4. **Lyrics** оставь пустым. Русские пояснения и монтажные указания в Lyrics не вставляй: это не слова песни.
5. Указанная длительность — желаемая длина музыкальной заготовки с запасом. Если в твоём интерфейсе доступно отдельное поле Duration, задай её там. Если поля нет, используй доступную длительность и обрежь результат при монтаже. Темп и развитие — творческие ориентиры, не гарантия точного исполнения.
6. Один раздел — одно отдельное задание. **Не вставляй весь этот документ в одно поле:** это не пакетный импорт. Сохраняй ID трека в названии результата, например C12A, чтобы не перепутать.
7. Исходную песню прикладывать не нужно: эти инструментальные треки создаются по тексту. Аудиореференс понадобится только если позже решишь добиваться узнаваемого повтора уже выбранной собственной темы.

Во всех блоках уже указано отсутствие вокала, хора, речи и звуковых эффектов. Музыка задаётся через инструменты, темп и драматургию космического приключения; существующие мелодии фильмов и игр не заимствуются. Выбирай доступную тебе модель Suno; названия моделей Topview к этим заданиям не относятся.

**[Семь повторяющихся тем T01–T07 — готовые промпты](#recurring-themes)** и **[темы трёх команд джедаев T08–T10](#jedi-themes)** (добавлены 19.10). Вместе с эпизодными заданиями в файле теперь 40 промптов.

## С чего начать

Для быстрой проверки трёх характеров: **C12A** (приключение/полёт), **C11** (ремонт/комедия), **C22B** (храм/тайна). Остальные промпты также готовы к самостоятельному использованию.

В связанных треках повторяется инструментальная палитра и описание коротких мотивов. **Отдельные текстовые генерации не гарантируют одну и ту же мелодию.** После выбора удачной темы её можно повторять фрагментами в монтаже; получение вариаций через аудиореференс/продолжение проверяется отдельно.

## Где какой трек

Номера C — музыкальные эпизоды из [карты](soundtrack-cue-sheet.csv), не номера видеосцен. Буквы A/B/C разделяют разные музыкальные состояния одного большого эпизода. Для исторических блоков без подтверждённых Scene ID названия сохранены без выдуманных номеров.

| Код | Трек | Куда | Заготовка |
|---|---|---|---|
| [C01](#c01) | Далеко от домашнего компьютера | Вступление: титры, флот, город | 120 с |
| [C02](#c02) | Хлеб и молоко | Голограмма и бытовая просьба | 60 с |
| [C03](#c03) | Формальности галактического масштаба | Арест и юридический спор | 90 с |
| [C04](#c04) | Через окно на крышу | Кабинет, окно, крыша, противники | 120 с |
| [C05](#c05) | Осторожно, мокрый пол | Коридоры, мокрый пол, офицер | 60 с |
| [C07](#c07) | Совет и фрагмент карты | Сцена 13: совет джедаев и карта | 90 с |
| [C08](#c08) | Все по кораблям | Погрузка и посадка экипажей | 90 с |
| [C09](#c09) | РосКОТмос идёт на прорыв | Космическое сражение; готовые сцены 45–46 | 120 с |
| [C11](#c11) | Лучший флот, худшее крыло | Сцены 43–44: неисправность и ремонт крыла | 90 с |
| [C12A](#c12a) | Тогда полечу на своём | Сцена 52: пересадка, разрушитель → Татуин | 90 с |
| [C12B](#c12b) | Из песков к озёрам | Сцена 53: взлёт с Татуина и путь на Набу | 90 с |
| [C13](#c13) | Пыльные улицы Татуина | Татуин, спидеры; подход к кантине | 90 с |
| [C14A](#c14a) | Под песком что-то движется | Сцены 16, 42, 56: пустынный бой и червь | 120 с |
| [C14B](#c14b) | Верхом на неприятностях | Сцена 48: фрагмент карты и отъезд на черве | 90 с |
| [C15](#c15) | Озёрный берег Набу | Сцена 39: подлёт и посадка на берегу | 90 с |
| [C16](#c16) | Рыбаки заняты важным | Рыбалка: разговорные фрагменты сцен 19–20 до песни Маши | 60 с |
| [C17](#c17) | Подводный город | Подводный город, рынок, угроза прорыва воды | 120 с |
| [C18A](#c18a) | Монстр в пещере | Сцена 17: пещерный бой, если исходная музыка требует замены | 120 с |
| [C18B](#c18b) | После боя, с картой | Сцены 17 → 36: отдых и уход из пещеры | 90 с |
| [C19](#c19) | Сквозь грозу к Кашиику | Сцена 37: Набу → лесная планета | 90 с |
| [C20](#c20) | Высоко в кронах | Кашиик: прибытие, лес, деревня | 120 с |
| [C21](#c21) | Мост над лесной бездной | Кашиик: мост, конфликт, бой, фрагмент | 120 с |
| [C22A](#c22a) | К руинам ситхов | Сцена 40: отлёт с лесной планеты и прибытие к руинам | 90 с |
| [C22B](#c22b) | Храм забытой технологии | Сцены 33–35: руины и поиски в храме | 120 с |
| [C22C](#c22c) | Великий древний компьютер | Находка ПК: сцены 35/38 и стык с выносом | 90 с |
| [C23A](#c23a) | Два кота против галактики | Кошачья ветка: сцены 23–32, боевые фрагменты | 120 с |
| [C23B](#c23b) | Красная точка решает всё | Сцена 47: уловка с красной точкой | 60 с |
| [C24A](#c24a) | Доставка особо ценного груза | Сцена 41: вывоз ПК, полёт к разрушителю | 90 с |
| [C24B](#c24b) | Компьютер наконец дома | Сцена 54: установка ПК в комнате корабля | 90 с |
| [C25](#c25) | Наконец-то поиграю | Warcraft-финал до вопроса о продуктах; сцена 55 | 60 с |

## Эпизоды, где отдельный фон не нужен

| Код карты | Эпизод | Что использовать |
|---|---|---|
| C06 | Танец на мостике | Уже выбранную музыку сцены; новую оркестровую подложку поверх не добавлять. |
| C10 | Корова и музыкальная шутка при гиперпрыжках | Существующую музыкальную шутку; для соседних перелётов подойдут фрагменты дорожек пути по монтажу. |
| C26 | Финальный танец, сцена28 | Сохранённое музыкальное решение сцены; этот файл его не заменяет. |
| C27 | Рок-номер49–51, вуки-фанаты, инструменты | Одну выбранную песню на весь номер. Готовые варианты и ссылки — в [music/README.md](README.md). |

C13 относится к подходу к кантине, C16 — к рыбалке и разговорам: во время уже существующего танца в кантине и песни Маши новый фон выключается. C25 заканчивается **до** вопроса о хлебе и молоке. Для тишины отдельная генерация не нужна.

## Задания для копирования

<a id="c01"></a>

### C01 — Далеко от домашнего компьютера

**Title:** `C01 | Серёгиус — Далеко от домашнего компьютера`  
**Куда:** Вступление: титры, флот, город.  
**Ориентир:** 120 секунд; около 104 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Вступительная тема; под закадровым текстом использовать более редкую середину.

**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-adventure opening, 104 BPM, broad 4/4. Warm French horns introduce a concise, singable four-note heroic idea: two rising gestures, a held note, a dry descending answer. Sweeping strings, answering flutes, restrained trumpets and timpani; spacious acoustic orchestra with only a faint cosmic synth bed. A grand galaxy seen through an earnest, stubborn hero's eyes, with a subtle hint of domestic absurdity. Begin promptly with a short fanfare, open into a lighter narration-friendly passage, then reprise the theme with warm confidence. Distinct eight-bar phrases, uncluttered middle register, a resolved ending with a natural reverb tail. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c02"></a>

### C02 — Хлеб и молоко

**Title:** `C02 | Серёгиус — Хлеб и молоко`  
**Куда:** Голограмма и бытовая просьба.  
**Ориентир:** 60 секунд; около 76 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Очень тихо под разговором; запомнить тембр для финала. Слова о продуктах оставить разборчивыми.

**Styles — скопировать целиком:**

```text
Instrumental only. Original intimate orchestral domestic-comedy underscore, 76 BPM. Warm solo clarinet, soft pizzicato cello, a few dry piano notes and a tiny celesta answer. An imposing space traveller receives a completely ordinary grocery reminder. Affectionate, understated and matter-of-fact, with a modest two-note questioning gesture; no sentimental swell. Begin lightly, alternate short phrases with generous quiet spaces, allow one mildly distracted harmonic detour, then settle into an open gentle ending. Small chamber ensemble, low density, restrained dynamics and room for spoken dialogue throughout. The humor comes from disproportion, not cartoon accents. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c03"></a>

### C03 — Формальности галактического масштаба

**Title:** `C03 | Серёгиус — Формальности галактического масштаба`  
**Куда:** Арест и юридический спор.  
**Ориентир:** 90 секунд; около 88 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Паузы и реплики важнее музыкального развития; не накладывать акцент на каждую шутку.

**Styles — скопировать целиком:**

```text
Instrumental only. Original orchestral procedural tension with dry deadpan humor, 88 BPM. Muted violas repeat a measured pulse under bass clarinet, soft bassoon and restrained low horn chords. A supposedly intimidating arrest becomes an absurdly serious legal argument. Start with controlled suspicion, exchange small question-and-answer figures between woodwinds, briefly tighten the harmony, then let the tension deflate without a punchline sting. No heroic fanfare, no sinister horror drone. Sparse foreground, regular phrase breaks and long pockets for dialogue. End on a short uncertain woodwind phrase and a clean natural decay. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c04"></a>

### C04 — Через окно на крышу

**Title:** `C04 | Серёгиус — Через окно на крышу`  
**Куда:** Кабинет, окно, крыша, противники.  
**Ориентир:** 120 секунд; около 138 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Энергичный материал для боевого блока; удары, разбитое стекло и крики — отдельные дорожки.

**Styles — скопировать целиком:**

```text
Instrumental only. Original kinetic symphonic action cue, 138 BPM, driving 4/4. Agile low-string ostinatos, bright violins, forceful but concise horn calls, timpani and tightly controlled orchestral snare. A confrontation bursts from a cramped office into an exposed rooftop chase. Open with immediate forward momentum, build through climbing sequences, thin the texture for a short breath, then return with a decisive brass-and-string surge. Keep melodic lines readable and percussion acoustic; tension comes from movement rather than endless loud impacts. Strong phrase boundaries, contrasting medium and high energy sections, one firm final chord and a clean tail. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c05"></a>

### C05 — Осторожно, мокрый пол

**Title:** `C05 | Серёгиус — Осторожно, мокрый пол`  
**Куда:** Коридоры, мокрый пол, офицер.  
**Ориентир:** 60 секунд; около 96 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Можно использовать только отдельные фразы; скольжение и реакция лучше работают без подчеркивания.

**Styles — скопировать целиком:**

```text
Instrumental only. Original restrained orchestral physical-comedy underscore, 96 BPM. Plucked strings, dry bassoon, short clarinet figures and a very occasional soft woodblock. A dignified officer tries to maintain authority in an embarrassingly slippery corridor. Keep the performance solemn and precise, with a prim little walking rhythm that hesitates, resumes and loses one beat. A brief poised opening, sparse stop-and-start development and a tiny unresolved ending. Frequent real rests, small dynamic range, no busy lead melody. Avoid cartoon slides, circus music and exaggerated musical pratfalls. Leave space for footsteps, dialogue and the visual joke. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c07"></a>

### C07 — Совет и фрагмент карты

**Title:** `C07 | Серёгиус — Совет и фрагмент карты`  
**Куда:** Сцена 13: совет джедаев и карта.  
**Ориентир:** 90 секунд; около 72 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Низкая плотность под диалогом и говорящим Лучиком; загадка без лишнего пафоса.

**Styles — скопировать целиком:**

```text
Instrumental only. Original chamber-orchestral mystery underscore, 72 BPM. Bass clarinet and low strings form a quiet, curious foundation; sparse celesta and harp introduce a three-note questioning motif. A council debates an ancient map fragment with great solemnity despite an unexpectedly unusual participant. Begin with patient uncertainty, let the motif pass between celesta and clarinet, offer a small warm harmonic clue and finish unresolved but inviting. Serious adventure with a trace of dry wit, never horror or parody music. Very light pulse, restrained low brass, clear gaps between phrases and plenty of room for speech. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c08"></a>

### C08 — Все по кораблям

**Title:** `C08 | Серёгиус — Все по кораблям`  
**Куда:** Погрузка и посадка экипажей.  
**Ориентир:** 90 секунд; около 112 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Общий монтаж сборов; под отдельными звуковыми шутками делать провалы.

**Styles — скопировать целиком:**

```text
Instrumental only. Original orchestral departure montage, 112 BPM. Nimble strings, buoyant clarinet answers, warm French horns, light timpani and a subtle airy synth texture. Different crews prepare for a grand expedition with brisk practical purpose. Start with a compact rhythmic pickup, build an optimistic rising four-note idea, pass through a lighter woodwind section, then bring the orchestra together for a clear departure. Energetic but not a full battle cue; modest comic timing without slapstick. Short editable phrases, alternating low-density and fuller passages, no long intro, a clean confident cadence with a natural tail. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c09"></a>

### C09 — РосКОТмос идёт на прорыв

**Title:** `C09 | Серёгиус — РосКОТмос идёт на прорыв`  
**Куда:** Космическое сражение; готовые сцены 45–46.  
**Ориентир:** 120 секунд; около 132 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Музыка серьёзного прорыва. Столкновения спутников и отделение деталей синхронизировать монтажом, не аудиопромптом.

**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-battle score, 132 BPM. Low horns and bass trombones state a compact, proud descending three-note motif over racing cellos, violas and controlled timpani. An improbably determined feline crew pilots a formidable spacecraft through a real fleet engagement. Play their courage completely straight; weighty brass, swift strings and a faint dark electronic undertone. Open already moving, intensify into a coordinated breakthrough, briefly expose the low motif, then surge toward a resolute exit. Wide dynamics without constant trailer impacts, clear musical punctuation, no comic meowing. A decisive ending with space for separate battle sound design. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c11"></a>

### C11 — Лучший флот, худшее крыло

**Title:** `C11 | Серёгиус — Лучший флот, худшее крыло`  
**Куда:** Сцены 43–44: неисправность и ремонт крыла.  
**Ориентир:** 90 секунд; около 92 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Увести музыку перед падением крыла и последней репликой. Нужные остановки поставить при монтаже; Suno не синхронизируется с кадром.

**Styles — скопировать целиком:**

```text
Instrumental only. Original deadpan orchestral repair-comedy underscore, 92 BPM. Small ensemble of bassoon, muted low brass, pizzicato strings and sparse woodblock. Very serious technicians become increasingly energetic while a stubborn spaceship wing refuses to cooperate. Begin with a precise little diagnostic pulse, repeat it with gradually more determined instrumental answers, rise to one overconfident flourish, then stop abruptly into a conspicuous pause. Resume only with a tiny embarrassed bassoon question and finish dry. The hero remains cold and unimpressed. Plenty of room for Russian dialogue and mechanical sound design; humor through rhythm and silence, not cartoon effects. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c12a"></a>

### C12A — Тогда полечу на своём

**Title:** `C12A | Серёгиус — Тогда полечу на своём`  
**Куда:** Сцена 52: пересадка, разрушитель → Татуин.  
**Ориентир:** 90 секунд; около 116 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Начало — разочарование после ремонта; далее уверенный полёт и приземление. Стикер не выделять громким ударом.

**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-travel cue, 116 BPM. A small dry bassoon hesitation gives way to warm French horns, agile strings, light woodwinds and restrained timpani. A resolute hero abandons a broken shuttle, boards his own craft and finally gets underway toward a desert world. Build from practical determination into a rising four-note travel idea, open into a broad airborne passage, then soften into a sunlit arrival. Earnest adventure with one subtle comic aftertaste, no exaggerated triumph. Immediate musical direction, distinct phrases, a lighter middle for cockpit shots and a clean settled ending. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c12b"></a>

### C12B — Из песков к озёрам

**Title:** `C12B | Серёгиус — Из песков к озёрам`  
**Куда:** Сцена 53: взлёт с Татуина и путь на Набу.  
**Ориентир:** 90 секунд; около 130 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Быстрый старт и каньон; конец спокойнее для перехода к Набу. Отдельная версия пути.

**Styles — скопировать целиком:**

```text
Instrumental only. Original exhilarating orchestral flight cue, 130 BPM. Tight string ostinatos and short horn calls propel a small personal spacecraft from a desert outpost through a winding canyon into open space. Use warm brass, agile flutes, timpani and a restrained spacious synth layer. Introduce a clear rising four-note travel gesture, sharpen the rhythm through a fast central passage, then broaden the harmony as the destination becomes a watery green world. Skilled movement, exhilaration and forward purpose rather than danger or tragedy. Clear contrasting sections, editable phrase ends, a gentler resolved close and a natural tail. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c13"></a>

### C13 — Пыльные улицы Татуина

**Title:** `C13 | Серёгиус — Пыльные улицы Татуина`  
**Куда:** Татуин, спидеры; подход к кантине.  
**Ориентир:** 90 секунд; около 92 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Только наружный фон и подход. Перед музыкой кантины/танцем закончить трек; существующий танец не заменять.

**Styles — скопировать целиком:**

```text
Instrumental only. Original orchestral desert-town underscore, 92 BPM. Dry plucked cello, warm bass clarinet, breathy flute, restrained frame drum and thin shimmering strings. Sun-baked streets, dusty vehicles and a traveller making his way toward a busy cantina. Curious and slightly wary, with a gently rolling pulse and a spare melody that leaves the environment audible. Begin with open space, add a modest walking rhythm, briefly brighten with woodwind answers, then thin back to a few plucked notes. Cinematic and organic, no nightclub groove. Finish quietly and cleanly so source music inside the next location can enter. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c14a"></a>

### C14A — Под песком что-то движется

**Title:** `C14A | Серёгиус — Под песком что-то движется`  
**Куда:** Сцены 16, 42, 56: пустынный бой и червь.  
**Ориентир:** 120 секунд; около 144 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Для боевой дуги; редактировать по реальным моментам боя. Рёв и световые мечи не включать в музыку.

**Styles — скопировать целиком:**

```text
Instrumental only. Original high-energy orchestral desert-action cue, 144 BPM. Rapid low strings, tense violin figures, biting but controlled horns, bass trombone and rolling timpani. Three fighters are locked in a dangerous confrontation while a colossal creature rises above them. Start with urgent forward motion, expand the harmonic scale as the threat grows, insert a sparse suspended passage, then drive into a vigorous final section. Keep a small questioning three-note motif hidden in the woodwinds to suggest the larger quest. Clear rhythm, strong contrasts, no wall of percussion. Finish on a firm suspended chord suitable for an editorial transition. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c14b"></a>

### C14B — Верхом на неприятностях

**Title:** `C14B | Серёгиус — Верхом на неприятностях`  
**Куда:** Сцена 48: фрагмент карты и отъезд на черве.  
**Ориентир:** 90 секунд; около 120 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Побег и абсурдная победа; героическая музыка играет всерьёз. При переходе с боя не накладывать две дорожки.

**Styles — скопировать целиком:**

```text
Instrumental only. Original exuberant orchestral adventure-comedy cue, 120 BPM, buoyant 6/8. Galloping strings, warm horn melody, quick flute answers and light timpani. After an absurdly dangerous encounter, the hero gets the map fragment and rides away on a gigantic desert creature with complete seriousness. Begin tense and nimble, release into a bold ascending phrase, carry a wide swinging sense of travel, then let a tiny woodwind reply puncture the grandeur without ruining it. Real cinematic excitement, no circus style or cartoon sound effects. Clear melodic phrases, a short quieter pocket and a confident final cadence. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c15"></a>

### C15 — Озёрный берег Набу

**Title:** `C15 | Серёгиус — Озёрный берег Набу`  
**Куда:** Сцена 39: подлёт и посадка на берегу.  
**Ориентир:** 90 секунд; около 84 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Сохранить воздух, воду и шум двигателя. В конце музыка уступает береговой атмосфере.

**Styles — скопировать целиком:**

```text
Instrumental only. Original luminous orchestral arrival cue, 84 BPM. Flowing strings, solo flute and oboe, delicate harp, warm restrained horns and soft celesta highlights. A small craft approaches a brilliant lake and a peaceful grassy shore; forward motion gradually turns into quiet wonder. Start with a gentle travelling pulse, open a broad lyrical phrase, then reduce to chamber textures as the craft comes to rest. Clear daylight, water and air, hopeful rather than sentimental. No grand finale, no long drone. Leave the middle register open, use graceful phrase endings and finish with a soft, clean natural decay. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c16"></a>

### C16 — Рыбаки заняты важным

**Title:** `C16 | Серёгиус — Рыбаки заняты важным`  
**Куда:** Рыбалка: разговорные фрагменты сцен 19–20 до песни Маши.  
**Ориентир:** 60 секунд; около 80 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Фон только для разговоров, если он нужен. Перед песней Маши выключить полностью; её вокал не дублировать.

**Styles — скопировать целиком:**

```text
Instrumental only. Original delicate lakeside comedy underscore, 80 BPM. Light pizzicato strings, mellow clarinet, bassoon and a few widely spaced harp notes. Two absorbed fishermen take their unhurried business extremely seriously while something more dramatic is about to interrupt them. Relaxed but not sleepy: a small strolling figure, gentle question-and-answer phrases and generous pauses for dialogue. Keep the melody modest, dynamics soft and harmony warm with one slightly awkward turn. No romantic swell, no percussion groove, no imitation of an existing song. Finish early and lightly so a separate vocal performance can begin in complete musical space. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c17"></a>

### C17 — Подводный город

**Title:** `C17 | Серёгиус — Подводный город`  
**Куда:** Подводный город, рынок, угроза прорыва воды.  
**Ориентир:** 120 секунд; около 78 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Первая часть — чудо и рынок; затем тревога. Шум прорыва воды оставлять отдельным эффектом.

**Styles — скопировать целиком:**

```text
Instrumental only. Original orchestral underwater-city cue, 78 BPM. Translucent divided strings, harp harmonics, celesta, soft flutes and a restrained low spatial synth bed. Begin with calm architectural wonder and a gently swaying pulse; add small animated woodwind figures for a living marketplace. Gradually darken the harmony with bass clarinet and low strings as a hidden structural threat emerges. End in controlled unresolved tension rather than a horror climax. Distinct wonder, activity and suspense sections with room for spoken exchanges. Organic orchestral detail, no watery sound effects, no giant impact, clean phrase boundaries and a quiet final decay. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c18a"></a>

### C18A — Монстр в пещере

**Title:** `C18A | Серёгиус — Монстр в пещере`  
**Куда:** Сцена 17: пещерный бой, если исходная музыка требует замены.  
**Ориентир:** 120 секунд; около 136 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Условный фон для существующего боя. Не запускать как обязательную замену хорошей встроенной музыки.

**Styles — скопировать целиком:**

```text
Instrumental only. Original dark symphonic creature-battle cue, 136 BPM. Churning cellos and basses, urgent upper strings, low horn calls, timpani and restrained bass drum. A desperate fight in a vast wet cavern becomes a hard-won collective victory. Immediate tension, a driving central confrontation, a brief breath with exposed low strings, then one clear surge toward resolution. Give the melody a stubborn heroic contour without constant fanfares. Keep percussion articulate and leave occasional open pockets for impacts and dialogue. Serious adventure rather than horror sound design; finish with a short exhausted release, not an oversized triumphal ending. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c18b"></a>

### C18B — После боя, с картой

**Title:** `C18B | Серёгиус — После боя, с картой`  
**Куда:** Сцены 17 → 36: отдых и уход из пещеры.  
**Ориентир:** 90 секунд; около 64 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Тихий переход: герои сидят, Серёга забирает единственный модуль и уходит. Оставить воду и шаги.

**Styles — скопировать целиком:**

```text
Instrumental only. Original quiet orchestral aftermath cue, 64 BPM. Warm cello, low clarinet, sparse harp and a few distant celesta notes over very soft sustained strings. Exhausted companions sit in a cavern after a victory; a small ancient map fragment quietly restores the hero's sense of purpose. Begin with tired relief, introduce a restrained three-note questioning idea, allow a gentle forward movement and return to calm. No victory march, no melodrama, no continuous arpeggios. Spacious chamber writing with long rests for dialogue and cave ambience. End with an understated open cadence and a delicate natural tail. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c19"></a>

### C19 — Сквозь грозу к Кашиику

**Title:** `C19 | Серёгиус — Сквозь грозу к Кашиику`  
**Куда:** Сцена 37: Набу → лесная планета.  
**Ориентир:** 90 секунд; около 128 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Низкий пролёт и штопор через грозу; после облака — простор. Гром и дождь из видеозвука.

**Styles — скопировать целиком:**

```text
Instrumental only. Original kinetic symphonic flight cue, 128 BPM. Racing strings, confident French horns, agile flute replies and rolling timpani. A small craft skims a lake, spirals through a towering storm cloud and emerges into clear space toward a forest world. Present a compact rising four-note travel gesture, intensify with climbing sequences and darker harmony, then open into broad warm brass above a lighter string pulse. Energetic, skilful and exhilarating, with a calmer window for a cockpit navigation moment. No disaster tone, no endless percussion impacts. Distinct phrases, one brief musical breath and a clean hopeful ending. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c20"></a>

### C20 — Высоко в кронах

**Title:** `C20 | Серёгиус — Высоко в кронах`  
**Куда:** Кашиик: прибытие, лес, деревня.  
**Ориентир:** 120 секунд; около 82 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Дерево и глубина; местные голоса и звуки леса должны оставаться слышны.

**Styles — скопировать целиком:**

```text
Instrumental only. Original orchestral forest-world underscore, 82 BPM. Low wooden flutes, bass clarinet, warm viola and cello, delicate plucked strings and sparse resonant wooden percussion. A traveller enters a towering forest settlement suspended among immense trees. Grounded, spacious and quietly curious; a slow organic walking pulse supports a restrained lyrical line. Begin with depth and stillness, gently reveal a warmer inhabited world, then settle into a light dialogue-friendly texture. No ceremonial chanting, no stereotyped tribal fanfare, no nature sound recordings. Clear breathing phrases, moderate acoustic reverb and an open gentle ending. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c21"></a>

### C21 — Мост над лесной бездной

**Title:** `C21 | Серёгиус — Мост над лесной бездной`  
**Куда:** Кашиик: мост, конфликт, бой, фрагмент.  
**Ориентир:** 120 секунд; около 126 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Под историей об адвокате использовать разреженный участок или тишину; бой — плотнее.

**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic forest-bridge action cue, 126 BPM. Tense plucked low strings grow into agile bowed ostinatos, short horn figures and controlled orchestral percussion. A precarious confrontation above a deep forest escalates into a sharp fight, then reveals another clue to the quest. Begin with cautious rhythmic suspense, move into a brisk central action passage, briefly strip back to bass clarinet and cello for a spoken exchange, then resolve with a small celesta question. Serious physical stakes with deadpan restraint. Strong contrasts without trailer-style booms, editable phrase ends and a short calm closing section. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c22a"></a>

### C22A — К руинам ситхов

**Title:** `C22A | Серёгиус — К руинам ситхов`  
**Куда:** Сцена 40: отлёт с лесной планеты и прибытие к руинам.  
**Ориентир:** 90 секунд; около 120 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Переход от полёта к тревожному исследованию; конец подходит к входу в руины.

**Styles — скопировать целиком:**

```text
Instrumental only. Original orchestral journey-to-ruins cue, 120 BPM. Warm horns and active strings begin with determined travel energy; bass clarinet, low brass and sparse celesta gradually shift the mood toward an ancient mystery. A hero leaves a green forest world and descends toward monumental ochre ruins beneath a hazy sunset. State a compact rising travel gesture, drive through one energetic middle passage, then slow the perceived motion through longer harmonies and reduced percussion. Wonder and unease, never horror. Keep clear phrase divisions, space for a cockpit insert and a restrained unresolved ending for entry into the ruins. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c22b"></a>

### C22B — Храм забытой технологии

**Title:** `C22B | Серёгиус — Храм забытой технологии`  
**Куда:** Сцены 33–35: руины и поиски в храме.  
**Ориентир:** 120 секунд; около 66 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Очень редкая подложка. Шаги, воздух храма и реплики в приоритете.

**Styles — скопировать целиком:**

```text
Instrumental only. Original orchestral ancient-temple mystery, 66 BPM. Low divided strings, bass clarinet, sparse celesta, single harp notes and very restrained low horns. A quiet explorer moves through monumental ruins toward a concealed technological relic. Introduce a small three-note questioning motif, let it echo between acoustic instruments, gradually reveal a warmer harmonic possibility, then hold the answer back. Patient discovery, architectural scale and curiosity; no horror drone, no sacred choir or chanting. Thin musical texture, deliberate silence between gestures, clear transitions and a soft unresolved ending with a clean natural tail. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c22c"></a>

### C22C — Великий древний компьютер

**Title:** `C22C | Серёгиус — Великий древний компьютер`  
**Куда:** Находка ПК: сцены 35/38 и стык с выносом.  
**Ориентир:** 90 секунд; около 74 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Музыка воспринимает старый бежевый компьютер как святыню; не добавлять компьютерные сигналы.

**Styles — скопировать целиком:**

```text
Instrumental only. Original restrained orchestral revelation cue, 74 BPM. Celesta and harp outline a curious three-note figure over soft strings; warm French horns slowly uncover a simple noble melody. An ancient temple reveals a supposedly priceless relic that is, absurdly, an old beige desktop computer. Treat the discovery with sincere awe and dignity, allowing the visual incongruity to carry the joke. Begin hushed, bloom into one warm harmonic reveal, then return to practical chamber-scale motion for carrying the object away. No parody sting, no triumphant wall of brass. Editable phrases, clear melodic space and a modest resolved ending. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c23a"></a>

### C23A — Два кота против галактики

**Title:** `C23A | Серёгиус — Два кота против галактики`  
**Куда:** Кошачья ветка: сцены 23–32, боевые фрагменты.  
**Ориентир:** 120 секунд; около 140 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Общий материал ветки; разбить под фактический монтаж. Не считать номера сцен гарантированно соседними.

**Styles — скопировать целиком:**

```text
Instrumental only. Original serious orchestral feline-heroes action cue, 140 BPM. Proud low horns and trombones state a compact descending three-note idea while cellos and violas drive a nimble repeating rhythm. Two fearless feline warriors face an outsized galactic conflict with absolute conviction. Tight, agile strings and restrained timpani, alternating broad heroic statements with light stalking woodwinds. Start decisively, build a swift confrontation, introduce a brief quiet tactical passage and finish with renewed momentum. The comedy lives in the picture, not novelty instruments. No meowing or cartoon gestures; clear sections and a firm clean ending. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c23b"></a>

### C23B — Красная точка решает всё

**Title:** `C23B | Серёгиус — Красная точка решает всё`  
**Куда:** Сцена 47: уловка с красной точкой.  
**Ориентир:** 60 секунд; около 108 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Начало ещё серьёзное; затем музыка становится лёгкой. Не акцентировать каждое движение точки.

**Styles — скопировать целиком:**

```text
Instrumental only. Original deadpan orchestral distraction cue, 108 BPM. A stern low-horn phrase starts with grand confidence, then abruptly gives way to nimble pizzicato strings, curious bassoon and small clarinet leaps. A formidable confrontation is undone by an irresistibly tiny moving point of light. Keep the performers musically earnest; light precise stalking rhythm, sudden pockets of silence and restrained playful motion rather than cartoon chaos. Develop a short descending three-note figure into smaller fragments, allow one comic hesitation, and finish with a tiny unresolved woodwind answer. Sparse mix, no novelty sound effects and no constant synchronized hits. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c24a"></a>

### C24A — Доставка особо ценного груза

**Title:** `C24A | Серёгиус — Доставка особо ценного груза`  
**Куда:** Сцена 41: вывоз ПК, полёт к разрушителю.  
**Ориентир:** 90 секунд; около 134 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Для динамики посадки с ПК и полёта. Падение каменной головы и грохот CRT — отдельные эффекты.

**Styles — скопировать целиком:**

```text
Instrumental only. Original energetic orchestral homeward-flight cue, 134 BPM. Fast strings, warm determined horns, light woodwind answers and articulate timpani. A hero protects an ancient beige computer as though it were the galaxy's greatest treasure, dodging falling ruins and braking hard toward his flagship. Open with practical urgency, develop a clear rising heroic gesture through a short danger passage, then broaden into relief without losing momentum. A brief lighter texture allows a cockpit gag to breathe before a controlled arrival. Sincere, adventurous and slightly absurd; no catastrophe ending. Strong editable phrases and a confident but compact final cadence. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c24b"></a>

### C24B — Компьютер наконец дома

**Title:** `C24B | Серёгиус — Компьютер наконец дома`  
**Куда:** Сцена 54: установка ПК в комнате корабля.  
**Ориентир:** 90 секунд; около 72 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Камерный домашний вариант после большого путешествия. Завершить до включения компьютера в следующем клипе.

**Styles — скопировать целиком:**

```text
Instrumental only. Original warm chamber-orchestral homecoming underscore, 72 BPM. Solo clarinet, soft cello, gentle piano, restrained harp and a small horn phrase far in the background. After a vast galactic journey, the hero carefully installs an old computer on his desk with immense personal satisfaction. Begin with a relaxed descending answer to a heroic rising idea, settle into a modest practical pulse, then let the harmony warm as everything finds its place. Understated relief, no sentimental climax or triumphal march. Sparse dialogue-friendly texture, short clear phrases, finish softly just before the next action with a clean tail. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```

<a id="c25"></a>

### C25 — Наконец-то поиграю

**Title:** `C25 | Серёгиус — Наконец-то поиграю`  
**Куда:** Warcraft-финал до вопроса о продуктах; сцена 55.  
**Ориентир:** 60 секунд; около 90 BPM; Instrumental включён; Lyrics пустое.  
**Для монтажа:** Только подход к игре, если нужен фон. Полностью закончить ДО вопроса о хлебе и молоке; сам вопрос и реакция — без новой музыки.

**Styles — скопировать целиком:**

```text
Instrumental only. Original understated orchestral gaming-anticipation cue, 90 BPM. Warm clarinet, pizzicato cello, soft piano and a few bright celesta notes; a very small repeating pulse suggests absorbed concentration. A traveller finally relaxes at his recovered computer, convinced that all interruptions are over. Comfortable, quietly pleased and gently comic, without imitating any existing game theme. Begin with relief, settle into a light regular figure, gradually reduce the instrumentation and end with a short dry cadence followed by clear silence. No dramatic sting or grand finish. Leave ample space for separate gameplay audio and a later spoken punchline. No vocals, choir, spoken words or sound effects. Original melodies only; natural acoustic dynamics.
```


<a id="recurring-themes"></a>

## Семь повторяющихся тем — музыкальная основа фильма

Добавлено 18.10.2026 по отдельному запросу владельца. **7 тем T01–T07 дополняют 30 эпизодных заданий Cxx.** Это исходные темы для повторного использования, а не семь дополнительных обязательных слоёв поверх готовой музыки. Всё — оригинальный приключенческий симфонический оркестр: духовые, подвижные струнные, загадочные камерные тембры. Без заимствования мелодий существующих фильмов и игр.

Сначала создай и выбери удачный вариант каждой T-темы. В связанных сценах повторяй фрагменты выбранной записи; для точного возвращения темы используй тот же аудиофрагмент. Отдельные генерации по похожему тексту **не гарантируют ту же мелодию**. Если позднее нужны новые аранжировки, используй выбранное собственное аудио как основу через доступные в твоём аккаунте функции; их доступность и стоимость проверяются отдельно. Описанные интервалы и форма — пожелания, результат нужно прослушать.

Для каждой темы: **Instrumental включён, Lyrics пустое; английский блок — в Styles.** Длительность ниже — ориентир заготовки, не точный хронометраж сцены. Название — в Title. Каждый блок запускается отдельно.

| Код | Тема | Где повторять |
|---|---|---|
| T01 | Главная тема героя | C01, C08, C12A/B, C19, C24A/B |
| T02 | Героическая тема котов | C09, C23A; короткая комическая вариация в C23B |
| T03 | Сквозная тема поиска | C07, C18B, C21, C22B/C; моменты получения фрагментов |
| T04 | Тема пути и открытого космоса | C12A/B, C15, C19, C22A, C24A |
| T05 | Общая тема опасности и сопротивления | C04, C14A/B, C18A, C21; для котов преимущественно T02 |
| T06 | Напоминание, ремонт и серьёзный абсурд | C02, C03, C05, C11, C16, C23B; финальная пауза без музыки |
| T07 | Тема возвращения и покоя | C24B, C25; спокойная реприза T01 после выбора аудио |

### T01 — Серёга — Я ненадолго

**Title:** `T01 | Серёгиус — Серёга — Я ненадолго`  
**Повторять:** C01, C08, C12A/B, C19, C24A/B.  
**Ориентир:** 112 BPM; 120–150 секунд.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-adventure film theme, 112 BPM. Warm French horns lead a memorable four-note motif: an upward leap, two determined rising steps, then a gently falling answer. Agile strings, answering clarinets, trumpets and acoustic timpani. An earnest, stubborn ordinary man treats a wildly disproportionate galactic errand as a quick trip before gaming. Noble, adventurous and warmly human, with dry humor rather than parody. State the hook clearly in the first eight bars, develop it through an energetic journey, present a sparse clarinet-and-cello version, then return to a confident orchestral statement. Clear eight-bar phrases and a compact resolved ending. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

### T02 — Коты — РосКОТмос

**Title:** `T02 | Серёгиус — Коты — РосКОТмос`  
**Повторять:** C09, C23A; короткая комическая вариация в C23B.  
**Ориентир:** 132 BPM; 120–150 секунд.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-adventure film theme, 132 BPM. Low French horns and trombones state a bold three-note descending motif, answered by nimble violas and bassoon. Agile string ostinatos, precise orchestral snare and timpani. Two fearless feline pilots and warriors take themselves completely seriously. Proud, disciplined, fast and resourceful; sincere heroism, no cute novelty music. Introduce the motif immediately, expand into a brisk breakthrough, reduce to a stealthy pizzicato passage, then bring back the same theme in full brass. Strong rhythm without a rigid military march. No meowing. Clean phrase endings and one decisive final cadence. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

### T03 — Карта — Три ноты тайны

**Title:** `T03 | Серёгиус — Карта — Три ноты тайны`  
**Повторять:** C07, C18B, C21, C22B/C; моменты получения фрагментов.  
**Ориентир:** 70 BPM; 120–150 секунд.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-adventure film theme, 70 BPM. Celesta introduces a distinctive three-note question: one small upward movement followed by a wider downward answer, left harmonically unresolved. Bass clarinet, low divided strings, sparse harp and restrained French horns. Scattered ancient map fragments gradually reveal a path to a hidden technological treasure. Curious and wondrous, never horror. Begin with the exposed motif, repeat it with changing harmony and instrumentation, move through a slightly more urgent middle, then briefly reveal a warm major-colored answer before a quiet unresolved ending. Spacious phrasing with real rests and room for dialogue; no continuous drone. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

### T04 — Перелёты — Между мирами

**Title:** `T04 | Серёгиус — Перелёты — Между мирами`  
**Повторять:** C12A/B, C15, C19, C22A, C24A.  
**Ориентир:** 124 BPM; 150–180 секунд.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-adventure film theme, 124 BPM. Soaring French horns carry a clear ascending five-note travel phrase above flowing strings and agile flute replies. Harp, light timpani and an almost inaudible cosmic synth bed within a predominantly acoustic orchestra. A small personal spacecraft crosses immense worlds, storms, desert skylines and lakes. Exhilarating forward motion and spacious discovery. Start promptly with the main phrase, develop a nimble flight section, open into a broad weightless panorama with reduced percussion, then reprise the theme for a controlled arrival. Contrasting textures, edit-friendly eight-bar sections and a warm resolved tail; no engine noises. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

### T05 — Сражения — Всё мешает пройти

**Title:** `T05 | Серёгиус — Сражения — Всё мешает пройти`  
**Повторять:** C04, C14A/B, C18A, C21; для котов преимущественно T02.  
**Ориентир:** 144 BPM; 120–150 секунд.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-adventure film theme, 144 BPM. Cellos and violas drive a distinctive syncopated short-short-long rhythmic motif, answered by concise horn calls and tense climbing violins. Acoustic timpani, controlled snare and low brass, with clear melody above the pulse. A stubborn hero fights through increasingly absurd obstacles on a very personal quest. Urgent, agile and determined, not grim or apocalyptic. Immediate rhythmic entry, escalating confrontation, a short sparse tactical pause, renewed action and a brief hard-won release. Preserve audible motif identity through the changes. No trailer booms, endless impacts or percussion wall. Firm clean ending. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

### T06 — Бытовая комедия — Хлеб и молоко

**Title:** `T06 | Серёгиус — Бытовая комедия — Хлеб и молоко`  
**Повторять:** C02, C03, C05, C11, C16, C23B; финальная пауза без музыки.  
**Ориентир:** 84 BPM; 90–120 секунд.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-adventure film theme, 84 BPM. Solo clarinet plays a simple two-note questioning gesture, followed after a real pause by a dry bassoon answer. Pizzicato cello, soft piano, occasional celesta; intimate chamber orchestra. An ordinary grocery reminder persists through grand adventures, pompous bureaucracy and an increasingly incompetent spacecraft repair. Affectionate deadpan humor, musicians utterly serious. Present the tiny hook clearly, develop a prim walking variation, build one restrained knot of rhythmic confusion, stop briefly, then resume with an innocently small answer. Sparse speech-friendly writing, no circus music, slide whistles or cartoon falls. Short dry ending with silence. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

### T07 — Возвращение домой — Почти всё вспомнил

**Title:** `T07 | Серёгиус — Возвращение домой — Почти всё вспомнил`  
**Повторять:** C24B, C25; спокойная реприза T01 после выбора аудио.  
**Ориентир:** 72 BPM; 120–150 секунд.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic space-adventure film theme, 72 BPM. Solo cello and warm clarinet introduce a modest lyrical homecoming melody, answered by soft piano and harp, with distant French horns recalling a heroic journey. An exhausted traveller finally sets his recovered old computer on the desk and believes he can relax. Quiet relief, affection and satisfaction with a faint unresolved domestic question. Begin intimately, bloom once into a restrained warm string ensemble, return to a light absorbed pulse, then gradually strip the instrumentation down to a brief dry cadence and silence. No sentimental climax, victory march or comic sting. Leave room for a later spoken punchline. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

<a id="jedi-themes"></a>

## Темы трёх команд джедаев — T08–T10

Добавлено 19.10.2026 по вопросу владельца. У каждой пары джедаев свой короткий мотив, чтобы зритель узнавал команду по музыке: при первом появлении пары, на сборах экипажей (C08) и в момент, когда пара теряет фрагмент карты. Палитра та же, что у T01–T07 (оркестр), но у каждой команды свой «голос»: Татуин — сухие щипковые и низкая медь, Набу — арфа, маримба и дуэт в терциях, Кашиик — деревянная перкуссия и перекличка низкой меди с деревом. Внутри пары мотив устроен как диалог двух героев. Как и с T01–T07: сначала выбрать удачный вариант, потом повторять фрагменты этой записи; отдельные генерации одну мелодию не гарантируют.

| Код | Команда | Где повторять |
|---|---|---|
| T08 | Татуин: Илюша и Артём | C08 (их посадка), C13, C14A/B; потеря фрагмента в 48 — короткий минорный обрывок |
| T09 | Набу: Паша и Саша | C08, C16 (до песни Маши), C17, C18A/B; уход Серёги с фрагментом в 36 — короткий обрывок |
| T10 | Кашиик: Лёша и Виталик | C08, C20, C21; притягивание фрагмента Канцлером — короткий обрывок |

### T08 — Татуин — Илюша и Артём: Пыль и два меча

**Title:** `T08 | Серёгиус — Татуин — Илюша и Артём`  
**Повторять:** C08, C13, C14A/B; обрывок при потере фрагмента в 48.  
**Ориентир:** 100 BPM; 90–120 секунд.  
**Характер:** два джедая с невозмутимым видом дерутся с Канцлером, лениво уворачиваясь от гигантского червя. Быстрый Илюша — флейта и скрипки, тяжёлый Артём — тромбон и виолончели.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic desert-duel theme for two warriors, 100 BPM, swaggering half-time stride. A quick, agile three-note figure on flute and violins is answered by a heavy, stubborn low phrase on trombone and cellos: two very different partners in one confident motif. Plucked cello, dry baritone acoustic guitar, cimbalom, frame drum, low brass, timpani. Sun-baked heat, unshakable cool, dry humor. State the duet motif clearly within the first eight bars, develop it into a confident dueling section, drop to a sparse lazy pocket of plucked notes, then return to a bold full statement. Western-tinged but orchestral, no electric guitar. A brief minor-key fragment of the motif near the end, then a firm cadence. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

### T09 — Набу — Паша и Саша: Рыбаки на задании

**Title:** `T09 | Серёгиус — Набу — Паша и Саша`  
**Повторять:** C08, C16 (до песни Маши), C17, C18A/B; обрывок, когда Серёга уходит с фрагментом в 36.  
**Ориентир:** 88 BPM; 90–120 секунд.  
**Характер:** беззаботные рыбаки у озера, которые вдруг вспоминают «у нас же важная миссия» и ныряют в подводный город. Два друга — валторна и фагот, играющие в терцию.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic lakeside theme for two easygoing friends, 88 BPM, lilting 6/8 barcarolle. Warm French horn and bassoon play a friendly melody in parallel thirds, two voices always together. Rippling harp and soft marimba water figures, pizzicato strings, light clarinet answers, gentle hand percussion. Lazy sunny fishing, good-natured and slightly goofy. Begin relaxed and sunlit, state the duet melody clearly, then a quick heroic lift as the strings and trumpets snap to attention, a shimmering underwater passage with celesta and harp glissandi, then the duet returns with new courage. No tropical pop, no steel drums, no circus style. Room for dialogue; clean ending. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

### T10 — Кашиик — Лёша и Виталик: Байки в кронах

**Title:** `T10 | Серёгиус — Кашиик — Лёша и Виталик`  
**Повторять:** C08, C20, C21; обрывок, когда Канцлер притягивает фрагмент.  
**Ориентир:** 116 BPM; 90–120 секунд.  
**Характер:** байки по лесу, эвок, Чубакка, спор о языке вуки, кальян, мост и дуэль с Канцлером. Перекличка низкой меди и высокого дерева — это их спор.  
**Styles — скопировать целиком:**

```text
Instrumental only. Original symphonic forest-adventure theme for two rowdy companions, 116 BPM. Driving groove of log drums, low toms and woody marimba with a restrained acoustic bass. Low French horns and bass clarinet call out a rugged four-note motif, and bright piccolo and xylophone answer back cheekily: two friends arguing and still moving together. Giant trees, speeding bikes, a laid-back break, a duel on a rope bridge. Open with the groove and the motif, ride an energetic section, settle into a lazy pocket with soft wooden flute, then build with tremolo strings and timpani to a bold return of the motif. Earthy and adventurous, no tribal cliché, no electric guitars. Strong final cadence. Natural acoustic dynamics, clear melodic identity. No vocals, choir, spoken words or sound effects. Entirely original melody; no quotations from existing film or game music.
```

**Как вплетать темы команд.** Мотив команды — 2–4 такта, не постоянный фон. В C08 (погрузка экипажей) три мотива могут пройти друг за другом, по одному на пару. В бою брать боевой кусок записи своей команды **или** T05, но не обе дорожки сразу. Когда Канцлер забирает фрагмент, мотив команды обрывается, и дальше звучит T01 или T03. В финальных титрах (49–51) темы команд не нужны: там одна песня.

### Как связать темы в монтаже

- **T01 → T07:** главная тема становится домашней: для узнаваемой репризы лучше взять тихий участок выбранной T01, а T07 использовать как самостоятельное завершение либо ориентир будущей аранжировки.
- **T03:** один короткий фрагмент повторяется при появлении карты; раскрытие тайны получает более светлый участок той же записи.
- **T06:** один и тот же короткий мотив может возвращаться у стикера с хлебом и молоком, но не обязан звучать при каждом его появлении. Перед вопросом Юли в 55 — полностью убрать музыку и оставить реплику с реакцией.
- **T02/T05:** для кошачьих боёв приоритет у собственной темы котов; T05 — для остальных столкновений. Не накладывать две темы одновременно.
- **T04:** использовать в перелётах с разной плотностью; T01 возвращать в ключевых героических моментах. Не требуется генерировать все Cxx заново после выбора тем.
- Под диалогом выбирать разреженные фразы и снижать громкость музыки. В танцах и песнях сохранять их собственное музыкальное решение. Встроенную музыку ролика сначала оценить отдельно, вторую дорожку поверх автоматически не добавлять.

## После генерации

- Сохрани выбранный аудиофайл и ссылку Suno с кодом Cxx. Прослушай целиком: иногда появляются нежелательные голоса, обрыв или неподходящее развитие.
- Точные входы, остановки, акценты и выходы музыки поставь при монтаже. Особенно важны пауза перед падением крыла и тишина перед финальным вопросом Юли.
- Если в ролике уже смешаны музыка, речь и шумы, не накладывай новую музыку сразу поверх. Сначала реши, что оставить или заменить; уменьшение громкости общего микса приглушит и речь.
- Боевые шумы, двигатели, рёв, удары, компьютерные сигналы и толпа — отдельный звук, поэтому они исключены из музыкальных заданий.

Карта охватывает27 крупных музыкальных эпизодов, из них4 сохраняют существующие песни/танцы. Остальные23 эпизода раскрыты в30 заготовок. Это не покадровый аудит всей текущей сборки: точная длительность, необходимость каждого трека и наличие встроенной музыки ещё проверяются под реальным монтажом.

Основа: [план](soundtrack-plan.md), [карта](soundtrack-cue-sheet.csv). Старый файл [трёх пилотов](soundtrack-pilot-prompts.md) оставлен как история предложения; для полного набора копировать задания отсюда.

Справка по интерфейсу, проверена18.10.2026: [Suno Custom Mode](https://help.suno.com/en/articles/3726721), [Suno Instrumental Generator](https://suno.com/tools/instrumental-generator). Указания о темпе, инструментах и музыкальном развитии в этом файле — авторские задания, а не обещание точной работы сервиса.
