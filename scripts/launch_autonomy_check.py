#!/usr/bin/env python3
"""Daily check: does the ChatGPT schedule launch Topview tasks on its own, without an open chat? (owner 17.10.2026)

usage: launch_autonomy_check.py <repo> [--hours 24] [--notify]

Reads only repository data:
  * ops/topview-launch-queue.json — submitted items and their active claim or preserved last_claim.
    A launch made by the scheduled automation has a run_id starting with "chatgpt-scheduled"
    (ops/CONTINUE-PROTOCOL.md); any other run_id is a working chat.
  * git log of the GitHub robot — "Topview telemetry — N/6 slots" messages show whether a slot was free.
Writes reports/launch-autonomy.json. With --notify it posts one comment to the robot's
`topview-events` issue when free slots were seen, ready items waited and the schedule launched nothing.
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


def launches(queue, since):
    out = []
    for it in queue.get("items") or []:
        claim = it.get("claim") or it.get("last_claim") or {}
        at = parse(claim.get("claimed_at"))
        if it.get("state") != "submitted" or not at or at < since:
            continue
        run = str(claim.get("run_id") or "")
        out.append({"item": it.get("id"), "scene_id": it.get("scene_id"), "claimed_at": iso(at), "run_id": run,
                    "source": "schedule" if run.startswith("chatgpt-scheduled") else "chat"})
    return sorted(out, key=lambda x: x["claimed_at"])


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
        return "free_slots_idle_no_schedule_launch"
    if launch_list:
        return "chat_only"
    return "no_free_slots" if not free_seen else "nothing_ready"


def build(repo, hours, now, log_lines):
    queue = json.loads((Path(repo) / "ops/topview-launch-queue.json").read_text(encoding="utf-8"))
    since = now - timedelta(hours=hours)
    ll = launches(queue, since)
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
        "schema_version": 1,
        "checked_at": iso(now),
        "window_hours": hours,
        "verdict": v,
        "launches": ll,
        "launches_by_schedule": sum(1 for x in ll if x["source"] == "schedule"),
        "launches_by_chat": sum(1 for x in ll if x["source"] == "chat"),
        "free_slot_observations": free[-20:],
        "ready_items_waiting": len(ready),
        "launcher_health": launcher,
        "launcher_observation_stale": launcher_stale,
        "note": "Только чтение репозитория. Запуск из расписания = run_id с префиксом chatgpt-scheduled.",
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
        text = (f"За {report['window_hours']} ч робот видел свободные слоты, в очереди ждут "
                f"{report['ready_items_waiting']} готовых пунктов, но в репозитории нет запусков расписания ChatGPT "
                f"(запусков из открытого чата: {report['launches_by_chat']}). "
                "Проверить выполнение существующего задания и его квитанции. Подробно: reports/launch-autonomy.json")
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
    if a.notify and report["verdict"] in ("free_slots_idle_no_schedule_launch", "launch_stalled"):
        notify(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
