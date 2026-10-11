# README-AI-SYNC v5.0

**Назначение:** краткая карта архитектуры и синхронизации AI Film Project. Пошаговые процедуры — `SYNC-RUNBOOK.md`; здесь только схема и роли хранилищ.
**Редакция:** генеральная зачистка 16.10.2026 (решение владельца 11.10, 05:45); историю хранит git.

> **Источник истины (решение владельца 11.10.2026, 03:25 МСК).** Канон один — GitHub `virudik/ai-film-prompts`, ветка `main`: `video-prompts.md` и ровно 7 инструкций. Google Drive, Notion, Claude Project, ChatGPT Project и Library — резервные копии только для чтения (`BACKUP-AI-RUNBOOK.md`). Свежий `main` всегда побеждает.

## Canonical data flow

`video-prompts.md` в GitHub `main`
→ минимальный коммит
→ `SYNC-TRIGGER.txt`
→ workflow `Sync canonical master` (`.github/workflows/sync-master.yml`)
→ валидация (`scripts/build_project_status.py`)
→ сгенерированный `project-status.json`
→ GitHub Pages / Control Center (только чтение).

Единственный master — `video-prompts.md` в `main`. `project-status.json` генерируется и никогда не используется как второй master.

## Seven-document takeover / recovery set

Канон (в порядке чтения):
1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

Новый чат читает **все семь**, затем свежий master и живые статусы (формат takeover — полное чтение; решение D7 — `AI-PROJECT-GUIDE.md`).

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
- **Topview** — телеметрия генераций (только чтение). Technical `success` ≠ approval.
- **Supabase** — backend комментариев и решений владельца (`owner_decisions`); прав на prompt / master / генерации нет.

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
- slow canonical берётся из master и статуса; новая активная задача Topview возвращает тот же Scene ID в slow; когда терминальной становится последняя активная задача, Topview-managed slow снимается автоматически без approval и смены редакторского статуса;
- Topview success не одобряет сцену;
- текущие счётчики / SHA / slow — из свежего master и статуса, не из исторических документов;
- master — UTF-8 без BOM, только LF;
- глобальное правило промтов `FRAME FILL / NO BARS`, если владелец явно не отменил.

## Control Center baseline

Сайт: `https://virudik.github.io/ai-film-prompts/` (шапка «GitHub main — канон · Pages — только чтение»). Постоянные функции: русский UI; карта активных сцен и полные промты; объединённая таблица slow + телеметрия Topview (статус / модель / запуск / прошло / очередь / ETA); трёхсостоянийный индикатор синхронизации; просмотр персонажей и референсов; светлая / тёмная тема (`ai-film-theme`); сворачиваемый «Контрольный отпечаток»; под ним сворачиваемый «💬 Комментарии, идеи и предложения»; нативные комментарии Supabase без входа в GitHub; панель «🔑 Владелец»; чип «Монитор». Кнопки «Архив GitHub» нет.

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
→ очередь / статус / ETA по задаче
→ `topview-status.json`
→ сайт.

Привязку не угадывать; очередь между задачами не копировать; rerun и approval автоматически не выполнять. Slow canonical должен совпадать в master, `project-status.json` и трёх представлениях Control Center; изменение slow завершено только после этой сквозной проверки (процедура — `SYNC-RUNBOOK.md`).

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

Мониторов два, пишет один (`monitor-role.json`, `scripts/monitor_role.py`). Основной по умолчанию — монитор Claude (`ops/CLAUDE-MONITOR.md`); ChatGPT «резервный контроль» — только чтение, пока владелец не выдал `chatgpt_writer_eligible=true`. Подхват — после 180 мин без здорового полного цикла основного; защита от одновременной записи — 50 мин. Оповещение `monitor-alert` — при молчании цикла больше 3 ч. Раз в сутки — глубокая проверка (`deep-audit-status.json`): полное чтение 7 инструкций, `validate_site.py`, живой сайт, здоровье, дрейф реестра персонажей. Подробности — `SYNC-RUNBOOK.md` («Мониторы и расписание»).

## Slow-state, ревизия и свежесть

- `README-AI-SYNC.md` описывает архитектуру и роли, а не дублирует runbook. Модель состояния Topview, слоты (ёмкость 6), publish gate и пять health-доменов — `SYNC-RUNBOOK.md`.
- `project-status.json.revision_date` вычисляется автоматически из семантического отпечатка master (`canonical_revision_sha256`, технические даты и пустые строки нормализуются): семантическое изменение ставит дату текущей синхронизации (`Europe/Moscow`), иначе дата сохраняется. Ручной даты в master нет.
- `project-status.synced_at` не подтверждает свежесть Topview или сертификата: `topview-status.checked_at` и `instruction-sync-status.checked_at` независимы. Пороги `check_public_freshness.py`: Topview 105 мин, сертификат 165 мин, master-sync 240 мин. Публичный JSON читает независимый read-only checker; запланированного GitHub-watchdog для свежести нет.
- Фильтры Control Center строятся только из актуальных активных сцен, названия — по-русски; одинаковые по смыслу теги объединяются (правила — `SYNC-RUNBOOK.md`).
- Принятые обновления Scenes 26–27: референсы Scene 27 — `@Image1` пара котов, `@Image2` Serega, `@Image3` Luchik, `@Image4` Ryzhik, `@Image5` точная локация руин; Scene 26 — только Лучик и Рыжик, референс Серёги не прикладывается, `@Image4` — локация (точная нумерация всегда из свежего master). Scene 27 — один Scene ID, три production-промта (30s Seedance 2.5 + split 2×15s Seedance 2.0).

## Scene Reference Pack automation

Пакеты референсов — рабочие активы, привязанные к Scene ID. Принятые кадры, которыми пользуется сцена, лежат в `references/scenes/scene-N/` в `main` (сайт показывает компактные миниатюры); рабочие копии пакета — на Drive / в Library (`BACKUP-AI-RUNBOOK.md`). `scene-reference-plan` фиксирует приоритеты внедрения. Референсы не заменяют канонический текст промта и сами не меняют состав сцен. Правила (reference-first, QC по одному кадру, save-before-next, восстановление входов Topview, команда «запускай сцену N» — только по команде владельца, безлимитный режим, кредиты не тратить, контрольные точки) — `SYNC-RUNBOOK.md`.

## Claude Code bootstrap adapter

Корневой `CLAUDE.md` — не-канонический bootstrap для Claude Code: не входит в набор из семи и в сертификат 7/7. Его единственная задача — направить в обычный takeover. Он остаётся коротким и не дублирует handoff или runbook; свежий `main` побеждает.