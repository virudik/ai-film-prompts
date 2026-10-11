#!/usr/bin/env python3
"""Deterministic slow-state edits of the canonical master (used by the Claude monitor).

Edits ONLY the slow-related markers, so the master commit stays minimal:
  * header bullet  "**⏳ N** ... медленной генерации: **IDS** — **K ... / K ... из 6**";
  * dedicated table "## ⏳ Сейчас в медленной генерации" (one row per active task);
  * TOC row marker "<br>**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**";
  * scene section marker "**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**" and a technical completion line;
  * "Canonical slow-list сейчас: **...**." and the two sync dates.

usage:
  master_slow_edit.py IN OUT --date DD.MM.YYYY --plan plan.json
plan.json:
  {"add":    [{"scene": 28, "task_id": "<32hex>", "model": "Seedance 2.0", "status": "init", "row_title": "28 — Танец A1"}],
   "finish": [{"scene": 30, "task_id": "<32hex>", "model": "Wan 3.0", "final_status": "success", "finished_utc": "09.10.2026 13:57:32 UTC"}]}
Terminal tasks remain canonical slow pending the owner's explicit site-panel decision.
Only a verified owner action may clear the marker. Physical slots are counted separately.
"""
import argparse, json, re, sys

LABEL = "⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ"
ABANDONED = "abandoned_by_owner"   # owner pressed «Не ждать» (tv_drop_task); the task itself is not cancelled


def plural(n, one, few, many):
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return one
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return few
    return many


def apply_plan(t, plan, date):
    """Pure core of the CLI: returns (new_text, info). Importable by the GitHub robot."""
    assert "\r" not in t, "master must be LF"

    lines = t.split("\n")
    # --- dedicated table bounds
    h = next(i for i, l in enumerate(lines) if l.startswith("## ⏳ Сейчас в медленной генерации"))
    rows_start = next(i for i in range(h, h + 6) if lines[i].startswith("|---")) + 1
    rows_end = rows_start
    while rows_end < len(lines) and lines[rows_end].startswith("|"):
        rows_end += 1

    # finish tasks: convert rows in place
    for f in plan.get("finish", []):
        idx = [i for i in range(rows_start, rows_end) if f"task `{f['task_id']}`" in lines[i] and LABEL in lines[i]]
        assert len(idx) == 1, ("active row not found", f)
        cells = lines[idx[0]].split(" | ")
        title = cells[0].lstrip("| ")
        if f["final_status"] == "success":
            lines[idx[0]] = f"| {title} | {LABEL} · ✅ Технический результат получен · `success` · {f['model']} | task `{f['task_id']}`; ждёт решения владельца в панели сайта |"
        elif f["final_status"] == ABANDONED:
            lines[idx[0]] = f"| {title} | ⚪ Снята с учёта владельцем · `{ABANDONED}` · {f['model']} | task `{f['task_id']}`; кнопка «Не ждать» только снимает ожидание — саму задачу в Topview отменяет владелец вручную |"
        else:
            lines[idx[0]] = f"| {title} | {LABEL} · ❌ Ошибка Topview · `{f['final_status']}` · {f['model']} | task `{f['task_id']}`; ждёт решения владельца в панели сайта |"

    # add tasks: append rows at table end
    new_rows = []
    for ad in plan.get("add", []):
        assert not any(f"task `{ad['task_id']}`" in l for l in lines), ("task already in master", ad)
        new_rows.append(f"| {ad['row_title']} | {LABEL} · `{ad.get('status', 'init')}` · {ad['model']} | task `{ad['task_id']}`; ждать terminal и проверить результат отдельно |")
    lines[rows_end:rows_end] = new_rows
    rows_end += len(new_rows)

    active_rows = [l for l in lines[rows_start:rows_end] if LABEL in l]
    active_by_scene = {}
    for l in active_rows:
        sid = int(re.match(r"^\|\s*(\d+)\s+—", l).group(1))
        active_by_scene.setdefault(sid, 0)
        active_by_scene[sid] += 1
    slow = sorted(active_by_scene)
    k = sum(bool(re.search(r'`(?:init|queued|running|processing)`', row)) for row in active_rows)  # real slots, not owner-pending terminal rows
    t = "\n".join(lines)

    # --- header bullet
    ids = ", ".join(map(str, slow)) if slow else "нет"
    hdr = re.compile(r"^- \*\*⏳ \d+\*\* [^\n]*$", re.M)
    assert len(hdr.findall(t)) == 1
    word = plural(len(slow), "сцена", "сцены", "сцен")
    tasks = plural(k, "активная Topview-задача", "активные Topview-задачи", "активных Topview-задач")
    slots = plural(k, "занятый слот", "занятых слота", "занятых слотов")
    tail = "Редакционная приёмка будущих результатов отдельно. Новые генерации автоматически не запускать."
    t = hdr.sub(f"- **⏳ {len(slow)}** {word} сейчас в медленной генерации: **{ids}** — **{k} {tasks} / {k} {slots} из 6**. {tail}", t)

    # --- canonical slow-list sentence and dates
    t, n = re.subn(r"Canonical slow-list сейчас: \*\*[^*]*\*\*\.", f"Canonical slow-list сейчас: **{ids}**.", t)
    assert n == 1
    t, n = re.subn(r"(- \*\*Последняя полная синхронизация:\*\* \*\*)\d\d\.\d\d\.\d{4}", r"\g<1>" + date, t)
    assert n == 1
    t, n = re.subn(r"(\*\*Синхронизация контекста:\*\* \*\*)\d\d\.\d\d\.\d{4}", r"\g<1>" + date, t)
    assert n == 1

    # --- TOC markers and section markers per scene
    finished_lines = {}
    for f in plan.get("finish", []):
        if f["final_status"] == "success":
            finished_lines.setdefault(f["scene"], []).append(f"{f['model']} task `{f['task_id']}` технически завершён {f['finished_utc']}. Результат требует отдельной редакционной проверки; новый Scene ID не создаётся.")
        elif f["final_status"] == ABANDONED:
            finished_lines.setdefault(f["scene"], []).append(f"{f['model']} task `{f['task_id']}` снята с учёта владельцем («Не ждать») {f['finished_utc']}. Отмена самой задачи в Topview — вручную; новый запуск только по решению владельца.")
        else:
            finished_lines.setdefault(f["scene"], []).append(f"{f['model']} task `{f['task_id']}` завершился ошибкой Topview (`{f['final_status']}`) {f['finished_utc']}. Новый запуск — только по решению владельца.")
    touched = {x["scene"] for x in plan.get("add", [])} | {x["scene"] for x in plan.get("finish", [])}
    for sid in sorted(touched):
        is_slow = sid in active_by_scene
        # TOC
        m = re.search(rf"^\|\s*{sid}\s*\|\s*\[[^\n]*$", t, re.M)
        assert m, ("toc row", sid)
        row = m.group(0)
        has = f"<br>**{LABEL}**" in row
        new = row
        if is_slow and not has:
            new = row[: row.rstrip().rfind("|")].rstrip() + f"<br>**{LABEL}** |"
        elif not is_slow and has:
            only_dropped = all(f["final_status"] == ABANDONED for f in plan.get("finish", []) if f["scene"] == sid)
            tail_txt = (" Задача снята с учёта владельцем («Не ждать»). |" if only_dropped
                        else " Технический результат получен; требуется отдельная редакционная проверка. |")
            new = row.replace(f"<br>**{LABEL}** |", tail_txt)
        t = t.replace(row, new, 1)
        # section
        s = t.index(f"\n## Сцена {sid} —")
        e = t.find("\n## Сцена ", s + 5)
        e = len(t) if e < 0 else e
        sec = t[s:e]
        marker = f"\n**{LABEL}**\n\n"
        if is_slow and marker not in sec:
            head_end = sec.index("\n", 1) + 1  # end of heading line
            sec = sec[:head_end] + marker + sec[head_end + 1:] if sec[head_end] == "\n" else sec[:head_end] + marker[1:] + sec[head_end:]
        if not is_slow and marker in sec:
            sec = sec.replace(marker, "\n", 1)
        if sid in finished_lines:
            mm = sec.find("<!-- scene-meta:")
            me = sec.index("-->\n", mm) + 4 if mm >= 0 else sec.index("\n", 1) + 1
            ins = "".join("\n" + x + "\n" for x in finished_lines[sid])
            sec = sec[:me] + ins + sec[me:]
        t = t[:s] + sec + t[e:]

    return t, {"slow": slow, "occupied": k, "active_by_scene": active_by_scene}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--date", required=True)
    ap.add_argument("--plan", required=True)
    a = ap.parse_args()
    t = open(a.inp, encoding="utf-8", newline="").read()
    plan = json.load(open(a.plan, encoding="utf-8"))
    t, info = apply_plan(t, plan, a.date)
    open(a.out, "w", encoding="utf-8", newline="").write(t)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()
