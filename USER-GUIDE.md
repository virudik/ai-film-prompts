# USER-GUIDE v4.0 — AI Film Project

**Дата актуализации:** 20.09.2026  
**Для кого:** владелец проекта и любой чат/агент, который должен быстро понять, как проект устроен.

## 1. Главное правило

Единственный editable master промтов:

`Google Drive / AI Film Prompts Master / video-prompts.md`  
Drive ID: `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`

GitHub, сайт, Notion и Library не являются вторым prompt master.

## 2. Что обязан прочитать новый чат

Перед вступлением в роль редактора новый чат читает **все семь** документов:

1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

После этого:
- fresh Drive `video-prompts.md`;
- live `project-status.json`;
- live `topview-status.json`;
- live `instruction-sync-status.json`;
- при работе с сюжетом: `film-analysis.md`, `film-backlog.md` и релевантный Notion `Кино`.

Чат не должен заставлять пользователя повторять сведения, которые уже есть в этих источниках.

## 3. Как изменить существующую сцену

Правильный процесс:

1. fresh-read exact Drive master;
2. найти Scene ID;
3. проверить slow/status/dependencies;
4. если меняется сам prompt — прочитать `PROMPT-STYLE-GUIDE.md`;
5. сделать минимальную правку;
6. сохранить в **тот же Drive file ID**;
7. trigger GitHub sync;
8. дождаться validation/status/Pages;
9. проверить результат;
10. только после этого сообщить о завершении.

## 4. Как добавить новую сцену

Удалённые Scene IDs не переиспользуются.

Если следующий Scene ID однозначно определяется из fresh master, чат **сам присваивает следующий новый стабильный ID** и не спрашивает пользователя номер.

Новая сцена должна получить:
- TOC entry;
- anchor;
- title;
- `scene-meta`;
- контекст;
- references;
- human summary;
- полный master-level prompt;
- корректные counts/status.

Slow-marker добавляется только при реальном запуске/решении о canonical slow.

## 5. Как писать промты

Полная обязательная инструкция:

`PROMPT-STYLE-GUIDE.md`  
Drive ID: `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`

Она обязательна для всех новых и существенно перерабатываемых prompts.

Перед prompt work чат:
- перечитывает guide;
- перечитывает master;
- сверяется с 1–2 актуальными похожими сценами.

Обычно master-level prompt должен проработать:
- engine/technical parameters;
- exact reference roles;
- identity/reference priority;
- scene goal;
- timeline/story flow;
- camera/continuity;
- performance;
- dialogue/vocal/lip-sync;
- lighting/material/environment;
- native audio;
- scene-specific negative prompt;
- `FRAME FILL / NO BARS`.

Нельзя возвращаться к коротким общим промтам, если master использует более детальную режиссёрскую структуру.

## 6. Slow и Topview

Slow membership определяет master / `project-status.json`, а не Topview.

Topview даёт telemetry:
- task;
- model;
- status;
- start/finish;
- queue;
- ETA.

`success` = задача технически закончилась. Это **не означает**, что ролик принят.

Slow-lock снимается только после пользовательского решения/ошибки/нужного workflow.

## 7. Control Center

Сайт:

`https://virudik.github.io/ai-film-prompts/`

Текущий baseline:
- активные сцены и полные prompts;
- merged slow + Topview;
- модель/status/start/elapsed/queue/ETA;
- sync lightsaber;
- reference viewer;
- светлая/тёмная тема;
- `Контрольный отпечаток`;
- непосредственно под ним отдельная раскрывающаяся секция `💬 Комментарии, идеи и предложения`;
- comments/replies без GitHub account через Supabase;
- старой кнопки `Архив GitHub` нет.

Site-only правки делаются в GitHub `index.html`, затем обязательны JS syntax check, duplicate IDs check и Pages verification.

## 8. Комментарии

Supabase:
- organization `Vint`;
- project `ai-film-comments`;
- ref `vzohfatqzyioydtgjiyd`;
- Edge Function `submit-comment`.

Есть:
- public read;
- anonymous posting;
- replies;
- RLS;
- honeypot;
- rate limit 5 / 10 min / IP.

В публичном HTML запрещён `service_role`. Comments не могут менять master или запускать генерации.

## 9. Где что хранится

**Drive** — editable master и инструкции.  
**GitHub** — mirror/status/site/Pages.  
**Notion** — идеи, сюжет, история, старый prompt bank.  
**Library** — recovery mirror/cache.  
**Topview** — telemetry генераций.  
**Supabase** — comments backend.

Если источники конфликтуют, current prompt/runtime truth берётся из fresh Drive master + live status JSON, а не из старой Library/Notion копии.

## 10. Как фиксировать новые функции и правила

Если в проекте появляется постоянное нововведение — функция сайта, backend, новый prompt rule, workflow, status, источник истины, recovery step — недостаточно просто изменить код.

В том же цикле нужно:
1. обновить релевантные Drive-инструкции;
2. обновить SAME `NEW-CHAT-HANDOFF.md`;
3. обновить `PROMPT-STYLE-GUIDE.md`, если меняется prompt-writing;
4. зеркалировать в GitHub;
5. refresh `instruction-sync-status.json`;
6. проверить status/Pages;
7. обновить Notion operational pointer;
8. обновить Library recovery copies.

Это обязательный Definition of Done для материальных изменений.

## 11. Notion

Notion `Кино` остаётся полезным для:
- старого сценарного плана;
- идей;
- локаций;
- исторических промтов;
- альтернативных сюжетных решений.

Но это не текущий prompt master.

Операционный указатель:
`AI Film — Актуальная инструкция / Handoff`.

Страница `Важные промты` считается legacy bank и должна использоваться как inspiration/history, а не как актуальный стандарт.

## 12. Library

Library нужна для восстановления между чатами.

Она должна содержать свежие recovery copies семи инструкций и связанных summary/status файлов, но при наличии Drive:
**Drive всегда сильнее Library**.

## 13. Что новый чат не должен делать

- не спрашивать известный Scene ID, если он выводится из master;
- не просить пользователя вручную вставлять текст, если доступна запись;
- не создавать параллельный master;
- не брать GitHub/Library copy как editable authority;
- не массово переписывать NEEDS_FIX;
- не approve/rerun по Topview success;
- не использовать старый Notion prompt как новый master prompt без проверки;
- не считать старый GitHub failure email текущей аварией без live-check.

## 14. Как понять, что задача реально завершена

Master change:
Drive write → GitHub sync → validation → current status → Pages.

Instruction/material change:
seven Drive docs → seven GitHub mirrors → fresh instruction status → Notion pointer → Library recovery copies.

До этого слово `ГОТОВО` преждевременно.

## 15. Персонажи и обычные имена в запросах

Новый чат обязан заранее ознакомиться со вкладкой сайта **Персонажи / Референсы** и `character-references.json`. Поэтому пользователь может писать естественно: «Паша говорит Саше», «заходит Серёжа», «Лёша идёт рядом с Виталиком» — без повторного описания внешности.

Редактор сам связывает имя с approved model sheet и current master, а в prompt фиксирует каноническую внешность/костюм/роль и reference priority. Если персонаж scene-specific и не находится в глобальном registry, используются свежие references конкретной сцены. Уточнение нужно только при настоящей неоднозначности.

Текущие global names: Серёга/Канцлер, Юля, Паша, Артём, Илюша, Саша, Лёша, Виталик. `Серёжа` в однозначном контексте = Серёга.

## 16. Монтажный разбор как часть onboarding

Перед сообщением «готов продолжать» новый чат открывает на сайте **Монтажный разбор фильма**, затем сверяет его с `film-analysis.md` и `film-backlog.md`. Это нужно, чтобы он понимал не только отдельные prompts, но и весь фильм: структуру, сюжетные пробелы, переходы, диалоги, финал и уже предложенные исправления.

Он не обязан держать весь большой HTML в активном контексте дословно; обязан извлечь актуальную рабочую карту и при конкретной монтажной задаче дочитать нужный участок.

## 17. Финальный onboarding check

Новый чат докладывает о готовности **только после** проверки актуальности Drive, GitHub, сайта, instruction status, references, montage context, Notion pointer и Library recovery. Если документация безопасно устарела — сначала актуализирует её. Если обнаружено противоречие, которое меняет творческий канон или approval, сообщает его пользователю вместо самовольного решения.

## 18. Новая генерация Topview может сама появиться как сцена

Автоматизация теперь умеет импортировать **новую видеогенерацию Topview**, которой ещё нет в проекте:
- находит новую video task;
- проверяет, что это не retry/duplicate;
- берёт настоящий prompt и модель из Topview;
- сама присваивает следующий Scene ID;
- создаёт описание сцены и сохраняет фактический prompt;
- running task добавляет в slow;
- completed result помечает `RESULT_RECEIVED`, но не «принято»;
- синхронизирует Drive → GitHub → сайт.

Если данных недостаточно или непонятно, новая ли это сцена, автоматизация ничего не записывает и просит решение вместо угадывания.

## 19. Служебные файлы на сайте

В шторке **«Служебные файлы»** теперь должен быть виден полный набор из семи инструкций с русскими названиями, плюс master, анализ фильма и backlog.

## 20. Как теперь работает Recovery Sync

Отдельной ежедневной automation нет. Одна `AI Film Recovery Sync` запускается каждый час:
- обычно делает лёгкую проверку проекта;
- один раз примерно в 24 часа, когда это показывает `deep-audit-status.json`, в том же запуске выполняет глубокий техосмотр master, prompts, персонажей, монтажного анализа, Notion, Library, сайта, Supabase и GitHub Actions/Pages.

Topview остаётся отдельным процессом: `Topview Scene Intake & Slow Watch`. Это специально, чтобы production intake/очереди/создание новых Scene ID не смешивались с recovery-аудитом.

## 22. Почему в «Служебных файлах» больше семи кнопок

Инструкций по-прежнему **ровно семь**. Они идут сверху вертикально и пронумерованы 1–7 в порядке обязательного чтения.

Ниже отдельно находятся три рабочих файла, и их кнопки тоже идут **строго друг под другом**:
1. канонический master;
2. анализ фильма;
3. backlog.

Это не восьмая, девятая и десятая инструкции и не копии существующих документов.
