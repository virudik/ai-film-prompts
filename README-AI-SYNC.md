# README-AI-SYNC v5.1

**Назначение:** карта архитектуры, репозитория и хранилищ AI Film Project: что где лежит, какой workflow что делает. Правила и процедуры здесь не повторяются — они в `SYNC-RUNBOOK.md` и других инструкциях (ссылки ниже).
**Редакция:** 18.10.2026 — убраны повторы с другими инструкциями (одно правило — одно место); генеральная зачистка 11–14.10.2026 до этого. Прежние тексты — `git log` и `archive/instructions-before-cleanup-2026-10-14/README-AI-SYNC.md`.

> **Источник истины:** GitHub `virudik/ai-film-prompts`, ветка `main` (`video-prompts.md` + ровно 7 инструкций); копии только для чтения; свежий `main` побеждает — `SYNC-RUNBOOK.md` (верх).

## Canonical data flow

`video-prompts.md` в GitHub `main`
→ минимальный коммит
→ `SYNC-TRIGGER.txt`
→ workflow `.github/workflows/sync-from-drive.yml` (имя файла историческое, в Actions — «Canonical master check and owner buttons (GitHub main; Drive is only a copy)»; master с Drive он больше не забирает, а собирает статус из `video-prompts.md` в `main`)
→ валидация (`scripts/build_project_status.py`, `health=ok`)
→ сгенерированный `project-status.json`
→ GitHub Pages / Control Center (только чтение).

Единственный master — `video-prompts.md` в `main`. `project-status.json` генерируется и никогда не используется как второй master.

## Seven-document takeover / recovery set

Канон — ровно 7 инструкций, в порядке чтения: `NEW-CHAT-HANDOFF.md` → `SYNC-RUNBOOK.md` → `AI-PROJECT-GUIDE.md` → `PROMPT-STYLE-GUIDE.md` → `USER-GUIDE.md` → `README-AI-SYNC.md` → `BACKUP-AI-RUNBOOK.md`. Когда читать все семь, а когда хватает брифа `shadow/takeover-brief.md` (D7) — `AI-PROJECT-GUIDE.md` «Формат takeover и решение D7». Сертификат 7/7 — `instruction-sync-status.json` (`SYNC-RUNBOOK.md` §8). Тема → инструкция — таблица «Где живёт каждое правило» в `AI-PROJECT-GUIDE.md`.

## Storage roles

Порядок приоритета: **GitHub `main` → Topview (телеметрия) → Notion (сюжет)**; резервные копии ниже и никогда не побеждают `main`.

- **GitHub `virudik/ai-film-prompts`, ветка `main`** — канон: единственный master `video-prompts.md`, 7 инструкций, `index.html` (Control Center), `film.html`, `references.html`, скрипты, машинные статусы (`project-status.json`, `instruction-sync-status.json`, `topview-status.json` и др.), `references/`, `ops/`, GitHub Pages. Второго master нет.
- **Резервные копии (только чтение):** Google Drive «AI Film Prompts Master», Notion-указатель, Claude Project, ChatGPT Project, Library — таблица, расписание и ID: `BACKUP-AI-RUNBOOK.md`. Автоматическое копирование — только из `main` в копии; ручная правка копии (issue `drive-drift`) переносится в `main` явно.
- **Notion** — база `Кино`: сюжет, идеи, старый сценарий, локации, исторические промты; не prompt authority, runtime не определяет. Операционный указатель: `AI Film — Актуальная инструкция / Handoff` (`SYNC-RUNBOOK.md` §12).
- **Topview** — task / model / status / queue / ETA / result (телеметрия, для агентов только чтение). Technical `success` ≠ approval. Генерации — только по команде владельца, безлимитный режим через сайт Topview; MCP / Canvas Topview платные — запрещено.
- **Supabase** (проект `ai-film-comments`, ref `vzohfatqzyioydtgjiyd`, организация `Vint`) — backend комментариев (`submit-comment`) и решений владельца (`owner_decisions`, Edge Function `owner-decision`, исходник `ops/supabase/owner-decision/`) и внешний запуск workflow (pg_cron + pg_net → `workflow_dispatch`, `ops/ROBOT-TRIGGER.md`). Применяют решения только робот / монитор / агент по канону; Supabase не получает прав на master, Scene ID, slow-lock, approval или запуск генераций.
- **GitHub Actions (роботы)** — детерминированные исполнители: телеметрия Topview, кнопки владельца, статус, копия Drive, архив MP4 (ниже).
- **Приватная Drive-папка `AI Film Generated Videos`** — автоархив готовых MP4 (не канон, не approval, `ops/TOPVIEW-VIDEO-ARCHIVE.md`).
- **Референсы** — принятые кадры сцены в `references/scenes/scene-N/` в `main` с manifest (сайт показывает миниатюры `references/thumbs/`); `scene-reference-plan.json` / `.md` — аудит недостающих кадров; рабочие копии пакетов — Drive «Scene Reference Packs» и Library (`BACKUP-AI-RUNBOOK.md`). Референсы не заменяют текст промта и сами не меняют состав сцен.
- **Очередь и задачи** — `ops/topview-launch-queue.json` (очередь бесплатных запусков), `ops/owner-tasks.json` (входящие задачи владельца), `ops/canon-lock.json` (кто сейчас правит канон), `work-resume-register.json` (точка продолжения работы).

## Компоненты и workflow

Workflow (`.github/workflows/`):
- `topview-robot.yml` — робот-писатель телеметрии Topview: `scripts/topview_api_scan.py` (только GET) → `scripts/robot_telemetry.py` (`noop` / `publish` / `hold`) → при необходимости минимальная правка slow-строк master `scripts/master_slow_edit.py` + `SYNC-TRIGGER.txt`. Пишет, только если `monitor-role.json: primary=robot` (`scripts/monitor_role.py --me robot`); аварийный выключатель — GitHub Variable `ROBOT_TELEMETRY=shadow`. Оповещения — issue с меткой `topview-events`. Запуск — `pg_cron` каждые 10 минут, запасное `7,37 * * * *`. Подробно — `ops/ROBOT-TELEMETRY.md`, правила — `SYNC-RUNBOOK.md`.
- `sync-from-drive.yml` («Canonical master check and owner buttons (GitHub main; Drive is only a copy)») — запуск `pg_cron` :02/:12/…, запасное `11,41 * * * *`, push `SYNC-TRIGGER.txt` / `instruction-sync-status.json` / `scripts/build_project_status.py` / самого workflow: статус master (`scripts/build_project_status.py`), `ci-status.json`, свежесть (`scripts/check_public_freshness.py`), сторож `drive-drift`, оповещение `monitor-alert`, job `owner_decisions` — кнопки владельца (`scripts/process_owner_decisions.py`, `scripts/robot_master_actions.py`, `scripts/robot_site_actions.py`).
- `topview-video-archive.yml` + `scripts/topview_video_archive.py` — автоархив MP4 успешных задач активных сцен в приватную Drive-папку через заранее созданные слоты владельца (`topview-archive-seeds.json`; мало слотов → issue `topview-archive-pool`); в git только метаданные `topview-video-archive.json`; `pg_cron` :05/:15/…, запасное `17,47 * * * *`.
- `drive-write.yml` («Drive copy refresh») + `scripts/drive_write.py` — суточное обновление Drive-копий master, 7 инструкций, `film-backlog.md`, `film-analysis.md` (`20 3 * * *` UTC = 06:20 МСК; keyless WIF, без JSON-ключа; без переменных `GCP_WORKLOAD_IDENTITY_PROVIDER` / `GCP_SERVICE_ACCOUNT` — чистый no-op), а также запросы `drive-write-requests/**`; ручную правку копии не перезаписывает, а открывает issue `drive-drift`.
- `canon-health.yml` — ежедневная проверка здоровья канона (`scripts/canon_health.py` → `canon-health.json`, блок «Здоровье канона» на сайте; новое предупреждение = одно письмо владельцу).
- Проверки: `validate-site.yml` («Validate Control Center», `scripts/validate_site.py`), `test-recovery-integration.yml` («AI Film integration recovery tests»), `validate-review-ledger.yml` / `reconcile-review-ledger.yml`.
- Производные: `build-thumbnails.yml` (`scripts/build_thumbnails.py`, миниатюры), `shadow-brief.yml` (`scripts/build_takeover_brief.py`, бриф D7, не канон), `library-snapshot.yml` (экспорт 7 инструкций, master и брифа для Library / Project).
- `projects-sync.yml` («Projects status») — после пуша в `projects/**` пересобирает `projects/<id>/project-status.json` (`scripts/projects.py`) и проверяет реестр проектов; Серёгиус не трогает. Проекты и их правила — `projects/README.md`; сайт переключает проект через `projects.js` (`?p=<id>`); кнопки других проектов — фаза 4 `scripts/robot_project_actions.py` в `sync-from-drive.yml`.
- Только ручные: `topview-api-probe.yml` (проба API, только чтение), `topview-prompt-match.yml` (сверка промтов задач с master, только чтение), `export-handoff.yml` (артефакт handoff).
- Выключенные заглушки (не включать): `build-master.yml`, `finalize-instruction-handoff.yml`, `one-time-sync-instruction-status.yml`.

Внешний запуск, токен и запасные расписания — `SYNC-RUNBOOK.md` «Запуск автоматики снаружи»; SQL без секретов — `ops/supabase/`; справка — `ops/ROBOT-TRIGGER.md`.

Ключевые скрипты: `scripts/cert_github.py` (сертификат инструкций), `scripts/monitor_role.py` (роль писателя: `claude` / `chatgpt` / `robot`), `scripts/monitor_status.py` (честная запись цикла), `scripts/master_scene_edit.py` (правка блока сцены), `scripts/master_slow_edit.py` (минимальная правка slow-меток и таблицы; одна метка на сцену), `scripts/topview_prompt_match.py` (привязка задача → сцена только по точному или нормализованному совпадению промта), `scripts/canon_lock.py` (замок канона), `scripts/continue_preflight.py` (проверка перед «Продолжай»).

## Кнопки владельца

Панель «🔑 Владелец» на сайте → Supabase `owner_decisions` → `sync-from-drive.yml`: фаза 1 «Брак» → `review-ledger.json`; фаза 2 «Принять» / «Переделать» / «В монтаж» → журнал и снятие canonical slow у завершённой сцены, «В фильме» / «Не нужна» / «Не ждать» → master (`ROBOT_MASTER_ACTIONS`, по умолчанию `on`); фаза 3 — очередь запуска, входящие задачи `ops/owner-tasks.json`, отметки референсов. Правила применения — `SYNC-RUNBOOK.md` «Кнопки владельца и задачи текстом»; для владельца — `USER-GUIDE.md` §20.

## Topview flow

`project-status.json.slow_scenes` → точная проверенная задача Topview → `topview-robot.yml` (`topview_api_scan.py` → `robot_telemetry.py`): очередь / статус / ETA по задаче → `topview-task-map.json` → `topview-status.json` → `topview-checkpoint.json` (одним коммитом) → сайт. Правила (slow, слоты, publish gate, привязка задач) — `SYNC-RUNBOOK.md` §10, §18 и «Canonical Topview state».

## Мониторы

Писатель телеметрии один: `monitor-role.json` + `scripts/monitor_role.py` (`primary=robot`, `standby=chatgpt`, монитор Claude выключен; справка — `ops/CLAUDE-MONITOR.md`). Процедура ChatGPT — `ops/CHATGPT-MONITOR-FAST-PATH.md`. Правила — `SYNC-RUNBOOK.md` «Мониторы и расписание».

## Где остальные правила

Master и Scene ID — `AI-PROJECT-GUIDE.md` §3; промты — `PROMPT-STYLE-GUIDE.md`; запись, проверка «готово», материальные изменения, известные сбои — `SYNC-RUNBOOK.md` §1–9, §13–14; сайт, комментарии, служебные файлы, ревизия и свежесть — `SYNC-RUNBOOK.md` §6, §11, §19 и «Валидатор, health и Control Center»; персонажи, монтаж и доклад о готовности — `AI-PROJECT-GUIDE.md` §15–17; референсы — `SYNC-RUNBOOK.md` «Scene Reference Pack automation»; резервные копии и восстановление — `BACKUP-AI-RUNBOOK.md`.

## Claude Code bootstrap adapter

Корневой `CLAUDE.md` — не-канонический bootstrap для Claude Code, а не восьмая инструкция: набор из семи не увеличивает и в сертификат 7/7 не входит (проверяется отдельно как адаптер). Его единственная задача — направить в обычный takeover (7 документов из `main` → свежий `video-prompts.md` → живые статусы); после bootstrap Claude Code восстанавливает состояние из них и не считает локальное состояние репозитория новее `main`. Он остаётся коротким, не копирует тело handoff или runbook и никогда не переопределяет `main`: при конфликте побеждает свежий `main`. Изменение контракта bootstrap документируется в инструкциях и в том же handoff; канонический набор остаётся из 7 файлов. Перед prompt-работой Claude Code, как любой агент, читает `PROMPT-STYLE-GUIDE.md` целиком.