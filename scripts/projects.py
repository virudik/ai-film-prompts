#!/usr/bin/env python3
"""Several film projects in one repository (owner decision 20.10.2026).

The registry is projects/projects.json. «Серёгиус» stays where it always was (repository root,
root «.»); every other project lives in projects/<id>/ with its own master, handoff, instructions,
references, launch queue, canon lock and project-status.json. Scene numbers are per project.

usage: projects.py <repo> list
       projects.py <repo> detect "<owner message>"
       projects.py <repo> status [--project ID] [--write]   build projects/<id>/project-status.json
       projects.py <repo> validate                         registry + folders + statuses (exit 1 on a problem)

Nothing here touches the root project's files: the root master, its status, robots and the root
canon lock keep their own scripts. This module only adds the other projects next to them.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REGISTRY = "projects/projects.json"
ROOT_ID = "seregius"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,30}$")
VALUE_PREFIX = "project:"          # owner button rows of other projects: owner_decisions.value = "project:<id>"
NOTE_RE = re.compile(r"^\s*\[проект:\s*([a-z0-9-]+)\]\s*", re.I)   # owner_task note prefix «[проект: <id>] …»
TELEMETRY = "projects/topview-projects.json"
REQUIRED_FILES = ("master", "handoff", "instructions", "references", "queue", "lock", "status")


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def load(root):
    return read_json(Path(root) / REGISTRY, {}) or {}


def projects(root, *, include_root=False):
    """Registry entries; the root project («Серёгиус») only when include_root=True."""
    out = []
    for p in load(root).get("projects") or []:
        if p.get("id") == ROOT_ID and not include_root:
            continue
        out.append(p)
    return out


def get(root, pid):
    for p in load(root).get("projects") or []:
        if p.get("id") == pid:
            return p
    return None


def other_ids(root):
    return [p["id"] for p in projects(root)]


# --------------------------------------------------------------------------- owner rows
def project_tasks(root):
    """task_id -> project for every task of the other projects the robot has seen (active + recent)."""
    tel = read_json(Path(root) / TELEMETRY, {}) or {}
    return tel


def project_of_row(row, telemetry=None):
    """Project of a Supabase owner_decisions row. Rows without a tag belong to the root project.

    Scene buttons of other projects carry value "project:<id>"; text tasks carry the note prefix
    «[проект: <id>]». Reference feedback is tagged by the image path (projects/<id>/...). Task buttons
    (tv_*: «Брак», «Готово ✓», «Не ждать») follow the task: a task recorded in projects/topview-projects.json
    belongs to that project."""
    tid = str((row or {}).get("task_id") or "")
    if tid and telemetry:
        for t in list(telemetry.get("active") or []) + list(telemetry.get("recent") or []):
            if t.get("task_id") == tid and t.get("project"):
                return t["project"]
    value = str((row or {}).get("value") or "")
    if value.startswith(VALUE_PREFIX):
        return value[len(VALUE_PREFIX):].strip() or ROOT_ID
    m = NOTE_RE.match(str((row or {}).get("note") or ""))
    if m:
        return m.group(1).lower()
    note = str((row or {}).get("note") or "")
    m = re.match(r"\s*projects/([a-z0-9-]+)/", note)
    if m and (row or {}).get("action") == "ref_feedback":
        return m.group(1)
    return ROOT_ID


def is_root_row(row, telemetry=None):
    return project_of_row(row, telemetry) == ROOT_ID


def strip_note_tag(note):
    return NOTE_RE.sub("", str(note or ""), count=1)


# --------------------------------------------------------------------------- detection
def _norm(text):
    return str(text or "").lower().replace("ё", "е")


def detect(text, registry):
    """Which project an owner message is about.

    returns {"project": id|None, "mentions": [ids in order], "default": bool, "reason": str}
    One project named -> that project. None named -> the default project («Серёгиус»).
    Several named -> project=None: split the message per project or ask the owner.
    """
    t = _norm(text)
    hits = []
    for p in registry.get("projects") or []:
        best = None
        for a in p.get("aliases") or []:
            a = _norm(a)
            if not a:
                continue
            i = t.find(a)
            if i >= 0 and (best is None or i < best):
                best = i
        if best is not None:
            hits.append((best, p["id"]))
    hits.sort()
    ids = list(dict.fromkeys(pid for _, pid in hits))
    if len(ids) == 1:
        return {"project": ids[0], "mentions": ids, "default": False, "reason": "назван один проект"}
    if not ids:
        d = registry.get("default_project") or ROOT_ID
        return {"project": d, "mentions": [], "default": True, "reason": "проект не назван — по умолчанию " + d}
    return {"project": None, "mentions": ids, "default": False,
            "reason": "названо несколько проектов — разделить сообщение по проектам или спросить владельца"}


# --------------------------------------------------------------------------- status
def _volatile(st):
    keep = dict(st or {})
    for k in ("synced_at", "revision_date", "audit_fingerprint", "instruction_sync", "warnings", "maintenance"):
        keep.pop(k, None)
    return keep


def build_status(root, pid, *, synced_at=None, write=False):
    """Validate one project's master and (optionally) write its project-status.json.

    Uses the same validator as the root master (scripts/build_project_status.py). A brand-new
    project has no retired scene IDs yet, so the «reserved IDs declared» check is not required
    until the first scene is closed. Returns (status, changed). The file is rewritten only when
    something besides the timestamps changed (no heartbeat churn)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_project_status as bps  # noqa: E402

    root = Path(root)
    p = get(root, pid)
    if not p or pid == ROOT_ID:
        raise ValueError(f"unknown project {pid!r}")
    master = root / p["master"]
    out = root / p["status"]
    prev = read_json(out, None)
    synced_at = synced_at or utcnow()
    try:
        st = bps.parse_master(master, synced_at, None, None, None, root / "instruction-sync-status.json",
                              None, None, out if out.is_file() else None, None, "Europe/Moscow")
    except SystemExit:
        st = {"health": "error", "checks": {"master_parsed": False}, "canonical_master_sha256": None,
              "synced_at": synced_at, "scene_ids": [], "scenes": 0, "prompt_texts": 0}
    checks = dict(st.get("checks") or {})
    if not st.get("reserved_scene_ids"):
        checks.pop("reserved_scene_ids_declared", None)
    st["checks"] = checks
    st["health"] = "ok" if checks and all(checks.values()) else "error"
    st.update(project=pid, project_name=p.get("name"), source_of_truth=f"GitHub main/{p['master']}",
              automation="GitHub main project master -> scripts/projects.py (validator of build_project_status.py) -> status -> Pages")
    if isinstance(st.get("audit_fingerprint"), dict):
        st["audit_fingerprint"]["health"] = st["health"]
    changed = prev is None or _volatile(prev) != _volatile(st)
    if write and changed:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return st, changed


# --------------------------------------------------------------------------- validation
def validate(root):
    """Problems as plain Russian strings; [] = everything is consistent."""
    root = Path(root)
    reg = load(root)
    bad = []
    items = reg.get("projects") or []
    ids = [p.get("id") for p in items]
    if not items:
        return ["нет реестра projects/projects.json"]
    if len(ids) != len(set(ids)):
        bad.append("повторяющийся id проекта в реестре")
    if reg.get("default_project") not in ids:
        bad.append("default_project не найден в реестре")
    if set(reg.get("launch_order") or []) != set(ids):
        bad.append("launch_order не совпадает со списком проектов")
    for p in items:
        pid = p.get("id") or "?"
        if not ID_RE.match(pid):
            bad.append(f"{pid}: недопустимый id")
        if not p.get("name"):
            bad.append(f"{pid}: нет названия")
        if pid == ROOT_ID:
            if p.get("root") != ".":
                bad.append("Серёгиус должен оставаться в корне репозитория")
            continue
        if p.get("root") != f"projects/{pid}":
            bad.append(f"{pid}: root должен быть projects/{pid}")
        for key in REQUIRED_FILES:
            rel = p.get(key)
            if not rel or not str(rel).startswith(f"projects/{pid}/"):
                bad.append(f"{pid}: поле {key} должно указывать внутрь projects/{pid}/")
            elif not (root / rel).is_file():
                bad.append(f"{pid}: нет файла {rel}")
        st = read_json(root / p.get("status", ""), None)
        master = root / p.get("master", "")
        if st and master.is_file():
            import hashlib
            if st.get("canonical_master_sha256") != hashlib.sha256(master.read_bytes()).hexdigest():
                bad.append(f"{pid}: project-status.json не соответствует мастеру (запусти projects.py . status --write)")
            if st.get("health") != "ok":
                bad.append(f"{pid}: мастер не проходит проверку ({', '.join(k for k, v in (st.get('checks') or {}).items() if not v)})")
        lock = read_json(root / p.get("lock", ""), None)
        if lock is not None and lock.get("state") not in ("free", "held"):
            bad.append(f"{pid}: замок проекта в неизвестном состоянии")
        q = read_json(root / p.get("queue", ""), None)
        if q is not None and (q.get("project") != pid or not isinstance(q.get("items"), list)):
            bad.append(f"{pid}: очередь должна иметь project={pid} и список items")
        refs = read_json(root / p.get("references", ""), None)
        if refs is not None:
            for c in refs.get("characters") or []:
                for img in [c.get("public_image"), c.get("full_image")] + [x.get("path") for x in c.get("images") or []]:
                    if img and not (root / img).is_file():
                        bad.append(f"{pid}: нет картинки {img}")
            for asset in refs.get("assets") or []:
                for x in asset.get("images") or []:
                    if x.get("path") and not (root / x["path"]).is_file():
                        bad.append(f"{pid}: нет картинки {x['path']}")
    return bad


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("cmd", choices=("list", "detect", "status", "validate"))
    ap.add_argument("text", nargs="?", default="")
    ap.add_argument("--project")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.repo)
    if a.cmd == "list":
        for p in projects(root, include_root=True):
            print(f"{p['id']:14} {p.get('root'):26} {p.get('name')}")
        return 0
    if a.cmd == "detect":
        print(json.dumps(detect(a.text, load(root)), ensure_ascii=False))
        return 0
    if a.cmd == "status":
        rc = 0
        for pid in ([a.project] if a.project else other_ids(root)):
            st, changed = build_status(root, pid, write=a.write)
            print(f"{pid}: health={st['health']} scenes={st.get('scenes')} prompts={st.get('prompt_texts')}"
                  + (" (записан)" if a.write and changed else " (без изменений)" if a.write else ""))
            rc |= st["health"] != "ok"
        return rc
    problems = validate(root)
    for x in problems:
        print("✕ " + x)
    if not problems:
        print("проекты в порядке")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
