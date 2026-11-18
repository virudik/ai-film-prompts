#!/usr/bin/env python3
"""Daily check: does the ChatGPT schedule launch Topview tasks on its own, without an open chat? (owner 17.10.2026)

usage: launch_autonomy_check.py <repo> [--hours 24] [--notify]

Reads only repository data:
  * ops/topview-launch-queue.json — submitted items and their active claim or preserved last_claim.
    Task-bound receipt triggers classify modern launches; missing IDs remain unknown.
    Historical chatgpt-scheduled prefixes are retained as explicitly labelled legacy evidence.
  * git log of the GitHub robot — "Topview telemetry — N/6 slots" messages show whether a slot was free.
Writes reports/launch-autonomy.json. With --notify it posts one comment to the robot's
`topview-events` issue only for a current unresolved launcher incident. Historical free slots alone cannot prove idle time.
Never launches, approves or edits the queue.
"""
import argparse, json, re, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT = "reports/launch-autonomy.json"
SLOTS_RE = re.compile(r"GitHub robot: Topview telemetry — (\d+)/(\d+) slots")


def parse(v):
    try:
        dt = datetime.fromisoformat(str(v).replace("Z", "+00:00"))
        return dt if dt.tzinfo else None
    except (TypeError, ValueError):
        return None


def iso(dt):
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z") if dt else None


def read_json(path):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def launch_source(item, claim, receipt):
    """Only task-bound evidence describes a launch. Missing runtime IDs are not chat."""
    task_id = item.get("task_id")
    execution = claim.get("execution_instance_id")
    bound = bool(task_id and receipt.get("task_id") == task_id
                 and receipt.get("item_id") == item.get("id")
                 and execution and receipt.get("execution_instance_id") == execution
                 and (not claim.get("automation_id") or claim["automation_id"] == receipt.get("automation_id")))
    trigger = receipt.get("actual_trigger") if bound else None
    if trigger in ("scheduled", "manual_run_now", "webhook") and receipt.get("automation_id"):
        return ("schedule" if trigger == "scheduled" else trigger), "bound_receipt_trigger"
    if trigger == "interactive":
        return "chat", "bound_receipt_trigger"
    # Legacy prefix is a historical convention, NOT a requirement for new run IDs.
    # Explicit but incomplete/unsupported evidence must never fall back to that convention.
    if not receipt.get("actual_trigger") and str(claim.get("run_id") or "").startswith("chatgpt-scheduled"):
        return "schedule", "legacy_run_id_prefix"
    return "unknown", "missing_or_unbound_trigger_evidence"


def launches(queue, since, repo=None, now=None):
    out, seen = [], set()
    for it in queue.get("items") or []:
        claim = it.get("claim") or it.get("last_claim") or {}
        # Completed/archived renders still count; a claim alone does not prove submission.
        submitted = parse(it.get("submitted_at"))
        legacy = it.get("state") == "submitted"
        if not legacy and not (it.get("task_id") and submitted):
            continue
        at = submitted or parse(claim.get("claimed_at"))
        if not at or at < since or (now and at > now):
            continue
        key = ("topview", it.get("task_id") or it.get("id"))
        if key in seen:
            continue
        seen.add(key)
        receipt = {}
        if repo and isinstance(it.get("receipt"), str):
            root = Path(repo).resolve()
            path = (root / it["receipt"]).resolve()
            if path.is_relative_to(root) and path.suffix == ".json":
                receipt = read_json(path)
        source, evidence = launch_source(it, claim, receipt)
        out.append({"item": it.get("id"), "scene_id": it.get("scene_id"),
                    "task_id": it.get("task_id"), "claimed_at": iso(parse(claim.get("claimed_at"))),
                    "submitted_at": iso(submitted), "observed_at": iso(at),
                    "time_basis": "submitted_at" if submitted else "legacy_claimed_at",
                    "run_id": claim.get("run_id"), "source": source, "source_evidence": evidence})
    return sorted(out, key=lambda x: x["observed_at"])


def ready_items(queue):
    return [it.get("id") for it in queue.get("items") or [] if it.get("state") in ("ready", "waiting_for_slot")]


def free_slot_observations(log_lines):
    """log_lines: 'ISO<TAB>subject'. Returns robot observations with at least one free slot."""
    seen = []
    for line in log_lines:
        at, _, subject = line.partition("\t")
        m = SLOTS_RE.search(subject)
        if m and int(m.group(1)) < int(m.group(2)):
            seen.append({"at": at, "occupied": int(m.group(1)), "capacity": int(m.group(2))})
    return seen


def verdict(launch_list, free_seen, ready, launcher_health=None):
    # One scheduled launch earlier in the 24-hour window must not hide a current stalled executor.
    # This unresolved diagnosis is independent of the telemetry robot's health=ok.
    if (launcher_health or {}).get("unresolved"):
        return "launch_stalled"
    sched = [x for x in launch_list if x["source"] == "schedule"]
    if sched:
        return "schedule_launched"
    if free_seen and ready:
        return "historical_free_slots_unverified"
    if launch_list:
        return "chat_only" if all(x["source"] == "chat" for x in launch_list) else "launches_observed"
    return "no_free_slots" if not free_seen else "nothing_ready"


def build(repo, hours, now, log_lines):
    queue = json.loads((Path(repo) / "ops/topview-launch-queue.json").read_text(encoding="utf-8"))
    since = now - timedelta(hours=hours)
    archive = read_json(Path(repo) / "archive/ops/topview-launch-queue-archive.json")
    # Current entries win deduplication; archived completed tasks remain historical evidence.
    combined = {"items": (queue.get("items") or []) + (archive.get("items") or [])}
    ll = launches(combined, since, repo=repo, now=now)
    free = free_slot_observations(log_lines)
    ready = ready_items(queue)
    try:
        launcher = json.loads((Path(repo) / "automation-monitor-status.json").read_text(encoding="utf-8")).get(
            "launcher_health", {})
    except (OSError, ValueError):
        launcher = {}
    v = verdict(ll, free, ready, launcher)
    launcher_checked = parse(launcher.get("checked_at"))
    launcher_stale = not launcher_checked or not timedelta(0) <= now - launcher_checked <= timedelta(minutes=90)
    return {
        "schema_version": 2,
        "checked_at": iso(now),
        "window_hours": hours,
        "verdict": v,
        "launches": ll,
        "launches_by_schedule": sum(1 for x in ll if x["source"] == "schedule"),
        "launches_by_chat": sum(1 for x in ll if x["source"] == "chat"),
        "launches_by_webhook": sum(1 for x in ll if x["source"] == "webhook"),
        "launches_by_manual_run_now": sum(1 for x in ll if x["source"] == "manual_run_now"),
        "launches_unknown_source": sum(1 for x in ll if x["source"] == "unknown"),
        "historical_opportunity_verified": False,
        "historical_opportunity_note": "Past free-slot observations are not joined to historical queue readiness, authorization or leases; no idle-launch incident inferred from them.",
        "free_slot_observations": free[-20:],
        "ready_items_waiting": len(ready),
        "launcher_health": launcher,
        "launcher_observation_stale": launcher_stale,
        "note": "Source requires a task/execution-bound trigger receipt; legacy prefixes retained as labelled evidence. Missing runtime ID never implies chat.",
    }


def git_log(repo, since):
    r = subprocess.run(["git", "-C", str(repo), "log", f"--since={iso(since)}", "--format=%cI\t%s",
                        "--author=github-actions"], text=True, capture_output=True)
    return r.stdout.splitlines()


def notify(report):
    if report["verdict"] == "launch_stalled":
        launcher = report.get("launcher_health") or {}
        text = (f"Текущая потребность в запуске остаётся unresolved: `{launcher.get('state')}` / "
                f"`{launcher.get('reason')}`; наблюдение {launcher.get('checked_at')}, "
                f"просрочено: {report.get('launcher_observation_stale')}. "
                f"За {report['window_hours']} ч подтверждено запусков расписания: {report['launches_by_schedule']}, "
                f"из чата: {report['launches_by_chat']}. Предыдущий запуск не снимает текущий инцидент. "
                "Проверить выполнение существующего handler и фактический исход сохранённых попыток. "
                "Подробно: reports/launch-autonomy.json")
    else:
        return None  # Historical opportunity is not a current actionable incident.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from robot_telemetry import GhNotifier
    return GhNotifier().post("Автозапуск: расписание ChatGPT простаивает", text)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--notify", action="store_true")
    a = ap.parse_args(argv)
    now = datetime.now(timezone.utc)
    report = build(a.repo, a.hours, now, git_log(a.repo, now - timedelta(hours=a.hours)))
    path = Path(a.repo) / OUT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["verdict"], report["launches_by_schedule"], report["launches_by_chat"], len(report["free_slot_observations"]))
    if a.notify and report["verdict"] == "launch_stalled":
        notify(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
