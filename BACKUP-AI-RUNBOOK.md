# BACKUP-AI-RUNBOOK v5.1 — резервный редактор и резервные копии AI Film

> **23.10.2026 — точные статусы и отпечаток.** Готовность показывать по каждой части: слот / исходный результат / подготовка и QC стыка / отдельный референс / решение владельца. Существующий робот строит `ops/queue-readiness.json`; success не делает вход готовым. Сайт обновляет также master/status/сертификат, сохраняя черновики. Процедура и источники — `ops/QUEUE-READINESS.md`. Новая62 — мост к червям; кабина37/39/40/41/52/53/59/60 — очищенный `S37-cockpit-empty.png`, без людей и мечей.

**Назначение:** порядок ведения резервных копий канона и восстановления по ним; что должен знать новый или резервный ИИ перед takeover. Это единственный дом правил о копиях; остальные правила — по ссылкам.
**Редакция:** 18.10.2026 — убраны повторы с другими инструкциями (одно правило — одно место); генеральная зачистка 11–14.10.2026 до этого. Прежние тексты — `git log` и `archive/instructions-before-cleanup-2026-10-14/BACKUP-AI-RUNBOOK.md`.

> **Источник истины (решение владельца 11.10.2026, 03:25 МСК).** Канон один — GitHub `virudik/ai-film-prompts`, ветка `main`: `video-prompts.md` и ровно 7 инструкций. Всё остальное — резервные копии только для чтения: Google Drive, Notion-указатель, файлы Claude Project, файлы ChatGPT Project, Library. Копию никогда не правят вместо канона и она никогда не переопределяет `main`. Этот документ регулирует **только** резервирование и восстановление; процедуры записи — `SYNC-RUNBOOK.md`.

## РЕЗЕРВНЫЕ КОПИИ КАНОНА — кто и когда обновляет (решение владельца 11.10.2026, 03:46 МСК)

Копии обновляются периодически и автоматически; опоздание копии ничего не ломает. Копии не должны отставать от `main` больше чем на 48 ч. Автоматическое направление копирования — только **из `main` в резервные копии**, никогда обратно в канон: ручная правка копии переносится в `main` явно (или согласуется с владельцем).

| Копия | Кто | Когда | Как |
|---|---|---|---|
| Google Drive «AI Film Prompts Master» (те же file ID) | **Робот GitHub — основной путь** (`drive-write.yml` «Drive copy refresh», `scripts/drive_write.py`; бесключевой вход Workload Identity Federation) | ежедневно 03:20 UTC (06:20 МСК; cron `20 3 * * *` — расписание GitHub может опаздывать на часы) | точные копии из `main` — master, 7 инструкций, `film-backlog.md`, `film-analysis.md` — только если sha отличается и файл на Drive равен одной из прошлых версий в git; вручную правленный файл не затирается (issue `drive-drift`); read-back sha; затем `cert_github.py . --drive-copy-dir` и коммит. Без переменных GitHub `GCP_WORKLOAD_IDENTITY_PROVIDER` и `GCP_SERVICE_ACCOUNT` — чистый no-op `not_configured` (настройка — `ops/DRIVE-WIF-SETUP.md`) |
| то же | **ChatGPT** — запасной путь, когда у него есть пишущая задача или рабочий чат (с 11.10 его единственная задача — только чтение) | суточно / в рабочем чате | Drive-коннектор: файлы, чей sha отличается от `main`, перезаписать точной копией из `main` в тот же файл Drive (file ID не меняются); перед записью убедиться, что файл на Drive совпадает с одной из прошлых версий в git (иначе его правили вручную — не затирать, перенести правку в `main` или спросить владельца); read-back; `cert_github.py . --drive-copy-dir <скачанные копии>` и коммит |
| то же | **Claude** — запасной путь, если робот сломался | в рабочем чате, если копия отстаёт от `main` (ежевечернее обслуживание 21:40 МСК выключено) | по одному файлу, сразу проверка размера (обрезанную запись перезаписать), read-back Drive-коннектором, `cert_github.py` |
| Файлы Claude Project (claude.ai) | Claude собирает комплект, владелец загружает (из облачной сессии файлы проекта недоступны) | при материальных изменениях канона, best-effort (ежевечернее обслуживание 21:40 МСК выключено) | `python3 scripts/build_project_files.py . <папка>` → 22 файла: `00-START-HERE.md`, `CURRENT-STATE.md` (= верхние блоки хендофа), `TAKEOVER-BRIEF.md` (D7), `CHARACTERS.md`, 7 инструкций, `video-prompts.md`, `film-analysis.md`, `film-backlog.md`, `model-sheets/*.jpg`; старые файлы проекта удалить, загрузить новые целиком; эти же файлы годятся для ChatGPT Project |
| Notion «🧭 AI Film — Актуальная инструкция / Handoff» (страница `3e1fe763-7762-81d5-8c4e-dce504d7c5ec`) | агент, внёсший изменение (Claude / ChatGPT) | best-effort при материальных изменениях | Summary + верхний блок-указатель |
| Файлы ChatGPT Project и Library | ChatGPT | суточная проверка ChatGPT | best-effort; если Library требует интерактивного разрешения — пометить stale и продолжить (`SYNC-RUNBOOK.md` «LIBRARY RECOVERY») |
| MP4 готовых роликов Topview — приватная папка Drive `AI Film Prompts Master / AI Film Generated Videos / Scene-NN` (не канон) | Робот GitHub (`topview-video-archive.yml`, `scripts/topview_video_archive.py`) | запуск снаружи — Supabase pg_cron каждые 10 мин (:05/:15/…, `ops/ROBOT-TRIGGER.md`); расписание GitHub — запасное | только успешные задачи **активных** сцен с доказанной привязкой Scene↔task; см. «MP4-архив роликов Topview» ниже |

**Состав копии Library** (best-effort): 7 инструкций, `READ-FIRST.txt`, `CURRENT-STATE.json`, `SITE-STATUS.md`, `SHIFT-HANDOFF.md` и recovery ZIP / summary / status, если он поддерживается как актуальный пакет; recovery-пакет указывает `main` и иерархию живых источников; копия никогда не переопределяет `main` и не предпочитается канону.

Свежесть Drive-копии видна в `instruction-sync-status.json` (поля `drive_copy_*` — информационные; сам сертификат GitHub-канонический: `python3 scripts/cert_github.py .`) и по issue `drive-drift`. После свежих коммитов инструкций Drive-копия может быть stale — это не неисправность канона; после суточного копирования проверить `drive_copy_match` и сертификат, а не делать выводы по старому timestamp. Если один агент выбыл (лимит), Drive-копию подхватывает другой при ближайшем обслуживании; Project files и Library каждого агента обновляет только он сам.

**Идентификаторы Drive (только для обновления копий).** Папка «AI Film Prompts Master» — `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`. Файлы:
- `video-prompts.md` → `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`
- `NEW-CHAT-HANDOFF.md` → `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- `SYNC-RUNBOOK.md` → `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `AI-PROJECT-GUIDE.md` → `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `PROMPT-STYLE-GUIDE.md` → `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`
- `USER-GUIDE.md` → `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` → `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `BACKUP-AI-RUNBOOK.md` → `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`
- `film-backlog.md` → `1YixC7zQFY7z3Bn1XGXxeQIMema3inCT9`; `film-analysis.md` — по точному имени в папке.
- Рабочая папка референсов «Scene Reference Packs» — `16LjAT7YkVGMAc1xw0WkjgGDYbAejzJNI` (копии и обменный канал изображений от ChatGPT; не канон).

### MP4-архив роликов Topview (с 13.10.2026)

Готовые ролики Topview робот GitHub копирует в приватную Drive-папку `AI Film Prompts Master / AI Film Generated Videos / Scene-NN` (файл `<Topview task ID>.mp4`); как работает копирование — `SYNC-RUNBOOK.md` «Автоархив готовых Topview MP4 в Drive». Это резервная копия результатов генерации, а не канон: ни master, ни статусы из неё не восстанавливаются; заархивированный ролик — не одобренная сцена. Индекс — `topview-video-archive.json` (Drive file ID, размер, MD5, SHA-256, без подписанных URL). Восстановление: найти запись по task_id, открыть `drive_url` под аккаунтом владельца. Нельзя делать папку публичной, выдавать права извне или править файлы вручную; пул слотов-заглушек пополнять только через Drive владельца, ключи и IAM не трогать.

### Архив в репозитории

Текст, убранный из инструкций при генеральной зачистке, не потерян: полные копии 7 инструкций до зачистки 14.10 — `archive/instructions-before-cleanup-2026-10-14/`, старые файлы корня (V3.5, предложение по оптимизации, снимок восстановления 08.10) — `archive/old-root-files/`, описание — `archive/README.md`; всё прочее — `git log`. Архив — не канон: нужный абзац возвращают в инструкцию обычной правкой (коммит → `python3 scripts/cert_github.py .`).

Никаких `v2`, `final`, `copy` вместо файлов канона. Ключи и токены не собирать в чат, копии, backup или Notion; JSON-ключи Google запрещены политикой организации и не создаются.

## 1. Takeover резервного ИИ — нельзя начинать с редактирования

Резервный агент проходит тот же приём смены, что любой новый чат (`AI-PROJECT-GUIDE.md` «Формат takeover и решение D7», §1, §14–17); для восстановления после сбоя — всегда полный приём (все 7 документов из `main`, свежий master, живые статусы, открытые `owner_decisions`). Capability preflight перед записью и review-only при отсутствии записи — `SYNC-RUNBOOK.md` §1. Правила master — `AI-PROJECT-GUIDE.md` §3; промты — `PROMPT-STYLE-GUIDE.md`; запись, инструкции, материальные изменения, сайт, Topview и мониторы — `SYNC-RUNBOOK.md`. Library и другие копии проверяются как recovery-only кэш: устаревшая копия не блокирует работу и не требует запросов разрешений у владельца.

## 2. Recovery-проверки

- **Свежесть и доказательства** фиксировать раздельно: `project-status.synced_at` и хеш master; `topview-status.checked_at` и идентичность task-map / checkpoint; `instruction-sync-status.checked_at` и blob-сверка 7 из 7; последний успешный артефакт Pages. Время успешной синхронизации или запуска задачи не заменяет `checked_at` Topview.
- **Дрейф Topview-состояния.** Любое расхождение `topview-status.checked_at == task-map.updated_at == task-map.last_scan_at == checkpoint.checked_at`, task IDs, ёмкости, занятых слотов или набора canonical slow Scene ID — основание для восстановления (пороги свежести — `SYNC-RUNBOOK.md` «Валидатор, health и Control Center»). При доступном Topview дрейф устраняется детерминированно: map → публичный статус → checkpoint **последним**, read-back каждой записи, проверка Pages (`SYNC-RUNBOOK.md` «Транзакционный порядок публикации»). При недоступном — сохранить последние подтверждённые данные и отдельно пометить degraded; свежесть простой заменой даты не чинить. Не дублировать часовые сообщения об одном инциденте.
- **Ревизия master.** Не восстанавливать ручную дату ревизии в `video-prompts.md`; проверять `project-status.json.canonical_revision_sha256` + `revision_date` (`SYNC-RUNBOOK.md`, валидатор).
- При восстановлении сайта и Topview-состояния проверять модель состояния, слоты, publish gate, health-домены и ledger по `SYNC-RUNBOOK.md`; review / approve / rerender / удаление / закрытие сцен — только по решению владельца.
- Снимки восстановления сохраняют структуру пакета референсов каждой сцены и различие «принято / отклонено».

## Scene Reference Pack — восстановление

Правила reference-first, QC по одному кадру, save-before-next и контрольных точек — `SYNC-RUNBOOK.md` «Scene Reference Pack automation». Принятый референс хранится в `references/scenes/scene-N/` в `main` (если им реально пользуется сцена) с manifest; рабочие копии пакета — на Drive в «Scene Reference Packs/Scene N — Reference Pack» и в Library `/AI Film/🎬 Серёгиус/Scene Reference Packs/Scene N`. Если Topview — единственный оставшийся источник, точные входные изображения задачи восстанавливаются через мост ниже, а не повторной загрузкой владельцем.

**Topview exact-input binary recovery bridge** (проверен 07.10 на 30 уникальных входах). Когда метаданные задачи Topview дают только S3 / source-пути, а `download_topview_canvas_nodes` возвращает короткоживущие авторизованные URL, точные байты источника можно сохранить без повторной загрузки владельцем:
1. создать / использовать авторизованный Topview Canvas и добавить точные S3-источники входов задачи как media nodes;
2. вызвать действие загрузки Canvas небольшими пачками, чтобы получить свежие авторизованные URL;
3. создать временную Google Slides-колоду по одному пустому слайду на изображение и вставить каждый URL через `createImage`;
4. экспортировать колоду в PPTX и извлечь точные байты из `ppt/media/`;
5. сохранить байты в `references/scenes/scene-N/` (если ими пользуется сцена), в рабочий пакет на Drive и в Library; записать в manifest сцены исходный task ID, роль в Topview (`Image1`, `Image2`…), sha256, ID файлов;
6. подписанный временный URL Topview никогда не публиковать (он истекает); временную колоду удалить.

`CLAUDE.md` — не-канонический bootstrap (`README-AI-SYNC.md` «Claude Code bootstrap adapter»). История решений — `NEW-CHAT-HANDOFF.md` (журнал) и `git log`.