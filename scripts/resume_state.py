#!/usr/bin/env python3
"""Task-specific recovery evidence. Read-only unless capture is explicitly used.

The register is canonical; generated packets never grant permission to execute.
No sorting by monitor timestamps, automatic retries, or inferred completion.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from resume_project import context

REGISTER = "work-resume-register.json"
CHECKPOINT = "reports/current-work-checkpoint.md"
QUEUE = "ops/topview-launch-queue.json"
FINISHED = re.compile(r"^(completed|done|closed|cancelled|superseded)", re.I)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def local_file(root, name):
    if not isinstance(name, str) or not name or "\\" in name:
        raise ValueError("invalid source path")
    p = Path(name)
    if p.is_absolute() or ".." in p.parts or ":" in name:
        raise ValueError("unsafe source path")
    path = (Path(root) / p).resolve()
    if not path.is_relative_to(Path(root).resolve()) or not path.is_file():
        raise ValueError("missing or unsafe source: " + name)
    return path


def section(text, anchor):
    """Bind a unique top-level checkpoint; surrounding log additions are harmless."""
    if not isinstance(anchor, str) or not anchor.startswith("# ") or "\n" in anchor:
        raise ValueError("invalid checkpoint anchor")
    parts = re.split(r"(?m)(?=^# )", text)
    matches = [p for p in parts if p.splitlines() and p.splitlines()[0] == anchor]
    if len(matches) != 1:
        raise ValueError("checkpoint anchor missing or ambiguous")
    # Cleanup may move separators / the archive pointer, never the substantive text.
    lines = matches[0].splitlines()
    while lines and (not lines[-1].strip() or lines[-1].strip() == "---"
                     or lines[-1].startswith("Более ранние записи —")):
        lines.pop()
    return "\n".join(lines) + "\n"


def select_work(register, work_id=None, project="seregius"):
    active = register.get("active_work")
    if not isinstance(active, list) or not all(isinstance(w, dict) for w in active):
        raise ValueError("invalid active work list")
    ids = [w.get("work_id") for w in active]
    if any(not isinstance(i, str) or not i for i in ids) or len(ids) != len(set(ids)):
        raise ValueError("missing or duplicate work ID")
    focus = register.get("resume_focus")
    if not work_id:
        if not isinstance(focus, dict) or focus.get("project") != project:
            raise ValueError("explicit resume focus is missing")
        work_id = focus.get("work_id")
    if register.get("project", "seregius") != project:
        raise ValueError("register belongs to another project")
    by_id = {w["work_id"]: w for w in active}
    idle = register.get("idle_state")
    if not active and isinstance(idle, dict) and idle.get("status") == "waiting_for_owner":
        by_id[idle["work_id"]] = idle
    seen = set()
    while work_id:
        if work_id in seen:
            raise ValueError("cyclic continuation reference")
        seen.add(work_id)
        w = by_id.get(work_id)
        if not w or FINISHED.match(str(w.get("status", ""))):
            raise ValueError("resume target is missing or finished: " + str(work_id))
        if not w.get("continuation_work_id"):
            return w
        work_id = w["continuation_work_id"]
    raise ValueError("resume target is empty")


def operation_guidance(item):
    """An existing task/claim outranks a stale ready flag, including archive stubs."""
    state = str(item.get("state") or "")
    if item.get("task_id"):
        action = "observe_existing_task"
    elif item.get("claim") or state in {"claimed", "submitting", "submission_unknown", "submitted"}:
        action = "reconcile_without_resubmitting"
    elif re.match(r"^(completed|cancelled|superseded|held|paused|blocked)", state):
        action = "do_not_submit"
    elif state == "waiting_for_slot":
        action = "fresh_launch_preflight_required"
    else:
        action = "inspect_state_without_submitting"
    return {"item_id": item.get("id"), "state": state, "task_id": item.get("task_id"),
            "recovery_action": action, "submit_authorized": False}


def verify_recovery(root, register, work_id=None, project="seregius"):
    reasons, sources = [], []
    selected, checkpoint_text = None, ""
    try:
        ctx = context(root, project)
        w = select_work(register, work_id, project)
        r = w.get("recovery")
        if not isinstance(r, dict) or r.get("schema_version") != 1:
            raise ValueError("selected work has no verified recovery record")
        for key in ("last_completed", "next_action", "verified_at"):
            if not isinstance(r.get(key), str) or not r[key].strip():
                raise ValueError("recovery field missing: " + key)
        if w.get("next_action") != r["next_action"]:
            raise ValueError("next action changed without a recovery checkpoint")
        when = datetime.fromisoformat(r["verified_at"].replace("Z", "+00:00"))
        if when.tzinfo is None:
            raise ValueError("recovery timestamp has no timezone")
        cp = r.get("checkpoint")
        if not isinstance(cp, dict) or cp.get("file") != ctx["checkpoint"]:
            raise ValueError("recovery checkpoint must use the canonical checkpoint file")
        raw = local_file(root, ctx["checkpoint"]).read_bytes()
        checkpoint_text = section(raw.decode("utf-8-sig"), cp.get("anchor"))
        if "work_id: " + w["work_id"] not in checkpoint_text:
            raise ValueError("checkpoint belongs to another work ID")
        if digest(checkpoint_text.encode()) != cp.get("sha256"):
            raise ValueError("selected checkpoint hash mismatch")
        sources.append({"file": ctx["checkpoint"], "sha256": digest(raw)})
        evidence = r.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise ValueError("last completed step has no evidence")
        for e in evidence:
            if not isinstance(e, dict):
                raise ValueError("invalid recovery evidence")
            data = local_file(root, e.get("file")).read_bytes()
            if digest(data) != e.get("sha256"):
                raise ValueError("recovery evidence changed: " + str(e.get("file")))
            sources.append({"file": e["file"], "sha256": digest(data)})
        selected = {"work_id": w["work_id"], "title": w.get("title", w["work_id"]),
                    "status": w.get("status"), "last_completed": r["last_completed"],
                    "next_action": r["next_action"], "verified_at": r["verified_at"],
                    "blockers": r.get("blockers", []), "evidence": evidence,
                    "read_next": r.get("read_next", []), "checkpoint": cp}
    except (ValueError, OSError, TypeError, KeyError) as e:
        reasons.append(str(e))
    return {"selected_work": selected, "checkpoint_text": checkpoint_text,
            "sources": sources, "reasons": reasons}


def capture(root, work_id, anchor, last_completed, next_action, evidence, read_next=(), focus=False, project="seregius"):
    """Called by the writer after verifying a stage, in the same canon transaction."""
    root = Path(root)
    ctx = context(root, project)
    path = local_file(root, ctx["register"])
    reg = json.loads(path.read_text(encoding="utf-8-sig"))
    w = select_work(reg, work_id, project)
    text = section(local_file(root, ctx["checkpoint"]).read_text(encoding="utf-8-sig"), anchor)
    if "work_id: " + w["work_id"] not in text:
        raise ValueError("checkpoint work ID does not match")
    if not evidence or not last_completed.strip() or not next_action.strip():
        raise ValueError("completion, next step and evidence are required")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    w["recovery"] = {"schema_version": 1, "verified_at": now,
        "last_completed": last_completed, "next_action": next_action,
        "checkpoint": {"file": ctx["checkpoint"], "anchor": anchor, "sha256": digest(text.encode())},
        "evidence": [{"file": p, "sha256": digest(local_file(root, p).read_bytes())} for p in evidence],
        "read_next": list(read_next), "blockers": []}
    w["next_action"], w["updated_at"] = next_action, now
    if focus:
        reg["resume_focus"] = {"work_id": w["work_id"], "project": project,
                               "set_at": now, "reason": "Explicitly selected by the authorized task writer"}
    reg["last_updated_at"] = now
    path.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo")
    p.add_argument("--capture", required=True, metavar="WORK_ID")
    p.add_argument("--anchor", required=True)
    p.add_argument("--last-completed", required=True)
    p.add_argument("--next-action", required=True)
    p.add_argument("--evidence", action="append", required=True)
    p.add_argument("--read-next", action="append", default=[])
    p.add_argument("--project", default="seregius")
    p.add_argument("--focus", action="store_true")
    args = p.parse_args()
    capture(args.repo, args.capture, args.anchor, args.last_completed, args.next_action,
            args.evidence, args.read_next, args.focus, args.project)


if __name__ == "__main__":
    main()
