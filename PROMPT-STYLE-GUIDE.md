# PROMPT-STYLE-GUIDE — единый стандарт видео-промтов

**Версия:** 1.4  
**Дата:** 22.09.2026  
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

## 6. Уровень подробности и принцип качества

Главный принцип: **maximum useful specificity, minimum redundant wording**.

Хороший master-level prompt — не самый длинный. Он достаточно конкретен, чтобы модель однозначно поняла персонажей, действие, пространство, камеру, звук и ограничения, но не повторяет один и тот же смысл в нескольких длинных блоках.

### 6.1. Самодостаточность без раздувания

Каждый production prompt, который пользователь копирует отдельно, должен быть самодостаточным. При этом автономность **не означает** механически копировать внутрь каждого блока весь scene-level bible.

В автономный prompt переносить:
- exact reference roles и priority;
- short appearance/identity lock каждого важного персонажа;
- обязательные continuity facts для этой части;
- конкретное действие / dialogue / vocals;
- camera plan;
- нужные lighting/audio/negative constraints;
- START STATE / END STATE, если prompt является частью последовательности.

Scene-level bible может хранить более подробную драматургию и общую режиссуру серии, но отдельный prompt должен содержать только ту её часть, которая реально нужна этой генерации.

### 6.2. Приоритеты MUST / SHOULD / MAY

При сложном prompt редактор обязан мысленно, а при необходимости явно, разделять требования по важности.

**MUST — нельзя потерять:** exact identity / approved costume or form; reference ownership and priority; обязательные персонажи и реквизит; точные действия, реплики и порядок событий; ключевой старт/финал; критический continuity.

**SHOULD — желательно сохранить:** конкретная траектория камеры; эмоциональная динамика; lighting / production-design нюансы; второстепенные физические реакции.

**MAY — можно оставить модели свободу:** микрожесты; небольшие естественные вариации ветра, дыма, воды; второстепенная фоновая жизнь, если она не ломает continuity.

Если требований слишком много, сокращать MAY и часть SHOULD, а не MUST.

### 6.3. Complexity budget

Не перегружать 20–30 секунд количеством независимых событий. Перед сохранением prompt проверить:
- сколько ключевых действий должно произойти;
- сколько персонажей одновременно говорят/двигаются;
- сколько смен композиции/камеры запрошено;
- хватает ли времени на реплику + паузу + реакцию + переход;
- не требуют ли два события несовместимых позиций персонажа или камеры одновременно.

Если prompt перегружен, лучше сократить beats или разделить генерацию, чем компенсировать перегрузку ещё большим количеством текста.

### 6.4. Запрет семантических дублей

Критическое правило можно повторить максимум там, где повторение действительно усиливает управление моделью, например один раз в `REFERENCE PRIORITY` и один раз в коротком `IDENTITY LOCK`.

Не нужно три-четыре раза разными словами повторять `same face`, `same costume`, `same location`, если смысл уже однозначно закреплён. Повторение не заменяет точность и может размывать относительный приоритет остальных требований.

### 6.5. Короткая формула «делать / не делать»

**Делать:** конкретно назначать роли референсов; защищать identity; писать только выполнимые beats; давать камере физически понятную траекторию; сохранять пространство и continuity; рассчитывать речь/пение по времени; описывать звук, если он нужен; оставлять модели свободу только в некритичных деталях.

**Не делать:** превращать prompt в набор эпитетов; смешивать роли нескольких reference images; заставлять пользователя вручную доклеивать общий identity-блок; повторять одну мысль 3–4 раза; перегружать 30 секунд независимыми событиями; использовать огромный универсальный negative prompt вместо рисков конкретной сцены; копировать устаревший live-example как источник истины; спрашивать заново уже известную внешность персонажа.

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


Для последовательных генераций предпочтительно явно фиксировать handoff:

```text
START STATE:
[позиция персонажей, поза/направление, состояние реквизита, камера/крупность, свет]

END STATE:
[позиция персонажей, поза/направление, состояние реквизита, камера/крупность, свет]
```

`END STATE` текущего блока должен быть совместим с `START STATE` следующего. Это полезнее абстрактной фразы `preserve continuity`, особенно для 8–30-секундных последовательностей.

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

Также это плохие практики:

- `same character as reference` без реальных distinguishing traits, если они уже известны из approved model sheet/registry;
- `see shared block above` / `follow the shared block above` внутри prompt, который копируется отдельно;
- несколько reference images без ясного ownership: кто задаёт лицо, кто костюм, кто композицию, кто локацию;
- огромный универсальный negative prompt, не связанный с рисками сцены;
- повторение одного identity/continuity правила в 3–5 местах вместо короткого приоритетного lock;
- слишком много beats для заданной длительности;
- камера, которая одновременно должна быть continuous take и делать физически невозможные скачки/обратные направления;
- полные копии live-prompts внутри этой инструкции как «вечные эталоны»: актуальный текст всегда брать из fresh master.

## 11. Финальный prompt-QA перед сохранением

Перед записью в master редактор обязан проверить не только наличие блоков, но и их **согласованность и полезность**.

### A. Структура и references
- [ ] Scene ID определён по стабильным правилам и не переиспользован.
- [ ] `scene-meta` соответствует движку, длительности, языку и production state.
- [ ] Есть `Контекст использования`, `Референсы`, `Что происходит`.
- [ ] Техническая строка соответствует реальному движку/режиму.
- [ ] Каждому reference назначена конкретная роль.
- [ ] При 2+ references явно разрешён ownership/priority там, где возможен конфликт.
- [ ] Environment/group/start/end reference не может случайно переопределить identity отдельного персонажа.

### B. Персонажи
- [ ] Каждый важный известный персонаж resolve через `character-references.json` + fresh master/current variant.
- [ ] В автономном production prompt есть short appearance/identity lock с реальными distinguishing traits.
- [ ] Costume/form соответствует именно этой сцене, а не случайному варианту из другой сцены.
- [ ] При нескольких персонажах ясно, какой reference принадлежит кому; запрещено face blending / swapping.

### C. Исполнимость и режиссура
- [ ] Timeline/story flow физически реалистичен для длительности.
- [ ] Dialogue/vocals реально помещаются в выделенное время с дыханием/паузами/реакциями.
- [ ] Complexity budget не перегружен лишними независимыми beats.
- [ ] Камера физически понятна, стабильна и совместима с заявленным continuous/shot-based режимом.
- [ ] Для цепочки сцен определены совместимые START STATE / END STATE, если это полезно.
- [ ] Performance описывает изменение состояния, а не только статичную эмоцию.

### D. Реализм, звук и негативы
- [ ] Environment / lighting / material realism описаны ровно настолько, насколько нужны сцене.
- [ ] Audio конкретен при `Native audio: on`.
- [ ] Negative prompt ориентирован на реальные риски именно этой сцены, а не является бесконечным универсальным хвостом.
- [ ] `FRAME FILL / NO BARS` присутствует, если пользователь явно не отменил правило.

### E. Редактура prompt
- [ ] Нет внутренних противоречий.
- [ ] Нет семантических дублей и ненужного повторения больших блоков.
- [ ] MUST-требования заметно важнее SHOULD/MAY деталей.
- [ ] Prompt полностью самодостаточен: один блок можно скопировать и запустить без текста выше/ниже.
- [ ] Нет зависимостей вида `see shared block above`.
- [ ] Все references, названные в prompt, реально существуют и используются.

### F. После записи
- [ ] Обновлены map/counts/meta, если это требуется архитектурой.
- [ ] Выполнена стандартная Drive → GitHub → validator/status → Pages проверка.

Если любой пункт A–E нарушен, prompt ещё не готов, даже если он выглядит длинным и «кинематографичным».

## 12. Эталон качества: только fresh master, без полнотекстовых копий

Эта инструкция **не хранит полные копии текущих live-prompts** как вечные примеры. Причина: master меняется, сцены могут быть удалены, переработаны или получить новые reference roles; встроенная копия неизбежно становится stale и начинает учить сменщика устаревшему состоянию.

Как работать правильно:
1. перед созданием/переработкой prompt перечитать fresh `PROMPT-STYLE-GUIDE.md`;
2. открыть fresh `video-prompts.md`;
3. выбрать одну-две **текущие активные** сцены, близкие по типу задачи (dialogue / action / music / continuous take / multiple references), только как живые structural examples;
4. брать из них удачные паттерны структуры, но не копировать факты, одежду, references или scene-specific negative prompt;
5. если пример в handoff/старом обсуждении расходится с fresh master, fresh master имеет приоритет.

Хороший эталон определяется не номером сцены, а качествами:
- ясные reference roles и priority;
- точный short identity lock;
- реалистичная timeline/beat structure;
- физически понятная камера;
- coherent 3D space;
- acting/dialogue/audio specificity;
- risk-oriented negative prompt;
- автономность copy-paste блока;
- отсутствие лишнего повторения.

Никогда не считать удалённую/неактивную сцену автоматически действующим эталоном только потому, что она когда-то была вставлена в документацию.

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

Не хранить здесь фиксированный список персонажей как canonical truth: он быстро устаревает. Актуальный roster и aliases всегда брать из fresh `character-references.json` + current master.

Персонажи, существующие только в конкретных current prompts (например Маша-Лагуна или Imperial Officer), разрешаются через fresh scene references/master. Не выдумывать global model sheet для персонажа, которого там нет.

Если user name/alias реально может относиться к двум разным людям и current sources не снимают неоднозначность, задать один точный вопрос. В остальных случаях resolve самостоятельно.

## 16A. Автономность каждого prompt-блока и обязательное описание внешности

Любой prompt, который пользователь может копировать в генератор как отдельный блок, обязан быть **полностью автономным**. Пользователь не должен собирать prompt из нескольких мест, отдельно копировать общий identity-блок или помнить правила, находящиеся выше по странице.

Обязательный стандарт для всех новых prompt-блоков и серийных частей одной сцены (`Часть 1`, `Песня 1`, `Shot 3` и т.п.):

- внутри **каждого** копируемого prompt-блока должен быть собственный краткий `CHARACTER APPEARANCE / IDENTITY LOCK`;
- в нём кратко фиксируются ключевые признаки внешности каждого важного персонажа: лицо, возрастной образ, телосложение/пропорции, кожа/цвет, волосы или эквивалентные head elements, одежда/костюм, силуэт и критические дизайн-элементы;
- attached model sheet / face reference остаётся абсолютным визуальным источником identity; если текстовое описание случайно конфликтует с approved reference, следует reference;
- для известного персонажа редактор обязан сам получить описание из `character-references.json` + fresh master/current scene variant. **Не спрашивать пользователя заново**, если identity уже однозначно известна;
- если у сцены есть длинный общий identity bible, он может оставаться в master как документация/continuity layer, но отдельный production prompt **не должен зависеть** от ссылки вида `see shared block above`, `follow the shared identity block above` и т.п.;
- каждый prompt должен работать по принципу: **открыл один блок → скопировал целиком → приложил указанные references → запустил генерацию**;
- short appearance lock должен быть достаточно конкретным, чтобы удерживать identity на wide / profile / orbit / close-up ракурсах, но не раздувать prompt повторением полного паспорта персонажа;
- если в prompt несколько персонажей, краткий appearance/identity lock обязателен для каждого важного персонажа либо в общем компактном block с явным разделением по именам;
- запрещено подменять точное описание общими словами вроде `same character as reference`, если в registry/master уже есть однозначные отличительные признаки, полезные для консистентности.

Рекомендуемый формат:

```text
CHARACTER APPEARANCE / IDENTITY LOCK:
@ImageX is the absolute visual authority for [Character Name]. Preserve the exact face, body proportions, approved skin/hair/color identity, costume or silhouette, and the key design elements from the attached reference. Do not redesign, beautify, age-shift, replace hairstyle/head structure, change costume logic, or alter the approved character design.
```

Это шаблон структуры, а не повод писать одинаковый абстрактный текст для всех. Для конкретного персонажа редактор должен подставлять **реальные отличительные признаки из approved model sheet/current variant**.

Definition of Done для любого автономного prompt:
- prompt полностью самодостаточен;
- внутри есть short appearance/identity lock с реальными отличительными признаками;
- нет зависимости от prose выше/ниже копируемого блока;
- reference roles ясны;
- written appearance не конфликтует с attached reference;
- пользователь не должен дополнительно уточнять, что именно ещё вставить в генератор.

### Совместимость со старыми prompts

Для **новых и существенно перерабатываемых** production prompts использовать стандартный заголовок `CHARACTER APPEARANCE / IDENTITY LOCK`.

Для старых prompts audit должен проверять **семантическое наличие** identity protection, а не только буквальное совпадение заголовка. Если equivalent lock уже корректно реализован внутри `ENVIRONMENT & ASSET LOCK`, `IMPORTANT REFERENCE RULE` или другого ясного блока, это не automatic failure. При следующей содержательной переработке сцену привести к текущему стандартному заголовку.

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

Раз в 24 часа `AI Film Recovery Sync` внутри daily deep audit может **проверять** активные/new prompts на regression относительно этого guide.

Проверять прежде всего:
- reference ownership/priority при нескольких изображениях;
- identity/appearance protection каждого важного персонажа;
- автономность copy-paste блока;
- timeline/dialogue timing feasibility;
- camera/continuity и START/END handoff для последовательностей;
- semantic duplication / prompt bloat;
- risk-oriented negative prompt;
- audio и `FRAME FILL / NO BARS`, когда применимо.

Audit должен быть **семантическим**, а не тупым grep по одному заголовку. Отсутствие буквальной строки `CHARACTER APPEARANCE / IDENTITY LOCK` в legacy prompt не является само по себе дефектом, если equivalent identity lock реально присутствует и однозначен.

Это audit, а не разрешение автоматически переписывать творческий prompt. Автоматически допустимы только однозначные механические/documentation fixes. Содержательное изменение сцены, диалога, режиссуры или approval требует обычного editor/user workflow. Deep-audit result записывается в `deep-audit-status.json`; Topview auto-intake остаётся отдельной automation.

## 20. Место этой инструкции в takeover order

На Control Center этот файл отображается как **№4 «Стандарт написания промтов»** в вертикальном seven-document списке. До него новый чат читает HANDOFF, Sync Runbook и Project Guide; после него — User Guide, README AI Sync и Backup AI Runbook.

Master/film-analysis/backlog, находящиеся в той же общей шторке, относятся к рабочим файлам проекта и не являются дополнительными prompt-инструкциями. В UI они вынесены в отдельный блок и также идут вертикально один под другим.

## 21. Граница ответственности этого guide

`PROMPT-STYLE-GUIDE.md` отвечает только за качество, структуру и provenance prompts. Runtime-модель Topview, slot capacity, `active_tasks[]`, slow-table UI, queue/ETA telemetry и recovery invariants находятся в `SYNC-RUNBOOK.md` и не должны дублироваться здесь.
