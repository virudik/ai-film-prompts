# Робот GitHub: сканер Topview (+ необязательно Drive-копия) — задание для облачной сессии Claude Code (НЕ КАНОН)

**Зачем отдельная сессия:** облачные сессии Claude Code до 5 ноября 10:59 МСК оплачиваются бонусом 100 $ и не тратят лимит подписки.

**Как запустить (владелец):** claude.ai/code → новая сессия → репозиторий `virudik/ai-film-prompts`, ветка `main` → вставить текст ниже целиком. Можно в любой день; не одновременно с генеральной зачисткой 16.10 (одна большая сессия за раз).

**Пока идёт сессия:** рабочий чат Claude канон не правит. Монитор Claude продолжает работать как обычно — сессия его не трогает и не выключает.

---

```text
Проект «AI Film Серёгиус». Канон — этот репозиторий, ветка main. Прочитай CLAUDE.md, верхние блоки NEW-CHAT-HANDOFF.md, ops/QUEST-THREE-KEYS.md (шаг Б), ops/CLAUDE-MONITOR.md (как монитор Claude сейчас сканирует Topview коннектором), scripts/topview_light_check.py, scripts/monitor_publish.py, scripts/topview_api_probe.py, topview-status.json, topview-task-map.json.

ЦЕЛЬ: робот GitHub Actions (без ИИ) сам проверяет очередь Topview через публичный API, чтобы монитор Claude можно было перевести на редкий режим и экономить лимит подписки. Решение о переводе — только владельца, после параллельного прогона.

ДАННЫЕ (проверено 11.10.2026 с ключом владельца): секрет TOPVIEW_API_KEY и переменная TOPVIEW_UID уже в GitHub. Заголовки: `Authorization: Bearer <key>`, `Topview-Uid: <uid>`. Эндпоинты (только GET):
- https://api.topview.ai/boards/list?pageNo=1&pageSize=50 → result {data[], pageNo, pageSize, total}; у доски boardId, name, taskCount, gmtModify.
- https://api.topview.ai/boards/tasks/list?boardId=…&mediaType=video&sortField=gmtCreate&sortOrder=desc&pageNo=…&pageSize=100 → result {data[], total}; у задачи boardTaskId, status, useUnlimitMode, gmtCreate, completedAt, parameters (modelName, positivePrompt…), errorCode, errorMessage.
- Детали одной задачи (очередь/ETA, если API их даёт) — найди «Get Board Task Detail» в https://docs.topview.ai/reference (к любой странице можно дописать .md). Основная доска AI Film: 1a6244cf1ae747ef847d949a80d6133c. Всего 11 досок, ёмкость безлимита — 6 слотов.

ЭТАП 1 — сканер (теневой режим):
1. scripts/topview_api_scan.py: полный обход всех досок и страниц (видео), активные безлимитные задачи (не success/fail), занятость N из 6, завершения с прошлого скана; сопоставление задача↔сцена ТОЛЬКО по topview-task-map.json (известные task_id) — новые задачи помечать «unknown_new», Scene ID не придумывать. Облегчённый режим как в topview_light_check.py (счётчики досок + первая страница основной доски), полный обход раз в ~3 ч или при расхождении счётчиков.
2. Workflow .github/workflows/topview-robot.yml: по расписанию каждые 30 мин + workflow_dispatch. В ТЕНЕВОМ режиме пишет ТОЛЬКО shadow/topview-robot-status.json (не topview-status.json и не прочие файлы телеметрии) и сравнение с последним topview-status.json монитора: совпадают ли активные задачи, статусы, занятость, завершения. Расхождения — в тот же файл и как notice-аннотация. Коммит только при изменении (чтобы не засорять историю), git pull --rebase перед push.
3. Безопасность: только GET; никаких submit/delete/rerun/approve, кредиты не тратить; ключи и промты в лог/аннотации/файлы не выводить (только счётчики, id задач, статусы, время). Время — только реальное время запроса. Технический success ≠ approval.
4. Тесты: tests/test_topview_api_scan.py на записанных фикстурах (без сети), добавить в .github/workflows/test-recovery-integration.yml. Прогнать: python3 -m unittest discover -s tests; python3 scripts/validate_site.py .
5. Запустить workflow вручную, убедиться в зелёном прогоне и правдоподобных данных; дать поработать параллельно с монитором Claude (минимум 1–2 дня); итог сравнения записать в ops/QUEST-THREE-KEYS.md (Б++).

ЭТАП 2 — НЕ ДЕЛАТЬ без решения владельца: переключение робота на запись настоящей телеметрии (через scripts/monitor_publish.py и scripts/monitor_role.py — один писатель!), монитор Claude на редкий режим. Подготовь только план переключения в ops/QUEST-THREE-KEYS.md.

ЧАСТЬ В (необязательно, только если в GitHub Secrets есть GDRIVE_SA_KEY — проверить по логу drive-write.yml «not_configured»): доработать .github/workflows/drive-write.yml / scripts/drive_write.py, чтобы раз в сутки обновлять Drive-копию (те же file ID в папке «AI Film Prompts Master»: video-prompts.md, 7 инструкций, film-backlog.md, film-analysis.md) точными копиями из main, только если sha отличается; перед записью проверить, что Drive-файл совпадает с одной из прошлых версий в git (иначе правили вручную — не затирать, открыть issue drive-drift); после записи read-back sha; затем python3 scripts/cert_github.py . --drive-copy-dir <скачанные копии> и коммит. Канон на Drive не писать — только копии. Без ключа часть В пропустить.

ОТЧЁТНОСТЬ: в верхний блок NEW-CHAT-HANDOFF.md — короткий пункт о сканере (теневой режим, где смотреть результат); python3 scripts/cert_github.py .; коммиты небольшими шагами. Ключи/пароли не просить. В конце — короткий отчёт владельцу: что сделано, как проверить, какие решения нужны от него.
```
