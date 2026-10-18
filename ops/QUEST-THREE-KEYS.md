# AI Film «Серёгиус»: робот GitHub и ключи (необязательная оптимизация)

Статус: справка (история ключей и шагов робота; на файл ссылается `USER-GUIDE.md`). Проверено: 18.10.2026.

> **Пересмотрено 11.10.2026, 04:32 МСК.** С 03:25 канон — GitHub `main`, поэтому для работы без компьютера ключи больше не нужны: канон правится коммитами, монитор Claude в облаке читает Topview и Supabase коннекторами. Ключи нужны только для того, чтобы рутину делал **робот GitHub Actions** — бесплатный планировщик в репозитории, скрипты без ИИ: не тратят лимиты подписок Claude/ChatGPT и не зависят от компьютера и чатов. Порядок: **Шаг А — Supabase**, **Шаг Б — Topview** (сначала проба), **Шаг В — Google** (необязательно, последним; **с 11.10 без файла-ключа**, см. ниже). Все три шага построены облачной сессией Claude Code 11.10 — статус в «Флажках прохождения» внизу. Сводка — `NEW-CHAT-HANDOFF.md` «ПЛАН НА БУДУЩЕЕ» п. 3.

**Что робот берёт на себя после ключей:** однозначные кнопки сайта каждые 30 мин (А); проверку Topview каждые 30 мин, если публичный API видит безлимитные доски и 6 слотов (Б) — тогда монитор Claude по решению владельца переходит на редкий режим (раз в 3–6 ч и по событию); обновление Drive-копии (В). **Что остаётся агентам и владельцу:** творческие правки и новые сцены, approval / rerender / закрытие сцен, запуск генераций Topview (безлимит только на сайте под входом владельца), неоднозначности.

**Состояние на 16.10.2026:** все три шага работают — кнопки фазы 2 включены владельцем 12.10, робот пишет телеметрию Topview с 13.10 (основной писатель), Drive-копия обновляется раз в сутки с 11.10. Подробности — «Флажки прохождения» ниже; текущие правила — `NEW-CHAT-HANDOFF.md`, `ops/ROBOT-TELEMETRY.md`. Текст ниже про настройку ключей — история.

## Общая точка назначения

**GitHub:** https://github.com/virudik/ai-film-prompts/settings/secrets/actions

Каждый ключ: **Settings → Secrets and variables → Actions → Secrets → New repository secret**. Указывать имя переменной в поле **Name**, секрет целиком в поле **Secret**, нажать **Add secret**. Никогда не вставлять секреты в репозиторий, Issues, сайт, комментарии, чат, скриншоты или файлы master.

**Важно:** под «тремя ключами» имеются в виду Google service account, Supabase secret, Topview API key. Для Topview дополнительно потребуется **UID** — это идентификатор, не отдельный ключ. Для будущего ИИ-редактора свободных промтов может понадобиться ещё ключ отдельной языковой AI API; для обычных кнопок он не требуется. GitHub автоматически предоставляет `GITHUB_TOKEN` своим Actions — персональный GitHub PAT не нужен.

## Шаг В (необязательно, последним) — Google Drive без файла-ключа (Workload Identity Federation)

> **Обновлено 11.10.2026.** Политика организации Google запрещает JSON-ключи (`iam.disableServiceAccountKeyCreation`) — её не трогаем, ключ `GDRIVE_SA_KEY` **не создаётся**. Вместо него GitHub Actions входит в Google по OIDC (`google-github-actions/auth`, `permissions: id-token: write`) и действует от имени сервисного аккаунта `ai-film-writer`. Нужен только чтобы робот сам обновлял Drive-копию для чтения; канон на Drive не пишется.

Пошаговая инструкция с готовыми командами для Google Cloud Shell: **`ops/DRIVE-WIF-SETUP.md`** (блок команд → доступ «Редактор» сервисному аккаунту только к папке «AI Film Prompts Master» → две переменные GitHub `GCP_WORKLOAD_IDENTITY_PROVIDER` и `GCP_SERVICE_ACCOUNT` → ручной прогон `probe`, затем `sync`). Без переменных `drive-write.yml` — аккуратный no-op `not_configured`. Что делает робот раз в сутки: точные копии из `main` по тем же file ID, только если sha отличается и Drive-файл равен одной из прошлых версий в git (иначе правили вручную — не затирать, issue `drive-drift`), read-back sha, затем `scripts/cert_github.py . --drive-copy-dir <копии>` и коммит.

Официально: https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines ; https://github.com/google-github-actions/auth

## Шаг А (первым) — Supabase: `SUPABASE_SERVICE_ROLE_KEY`

1. Открыть **только свой проект** https://supabase.com/dashboard/project/vzohfatqzyioydtgjiyd/settings/api-keys .
2. Для текущего репозиторного обработчика `scripts/process_owner_decisions.py` готовым вариантом остаётся **Legacy `service_role`** (`eyJ…`). Это привилегированный ключ серверной базы, **НЕ** публичный `sb_publishable_...`, **НЕ** пароль панели `OWNER_DECISION_KEY`. 
3. В GitHub Secrets создать имя **`SUPABASE_SERVICE_ROLE_KEY`** и вставить весь Legacy `service_role`.
4. GitHub workflow `.github/workflows/sync-from-drive.yml` (уже по расписанию `*/30 * * * *`) читает решения владельца, применяет безопасные однозначные кнопки к `review-ledger.json`, проверяет commit и только после него ставит `applied` в Supabase. Следующая фаза — `in_film` / `scene_not_needed` / `tv_drop_task` прямым коммитом master в GitHub `main` (Drive-писатель для этого больше не нужен).
5. **Современный вариант для следующего обновления:** Supabase рекомендует новый `sb_secret_...` вместо Legacy; текущую HTTP-авторизацию обработчика нужно проверить/адаптировать на новый формат перед его подстановкой. Не отключать legacy, пока переход и end-to-end не протестированы.
6. Проверка: создать только контролируемую и безопасную заявку в панели → дождаться запланированного GitHub job (или запустить workflow вручную) → подтвердить status=applied **после** commit и отсутствие изменений чужих сцен.

Официально: https://supabase.com/docs/guides/getting-started/api-keys ; https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys

## Шаг Б — Topview: `TOPVIEW_API_KEY` и идентификатор `TOPVIEW_UID` (сначала только проба)

1. Войти в https://www.topview.ai/ под аккаунтом, где находятся генерации AI Film.
2. На главной странице нажать аватар **в правом верхнем углу** → выбрать пространство/аккаунт → **API Settings → API**.
3. Там отображаются **Topview Uid** и **Key**. Если Key отсутствует, нажать **Add Key**. Это настоящий API key, а не пароль сайта и не OAuth-доступ ChatGPT.
4. В GitHub **Secrets** добавить **`TOPVIEW_API_KEY`** (весь Key без слова `Bearer`). В GitHub **Variables** рядом создать **`TOPVIEW_UID`** с точным Topview Uid. Если хочешь спрятать и UID, можно хранить его также в Secrets — но workflow должен ссылаться на соответствующее место.
5. Проверка только чтением: `GET` к официальному `https://api.topview.ai/v1/tts/list` с заголовками `Authorization: Bearer <TOPVIEW_API_KEY>` и `Topview-Uid: <TOPVIEW_UID>`. Ключи никогда не выводить в лог. Затем попробовать официальный Query Task для *известного* Task ID и оценить, видит ли public API **именно задачи бесплатной очереди досок**, а не отдельную API-генерацию.
6. Для нашего проекта недостаточно просто знать статус одного ролика: нужно подтвердить полный обзор всех досок/задач, `useUnlimitMode`, активные состояния и свободные слоты **из 6**. Если через public API этого нельзя получить, **не публиковать ложное «0/6»**; на сайте показывать «данные Topview не подтверждены» и оставить подключённый Topview-исполнитель до официального поддерживаемого способа.
7. Никаких `POST task/submit`, новых генераций, трат кредитов, автоматических approval/rerender/delete. Topview API-кредиты и условия веб-безлимита могут отличаться; получение Key не означает, что API-запуски бесплатны.

Официально: https://docs.topview.ai/reference/authentication-1 ; https://docs.topview.ai/reference/image-to-video-v2-text-to-video-omni-reference-api-usage ; https://docs.topview.ai/docs/billing-rules

## Итоговый алгоритм (после активации)

**Кнопки и задачи:** сайт `🔑 Владелец` → аутентифицированное решение в Supabase → существующая плановая GitHub Actions (`*/30 * * * *`) → защита от дублей и конфликтов → `review-ledger.json` либо коммит `video-prompts.md` в GitHub `main` → валидатор `health=ok` → Pages → запись `applied` и ссылки на результат. Текстовые творческие правки требуют редакционной модели, style guide, референсов, проверки continuity и явного решения при неоднозначности.

**Видео/медленная очередь:** Topview read-only API → проверка доступного покрытия и соответствия Task ID → карта scene↔task (без угадывания) → `topview-status.json`/сайт **только по реально подтверждённой полной выборке** → «занято N/6, свободно 6-N, время фактической проверки», техническое окончание отдельно от человеческой приёмки. Если API не обеспечивает полноту, источник и возраст данных помечаются, устаревшая статистика не выдается за свежую.

**Мониторы:** задачи Claude и ChatGPT/Work не выключать и не урежать, пока цепочка робота не проверена на реальных данных end-to-end; переход монитора Claude на редкий режим — только решением владельца. Не создавать дубли Recovery / slot watcher. Одновременно master меняет только один разрешённый исполнитель, с CAS SHA/readback.

## Флажки прохождения

- [x] **А (чтение).** `SUPABASE_SERVICE_ROLE_KEY` добавлен владельцем 11.10 06:37 МСК; плановый запуск 03:49Z: job `owner_decisions` без «not configured», шаг успешен — робот читает Supabase.
- [x] **А (E2E).** Первая реальная кнопка владельца → commit робота в `review-ledger.json` → Supabase `applied`: коммит `7024200d` (11.10 23:53 UTC, 15 решений владельца).
- [x] **А+ — ВКЛЮЧЕНО владельцем 12.10.** Фаза 2 по умолчанию `on` (`ROBOT_MASTER_ACTIONS=${{ vars.ROBOT_MASTER_ACTIONS || 'on' }}`), переменная `ROBOT_MASTER_ACTIONS=off` приостанавливает; «🎞 В фильме» применяется автоматически. Первое реальное применение — коммит `db010cf5` (12.10 00:02 UTC, «В фильме» сцен 20, 21, 26, validator health=ok). Исходно построено 11.10: `in_film` / `scene_not_needed` / `tv_drop_task` прямым коммитом master в GitHub: `scripts/robot_master_actions.py` + шаг «Phase 2» в `sync-from-drive.yml`, тесты на фикстурах зелёные (diff master, резервирование ID, конфликты → `needs_owner`, commit-before-ack, гонка push).
- [x] **Б.** `TOPVIEW_API_KEY` (Secret) и `TOPVIEW_UID` (Variable) добавлены владельцем 11.10 06:52 МСК; ключ рабочий.
- [x] **Б+ — положительно (11.10 07:25, исправление первого вывода):** по ссылкам владельца найдены документированные эндпоинты досок — `GET https://api.topview.ai/boards/list` (все 11 досок, `taskCount`, `total`) и `GET /boards/tasks/list?boardId=…&mediaType=video&sortField=gmtCreate&sortOrder=desc` (основная доска: total 391; поля `boardTaskId`, `status`, `useUnlimitMode`, `gmtCreate`, `completedAt`, `parameters`, `errorCode`…). Первые догадки (`/v1/board/...`, task-query API) отвечали 5000/4004 — не те адреса. Очередь/ETA — `GET /boards/tasks/detail?taskId=…` (поле `estimateInfo`: `queueCount`, `estimatedWaitSeconds`, `estimatedProcessSeconds`; найдено в docs.topview.ai/reference, «Get Board Task Detail»).
- [x] **Б++ — робот основной писатель телеметрии с 13.10** (решение владельца: «пускай робот всё делает», без 1–2 дней параллельного прогона). `topview-robot.yml` → `scripts/robot_telemetry.py`, запуск каждые 10 минут снаружи (Supabase pg_cron, `ops/ROBOT-TRIGGER.md`); `monitor-role.json`: `primary=robot`, `standby=chatgpt`; монитор Claude выключен; аварийная остановка — `ROBOT_TELEMETRY=shadow`. Подробно — `ops/ROBOT-TELEMETRY.md`. Исходно 11.10 (теневой режим): `scripts/topview_api_scan.py` + `.github/workflows/topview-robot.yml` (каждые 30 мин): пишет только `shadow/topview-robot-status.json` и сравнивает себя с `topview-status.json` монитора (расхождения — в файл и в notice-аннотацию `topview-robot-shadow`). Первый ручной прогон на GitHub 11.10 10:50 UTC зелёный: живой API подтверждён (11 досок, 560 видео-задач, занято 6/6, 6 новых задач без сцены → `unknown_new`, расхождение с монитором записано в `comparison`).
- [x] **В — РАБОТАЕТ (11.10 14:05 UTC).** Владелец настроил WIF; `probe` и `sync` зелёные: 10 файлов найдены, записано 3 устаревшие копии (`video-prompts.md`, `NEW-CHAT-HANDOFF.md`, `BACKUP-AI-RUNBOOK.md`), остальные 7 уже совпадали, у всех sha Drive = GitHub, ручных правок (drift) нет, сертификат инструкций `drive_copy_match` 7/7. Дальше — само раз в сутки (03:20 UTC; ежедневные коммиты робота «Drive copy refresh» 13, 14, 15.10). Построено так: бесключевой вход (11.10): `drive-write.yml` / `drive_write.py` на `google-github-actions/auth`, суточное обновление копий, drift-guard, no-op `not_configured`; настройка — `ops/DRIVE-WIF-SETUP.md`.
  - 11.10 07:37: создание JSON-ключа заблокировано политикой организации Google Cloud (`iam.disableServiceAccountKeyCreation`, «Secure by Default»). Политику не отключаем.
- [x] Новая архитектура записана в канон: `NEW-CHAT-HANDOFF.md` (верхние блоки про робота), `BACKUP-AI-RUNBOOK.md`, `SYNC-RUNBOOK.md`, `USER-GUIDE.md`, `AI-PROJECT-GUIDE.md`, `README-AI-SYNC.md` — после зачистки инструкций 14.10 (`reports/cleanup-2026-10-14/`).

## План переключения шага Б на настоящую телеметрию (история: владелец переключил 13.10 без параллельного прогона; действующий порядок и откат — `ops/ROBOT-TELEMETRY.md`)

1. **Параллельный прогон 1–2 суток.** Смотреть `shadow/topview-robot-status.json` → `comparison`: `consistent` / `differences` / `monitor_may_lag`, число `unknown_new`, `slots.complete`, `scan.detail_failed`, ошибки job `topview-robot` в Actions. Критерий готовности: ни одного расхождения, которое не объясняется отставанием монитора (он ходит раз в 3 ч); все завершения, замеченные монитором, видны и у робота; ложных `unknown_new` нет; занятость N из 6 совпадает.
2. **Если критерий выполнен — владелец решает:** (а) робот публикует `topview-status.json` / `topview-task-map.json` / журнал / checkpoint через `scripts/monitor_publish.py` (тот же порядок записи, checkpoint последним) и только когда `scripts/monitor_role.py` разрешает писать (робот становится третьим именованным писателем в `monitor-role.json`, без автоподхвата ChatGPT); (б) монитор Claude переходит на редкий режим: раз в 3–6 ч и по событию — новая задача без сцены (`unknown_new`), неоднозначность task↔Scene, правка master, расхождение робот/монитор, молчание робота (`monitor-alert`).
3. **Что остаётся за агентом даже после переключения:** сопоставление новой задачи со сценой (робот Scene ID не придумывает), правки slow-набора в master, любые approval / rerender / удаление.
4. **Откат:** выключить расписание `topview-robot.yml` и вернуть монитору ежечасный режим — файлы телеметрии формат не меняют.

**Секреты сюда, в чат или в общедоступные файлы НЕ присылать.** Достаточно сообщения «ключи добавлены» без значений — дальше можно проверять Actions и статусы по логам.
