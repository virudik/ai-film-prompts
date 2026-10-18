# Drive-копия без файла-ключа: настройка за ~10 минут (НЕ КАНОН, инструкция владельцу)

Статус: справка (настройка суточной Drive-копии через Workload Identity Federation). Проверено: 18.10.2026.

Политика Google вашей организации запрещает JSON-ключи сервисных аккаунтов (`iam.disableServiceAccountKeyCreation`) — **политику не трогаем и ключ не создаём**. Вместо ключа используется **Workload Identity Federation**: GitHub Actions сам доказывает Google, что он — репозиторий `virudik/ai-film-prompts`, и получает короткий токен сервисного аккаунта `ai-film-writer`. Секретов нет ни в GitHub, ни в чате, ни в файлах. Всё бесплатно.

**Зачем:** раз в сутки (03:20 UTC ≈ 06:20 МСК) робот обновляет Drive-копию (те же файлы: `video-prompts.md`, 7 инструкций, `film-backlog.md`, `film-analysis.md`) точными копиями из GitHub `main`. Канон на Drive не пишется. Если файл на Drive правили руками — робот его **не затирает**, а открывает issue `drive-drift`.

Что вы делаете: **(1)** вставляете один блок команд в Cloud Shell, **(2)** даёте адресу сервисного аккаунта доступ «Редактор» к одной папке на Drive, **(3)** записываете два значения в GitHub Variables, **(4)** нажимаете «Run workflow» для проверки и пишете мне «готово».

## 1. Cloud Shell: один блок команд

1. Откройте https://console.cloud.google.com/ . В верхней строке выберите **тот проект, где вы создали `ai-film-writer`** (сервисный аккаунт нужен именно из него).
2. Нажмите кнопку **«>_»** (Activate Cloud Shell) справа вверху. Подождите приглашения командной строки.
3. Вставьте целиком и нажмите Enter (имя репозитория уже подставлено):

```bash
PROJECT_ID="$(gcloud config get-value project)"
PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"
REPO="virudik/ai-film-prompts"
SA_EMAIL="ai-film-writer@${PROJECT_ID}.iam.gserviceaccount.com"
POOL="github"
PROVIDER="ai-film-repo"

echo "Проект: $PROJECT_ID ($PROJECT_NUMBER)"
gcloud iam service-accounts describe "$SA_EMAIL" --format='value(email)'   # должен вывести адрес; если ошибка — выбран не тот проект

# 1) включить нужные API (IAM Credentials, STS, Drive)
gcloud services enable iamcredentials.googleapis.com sts.googleapis.com iam.googleapis.com drive.googleapis.com

# 2) пул удостоверений и провайдер GitHub OIDC — пускает ТОЛЬКО этот репозиторий
gcloud iam workload-identity-pools create "$POOL" --location=global --display-name="GitHub Actions"
gcloud iam workload-identity-pools providers create-oidc "$PROVIDER" \
  --location=global --workload-identity-pool="$POOL" \
  --display-name="ai-film-prompts repo" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository == '${REPO}'"

# 3) разрешить именно этому репозиторию действовать от имени ai-film-writer
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/attribute.repository/${REPO}"

# 4) два значения для GitHub (это НЕ секреты, а идентификаторы)
echo
echo "=== Скопируйте эти две строки ==="
echo "GCP_WORKLOAD_IDENTITY_PROVIDER = $(gcloud iam workload-identity-pools providers describe "$PROVIDER" --location=global --workload-identity-pool="$POOL" --format='value(name)')"
echo "GCP_SERVICE_ACCOUNT            = $SA_EMAIL"
```

Если какая-то команда пишет `ALREADY_EXISTS` — этот шаг уже делали, это нормально: блок можно запускать повторно. Если проверка сервисного аккаунта (вторая команда) выдаёт ошибку `NOT_FOUND` — в верхней строке выбран не тот проект: переключите проект и вставьте блок заново. Если Google отвечает про организационную политику на создание провайдера — пришлите мне текст ошибки, обходной путь подберём (политику всё равно не отключаем).

## 2. Google Drive: доступ ТОЛЬКО к одной папке

1. Откройте папку **«AI Film Prompts Master»** (ID `1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`) → **Поделиться**.
2. Вставьте адрес из строки `GCP_SERVICE_ACCOUNT` (вида `ai-film-writer@…iam.gserviceaccount.com`) → роль **Редактор** → снимите галочку «Уведомить» → **Отправить**.
3. Не делайте папку общедоступной и не давайте этому адресу доступ ко всему «Моему диску».

## 3. GitHub: две переменные (Variables, не Secrets)

https://github.com/virudik/ai-film-prompts/settings/variables/actions → **New repository variable**:

| Name | Value |
|---|---|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | **ваша** строка из вывода Cloud Shell, вида `projects/<ЧИСЛО>/locations/global/workloadIdentityPools/github/providers/ai-film-repo` (ЧИСЛО — номер вашего проекта; копируйте строку целиком из вывода, не из этой таблицы) |
| `GCP_SERVICE_ACCOUNT` | **ваш** адрес из вывода Cloud Shell (`ai-film-writer@ИД-ПРОЕКТА.iam.gserviceaccount.com`, без угловых скобок) |

Пока этих переменных нет, workflow «Drive copy refresh» ничего не делает (`not_configured`) — это безопасно.

## 4. Проверка

1. https://github.com/virudik/ai-film-prompts/actions/workflows/drive-write.yml → **Run workflow** → `action = probe` (только чтение, ничего не пишет). В логе по каждому файлу: `current` (уже совпадает), `would_write` (копия отстала, будет обновлена), `drift` (на Drive правили вручную — не затрём).
2. Если проба зелёная — снова **Run workflow** с `action = sync`: файлы обновятся, робот перечитает их и сверит sha256, затем обновит `instruction-sync-status.json` (`scripts/cert_github.py . --drive-copy-dir …`).
3. Напишите мне «Drive готов» — дальше обновление идёт само раз в сутки.

**Типичные ошибки.** `invalid_target` — в переменную вставлен пример из инструкции вместо реального значения: возьмите две строки из конца вывода блока команд (если вывод потерян — вставьте последние две команды `echo` блока ещё раз).  `unauthorized_client` / `attribute condition` — опечатка в имени репозитория или провайдера в переменной. `403 … Drive API has not been used` — не включён Drive API (команда 1 выше). `File not found` — папка не предоставлена адресу сервисного аккаунта (шаг 2). Файл `film-analysis.md` ищется на Drive по имени внутри папки; если их там два или ни одного, робот его пропустит и скажет об этом в логе (ничего не создаёт).
