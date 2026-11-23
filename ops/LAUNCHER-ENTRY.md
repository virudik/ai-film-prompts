# Одна команда для Dot и Grok: launcher_entry

Статус: действует. Проверено: 23.11.2026.

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

- **Fail-fast после CAS:** `isError=true`, transport error, отказ compare-and-swap или неопределённый ответ останавливают переход к следующей фазе. Fetch/readback сначала; только exact подготовленный own payload на main допускает intent/verify. Успешный HTTP/tool result без exact readback тоже недостаточен. При отсутствии claim **не запускать intent**. Ранний read-only precheck теперь отвергает это до нового `.busy`; та же проверка повторяется под marker против гонки. Старые markers не удаляются.
- **Race только до публикации claim:** при обычном продвижении main не повторять старый whole-queue blob и не force. В том же непрерывном исполнении, при session=claim_prepared и отсутствии marker, можно `launcher_entry.py . refresh-claim --request ... --session ...`. Wrapper проверяет сохранённые base item/main SHA, ancestry и каждый commit main: item должен быть неизменным, ledger тоже. Publish-then-revert, изменённый item/ledger, чужая lease, неизвестная отправка, другая execution identity или phaseintent/verify запрещают этот путь. Старые session без base evidence не дополнять догадками. Затем заново полный prepare_claim со fresh queue/priority/scan/route/lease/preflight; claim ID остаётся прежним, transaction и expected_main_sha новые. Это не публикация: снова отдельная CAS/readback; лишь после неё intent. После потери управления или неоднозначного результата — reconciliation, не refresh.
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

### Отдельная доказательная схема: source-bound abort до step

Если numeric Python exit не был отдельно записан из-за foreground shell `python … claim … >stdout; head …`, не подставлять `exit_code=2` в strict assessment выше. Допускается отдельный независимо проверенный **source-bound** вывод только при совокупности: полный terminal tool transcript без truncation/timeout с точным snapshot-rejection JSON; историческая привязка к проверенному legacy source SHA256 выше и его relevant imports через сохранённый clean checkout → известную цепочку checkout без правок кода; учтены все последующие вызовы; второй вызов, если был, завершился только FileExistsError на прежнем marker; старый worker остановлен и не продолжает фазы. Нынешний hash без этой цепочки недостаточен.

Записывать отдельно **observed** (shell exit0, Python exit unknown, оригинальный stdout утрачен/перезаписан, сохранён реконструированный tool transcript) и **derived from reviewed source** (exclusive marker создан этим invocation, snapshot error возник до step/claim transaction, foreground child завершился до head). Исторические байты request не нужны для доказательства отсутствия step; `request_read=false` не утверждать, если не различён первый/второй snapshot. Новая попытка всегда использует заново проверенный request. Это не прохождение strict checker и не разрешение удалить marker.

Source-bound assessment подтверждает только прежний abort. Для abort receipt и новой начальной попытки полностью сохраняются шаги3–6 выше: свежая сверка actual peer/lease/queue/history/ledger/full live scan, собственная редакторская lease/CAS/readback, затем ещё одна свежая проверка и обычный claim/intent/verify. Source assessment без live reconciliation не объявлять разрешением на новую session или Create. В публикуемый assessment входят только allowlisted факты/выводы и hashes приватных свидетельств, не их локальные пути/сырой request.

### Отдельная схема: claim не публиковался, старый intent marker сохраняется

Это узкое source-bound reconciliation, **не** strict exit-2/pre-step исключение и не продолжение старой session. Применимо к известному wrapper SHA256 `9eb35e9e0555c91c2d81d28bc9a85b0a4e7dff5e10db8124db8253bd322b4aa0`: он читает immutable main snapshot и сравнивает digest целого item с `session.expected_item_sha` **до** `prepare_transaction`. Само наличие error file, отсутствие task в очереди или истечение lease ничего не доказывают.

1. Сохранить неизменными старые session, busy, pending (если есть), prepared claim и error. Для этого исключения необходимы исходная `claim_prepared` session, точный подготовленный claim payload с тем же claim_id/digest и expected_main_sha; busy ровно phase=intent, pending отсутствует. Любые intent_prepared/verify_consumed, неизвестные дополнительные вызовы или неподтверждённый источник требуют отдельного разбора. Старый worker явно прекращает управление и не имеет отложенного claim/intent/verify/Create. Не заменять это одним ps, provider completed или отсутствием сообщения.
2. Независимо проверить привязку фактически использованного неизменённого source к известному хешу и его snapshot/readback gate; зафиксировать ограничения, если exact argv/exit утрачен. Не выдавать текущий source hash за доказательство исторического исполнения. `python_exit_code_observed=null`, original command unknown сохраняются; summary и artifact не становятся raw transcript.
3. Проверить полный сохранённый граф main от expected_main_sha подготовленного claim до текущего main, включая промежуточные commits (не только последний снимок): исходный expected item digest никогда не встречался, никакого claim/intent/task/истории отправки/расхода попытки у item нет, ledger не содержит соответствующей попытки. Допустим только непрерывный waiting_for_slot либо документированный blocked_recovery; hold не стирать для проверки. Publish-then-revert, разрыв истории, shallow-граница внутри проверяемого диапазона, force-rewrite/неучтённые refs или иной источник делают вывод недостаточным. `scripts/no_published_claim.py:assess` проверяет Git/item/payload часть read-only; ledger, actual source binding, остановка исполнителя и live UI проверяются отдельно, не подделываются входными boolean.
4. Вывод ограничен: **в сохранённой ancestry нет payload, необходимого этому reviewed helper для подготовки intent**. Это не абсолютное доказательство отсутствия ручного/внепротокольного Create. Поэтому обязательна новая полная live сверка всех досок и точного item по normalized prompt, входам, task IDs и временному окну; неоднозначность/совпадение — reconcile существующего task, не новая попытка. Проверить всех активных peer и актуальные claims/history/ledger. Старый scan, новый час и TTL не разрешают отправку.
5. После независимого review взять собственную короткую редакторскую lease штатным CAS/readback; при изменении source/item/peer/lock остановиться и сверить заново. Сохранить отдельный отчёт в reports/preclaim-aborts с observed/derived/limitations, hashes, границами полного графа и живой сверкой, без private paths/request/секретов. Если recovery hold был единственным blocker и все условия доказаны, допустимо **в этой же CAS** вернуть его previous_state=waiting_for_slot, сохранив recovery_hold как resolved с указателем на отчёт. Не менять priority, разрешения, историю, retry/расход, claim/task IDs; не выдумывать их отсутствие. Освободить только свою lease, перечитать результат. Пока отсутствует хотя бы одно доказательство, hold остаётся.
6. Отчёт всегда create_allowed=false и new_session_allowed_by_this_report=false. Он фиксирует reconciliation, а не выдаёт runtime permit. После опубликованного разрешения hold новый genuine runtime может начать только новый обычный initial claim с новой локальной session и всеми свежими guards, независимым полным live scan, собственными lease/CAS/intent/verify; старую session/marker не удалять, не продолжать и не переименовывать для обхода. Не повторять неопределённый Create. При новых конкурирующих действиях/unknown остановиться. Это не повышение retry budget и не обход S89E или другого уже submitted результата.
