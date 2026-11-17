# Одна команда для Dot и Grok: launcher_entry

Обёртка над `launcher_coordination.py`, не новый launcher и не обход защиты. Одинакова для Dot (`ordinary`), Work и Grok. Очередь, разрешения, глобальная lease, CAS и ledger остаются прежними. Ничего не отправляет в Topview, не получает замок и не публикует GitHub сама. **Отдельный CAS между фазами обязателен.**

## Короткая последовательность

```sh
python3 scripts/launcher_entry.py . plan --request /tmp/launch-request.json
python3 scripts/launcher_entry.py . claim --request /tmp/launch-request.json --session /tmp/launch-session.json > /tmp/claim-transaction.json
# CAS publish claim-transaction.files with expected_main_sha; fetch/readback main
python3 scripts/launcher_entry.py . intent --request /tmp/launch-request.json --session /tmp/launch-session.json > /tmp/intent-transaction.json
# CAS publish ALL intent-transaction.files together with expected_main_sha; fetch/readback main
python3 scripts/launcher_entry.py . verify --request /tmp/launch-request.json --session /tmp/launch-session.json
# Only on checks_passed:true: exactly one UI Create, immediately, in THIS uninterrupted execution
```

Перед `claim` отдельно получить собственную точную lease и прочитать её обратно. `plan` только показывает следующий готовый пункт и состояние замка, не резервирует слот и не утверждает, что live-слот свободен. При 6/6, чужом замке или неготовой форме отправка не разрешается.

Каждая команда обновляет `origin/main` через read-only `git fetch`. Guards читают отдельный временный снимок из Git blobs этого commit, а не изменяемые файлы checkout; даже скрытые `assume-unchanged`/`skip-worktree` правки не становятся readback. Перед выдачей результата main сверяется повторно. Checkout должен в точности соответствовать свежему `origin/main`, без изменений отслеживаемых файлов. Если HEAD устарел, команда откажет: перейти на свежий main обычным безопасным способом, сверить новое состояние и не переносить старые разрешения на Create. Не использовать `reset --hard` поверх чужой работы. Рабочий checkout может быть отдельным worktree. Локально изменённая очередь и локальный непубликовавшийся commit не считаются readback.

## Один файл запроса вместо повторения ID и SHA

`/tmp/launch-request.json` содержит:

```json
{
  "actor": {"...": "тот же полный реальный actor, который требует launcher_coordination.py"},
  "item_id": "точный ID из очереди",
  "preflight": {"...": "фактически проверенная готовая форма и все исходные guard поля"},
  "scan": {
    "complete": true,
    "checked_at": "реальное UTC время полного скана",
    "free_slots": 1,
    "item_reconciliation": {
      "точный ID из очереди": {
        "complete": true,
        "matched_task_ids": [],
        "ambiguous": false
      }
    }
  }
}
```

Это описание структуры, **не готовое доказательство проверки**. Actor сохраняет execution UUID, реальную surface/kind, route generation, точное время собственной lease и все поля разрешённого пути. Для Grok сохраняются genuine run/event identity и исходное разрешение; wrapper не выдумывает их. Preflight остаётся полным по действующему протоколу (полный prompt и input SHA/order/QC, owner_authorized, Unlimited0, модель, параметры). Бесплатность не выводится из отсутствия цены. `scan` обновляется фактическим полным сканом перед соответствующей фазой; данные старше 120 секунд или неоднозначные совпадения блокируют действие. Обёртка сама аккаунт не сканирует.

## Что хранится и что публиковать

- Вывод `claim` / `intent` содержит `expected_main_sha` и `files`. Это подготовленный JSON transaction, **не факт публикации**. Сериализовать каждое значение `files[path]` в JSON и публиковать все указанные пути одним GitHub CAS с этим expected SHA. Отказ CAS: свежая сверка, не force и не слепой повтор.
- Private session автоматически сохраняет исходные claim/intent IDs, SHA payload, actor и фазу. Их больше не надо копировать вручную. Сессия находится **вне checkout** и никогда не публикуется вместе с request/личными техническими входами.
- `intent` принимает только точный readback ранее подготовленного claim. `verify` принимает только точный readback исходного intent и проверяет все прежние guards, включая ledger.
- До выдачи результата `verify` локальная фаза становится `verify_consumed`. Повтор этой команды с той же сессией запрещён. `.busy` защищает от одновременного входа в фазу и остаётся при сбое после её начала. Marker создаётся только после двух read-only проверок свежего snapshot, но до чтения локальной session и вызова step; чистый отказ snapshot до входа в фазу не создаёт новый marker. Уже существующий marker эта проверка не удаляет и не разблокирует. При ошибке, потере вывода, разрыве исполнения или таймауте не удалять marker и не создавать новую сессию ради повторного Create: только reconciliation по общему протоколу.
- Сессия не является возобновляемым разрешением. Даже если файл сохранён, новый чат/процесс управления после разрыва исполнения не имеет права продолжить старый intent. Обычные последовательные CLI-вызовы одного непрерывного агента допустимы; возобновление после неизвестного исхода нет.
- После единственного Create сохранить настоящий task ID/receipt либо неизвестный исход, затем освободить только свою lease. Эти шаги не автоматизированы wrapper и остаются обязательными.

Совместимость: исходные команды `launcher_coordination.py` не меняются. Обёртка сокращает количество ручных аргументов, но не заменяет проектный протокол и не заставляет сторонний браузер соблюдать его. Внедрение у второго агента подтверждается его собственной read-only квитанцией, не тестовым видео.

## Узкое reconciliation: доказанный отказ до первоначального claim

Это исключение касается только **первой попытки claim, которая доказанно завершилась до вызова `step`**. Оно не снимает `.busy`, не продолжает старую сессию и не разрешает Create. Для intent/verify, crash, timeout, потери/обрезки вывода, неизвестного процесса или результата действует прежний запрет и общий reconciliation.

1. Сохранить неизменными marker, request, полный stdout и терминальный результат именно того command invocation. Нужны фактические argv/identity, exit=2, доказательство завершения процесса и управляющей обёртки, а также что marker отсутствовал до вызова и создан им. Один `ps`/PID или предположение по времени не являются доказательством. Связать SHA256 полного stdout и неизменного исходного request с фактической записью runner/argv; item_id и actor должны точно совпадать с исходным request, не подставлять другую задачу; не заполнять недостающие доказательства догадками.
2. Разрешён только известный старый исходник `launcher_entry.py` с SHA256 `76b2b7e15a8394e70ad1338148f50ee03006fc0c89d8ef552a0bfd95e76fca31`, где marker создавался до snapshot. Marker содержит ровно `{"phase":"claim"}`; session и pending отсутствуют. Полный stdout содержит только `checks_passed=false`, `create_allowed=false` и один из pre-step отказов: `checkout_must_equal_fresh_origin_main`, `tracked_checkout_must_be_clean`, `main_changed_during_phase; reconcile_without_Create`. Иной исходник требует отдельного review, не расширять список на ходу.
3. Сделать read-only сверку **текущего** исполнителя, свежего main/route/очереди/history/ledger и полный live scan всех досок с reconciliation точного item. Lease должна быть явно free; чужую, даже просроченную или неоднозначную, эта процедура не снимает. Item должен оставаться waiting_for_slot без claim/intent/task и без истории попыток/архива/ledger-записи; совпавший или неоднозначный live task запрещает исключение. Grok мог уже забрать слот: старый снимок или отсутствие ответа не доказывают обратного.
4. `assess_preclaim_abort` формирует только read-only assessment для записи abort receipt. Входные process/provenance берутся из настоящего command runner; функция не удостоверяет выдуманные поля. В публичный результат входят только allowlisted поля и hashes доказательств, не полный process_result/argv/локальные пути. Результат всегда `create_allowed=false`, `new_session_allowed_by_this_report=false`; marker остаётся неизменным. Missing/uncertain evidence означает отказ от этого исключения, а не разрешение удалить marker.
5. Если всё доказано, взять **новую собственную короткую редакторскую lease** обычным CAS/readback, вновь сверить main, очередь/history/ledger и текущие действия других исполнителей. При изменении item, появлении claim/intent/task или занятой lease остановиться. Сохранить abort receipt с hashes исходных доказательств и текущих main/item/scan под `reports/preclaim-aborts/`; не публиковать секреты, private request или локальные пути. Освободить только свою lease и прочитать сохранённую квитанцию. Receipt не резервирует слот и не меняет очередь, retry budget или старые markers.
6. Только после этого допускается **совершенно новая начальная попытка claim**, с новой локальной session, не продолжение intent/verify. Перед ней заново проверить fresh main, разрешённый настоящий actor/generation, доступность слота и полный live scan/reconciliation, затем собственная lease и весь обычный claim → CAS/readback → intent → CAS/readback → verify → единственный Create. Снимок до abort receipt не переносить. Если другой исполнитель уже начал или задача отправлена/неоднозначна, новой попытки нет.

Этот протокол не даёт права повышать retry counter, повторять Create или обходить owner/QC/стык/Unlimited0. Не удалось доказать начальный abort — сохранять блокировку и позволить другому штатному исполнителю независимо сверить очередь по общему протоколу, не навязывая ему запуск.
