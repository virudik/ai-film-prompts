# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: ready
Проверено: 2026-10-31T15:24:03+00:00
Задача: TOPVIEW-SLOT-PRIORITY-20261024 — Заполнение свободных Topview-слотов — задача №1

Последний подтверждённый этап: Простой 5ч40м19с разобран; исправление71f43c36111659f708af28f4655757f90cffd493 опубликовано и прочитано обратно.91 целевой тест, независимый review,282 CI tests и live consistency прошли; штатный robot12:20Z выполнил новый код и записал capacity_full. Оба существующих automation prompts обновлены и точно проверены.
Следующий шаг: При следующем настоящем Relay/HH:55 проверить его собственную начальную и итоговую квитанции. Перед следующим Create свежие main/решения/замок, существующие task IDs и полный глобальный scan: при свободной ёмкости первая S71-WAN30, затем S56-SEED20-P2 по живой готовности/priority. S72 task22dbd25cdd9f47cd9e44300e55f5e44f наблюдать без повтора; unknown сначала сверить.

## Контрольная точка

# Простой слота: расследование и исправление автоматики · 31.10.2026

work_id: TOPVIEW-SLOT-PRIORITY-20261024

Исправлено и проверено 2026-10-31T12:22:06Z. Простой 31.10.2026: S48-P1 завершилась 08:28:29 МСК; S72-WAN30 заняла слот 14:08:48 МСК. Потеряно 5ч40м19с. Робот видел свободный слот и доставил четыре сигнала; первый обработчик взял замок, но не оставил результата/блокера. После трёх повторов прежний re-wake прекращался; старый scheduled success мог скрыть текущий простой. Внутренняя причина остановки фонового worker не раскрыта доступным API.

Код опубликован `71f43c36111659f708af28f4655757f90cffd493`, 8 файлов точно прочитаны обратно. Первые три повтора через20мин, далее через60мин пока сохраняется потребность; независимый контроль исполнения до проверки интервала; launch_stalled при неисполненной потребности; монотонные ID; реальные квитанции и подтверждённые task IDs. Claim/unknown не сбрасываются и не разрешают повторный Create. Заменённый wake issue закрывается как superseded/not_planned, не как исполнение.

Обновлены ровно два существующих prompt: часовой6acae6ab433481919e88665c520b8ef2 и Relay6adc585e7ac08191bb93825117dc7213. Точный readback подтверждён; HH:55 Europe/Moscow, enabled и одна прежняя relay.message-подписка сохранены. Реальный исполнитель должен сохранить начало и итог; no_update не заменяет квитанцию. Интерактивный чат не создавал ни событийный ACK, ни reports/topview-launcher-cycle.json от имени расписания.

Проверки:91 целевой тест и независимый review PASS; GitHub integration run41200577107 — success/282 tests; canon-health run41200577121 — success; live instruction-consistency — ok. Штатный robot run41200624806 на новом коде — success: light scan12:20:31Z,6/6 занято, launcher_health12:20:36Z=capacity_full; этот статус прямо не доказывает исполнение фонового launcher. Нового Create в расследовании0.

Граница проверки: успешный запуск без открытого чата после исправления ещё не наблюдался — сейчас свободных слотов нет. Следующий настоящий runtime должен подтвердить себя собственной квитанцией и, при доступной ёмкости, task ID. Гарантия непрерывной работы внутреннего worker не заявляется.

Следующий шаг: При следующем настоящем Relay/HH:55 проверить его собственную начальную и итоговую квитанции. Перед следующим Create свежие main/решения/замок, существующие task IDs и полный глобальный scan: при свободной ёмкости первая S71-WAN30, затем S56-SEED20-P2 по живой готовности/priority. S72 task22dbd25cdd9f47cd9e44300e55f5e44f наблюдать без повтора; unknown сначала сверить.

Доказательства: `reports/topview-slot-idle-2026-10-31.json`, `reports/topview-slot-idle-fix-2026-10-31.json`, `reports/instruction-consistency.json`.

## Обязательные правила

- Since 11.10.2026: GitHub main = canon (master + 7 docs, status, site); Drive / Notion / Library / Project files = read-only backups; Topview = telemetry; Notion = story. — `NEW-CHAT-HANDOFF.md`
- One master: video-prompts.md in GitHub main; no v2/final/copy. — `AI-PROJECT-GUIDE.md`
- Before any master write: fresh git pull of main; minimal commit → SYNC-TRIGGER → validator health=ok → Pages → verification; rejected push = another writer, redo from scratch. — `NEW-CHAT-HANDOFF.md`
- Instruction edits: fresh pull → minimal commit → scripts/cert_github.py → push → verify; never replay a stale write. — `NEW-CHAT-HANDOFF.md`
- Scene IDs stable; retired IDs never reused; rerender keeps the same Scene ID. — `AI-PROJECT-GUIDE.md`
- Topview technical success ≠ editorial approval; never auto approve/rerun/delete/close. — `SYNC-RUNBOOK.md`
- Slot capacity 6; one active task = one slot; a terminal task frees its slot at once; canonical slow is cleared only by an explicit owner button (11.10.2026), never by a technical terminal. — `SYNC-RUNBOOK.md`
- One writer, decided by monitor-role.json + scripts/monitor_role.py: since 13.10.2026 the GitHub robot (topview-robot.yml → robot_telemetry.py, every 10 min via Supabase pg_cron) is primary, ChatGPT is standby and takes over only after 180 min without a verified healthy robot cycle; the Claude monitor is off; kill switch ROBOT_TELEMETRY=shadow. Old ChatGPT HH:00 monitor and archived Recovery/slot-watcher stay off. — `NEW-CHAT-HANDOFF.md`
- Never fake checked_at/queue/ETA; partial phases keep last confirmed timestamps. — `SYNC-RUNBOOK.md`
- Owner decides only creative/editorial choices, ambiguous task↔Scene mapping, approval, rerender, deletion/closing; deterministic work is done by the agent; never ask for info already in sources. — `AI-PROJECT-GUIDE.md`
- Every copyable prompt is self-contained: identity lock, reference roles/priority, camera/space, timeline, native audio, negatives, FRAME FILL. — `PROMPT-STYLE-GUIDE.md`
- Material workflow/site/authority/recovery change → relevant canonical docs + SAME handoff → cert_github.py certificate → push to main → Notion pointer → backup copies (best-effort). — `SYNC-RUNBOOK.md`
- Agents may launch only owner-authorized queue items via the website in Unlimited mode at zero credits. Paid Topview launches are performed only by the owner. — `SYNC-RUNBOOK.md`
- Library is best-effort, never a completion gate. — `SYNC-RUNBOOK.md`
- Never say «готово» before the relevant read-back/verification passed. — `SYNC-RUNBOOK.md`

## Прочитать под задачу

- `ops/TOPVIEW-EVENT-WAKE.md`
- `automation-monitor-status.json`
- `reports/topview-event-wake.json`
- `ops/topview-launch-queue.json`

## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 48

## Пробелы

Нет ошибок локальной проверки. Живые проверки выше обязательны.
