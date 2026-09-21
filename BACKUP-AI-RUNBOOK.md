# BACKUP-AI-RUNBOOK v4.0 — резервный редактор AI Film

**Дата актуализации:** 20.09.2026  
**Назначение:** правила безопасного takeover для нового/резервного ИИ.

## 1. Нельзя начинать с редактирования

Новый агент сначала читает **все семь** обязательных документов:

1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

Затем:
- fresh exact Drive `video-prompts.md`;
- live `project-status.json`;
- live `topview-status.json`;
- live `instruction-sync-status.json`;
- при story/editing — `film-analysis.md`, `film-backlog.md`, затем релевантный Notion `Кино`.

Только после этого takeover считается завершённым.

## 2. Capability preflight

Перед записью агент должен доказать, что конкретное окружение умеет:

1. читать exact Drive master ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`;
2. писать обратно в **тот же file ID**;
3. читать/писать repo `virudik/ai-film-prompts`;
4. обновлять `SYNC-TRIGGER.txt`;
5. проверять Actions/status/Pages.

Для instruction maintenance также нужны:
- read/write exact seven Drive instruction IDs;
- exact GitHub mirror update;
- проверка `instruction-sync-status.json`.

Если same-ID Drive write недоступна — агент **review-only**. Он не создаёт новый master и не притворяется, что запись выполнена.

## 3. Источник истины

Drive:
- prompt master;
- seven canonical instruction/recovery docs.

GitHub:
- mirrors;
- Control Center;
- machine status;
- Pages.

Notion:
- story/ideas/history.

Library:
- recovery mirror/cache.

Topview:
- telemetry.

Supabase:
- comments backend.

Ни один из последних пяти не становится prompt master.

## 4. Правила master

- stable Scene IDs;
- deleted IDs never reused;
- no `v2/final/copy`;
- fresh-read before write;
- minimal edit;
- same Drive ID;
- update TOC/count/meta consistently;
- no automatic slow rerun;
- Topview success != approval;
- `NEEDS_FIX` != permission to rewrite everything.

Если следующий Scene ID однозначно вычисляется по fresh master, новый чат сам выбирает следующий unused stable ID и **не задаёт лишний вопрос пользователю**.

## 5. Правила prompt-writing

Перед новым/существенным prompt:
- fresh-read `PROMPT-STYLE-GUIDE.md`;
- fresh-read master;
- inspect 1–2 current similar scenes.

Новый prompt должен соответствовать master-level сложности, а не быть коротким generic описанием.

Обязательные типовые элементы:
- exact refs / identity priority;
- story flow/timeline;
- camera/continuity;
- performance;
- dialogue/vocal/lip sync;
- lighting/material/environment;
- native audio;
- scene-specific negative prompt;
- `FRAME FILL / NO BARS`.

Approved model sheet сильнее случайного frame similarity.

## 6. Routine write procedure

`fresh-read`
→ `minimal same-ID Drive edit`
→ `SYNC-TRIGGER.txt`
→ `sync-from-drive.yml`
→ `validation`
→ `GitHub mirror`
→ `project-status.json`
→ `Pages`
→ `verification`
→ `report`

Не говорить `ГОТОВО` до relevant verification.

## 7. Seven-document instruction maintenance

Canonical set:
- `NEW-CHAT-HANDOFF.md`
- `SYNC-RUNBOOK.md`
- `AI-PROJECT-GUIDE.md`
- `PROMPT-STYLE-GUIDE.md`
- `USER-GUIDE.md`
- `README-AI-SYNC.md`
- `BACKUP-AI-RUNBOOK.md`

Drive authority → GitHub mirror.

`instruction-sync-status.json` должен проверять все семь.

Автоматический repair:
Drive → GitHub only.

Нельзя автоматически:
GitHub → Drive.

## 8. Material Change Duty

Если агент внедрил постоянное нововведение:
- функцию сайта;
- новый backend;
- новый prompt rule;
- новый sync/recovery behavior;
- новый source-of-truth rule;
- новый status;

он обязан **в том же сеансе**:
1. обновить релевантные canonical Drive docs;
2. обновить SAME handoff;
3. обновить prompt guide, если применимо;
4. синхронизировать GitHub mirrors;
5. refresh instruction status;
6. проверить site/status;
7. обновить Notion operational pointer;
8. обновить Library recovery copies.

Изменение кода без документации не считается законченным.

## 9. Control Center current baseline

Сайт уже умеет:
- active scenes/full prompts;
- merged slow/Topview;
- sync lightsaber;
- references;
- theme light/dark;
- `Контрольный отпечаток`;
- отдельную collapsible секцию `💬 Комментарии, идеи и предложения` сразу ниже;
- Supabase comments/replies без GitHub login.

Старой кнопки `Архив GitHub` нет.

Комментарии:
- Supabase `ai-film-comments`;
- ref `vzohfatqzyioydtgjiyd`;
- Edge Function `submit-comment`;
- RLS + honeypot + 5 messages/10min/IP;
- no admin/service secret in public HTML;
- no master mutation rights.

## 10. Site-only edit procedure

Править `index.html` в GitHub.

После:
- JS syntax check;
- duplicate IDs;
- secret scan;
- Pages verification.

Scene/prompt data нельзя hard-code в HTML.

Если site change становится постоянным — выполнить Material Change Duty.

## 11. Topview safety

Canonical slow = fresh `project-status.json.slow_scenes`.

Task mapping:
- exact task;
- full current scene semantics;
- model/reference match;
- `verified=true` only when proven.

Passive telemetry never:
- approves;
- clears slow;
- edits master;
- reruns automatically.

Отдельная `Topview Scene Intake & Slow Watch` имеет узкое write-исключение: genuinely new scene import и добавление existing Scene ID в canonical slow при доказанном newly discovered existing-scene render/retry. Это не разрешение approve/delete/slow-clear/rerun.

## 12. Recovery known issues

- concurrent GitHub writers → use fresh origin/rebuild/retry;
- BOM → master UTF-8 without BOM;
- stale instruction status → refresh verification;
- historical checkpoint conflicts → do not treat as live;
- stale Topview mapping → compare against fresh canonical scene body;
- old GitHub failure email → compare timestamps with newer success/live status.

## 13. Notion / Library

Notion:
- use for story/ideas/history;
- operational page `AI Film — Актуальная инструкция / Handoff`;
- `Важные промты` is legacy bank.

Library:
- recovery mirror/cache;
- keep current copies of seven docs + recovery summary/status;
- never prefer Library over accessible Drive.

## 14. Правило поведения сменщика

Если ответ есть в canonical docs/status:
- не спрашивать пользователя повторно;
- не импровизировать другую архитектуру;
- не перекладывать ручную работу на пользователя, если есть инструменты;
- продолжать с текущего состояния;
- при ограничении инструмента честно указать конкретный недоступный шаг.

Цель takeover: пользователь должен иметь возможность сказать только новую творческую/рабочую задачу, а сменщик уже знает инфраструктуру и процесс.

## 15. Character registry и монтажный контекст до takeover

До вступления в роль резервный агент обязан открыть `references.html`, прочитать `character-references.json` и сопоставить глобальные имена/aliases/model sheets с current master. Пользователь имеет право называть персонажей коротко по именам; агент должен сам восстановить identity/appearance/costume/reference mapping.

Также до takeover открыть `Seregius_montazhny_razbor.html` и сверить его с `film-analysis.md` + `film-backlog.md`. Извлечь compact working map фильма и текущих сюжетно-монтажных проблем.

Approved individual model sheet outranks group/environment similarity. Current master outranks stale scene-usage metadata. Если имя реально ambiguous — спросить; иначе не перекладывать повторное описание на пользователя.

## 16. Readiness gate резервного редактора

Перед `готов продолжать` выполнить cross-layer audit: Drive canonical docs/master → GitHub mirrors/status/site → references → montage sources → Notion operational pointer → Library recovery. Безопасный documentation drift исправить согласно authority. Не менять story/master/approval на основании audit без пользовательского решения.

## 17. Topview task-intake awareness

Резервный агент должен знать, что automation `Topview Scene Intake & Slow Watch` имеет два ограниченных write-права:
1. создавать новую Scene ID из genuinely new Topview video task;
2. привязывать newly discovered task к **существующей active canonical scene** и добавлять этот existing Scene ID в canonical slow, если task queued/running/init/processing и match доказан.

Existing-scene match считается доказанным только при exact/normalization-equivalent canonical prompt или explicit provenance; допустимы лишь несемантические различия `@image` ↔ `<<<Image>>>`, whitespace/line endings/reference-token formatting плюс совместимые model/duration/references. Общая semantic similarity не даёт права ни привязать, ни тихо проигнорировать task.

Правила:
- known task ID → не новый intake;
- existing-scene retry/replacement → новый Scene ID не создаётся, task mapping обновляется, running → existing Scene ID slow;
- genuinely new task → actual prompt сохраняется verbatim, новый ID только после fresh master;
- technical `success` ≠ APPROVED;
- ambiguous task → no write, ask/notify;
- no auto-rerun/delete/slow-clear;
- после canonical write обязателен normal sync/validation/Pages/task mapping.

При recovery обязательно проверять, что одна Topview task не импортирована дважды и что newly launched retry существующей сцены не был ошибочно отброшен как «семантически похожий» без task binding/slow update.

## 18. Recovery automation topology

Резервный агент должен ожидать две служебные automation:
1. `AI Film Recovery Sync` — hourly light check, плюс daily deep audit внутри того же hourly schedule по `deep-audit-status.json`;
2. `Topview Scene Intake & Slow Watch` — отдельный production intake/slow watcher.

При takeover проверить `deep-audit-status.json`: когда был последний successful deep audit, какие sections/warnings/unresolved. Старый/missing/failed status означает, что deep audit должен быть выполнен следующим Recovery run или вручную до уверенного readiness report.

## 21. Не путать instruction set с рабочими файлами

В шторке сайта **«Служебные файлы»** ссылок больше семи, но canonical instruction set всё равно состоит ровно из 7 документов. Эти семь кнопок идут вертикально в takeover order 1→7.

Master, film-analysis и backlog вынесены ниже как **рабочие файлы проекта** и также отображаются вертикально один под другим. Резервный агент не должен ошибочно считать их дополнительными инструкциями или искать «лишние копии» seven-document set.

## Canonical Topview state — minimal operational model

This is the permanent Topview rule for the master, watcher, recovery and Control Center:

- **Scene ID** identifies the creative scene. **Topview task ID** identifies one render attempt.
- A rerun/rerender/revised prompt for the same creative scene keeps the same Scene ID.
- Persistent Topview state is intentionally minimal:
  - `topview-task-map.json.active_by_scene` stores only currently active task IDs per Scene ID;
  - `topview-task-map.json.processed_tasks` stores only a bounded recent dedup/statistics journal: `task_id`, `scene_id`, `final_status`, `finished_at`;
  - keep at most the most recent 200 processed tasks and do not persist queue/ETA history or permanent `attempts[]` / `active_attempts[]` trees.
- `SLOW` / `SLOW_PENDING` means that a Topview-managed scene currently has at least one active task in `init`, `queued`, `running` or `processing`.
- A new active task for an existing scene adds/returns that same Scene ID to canonical slow.
- If several tasks of one scene are active, canonical slow still contains the Scene ID once; all active task IDs remain in `active_by_scene`.
- When one task becomes terminal (`success`, `fail`, `failed`, `cancelled`), remove that task ID from active state and append/update the minimal processed journal.
- When the **last Topview-managed active task** for that scene becomes terminal, remove the Scene ID from canonical slow automatically. This changes only render state: **never auto-approve, never auto-rerun, and do not change editorial/production state because rendering ended**.
- Never auto-clear a canonical slow scene when there is no proven Topview active mapping; unknown/manual slow state is not cleared by guess.
- `topview-status.json` stays compact but exposes transient `active_tasks[]`: one telemetry object for every task that is active **right now**. It also keeps the backward-compatible current/primary scene snapshot plus `active_task_ids`. No terminal task history, queue history or ETA history is stored there.
- Control Center slow table deliberately shows **one row per active Topview task / occupied slot**. Therefore the same Scene ID may appear in several rows when it has several simultaneous renders. This is a slot view, not a duplicate-scene model.
- A new Scene ID is created only for a genuinely new creative scene. Ambiguous classification means no master write and user notification.

Principle: **keep only the state required for correctness and deduplication; detailed render history is not a permanent project entity**.

### Точное ТЗ — Topview slow slots, capacity = 6

Это постоянный UI/automation contract:

1. **Ёмкость:** Topview допускает максимум **6 одновременно активных slow-generation tasks**. `slot_capacity = 6`.
2. **Что занимает слот:** каждый отдельный Topview `task_id` в состоянии `init`, `queued`, `running` или `processing` занимает **ровно 1 слот**.
3. **Scene ID и слоты — разные счётчики:** canonical `slow_scenes` остаётся множеством уникальных Scene ID без дублей. Число slow Scene ID **нельзя** использовать как число занятых слотов.
4. **Повторный запуск той же сцены:** если одна Scene ID одновременно запущена 2–3 раза, она остаётся одной canonical scene, но занимает 2–3 Topview slot и должна появляться 2–3 отдельными строками в slow-таблице сайта.
5. **Заголовок сайта:** справа от `⏳ Сейчас в медленной генерации — Topview` показывать только динамический счётчик занятых слотов:
   - `занято X из 6`
   - `X` = количество реально активных `task_id`.
   - Не выводить в компактной шапке `свободно Y` и время последней синхронизации.
   - `free_slots` и `checked_at` остаются допустимыми внутренними telemetry/diagnostic полями, но не являются частью заголовка.
   При текущих шести active tasks ожидаемый вид: **`занято 6 из 6`**.
6. **Таблица:** одна строка = один active `task_id` = один занятый slot. Сохраняются прежние 8 колонок и их базовые пропорции: `#`, `Сцена`, `Модель`, `Статус`, `Запуск`, `Прошло`, `Очередь`, `Оценка времени`. Новую колонку `Attempt`/`Task ID` не добавлять. Если Scene ID повторяется, номер и название сцены повторяются в нескольких строках.
7. **Telemetry:** `topview-status.json` должен содержать:
   - `slot_capacity`;
   - `occupied_slots`;
   - `free_slots`;
   - transient `active_tasks[]`, где на каждый активный task есть как минимум `scene_id`, `task_id`, `model/model_id`, `topview_status`, `started_at`, `checked_at`, `queue_count`, provider wait/process estimates и verification/mapping confidence, если известны.
8. **Точность строки:** queue/ETA/status/start time каждой строки берутся **только из того task_id, которому принадлежит эта строка**. Не усреднять и не переносить очередь/ETA между параллельными попытками одной сцены.
9. **Primary scene snapshot:** scene-level поля в `topview-status.json` можно сохранять для обратной совместимости/других частей сайта, но они **не являются источником slot-count** и не заменяют `active_tasks[]`.
10. **Завершение:** terminal task (`success`, `fail`, `failed`, `cancelled`) немедленно перестаёт занимать slot и удаляется из `active_tasks[]`/`active_by_scene`. В minimal `processed_tasks` можно оставить только дедуп-факт.
11. **Slow lifecycle:** если у Scene ID остаётся хотя бы один active task, Scene ID остаётся canonical slow. Если завершается последний Topview-managed active task, watcher снимает только render slow-state; approval/editorial/production state не меняются автоматически.
12. **Over-capacity guard:** если из-за race/provider anomaly `occupied_slots > 6`, не скрывать проблему: показывать фактическое `занято X из 6`, считать это warning и уведомлять пользователя/аудит.
13. **Никакой тяжёлой истории:** это правило не возвращает старую permanent `attempts[]` модель. `active_tasks[]` содержит только текущие активные задачи; после terminal state подробная telemetry не хранится бессрочно.
14. **Recovery/audit:** при проверке сайта и Topview state отдельно сверять `occupied_slots == len(active_tasks[]) == sum(len(active_by_scene[scene]))` и `free_slots == max(0, 6 - occupied_slots)`. Не сравнивать `occupied_slots` с количеством уникальных `slow_scenes`.


### Recovery check: автономность prompts

При восстановлении/передаче проекта проверять `PROMPT-STYLE-GUIDE.md`: каждый новый автономный production prompt должен содержать собственный short `CHARACTER APPEARANCE / IDENTITY LOCK`. Если prompt зависит от внешнего `shared block above`, это drift от действующего стандарта и требует исправления в master, а не просьбы пользователю вручную доклеить описание.

### Recovery: prompt-quality contract

При takeover/recovery считать fresh `PROMPT-STYLE-GUIDE.md` единственным стилевым стандартом. Проверять prompt semantically: self-contained copy-paste block, real appearance/identity protection, reference ownership/priority, feasible timing, coherent camera/continuity, risk-oriented negatives, no excessive duplication. Не восстанавливать старые полнотекстовые examples как canonical truth. Topview runtime/slot contract проверять по `SYNC-RUNBOOK.md`, не по prompt guide.
