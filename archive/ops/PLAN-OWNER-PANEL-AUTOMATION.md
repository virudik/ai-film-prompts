# AI Film — автоматическое применение решений из панели сайта (план внедрения)

**Статус на 11.10.2026 (пересмотрен 04:32):** первая серверная фаза подготовлена в GitHub, но не подтверждена end-to-end и без ключа Supabase НЕ выполняется. С 03:25 канон — GitHub `main`: фазы, меняющие master, делаются прямым коммитом, Drive-писатель для них не нужен. Этот файл — рабочее ТЗ, **не канонический источник**. При активации внести запись в `NEW-CHAT-HANDOFF.md`, `SYNC-RUNBOOK.md`, `USER-GUIDE.md` в GitHub `main`, проверить статус и Pages.

## Задача

Владелец нажимает кнопку у Scene ID или пишет текстовое требование в панели `🔑 Владелец`. Сайт сохраняет намерение в `public.owner_decisions` Supabase. **Никакого GitHub PAT, service-role key, GDrive JSON и AI API key в браузере/Pages**. Статусы видны владельцу в той же панели.

## Текущий серверный обработчик (MVP)

Ранее существовавший workflow `.github/workflows/sync-from-drive.yml` запускается `*/30 * * * *`, а также вручную. В него добавлен отдельный job `owner_decisions` **без отдельной автоматизации**. Job срабатывает на schedule/dispatch, в том числе если основная Drive-синхронизация завершилась с ошибкой. GitHub Actions получает секрет `SUPABASE_SERVICE_ROLE_KEY` из настроек репозитория, читает только заявки, которые может обработать детерминированно, применяет минимальный diff к `review-ledger.json`, запускает `scripts/validate_review_ledger.py`, коммитит в GitHub, **только после успешного push** переводит соответствующие Supabase-записи в `applied`. Сбой или гонка → повтор от свежего HEAD в следующем запуске, `in_progress` с префиксом `github-owner-sync:` повторяем. Секрет отсутствует → явное `not configured`, ничего не применяется.

Автоматически обрабатываются только **явные** и однозначные кнопки `accept`, `redo`, `to_montage`, `tv_mark_status(result_bad)`, и только в `review-ledger.json`. Конфликт «Принять» против «Переделать/Брак» одной сцены → `needs_owner`; уже вставленная в фильм сцена не откатывается. Успех Topview не приравнивается к решению владельца.

**Не охвачено этим MVP:** `in_film`, `scene_not_needed`, `tv_drop_task`, `tv_mark_status(result_ok)` (требуются валидатор и/или изменение master+Topview task mapping); `owner_task` с произвольным творческим текстом (нужен AI-редактор с prompt-style, Drive refs и верификацией). Такие заявки остаются видимыми в Supabase для действующего основного монитора/рабочего чата. Никакие Topview видео или платные генерации не запускаются.

## Ключи и настройка

1. На GitHub `virudik/ai-film-prompts` в **Settings → Secrets and variables → Actions** создать `SUPABASE_SERVICE_ROLE_KEY`, значение — `service_role`/secret API key проекта Supabase `vzohfatqzyioydtgjiyd`. Не путать с публичным `sb_publishable_...`, который не имеет права менять защищённые решения. Не помещать секрет в чат или код. Это привилегированный ключ ко всему проекту Supabase: хранить только в защищённом серверном хранилище; в будущем заменить узко-скоупным proxy/Edge Function token.
2. Правки master роботом — прямой коммит в GitHub `main` от свежего HEAD (минимальный diff; push отклоняется при гонке — повтор с нуля), затем валидатор `health=ok` и Pages. `GDRIVE_SA_KEY` для этого не нужен (он только для автообновления Drive-копии).
3. Удостовериться в первом реальном run `sync-from-drive.yml`: job `owner_decisions` executed, `review-ledger.json` verified, Supabase `status=applied` verified. Зеленый skipped/no-op — **не тест применения**.
4. Не отключать `AI Film — единый монитор`, Claude primary/ChatGPT standby; Github job — отдельный исполнитель решений владельца, не третий Topview монитор и не меняет `monitor-role.json`.

## Целевая полная схема — следующие фазы

- **Фаза 2 — построена 11.10.2026, ВЫКЛЮЧЕНА** (`scripts/robot_master_actions.py` + `scripts/master_scene_edit.py`, шаг «Phase 2» в `sync-from-drive.yml`; включение — только переменная GitHub `ROBOT_MASTER_ACTIONS=on`, по умолчанию «план без записи»). Реализовано ниже описанное; `applied` ставится только после push + `health=ok` + read-back; открытая `owner_task` по сцене откладывает кнопку. `base_sha256` заменён свежим чтением `main` и откатом при отклонённом push. Исходная формулировка: Строго определённые операции `in_film` / `scene_not_needed` / `tv_drop_task` делаются прямым коммитом master в GitHub `main` от свежего HEAD с проверкой `base_sha256`, reserved Scene IDs, revalidation dependencies, валидатором и Pages. Статус `applied` только после всего цикла. Если существует active Topview task или коллизия master — `needs_owner`, ничего не закрывать.
- **Фаза 3.** Структурированное редактирование сцены: `scene_id`, выбор поля (реплики, действие, камера, референсы, длительность), текст изменения, базовая ревизия master; необязательный предпросмотр diff. Сервер получает fresh master из `main` + PROMPT-STYLE-GUIDE + близкие сцены/refs, строит proposal, валидирует identity, continuity, syntax и зависимости. Конкретно сформулированная правка владельца может быть применена автоматически после проверки; неоднозначность → `needs_owner`. Для LLM-части потребуется отдельный серверный AI API key, GitHub Actions secrets и лимиты. Не предоставлять LLM права произвольных файловых/секретных записей.
- **Фаза 4.** Статус прогресса и история в панели: `pending` → `in_progress` → `applied` / `needs_owner` / `rejected`; ссылки на проверенный GitHub commit/master SHA, ошибка и повтор. `owner_task` не смешивать со статусом однозначной кнопки.

## Тесты и safety

Изоляция service_role, отсутствие PAT в HTML, консистентность SHA и commit-before-ack, защита от повторного выполнения, конфликта с `inserted_into_film`, несогласованных одновременных решений, отменённой заявки и сломанных ledger-инвариантов. Реальное рабочее состояние объявлять только после E2E с тестовой заявкой и корректным прочтением Supabase и GitHub. Архитектура не отменяет принцип единственного редактора master.
