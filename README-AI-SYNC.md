# README-AI-SYNC v5.0

**Назначение:** краткая карта архитектуры и синхронизации AI Film Project. Пошаговые процедуры — `SYNC-RUNBOOK.md`; здесь только схема и роли хранилищ.
**Редакция:** генеральная зачистка (решение владельца 11.10, 05:45), сверено с `main` на 14.10.2026. Полная версия до зачистки — `archive/instructions-before-cleanup-2026-10-14/README-AI-SYNC.md`; историю хранит git.

> **Источник истины (решение владельца 11.10.2026, 03:25 МСК).** Канон один — GitHub `virudik/ai-film-prompts`, ветка `main`: `video-prompts.md` и ровно 7 инструкций. Google Drive, Notion, Claude Project, ChatGPT Project и Library — резервные копии только для чтения (`BACKUP-AI-RUNBOOK.md`). Свежий `main` всегда побеждает.

## Canonical data flow

`video-prompts.md` в GitHub `main`
→ минимальный коммит
→ `SYNC-TRIGGER.txt`
→ workflow `.github/workflows/sync-from-drive.yml` (имя историческое, в Actions — «Sync canonical master from Google Drive»; master с Drive он больше не забирает, а собирает статус из `video-prompts.md` в `main`)
→ валидация (`scripts/build_project_status.py`, `health=ok`)
→ сгенерированный `project-status.json`
→ GitHub Pages / Control Center (только чтение).

Единственный master — `video-prompts.md` в `main`. `project-status.json` генерируется и никогда не используется как второй master.

`sync-from-drive.yml` запускается push-ем `SYNC-TRIGGER.txt`, внешним `workflow_dispatch` из Supabase pg_cron (:02/:12/…, `ops/ROBOT-TRIGGER.md`) и запасным GitHub `schedule:` (ненадёжен, может опаздывать на часы). Тот же workflow применяет кнопки владельца, ловит ручную правку Drive-копии (issue `drive-drift`) и молчание монитора (issue `monitor-alert`).

## Seven-document takeover / recovery set

Канон (в порядке чтения):
1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

Новый чат принимает смену коротко по брифу `shadow/takeover-brief.md` (решение D7, 14.10.2026) или, при любом триггере, читает **все семь**; затем свежий master и живые статусы. Порядок и триггеры — `NEW-CHAT-HANDOFF.md`, «Приём смены и решение D7».

Поток сертификата инструкций:
файлы в `main`
→ `python3 scripts/cert_github.py .` (git-blob и sha256 каждого файла)
→ `instruction-sync-status.json` (все семь; `source_of_truth=github`)
→ проекция health в `project-status.json`.

Состояние резервных копий в сертификате — справочные поля `drive_copy_*`, они не блокируют.

## Storage roles

- **GitHub `main`** — канон: master, 7 инструкций, Control Center, скрипты, машинные статусы, references, Pages.
- **Резервные копии (только чтение):** Google Drive, Notion-указатель, Claude Project, ChatGPT Project, Library — `BACKUP-AI-RUNBOOK.md`.
- **Notion** — сюжет, идеи, история; не prompt authority. Операционный указатель: `AI Film — Актуальная инструкция / Handoff`.
- **Topview** — телеметрия генераций (только чтение). Technical `success` ≠ approval. Генерации — только по команде владельца, безлимитный режим через сайт Topview; MCP / Canvas Topview платные — запрещено.
- **Supabase** — backend комментариев и решений владельца (`owner_decisions`) и внешний запуск workflow (pg_cron + pg_net → `workflow_dispatch`, `ops/ROBOT-TRIGGER.md`); прав на prompt / master / генерации нет.
- **GitHub Actions (роботы)** — детерминированные исполнители: телеметрия Topview, кнопки владельца, статус, копия Drive, архив MP4 (карта — «Компоненты и workflow»).
- **Приватная Drive-папка `AI Film Generated Videos`** — автоархив готовых MP4 (не канон, не approval, `ops/TOPVIEW-VIDEO-ARCHIVE.md`).

## Компоненты и workflow

Workflow (`.github/workflows/`):
- `topview-robot.yml` — робот-писатель телеметрии Topview: `scripts/topview_api_scan.py` (только GET) → `scripts/robot_telemetry.py` (`noop` / `publish` / `hold`) → при необходимости минимальная правка slow-строк master `scripts/master_slow_edit.py` + `SYNC-TRIGGER.txt`. Пишет, только если `monitor-role.json: primary=robot` (`scripts/monitor_role.py --me robot`); аварийный выключатель — GitHub Variable `ROBOT_TELEMETRY=shadow`. Оповещения — issue с меткой `topview-events`. Подробно — `ops/ROBOT-TELEMETRY.md`.
- `sync-from-drive.yml` — статус master (`scripts/build_project_status.py`), кнопки владельца (`scripts/process_owner_decisions.py`, `scripts/robot_master_actions.py`), свежесть (`scripts/check_public_freshness.py`), `drive-drift`, `monitor-alert`.
- `topview-video-archive.yml` + `scripts/topview_video_archive.py` — автоархив MP4 успешных задач активных сцен в приватную Drive-папку через заранее созданные слоты владельца (`topview-archive-seeds.json`; мало слотов → issue `topview-archive-pool`); в git только метаданные `topview-video-archive.json`. Не канон, не approval, не влияет на slow (`ops/TOPVIEW-VIDEO-ARCHIVE.md`).
- `drive-write.yml` + `scripts/drive_write.py` — обновление Drive-копий master, 7 инструкций, `film-backlog.md`, `film-analysis.md` (keyless WIF; раз в сутки и вручную); ручную правку копии не перезаписывает, а открывает issue `drive-drift`.
- `validate-site.yml` (`scripts/validate_site.py`), `test-recovery-integration.yml` (интеграционные тесты), `validate-review-ledger.yml` / `reconcile-review-ledger.yml`, `build-thumbnails.yml`, `shadow-brief.yml` (`scripts/build_takeover_brief.py`, не канон); только ручные: `topview-api-probe.yml`, `topview-prompt-match.yml`, `export-handoff.yml`, `publish-montage-report.yml`; отключённые наследия: `build-master.yml`, `finalize-instruction-handoff.yml`, `one-time-sync-instruction-status.yml`.

Внешний запуск: GitHub `schedule:` ненадёжен, поэтому Supabase pg_cron + pg_net вызывает `workflow_dispatch`: `topview-robot.yml` — каждые 10 минут, `sync-from-drive.yml` — :02/:12/…, `topview-video-archive.yml` — :05/:15/… Токен — в Supabase Vault; SQL без секретов — `ops/supabase/`; справка — `ops/ROBOT-TRIGGER.md`. Расписания в самих workflow оставлены запасными.

Ключевые скрипты: `scripts/cert_github.py` (сертификат инструкций), `scripts/monitor_role.py` (роль писателя: `claude` / `chatgpt` / `robot`), `scripts/master_scene_edit.py` (правка блока сцены), `scripts/master_slow_edit.py` (минимальная правка slow-меток и таблицы; одна метка на сцену), `scripts/topview_prompt_match.py` (привязка задача → сцена только по точному или нормализованному совпадению промта).

## Кнопки владельца

Панель «🔑 Владелец» на сайте → Supabase `owner_decisions` (Edge Function, исходник `ops/supabase/owner-decision/`) → `sync-from-drive.yml`: фаза 1 «Брак» → `review-ledger.json` (`process_owner_decisions.py`); фаза 2 «Принять» / «Переделать» / «В монтаж» → одновременно журнал и снятие canonical slow у завершённой сцены; «В фильме» / «Не нужна» / «Не ждать» → `robot_master_actions.py` (GitHub Variable `ROBOT_MASTER_ACTIONS`, по умолчанию `on`; `off` — пауза). Решение получает `applied` только после коммита, валидатора и read-back; неоднозначное → `needs_owner`. «В фильме» применяется автоматически. Текстовые задачи владельца (`owner_task`) выполняет агент. Кнопки не запускают генерации.

## Prompt-writing flow

Перед новым или существенно изменённым промтом:
`PROMPT-STYLE-GUIDE.md`
→ свежий master (`git pull`)
→ 1–2 близкие актуальные сцены
→ master-level промт
→ минимальный коммит в `main`
→ sync / валидатор / Pages.

Если следующий Scene ID очевиден из свежего master, редактор берёт следующий новый стабильный ID сам; закрытые ID не переиспользуются. Новую сцену из Topview-задачи заводят только с согласия владельца.

## Master invariants

- единственный master, без дублей и версий `v2` / `final` / `copy`;
- стабильные Scene ID;
- `project-status.json` генерируется, не используется как второй master;
- slow canonical берётся из master и статуса; новая активная задача Topview возвращает тот же Scene ID в slow; терминальная задача освобождает физический слот Topview, но canonical slow снимается **только по явной кнопке владельца**: обработчик кнопок записывает решение и смену slow вместе после подтверждённого завершения; робот телеметрии и монитор сами slow не снимают;
- в карточке каждой canonical slow-сцены ровно одна простая метка `**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**` (14.10.2026); живой статус задачи сайт показывает по телеметрии;
- Topview success не одобряет сцену;
- текущие счётчики / SHA / slow — из свежего master и статуса, не из исторических документов;
- master — UTF-8 без BOM, только LF;
- глобальное правило промтов `FRAME FILL / NO BARS`, если владелец явно не отменил.

## Control Center baseline

Сайт (GitHub Pages, только чтение): `https://virudik.github.io/ai-film-prompts/` (шапка «GitHub main — канон · Drive — копия»). Постоянные функции: русский UI; карта активных сцен и полные промты; объединённая таблица slow + телеметрия Topview (статус / модель / запуск / прошло / очередь / ETA); трёхсостоянийный индикатор синхронизации; просмотр персонажей и референсов; светлая / тёмная тема (`ai-film-theme`); сворачиваемый «Контрольный отпечаток»; под ним сворачиваемый «💬 Комментарии, идеи и предложения»; нативные комментарии Supabase без входа в GitHub; панель «🔑 Владелец»; чип «Монитор»; в карточке slow-сцены метка по живой телеметрии («✅ ГОТОВО — ждёт решения владельца» / «❌ ОШИБКА TOPVIEW — ждёт решения владельца» / «⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ»); ссылки на копии в Drive («💾 Drive N» в таблице slow, «💾 MP4 N» в карточках). Кнопки «Архив GitHub» нет.

Owner-facing контракт слотов, который валидатор и восстановление сохраняют: `M из 6` занятых слотов (ниже `Свободно Y · N сцен`); подробный заголовок `занято M из 6 · свободно Y · timestamp`; карточка рабочих направлений — только число (без `W5…W15`); компактное левое меню (Service Files и Filters свёрнуты, активный фильтр виден); плавающая «↑ Наверх».

## Supabase comments

Организация `Vint`; проект `ai-film-comments` (ref `vzohfatqzyioydtgjiyd`); Edge Function `submit-comment`; публичное чтение опубликованных; анонимная публикация и ответы; RLS; honeypot; лимит 5 / 10 мин / IP; во фронтенде только publishable key; service / admin-секреты не выставляются; комментарии не меняют master.

## Material-change propagation

Постоянное изменение архитектуры сайта, workflow, стандарта промтов, authority, восстановления или модели статуса не завершено, пока не пройдено:
реализация
→ релевантные инструкции
→ тот же `NEW-CHAT-HANDOFF.md`
→ `PROMPT-STYLE-GUIDE.md`, если применимо
→ `cert_github.py` и коммит в `main`
→ проверка статуса / Pages
→ Notion-указатель
→ резервные копии (best-effort, не блокируют; пропускать при интерактивном подтверждении).

Эфемерные очередь / ETA / SHA по всем документам как постоянный текст не размножать.

## Site-only changes

Править `index.html` в `main`. После правки: `scripts/validate_site.py` (синтаксис JS, дубли id, контракты), отсутствие секретов, `tests/site_status_check.js`, Pages. Постоянная функция — ещё и Material-change propagation.

## Topview flow

`project-status.json.slow_scenes`
→ точная проверенная задача Topview
→ `topview-robot.yml` (`topview_api_scan.py` → `robot_telemetry.py`): очередь / статус / ETA по задаче
→ `topview-task-map.json` → `topview-status.json` → `topview-checkpoint` (одним коммитом)
→ сайт.

Привязку не угадывать (неоднозначное — `hold` и сообщение владельцу); очередь между задачами не копировать; запуск, rerun, удаление и approval автоматически не выполнять; кредиты не тратить. Slow canonical должен совпадать в master, `project-status.json` и трёх представлениях Control Center; изменение slow завершено только после этой сквозной проверки (процедура — `SYNC-RUNBOOK.md`).

## Recovery safeguards

- sync-workflow при конкурентных писателях перечитывает `origin/main`, пересобирает и повторяет;
- защита от BOM / CRLF в master;
- проверки свежести живых статусов (`scripts/check_public_freshness.py`);
- исторический снимок ≠ текущий инвариант;
- привязку Topview сверять со свежим телом сцены;
- резервные копии не переопределяют `main`: правка копии, сделанная вручную, переносится в `main` явно.

## Definition of Done

Изменение prompt / master: коммит в `main` + успешный sync + валидатор + текущий статус + Pages.
Изменение инструкций / материальное: все семь файлов в `main` содержат правило + свежий `instruction-sync-status.json` (`cert_github.py`) + Notion-указатель. Резервные копии — best-effort; `pending/stale` завершение не блокирует, если живой канон здоров.
Если какой-то обязательный слой не проверен, сообщить об этом явно, а не заявлять полное завершение.

## Character / film-context flow

Контекст takeover включает два смысловых слоя:
`references.html` + `character-references.json`
→ карта «каноническое имя / алиас / model sheet»
→ сверка со свежим master
→ разрешение имён на естественном языке в новых промтах.

`Seregius_montazhny_razbor.html` (и `-2`) + `film-analysis.md` + `film-backlog.md` + релевантный Notion `Кино`
→ компактная актуальная карта фильма, сюжета и монтажа.

Так следующий чат понимает запросы вида «Паша говорит Саше, потом заходит Серёжа» без повторного описания известных персонажей и понимает монтажную функцию новой сцены.

## Takeover readiness check

До отчёта о готовности агент проверяет актуальность семи документов, master / статусов, сайта, реестра персонажей, монтажных источников и Notion-указателя. Резервные копии — информационно; устаревший кэш не блокирует готовность. Безопасный дрейф документации исправляется по правилам authority; творческие и approval-конфликты требуют решения владельца. Монитор остаётся лёгким: проверяет наличие и целостность этих слоёв и предупреждает о дрейфе, но не перечитывает тяжёлый монтажный HTML и массив изображений каждый цикл.

## Topview task-intake flow

Неизвестная видео-задача Topview:
`unknown video task`
→ уже известный task ID? — это обычная телеметрия
→ совпадение с активным промтом сцены (точное или с точностью до нормализации) либо явное происхождение?
  → привязать к **существующему Scene ID**
  → если queued / running / init / processing — добавить Scene ID в canonical slow
  → редакторский и производственный статус сохранить, дубль Scene ID не создавать
→ явно отличается от активных сцен?
  → совсем новая сцена: сообщить владельцу; новый Scene ID — только с его согласия (решение 10.10), с дословным фактическим промтом задачи
→ неоднозначно?
  → ничего не менять в master, сообщить владельцу
→ `SYNC-TRIGGER.txt` → sync → валидатор → `project-status.json` → Pages → обновление привязки и телеметрии.

Нормализация игнорирует только несемантические различия (`@image` ↔ `<<<Image>>>`, пробелы, формат токенов референсов). Смысловое сходство само по себе не позволяет молча отбросить новую задачу. Technical success никогда не равен approval.

## Service-files UI

В «Служебных файлах» две логические группы: «Инструкции — читать по порядку» (ровно 7 документов, вертикально 1→7) и «Рабочие файлы проекта» (master → analysis → backlog, тоже вертикально). Машинная логика считает размер набора инструкций равным 7 независимо от числа ссылок в UI.

## Мониторы и восстановление

Писатель телеметрии один (`monitor-role.json`, `scripts/monitor_role.py`). С 13.10.2026 (решение владельца) `primary=robot` — GitHub-робот `topview-robot.yml` (`ops/ROBOT-TELEMETRY.md`), `standby=chatgpt`: при здоровом роботе ChatGPT-монитор только читает (`skip`) и сам подхватывает запись после 180 мин без подтверждённого здорового цикла робота, становясь основным; робот возвращается только по команде владельца. Монитор Claude выключен (`ops/CLAUDE-MONITOR.md` — справка). Защита от одновременной записи — 50 мин. Аварийная остановка робота — GitHub Variable `ROBOT_TELEMETRY=shadow` (пишет только `shadow/robot-cycle-preview.json`). Молчание здорового цикла ловит issue `monitor-alert` (`sync-from-drive.yml`). Суточная глубокая проверка (`deep-audit-status.json`) роботом не выполняется. Подробности — `SYNC-RUNBOOK.md` («Мониторы и расписание»).

## Slow-state, ревизия и свежесть

- `README-AI-SYNC.md` описывает архитектуру и роли, а не дублирует runbook. Модель состояния Topview, слоты (ёмкость 6), publish gate и пять health-доменов — `SYNC-RUNBOOK.md`.
- `project-status.json.revision_date` вычисляется автоматически из семантического отпечатка master (`canonical_revision_sha256`, технические даты и пустые строки нормализуются): семантическое изменение ставит дату текущей синхронизации (`Europe/Moscow`), иначе дата сохраняется. Ручной даты в master нет.
- `project-status.synced_at` не подтверждает свежесть Topview или сертификата: `topview-status.checked_at` и `instruction-sync-status.checked_at` независимы. Пороги `check_public_freshness.py`: Topview 105 мин, сертификат 165 мин, master-sync 240 мин. `check_public_freshness.py` вызывается из `sync-from-drive.yml`; отдельного workflow-watchdog свежести нет.
- Фильтры Control Center строятся только из актуальных активных сцен, названия — по-русски; одинаковые по смыслу теги объединяются (правила — `SYNC-RUNBOOK.md`).
- Принятые обновления Scenes 26–27: референсы Scene 27 — `@Image1` пара котов, `@Image2` Serega, `@Image3` Luchik, `@Image4` Ryzhik, `@Image5` точная локация руин; Scene 26 — только Лучик и Рыжик, референс Серёги не прикладывается, `@Image4` — локация (точная нумерация всегда из свежего master). Scene 27 — один Scene ID, три production-промта (30s Seedance 2.5 + split 2×15s Seedance 2.0).

## Scene Reference Pack automation

Пакеты референсов — рабочие активы, привязанные к Scene ID. Принятые кадры, которыми пользуется сцена, лежат в `references/scenes/scene-N/` в `main` (сайт показывает компактные миниатюры); рабочие копии пакета — на Drive / в Library (`BACKUP-AI-RUNBOOK.md`). `scene-reference-plan` фиксирует приоритеты внедрения. Референсы не заменяют канонический текст промта и сами не меняют состав сцен. Правила (reference-first, QC по одному кадру, save-before-next, восстановление входов Topview, команда «запускай сцену N» — только по команде владельца, безлимитный режим, кредиты не тратить, контрольные точки) — `SYNC-RUNBOOK.md`.

## Claude Code bootstrap adapter

Корневой `CLAUDE.md` — не-канонический bootstrap для Claude Code: не входит в набор из семи и в сертификат 7/7. Его единственная задача — направить в обычный takeover. Он остаётся коротким и не дублирует handoff или runbook; свежий `main` побеждает.