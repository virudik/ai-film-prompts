# NEW CHAT HANDOFF — AI Film Project
**Checkpoint: 19.09.2026**


Этот файл — переходная точка для следующего чата. Он не заменяет fresh-read master/status.


## 1. Что новому ChatGPT проверить в первую очередь


До любых изменений:


1. Прочитать этот `NEW-CHAT-HANDOFF.md`.
2. Прочитать `SYNC-RUNBOOK.md`.
3. Прочитать `AI-PROJECT-GUIDE.md`.
4. Fresh-read Drive `video-prompts.md`, file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`.
5. Прочитать live GitHub `project-status.json`.
6. Прочитать live `topview-status.json`.
7. Прочитать live `instruction-sync-status.json`.
8. Повторить пользователю current fingerprint:
   - revision
   - master SHA
   - scenes/prompts
   - work items
   - slow scenes
   - health
   - instruction sync health
9. Если задача про сюжет/монтаж — `film-analysis.md` + `film-backlog.md`.
10. Только после этого писать.


## 2. Ключевые точки


Drive folder:
`1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`


Drive master:
`1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`


GitHub:
`virudik/ai-film-prompts`


Viewer:
`https://virudik.github.io/ai-film-prompts/`


Handoff Drive ID:
`1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`


## 3. Snapshot на момент передачи


- 17 active scenes
- 20 prompt texts
- W5, W7, W8
- canonical slow list: 2,6,12,14,15,18
- Scene IDs: 1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18


Всегда fresh-check.


## 4. Самое важное safety-состояние


Topview current observed:
- scene 2 task технически `success`
- scene 6 task технически `success`
- canonical master всё ещё содержит scenes 2 and 6 in slow list; это intentional до решения пользователя


Это intentional safety state.
Topview completion не снимает slow-lock автоматически.


Новый чат должен проверить результаты scenes 2 and 6 по отдельности и дождаться решения пользователя для каждой:
- принять;
- доработать;
- оставить;
- перезапустить.


Только после решения обновлять master slow state.


## 5. Что сделано в этом чате


### Control Center


Сделано:
- technical links → `Служебные файлы`;
- technical explanations/status legend → `Контрольный отпечаток`;
- search helper убран;
- advanced filters свёрнуты;
- duplicated status blocks сокращены;
- `17 Сцен` кликабельно ведёт к scene map;
- `20 Промтов` ведёт к full prompts;
- slow count ведёт к slow filter;
- work count ведёт к `Сцены в работе`;
- W5/W7/W8 вернули в обычную масштабируемую таблицу;
- active scene map восстановлена;
- scene 1 navigation conflict fixed;
- dependencies показываются по-русски;
- Topview completion time находится внутри Status;
- Topview sync timestamp справа в header;
- `Очередь Topview` сокращено до `Очередь`;
- per-task queue telemetry исправлена;
- `running`/`processing` → `Выполняется`;
- `init`/`queued` → `В очереди`;
- `success` → `Завершено`;
- `fail`/`failed` → `Ошибка`;
- time estimate оставлена как согласовано: `≈ ... · Topview ... · история ...`;
- button styles/hover выровнены;
- obsolete CSS/renderer частично очищены;
- health ok = green lightsaber `✓ СИНХРОНИЗАЦИЯ В ПОРЯДКЕ`;
- error state = red lightsaber `✕ ОШИБКА СИНХРОНИЗАЦИИ`;
- рукоятка увеличена;
- анимация меча затем замедлена.


### Slow section


Пользователь запросил короткий heading:
`## ⏳ Сейчас в медленной генерации`


без суффикса `— НЕ ЗАПУСКАТЬ ПОВТОРНО`.


Safety остаётся в slow markers и логике.


### Work notes


Общий development paragraph убран.
W5/W7/W8 notes разнесены в их rows.
Historical W context перенесён ближе к соответствующим active scenes, где уместно.


### References


Сделано:
- cards упрощены;
- repeated priority text убран;
- `Основной референс` — основной label;
- legacy aliases secondary;
- repeated `Нажми на лист...` убрано;
- lightbox fixed;
- 960px previews используются для скорости;
- Drive содержит `reference-originals.zip`;
- Drive также содержит `reference-serega-original.jpg`.


## 6. Что НЕ закончено / нельзя считать законченным


1. **Scenes 2 and 6 Topview success vs canonical slow.**
   Обе технически завершены, но остаются slow до пользовательского решения по каждому ролику.


2. **Не менять time estimate** без нового запроса.


3. После крупных instruction changes Drive originals остаются каноном. Hourly `AI Film Recovery Sync` автоматически ремонтирует exact GitHub mirrors из Drive → GitHub и обновляет проверку; для срочного изменения основной редактор всё равно должен выполнить немедленную сверку, а semantic conflict не исправлять автоматически в Drive.


4. **Следить за concurrent-write recovery.**
   18 сентября были transient падения sync на `git push (fetch first)` из-за одновременных telemetry-коммитов. 19.09.2026 workflow исправлен на fresh-fetch/rebuild/retry; исправление затем подтверждено несколькими успешными sync runs. Последний проверенный status: 19.09.2026 revision, health=ok, instruction_sync=ok, Drive master полностью совпадает с GitHub mirror.


## 7. Как менять master


1. Fresh-read exact Drive master.
2. Не использовать старую GitHub/Library copy как source.
3. Изменить только нужный Scene ID.
4. При необходимости обновить:
   - scene map row
   - full section
   - scene-meta
   - counts
   - slow table/status
5. Save SAME Drive file ID.
6. Update GitHub `SYNC-TRIGGER.txt`.
7. Wait sync workflow.
8. Verify `project-status.json`.
9. Verify Pages.
10. Report exact change.


## 8. Как управлять сайтом


UI:
GitHub `index.html`


References UI:
GitHub `references.html`


Registry:
GitHub `character-references.json`


Site-only changes можно делать прямо в GitHub presentation layer.


После UI change:
1. update exact file;
2. JS syntax check;
3. duplicate HTML ID check;
4. wait Pages deploy;
5. verify conclusion.


Scene/prompt content всё равно меняется только в Drive master.


## 9. Topview telemetry


Automation:
`Topview Slow Watch` — hourly, **только Topview telemetry**. Instruction mirror/recovery checks не дублируются здесь; ими владеет отдельная hourly `AI Film Recovery Sync`.


Rules:
- query exact mapped task per scene;
- no global queue copied to every row;
- Topview read-only;
- success != accepted;
- no automatic slow-lock removal;
- never replace user-confirmed refs from similarity.


## 10. Instruction sync


Canonical Drive instructions:
- AI-PROJECT-GUIDE.md
- SYNC-RUNBOOK.md
- USER-GUIDE.md
- README-AI-SYNC.md
- BACKUP-AI-RUNBOOK.md


Authorized verification compares full text with GitHub mirrors.


Mismatch / repair:
- `instruction-sync-status.json` остаётся `error`, пока расхождение не устранено и не перепроверено;
- если это только exact-text drift GitHub mirror и canonical Drive-файл читается, hourly `AI Film Recovery Sync` может автоматически восстановить **только Drive → GitHub**;
- GitHub → Drive автоматически запрещено;
- semantic conflict, missing/unreadable Drive source или неоднозначность автоматически в Drive не переписывать — сообщить точные файлы и формулировки пользователю;
- после repair выполнить exact-text verification и обновить `instruction-sync-status.json`.


## 11. Confirmed reference identities


- Серёга
- Юля
- Паша
- Артём
- Илюша
- Саша
- Лёша
- Виталик


Natural names should map to these identities; user should not need internal aliases.


## 12. Slow table — уже реализованное решение


Объединение сделано до handoff, несмотря на старую запись обратного:
- на Control Center видна одна таблица `⏳ Сейчас в медленной генерации — Topview`;
- строки определяет canonical `slow_scenes`;
- Topview только добавляет telemetry;
- raw master slow-table скрывается на сайте, но остаётся в canonical Markdown;
- текущее решение оставить как есть, пока пользователь не попросит изменить.


High-resolution references тоже завершены: 19.09.2026 проверены все 8 `references/full/*.jpg` и использование `model_sheet.full_image` lightbox.


## 13. Ready-to-paste command for next chat


> Продолжаем AI Film project. Сначала открой свежий Google Drive `NEW-CHAT-HANDOFF.md`, `SYNC-RUNBOOK.md`, `AI-PROJECT-GUIDE.md` и exact master `video-prompts.md` file ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`. Затем прочитай live `project-status.json`, `topview-status.json`, `instruction-sync-status.json` из `virudik/ai-film-prompts` и повтори текущий audit fingerprint. Не используй старые копии как master. Не меняй Scene IDs. Не перезапускай slow scenes автоматически. Обрати особое внимание: scenes 2 and 6 сейчас Topview success, но canonical slow-lock ещё не снят — сначала проверить каждый результат и спросить решение. Site UI меняется в GitHub `index.html`, scene/prompt content меняется только в Drive master. Slow UI уже объединён — не возвращай устаревшее утверждение, что это только план. Full-res lightbox для 8 model sheets проверен 19.09.2026. Перед `ГОТОВО` проверь sync workflow, validation и Pages.


## 14. Зачем этот handoff


Следующий чат должен за несколько минут понять:
- где истина;
- какие файлы редактируемые;
- как синхронизировать;
- какие UI решения уже приняты;
- какие решения ещё обсуждаются;
- что нельзя автоматически перезапускать или удалять.




## 15. Corrections after takeover — 19.09.2026


Новый чат перепроверил фактическое состояние и исправил расхождение документации с реальностью:
- объединённая slow-таблица уже существовала — зафиксировано как DONE;
- full-res lightbox и 8 public originals уже существовали — зафиксировано как DONE;
- в Drive master добавлен подраздел `Ближайшие направления` с 7 рабочими направлениями дальнейшего производства;
- диагностированы письма GitHub: последние transient failures были non-fast-forward race, а не потеря Drive master;
- `sync-from-drive.yml` усилен fresh-fetch/rebuild/retry;
- Control Center health усилен проверкой freshness и latest public sync workflow;
- любые новые изменения сайта/master после этого checkpoint снова должны отражаться здесь и в canonical instructions.
- Исправлена только служебная подпись scene 18: `Seedance 2.5` → `Wan 3.0`, чтобы она совпадала с scene-meta и фактической Topview task. Prompt body и canonical slow-lock не менялись.


- Takeover incident 19.09.2026: a raw-file rewrite briefly inserted UTF-8 BOM at the beginning of `video-prompts.md`, which made the workflow fail the strict `^#` header check in 4–6 seconds. BOM was removed from the SAME Drive file ID; workflow was hardened to strip optional BOM before validation. Do not interpret those fast runs as Drive/master-content corruption.

## 16. Verified recovery checkpoint — 19.09.2026

- После удаления UTF-8 BOM и добавления encoding guard sync снова проходит успешно.
- Несколько последующих `Sync Drive master and generated project status` завершились успешной публикацией.
- Последний проверенный fingerprint: revision `19.09.2026`, 17 scenes, 20 prompt texts, W5/W7/W8, slow `2,6,12,14,15,18`, health `ok`, instruction sync `ok`.
- Проверенный canonical master SHA-256: `66c0f71841d57dd1f47b731f7f25680053e75040ac4a83962c6cf4e43e821e96`.
- GitHub `video-prompts.md` полностью совпадает с Drive master и содержит раздел `Ближайшие направления` и исправление scene 18 на Wan 3.0.
- Старые письма GitHub `Run failed` до этого checkpoint не считать признаком текущей поломки без fresh-check latest workflow/status.


## 17. Infrastructure/UI update — 19.09.2026

- Automation `AI Film Handoff Refresh` переименована в `AI Film Recovery Sync` и переведена с weekly на hourly.
- Она автоматически чинит пять canonical instruction mirrors только Drive → GitHub, никогда GitHub → Drive, затем делает exact-text verification и semantic consistency check.
- Semantic check обязан ловить stale contradiction `slow tables are planned/not merged` vs фактическое `already merged`, scene 18 engine mismatch, source-of-truth drift, auto-clear slow lock и устаревшие race/BOM rules.
- Control Center получил третий health state: yellow `! БЫЛИ ОШИБКИ СИНХРОНИЗАЦИИ` после восстановленного workflow failure; он держится до 3 последовательных successful sync-runs. Green = stable healthy; red = unresolved/stale/unhealthy.
- Из meta-line удалено дублирующее `N мин назад`, если уже показано точное время.
- Topview `success` при сохранённом canonical slow-lock теперь показывается как `Завершено` / следующая строка `ждёт решения`.
- Проверка slow engines 19.09.2026: 2 Seedance 2.5, 6 Seedance 2.5, 12 Wan 3.0, 14 Seedance 2.5, 15 Wan 3.0, 18 Wan 3.0; master и Topview совпадают по всем six slow scenes. Старое расхождение было только в служебной строке контекста scene 18 и уже исправлено.

## 18. Library / Notion refresh — 19.09.2026

- После infrastructure/UI update свежие Drive-версии пяти canonical instruction files перезаписаны в одноимённые canonical copies ChatGPT Library.
- `NEW-CHAT-HANDOFF.md` также обновлён в Library; старые исторические `*-updated.md`/`video-prompts(n).md` не являются каноном и не использовались как источник.
- В Notion обновлены пять instruction mirror pages из свежих canonical Drive-файлов: External AI / Project Guide, ChatGPT Sync Runbook, User Guide, Sync Rules, Backup AI / Takeover instruction.
- Notion `AI Video Prompts — Master Hub` получил checkpoint 19.09.2026 с hourly Recovery Sync, three-state lightsaber, merged slow UI, `Завершено` / следующая строка `ждёт решения` и scene 18 = Wan 3.0.
- Это documentation/backup refresh; prompt master и production state этим шагом не менялись.

## 19. Hourly automation responsibility split — 19.09.2026

- `Topview Slow Watch`: только per-task Topview status/queue/ETA/result telemetry + защита user-confirmed character references; не читает и не чинит instruction mirrors.
- `AI Film Recovery Sync`: canonical instruction Drive → GitHub mirror repair, exact-text verification, semantic consistency check и material handoff refresh.
- Обе задачи остаются hourly, но больше не дублируют instruction reads/writes; это уменьшает расход connector calls и вероятность concurrent commits.


## 20. Pending infrastructure / site ideas — 19.09.2026

These are **not implemented yet** and must not be reported as completed:
- Personal domain mirror: user wants `рудик.рф/промты` to duplicate the AI Film Control Center. Exact path hosting requires access to the current `рудик.рф` hosting/router (DNS alone cannot route a URL path). A custom subdomain such as `prompts.рудик.рф` would be easier to point directly at GitHub Pages, but user specifically asked about `/промты`; do not change DNS/domain without explicit approval.
- YouTube-free playback for Russian visitors: do not assume a YouTube iframe will work without VPN. For videos the user owns, preferred design is an independent playable copy on storage/CDN or another video host reachable by the target audience, with YouTube kept as an optional secondary source. Do not build a brittle server-side YouTube proxy.
- Personal-site redesign draft exists in ChatGPT Library as `index(1).html`; it is not confirmed as the deployed source of `рудик.рф` and must not overwrite the live site without hosting/source verification.
- Possible future Control Center features: a dedicated `Сейчас` view (blockers + completed renders + W-items) is the strongest candidate; a separate decision queue is partly covered already by `Завершено` / следующая строка `ждёт решения`; `Что изменилось с прошлого sync` is useful but lower priority; generated `workflow-status.json` could remove the browser's dependency on unauthenticated GitHub REST API, but is not necessary while current API usage is low. Avoid feature creep while film work is blocked by story/scene decisions.
- Backup-editor architecture: Claude/Gemini/Grok/DeepSeek capability depends on the actual environment/connectors. A future local deterministic sync helper (`sync-master.ps1`/`.py`) remains a good resilience idea, but is not implemented.


## 21. Final site tidy-up before feature freeze — 19.09.2026

- Резервная инструкция окончательно отвязана от Claude: ссылка называется `Инструкция для резервного ИИ`, технический файл мигрирован на `BACKUP-AI-RUNBOOK.md`, старое Claude-specific имя больше не используется. Любой резервный ИИ обязан пройти capability preflight.
- В slow/Topview таблице успешная task при сохранённом canonical slow-lock теперь визуально показывает `Завершено` и строкой ниже `ждёт решения`; дата завершения остаётся отдельной строкой ниже.
- В `Персонажи / Референсы` порядок изменён минимально: Юля теперь сразу после Серёги; остальные персонажи сохранили взаимный порядок.
- Рукоятка sync lightsaber намеренно НЕ менялась: пользователь попросил сначала показать варианты и выбрать один.
- После этих трёх UI tidy-up изменений сайт считать feature-frozen до нового явного запроса; возвращаемся к работе над фильмом.


## 22. Backup AI filename migration — 19.09.2026

- По явному запросу пользователя Claude-specific техническое имя удалено из активной архитектуры.
- Canonical Drive file ID `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1` переименован в `BACKUP-AI-RUNBOOK.md`; file ID сохраняется.
- GitHub/Pages/Notion/Library/automation links должны использовать `BACKUP-AI-RUNBOOK.md` и human label `Инструкция для резервного ИИ`.
- Предыдущее Claude-specific имя резервной инструкции больше не считать каноническим и не восстанавливать.
- В Topview slow table служебные колонки Model/Status/Start/Elapsed/Queue сделаны compact-width, чтобы не растягиваться шире содержимого.


## 23. Topview nowrap + saber animation clarification — 19.09.2026

- На широком экране Topview table остаётся `width:100%`: compact-width служебные колонки занимают только необходимое, а свободное место получают прежде всего название сцены и ETA; таблица не схлопывается в узкую полосу.
- `Seedance 2.5` / `Wan 3.0` теперь принудительно остаются в одну строку внутри Model cell.
- `ждёт решения` остаётся отдельной строкой под `Завершено`, но сама фраза больше не разрывается на две строки.
- Красный/жёлтый/зелёный sync lightsaber уже используют одну animation family: moving `saberFlow` gradient + state-specific glow pulse. Отдельную новую анимацию текста не добавляли; на красном существующий эффект просто заметнее из-за контраста.

## 23. Validator follow-up after backup-AI rename — 19.09.2026

- После миграции на `BACKUP-AI-RUNBOOK.md` сайт некоторое время корректно показывал красный sync health: новые GitHub workflow действительно падали на validation.
- Причина: `scripts/build_project_status.py` всё ещё содержал старое имя `CLAUDE-TAKEOVER-RUNBOOK.md` в `INSTRUCTION_FILES`, поэтому свежий `instruction-sync-status.json` с пятью `match=true` файлами всё равно интерпретировался как `instruction_sync_error`.
- Validator обновлён на `BACKUP-AI-RUNBOOK.md`.
- Первый sync после исправления успешно завершился commit `72c3e81de429fdf144e263af2e052c4e009cef7a`; свежий `project-status.json`: `health=ok`, `instruction_sync=ok`, warnings пусты.
- По UI-правилу после первого successful run за недавним failure меч должен перейти с красного на жёлтый `! БЫЛИ ОШИБКИ СИНХРОНИЗАЦИИ`; зелёный возвращается после 3 последовательных successful sync-runs.

## 24. Semantic SHA false-positive fix — 19.09.2026

- Hourly `AI Film Recovery Sync` correctly noticed that `SYNC-RUNBOOK.md` still showed an older recovery SHA `861c19e4…` while live `project-status.json` showed `66c0f718…`; exact Drive→GitHub mirrors themselves were matching.
- The stale runbook checkpoint was refreshed to `66c0f718…` and instruction health re-verified.
- More importantly, recovery semantics were hardened: SHA values explicitly labelled as historical/checkpoint snapshots are not live invariants and must not trigger `instruction_sync=error` merely because a later legitimate master edit changes the current SHA.
- CURRENT fingerprint authority is fresh `project-status.json`. Only values explicitly claiming to be current/latest/live should be compared against it as a semantic invariant.

## 25. Future UI idea — режим `Сейчас`

- Статус: **не реализовано; сохранить как будущую идею**. Не внедрять без нового явного запроса пользователя.
- Это дополнительная вкладка/view поверх текущего Control Center, а не замена полного режима. Полный список сцен/промтов/slow/W-items/references остаётся доступным и не урезается.
- Цель: коротко показывать, что требует внимания сейчас. Предлагаемый порядок: (1) пользовательское решение; (2) реальные проблемы/блокеры; (3) уже запущенные slow/Topview задачи; (4) следующее логическое действие из canonical W-items/backlog или явно подтверждённого пользователем приоритета.
- `Сейчас` не имеет права автоматически менять master, Scene IDs, production_state, slow-lock, approval или запускать генерации.
- Технический приоритет должен быть детерминированным по статусам. Творческий/сюжетный приоритет нельзя придумывать самостоятельно: только из канонических W-items/backlog или после явного решения пользователя.
- Реализация в будущем должна по возможности агрегировать уже существующие `project-status.json`, `topview-status.json`, W-items и production state без создания параллельного источника истины.



## 26. Active-status / comments / no-bars update — 19.09.2026

- Fresh Topview telemetry показывает scenes 2 и 6 как `success`; canonical slow list остаётся `2,6,12,14,15,18` до просмотра и решения пользователя. Scenes 12,14,15,18 всё ещё pending.
- Active scene map теперь синхронизирует presentation-status canonical slow-сцен из `topview-status.json`: success = зелёный `✓ ГЕНЕРАЦИЯ ЗАВЕРШЕНА`; init/queued = `⏳ В ОЧЕРЕДИ`; running/processing = `▶ ВЫПОЛНЯЕТСЯ`; fail = `✕ ОШИБКА ГЕНЕРАЦИИ`. Это display-only и не меняет slow-lock/approval.
- Под `🛠️ Сцены в работе` и блоком `Ближайшие направления` добавлен раздел `💬 Комментарии / идеи и предложения`. Backend без отдельного сервера: public GitHub Issue #8. Сайт читает comments через GitHub API; публикация/ответ выполняются в GitHub и требуют GitHub login. Комментарии не являются canonical commands.
- Во все 20 текущих prompt blocks master добавлено одно и то же правило `FRAME FILL / NO BARS`: full-frame edge-to-edge, no letterboxing/pillarboxing/black bars/side bars/decorative borders/empty margins.
- Уведомление Email Monitor о серии старых `Run failed` было ложным как утверждение о текущем состоянии: live `project-status.json` уже был `health=ok` и имел более свежие successful sync. Email Monitor обновлён: для `ai-film-prompts` он обязан сравнивать timestamps и live status перед заявлением, что failure продолжается.
- Предыдущая фраза automation про невозможность обновить same-ID handoff означала сбой/ограничение connector write в том конкретном automation run. Safety-поведение было правильным: GitHub handoff mirror не обновлялся отдельно, чтобы не создать GitHub→Drive drift. В основном чате same-ID Drive write снова доступен; этот handoff теперь обновлён именно в исходном Drive file ID `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`, после чего зеркало должно сверяться Drive→GitHub.
