# Dot основной, Grok резервный

Статус: действует. Проверено: 16.11.2026.

Это единственное место для порядка пробуждения и для предупреждений сайта. Остальные инструкции только ссылаются сюда и схему заново не описывают.

**Запуск.** Dot (ChatGPT) — основной исполнитель, его будят первым. Grok — резерв: около 20 минут нет ACK или около 30 минут нет прогресса. На практике это 20–40 минут: проверка идёт на реальных прогонах робота, а не по обещанной минуте. Решение владельца 16.11 (t626u): Dot запускает, Grok страхует; лимиты Grok беречь для генерации видео. Часовые страховки HH:55 и :00 пока остаются. После выбора резерва эпизод остаётся на Grok с проверкой раз в 60 минут, поэтому часовые страховки пока единственный третий уровень и их не отключать. Действующая непротухшая lease подавляет чужие пробуждения. Только бесплатный Unlimited за 0 кредитов. Повторы — `ops/TOPVIEW-RETRY.md`.

**Предупреждения сайта — два разных слоя. Код не переключён.**

Действующий маршрут (его исполняет код сейчас). `scripts/site_alerts.py` вызывают `canon-health.yml` и `topview-robot.yml`. Скрипт собирает предупреждения `canon-health` уровня warn/fail/error и условия жёлтой или красной плашки: нет времени Topview, время из будущего, проверка Topview старше 2 часов, неполный или ошибочный цикл монитора, ошибка синхронизации. Info-заметки не входят. Когда набор изменился, один раз шлёт сообщение Agent Relay на `site_alert_address` из `ops/relay-wake.json`. Сейчас этот адрес — Grok, не Dot. Порога 2 часа нет. Тот же набор повторно не шлётся.

Планируемый маршрут (решение владельца 16.11.2026, t633u). Его код не исполняет. Здоровье канона, размер файлов и ошибки Pages получает Dot. Grok перехватывает (1) по команде владельца в любой момент или (2) сам, если Dot за 2 часа не ответил (нет ACK) и не начал исправлять (нет прогресса), и тогда сообщает владельцу. Это не запуск видео и не разрешение Create. Пороги запуска 20 и 30 минут этот план не меняет. Новых адресов здесь нет.

Ниже — механизм включения видео-пробуждения. Он уже включён. Планируемые предупреждения сайта его не отменяют и код не переключают.

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

The genuine worker writes its exact business `event_id` in `reports/topview-event-wake.json.events[]`, under own lease/CAS/readback. Before long work: `outcome=started`, `retryable=true`, `execution.state=started`, `execution.stage=intake`, actual `execution.updated_at`. Update stage/time as real work advances. A test may use an explicitly read-only test event and must never create video/claim. Do not manufacture a worker receipt from an interactive coordinator. Runtime run ID is null if unavailable, never invented.

## Acceptance and rollback

Before enable: verify primary bot delivery into the current dot and its genuine early ACK; test primary-no-assignment, no-ACK backup, fresh ACK suppression, held lease suppression, backup-no-primary-DM and rejected-CAS-no-send without Topview. Confirm Grok still receives the unchanged issue-assigned backup. Record evidence, then flip only `dispatch.enabled=true` under own canon lease/CAS. Rollback is `false`: restores legacy simultaneous issue-assigned + primary DM, preserving the backup and queue safeguards.

Do not disable the hourly insurance until primary and backup runtime behavior is proven. No paid generation is part of acceptance.

## Verification limits

Read-only stage/time fixtures prove parser compatibility and progress suppression, not future worker reliability. Actual launch latency and long production heartbeat remain operational observations. Legacy hourly insurance is retained; it may still consume model quota. After backup selection an unchanged episode stays backup-only with 60-minute checks. Any dated final receipt also restarts the 30-minute progress grace. Unknown submissions remain reconcile-only.
