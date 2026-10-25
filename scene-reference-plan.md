# Scene Reference Pack Plan — AI Film Серёгиус

Обновлено: 2026-10-11T18:26:33Z

25 типизированных manifests: 18 активных и 7 исторических «в фильме». 58 привязок всего; 51 относятся к активным промтам (включая 20 вариантов Scene 28). Канон — GitHub `main/video-prompts.md`; этот файл — производный индекс, не разрешение на генерацию.

## Global workflow

1. Before a scene is created or launched, read fresh canonical master + prompt guide + scene pack manifest.
2. Reuse approved character sheets, exact location refs, exact props and exact first/last frames before making anything new.
3. Decide whether the scene needs additional scene-specific stills: pair/group blocking, pose, prop handoff, lighting state, or continuity state.
4. Generate one still at a time. After each result, visually compare identity, wardrobe, location, geometry, pose and character count. Reject drift/duplicates/merged faces/incorrect anatomy.
5. The moment a still is accepted as useful, SAVE IT BEFORE THE NEXT GENERATION: Drive Scene pack + Library recovery + GitHub/site thumbnail when it is part of the scene inputs.
6. Multi-character images are built from small verified groups/subgroups; individual sheets always outrank composition helpers for identity.
7. For scenes already rendered in Topview, recover and record the exact input-image S3 sources from the corresponding task; reuse them and propose only additive improvements.
8. On the site, scene-used reference images are shown as compact thumbnails linking to the full file. Do not let full-size images change the page scale.
9. Command `запускай сцену N` means: fresh-read master/status -> resolve scene pack -> ensure required references -> update prompt reference mapping if needed -> preflight Topview model/slots/cost -> submit only after the user's command. Technical success never means approval.
10. Never silently spend credits for a reference-image helper. Prefer an actually verified unlimited route when available; otherwise stop before submit and report the cost/path issue.

## Текущий статус

| Сцена | Состояние канона | Привязок | Файлов в manifest | Остаток |
|---|---|---:|---:|---|
| 10 | in_film | 1 | 4 | Исторический пакет; задача закрыта владельцем. |
| 11 | in_film | 1 | 4 | Исторический пакет; задача закрыта владельцем. |
| 13 | active | 1 | 9 | Обязательные референсы учтены; приёмка и запуск отдельно. |
| 16 | active | 1 | 6 | Обязательные референсы учтены; приёмка и запуск отдельно. |
| 17 | in_film | 1 | 10 | Исторический пакет; задача закрыта владельцем. |
| 19 | in_film | 1 | 8 | Исторический пакет; задача закрыта владельцем. |
| 20 | active | 13 | 8 | Обязательные референсы учтены; приёмка и запуск отдельно. |
| 21 | active | 1 | 6 | Обязательные референсы учтены; приёмка и запуск отдельно. |
| 22 | in_film | 1 | 2 | Исторический пакет; задача закрыта владельцем. |
| 23 | in_film | 1 | 6 | Исторический пакет; задача закрыта владельцем. |
| 24 | active | 1 | 4 | Обязательные референсы учтены; приёмка и запуск отдельно. |
| 25 | active | 1 | 4 | Обязательные референсы учтены; приёмка и запуск отдельно. |
| 26 | active | 1 | 4 | Обязательные референсы учтены; приёмка и запуск отдельно. |
| 27 | active | 3 | 6 | Обязательные референсы учтены; приёмка и запуск отдельно. |
| 28 | active | 20 | 24 | A1/A2 Seedance 2.0 15s and B1/B2 Wan 3.0 30s are owner-authorized A/B candidates; launch only via signed-in Topview website with verified unlimited zero-credit mode. If Seedance is not unlimited, owner fallback is B1/B2/B4/B5. A3/B3 require actual C28 from part 2. |
| 29 | in_film | 1 | 4 | Исторический пакет; задача закрыта владельцем. |
| 30 | active | 1 | 6 | Drive Scene Reference Pack folder and Library copy not created (reused assets already live in packs of Scenes 10/26/27) |
| 31 | active | 1 | 6 | Drive Scene Reference Pack folder and Library copy not created (reused assets already live in packs of Scenes 10/26/27) |
| 32 | active | 1 | 6 | Drive Scene Reference Pack folder and Library copy not created (reused assets already live in packs of Scenes 10/26/27) |
| 33 | active | 1 | 2 | Drive Scene Reference Pack folder and Library copy not created (reused assets already live in packs of Scenes 10/26/27) |
| 34 | active | 1 | 2 | Drive Scene Reference Pack folder and Library copy not created (reused assets already live in packs of Scenes 10/26/27) |
| 35 | active | 1 | 2 | Внешний task уже active; не повторять. В его входах нет Video1/Image3. Видео34 и кандидат конца сохранены для проверки стыка после результата. |
| 36 | active | 1 | 5 | @Video1 — фактический конец Scene 17 из монтажа: выгрузить и сохранить перед запуском; без него сцена остаётся DRAFT. |
| 37 | active | 1 | 3 | @Video1 — корабль и кабина Канцлера из ч. 1 (09:20–09:55): выгрузить из монтажа перед запуском.; @Video2 — установочный план лесной планеты (51:52–52:40): выгрузить; корабль лесной пары не использовать. |
| 38 | active | 1 | 2 | @Video1/@Image3 — выбранный конечный кадр Scene 35: Scene 35 ещё не сгенерирована; до этого сцена DRAFT. |

Счётчики получены из manifests; состояние active/in_film — из свежего master/status и владельческого ledger. Наличие обязательных полей не означает готовность всех входов: Scenes 35–38 остаются DRAFT с недостающими реальными видео/граничными кадрами. `null` у Drive/Library означает отсутствие подтверждённого ID. Для кандидатов Scene 35 создан один пакет в Drive; остальные новые папки 29–38 не дублировались.

Scene 16: оба точных исходных видео сохранены в Drive/Library, Video1 — второй ролик. Пустая локация — реконструкция, не оригинальное фото. Конфликт владельческих решений «Принять / Переделать» не разрешается индексом.

Scenes 10/11: дополнительный three-shot отменён владельцем; обе сцены в фильме. Scene 17 также в фильме, точный исходный Video1 сохранён; новые Scenes 36–37 требуют фактического монтажного стыка и транспорта.

Scene 19: историческая задача e4ad0298… использовала Image3=Саша, Image4=Паша, Image5=Маша. Архивный canonical prompt имеет другую нумерацию; его mapping сохранён отдельно. Исторические task slots не переносить на новые промты.

Scene 28: точные S28 и G28 с составом 9+1+2 сохранены. R28A/R28B зарегистрированы как архивные композиционные помощники, без добавления к рабочим слотам и без owner approval. A3/B3 ждут C28 из реального чистого результата части 2. C28 не рисовать вручную.

Статусы технического результата, slow и редакционная приёмка независимы. Старые редакции/копии не переопределяют GitHub. Порядок одного писателя и проверки публикации — по свежим инструкциям; глобальная оптимизация остаётся на отдельное решение владельца.


### Сцена63 ·25.10.2026
Три новых кадра храма сохранены в `references/scenes/scene-63/`; точный лист Серёги — четвёртый вход. Галерея, портрет/восхищение, тронный зал. Визуально проверены каменный материал статуй и единственный живой герой.30с готова без чужого видео; P2 альтернативы ждёт свою P1. Публикация через master-gallery и общий экран изображений Серёгиуса.
