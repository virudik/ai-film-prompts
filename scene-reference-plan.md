# Scene Reference Pack Plan — AI Film Серёгиус

Обновлено: 2026-10-08T09:58:58.592675Z

15 типизированных манифестов; 46 автономных привязок промтов, включая 20 вариантов Scene 28. Это индекс референсов, не новый канон и не разрешение на генерацию. Свежий Drive master остаётся авторитетным.

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

| Сцена | Промтов | Референсов | Остаток |
|---|---:|---:|---|
| 10 | 1 | 4 | New identity-locked three-shot image generation was blocked by the image tool; exact original three source inputs are saved and usable. |
| 11 | 1 | 4 | New identity-locked three-shot image generation was blocked by the image tool; exact original three source inputs are saved and usable. |
| 13 | 1 | 6 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 16 | 1 | 6 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 17 | 1 | 7 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 19 | 1 | 5 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 20 | 11 | 5 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 21 | 1 | 4 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 22 | 1 | 2 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 23 | 1 | 4 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 24 | 1 | 4 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 25 | 1 | 4 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 26 | 1 | 4 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 27 | 3 | 6 | Обязательные референсы сохранены; редакционная приёмка видео отдельно. |
| 28 | 20 | 21 | C28 is intentionally deferred until a clean frame from generated part 2 exists. Unlimited submit route still needs verified access. |

В каждом MANIFEST.json: identity/location/prop, start/end, helpers, owner approval отдельно от assistant QC, historical Topview provenance, локальные слоты каждого промта, SHA-256 и известные ID. null означает отсутствие доказанного ID, а не готовый файл.

Scene 16: оба точных видео сохранены в Drive и Library, Video1 — второй ролик. Чистая локация является реконструкцией кадра около 14 секунд. Scene 17: существующий Drive Video1 сохранён в Library без дублирования в Drive; Video2 остаётся необязательным и непривязанным.

Scene 28: A1/A2 подготовлены; A3/B3 ждут C28 из чистого результата A2. C28 нельзя рисовать вручную. Платный запуск запрещён.

Scene 10/11: три оригинальных входа доступны; отклонённый инструментом дополнительный three-shot не создан и не обходится. Для Scene 26 не прикреплять Серёгу.

Сохранение нового полезного кадра до следующей генерации, exact same-ID canonical guard, 7/7, один монитор и порядок синхронизации остаются без изменений. Оптимизация только в отдельном предложении.
