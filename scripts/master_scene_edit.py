#!/usr/bin/env python3
"""Deterministic scene retirement in the canonical master (video-prompts.md).

Used by the GitHub robot (scripts/robot_master_actions.py) for the owner buttons
«🎞 В фильме» (in_film) and «✕ Не нужна» (scene_not_needed). Pure text functions,
no network, no git. The edit is minimal and mirrors what the owner/agents did by
hand for scenes 10, 11, 17, 19, 22, 23, 29:

  * remove the scene section (separator, <a id="scene-N">, heading … last prompt fence);
  * remove its row from the table of contents;
  * remove its (non-active) row from the table «⏳ Сейчас в медленной генерации»;
  * decrement the two counters (scenes / full prompt texts) in the revision block and
    in the «В active master остаются …» sentence;
  * add N to the list «Сцены … удалены из active master; их Scene ID зарезервированы»
    (the Scene ID is reserved forever, never reused);
  * for in_film only: drop `dependencies` entries pointing at N from other scenes'
    scene-meta (the validator requires dependency targets to exist).

Anything not provably unambiguous raises NeedsOwner and NOTHING is written:
active Topview slow marker, the scene being the «Последняя оформленная активная
сцена», dangling #scene-N links, unrecognised master format, scene_not_needed with
dependents, a scene ID already reserved, etc.
"""
import json
import re

LABEL = "⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ"
# Some sections (16, 28) have no '---' separator in front of their anchor, so it is optional.
BLOCK_RE = re.compile(r'^(?:---\n\n)?<a id="scene-(\d+)"></a>\n', re.M)


class NeedsOwner(Exception):
    """The edit is ambiguous or unsafe; the robot must not touch the master."""


def plural(n, one, few, many):
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return one
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return few
    return many


def scene_blocks(text):
    """[(scene_id, start, end)] — block = optional '---' separator + anchor + section, up to the next block
    (or the closing '---' at the end of the file, which stays)."""
    marks = [(int(m.group(1)), m.start()) for m in BLOCK_RE.finditer(text)]
    blocks = []
    for i, (sid, start) in enumerate(marks):
        if i + 1 < len(marks):
            end = marks[i + 1][1]
        elif text.endswith("\n---\n") and len(text) - 4 > start:
            end = len(text) - 4          # keep the final '---'
        else:
            end = len(text)
        blocks.append((sid, start, end))
    return blocks


def _join_ids(ids):
    ids = sorted(set(ids))
    if len(ids) == 1:
        return str(ids[0])
    return ", ".join(map(str, ids[:-1])) + " и " + str(ids[-1])


def active_scene_ids(text):
    return [int(x) for x in re.findall(r"^## Сцена (\d+)\b", text, re.M)]


def reserved_scene_ids(text):
    m = re.search(r"(?-i:Сцены)\s+([^\n]+?)\s+удалены из active master[^\n]*?зарезервированы", text, re.I)
    return [int(x) for x in re.findall(r"\d+", m.group(1))] if m else []


def slow_label_in_scene(text, scene_id):
    for sid, start, end in scene_blocks(text):
        if sid == scene_id:
            return f"**{LABEL}**" in text[start:end]
    return False


def _retire_counters(text, prompts_removed, scenes_after):
    """Update the revision line and the «В active master остаются …» sentence."""
    rev = re.compile(r"(\*\*(?:\d{2}\.\d{2}\.\d{4} · )?)(\d+)( сцен[^·\n]*? · )(\d+)( полн[^*\n]*?)(\*\*)")
    m = rev.search(text)
    if not m:
        raise NeedsOwner("строка ревизии master не распознана (счётчики сцен/промтов)")
    prompts_after = int(m.group(4)) - prompts_removed
    if int(m.group(2)) - 1 != scenes_after or prompts_after < 0:
        raise NeedsOwner("счётчики в шапке master не совпадают с фактическим числом сцен")
    scene_tail = re.sub(r"^ сцен\w*", " " + plural(scenes_after, "сцена", "сцены", "сцен"), m.group(3))
    prompt_tail = re.sub(r"^ полн\S* \S+ промт\w*",
                         " " + plural(prompts_after, "полный текст промта", "полных текста промта",
                                      "полных текстов промта"), m.group(5))
    text = text[:m.start()] + f"{m.group(1)}{scenes_after}{scene_tail}{prompts_after}{prompt_tail}{m.group(6)}" + text[m.end():]
    sent = re.compile(r"(\*\*)(\d+)( актуальн\w+ сцен\w*)( и )(\d+)( полн[^*\n]*?)(\*\*)")
    m = sent.search(text)
    if m:
        scene_w = plural(scenes_after, "актуальная сцена", "актуальные сцены", "актуальных сцен")
        prompt_w = plural(prompts_after, "полный текст промта", "полных текста промта", "полных текстов промта")
        text = text[:m.start()] + f"**{scenes_after} {scene_w} и {prompts_after} {prompt_w}**" + text[m.end():]
    return text


def _add_reserved(text, scene_id):
    pat = re.compile(r"((?-i:Сцены)\s+\*\*)([^*\n]+?)(\*\*\s+удалены из active master[^\n]*?зарезервированы)", re.I)
    m = pat.search(text)
    if not m:
        raise NeedsOwner("список зарезервированных Scene ID в master не найден — не могу зарезервировать ID")
    ids = [int(x) for x in re.findall(r"\d+", m.group(2))]
    if scene_id in ids:
        raise NeedsOwner(f"Scene ID {scene_id} уже зарезервирован, но раздел сцены ещё в master — конфликт")
    return text[:m.start()] + m.group(1) + _join_ids(ids + [scene_id]) + m.group(3) + text[m.end():]


def _drop_dependencies(text, scene_id, allow):
    """Remove dependency entries that point at scene_id from other scenes' scene-meta."""
    dropped = []
    meta_re = re.compile(r"<!-- scene-meta: (\{.*?\}) -->")
    out, pos = [], 0
    for m in meta_re.finditer(text):
        raw = m.group(1)
        try:
            meta = json.loads(raw)
        except ValueError:
            raise NeedsOwner("scene-meta одной из сцен не является корректным JSON")
        deps = meta.get("dependencies") or []
        hit = [d for d in deps if isinstance(d, dict) and d.get("scene") == scene_id]
        if not hit:
            continue
        if not allow:
            raise NeedsOwner(f"от сцены {scene_id} зависят другие сцены; решение «не нужна» требует выбора владельца")
        compact = json.dumps(meta, ensure_ascii=False, separators=(",", ":"))
        if compact != raw:
            raise NeedsOwner("scene-meta зависимой сцены записан нестандартно; автоматическая правка небезопасна")
        meta["dependencies"] = [d for d in deps if d not in hit]
        owner = None
        # which scene owns this meta: the nearest preceding '## Сцена N'
        for h in re.finditer(r"^## Сцена (\d+)\b", text[:m.start()], re.M):
            owner = int(h.group(1))
        dropped.append({"scene": owner, "dependency": hit})
        out.append((m.start(1), m.end(1), json.dumps(meta, ensure_ascii=False, separators=(",", ":"))))
    for a, b, new in reversed(out):
        text = text[:a] + new + text[b:]
    return text, dropped


def retire_scene(text, scene_id, *, mode, date=None):
    """Retire `scene_id` from the master text. mode: 'in_film' | 'scene_not_needed'.

    Returns (new_text, report). Raises NeedsOwner when anything is unclear.
    A scene that is already gone AND reserved yields report['already_retired']=True and
    the text unchanged (idempotent retry after an interrupted run)."""
    if mode not in ("in_film", "scene_not_needed"):
        raise ValueError("mode")
    if "\r" in text or text.startswith("﻿"):
        raise NeedsOwner("master не в формате UTF-8/LF без BOM")
    ids = active_scene_ids(text)
    if scene_id not in ids:
        if scene_id in reserved_scene_ids(text):
            return text, {"scene_id": scene_id, "already_retired": True, "dependents_dropped": []}
        raise NeedsOwner(f"Scene ID {scene_id} нет ни среди активных сцен master, ни среди зарезервированных")
    blocks = {sid: (s, e) for sid, s, e in scene_blocks(text)}
    if sorted(blocks) != sorted(ids) or scene_id not in blocks:
        raise NeedsOwner("якоря/разделы сцен в master не согласованы; автоматическая правка небезопасна")
    start, end = blocks[scene_id]
    block = text[start:end]
    if f"**{LABEL}**" in block:
        raise NeedsOwner(f"у сцены {scene_id} стоит отметка «в медленной генерации» (активная задача Topview)")
    fences = [l for l in block.splitlines() if l.strip().startswith("```")]
    if len(fences) % 2:
        raise NeedsOwner("в разделе сцены не закрыт блок промта")
    prompts_removed = len(fences) // 2

    latest = re.search(r"\*\*Последняя оформленная активная сцена:\*\*\s*(\d+)\b", text)
    if latest and int(latest.group(1)) == scene_id:
        raise NeedsOwner("сцена указана как «последняя оформленная активная» — нужно решить, какую назвать вместо неё")

    # 1. section
    new = text[:start] + text[end:]
    # 2. TOC row (exactly one)
    toc = re.compile(rf"^\|\s*{scene_id}\s*\|\s*\[[^\n]*\n", re.M)
    if len(toc.findall(new)) != 1:
        raise NeedsOwner("строка оглавления сцены не найдена или не единственна")
    new = toc.sub("", new, count=1)
    # 3. slow table rows of this scene (finished/dropped rows only)
    row = re.compile(rf"^\|\s*{scene_id}\s+—[^\n]*\n", re.M)
    for r in row.findall(new):
        if LABEL in r:
            raise NeedsOwner(f"в таблице медленной генерации у сцены {scene_id} есть активная строка")
    new = row.sub("", new)
    # 4. nothing may still link to the removed section
    if re.search(rf"\(#scene-{scene_id}\)|href=[\"']#scene-{scene_id}[\"']|#scene-{scene_id}\b", new):
        raise NeedsOwner("в master остались ссылки на удаляемый раздел сцены")
    # 5. dependents
    new, dropped = _drop_dependencies(new, scene_id, allow=(mode == "in_film"))
    # 6. counters + reserved ID
    new = _retire_counters(new, prompts_removed, len(ids) - 1)
    new = _add_reserved(new, scene_id)
    # 7. «Синхронизация контекста» date (as the monitor does on content changes)
    if date:
        new = re.sub(r"(\*\*Синхронизация контекста:\*\* \*\*)\d\d\.\d\d\.\d{4}", r"\g<1>" + date, new, count=1)
    return new, {"scene_id": scene_id, "already_retired": False, "mode": mode,
                 "prompts_removed": prompts_removed, "dependents_dropped": dropped,
                 "scenes_after": len(ids) - 1}
