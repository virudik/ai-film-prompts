# Аудит всех промтов master по PROMPT-STYLE-GUIDE — октябрь 2026

> Отчёт Claude Code, облачная сессия 11.10.2026. **Не канон.** `video-prompts.md` не менялся; все «предложенные diff» ниже — текст для решения владельца/писателя канона, **не применены**. Технический success Topview ≠ approval; ничего в Topview не запускалось.
> Основа: `main` на 11.10.2026 (`35882ee`), master SHA-256 `2a018157…`, 18 сцен / 51 промт, `PROMPT-STYLE-GUIDE.md` (полностью), `character-references.json`, `review-ledger.json`, `topview-task-map.json`, манифесты `references/scenes/*`, `shadow/topview-robot-status.json`. Прочитан весь master; 11 однотипных частей Scene 20 сверены построчным диффом относительно части 1; 20 блоков Scene 28 — диффом A↔B и по секциям. Автопроверка структуры: `reports/tools/prompt_lint.py` (read-only; её вывод — зацепки, не вердикт).

## 0. Как читать оценки

| Оценка | Смысл |
|---|---|
| **A** | Копируется и запускается как есть; замечания косметические. |
| **B** | Запускаемо; есть правки, которые снизят риск брака, но не обязательны. |
| **C** | Перед (пере)запуском нужны правки или входы, иначе высокий риск впустую занять слот. |
| **D** | Запуск невозможен: нет обязательных входов. |

Критерии (§5, §6, §8, §11, §16A гайда): автономность (identity lock, роли и приоритет референсов, камера/пространство, таймлайн, native audio, негативы, FRAME FILL), соответствие длительности/модели, ссылки на реальные файлы, continuity с соседними сценами (граничные кадры), повторы и противоречия.

**Что подтверждено проверкой по всем 51 блокам:** все `references/…` файлы, на которые ссылается master (41 путь), реально лежат в репозитории; длительность в строке `Mode:` совпадает с таймлайном везде (дыр и нахлёстов по секундам нет); русская речь есть только в Scene 13 и 26 — обе на Wan 3 (правило движка соблюдено); во всех блоках есть негатив; в блоках с `Native audio: on` есть AUDIO.

**Что не проверялось:** сами видео (просмотр не выполнялся), реальный текст, ушедший в Topview (см. `topview-unknown-mapping-2026-10-11.md`), аудио.

## 1. Сводная таблица

Состояние — из `review-ledger.json` (человеческие решения) и master; «рендер» — последняя известная Topview-задача.

| Сцена | Блоков | Движок: meta / промт / факт | Состояние | Оценка | Главные находки |
|---|---:|---|---|:--:|---|
| **13** Совет, кот Лучик | 1 | Wan 3 / Wan 3 / Wan 3.0 | `NEEDS_RERENDER`, `needs_redo` | **B+** | Нет END STATE; `@image3` пропущен в нумерации, дополнительные @image6/7 стоят выше основных. Речевая логика (speaker ownership) — образец. |
| **16** Татуин, червь | 1 | Seedance 2.5 / (нет) / Wan 3.0 | принято, «в монтаж» | **B** | `target_engine` ≠ реальному запуску; `@Video1` — файл только на Drive (в репозитории нет); у Канцлера не указан меч. Править нечего: сцена принята. |
| **20** Маша, песня 1–11 | 11 | Seedance 2.5 / (нет строки) / Wan 3.0 (3 части) | принято (20 в целом) | **B−** | В части 11 «cut naturally into MASHA SONG PART 11» (копипаст-ошибка); ≈12,5 тыс. знаков на часть с дословным повтором BIBLE и 4-кратным повтором identity-правил; нет START/END STATE. |
| **20** вставки 12, 13 | 2 | Seedance 2.5 | то же | **C** | Не автономны (`Parts 1–11`, `Part13`, пути `references/full/…` внутри промта); 6 смен плана за 30 с; у Паши «clean-shaven», а на sheet — лёгкая щетина; у 13 два блока NEGATIVE. |
| **21** Мостик→космос | 1 | Seedance 2.5 / Seedance 2.5 / Wan 3.0 | `needs_redo` (причина не записана); **запущен повтор** | **B+** | Запрет бликов на стекле повторён 5×; причина redo неизвестна — править содержательно нечего. |
| **24** Кабина: взлёт | 1 | Seedance 2.5 / то же / Wan 3.0 | `needs_redo`; **запущен повтор** | **B** | «canopy» (4×) противоречит «не bubble canopy»; нет END STATE; причина redo неизвестна. |
| **25** Кабина: бой | 1 | Seedance 2.5 / то же | **первый запуск** (ранее не рендерилась) | **B** | Нет END STATE; стык 25→26 (космос → стоят на планете) не определён; «canopy». |
| **26** Ультиматум | 1 | Wan 3 / Wan 3 / Wan 3.0 | принято, «в монтаж» | **B+** | Мат в реплике Рыжика (2 слова) — осознанное решение?; масштаб «по колено человека» без человека в кадре; сторона off-camera Серёги не задана → стык в 27. |
| **27** Бой котов | 3 | Seedance 2.5 / 2.5 + 2.0 / Wan 3.0 (30 с) | `needs_redo`; **запущен повтор 30 с** | **B−** | У 30 с нет START STATE и нет текстового lock Серёги (в 15 с-частях есть); во всех трёх «older black-basalt wording», которого модель не видела; части 15 с — 9 851 / 9 751 из 10 000 знаков. |
| **28** Танец (A1–A10) | 10 | Seedance 2.0 | `READY`, не запускалась | **B+** | Редакторские/операторские фразы внутри блоков (A8, A9, A10); A3 требует C28, которого нет. |
| **28** Танец (B1–B10) | 10 | Wan 3.0 | то же | **B+** | То же (B8, B9, B10); 30 с на простой мотив — риск вялости (описан в master). |
| **30** Колоннада | 1 | Wan 3 / Wan 3.0 | `needs_redo`; (возможно) запущен повтор | **B−** | Нет FRAME FILL-блока; «STARTING HISTORY: Optional next battle after Scene27» — не START STATE; `EDITING NOTE` внутри промта. |
| **31** Лестница | 1 | то же | то же | **B−** | То же. |
| **32** Арка | 1 | то же | то же | **B−** | То же. |
| **33** Руины | 1 | Wan 3 / Wan 3.0 | принято, «в монтаж» | **B** | Нет стандартного FRAME FILL (`FULL FRAME 16:9.`); место в хронологии не определено (в самом промте). |
| **34** Вход в храм | 1 | то же | принято, «в монтаж» | **B** | Нет стандартного FRAME FILL (`16:9 edge-to-edge.`). |
| **35** Находка ПК | 1 | Wan 3 / Wan 3.0 | `DRAFT` | **D** | Нужен реальный конечный кадр Scene 34 (`@Video1/@Image3`), в репозитории его нет; нет FRAME FILL; фраза про Warcraft внутри промта. |
| **36** Уход с картой | 1 | Wan 3 / Wan 3.0 | `DRAFT` | **D** | Нужны `@Video1` (конец Scene 17 — кадры в фильме, не в репо) и `@Video2` (транспорт на Набу — не подобран); Паша и Саша в кадре, но их identity не приложен; нет FRAME FILL. |
| **37** Перелёт к лесу | 1 | Wan 3 / Wan 3.0 | `DRAFT` | **D** | Нужны три видео-входа (конец 36, корабль/планета, первый кадр леса) — ни одного нет; перегружен для 30 с (посадка, взлёт, атмосфера, космос, планета); «Лёха» ↔ «Лёша». |
| **38** Рассматривает ПК | 1 | Wan 3 / Wan 3.0 | `DRAFT` | **C+** | Зависит от результата 35; повторяет бит «вытирает пыль с CRT» из 35; фраза «No generation authorized by this draft.» внутри промта; нет FRAME FILL. Сам текст сильный. |

Итого по 20 строкам таблицы: **A — 0, B-класс — 15, C — 2, D — 3.** Ни одна сцена не нарушает правило русской речи → Wan; ни в одной нет дыр в тайминге.

## 2. Сквозные наблюдения

### 2.1. Стыки соседних сцен (граничные кадры)

| Стык | Состояние | Комментарий |
|---|---|---|
| 24 → 25 | ✔ | END 24 («устойчивый полёт, звёзды впереди») совместим со START 25 («уже в прямом полёте»). |
| **25 → 26** | ⚠ разрыв | 25 заканчивается боем в космосе, 26 начинается стоящими на каменной террасе планеты. Ни посадки, ни прибытия нет ни в одном промте. Либо это монтажная склейка (тогда нужна решённая функция в монтаже), либо недостающий короткий переход. Решение — владельца. |
| **26 → 27** | ⚠ не определено | 27 «продолжает позиции Scene 26 слева-справа», но в 26 Серёги нет, а сторона, откуда он «смотрит» (off-camera), нигде не названа. Модель 27 свободна расставить его с любой стороны. |
| **27 → 30** | ⚠ мелкое | 27 заканчивается: Серёга на колене / в низкой обороне, камера низко за ним. 30 начинается «коты по обе стороны Серёги… смыкаются на пурпурном человеке» — позы не заданы. |
| 30 → 31 | ✔ | END 30 («отступает по связной лестнице, упавшая колонна позади») = START 31. |
| 31 → 32 | ✔ | END 31 («старая арка впереди») = START 32. |
| **32 → 33** | ⚠ сюжетная дыра | Дуэль 27–32 нигде не разрешается («No final victory or death»). Scene 33 при этом показывает Серёгу одного, без котов, и сама разрешает ставить себя «до или после боя». Как закончился бой и почему он один — не определено ни в одной сцене. |
| 33 → 34 → 35 | ✔ | Цепочка согласована по направлению движения и месту. |
| 35 → 38 | ✔ позы / ⚠ бит | START 38 («компьютер уже найден, рука у клавиатуры») совпадает с END 35 («тянется к клавиатуре, питание не нажимает»), но оба показывают один и тот же бит «вытирает пыль с CRT» (35, [0:17–0:23]; 38, [0:05–0:10]). |
| 36 → 37 | ✔ (при наличии видео) | END 36 («идёт к кораблю с картой») → START 37 («у люка корабля»). |
| 17 → 36 | вход вне репо | START LOCK 36 опирается на последний кадр Scene 17, который уже в фильме; файла кадра в `references/` нет (есть `S17-post-battle-seated.png` — подходящий вспомогательный кадр, в промте не используется). |
| Scene 20, части 1→11 | ⚠ общий текст | Везде одна формула «End this part on a stable, usable composition…»; фактических START/END STATE (где стоит Маша на берегу, куда повёрнута, направление движения) нет. «Не менять направление экрана» без указания самого направления. |
| Scene 28, A1→A2→A3 | ✔ | END STATE каждого блока совпадает со START STATE следующего (60 см лицом к лицу → жесты → разъезд). Исключение: A3/B3 ждут C28 (нет). |

### 2.2. Повторы и противоречия

- **Дословные повторы (гайд §6.4):** BIBLE Scene 20 повторена в каждой из 11 частей; в частях 1–11 identity-правила звучат 4–5 раз («IMPORTANT REFERENCE RULE», «IDENTITY LOCK», «COSTUME SURFACE LOCK», «SEQUENCE CONTINUITY LOCK», пункт BIBLE). В Scene 21 запрет бликов/отражений на стекле повторён в таймлайне, блоке CRITICAL, LIGHTING, CAMERA и NEGATIVE. Для Scenes 30–32 блоки `POWER`/`DESTRUCTION PHYSICS`/`CONTINUITY`/`NATIVE AUDIO`/`NEGATIVE` совпадают между собой ≈ на 75 % — это допустимо (каждый блок обязан быть автономным), но означает, что любая правка физики должна быть внесена в три места.
- **Противоречие «canopy»:** Scene 24 запрещает «bubble canopy» и тут же использует «Through the canopy» / «slide past the canopy»; Scene 25 — «canopy» в таймлайне и в NEGATIVE («generic fighter canopy»). Для кабины с фото `@Image4` корректнее «forward windows/viewports».
- **Операторские и редакторские фразы внутри копируемых блоков** (модель не должна их видеть): Scene 20 часть 12 («editorial cut to Part13/another existing phrase»); Scene 28 A8/A9/B8/B9 («Use this prompt only after the pose reference is actually prepared and approved» — L28/S28 уже созданы, фраза устарела; «reached by an editorial cut from another dance fragment»), A10/B10 («editorial freeze»); Scenes 30–32 («EDITING NOTE: … Do not claim the selected prior render already exists»); Scene 35 («suitable for the existing Warcraft/CRT story»); Scene 38 («No generation authorized by this draft.»).
- **Упоминания других сцен и «старых формулировок», смысла для модели не имеющие:** Scene 27 («@Image5 overrides older black-basalt / black-monolith / volcanic-glow / deep-red-storm wording» — модель этих формулировок никогда не получала; кроме того, они «заряжают» нежелательные слова в позитивной части промта); Scenes 30–32 («Scenes26/27»); Scene 38 («as Scenes 33–35»).
- **Репозиторные пути внутри промта:** Scene 20 часть 12 — `references/full/sasha.jpg`, `references/full/pasha.jpg` (генератор их не прочитает).
- **Фактическая внешность vs текст:** на sheet Паши — лёгкая щетина, короткие волосы с залысинами и тёмные наручи-бракеры; в master (Scene 20 ч. 12, Scene 28 A4/B4/A10) он «clean-shaven», наручи не упомянуты. Приложенный sheet имеет приоритет, но слово «clean-shaven» провоцирует модель убрать щетину. Серёга на sheet — тёмно-пурпурная мантия **с капюшоном** и чёрными рукавами подкладки; в тексте «long deep-purple robe» (капюшон не назван) — риск дрейфа силуэта, не критичный.
- **Нейминг движка:** `scene-meta.target_engine` — «Wan 3» (13, 26, 30–38) vs «Wan 3.0» в промте; для 16, 20, 21, 24, 25, 27 `target_engine` = Seedance 2.5, а реальные запуски — Wan 3.0 (master это знает: «планируемый движок и фактическая модель различаются»). Для будущих правок решить, меняет ли владелец целевой движок.
- **Мат:** в Scene 26 два нецензурных слова в реплике Рыжика («блядь», «распиздяями»). В заметках Саши (22:30) отмечено «мат перезвучить стоит» — решение о мате в финальной озвучке за владельцем. На сам промт это не влияет (Scene 26 принята).
- **Тексты песни:** части 1–11 Scene 20 содержат дословные строки охраняемой песни («Zombie»); master утверждает, что текст предоставлен пользователем (гайд §H это допускает). Но репозиторий публикуется на GitHub Pages: дословные тексты песни окажутся на публичном сайте. Решение владельца: оставить / заменить на плейсхолдеры (§H допускает) / убрать с публичной страницы. В промтах этого не менять без решения.

## 3. Находки по сценам и предложенные diff

Формат: **находка → предложение (текст, не применено)**. «≈ знаков» — оценка влияния на размер блока.

### Scene 13 — оценка B+

- Нет END STATE (есть последний бит `[0:27–0:30]`). Предложение: добавить после таймлайна  
  `END STATE: PURPLE strokes the cat across his lap, the cat's head resting down; BLACK back at the hookah; same two-shot geometry as @image1.` (≈ +190 знаков.)
- Нумерация: `@image3` не используется; `@image6/@image7` описаны первыми. Предложение: в строке REFERENCES сначала `@image1`, `@image2`, `@image4`, `@image5`, затем «supplemental @image6/@image7». Содержательно ничего не меняется; в манифесте слоты уже совпадают с master.
- Остальное (speaker ownership, push-in до реплики, закрытые рты, Wan 3) — образцовое для диалогов; не трогать.

### Scene 16 — оценка B (принята)

- В строке `Optimized for …` движок не назван, `scene-meta.target_engine` = Seedance 2.5, фактический запуск — Wan 3.0. Предложение: либо `target_engine: "Wan 3"`, либо оставить как есть (сцена принята, новых запусков не будет).
- `@Video1` — файл Drive/Library (`S16-desert-source-2.mp4`), в репозитории его нет, поэтому блок не «копируется и запускается» без обращения к Drive. Это зафиксировано в манифесте; при повторном запуске приложить видео из Drive.
- Меч Канцлера в сцене нигде не описан (у Ильюши — синий, у Артёма — зелёный, по `@Image5`). Если нужен красный клинок Серёги (как в сценах 27–32), добавить в `@Image5`/CHARACTER-блок: `Serega: no blade ignited unless stated` или `RED saber`. Решение сюжетное — владельцу.

### Scene 20 · части 1–11 — оценка B−

1. **Копипаст-ошибка в части 11 (диспетчеризация монтажа).** Раздел `TRANSITION / EDITING HANDOFF` последней части:  
   *Было:* `End this part on a stable, usable composition and a believable emotional state that can cut naturally into MASHA SONG PART 11.` … `so the next 30-second render can continue seamlessly.`  
   *Стало (предложение):* `This is the final part of the sequence. End on the stable wide lakeside composition described above, with Masha small but readable; no next part follows. Do not fade to black, do not freeze-frame, do not jump to a different location.` (≈ −130 знаков.)
2. **Размер и повторы.** Блок ≈ 12,5 тыс. знаков; `GLOBAL DIRECTING BIBLE` (≈ 1,9 тыс.) дословно повторена в каждой части; она же есть в шапке сцены. Предложение: из копируемых блоков оставить 3 пункта (локация постоянна; Маша в кадре почти всегда; плавная физически мотивированная камера), остальное — только в шапке (≈ −1,5 тыс. знаков на часть). Блоки `IMPORTANT REFERENCE RULE` + `CHARACTER APPEARANCE / IDENTITY LOCK` + `COSTUME SURFACE LOCK` + `SEQUENCE CONTINUITY LOCK` объединить в один `REFERENCE PRIORITY / IDENTITY LOCK` (≈ −700 знаков). **Оговорка:** части 3, 9, 10, 11 уже отрендерены прежним текстом; правка действует только на будущие запуски (master об этом уже говорит). Если реплейсить — единым проходом во все 11 частей, иначе нарушается принцип «одна правка во все варианты».
3. **Нет START/END STATE.** Для частей, где Маша идёт (2, 6, 9), задать направление (например, «вдоль берега слева направо в кадре»), а END каждой части — как START следующей. Пример для части 2 → 3: `END STATE: Masha stops mid-frame, torso turned to the lens, shoreline behind her left-to-right, medium framing.` / `START STATE: Masha stands mid-frame, torso turned to the lens, medium framing, same shoreline direction.` Направление — творческое решение.
4. **Движок.** `target_engine` — Seedance 2.5; три последние части (9–11) и Scene 20 ч. 12 уходили на Wan 3.0. В заголовке `Optimized for …` в частях 1–11 нет вообще. Решение владельца: целевой движок сцены.

### Scene 20 · вставки 12 и 13 — оценка C

Часть 12 (`Песня Маши 12`) и 13 написаны иначе, чем 1–11 (короче, «bible»-стиль), и не дотягивают до §6.1/§16A.

1. **Автономность.** В части 12: «same exact lake / shore from Parts 1–11» (стоит заменить прямым описанием берега); пути `references/full/sasha.jpg`, `references/full/pasha.jpg` внутри промта; «End with stable expression for editorial cut to Part13/another existing phrase» (реплика для монтажёра, не для модели). Предложение: убрать эти три фрагмента.
2. **Нет `CHARACTER APPEARANCE / IDENTITY LOCK` для Саши и Паши** — только по одной строке в `REFERENCES (AUTHORITATIVE)`. Предложение (по sheet'ам; текст ≈ 500 знаков):  
   `SASHA (@Image6): round wire glasses, short dark hair with a receding hairline, full dark beard, cream inner tunic under a dark burgundy hooded robe, brown belt with pouches, brown boots. PASHA (@Image7): short brown hair with receding temples, no beard (light stubble at most), dark navy tunic and trousers, dark leather forearm bracers, brown belt, tall dark boots. Do not blend the two faces; the sheets outrank this text.`  
   Исправляет «CLEAN-SHAVEN MALE» (на sheet щетина).
3. **Перегруз (§6.3).** За 30 с заказано 6 смен места/плана (реальная Маша → воспоминание-пара на берегу → shot/reverse-shot с жестом → два мужчины с зонтом/фото → match-cut назад → портрет), плюс «motivated internal music-video cuts». Это противоречит остальной сцене («no hard cuts, no random montage») и плохо управляется. Вариант (владельцу): оставить 3 бита (Маша → фантазия-пара одним устойчивым планом → Маша), остальное на монтаж.
4. **Противоречие правил пения.** `MUSIC / DIALOGUE RULE` велит «mouth movement should match the established user-provided song at the edit stage, or a neutral sustained wordless vocal phrase» — это инструкция монтажёру. Для генератора: либо `wordless sustained vocalise, sung, no lyric words`, либо точный текст (как в 1–11). Сейчас модель получит два взаимоисключающих указания.
5. **Часть 13:** два блока NEGATIVE (ранний и поздний) — слить; `FRAME FILL` — одной фразой вместо стандартного блока (то же в части 12: `FRAME: no bars, full frame.`). Предложение: заменить обе на стандартную формулу гайда:  
   `FRAME FILL / NO BARS: Fill the entire generated frame edge-to-edge. No letterboxing, no pillarboxing, no black bars, no side bars, no decorative borders, no empty margins.`

### Scene 21 — оценка B+

- Причина `needs_redo` не записана → содержательные правки вслепую невозможны. Спросить владельца, что не понравилось (стекло? лица? траектория?).
- Мелкая редактура: перечень запретов (flare / reflection / refraction / blur / flash) повторён в `[0:17–0:19] CRITICAL GLASS CROSSING`, `LIGHTING`, `CAMERA` и `NEGATIVE`. Ссылаться «выше» в автономном блоке нельзя (§16A), поэтому предложение такое: полный перечень оставить в `CRITICAL GLASS CROSSING` и в `NEGATIVE`, а в `LIGHTING` заменить пятое повторение одной фразой  
  `Exposure and colour stay continuous through the glass; no brightness jump.`  
  Экономия ≈ 400 знаков; запрет не ослабляется.

### Scene 24 — оценка B

*Было:* `Through the canopy, the hangar/pad begins to move downward…`; `Exterior structures slide past the canopy…`.  
*Стало:* `Through the forward windows/viewports…`; `…slide past the windows…` (оба места); в NEGATIVE оставить «generic bubble-canopy starfighter». Устраняет конфликт с `ENVIRONMENT / COCKPIT LOCK` (нельзя bubble canopy). Нет END STATE-заголовка: добавить `END STATE: stable forward flight, stars/upper atmosphere ahead, Ryzhik frame-left checking navigation, Luchik frame-right at the controls.` (≈ +200). Причина `needs_redo` неизвестна.

### Scene 25 — оценка B

- Те же «canopy» (таймлайн `[0:00–0:06]`, `[0:06–0:13]`, CAMERA). Предложение: «windows/viewports».
- Нет END STATE. Стык в 26 — решение владельца (варианты: (а) монтажная склейка на звук/вспышку без доп. сцены; (б) короткая сцена посадки; (в) END 25 = «корабль выходит из боя к планете с руинами» и START 26 — «на террасе после посадки»). Любой выбор — творческий, в промт не вносился.
- Первый запуск этой сцены уже в очереди: результат даст первые данные о том, держит ли модель левую/правую стороны Рыжика/Лучика на 30 с.

### Scene 26 — оценка B+ (принята)

- Сторона off-camera Серёги не задана. Чтобы 27 мог продолжить, предложение (в 26 править не обязательно; сцена принята, правку лучше внести в START STATE сцены 27): `Serega is off-camera on the frame-right side of the terrace; both cats face and angle their sabers toward frame-right.`
- «Head height roughly around a human knee» при отсутствии человека в кадре не задаёт масштаб. Предложение: привязать к объектам кадра («head below the height of a single terrace step / statue plinth») — для будущих запусков.
- Два нецензурных слова в репликах Рыжика («блядь», «распиздяями»): см. 2.2 (решение владельца).

### Scene 27 — оценка B−

1. **30 с: нет START STATE и нет текстового identity lock Серёги.** В частях 15 с он есть («pale older Chancellor face and build, balding crown with sparse light hair, long deep-purple robe»). Предложение для 30 с — перенести эти две строки (≈ +420 знаков) и добавить START STATE по образцу Части 1:  
   `START STATE: RYZHIK is slightly forward on camera-left/center, LUCHIK half a step behind on the opposite side, both facing frame-right; SEREGA stands frame-right at about four metres across the terrace, red saber ignited. All sabers lit. The fight begins from this standoff.` (≈ +330.)
2. **Лишний абзац `CONTINUITY FROM SCENE 26`** во всех трёх блоках (575 / 545 / 419 знаков): говорит о «старых черно-базальтовых формулировках», которых модель никогда не видела, и даёт модели слова `black-basalt / volcanic / deep-red-storm` в позитивной части (в NEGATIVE они уже есть). Предложение: заменить одной строкой `Begin directly after the cats' challenge, already inside the ancient sunset-lit stone city of @Image5; no new arrival, no temporal reset.` (≈ −400…−500 знаков на блок.) Части 15 с: 9 851 и 9 751 знак из лимита 10 000 — после замены с запасом; **любое добавление без такого вычитания части 1 уведёт за 10 000.**
3. Повтор запущен только для 30 с. 15 с-части не запускались; ничего в них менять без запуска не нужно, но правку 2 разумно внести во все три блока сразу (принцип §«одна правка во все production-варианты»).

### Scene 28 — оценка B+ (A- и B-версии)

1. **Операторские фразы внутри блоков:**  
   - A8/B8: `Use this prompt only after the pose reference is actually prepared and approved for anatomy.` (L28 существует и проверен) и `reached by an editorial cut from another dance fragment`;  
   - A9/B9: то же про S28 + `The following ensemble shot is an editorial cut to another formation`;  
   - A10/B10: `for the later editorial freeze`, `credits and any extended freeze are editorial operations outside this generation`.  
   Предложение: удалить первую фразу целиком; остальные заменить на нейтральное описание кадра: `This clip starts already in the supported pose; do not show the lift.` / `End on the held pose; nothing follows inside this clip.`
2. **A3/B3 зависят от несуществующего C28** (`@Image4 = будущий C28`). Пока C28 нет, блок невозможно запустить. Предложение: в тексте оставить fallback — `if C28 is unavailable, use P28 as the pose/axis reference` (P28 существует) — решение владельца, т. к. меняется порядок работы (A3 можно будет запускать без результата части 2).
3. A8/A9: «clockwise half-turn viewed from above» при камере на уровне груди — читается двусмысленно. Предложение: `a slow half-turn clockwise (seen from above) around his own vertical axis`.
4. Остальное — образец: START/END STATE совпадают по цепочке, внешность каждого персонажа описана, отрицания специфичны, свет по партитуре. Версии B (30 с) — те же шаги с растянутыми паузами; риск вялости отмечен в самом master.
5. Музыкальная рекомендация («Dance Commander») — не в промте, но в публичном master: уже есть оговорка «права этим планом не предоставляются».

### Scenes 30, 31, 32 — оценка B−

- **START STATE.** *Было (30):* `STARTING HISTORY: Optional next battle after Scene27, identical sunset city; start with the same terrace architecture, any verified prior damage preserved. The cats on both sides of Serega, all sabers lit.`  
  *Стало:* `START STATE: Serega stands on the weathered terrace, red saber lit, giving ground; Ryzhik (green) at his left, Luchik (blue) at his right, both knee-high cats closing in; same sunset city and dust as @Image5.` Для 31/32 — аналогично по их END STATE соседа (`END` 30 → `START` 31, `END` 31 → `START` 32 уже согласованы).
- **EDITING NOTE** во всех трёх — удалить из копируемого блока (это пометка для монтажёра).
- **FRAME FILL**: добавить стандартный блок (сейчас `Full 16:9 edge-to-edge` внутри NEGATIVE) — ≈ +190 знаков.
- Идентичность Серёги/котов описана в `REFERENCES / SPACE / IDENTITY` — отдельный заголовок не обязателен (§16A: смысловая проверка), но при переработке привести к `CHARACTER APPEARANCE / IDENTITY LOCK`.
- Если запущенный повтор использовал тот же текст — после результата оценивать с учётом пунктов выше.

### Scenes 33, 34 — оценка B (приняты)

- Вместо стандартного FRAME FILL — `FULL FRAME 16:9.` (33) и `16:9 edge-to-edge.` (34). Предложение: стандартная формула (≈ +180 знаков) — при следующем содержательном изменении, не отдельной правкой принятых сцен.

### Scene 35 — оценка D (DRAFT)

- Блокирующий вход: `@Video1/@Image3 MUST be the genuine end of approved-for-use Scene 34` — реального кадра в репозитории нет (результат 34 принят «в монтаж», кадр можно выгрузить из Topview/монтажа). Без него блок не автономен.
- Фраза внутри промта `End on an unresolved find suitable for the existing Warcraft/CRT story.` Предложение: `End on the unresolved find; the computer stays dormant.`
- Нет FRAME FILL. Бит «Serega brushes dust from a bulky CRT» ([0:17–0:23]) пересекается с Scene 38 — решить, где он остаётся.

### Scene 36 — оценка D (DRAFT)

- Обязательные входы: `@Video1` (последний кадр Scene 17 — в фильме, в репо нет) и `@Video2` («существующий кадр транспорта на Набу»), **не подобран**; промт сам пишет «If not provided, the render is NOT ready».
- **Паша и Саша в кадре, но identity не приложен** (в `REFERENCES` только Серёга, пещера, карта). Для сцены, где они сидят в кадре первые ~12 с, это главный риск дрейфа лиц. Предложение: добавить `@Image4 = references/full/pasha.jpg`, `@Image5 = references/full/sasha.jpg` + короткий lock (см. текст для Scene 20 ч. 12) либо приложить как `@Video1` последний кадр 17 с явным «faces of the two seated men are owned by @Video1». Нужна проверка лимита числа входов Wan 3.0.
- Вспомогательные кадры уже есть в паке Scene 17: `S17-post-battle-seated.png` (поза и расстановка), `S17-map-handoff.png` (карта в руках) — подходят для `@Image` вместо `@Video1`, если видео не загружается.
- Нет FRAME FILL.

### Scene 37 — оценка D (DRAFT)

- Три обязательных видео-входа, ни одного нет: конец 36 (сцена не создана), кадр корабля/планеты из монтажа, открывающий кадр лесной группы.
- **Перегруз 30 с (§6.3):** посадка в люк, закрытие, взлёт, атмосфера, космос, подход к планете + одна «time-compression edit» между атмосферой и космосом. Варианты (владельцу): (а) разделить на две сцены (отлёт / прибытие); (б) убрать посадку (она уже в конце 36); (в) оставить только отлёт + атмосферу, прибытие — монтаж.
- «Лёха» в тексте — алиас Лёши (PURPLE): в реестре добавлен (`character-references.json`), в промте при следующей правке использовать «Lesha».
- Нет FRAME FILL.

### Scene 38 — оценка C+ (DRAFT)

- Нужен реальный конечный кадр Scene 35 (которая ещё не создана) — по самому тексту DRAFT корректно.
- Бит `[00:05–00:10]` «вытирает узкую полосу пыли с нижней рамки CRT» повторяет Scene 35 `[00:17–00:23]` («brushes dust from… CRT monitor»). Предложение (владельцу): заменить в 38 на «читает надписи/шильдики на корпусе» или убрать из 35.
- Операторская фраза в END: `No generation authorized by this draft.` — удалить из копируемого блока.
- В тексте «as Scenes 33–35» → «as in the preceding scene».
- Нет FRAME FILL (только в NEGATIVE «pillarbox or black bars»).

## 4. Механический пакет (однозначные правки без творческого выбора)

Если писатель канона захочет сделать «одним коммитом» (каждый пункт — отдельная строка/блок, смысл сцен не меняется):

1. Scene 20 ч. 11: исправить `TRANSITION` (см. Scene 20, п. 1).
2. Сцены 30, 31, 32, 33, 34, 35, 36, 37, 38: добавить стандартный `FRAME FILL / NO BARS` (9 блоков).
3. Сцены 30, 31, 32: удалить `EDITING NOTE`; `STARTING HISTORY` → `START STATE`.
4. Сцена 28 A8/B8/A9/B9/A10/B10: убрать операторские/редакторские фразы.
5. Сцена 24/25: «canopy» → «windows/viewports» (в позитивной части).
6. Сцена 20 ч. 12: убрать пути `references/full/…` и «Parts 1–11»/«Part13».
7. Сцена 38: убрать `No generation authorized by this draft.`; сцена 35: фраза про Warcraft.

Не применять к уже запущенным/принятым результатам: правка master не меняет отправленный в Topview текст (правило provenance, §18 гайда).

## 5. ТОП-10 исправлений по важности

1. **Выяснить у владельца причину `needs_redo` для 21, 24, 27, 30, 31, 32 до того, как очередь Topview (6 из 6 слотов, ~24 ч) отработает те же тексты.** Если в задачах ушёл прежний промт, повтор занимает все 6 слотов и, вероятно, воспроизводит тот же дефект. (Не правка промта, но самый дорогой риск.)
2. **Scene 27 (30 с):** добавить START STATE и текстовый identity lock Серёги, убрать «older wording»; такую же замену абзаца `CONTINUITY FROM SCENE 26` внести в обе 15 с-части (укладываясь в 10 000 знаков).
3. **Scene 36:** приложить identity Паши и Саши (они в кадре 12 с без референса лиц); зафиксировать список обязательных входов (`@Video1`, `@Video2` либо кадры `S17-post-battle-seated.png`/`S17-map-handoff.png`).
4. **Сюжетная дыра 32→33 и 25→26:** решить, как заканчивается дуэль 27–32 и как коты оказываются на планете. Без этого 33–38 и 26 нельзя уверенно ставить в монтаж, а ни один из промтов этот момент не покрывает.
5. **Scene 20, часть 11:** исправить `TRANSITION` («into MASHA SONG PART 11» в последней части) — однострочная механическая ошибка.
6. **Scene 20, вставка 12:** переписать как автономный блок: убрать пути/«Parts 1–11»/«Part13», добавить identity lock Саши и Паши по sheet'ам (исправить «clean-shaven»), сократить до ≤3 смен плана, убрать инструкцию «match at the edit stage».
7. **Scenes 30–32:** `STARTING HISTORY` → настоящий `START STATE`, удалить `EDITING NOTE`, добавить FRAME FILL; стык 27→30 (поза Серёги).
8. **Scene 28:** убрать операторские фразы в A8/A9/A10/B8/B9/B10 и определить fallback для A3/B3 (C28 ещё нет; P28 есть).
9. **Scene 37:** разгрузить (посадка + взлёт + атмосфера + космос + планета за 30 с) и закрыть три видео-входа; **Scenes 35/38:** убрать повтор бита «пыль с CRT» и фразы-пометки.
10. **FRAME FILL в 9 новых сценах (30–38)** и «canopy» в 24/25 — механическая чистка (см. §4).

## 6. Что требует решения владельца (не техническое)

- Причина `needs_redo` у 21, 24, 27, 30–32 (см. топ-10 п. 1).
- Как заканчивается бой 27–32 и как коты попадают на планету (п. 4).
- Целевой движок сцен 16/20/21/24/25/27 (meta Seedance 2.5 vs реальный Wan 3.0).
- Мат в Scene 26 и дословные строки песни в публичном master.
- Нужен ли у Scene 20 весь набор из 13 частей и каково место вставок 12–13 (подробнее — `montage-plan-v3-draft.md`).
