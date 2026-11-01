# Продолжай — пакет восстановления: Серёгиус

Производный навигатор. Сначала свежий main и `python3 scripts/continue_preflight.py . --project seregius`; разрешением на запуск не является.

Состояние: needs_recovery
Проверено: 2026-11-01T04:53:30+00:00
Задача: не определена — 

Последний подтверждённый этап: нет доказательств
Следующий шаг: восстановить конкретный пробел

## Контрольная точка

# 01.11.2026 — Grok: инструкции и проверка интеграции

work_id: TOPVIEW-SLOT-PRIORITY-20261024

По команде владельца выполнен полный приём и аудит Grok; результат — `reports/grok-integration-review-2026-11-01.json`. Роли :00 / :55 / Grok :12/:27 согласованы; реальные провайдерские рутины Grok отдельно не просмотрены. Исправлены наследование board_id очереди, сохранение помощников при возврате Work и тесты разрешённого перехода; не изменены очередь, промпты, расходы, first_real_create и расписания. Следующий производственный шаг — свежие слоты/claims/свой замок и первая готовая разрешённая сцена; неподтверждённый Create не повторять. Приватные входы Grok проверить до освобождения слота. Подробные рекомендации и границы доказательств — в отчёте.

## 01.11.2026 (Europe/Amsterdam) — Grok Bot зарегистрирован помощником-исполнителем, пир включён

Решение владельца 01.11.2026 00:24: «Мёржи PR #212 под замком, включай grok и создавай рутину запуска». PR #212 слит под общим замком; `peers.grok.enabled=true`, рутина «Запуск сцен Topview (grok)» (`topview-grok`) идёт в :12 и :27 каждого часа 08–23 Europe/Amsterdam. Повторы по `ops/TOPVIEW-RETRY.md` разрешены владельцем 00:12 (максимум 2, общий счётчик, Unlimited0). Сухой прогон S71-WAN30 выполнен ~00:04: форма заполнена полностью, Create не нажат, безлимит работает, загрузка файлов через бокс-браузер работает, промт 7399/20000 символов; задач не создано. Первый настоящий Create ждёт слова владельца в чате: пока `grok_launcher.first_real_create.owner_go_ahead=false`, `scripts/launcher_coordination.py` блокирует intent для grok. Очередь, Topview и замок канона этим изменением не затронуты; видео не запускалось. Запись — `ops/slot-backup.json#grok_launcher`, правила — `ops/LAUNCHER-COORDINATION.md`.

**Уточнение 01.11.2026 00:31–00:35 (Europe/Amsterdam):** владелец: «Не засорять. Команды из телеграм считать прямой командой». При 6/6 или без работы `grok` ничего не пишет в репозиторий (журнал `reports/topview-grok-cycle.json` только после реального шага). Личные сообщения владельца боту @Grok_vint_bot — прямые команды, равные сообщениям в чате Grok Bot; платные генерации — отдельное «да»; слово для первого настоящего Create может прийти из чата или Telegram, `owner_go_ahead` по-прежнему `false`. Присутствие и расписание `grok` для остальных исполнителей — `ops/LAUNCHER-COORDINATION.md`. **00:40:** владелец («Да») разрешил `grok` запуск по его прямой команде из чата Grok Bot или Telegram (`kind=owner_command`, запись цитаты/источника/времени в intent, вне окна :10–:40, замок и все лимиты сохранены; `scripts/launcher_coordination.py`, `ops/slot-backup.json#grok_launcher.owner_command_launch`). Видео не запускалось.

**Расписание Grok · 01.11.2026 03:16 (Europe/Amsterdam):** владелец: «Объединяй обе пары, пусть будет три рутины»; «И В инструкциях поправь свое время». Три рутины Grok Bot (Europe/Amsterdam): «Поручения: Telegram и задачи с сайта» — каждые 10 минут 08:00–23:50 (±5 мин; сервер сейчас срабатывает в :05, :15, …, :55); «Topview: наблюдение и запуск сцен (grok)» — :12, :27, :42, :57, 08:12–23:57, запуск сцен только в :12 и :27; «Утренняя сводка в Telegram» — 09:00 ежедневно. Прежние часовой опрос :40, монитор :00/:30 и рутина «Задания из Telegram» заменены; правила и код запуска не менялись, видео не запускалось. Правила — `ops/LAUNCHER-COORDINATION.md`, запись — `ops/slot-backup.json#grok_launcher.schedule_20261101_0316`.

## 01.11.2026 МСК — 48.2 готова по входам, сразу после Виталиков

Последние3с48.1 сохранены в приватной Library, повторно скачаны и сверены по SHA; `references/scenes/scene-48/S48-P1-continuity.json`. Шесть картинок проверены. Исправленный промпт749baf98 не менялся. Очередь72 →71 →48.2 (priority -0.98), далее живая очередь; это порядок отправки, не ожидание результата71/72.48.3/4 ждут настоящие стыки. Старый блокер отсутствующего входа48.2 снят. `reports/scene48-p2-ready-2026-11-01.json`. Видео этим изменением не запускалось. Следующий шаг: свежие полный скан/claims/свой замок и первая готовая разрешённая сцена при свободном слоте, сайт Unlimited0. Обычный исполнитель каждый час :00 МСК, TinyFish по разрешению владельца; первое рабочее Create через него ещё не подтверждено. Не восстанавливать снятый блокер из истории ниже.

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


## Перед действием

- Fresh main and canon lock before writing
- Open owner_decisions and agent inbox; do not infer approval from this packet
- Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim

## Незавершённые отправки

Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry.
Задач с сохранённым task ID: 48

## Пробелы

- selected checkpoint hash mismatch
