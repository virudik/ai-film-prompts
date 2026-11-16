# Dot основной, Grok резервный

Статус: действует. Проверено: 16.11.2026.

Это единственное место для порядка пробуждения и для предупреждений сайта. Остальные инструкции только ссылаются сюда и схему заново не описывают.

**Запуск.** Dot (ChatGPT) — основной исполнитель, его будят первым. Grok — резерв: около 20 минут нет ACK или около 30 минут нет прогресса. На практике это 20–40 минут: проверка идёт на реальных прогонах робота, а не по обещанной минуте. Решение владельца 16.11 (t626u): Dot запускает, Grok страхует; лимиты Grok беречь для генерации видео. Часовые страховки HH:55 и :00 пока остаются. После выбора резерва эпизод остаётся на Grok с проверкой раз в 60 минут, поэтому часовые страховки пока единственный третий уровень и их не отключать. Действующая непротухшая lease подавляет чужие пробуждения. Только бесплатный Unlimited за 0 кредитов. Повторы — `ops/TOPVIEW-RETRY.md`.

**Отметка, что резерв проснулся (решение владельца Виталик, 16.11.2026, t639u).** Когда Grok получает резервный wake (issue-assigned `TOPVIEW_SLOT_WAKE_V2`), но видит свежий прогресс Dot или чужую действующую lease/claim, он ничего не запускает: без claim, intent, Create и ACK. Свежий прогресс Dot — запись в `reports/topview-event-wake.json` для этого `event_id` или коммит прогресса Dot в `main` моложе 30 минут. В самом issue обязателен один короткий комментарий-отметка: «Grok проснулся ЧЧ:ММ МСК (резервный wake, event <event_id>). Dot активен: <коммит/время>. Резерв не нужен, ничего не запускал.» Если причина — чужая действующая lease/claim, в слоте «Dot активен» называется её держатель и срок; коммит не выдумывается. Это не ACK и не захват запуска: в `reports/topview-event-wake.json` ничего не пишется. Один комментарий на issue, без дубля при повторном событии. Если Grok перехватывает, кроме ACK он пишет в issue: «Grok перехватил резервом в ЧЧ:ММ МСК». Цель — при проверке страховки видно, что Grok проснулся и принял сигнал, даже если не вмешался. Повод: issue 737 (16.11.2026, 18:40 МСК) — Grok проснулся, увидел коммит Dot `3201da3f` от 18:22 МСК и промолчал, из-за чего пробуждение выглядело как разрыв.

**Предупреждения сайта: проект изменения, не включать до отдельной приёмки.**

Блокер интеграции: текущий получатель Relay должен получить и проверить отдельную ветку обработки `SITE_ALERT_V2`; существующий обработчик видеослотов не является такой веткой. Обновление automation и включение выполняются отдельно после обзора и явного решения владельца. Этот PR не устанавливает обработчик и не доказывает доставку ни Dot, ни Grok.

`scripts/site_alerts.py` вызывается существующими `canon-health.yml` и `topview-robot.yml`, без нового расписания. Новый набор warn/fail/error и предупреждений плашки получает Dot (`site_alert_address`, текущий адрес Dot из конфигурации). Grok получает резервный сигнал по тому же incident: через 30 минут для явных fail/error, через 120 минут для warn и неоднозначных предупреждений, если нет более свежего настоящего ACK/прогресса Dot. Значения заданы в `site_alert_routing`, не связаны с порогами видеозапуска 20/30. Порог проверяется на реальных прогонах робота, не является обещанием доставки по минутам. Ошибка Pages считается критической, только если исходная проверка явно классифицировала её как fail/error; отсутствие такого источника не подменять догадкой.

`ops/site-alert-state.json` версии 2 содержит signature, уникальный incident_id, время первого обнаружения, транспортные результаты primary/backup. Пока хотя бы одна проблема сохраняется, incident_id, настоящий прогресс и отметка отправленного backup сохраняются при изменении соседних предупреждений. Покрытие резервом хранится отдельно для каждого появления проблемы (код, критичность, порядковый номер появления). Таймер считается отдельно для каждого ещё не покрытого появления проблемы по его критичности; новая проблема после прежнего backup получает собственный таймер. Повышение критичности той же непрерывной проблемы сокращает порог, но не скрывает уже прошедшее время. Просроченный backup приоритетнее очередного обновления primary, поэтому меняющиеся соседние warn не удерживают резерв бесконечно. Полный сброс проблемы закрывает эпизод; повтор после исправления получает новый sequence. Legacy Grok-квитанция не считается отправкой новому primary. Ошибка доставки не считается ACK и не сбрасывает таймер. Один резервный сигнал не доказывает пробуждение или исправление. Два workflow используют общую concurrency-группу site-alert-routing; после конфликта push перечитывают main и пересчитывают решение, не переносят старую квитанцию через rebase. Стабильный payload даёт транспортную идемпотентность при повторе; это не атомарная транзакция между Relay и Git. Ошибка отправки повторяется не чаще раза в 10 минут, чтобы коммит ошибки не образовывал цикл самопробуждения.

Обработчик пишет настоящий ACK и затем прогресс под собственной lease/CAS/readback в отдельный `reports/site-alert-receipts.json`, не в видеоквитанции. Пример структуры (значения только фактические): `{"schema_version":1,"events":[{"incident_id":"точный SITE_ALERT_V2 ID","actor":"dot","state":"acknowledged","updated_at":"фактическое UTC с часовым поясом","evidence":"что действительно проверено"}]}`. Прогресс: `state=in_progress`; завершение: `state=resolved` или `blocked`. Таймер продлевают только acknowledged/in_progress, точный текущий incident_id, actor=dot, непустое evidence и дата между началом эпизода и текущим временем. Старый commit, чужой incident, будущая дата или resolved при всё ещё существующей проблеме не доказывают активной работы. Чужую lease не перехватывать; при блокировке не писать ложный ACK.

Grok при резервном сигнале проверяет свежие данные и сообщает владельцу результат. Прямая команда владельца по-прежнему может назначить Grok немедленно. Этот путь не запускает видео, не меняет очередь и не даёт права Create. Info-заметки не включаются. Код и тесты не заменяют живую приёмку «Dot получил → записал ACK → резерв получил → подтвердил»: до её фактического прохождения end-to-end не считается доказанным.

## Dispatch mechanism (video wake) · 15.11.2026

Owner requested one initial AI wake, not two competing full scans. This change routes notifications only; it never grants ownership or permission to Create.

## Activation status

Enabled after read-only transport/ACK acceptance on 15.11.2026; evidence: `reports/primary-backup-acceptance.json`. Primary test714 produced a genuine webhook-triggered, delegated started ACK in 888c8352 and completed ACK in a83c2578. Relay-to-started delay was 7m19s, so thresholds are 20/30 minutes. Grok backup runtime evidence is its explicit correlated self-report about issue713, not an independently inspected Grok execution log. Existing HH:55/HH:00 insurance is unchanged and can still consume model quota.

## Enabled behavior

- New demand episode (active global task set) first wakes only dot through the existing configured ChatGPT Relay inbox. The audit issue has **no assignee**, so it does not also wake Grok through issue-assigned.
- A subsequent fresh complete robot scan checks the exact event receipt. Missing ACK after 20 minutes allows a backup wake. A real dated receipt/`execution.updated_at` suppresses another AI wake until 30 minutes without progress. Checks occur on actual robot runs, not exact promised deadlines.
- Any held unexpired/malformed global lease suppresses competing wakes. An expired lease does not clear claim/intent or authorize Create.
- Backup wake uses the existing Grok GitHub issue-assigned route, **without a duplicate dot DM**. Further backup checks are paced at 60 minutes while demand remains.
- Both workers obey the shared CAS/lease/claim/intent/verify protocol. Any claimed/submitting/unknown item first requires reconciliation; the wake's text explicitly prohibits retrying an unknown Create. The robot never edits queues or launches videos.
- Route decision is saved in `automation-monitor-status.json.notification_state.robot_dispatch` and CAS pushed/read back **before** external notification. `attempted_at` proves an attempt, not delivery or work. A failed CAS causes no wake.

## ACK contract

The genuine worker writes its exact business `event_id` in `reports/topview-event-wake.json.events[]`, under own lease/CAS/readback. Before long work: `outcome=started`, `retryable=true`, `execution.state=started`, `execution.stage=intake`, actual `execution.updated_at`. Update stage/time as real work advances. A test may use an explicitly read-only test event and must never create video/claim. Do not manufacture a worker receipt from an interactive coordinator. Runtime run ID is null if unavailable, never invented. A stand-down under «Отметка, что резерв проснулся» is not this ACK and writes nothing in that file. A real backup takeover still writes this ACK and adds the issue line «Grok перехватил резервом в ЧЧ:ММ МСК».

## Acceptance and rollback

Before enable: verify primary bot delivery into the current dot and its genuine early ACK; test primary-no-assignment, no-ACK backup, fresh ACK suppression, held lease suppression, backup-no-primary-DM and rejected-CAS-no-send without Topview. Confirm Grok still receives the unchanged issue-assigned backup. Record evidence, then flip only `dispatch.enabled=true` under own canon lease/CAS. Rollback is `false`: restores legacy simultaneous issue-assigned + primary DM, preserving the backup and queue safeguards.

Do not disable the hourly insurance until primary and backup runtime behavior is proven. No paid generation is part of acceptance.

## Verification limits

Read-only stage/time fixtures prove parser compatibility and progress suppression, not future worker reliability. Actual launch latency and long production heartbeat remain operational observations. Legacy hourly insurance is retained; it may still consume model quota. After backup selection an unchanged episode stays backup-only with 60-minute checks. Any dated final receipt also restarts the 30-minute progress grace. Unknown submissions remain reconcile-only.
