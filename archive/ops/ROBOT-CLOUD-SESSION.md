# Робот GitHub: три шага квеста — задание для облачной сессии Claude Code (НЕ КАНОН)

Решение владельца 11.10.2026 07:40: все три направления робота поручить одной облачной сессии — А (кнопки сайта), Б (сканер Topview), В (Drive-копия без файла-ключа).

**Статус (11.10.2026):** задание выполнено — шаги А (фаза 2, выключена), Б (сканер, теневой режим) и В (бесключевой Drive, ждёт настройки владельца) построены; итог — верхний блок `NEW-CHAT-HANDOFF.md` «РОБОТ GITHUB» и флажки в `ops/QUEST-THREE-KEYS.md`. Инструкция владельцу по шагу В — `ops/DRIVE-WIF-SETUP.md`.

**Зачем отдельная сессия:** облачные сессии Claude Code до 5 ноября 10:59 МСК оплачиваются бонусом 100 $ и не тратят лимит подписки.

**Как запустить (владелец):** claude.ai/code → новая сессия → репозиторий `virudik/ai-film-prompts`, ветка `main` → вставить текст ниже целиком. Не одновременно с генеральной зачисткой 16.10 (одна большая сессия за раз). На шаге В сессия попросит владельца один раз выполнить несколько команд в Google Cloud Shell — секретов там нет.

**Пока идёт сессия:** рабочий чат Claude канон не правит. Монитор Claude продолжает работать — сессия его не трогает и не выключает.

---

```text
Проект «AI Film Серёгиус». Канон — этот репозиторий, ветка main. Прочитай CLAUDE.md, верхние блоки NEW-CHAT-HANDOFF.md, ops/QUEST-THREE-KEYS.md, ops/PLAN-OWNER-PANEL-AUTOMATION.md, ops/CLAUDE-MONITOR.md, scripts/process_owner_decisions.py, scripts/topview_light_check.py, scripts/monitor_publish.py, scripts/monitor_role.py, scripts/topview_api_probe.py, scripts/drive_write.py, .github/workflows/sync-from-drive.yml и drive-write.yml.

ЦЕЛЬ: робот GitHub Actions (скрипты без ИИ) берёт на себя детерминированную рутину, чтобы экономить лимиты Claude/ChatGPT и не зависеть от компьютера владельца. Творческое, неоднозначное, approval/rerender/удаление сцен — НЕ робот. Технический success ≠ approval. Один писатель канона (monitor_role.py); гонки решает git: push отклонён → перечитать и повторить с нуля. Ключи/пароли никогда не просить и не выводить в логи, аннотации, файлы.

ШАГ А — кнопки сайта (ключ SUPABASE_SERVICE_ROLE_KEY уже в Secrets; робот читает Supabase — подтверждено 11.10):
1. Сейчас job owner_decisions применяет accept / redo / to_montage / tv_mark_status(result_bad) к review-ledger.json. Добавить фазу 2 из ops/PLAN-OWNER-PANEL-AUTOMATION.md: in_film / scene_not_needed / tv_drop_task — прямым коммитом video-prompts.md в main (минимальный diff: раздел сцены, строка оглавления, счётчики; Scene ID резервируется навсегда), затем SYNC-TRIGGER и проверка project-status.health=ok; Supabase applied ТОЛЬКО после успешного push и health=ok. Если у сцены есть активная задача Topview, конфликт кнопок или неоднозначность — needs_owner, ничего не трогать. owner_task (свободный текст) — не робот.
2. Включение фазы 2 — только переменной GitHub ROBOT_MASTER_ACTIONS=on (по умолчанию выключено); владелец включает сам после проверки. До этого — режим «план без записи» с отчётом в аннотации.
3. Тесты на фикстурах (без сети): правильный diff master, резервирование ID, конфликты → needs_owner, commit-before-ack.

ШАГ Б — сканер Topview (ключ TOPVIEW_API_KEY + переменная TOPVIEW_UID уже есть; проверено 11.10):
Эндпоинты (только GET; заголовки `Authorization: Bearer <key>`, `Topview-Uid: <uid>`):
- https://api.topview.ai/boards/list?pageNo=1&pageSize=50 → result {data[], total}; доска: boardId, name, taskCount, gmtModify.
- https://api.topview.ai/boards/tasks/list?boardId=…&mediaType=video&sortField=gmtCreate&sortOrder=desc&pageNo=…&pageSize=100 → result {data[], total}; задача: boardTaskId, status, useUnlimitMode, gmtCreate, completedAt, parameters, errorCode, errorMessage.
- Детали задачи (очередь/ETA) — найти «Get Board Task Detail» в https://docs.topview.ai/reference (к странице можно дописать .md).
Основная доска 1a6244cf1ae747ef847d949a80d6133c, всего 11 досок, 6 безлимитных слотов.
1. scripts/topview_api_scan.py: облегчённый/полный обход как topview_light_check.py; активные безлимитные задачи, занятость N из 6, завершения; задача↔сцена ТОЛЬКО по topview-task-map.json, новые — unknown_new (Scene ID не придумывать).
2. .github/workflows/topview-robot.yml: каждые 30 мин + workflow_dispatch. ТЕНЕВОЙ режим: пишет только shadow/topview-robot-status.json и сравнение с topview-status.json монитора (расхождения — туда же и в notice-аннотацию); коммит только при изменении.
3. Переключение на настоящую телеметрию (через monitor_publish.py + monitor_role.py) и редкий режим монитора Claude — НЕ делать, только план в ops/QUEST-THREE-KEYS.md; решение владельца после 1–2 дней параллельного прогона.

ШАГ В — Drive-копия без файла-ключа (Workload Identity Federation):
Политика организации Google владельца запрещает JSON-ключи (iam.disableServiceAccountKeyCreation) — политику не трогать. Сделать бесключевой вход GitHub → Google:
1. Подготовить для владельца короткую инструкцию по-русски + готовые команды для Google Cloud Shell (кнопка «>_» вверху console.cloud.google.com), подставив имя репозитория virudik/ai-film-prompts: включить IAM Credentials API и Drive API; workload identity pool + OIDC-провайдер для GitHub (issuer https://token.actions.githubusercontent.com, attribute condition строго на этот репозиторий); сервисный аккаунт ai-film-writer (владелец уже создал его 11.10 — использовать его); привязка roles/iam.workloadIdentityUser только для этого репозитория. Затем владелец даёт адресу сервисного аккаунта доступ «Редактор» ТОЛЬКО к папке «AI Film Prompts Master» на Drive и записывает в GitHub Variables (не секреты): GCP_WORKLOAD_IDENTITY_PROVIDER и GCP_SERVICE_ACCOUNT. Спросить владельца, когда готово.
2. Переделать drive-write.yml / drive_write.py: вход через google-github-actions/auth (permissions: id-token: write) вместо GDRIVE_SA_KEY; раз в сутки обновлять Drive-копию (те же file ID: video-prompts.md, 7 инструкций, film-backlog.md, film-analysis.md) точными копиями из main, только если sha отличается; перед записью — Drive-файл должен совпадать с одной из прошлых версий в git (иначе правили вручную: не затирать, issue drive-drift); после записи read-back sha; затем python3 scripts/cert_github.py . --drive-copy-dir <копии> и коммит. Канон на Drive не писать. Без переменных — аккуратный no-op «not_configured».

ПРОВЕРКИ И ОТЧЁТ: python3 -m unittest discover -s tests (новые тесты добавить в .github/workflows/test-recovery-integration.yml); python3 scripts/validate_site.py .; ручной запуск новых workflow, зелёный прогон. Коммиты небольшими шагами, git pull --rebase перед push. В верхний блок NEW-CHAT-HANDOFF.md — короткий пункт по каждому шагу (что работает, что в теневом/выключенном режиме, какие решения нужны от владельца); флажки в ops/QUEST-THREE-KEYS.md; python3 scripts/cert_github.py . В конце — короткий отчёт владельцу по-русски: что сделано, как проверить, что ему включить или решить.
```
