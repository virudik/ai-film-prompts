# BACKUP-AI-RUNBOOK v4.0 — резервный редактор AI Film

**Дата актуализации:** 20.09.2026  
**Назначение:** правила безопасного takeover для нового/резервного ИИ.

## 1. Нельзя начинать с редактирования

Новый агент сначала читает **все семь** обязательных документов:

1. `NEW-CHAT-HANDOFF.md`
2. `SYNC-RUNBOOK.md`
3. `AI-PROJECT-GUIDE.md`
4. `PROMPT-STYLE-GUIDE.md`
5. `USER-GUIDE.md`
6. `README-AI-SYNC.md`
7. `BACKUP-AI-RUNBOOK.md`

Затем:
- fresh exact Drive `video-prompts.md`;
- live `project-status.json`;
- live `topview-status.json`;
- live `instruction-sync-status.json`;
- при story/editing — `film-analysis.md`, `film-backlog.md`, затем релевантный Notion `Кино`.

Только после этого takeover считается завершённым.

## 2. Capability preflight

Перед записью агент должен доказать, что конкретное окружение умеет:

1. читать exact Drive master ID `1yoUVfEAumOClvlBg8prFIX_BFFfoCZqj`;
2. писать обратно в **тот же file ID**;
3. читать/писать repo `virudik/ai-film-prompts`;
4. обновлять `SYNC-TRIGGER.txt`;
5. проверять Actions/status/Pages.

Для instruction maintenance также нужны:
- read/write exact seven Drive instruction IDs;
- exact GitHub mirror update;
- проверка `instruction-sync-status.json`.

Если same-ID Drive write недоступна — агент **review-only**. Он не создаёт новый master и не притворяется, что запись выполнена.

## 3. Источник истины

Drive:
- prompt master;
- seven canonical instruction/recovery docs.

GitHub:
- mirrors;
- Control Center;
- machine status;
- Pages.

Notion:
- story/ideas/history.

Library:
- recovery mirror/cache.

Topview:
- telemetry.

Supabase:
- comments backend.

Ни один из последних пяти не становится prompt master.

## 4. Правила master

- stable Scene IDs;
- deleted IDs never reused;
- no `v2/final/copy`;
- fresh-read before write;
- minimal edit;
- same Drive ID;
- update TOC/count/meta consistently;
- no automatic slow rerun;
- Topview success != approval;
- `NEEDS_FIX` != permission to rewrite everything.

Если следующий Scene ID однозначно вычисляется по fresh master, новый чат сам выбирает следующий unused stable ID и **не задаёт лишний вопрос пользователю**.

## 5. Правила prompt-writing

Перед новым/существенным prompt:
- fresh-read `PROMPT-STYLE-GUIDE.md`;
- fresh-read master;
- inspect 1–2 current similar scenes.

Новый prompt должен соответствовать master-level сложности, а не быть коротким generic описанием.

Обязательные типовые элементы:
- exact refs / identity priority;
- story flow/timeline;
- camera/continuity;
- performance;
- dialogue/vocal/lip sync;
- lighting/material/environment;
- native audio;
- scene-specific negative prompt;
- `FRAME FILL / NO BARS`.

Approved model sheet сильнее случайного frame similarity.

## 6. Routine write procedure

`fresh-read`
→ `minimal same-ID Drive edit`
→ `SYNC-TRIGGER.txt`
→ `sync-from-drive.yml`
→ `validation`
→ `GitHub mirror`
→ `project-status.json`
→ `Pages`
→ `verification`
→ `report`

Не говорить `ГОТОВО` до relevant verification.

## 7. Seven-document instruction maintenance

Canonical set:
- `NEW-CHAT-HANDOFF.md`
- `SYNC-RUNBOOK.md`
- `AI-PROJECT-GUIDE.md`
- `PROMPT-STYLE-GUIDE.md`
- `USER-GUIDE.md`
- `README-AI-SYNC.md`
- `BACKUP-AI-RUNBOOK.md`

Drive authority → GitHub mirror.

`instruction-sync-status.json` должен проверять все семь.

Автоматический repair:
Drive → GitHub only.

Нельзя автоматически:
GitHub → Drive.

## 8. Material Change Duty

Если агент внедрил постоянное нововведение:
- функцию сайта;
- новый backend;
- новый prompt rule;
- новый sync/recovery behavior;
- новый source-of-truth rule;
- новый status;

он обязан **в том же сеансе**:
1. обновить релевантные canonical Drive docs;
2. обновить SAME handoff;
3. обновить prompt guide, если применимо;
4. синхронизировать GitHub mirrors;
5. refresh instruction status;
6. проверить site/status;
7. обновить Notion operational pointer;
8. обновить Library recovery copies.

Изменение кода без документации не считается законченным.

## 9. Control Center current baseline

Сайт уже умеет:
- active scenes/full prompts;
- merged slow/Topview;
- sync lightsaber;
- references;
- theme light/dark;
- `Контрольный отпечаток`;
- отдельную collapsible секцию `💬 Комментарии, идеи и предложения` сразу ниже;
- Supabase comments/replies без GitHub login.

Старой кнопки `Архив GitHub` нет.

Комментарии:
- Supabase `ai-film-comments`;
- ref `vzohfatqzyioydtgjiyd`;
- Edge Function `submit-comment`;
- RLS + honeypot + 5 messages/10min/IP;
- no admin/service secret in public HTML;
- no master mutation rights.

## 10. Site-only edit procedure

Править `index.html` в GitHub.

После:
- JS syntax check;
- duplicate IDs;
- secret scan;
- Pages verification.

Scene/prompt data нельзя hard-code в HTML.

Если site change становится постоянным — выполнить Material Change Duty.

## 11. Topview safety

Canonical slow = fresh `project-status.json.slow_scenes`.

Task mapping:
- exact task;
- full current scene semantics;
- model/reference match;
- `verified=true` only when proven.

Telemetry never:
- approves;
- clears slow;
- edits master;
- reruns automatically.

## 12. Recovery known issues

- concurrent GitHub writers → use fresh origin/rebuild/retry;
- BOM → master UTF-8 without BOM;
- stale instruction status → refresh verification;
- historical checkpoint conflicts → do not treat as live;
- stale Topview mapping → compare against fresh canonical scene body;
- old GitHub failure email → compare timestamps with newer success/live status.

## 13. Notion / Library

Notion:
- use for story/ideas/history;
- operational page `AI Film — Актуальная инструкция / Handoff`;
- `Важные промты` is legacy bank.

Library:
- recovery mirror/cache;
- keep current copies of seven docs + recovery summary/status;
- never prefer Library over accessible Drive.

## 14. Правило поведения сменщика

Если ответ есть в canonical docs/status:
- не спрашивать пользователя повторно;
- не импровизировать другую архитектуру;
- не перекладывать ручную работу на пользователя, если есть инструменты;
- продолжать с текущего состояния;
- при ограничении инструмента честно указать конкретный недоступный шаг.

Цель takeover: пользователь должен иметь возможность сказать только новую творческую/рабочую задачу, а сменщик уже знает инфраструктуру и процесс.
