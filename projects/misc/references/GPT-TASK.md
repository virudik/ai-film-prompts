# Общее задание для ChatGPT: нарисовать референсы для проекта «Разное», сцены 1 «Тихий маяк» и 2 «Тихая планета»

Это самодостаточное задание на **59 картинок** (сцена 1 — 26, сцена 2 — 33). Видео не генерируем, только картинки. Рисуешь ты в обычном чате, регистрацию в репозитории делаешь по разделу 5 (или передаёшь файлы Grok Bot). Ничего не одобряй от имени владельца: все картинки `editorial_status: not_approved`.

## 1. О чём две сцены

Оба ролика — **вертикальные 9:16**, около 2 минут, оригинальные мультфильмы в духе 3D-семейного кино, рассказ от первого лица по-русски детским голосом. Все герои, места и сюжеты собственные; реальных людей, чужих персонажей и брендов нет.

- **Сцена 1 «Тихий маяк»** — мальчик Ярик (7 лет, особенности развития), семья и помощники становятся его маяком. 8 подсцен A1–A8 по 15 с (Seedance 2.0) или 4 ролика B1–B4 по 30 с (Wan 3.0 / Seedance 2.5). Герои: Ярик, мама Лена, Соня, Анна Сергеевна, пёс Бублик, Варя. Палитра: янтарь, персик, мята; внутреннее море — бирюзово-фиолетовое; ночь — глубокий синий и тёплый луч маяка.
- **Сцена 2 «Тихая планета»** — мальчик Мирон (5 лет, аутизм): громкий мир, трудные дни, бабушка Нина находит помощь, успехи, школа, тревога, космический финал. Те же две версии (A1–A8 / B1–B4). Герои: Мирон, мама Вера, бабушка Нина, Дарья Андреевна, доктор Марк Львович, парикмахер Лиля, лошадь Туман. Палитра: холодный дождливый синий и золотой закат снаружи; тёплый янтарь дома; чистый мятно-голубой в клинике; глубокий космос в финале.

Подсцены сцены 1: A1 Громко · A2 Двор · A3 Внутреннее море · A4 Ботинки · A5 Маяк · A6 Три картинки · A7 Стёклышко · A8 Побудьте рядом.
Подсцены сцены 2: A1 Тихий космонавт · A2 Слишком громко · A3 Бегство от шума · A4 Перегруз и бессонные ночи · A5 Бабушка находит помощь · A6 Я учусь · A7 Школа и счета · A8 Тихая планета.

## 2. Единые правила стиля и формата (обязательно для каждой картинки)

**STYLE BLOCK — вставляй в конец каждого промта дословно (в промтах ниже он уже есть):**

```text
Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

- Один мир, один художник: те же пропорции, цвета и одежда на всех листах и во всех кадрах. Сцена 2 нарисована в том же стиле, что и сцена 1, но это другие люди и другой мир: не смешивай героев двух сцен.
- Без текста, букв, цифр, логотипов, водяных знаков, рамок. Карточки с пиктограммами, книжки, школьные гирлянды, бумажные счета и пузырьки — без надписей и без читаемых чисел. Названий студий, мультфильмов и торговых марок не используй, чужих мультперсонажей не рисуй.
- Если на картинке есть персонаж, сверяй с листом: лицо, причёска, одежда не меняются. Лист персонажа всегда выше кадра локации.
- **ФОРМАТ (решение владельца 01.11.2026: «вертикаль как в рилсе»):**
  - **ВСЕ локации, листы реквизита и ключевые кадры K1–K8 обеих сцен — ВЕРТИКАЛЬНО 9:16**, PNG, 1024×1792 (или 1080×1920). Если генератор даёт только 1024×1536 (2:3) — перерисуй или перекадрируй до 9:16 без чёрных полос и без вставки горизонтальной картинки в вертикальный холст.
  - **Листы персонажей и листы эмоций (сцена 1: C1–C9; сцена 2: M1, M2, M3, V1, V2, N1, N2, D1, R1, B1, H1) остаются ГОРИЗОНТАЛЬНЫМИ листами-развёртками 3:2, ≥1536×1024, PNG** на нейтральном светло-сером фоне. Так принято во всём репозитории (листы Ярика, Рыжика и других — горизонтальные); они задают только внешность и в видео попадают как референс, а не как кадр.
- **Композиция для вертикали:** главный объект по центру; кадр по высоте слоями (внизу пол/брусчатка/вода, в середине персонаж, вверху потолок/небо/маяк); персонажи друг над другом или друг за другом, а не в ряд по ширине; лица крупные, читаются на телефоне; безопасные поля сверху и снизу под интерфейс; никаких широких панорам и «горизонтального кино» внутри кадра.
- **Самопроверка после каждой картинки:** внешность совпадает с описанием; нет лишних людей, лап, пальцев; нет текста и чисел; формат верный (вертикаль для локаций/реквизита/кадров, горизонтальный лист для персонажей). При браке переделай, не дожидаясь команды.
- Сохраняй рядом с каждым файлом `<имя>.prompt.txt` с точным промтом.
- **Порядок работы:** сначала листы персонажей и эмоций (сцена 1: C1–C9, сцена 2: M1–H1), затем локации и реквизит, затем ключевые кадры. Первыми в каждой сцене — самые важные: сцена 1 — K1, K3, K5, K8; сцена 2 — K2, K4, K5, K8.

## Часть I. Сцена 1 «Тихий маяк» (файлы 1–26)

### I-1. Персонажи сцены 1 (листы — горизонтальные)

Описания для проверки (дословно из канона промтов):

- **Ярик:** YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Same face, hair and proportions in every shot.
- **Мама Лена:** MAMA LENA: 34-year-old woman, tan skin, dark-brown curly hair in a high loose bun with a few strands free, warm dark eyes, soft laugh lines, no glasses; light-blue denim shirt with rolled sleeves over a white tee, dark jeans.
- **Соня:** SONYA: 12-year-old girl, fair skin with rosy cheeks, long straight light-brown hair in a side braid, round blue-grey eyes, lilac windbreaker with a small cluster of enamel pins on the pocket, jeans, white sneakers.
- **Анна Сергеевна:** ANNA SERGEEVNA: woman of about 48, tall, pale-beige skin, short silver-grey bob, warm brown eyes, deep smile lines, no glasses; plum linen tunic, wooden bead necklace, soft flat shoes.
- **Бублик (пёс):** BUBLIK: medium-large fluffy cream-and-apricot mixed-breed dog with floppy ears, dark brown nose, kind dark eyes and a sky-blue bandana.
- **Варя:** VARYA: 6-year-old girl, light skin with freckles, two short dark-brown pigtails with orange hair ties, gap-toothed smile; light-blue dungarees over a striped tee.

Дополнительный вид Ярика (для A5): тёмно-синяя пижама с мелкими жёлтыми звёздами, лицо и причёска те же. Жёлтые детские наушники с тремя синими волновыми наклейками — реквизит, не часть листа.

Порядок: C1 → C2 (по C1) → C3 → C4 → C5 → C6 → C7 → C8 → C9. Для C2/C4/C6 прикрепляй основной лист как image 1.

#### 1. C1 · Ярик — основной лист (4 ракурса)

- **Файл:** `projects/misc/references/yarik.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. YARIK: 7-year-old boy, small for his age, light warm-olive skin, tousled dark-brown wavy hair with a cowlick at the crown, large hazel-brown eyes, light freckles across the nose, slightly prominent ears; brick-red hooded sweatshirt with a small white sailboat patch on the chest, navy trousers, grey velcro sneakers. Expression in the views: calm, gentle, slightly guarded. In the close-up show the cowlick and freckles clearly. Add a small second row of detail insets: the sailboat patch on the sweatshirt and the velcro sneaker. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 2. C2 · Ярик — лист эмоций

- **Файл:** `projects/misc/references/yarik-expressions.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`)
- **Промт:**

```text
Use the attached model sheet of Yarik as the exact identity reference (image 1). Expression sheet on a plain neutral light-grey background: a 3×3 grid of head-and-shoulders portraits of the same character with identical face, hair and clothing as image 1. Expressions: neutral; calm and curious; startled; overwhelmed with eyes shut; crying; guilty; comforted and relieved; shy small smile; joyful. Keep the brick-red hooded sweatshirt visible. This is a quiet sensitive child; expressions are subtle, no exaggeration. Do not change design, age or colours. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 3. C3 · Мама Лена — основной лист

- **Файл:** `projects/misc/references/mama-lena.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. MAMA LENA: 34-year-old woman, tan skin, dark-brown curly hair in a high loose bun with a few strands free, warm dark eyes, soft laugh lines, no glasses; light-blue denim shirt with rolled sleeves over a white tee, dark jeans. Expression in the views: warm, gentle, a little tired. In the close-up show the curls, loose strands and laugh lines. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 4. C4 · Мама Лена — лист эмоций

- **Файл:** `projects/misc/references/mama-lena-expressions.png`
- **Приложить как входы:** image 1 = Мама Лена — основной лист (`projects/misc/references/mama-lena.png`)
- **Промт:**

```text
Use the attached model sheet of Mama Lena as the exact identity reference (image 1). Expression sheet on a plain neutral light-grey background: a 3×3 grid of head-and-shoulders portraits of the same character with identical face, hair and clothing as image 1. Expressions: neutral; calm and curious; startled; overwhelmed with eyes shut; crying; guilty; comforted and relieved; shy small smile; joyful. Include tired-but-loving and moved-to-tears variants within the nine. Do not change design, age or colours. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 5. C5 · Соня — основной лист

- **Файл:** `projects/misc/references/sonya.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. SONYA: 12-year-old girl, fair skin with rosy cheeks, long straight light-brown hair in a side braid, round blue-grey eyes, lilac windbreaker with a small cluster of enamel pins on the pocket, jeans, white sneakers. Expression in the views: shy, kind. In the close-up show the side braid and enamel pins. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 6. C6 · Соня — лист эмоций

- **Файл:** `projects/misc/references/sonya-expressions.png`
- **Приложить как входы:** image 1 = Соня — основной лист (`projects/misc/references/sonya.png`)
- **Промт:**

```text
Use the attached model sheet of Sonya as the exact identity reference (image 1). Expression sheet on a plain neutral light-grey background: a 3×3 grid of head-and-shoulders portraits of the same character with identical face, hair and clothing as image 1. Expressions: neutral; calm and curious; startled; overwhelmed with eyes shut; crying; guilty; comforted and relieved; shy small smile; joyful. Include protective, quietly proud and relieved variants within the nine. Do not change design, age or colours. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 7. C7 · Анна Сергеевна — лист (ракурсы + эмоции)

- **Файл:** `projects/misc/references/anna-sergeevna.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. ANNA SERGEEVNA: woman of about 48, tall, pale-beige skin, short silver-grey bob, warm brown eyes, deep smile lines, no glasses; plum linen tunic, wooden bead necklace, soft flat shoes. Expression in the views: calm, patient, warm. Add a second row of six small head portraits: neutral, waiting patiently, encouraging, moved, proud, laughing softly. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 8. C8 · Бублик — лист (ракурсы + эмоции)

- **Файл:** `projects/misc/references/bublik.png`
- **Промт:**

```text
Animal model sheet on a plain neutral light-grey background: one single dog. Layout: four full-body views in a row with identical scale — front, three-quarter front, side, back — plus a row of six head portraits: calm, curious, happy, sleepy, comforting, alert. BUBLIK: medium-large fluffy cream-and-apricot mixed-breed dog with floppy ears, dark brown nose, kind dark eyes and a sky-blue bandana. Fluffy coat texture readable, same colours in all views. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 9. C9 · Варя — лист (ракурсы + эмоции)

- **Файл:** `projects/misc/references/varya.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. VARYA: 6-year-old girl, light skin with freckles, two short dark-brown pigtails with orange hair ties, gap-toothed smile; light-blue dungarees over a striped tee. Add a second row of six small head portraits: neutral, curious, shy, gap-toothed smile, laughing, thoughtful. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

### I-2. Локации и реквизит сцены 1 (ВЕРТИКАЛЬ 9:16)

#### 10. L1 · Кухня

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-L1-kitchen.png`
- **Промт:**

```text
Interior of a small sunny apartment kitchen in the morning: pale-mint cabinets, wooden table with two chairs, round wall clock, kettle on a gas stove, window with warm morning light, fridge with magnets and children's drawings of boats, a cereal box on the table. Tall view showing the whole room from floor to ceiling, no people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, empty of main characters unless stated, clear layout for use as a location reference.
```

#### 11. L2 · Прихожая

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-L2-hallway.png`
- **Промт:**

```text
Narrow apartment hallway in the morning: wall coat hooks with jackets, a shoe bench and shoe rack, round mirror, a warm ceiling lamp, front door with a small window showing grey morning, wooden floor, a school bag hook. Tall view from floor to ceiling or ground to sky, no people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, empty of main characters unless stated, clear layout for use as a location reference.
```

#### 12. L3 · Комната Ярика ночью

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-L3-yarik-room-night.png`
- **Промт:**

```text
A small child's bedroom at night: single bed with a navy bedspread with small stars, a shelf with a glass jar of sea glass and a small free spot for a lighthouse night-light, window with warm city lights outside, a rug, soft toys, a dark blue palette with warm accents. Tall view from floor to ceiling or ground to sky, no people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, empty of main characters unless stated, clear layout for use as a location reference.
```

#### 13. L4 · Двор с площадкой

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-L4-courtyard.png`
- **Промт:**

```text
A city courtyard playground in autumn: five-storey brick apartment building, a blue slide, swings, a sandbox with a wooden edge, birch trees with yellow leaves, a bench, concrete path, golden afternoon light. Tall view from floor to ceiling or ground to sky, no people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, empty of main characters unless stated, clear layout for use as a location reference.
```

#### 14. L5 · Кабинет занятий

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-L5-therapy-room.png`
- **Промт:**

```text
A bright small therapy room for children: round light-wood table with two small chairs, low shelves with soft toys and baskets, a big rug with a wave pattern in blue and cream, window with sheer curtains and soft daylight, a beanbag, a potted plant. Tall view from floor to ceiling or ground to sky, no people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, empty of main characters unless stated, clear layout for use as a location reference.
```

#### 15. L6 · Внутреннее море — шторм

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-L6-inner-sea-storm.png`
- **Промт:**

```text
Inner world of a child: a dark teal stormy sea under a purple sky, towering waves made of swirling translucent shapes and ribbons like visualised sound, a tiny wooden rowboat with two oars in the middle, a dark unlit striped lighthouse tiny on the far horizon. Tall cinematic view with stacked layers (sky above, towering waves, boat below centre), moody but not frightening, painterly-3D look. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, clear layout for use as a location reference.
```

#### 16. L7 · Внутреннее море — штиль и маяк

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-L7-inner-sea-calm.png`
- **Промт:**

```text
Inner world of a child after the storm: a calm glittering teal and gold sea at dusk, soft pink-violet clouds, the same striped lighthouse now lit with a warm sweeping beam, the same tiny wooden rowboat with two oars floating peacefully in the middle, gentle golden ripples. Tall cinematic view with stacked layers (sky and lit lighthouse above, calm sea, boat below centre), hopeful. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, clear layout for use as a location reference.
```

#### 17. L8 · Берег и маяк на закате

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-L8-seaside-lighthouse.png`
- **Промт:**

```text
A pebble beach at dusk with a wooden promenade and a tall red-and-white striped lighthouse on a headland in the distance, calm teal sea with golden-hour sky, small waves, a wooden pier on the left, warm rim light. Tall view with the beach in the lower half and sea and sky above, no people, lighthouse unlit. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, empty of main characters unless stated, clear layout for use as a location reference.
```

#### 18. P1 · Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-P1-props-sheet.png`
- **Промт:**

```text
Prop sheet in a VERTICAL 9:16 portrait frame (1024×1792) on a plain neutral light-grey background: four rows, one item per row, each item shown from two angles side by side, identical style: (1) children's over-ear noise-cancelling headphones in mustard yellow with three small hand-placed blue wave stickers on the left cup; (2) a clear glass jar and a small beige cloth drawstring bag with about ten smooth sea-glass pieces in green, blue and white nearby (one bright blue piece slightly larger); (3) a small lighthouse night-light, red-and-white striped, glowing warm lamp at the top, shown unlit and lit; (4) three large soft rounded picture cards with simple pictograms and NO text or letters: a figure pointing to itself, a reaching hand, an ear with a small soft cloud. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

### I-3. Ключевые кадры сцены 1 K1–K8 (ВЕРТИКАЛЬ 9:16)

Кадры задают постановку, а не внешность: лица берутся только из листов. Все — вертикаль 9:16 (1024×1792). Первыми рисуй K1, K3, K5, K8 (самые важные).

#### 19. K1 · A1 · стартовый кадр (Кухня)

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-K1-kitchen-sound.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`); image 2 = Мама Лена — основной лист (`projects/misc/references/mama-lena.png`); image 3 = Кухня (`projects/misc/references/scenes/scene-1/MS01-L1-kitchen.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Medium-full vertical shot in the kitchen from image 4. Yarik (image 1) sits at the table with a cereal bowl and a spoon, small warm yellow sparks around the spoon and soft orange rings drifting from the round wall clock toward his ears. Mama Lena (image 2) stands at the stove three-quarters to camera, kettle on the flame. Morning sun. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 20. K2 · A2 · ключевой кадр (Двор)

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-K2-courtyard-retreat.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`); image 2 = Двор с площадкой (`projects/misc/references/scenes/scene-1/MS01-L4-courtyard.png`); image 3 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки (`projects/misc/references/scenes/scene-1/MS01-P1-props-sheet.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Courtyard from image 2. Yarik (image 1) stands at the edge of the playground, shoulders raised, one hand on his ear, holding the small beige cloth bag from image 3; blurred generic children run and shout behind him; faint translucent blue ripples of sound reach toward him. Autumn light. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 21. K3 · A3 · стартовый кадр (Внутреннее море)

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-K3-inner-sea-boat.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`); image 2 = Внутреннее море — шторм (`projects/misc/references/scenes/scene-1/MS01-L6-inner-sea-storm.png`); image 3 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки (`projects/misc/references/scenes/scene-1/MS01-P1-props-sheet.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Inner sea storm from image 2. Yarik (image 1, brick-red hoodie) alone in a small wooden rowboat gripping two oars on a high wave; a few tiny glowing paper boats made of pale light drift away from him in the wind; the dark unlit striped lighthouse from image 3 is tiny on the horizon. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 22. K4 · A4 · стартовый кадр (Прихожая)

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-K4-hallway-boots.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`); image 2 = Мама Лена — основной лист (`projects/misc/references/mama-lena.png`); image 3 = Соня — основной лист (`projects/misc/references/sonya.png`); image 4 = Прихожая (`projects/misc/references/scenes/scene-1/MS01-L2-hallway.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Hallway from image 4. Mama Lena (image 2) crouches holding one stiff new brown leather boot, coat half on, glancing at her watch; Yarik (image 1) sits on the shoe bench pulling his foot away with a grimace; Sonya (image 3) waits at the door with her school bag. Short orange-red spiky sound shapes flicker near his foot. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 23. K5 · A5 · ключевой кадр (Комната ночью)

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-K5-night-lighthouse.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`); image 2 = Соня — основной лист (`projects/misc/references/sonya.png`); image 3 = Бублик — лист (ракурсы + эмоции) (`projects/misc/references/bublik.png`); image 4 = Комната Ярика ночью (`projects/misc/references/scenes/scene-1/MS01-L3-yarik-room-night.png`); image 5 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки (`projects/misc/references/scenes/scene-1/MS01-P1-props-sheet.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Bedroom at night from image 4. Yarik (image 1 face and hair, now in navy pyjamas with small yellow stars) sits up in bed with the yellow headphones from image 5 on his head; Sonya (image 2) sits on the bed edge; Bublik (image 3) lies across his feet; the lighthouse night-light from image 5 glows on the shelf and a soft warm beam sweeps across the wall. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 24. K6 · A6 · ключевой кадр (Кабинет занятий)

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-K6-three-cards.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`); image 2 = Анна Сергеевна — лист (ракурсы + эмоции) (`projects/misc/references/anna-sergeevna.png`); image 3 = Кабинет занятий (`projects/misc/references/scenes/scene-1/MS01-L5-therapy-room.png`); image 4 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки (`projects/misc/references/scenes/scene-1/MS01-P1-props-sheet.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Therapy room from image 3. Anna Sergeevna (image 2) and Yarik (image 1, yellow headphones around his neck) at the round table; three large picture cards with pictograms only (a figure pointing to itself, a reaching hand, an ear with a soft cloud, as on the prop sheet image 4) lie in a row; Anna smiles softly with a hand over her heart; Yarik has a tiny shy smile. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 25. K7 · A7 · ключевой кадр (Двор)

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-K7-gift-glass.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`); image 2 = Бублик — лист (ракурсы + эмоции) (`projects/misc/references/bublik.png`); image 3 = Варя — лист (ракурсы + эмоции) (`projects/misc/references/varya.png`); image 4 = Двор с площадкой (`projects/misc/references/scenes/scene-1/MS01-L4-courtyard.png`); image 5 = Лист реквизита: наушники, банка со стёклышками, маяк-ночник, карточки (`projects/misc/references/scenes/scene-1/MS01-P1-props-sheet.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Courtyard from image 4. Yarik (image 1, yellow headphones on) sits at the sandbox edge and places a bright blue sea-glass piece (image 5) in the palm of Varya (image 3), who has put a small spiral shell next to his line of glass; Bublik (image 2) lies beside them; background children are blurred. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 26. K8 · A8 · ключевой кадр (Берег)

- **Файл:** `projects/misc/references/scenes/scene-1/MS01-K8-beach-hug.png`
- **Приложить как входы:** image 1 = Ярик — основной лист (4 ракурса) (`projects/misc/references/yarik.png`); image 2 = Мама Лена — основной лист (`projects/misc/references/mama-lena.png`); image 3 = Соня — основной лист (`projects/misc/references/sonya.png`); image 4 = Бублик — лист (ракурсы + эмоции) (`projects/misc/references/bublik.png`); image 5 = Берег и маяк на закате (`projects/misc/references/scenes/scene-1/MS01-L8-seaside-lighthouse.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Pebble beach at dusk from image 5. Mama Lena (image 2), Sonya (image 3) and Bublik (image 4) hug Yarik (image 1, headphones in his hand) in a group hug; the red-and-white lighthouse beam is lit and sweeps over them and the calm golden-teal sea. Tall emotional composition, group in the lower half, lighthouse and sky above. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

**Итого: 18 основных картинок (9 листов персонажей, 8 локаций, 1 лист реквизита) + 8 ключевых кадров = 26 файлов.**

## Часть II. Сцена 2 «Тихая планета» (файлы 27–59)

### II-1. Персонажи сцены 2 (листы — горизонтальные)

Описания для проверки (дословно из канона промтов):

- **Мирон:** MIRON: 5-year-old boy, small and slight, fair skin with rosy cheeks, soft curly honey-blond hair falling over his forehead, large round green eyes with long lashes, a small gap between the front teeth; mustard-yellow zip hoodie with a small white rocket patch on the chest, forest-green trousers, orange sneakers. Same face, hair and proportions in every shot.
- **Мама Вера:** MAMA VERA: 35-year-old woman, light-olive skin, auburn shoulder-length bob with side-swept fringe, round tortoiseshell glasses, hazel eyes, a small beauty mark on the left cheek; terracotta knit cardigan with big patch pockets over a cream blouse, dark-blue jeans, thin gold hoop earrings.
- **Бабушка Нина:** GRANDMA NINA: 62-year-old woman, tall and upright, warm tan skin, short silver-white curly hair, strong expressive eyebrows, no glasses, large silver hoop earrings; plum-purple track jacket with white side stripes, grey joggers, white sneakers, a sports whistle on a lanyard (a retired swimming coach).
- **Дарья Андреевна:** DARYA ANDREEVNA (the specialist): 30-year-old woman, deep-brown skin, long black braid over one shoulder, warm dark eyes, kind steady smile; sage-green linen shirt, cream trousers, soft flat shoes.
- **Доктор Марк Львович:** DOCTOR MARK LVOVICH: 52-year-old man, bald with grey hair at the sides, trimmed grey beard, round blue-framed glasses, calm gentle expression; white coat over a checked shirt, stethoscope around the neck.
- **Парикмахер Лиля:** LILYA THE BARBER: 28-year-old woman, pale freckled skin, short pink-dyed pixie cut, red barber apron over a black t-shirt, small silver scissors in her hand.
- **Лошадь Туман:** TUMAN: gentle grey dappled horse with a white mane and tail, kind dark eyes, a brown saddle blanket and a small navy children's riding helmet on the boy (never on the horse).
- **Мирон в скафандре (доп. лист):** MIRON IN HIS SPACE SUIT (opening and finale only): the same boy in a mint-and-cream quilted space suit with copper rings at the neck and wrists and a small white rocket patch on the chest, orange boots, and a clear round glass dome helmet with a thin copper rim; when he wears the dome with ordinary clothes it is the same dome.

Порядок: M1 → M2 (по M1) → M3 (по M1) → V1 → V2 → N1 → N2 → D1 → R1 → B1 → H1. Для M2/V2/N2 прикрепляй основной лист как image 1.

#### 27. S2-M1 · Мирон — основной лист (4 ракурса)

- **Файл:** `projects/misc/references/miron.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. MIRON: 5-year-old boy, small and slight, fair skin with rosy cheeks, soft curly honey-blond hair falling over his forehead, large round green eyes with long lashes, a small gap between the front teeth; mustard-yellow zip hoodie with a small white rocket patch on the chest, forest-green trousers, orange sneakers. Expression in the views: gentle, a little guarded, big curious eyes. In the close-up show the curls, long lashes and the small gap in the teeth. Add a small second row of detail insets: the white rocket patch and the orange sneaker. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 28. S2-M2 · Мирон — лист эмоций

- **Файл:** `projects/misc/references/miron-expressions.png`
- **Приложить как входы:** image 1 = Мирон — основной лист (4 ракурса) (`projects/misc/references/miron.png`)
- **Промт:**

```text
Use the attached model sheet of Miron as the exact identity reference (image 1). Expression sheet on a plain neutral light-grey background: a 3×3 grid of head-and-shoulders portraits of the same character with identical face, hair and clothing as image 1. Expressions: neutral; calm and curious; startled; overwhelmed with eyes shut; crying; guilty; comforted and relieved; shy small smile; joyful. Keep the mustard hoodie visible. This is a quiet sensitive 5-year-old; expressions are subtle, no exaggeration; include one with a single tear. Do not change design, age or colours. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 29. S2-M3 · Мирон в скафандре — лист (4 ракурса)

- **Файл:** `projects/misc/references/miron-spacesuit.png`
- **Приложить как входы:** image 1 = Мирон — основной лист (4 ракурса) (`projects/misc/references/miron.png`)
- **Промт:**

```text
Use the attached model sheet of Miron as the exact identity reference (image 1): same face, hair and proportions. Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right showing the clear glass dome. MIRON IN HIS SPACE SUIT (opening and finale only): the same boy in a mint-and-cream quilted space suit with copper rings at the neck and wrists and a small white rocket patch on the chest, orange boots, and a clear round glass dome helmet with a thin copper rim; when he wears the dome with ordinary clothes it is the same dome. Even flat lighting, consistent proportions and colours across all views, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 30. S2-V1 · Мама Вера — основной лист

- **Файл:** `projects/misc/references/vera.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. MAMA VERA: 35-year-old woman, light-olive skin, auburn shoulder-length bob with side-swept fringe, round tortoiseshell glasses, hazel eyes, a small beauty mark on the left cheek; terracotta knit cardigan with big patch pockets over a cream blouse, dark-blue jeans, thin gold hoop earrings. Expression in the views: warm, attentive, a little tired. In the close-up show the glasses, the beauty mark and the bob with side fringe. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 31. S2-V2 · Мама Вера — лист эмоций

- **Файл:** `projects/misc/references/vera-expressions.png`
- **Приложить как входы:** image 1 = Мама Вера — основной лист (`projects/misc/references/vera.png`)
- **Промт:**

```text
Use the attached model sheet of Mama Vera as the exact identity reference (image 1). Expression sheet on a plain neutral light-grey background: a 3×3 grid of head-and-shoulders portraits of the same character with identical face, hair and clothing as image 1. Expressions: neutral; calm and curious; startled; overwhelmed with eyes shut; crying; guilty; comforted and relieved; shy small smile; joyful. Include tired-but-loving, quietly sobbing, relieved and proud-through-tears variants within the nine. Do not change design, age or colours. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 32. S2-N1 · Бабушка Нина — основной лист

- **Файл:** `projects/misc/references/nina.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. GRANDMA NINA: 62-year-old woman, tall and upright, warm tan skin, short silver-white curly hair, strong expressive eyebrows, no glasses, large silver hoop earrings; plum-purple track jacket with white side stripes, grey joggers, white sneakers, a sports whistle on a lanyard (a retired swimming coach). Expression in the views: confident, energetic. In the close-up show the silver curls, earrings and the whistle. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 33. S2-N2 · Бабушка Нина — лист эмоций

- **Файл:** `projects/misc/references/nina-expressions.png`
- **Приложить как входы:** image 1 = Бабушка Нина — основной лист (`projects/misc/references/nina.png`)
- **Промт:**

```text
Use the attached model sheet of Grandma Nina as the exact identity reference (image 1). Expression sheet on a plain neutral light-grey background: a 3×3 grid of head-and-shoulders portraits of the same character with identical face, hair and clothing as image 1. Expressions: neutral; calm and curious; startled; overwhelmed with eyes shut; crying; guilty; comforted and relieved; shy small smile; joyful. Include determined, tender, joyful and worried variants within the nine. Do not change design, age or colours. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 34. S2-D1 · Дарья Андреевна (специалист) — лист

- **Файл:** `projects/misc/references/darya.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. DARYA ANDREEVNA (the specialist): 30-year-old woman, deep-brown skin, long black braid over one shoulder, warm dark eyes, kind steady smile; sage-green linen shirt, cream trousers, soft flat shoes. Expression in the views: patient, warm. Add a second row of six small head portraits: neutral, encouraging, laughing softly, thoughtful, proud, calm. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 35. S2-R1 · Доктор Марк Львович — лист

- **Файл:** `projects/misc/references/mark.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. DOCTOR MARK LVOVICH: 52-year-old man, bald with grey hair at the sides, trimmed grey beard, round blue-framed glasses, calm gentle expression; white coat over a checked shirt, stethoscope around the neck. Expression in the views: calm, kind. Add a second row of six small head portraits: neutral, listening, smiling kindly, serious, reassuring, thoughtful. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 36. S2-B1 · Парикмахер Лиля — лист

- **Файл:** `projects/misc/references/lilya.png`
- **Промт:**

```text
Character model sheet on a plain neutral light-grey background, one single character only. Layout: four full-body views in a row with identical scale and neutral relaxed pose — front, three-quarter front, side profile, back — plus one large head-and-shoulders close-up on the right. LILYA THE BARBER: 28-year-old woman, pale freckled skin, short pink-dyed pixie cut, red barber apron over a black t-shirt, small silver scissors in her hand. Expression in the views: friendly, careful. Add a second row of six small head portraits: neutral, concentrating, smiling, surprised, sympathetic, laughing. Even flat lighting, consistent proportions and colours across all views, no props other than listed, no extra people. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 37. S2-H1 · Лошадь Туман — лист (ракурсы)

- **Файл:** `projects/misc/references/tuman.png`
- **Промт:**

```text
Animal model sheet on a plain neutral light-grey background: one single horse. Layout: four full-body views in a row with identical scale — front, three-quarter front, side, back — plus a row of six head portraits: calm, curious, gentle, sleepy, alert, friendly. TUMAN: gentle grey dappled horse with a white mane and tail, kind dark eyes, a brown saddle blanket; no rider, no helmet on the horse. Coat texture readable, same colours in all views. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

### II-2. Локации и реквизит сцены 2 (ВЕРТИКАЛЬ 9:16)

#### 38. S2-L1 · Гостиная вечером

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L1-living-room.png`
- **Промт:**

```text
Interior of a cosy family living room in the evening: a soft beige sofa with cushions, a thick rug, a wall TV showing a colourful cartoon of a round orange balloon character with a smiling face and a small basket, a floor lamp with warm light, shelves with picture books, a low table with a mug; sense of safety and warmth. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 39. S2-L2 · Городская площадь на закате

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L2-city-square.png`
- **Промт:**

```text
A city square after rain at golden sunset: old-town buildings with ornate facades, wet reflective cobblestones, a few blurred cars with headlights approaching, warm sun low over the roofs, blurred pedestrians far away, wet lamp posts. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 40. S2-L3 · Супермаркет — проход между полками

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L3-supermarket.png`
- **Промт:**

```text
A bright supermarket aisle seen at child eye level: tall shelves full of plain colourful boxes and packages with abstract shapes and no brand names or text, shiny floor, white fluorescent ceiling lights, a distant shopper blurred. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 41. S2-L4 · Двор детского сада

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L4-kindergarten-yard.png`
- **Промт:**

```text
A green kindergarten yard in early autumn: a low fence, flower beds, a small climbing frame, a sandbox, young trees with a few yellow leaves, soft overcast light, blurred children and a teacher very far away. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 42. S2-L5 · Парикмахерская

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L5-barbershop.png`
- **Промт:**

```text
A small bright barbershop: a barber chair with a dark cape on a hook, a large mirror, a counter with combs and scissors in a jar, a small screen, light wooden floor, plants. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 43. S2-L6 · Комната Мирона ночью

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L6-miron-bedroom-night.png`
- **Промт:**

```text
A small child's bedroom at night: a single bed with a quilted blanket, a window with a crescent moon and city lights, a bedside table in the foreground with amber glass medicine bottles and a plain pill organiser (no labels, no text), a warm small lamp, a dark blue palette with warm accents. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 44. S2-L7 · Коридор клиники и стойка регистрации

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L7-clinic-corridor.png`
- **Промт:**

```text
A bright pale-blue clinic corridor with a long perspective: a reception desk with a keyboard, a clipboard and a rubber stamp, closed doors, a bench, ceiling lights, a tiny blurred figure at the far end; no readable signs or text. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 45. S2-L8 · Кабинет центра развития

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L8-development-center.png`
- **Промт:**

```text
A warm child development centre room: a small light-wood table with two small chairs, shelves with soft toys and baskets, a big window with soft sunlight and sheer curtains, a rug, a houseplant. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 46. S2-L9 · Кабинет доктора

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L9-doctor-office.png`
- **Промт:**

```text
A doctor's office: a tidy desk with a folder and a lamp, a glass cabinet with binders, a window with a calm view of trees, a chair for the patient, soft daylight. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 47. S2-L10 · Школа в день линейки

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L10-school-entrance.png`
- **Промт:**

```text
A school entrance on the first day of school in golden sun: a historic building with a small dome, bunting and bunches of balloons without any text, a broad path with fallen leaves, blurred families in the background. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 48. S2-L11 · Кухня ночью

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L11-night-kitchen.png`
- **Промт:**

```text
A small kitchen at night: a wooden table under a hanging amber lamp, a window with dark blue night outside, cups and a notebook on the table, the rest of the room in soft shadow. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 49. S2-L12 · Луг у конюшни

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L12-stable-meadow.png`
- **Промт:**

```text
A golden meadow at the end of the day beside a stable: a wooden fence, big oaks, long rim light, a sandy path, a hint of a stable door at the edge. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 50. S2-L13 · Космос и Земля

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-L13-space-earth.png`
- **Промт:**

```text
Deep space with the Earth glowing blue at the lower side, soft white atmosphere edge, small white stars, empty of people, calm and hopeful; no flags, no text. Vertical 9:16 portrait frame (1024×1792), tall composition with clear foreground, middle ground and background layers, no people unless stated, clear layout for use as a location reference. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 51. S2-P1 · Лист реквизита: стеклянный купол, карточки, книжка, пластилин, счета

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-P1-props-sheet.png`
- **Промт:**

```text
Prop sheet in a VERTICAL 9:16 portrait frame (1024×1792) on a plain neutral light-grey background: five rows, one item per row, each shown from two angles side by side, identical style: (1) a clear round glass dome helmet with a thin copper rim, empty, shown from the front and in three-quarter; (2) three large soft rounded picture cards with simple pictures and NO text: an elephant, a red apple, a round orange balloon character with a smiling face; (3) a colourful children's picture book about the orange balloon, closed and open (pictures only, no letters); (4) lumps of red and green plasticine with two small tools on a small board; (5) paper receipts, a small desktop calculator and a few coins with NO readable numbers or currency symbols. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

### II-3. Ключевые кадры сцены 2 K1–K8 (ВЕРТИКАЛЬ 9:16)

Кадры задают постановку, а не внешность: лица берутся только из листов. Первыми рисуй K2, K4, K5, K8.

#### 52. S2-K1 · A1 · стартовый кадр (скафандр на улице)

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-K1-suit-street.png`
- **Приложить как входы:** image 1 = Мирон в скафандре — лист (4 ракурса) (`projects/misc/references/miron-spacesuit.png`); image 2 = Городская площадь на закате (`projects/misc/references/scenes/scene-2/MS02-L2-city-square.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Full-body shot of Miron (image 1) in the mint space suit and clear glass dome helmet, standing alone and small on the wet evening square from image 2; blurred lamps and passers-by behind; a single teardrop slides down the glass; cool dusk with warm bokeh. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 53. S2-K2 · A2 · ключевой кадр (дом, пузырь тишины)

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-K2-home-bubble.png`
- **Приложить как входы:** image 1 = Мирон — основной лист (4 ракурса) (`projects/misc/references/miron.png`); image 2 = Мама Вера — основной лист (`projects/misc/references/vera.png`); image 3 = Гостиная вечером (`projects/misc/references/scenes/scene-2/MS02-L1-living-room.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Cosy living room from image 3: Miron (image 1) in his mustard hoodie leans against mama Vera (image 2) on the rug; they face the TV with the orange balloon cartoon; a soft translucent glowing bubble surrounds them; mama's hand on his shoulder. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 54. S2-K3 · A3 · ключевой кадр (магазин, испуг)

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-K3-store-fear.png`
- **Приложить как входы:** image 1 = Мирон — основной лист (4 ракурса) (`projects/misc/references/miron.png`); image 2 = Мама Вера — основной лист (`projects/misc/references/vera.png`); image 3 = Супермаркет — проход между полками (`projects/misc/references/scenes/scene-2/MS02-L3-supermarket.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Supermarket aisle from image 3 at child height: tight close-up of Miron (image 1) with wide frightened eyes and open mouth, plain boxes tumbling past his face; mama Vera (image 2) blurred in the background turning with shock. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 55. S2-K4 · A4 · ключевой кадр (бабушка обнимает маму)

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-K4-grandma-hug.png`
- **Приложить как входы:** image 1 = Бабушка Нина — основной лист (`projects/misc/references/nina.png`); image 2 = Мама Вера — основной лист (`projects/misc/references/vera.png`); image 3 = Мирон — основной лист (4 ракурса) (`projects/misc/references/miron.png`); image 4 = Комната Мирона ночью (`projects/misc/references/scenes/scene-2/MS02-L6-miron-bedroom-night.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Night bedroom from image 4: Grandma Nina (image 1) in her purple track jacket hugs her daughter Vera (image 2) firmly; Vera leans into her; Miron (image 3) sleeps in the bed behind them; a bar of warm corridor light widens over the floor; medicine bottles blurred in the lower foreground. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 56. S2-K5 · A5 · ключевой кадр (карточка с шариком)

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-K5-dome-cards.png`
- **Приложить как входы:** image 1 = Мирон — основной лист (4 ракурса) (`projects/misc/references/miron.png`); image 2 = Дарья Андреевна (специалист) — лист (`projects/misc/references/darya.png`); image 3 = Кабинет центра развития (`projects/misc/references/scenes/scene-2/MS02-L8-development-center.png`); image 4 = Лист реквизита: стеклянный купол, карточки, книжка, пластилин, счета (`projects/misc/references/scenes/scene-2/MS02-P1-props-sheet.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Development-centre room from image 3: Miron (image 1) in his mustard hoodie wearing the clear glass dome from image 4 at a small table, pointing to the orange balloon card; Darya (image 2) sits low opposite him smiling; sunny window light. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 57. S2-K6 · A6 · ключевой кадр (чтение с мамой)

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-K6-reading.png`
- **Приложить как входы:** image 1 = Мирон — основной лист (4 ракурса) (`projects/misc/references/miron.png`); image 2 = Мама Вера — основной лист (`projects/misc/references/vera.png`); image 3 = Гостиная вечером (`projects/misc/references/scenes/scene-2/MS02-L1-living-room.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Living-room sofa from image 3: mama Vera (image 2) in glasses reads a picture book, Miron (image 1) on her lap follows the pictures with his finger and smiles with the little gap in his teeth; warm lamp light; close and intimate. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 58. S2-K7 · A7 · ключевой кадр (первый день в школе)

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-K7-school-day.png`
- **Приложить как входы:** image 1 = Мирон — основной лист (4 ракурса) (`projects/misc/references/miron.png`); image 2 = Мама Вера — основной лист (`projects/misc/references/vera.png`); image 3 = Бабушка Нина — основной лист (`projects/misc/references/nina.png`); image 4 = Школа в день линейки (`projects/misc/references/scenes/scene-2/MS02-L10-school-entrance.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. School entrance from image 4 in golden sun: Miron (image 1) in a brown jacket with a small backpack walks between mama Vera (image 2) and Grandma Nina (image 3), holding both hands, and looks up beaming; balloons and bunting above. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

#### 59. S2-K8 · A8 · ключевой кадр (космос)

- **Файл:** `projects/misc/references/scenes/scene-2/MS02-K8-space.png`
- **Приложить как входы:** image 1 = Мирон в скафандре — лист (4 ракурса) (`projects/misc/references/miron-spacesuit.png`); image 2 = Космос и Земля (`projects/misc/references/scenes/scene-2/MS02-L13-space-earth.png`)
- **Промт:**

```text
Use the attached images as exact references: character sheets control faces, hair, ages and clothing; location and prop images control only their elements. Deep space from image 2: Miron (image 1) in the mint space suit floats calmly with a thin copper tether trailing, a gentle half-smile, the glowing Earth in the lower half of the tall frame, stars around; small and brave. Vertical 9:16 portrait composition (1024×1792), main subject centred, subjects stacked high-to-low, readable large faces, no text. Style: high-end 3D animated family-feature look, stylized but physically grounded, soft rounded forms, large expressive eyes, subtle subsurface skin scattering, detailed hair and fabric, warm natural palette, soft studio lighting. No text, no logos, no watermark, no borders.
```

## 5. Как зарегистрировать в репозитории `virudik/ai-film-prompts` (проект `misc`, обе сцены)

Обе сцены уже лежат в `projects/misc/video-prompts.md` (DRAFT), персонажи и локации описаны в `projects/misc/character-references.json` без картинок (`planned_reference_images`). Работа только внутри `projects/misc/`. Если ты не можешь писать в репозиторий — отдай файлы Grok Bot, он выполнит эти шаги.

1. `git pull`; взять замок проекта: `python3 scripts/canon_lock.py . acquire --project misc --holder chatgpt:ordinary:<UUID4> --task "Разное: референсы сцен 1 и 2" --minutes 45 --push` (или `work`; чужой действующий замок не перехватывать — подождать/сообщить).
2. Положить файлы по путям выше: листы персонажей — `projects/misc/references/*.png`; сцена 1 — `projects/misc/references/scenes/scene-1/MS01-*.png`; сцена 2 — `projects/misc/references/scenes/scene-2/MS02-*.png`; рядом `*.prompt.txt`.
3. Для каждого файла посчитать SHA256 и размеры; проверить формат (вертикаль 9:16 для локаций, реквизита, кадров; горизонталь 3:2 для листов персонажей).
4. По `manifest.json` на сцену: `projects/misc/references/scenes/scene-1/manifest.json` и `…/scene-2/manifest.json` (по образцу `projects/kotmonavty/references/scenes/scene-4/manifest.json`): `{schema_version:1, project:"misc", scene:N, title, updated_at, status:"references_ready", editorial_status:"not_approved", references:[{tag, role, path, sha256}]}`.
5. `projects/misc/character-references.json`: у каждого героя (сцена 1: yarik, mama-lena, sonya, anna-sergeevna, bublik, varya; сцена 2: miron, vera, nina, darya, mark, lilya, tuman) заполнить `model_sheet.public_image` и `full_image` реальным путём основного листа, `model_sheet.additional` — подписью листа эмоций/доп. листа (у Мирона — лист эмоций и лист скафандра), в `reference_images` добавить `{path, caption, editorial_status:"not_approved", derived_from:[основной лист]}`; в `provenance.status` поставить `generated`, убрать `planned_reference_images`. Для `assets[]` (локации, реквизит обеих сцен) заполнить `images:[{path, caption, sha256, scenes:[N]}]` вместо `planned_reference_images`. Ничего не писать как `approved`.
6. Создать/дополнить `projects/misc/references/usage-index.json` по образцу `projects/kotmonavty/references/usage-index.json`: `{schema_version:1, project:"misc", updated_at, generated_image_count, generated_orphans:[], images:[{path, scenes:[N], roles:[…], sha256, editorial_status:"not_approved"}]}`.
7. В `projects/misc/video-prompts.md`, сцены 1 и 2: в каждой подсцене заменить список «Планируемые референсы» на галерею `<div class="scene-ref-gallery"><figure><a href="путь">…</figure></div>` и строку `Входы:` с реальными путями (по образцу Сцены 4 Котмонавтов); в «Готовность» убрать «картинок ещё нет». `production_state` остаётся `DRAFT`, `READY` не ставить. Формат 9:16 не менять.
8. `python3 scripts/projects.py . status --project misc --write` (health=ok), `python3 scripts/projects.py . validate`, `python3 -m unittest discover -s tests`; проверить `references.html?p=misc` и `index.html?p=misc`. Один коммит, замок освободить последним коммитом (`canon_lock.py . release …`), push в `main` только с разрешения владельца.
9. Очередь Topview (`projects/misc/ops/topview-launch-queue.json`) не трогать, видео не запускать. Запуск в Topview — только в формате 9:16 и только по отдельной команде владельца.

## Контрольный список (всего 59)
- Сцена 1: C1–C9 (9 листов) + L1–L8 (8 локаций) + P1 + K1–K8 = 26.
- Сцена 2: листы M1, M2, M3, V1, V2, N1, N2, D1, R1, B1, H1 (11) + локации S2-L1…S2-L13 (13) + S2-P1 + K1–K8 (8) = 33.
