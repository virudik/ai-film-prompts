#!/usr/bin/env python3
"""Build a small, reproducible recovery view from one checkout. No scheduler or writer."""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from continue_preflight import evaluate
from resume_state import REGISTER, CHECKPOINT, QUEUE, digest, local_file, operation_guidance, verify_recovery

GENERATOR = "continue-2.0"


def build(root, work_id=None):
    root = Path(root)
    result = evaluate(root, work_id)
    sources = []
    paths = {REGISTER, CHECKPOINT, QUEUE, "ops/CONTINUE-PROTOCOL.md",
             "shadow/takeover-brief.json", "shadow/current-checkpoint.md",
             "project-status.json", "instruction-sync-status.json", "monitor-role.json"}
    checkpoint_text, queue, invariants = "", {}, []
    try:
        brief = json.loads(local_file(root, "shadow/takeover-brief.json").read_bytes())
        for s in brief.get("sources", []):
            local_file(root, s["file"])
            paths.add(s["file"])
        invariants = [{"id": i["id"], "rule": i["rule"], "owner_doc": i["owner_doc"],
                       "anchor": i["anchor"]} for i in brief.get("invariants", [])]
        reg = json.loads(local_file(root, REGISTER).read_bytes())
        recovery = verify_recovery(root, reg, work_id)
        checkpoint_text = recovery["checkpoint_text"]
        paths.update(s["file"] for s in recovery["sources"])
        queue = json.loads(local_file(root, QUEUE).read_bytes())
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        result["reasons"].append("recovery packet source invalid: " + str(e))
    for p in sorted(paths):
        try:
            raw = local_file(root, p).read_bytes()
            sources.append({"file": p, "sha256": digest(raw), "bytes": len(raw)})
        except (OSError, ValueError) as e:
            result["reasons"].append(str(e))
    active = queue.get("items", []) if isinstance(queue, dict) else None
    archived = queue.get("archived_items", []) if isinstance(queue, dict) else None
    if not isinstance(active, list) or not isinstance(archived, list):
        items = []
        result["reasons"].append("invalid launch queue")
    else:
        items = active + archived
        if not all(isinstance(i, dict) for i in items):
            items = []
            result["reasons"].append("invalid launch queue item")
    operations = [operation_guidance(i) for i in items if i.get("task_id") or i.get("claim")
                  or i.get("state") in {"claimed", "submitting", "submission_unknown", "submitted"}]
    unresolved = [i for i in operations if i["recovery_action"] == "reconcile_without_resubmitting"]
    ready = sorted((i for i in items if i.get("state") == "waiting_for_slot"
                    and not i.get("task_id") and not i.get("claim")),
                   key=lambda i: (i["priority"] if isinstance(i.get("priority"), (int, float)) else 9999,
                                  str(i.get("id", ""))))
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, stderr=subprocess.DEVNULL).decode().strip()
    except (OSError, subprocess.CalledProcessError):
        head = None
    return {
        "schema_version": 1, "generator": GENERATOR,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_head": head, "source_fingerprint": digest(json.dumps(sources, sort_keys=True).encode()),
        "status": "needs_recovery" if result["reasons"] else "ready",
        "ready_for_resume": not result["reasons"], "execution_authorized": False,
        "reasons": result["reasons"], "selected_work": result.get("selected_work"),
        "checkpoint_text": checkpoint_text, "invariants": invariants,
        "read_next": (result.get("selected_work") or {}).get("read_next", []),
        "live_checks_required": ["Fresh main and canon lock before writing",
            "Open owner_decisions and agent inbox; do not infer approval from this packet",
            "Current capabilities; for a video submit use all-project slot scan, input/QC, Unlimited0 and CAS claim"],
        "queue_recovery": {"unresolved": unresolved, "existing_task_count": sum(bool(i["task_id"]) for i in operations),
            "existing_tasks": [{"item_id": i["item_id"], "task_id": i["task_id"]} for i in operations if i["task_id"]],
            "next_candidates": [operation_guidance(i) for i in ready[:3]],
            "rule": "Existing task ID: inspect, never resubmit. Claim/unknown without receipt: reconcile first; no retry."},
        "sources": sources,
    }


def markdown(packet):
    w = packet.get("selected_work") or {}
    lines = ["# Продолжай — пакет восстановления Серёгиуса", "",
             "Производный навигатор. Сначала свежий main и `scripts/continue_preflight.py`; разрешением на запуск не является.",
             "", "Состояние: " + packet["status"], "Проверено: " + packet["checked_at"],
             "Задача: " + str(w.get("work_id", "не определена")) + " — " + str(w.get("title", "")),
             "", "Последний подтверждённый этап: " + str(w.get("last_completed", "нет доказательств")),
             "Следующий шаг: " + str(w.get("next_action", "восстановить конкретный пробел")),
             "", "## Контрольная точка", "", packet.get("checkpoint_text", ""),
             "## Обязательные правила", ""]
    lines += ["- " + i["rule"] + " — `" + i["owner_doc"] + "`" for i in packet["invariants"]]
    lines += ["", "## Прочитать под задачу", ""] + ["- `" + p + "`" for p in packet["read_next"]]
    lines += ["", "## Перед действием", ""] + ["- " + x for x in packet["live_checks_required"]]
    q = packet["queue_recovery"]
    lines += ["", "## Незавершённые отправки", "", q["rule"],
              "Задач с сохранённым task ID: " + str(q["existing_task_count"])]
    lines += ["- " + str(i["item_id"]) + ": " + i["recovery_action"] for i in q["unresolved"]]
    lines += ["", "## Пробелы", ""] + (["- " + r for r in packet["reasons"]] or ["Нет ошибок локальной проверки. Живые проверки выше обязательны."])
    return "\n".join(lines) + "\n"


def write(root, out="shadow", work_id=None):
    packet = build(root, work_id)
    out = Path(root) / out
    out.mkdir(parents=True, exist_ok=True)
    dest = out / "resume-packet.json"
    try:
        old = json.loads(dest.read_bytes())
        # No timestamps-only commits or refresh of a stale observation.
        stable = lambda p: {k: v for k, v in p.items() if k not in {"checked_at", "source_head", "packet_bytes"}}
        if stable(old) == stable(packet):
            packet["checked_at"], packet["source_head"] = old["checked_at"], old.get("source_head")
    except (OSError, ValueError, KeyError):
        pass
    md = markdown(packet)
    packet["packet_bytes"] = len(md.encode())
    dest.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "resume-packet.md").write_text(md, encoding="utf-8")
    return packet


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", nargs="?", default=".")
    p.add_argument("--out", default="shadow")
    p.add_argument("--work-id")
    a = p.parse_args()
    result = write(a.repo, a.out, a.work_id)
    print(json.dumps({k: result[k] for k in ("status", "reasons", "packet_bytes")}, ensure_ascii=False))
