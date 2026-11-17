# SITE_ALERT_V2: приёмная сторона (Grok и Dot)

Статус: подготовлено, не включено. Проверено: 17.11.2026.

Порядок пробуждения и роли — `ops/PRIMARY-BACKUP-WAKE.md`; приёмка — `ops/SITE-ALERT-ACCEPTANCE.md`. Здесь только контракт получателя. Документ и код ничего не включают: `site_alert_routing.enabled` остаётся `false`, `wake_roles` не задаётся, canary не отправляется.

## Вызов

Обработчик Relay, получив событие, у которого первая строка начинается с `SITE_ALERT`, вызывает в **отдельной чистой** копии репозитория:

```
python3 scripts/site_alert_handler.py --repo <копия> --sync --actor grok \
  --sender-id <аутентифицированный sender agent ID из метаданных Relay> \
  --message-id <ID сообщения Relay> --event-id <ID события Relay> [--run-id <ID прогона, если есть>] \
  --message-file <файл с полным текстом> [--allow-test-id <точный ID из сохранённого промпта>]
```

Ответ — JSON. `terminal: true` у любого site-события, в том числе отклонённого: после него обработчик **не переходит** к ветке Topview/слотов, не вызывает Topview, не трогает очередь и lease видео. Единственный нетерминальный ответ — `outcome=not_site_alert` (код выхода 3): это не site-событие. Код 0 — успех, 2 — отказ с `reason`.

## Проверки (отказ закрыто)

1. **Отправитель.** `--sender-id` берётся только из аутентифицированных метаданных Relay, не из текста. Он должен совпасть с `ops/relay-wake.json` `sender_agent_id` (робот `topview-robot`). Сообщение коллеги, в том числе Dot (`chatgpt@cloud-239644772681871360`), не является SITE_ALERT_V2: `wrong_authenticated_sender`.
2. **Свежий main.** `git fetch`; при `--sync` чистая копия сбрасывается на `origin/main`. HEAD ≠ origin/main — `not_fresh_main`, грязная копия — `dirty_checkout`. Решение принимается по incident в этом main (`ops/site-alert-state.json`).
3. **Admission gate** PR 747 (`site_alert_receiver.validate`): `recipient_role`/`recipient_actor` совпадают с текущей ролью actor по `wake_roles` (нет блока — Dot основной, Grok резерв); точный текущий `incident_id`, роли состояния, тот же набор проблем и `occurrence_set`; production только при `site_alert_routing.enabled=true`. Причины: `wrong_current_recipient`, `stale_roles`, `stale_incident`, `problem_changed_or_resolved`, `stale_occurrence`, `production_disabled_or_wrong_marker`, `duplicate_field`.
4. **Дубли.** Тот же (incident, actor, message_id, state) — `duplicate`/`duplicate_message`, без записи; повторная доставка не продлевает прогресс. Второй ACK того же actor на тот же incident — `already_acknowledged`.
5. **Lease.** Собственный замок канона `ops/canon-lock.json`, holder `<actor>:<UUID4>`, 10 минут. Чужой действующий замок — `blocked_lock`, `receipt=not_saved`, ложного ACK нет. Замок берётся отдельным CAS-push (без force), затем fetch и readback: держатель — мы, иначе `lease_readback_failed`.
6. **Повторная проверка** gate на main, содержащем нашу lease.
7. **ACK.** Строка в `reports/site-alert-receipts.json` и освобождение замка — одним коммитом, CAS-push. Отклонённый push — перечитать main и решить заново (до 6 попыток, затем `cas_exhausted`). Затем fetch и readback: строка с нашим `message_id`/`holder` есть, замок свободен — иначе `receipt_readback_failed`. Неиспользованную lease обработчик пытается освободить; не получилось — она истекает сама.

Строка квитанции: `incident_id`, `actor`, `role`, `state` (`acknowledged` | `in_progress` | `blocked` | `resolved`), `updated_at` (UTC, фактическое), `evidence`, `message_id`, `event_id`, `run_id` (null, если не выдан, не выдумывается), `occurrence_set`, `read_main_sha`, `holder`. Хранятся последние 200 строк. `in_progress`/`blocked`/`resolved` требуют непустой `--evidence`. `resolved` допускается только после своего ACK и когда incident в main уже закрыт.

Таймер резерва (`site_alerts.progress_at`) продлевают только `acknowledged`/`in_progress` текущего **primary**. ACK резервного получателя записывается с `actor`/`role=backup`, но таймер primary не продлевает. При `wake_roles` Grok → Dot ACK Grok как primary продлевает таймер; квитанции видео (`reports/topview-event-wake.json`, поле `actor`) этот обработчик не трогает.

## SITE_ALERT_V2_TEST

Только при `site_alert_routing.enabled=false`, `read_only=true` и точном `test_id` из `--allow-test-id`. Список в сохранённом промпте по умолчанию пуст; неизвестный ID — `test_not_authorized`. Ответ `outcome=test_received`, `writes=none`: `test_id`, `actor`, `role`, `message_id`, `event_id`, `run_id`, `received_at_utc`, `main_sha`. Никаких ACK, lease, коммитов и вызовов Topview; `--state` кроме ACK — `test_is_read_only`. Получатель отвечает этим в исходном чате и в DM Dot и завершает обработку.

## Что это не доказывает

Тесты `tests/test_site_alert_handler.py` гоняют обработчик на локальном bare-репозитории с настоящими билдерами сообщений робота и canary. Это не доказывает доставку Relay, установку сохранённого промпта и реальное пробуждение. Живая приёмка — по `ops/SITE-ALERT-ACCEPTANCE.md`.
