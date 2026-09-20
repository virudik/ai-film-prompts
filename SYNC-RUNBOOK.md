# SYNC-RUNBOOK v4.0 — AI Film Project

**Дата актуализации:** 20.09.2026  
**Назначение:** пошаговая инструкция записи, синхронизации, проверки и recovery для master, инструкций, сайта и связанных зеркал.

## 1. Обязательный preflight перед любой записью

Редактор сначала читает весь seven-document takeover set:

1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

Затем:
- fresh Drive `video-prompts.md`;
- live GitHub `project-status.json`;
- live `topview-status.json`;
- live `instruction-sync-status.json`.

Для prompt work дополнительно обязательно fresh-read `PROMPT-STYLE-GUIDE.md` + 1–2 релевантные master-сцены.

Для story/editing work — `film-analysis.md`, `film-backlog.md`, при необходимости `PROGRESS.md`, монтажный HTML и Notion `Кино`.

Перед первой записью окружение должно подтвердить:
- read exact Drive master ID;
- same-ID Drive write;
- GitHub read/write;
- возможность проверить workflow/status/Pages.

Если same-ID Drive write недоступна, агент review-only.

## 2. Канонические Drive IDs

Folder:
`1mRBfoh5ljjINMWKolxG-ciRcitOp-VW6`

Prompt master:
`video-prompts.md` → `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`

Seven-document instruction/recovery set:
- `NEW-CHAT-HANDOFF.md` → `1lRLQZkxo6Kh6MDx8StS_c5M8cjfHDxnD`
- `SYNC-RUNBOOK.md` → `1l7xXu9RDqffwJeLsc3UoPrVnx0HEdne4`
- `AI-PROJECT-GUIDE.md` → `1fwklz2CLoCBDpGnGyaPfiPnEqlKz8Q2u`
- `PROMPT-STYLE-GUIDE.md` → `14VzE8DwjKIquGJWENci6rYWj_1xEn34d`
- `USER-GUIDE.md` → `1rEmigK5FEznmzo9g3yANlXRwNiPRwvbO`
- `README-AI-SYNC.md` → `1hYMZ14esluB-kucasD6LjHWb_cBW_3wX`
- `BACKUP-AI-RUNBOOK.md` → `1WwKoxhC7tGNG9xy-I7OduKYZBhVH0Ss1`

Никаких `v2`, `final`, `copy` вместо этих файлов.

## 3. Routine: изменить существующую scene / prompt

1. Fresh-read exact Drive master.
2. Найти exact Scene ID.
3. Проверить slow-lock и `scene-meta`.
4. Если prompt materially меняется — fresh-read `PROMPT-STYLE-GUIDE.md`.
5. Изменить только нужный scene block и связанные TOC/count/status/meta.
6. Сохранить **в тот же Drive file ID**.
7. Убедиться, что raw Markdown UTF-8 without BOM.
8. Обновить GitHub `SYNC-TRIGGER.txt`.
9. Дождаться `sync-from-drive.yml`.
10. Проверить validator.
11. Проверить Drive master == GitHub `video-prompts.md`.
12. Проверить `project-status.json`.
13. Проверить Pages build.
14. Если сцена slow — не менять Topview mapping без доказанной необходимости.
15. Только затем сообщать `ГОТОВО`.

## 4. Routine: добавить новую scene

Перед добавлением:
- fresh-read master;
- получить `latest_scene`;
- учитывать удалённые historical IDs;
- не переиспользовать удалённые номера;
- если следующий ID однозначен, не спрашивать пользователя.

Добавить:
- anchor;
- заголовок `## Сцена N`;
- `scene-meta`;
- human wrapper: контекст / референсы / что происходит;
- полный master-level prompt;
- TOC row;
- counts/revision/current-state text, только где это действительно current;
- slow marker/table только если генерация реально запущена или пользователь явно перевёл сцену в canonical slow.

После — полный routine sync из раздела 3.

## 5. Routine: удалить/закрыть scene

Scene удаляется из active master только когда пользователь подтвердил, что результат принят и prompt больше не нужен.

Topview `success` сам по себе не является approval.

При удалении:
- убрать section;
- убрать TOC;
- убрать current slow entry, если применимо и пользователь это решил;
- обновить counts;
- **не переиспользовать Scene ID**;
- проверить зависимости других scene-meta;
- sync/validate/Pages.

## 6. Routine: site-only UI change

Site-only изменения делаются в GitHub `index.html`, если они не меняют prompt data.

После изменения:
1. JS syntax check;
2. duplicate HTML IDs check;
3. проверить отсутствие секретов;
4. проверить, что scene/prompt data по-прежнему грузится из master/status, а не hard-coded;
5. commit;
6. дождаться Pages;
7. проверить текущий UI/code state.

Если функция становится постоянной частью архитектуры — применить **Material Change Documentation Rule** из раздела 9.

Текущий baseline:
- merged slow/Topview;
- sync lightsaber;
- active scene map;
- references;
- light/dark theme;
- collapsible `Контрольный отпечаток`;
- отдельная collapsible `💬 Комментарии, идеи и предложения` сразу под ним;
- native Supabase comments/replies без GitHub login;
- старой кнопки `Архив GitHub` нет.

## 7. Routine: instruction change

Google Drive — authority.

Если меняется правило:
1. определить все затронутые документы;
2. fresh-read их Drive originals;
3. изменить SAME Drive IDs;
4. если изменение важно следующему чату — обновить SAME `NEW-CHAT-HANDOFF.md`;
5. если изменился prompt standard — обновить SAME `PROMPT-STYLE-GUIDE.md`;
6. exact-mirror Drive → GitHub;
7. re-read Drive + GitHub full text;
8. обновить `instruction-sync-status.json`;
9. проверить `project-status.json` не содержит `instruction_sync_stale/error`;
10. обновить Notion operational pointer, если меняется будущий workflow;
11. обновить Library recovery copies.

Автоматический repair допускается только **Drive → GitHub**.

## 8. `instruction-sync-status.json`

Status должен описывать **все семь** обязательных документов.

Для каждого:
- exact Drive file ID;
- Drive modified_at;
- GitHub blob SHA;
- `match: true/false`.

Общие поля:
- fresh `checked_at`;
- `health`;
- `all_match`;
- `freshness_max_hours`;
- `semantic_check`.

Нельзя оставлять старый five-file snapshot как якобы current после расширения recovery set.

Если status stale, сам факт stale не означает повреждение master; это означает, что verification нужно обновить.

## 9. Material Change Documentation Rule

Изменение считается материальным, если меняет способ работы следующих чатов или архитектуру проекта:
- новая постоянная функция сайта;
- новый backend/integration;
- новый обязательный prompt rule;
- смена authority/source of truth;
- новый status/workflow;
- новый recovery rule;
- новый обязательный документ;
- изменение способа синхронизации.

Такое изменение **не завершено**, пока:
- relevant Drive docs не обновлены;
- HANDOFF не обновлён;
- prompt guide обновлён, если касается prompt-writing;
- GitHub mirrors не синхронизированы;
- instruction status не refreshed;
- Notion operational pointer не обновлён, если меняется workflow;
- Library recovery mirror не refreshed.

Runtime telemetry (queue/ETA/SHA) не нужно копировать во все docs: её читают live.

## 10. Topview telemetry

Canonical slow membership:
`project-status.json.slow_scenes`.

Для каждой slow scene:
- exact task mapping;
- сравнение task prompt/references с fresh canonical scene;
- `verified=true` только при доказанном match;
- queue_count только из exact task;
- provider ETA только из exact task;
- historical ETA отдельно;
- `success` не снимает slow-lock.

Нельзя:
- remap из-за старого handoff/title;
- копировать одну очередь на все сцены;
- автоматически rerun;
- автоматически approve.

## 11. Comments / Supabase

Backend:
- Supabase project `ai-film-comments`
- ref `vzohfatqzyioydtgjiyd`
- organization `Vint`
- Edge Function `submit-comment`

Security baseline:
- public read published comments;
- anonymous post/reply;
- RLS;
- honeypot;
- 5 сообщений / 10 минут / IP;
- frontend publishable key only;
- no service_role in public code;
- no permission to mutate master/status/generation.

Любое изменение этой архитектуры документировать как Material Change.

## 12. Library recovery maintenance

Library — recovery mirror/cache, not authority.

После материальных instruction/handoff changes обновлять Library copies:
- all seven docs;
- `READ-FIRST.txt`;
- `CURRENT-STATE.json`;
- `SITE-STATUS.md`;
- `SHIFT-HANDOFF.md`;
- recovery ZIP, если он поддерживается как актуальный пакет.

Library copy никогда не должна молча переопределять более свежий Drive.

## 13. Notion maintenance

Notion `Кино` — story/history/idea bank.

Операционный указатель:
`AI Film — Актуальная инструкция / Handoff`.

При material workflow change обновить указатель, чтобы он:
- указывал Drive как authority;
- перечислял current seven-document takeover set;
- не выдавал старые prompts за master.

`Важные промты` — legacy idea/prompt bank; использовать как reference/history, не как текущий standard.

## 14. Recovery / known failures

### Non-fast-forward / concurrent writers
Sync должен refetch latest `origin/main`, rebuild status и retry push; не перетирать более свежий telemetry commit.

### UTF-8 BOM
Master должен быть UTF-8 without BOM. Workflow может strip optional BOM до validation, но канонический raw master хранится без BOM.

### Stale instruction status
Refresh exact comparisons; не объявлять master broken только из-за старого timestamp.

### Historical/current semantic conflict
Исторический checkpoint не является live invariant. Current claims должны быть единичными и чётко помеченными.

### Topview false mismatch
Сравнивать exact task с fresh current scene body, а не с памятью/старым title.

## 15. Verification before final answer

Для master change:
- exact Drive same-ID write confirmed;
- workflow success;
- validator success;
- Drive/GitHub mirror match;
- project-status current;
- Pages success.

Для instruction/material change:
- all seven Drive docs contain new rule;
- all seven GitHub mirrors exact-match Drive;
- fresh instruction-sync-status all seven;
- project-status no stale/error instruction warning;
- Notion pointer current;
- Library recovery current.

Не писать пользователю `ГОТОВО`, если relevant verification не завершена.
