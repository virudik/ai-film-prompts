# AI Film «Серёгиус»: квест трёх ключей

**Цель:** GitHub Actions получает решения панели сайта из Supabase, безопасно изменяет *тот же* файл `video-prompts.md` в Google Drive, пересобирает GitHub Pages и в перспективе отслеживает видео/шесть бесплатных слотов Topview без включённого компьютера и лимитов Claude/ChatGPT Work.

**Внимание:** на 11.10.2026 есть готовые частичные workflow, но полный автономный цикл ещё **не подтверждён**. Одни лишь ключи его автоматически не включат. Особенно публичный Topview API пока не подтверждён как источник полного списка board tasks и точных 6 бесплатных слотов. До проверки Topview-счётчик обязан показывать «нет подтверждённых данных», а не выдумывать 0/6.

## Общая точка назначения

**GitHub:** https://github.com/virudik/ai-film-prompts/settings/secrets/actions

Каждый ключ: **Settings → Secrets and variables → Actions → Secrets → New repository secret**. Указывать имя переменной в поле **Name**, секрет целиком в поле **Secret**, нажать **Add secret**. Никогда не вставлять секреты в репозиторий, Issues, сайт, комментарии, чат, скриншоты или файлы master.

**Важно:** под «тремя ключами» имеются в виду Google service account, Supabase secret, Topview API key. Для Topview дополнительно потребуется **UID** — это идентификатор, не отдельный ключ. Для будущего ИИ-редактора свободных промтов может понадобиться ещё ключ отдельной языковой AI API; для обычных кнопок он не требуется. GitHub автоматически предоставляет `GITHUB_TOKEN` своим Actions — персональный GitHub PAT не нужен.

## Ключ 1 — Google Drive: `GDRIVE_SA_KEY`

1. Открыть https://console.cloud.google.com/ и выбрать или создать отдельный проект, например `ai-film-automation`.
2. Открыть https://console.cloud.google.com/apis/library/drive.googleapis.com и **Enable** Google Drive API в этом проекте.
3. Открыть https://console.cloud.google.com/iam-admin/serviceaccounts → **Create service account** → имя `ai-film-writer`. Это отдельный технический аккаунт, не твой Google-пароль. Для самого проекта Google Cloud не назначать чрезмерных ролей.
4. Открыть созданный service account → **Keys → Add key → Create new key → JSON → Create**. Google скачает `.json` однократно; сохранить вне публичных папок.
5. Скопировать из JSON поле **`client_email`** (`…@…iam.gserviceaccount.com`). Открыть в Google Drive папку **AI Film Prompts Master** (ID `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`), **Поделиться → Ввести client_email → Редактор → Отправить/Поделиться**. Не делать общедоступной, не давать боту доступ ко всему «Моему диску». При необходимости проверить, что именно исходный мастер ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj` наследует доступ.
6. В GitHub Secrets создать имя **`GDRIVE_SA_KEY`** и вставить **полное содержимое JSON**, начиная с `{` и заканчивая `}` — не путь к файлу, не email, не значение `private_key` отдельно.
7. После этого сделать пробу через существующий `.github/workflows/drive-write.yml`: idempotent same-ID запись тестового документа, затем разрешённая правка мастера с `base_sha256`, повторное скачивание того же file ID, сравнение SHA, `SYNC-TRIGGER`, статус `project-status.health=ok` и Pages success. До реального `applied` не считать пункт внедрённым.

Официально: https://docs.cloud.google.com/iam/docs/keys-create-delete ; https://support.google.com/drive/answer/7166529

## Ключ 2 — Supabase: `SUPABASE_SERVICE_ROLE_KEY`

1. Открыть **только свой проект** https://supabase.com/dashboard/project/vzohfatqzyioydtgjiyd/settings/api-keys .
2. Для текущего репозиторного обработчика `scripts/process_owner_decisions.py` готовым вариантом остаётся **Legacy `service_role`** (`eyJ…`). Это привилегированный ключ серверной базы, **НЕ** публичный `sb_publishable_...`, **НЕ** пароль панели `OWNER_DECISION_KEY`. 
3. В GitHub Secrets создать имя **`SUPABASE_SERVICE_ROLE_KEY`** и вставить весь Legacy `service_role`.
4. GitHub workflow `.github/workflows/sync-from-drive.yml` (уже по расписанию `*/30 * * * *`) читает решения владельца, применяет безопасные однозначные кнопки к `review-ledger.json`, проверяет commit и только после него ставит `applied` в Supabase. Сам master этот этап пока не изменяет.
5. **Современный вариант для следующего обновления:** Supabase рекомендует новый `sb_secret_...` вместо Legacy; текущую HTTP-авторизацию обработчика нужно проверить/адаптировать на новый формат перед его подстановкой. Не отключать legacy, пока переход и end-to-end не протестированы.
6. Проверка: создать только контролируемую и безопасную заявку в панели → дождаться запланированного GitHub job (или запустить workflow вручную) → подтвердить status=applied **после** commit и отсутствие изменений чужих сцен.

Официально: https://supabase.com/docs/guides/getting-started/api-keys ; https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys

## Ключ 3 — Topview: `TOPVIEW_API_KEY` и идентификатор `TOPVIEW_UID`

1. Войти в https://www.topview.ai/ под аккаунтом, где находятся генерации AI Film.
2. На главной странице нажать аватар **в правом верхнем углу** → выбрать пространство/аккаунт → **API Settings → API**.
3. Там отображаются **Topview Uid** и **Key**. Если Key отсутствует, нажать **Add Key**. Это настоящий API key, а не пароль сайта и не OAuth-доступ ChatGPT.
4. В GitHub **Secrets** добавить **`TOPVIEW_API_KEY`** (весь Key без слова `Bearer`). В GitHub **Variables** рядом создать **`TOPVIEW_UID`** с точным Topview Uid. Если хочешь спрятать и UID, можно хранить его также в Secrets — но workflow должен ссылаться на соответствующее место.
5. Проверка только чтением: `GET` к официальному `https://api.topview.ai/v1/tts/list` с заголовками `Authorization: Bearer <TOPVIEW_API_KEY>` и `Topview-Uid: <TOPVIEW_UID>`. Ключи никогда не выводить в лог. Затем попробовать официальный Query Task для *известного* Task ID и оценить, видит ли public API **именно задачи бесплатной очереди досок**, а не отдельную API-генерацию.
6. Для нашего проекта недостаточно просто знать статус одного ролика: нужно подтвердить полный обзор всех досок/задач, `useUnlimitMode`, активные состояния и свободные слоты **из 6**. Если через public API этого нельзя получить, **не публиковать ложное «0/6»**; на сайте показывать «данные Topview не подтверждены» и оставить подключённый Topview-исполнитель до официального поддерживаемого способа.
7. Никаких `POST task/submit`, новых генераций, трат кредитов, автоматических approval/rerender/delete. Topview API-кредиты и условия веб-безлимита могут отличаться; получение Key не означает, что API-запуски бесплатны.

Официально: https://docs.topview.ai/reference/authentication-1 ; https://docs.topview.ai/reference/image-to-video-v2-text-to-video-omni-reference-api-usage ; https://docs.topview.ai/docs/billing-rules

## Итоговый алгоритм (после активации)

**Кнопки и задачи:** сайт `🔑 Владелец` → аутентифицированное решение в Supabase → существующая плановая GitHub Actions (`*/30 * * * *`) → защита от дублей и конфликтов → `review-ledger.json` либо same-ID `video-prompts.md` через Google Drive writer → валидатор `health=ok` → GitHub зеркало + Pages → запись `applied` и ссылки на результат. Текстовые творческие правки требуют редакционной модели, style guide, референсов, проверки continuity и явного решения при неоднозначности.

**Видео/медленная очередь:** Topview read-only API → проверка доступного покрытия и соответствия Task ID → карта scene↔task (без угадывания) → `topview-status.json`/сайт **только по реально подтверждённой полной выборке** → «занято N/6, свободно 6-N, время фактической проверки», техническое окончание отдельно от человеческой приёмки. Если API не обеспечивает полноту, источник и возраст данных помечаются, устаревшая статистика не выдается за свежую.

**Мониторы:** задачи Claude и ChatGPT/Work не выключать, пока облачная цепочка не проверена на реальных данных end-to-end. Не создавать дубли Recovery / slot watcher. Одновременно master меняет только один разрешённый исполнитель, с CAS SHA/readback.

## Флажки прохождения

- [ ] `GDRIVE_SA_KEY` в GitHub Secrets; сервисному аккаунту выдан Editor **на ограниченную папку**
- [ ] Есть `drive-write` → real `applied` → same-ID readback SHA → `project-status.health=ok` → Pages success
- [ ] `SUPABASE_SERVICE_ROLE_KEY` в GitHub Secrets; контролируемая кнопка привела к реальному commit и Supabase `applied`
- [ ] `TOPVIEW_API_KEY` в GitHub Secrets и `TOPVIEW_UID` в GitHub Variables
- [ ] Read-only Topview auth test прошёл, известный task ID проверен
- [ ] Подтверждён **полный** обзор безлимитных board tasks и занятости 6 слотов (или документирована невозможность публичного API)
- [ ] Зафиксирована в canonical Drive документах и handoff успешно проверенная новая архитектура

**Секреты сюда, в чат или в общедоступные файлы НЕ присылать.** Достаточно сообщения «ключи добавлены» без значений — дальше можно проверять Actions и статусы по логам.