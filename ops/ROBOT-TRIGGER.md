# Внешний триггер робота (Supabase → GitHub) — рабочая справка

Статус: действует. Проверено: 22.10.2026.

**Статус 13.10.2026: работает.** Это не канон, а описание инфраструктуры, которая живёт вне репозитория.

## Зачем
Расписание GitHub Actions (`schedule:`) не гарантирует время: по истории запусков 12–13.10 `topview-robot` (задано каждые 30 минут) срабатывал раз в 5–7 часов, то же `sync-from-drive` и суточная копия Drive. Поэтому «каждые 30 минут» в старых документах недостоверно. Решение владельца 13.10: запускать робота снаружи.

## Как устроено
- Supabase (проект `ai-film-comments`, `vzohfatqzyioydtgjiyd`): расширения `pg_cron` и `pg_net`, функция `public.dispatch_github_workflow(файл)`, три задачи:
  - `dispatch-topview-robot` — каждые 10 минут (:00) → `topview-robot.yml` (сканер Topview);
  - `dispatch-sync-from-drive` — :02/:12/… → `sync-from-drive.yml` (кнопки владельца, статус, оповещения);
  - `dispatch-topview-video-archive` — :05/:15/… → `topview-video-archive.yml` (копии MP4 в Drive).
  - `dispatch-self-heal` — :19/:49 → `self-heal.yml` (самопроверка автоматики; добавлено 22.10.2026 по «да» владельца, проверено: ответ GitHub 204).
- Токен GitHub (fine-grained, один репозиторий, права только Actions: Read and write) лежит в Supabase Vault под именем `github_dispatch_token`. В репозитории, чате и логах его нет. Срок действия выбирал владелец при создании; продлевать до окончания.
- SQL без секретов: `ops/supabase/2026-10-13_robot_dispatch_cron.sql`.
- Расписание GitHub в самих workflow оставлено как запасное (может опаздывать на часы).
- Конкуренция: у каждого workflow своя `concurrency`-группа, параллельные запуски одного файла не пересекаются.

## Проверка и управление
- Принято GitHub: `select status_code, count(*) from net._http_response group by 1;` — 204.
- Запуски: Actions → событие `workflow_dispatch`.
- Остановить: `select cron.unschedule('<имя>');` или удалить токен в GitHub (Settings → Developer settings). Тогда остаётся расписание GitHub.
- Задачи вызывают workflow по имени файла, поэтому файлы workflow не переименовывать (зачистка 14.10 переименование `sync-from-drive.yml` отменила). Если всё же переименуют — задачу в pg_cron пересоздать с новым именем в том же коммите.
- Если триггер молчит больше 3 часов, сработает `monitor-alert` (D3).
