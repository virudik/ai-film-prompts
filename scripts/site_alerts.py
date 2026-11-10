#!/usr/bin/env python3
"""Tell Grok Bot about actionable site problems. The GitHub robots call this.

canon-health.yml and topview-robot.yml already inspect the canon and the Topview
snapshot. This script does not add a Grok schedule and does not poll the site.

A DM goes out only when the set changes. The set is canon-health warn/fail/error
items plus the conditions that turn the dashboard banner red or yellow (stale,
missing or future Topview time, an unhealthy monitor cycle, a canon sync error).
Info notes, including the Sunday cleanup hints, are not included. The same set
is not sent again. Delivery is the existing Agent Relay DM
(ops/relay-wake.json site_alert_address, secret AGENT_RELAY_TOKEN).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import relay_wake  # noqa: E402

STATE = "ops/site-alert-state.json"
STALE_MIN = 120          # index.html STALE_MIN: yellow «данные устарели»
FUTURE_MIN = 10


def read_json(root, rel):
    try:
        return json.loads((Path(root) / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def age_minutes(value, now):
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (now - dt.astimezone(timezone.utc)).total_seconds() / 60


def add(alerts, code, detail, text):
    alerts.append({"code": code, "detail": detail, "text": text})


def collect(root, now):
    """Actionable problems only. Info notes are ignored on purpose."""
    root = Path(root)
    alerts = []
    health = read_json(root, "canon-health.json")
    for problem in health.get("problems") or []:
        if not isinstance(problem, dict) or problem.get("level") not in ("warn", "fail", "error"):
            continue
        text = str(problem.get("text") or "")
        add(alerts, f"canon:{problem.get('code')}:{problem.get('file') or ''}", text, text)

    top = read_json(root, "topview-status.json")
    tv_age = age_minutes(top.get("checked_at"), now)
    if tv_age is None:
        add(alerts, "banner:topview-missing", "missing",
            "Плашка: нет времени проверки Topview (topview-status.json checked_at).")
    elif tv_age < -FUTURE_MIN:
        add(alerts, "banner:topview-future", "future",
            "Плашка: время проверки Topview из будущего.")
    elif tv_age > STALE_MIN:
        add(alerts, "banner:topview-stale", "older-than-2h",
            f"Плашка «ДАННЫЕ TOPVIEW УСТАРЕЛИ»: опубликованный topview-status.json checked_at {top.get('checked_at')}.")

    monitor = read_json(root, "automation-monitor-status.json")
    cycle = monitor.get("last_scheduled_cycle") if isinstance(monitor.get("last_scheduled_cycle"), dict) else {}
    mon_age = age_minutes(cycle.get("completed_at"), now)
    note = str(cycle.get("note") or "")[:180]
    if cycle.get("health") == "degraded":
        add(alerts, "banner:monitor-degraded", note or "degraded",
            "Плашка «МОНИТОР: НЕПОЛНЫЙ ЦИКЛ»: " + (note or "цикл degraded."))
    elif cycle.get("health") == "error":
        add(alerts, "banner:monitor-error", note or "error",
            "Плашка «МОНИТОР: ОШИБКА ЦИКЛА»: " + (note or "цикл error."))
    elif mon_age is None:
        add(alerts, "banner:monitor-missing", "missing", "Плашка: нет времени последнего цикла монитора.")
    elif mon_age < -FUTURE_MIN:
        add(alerts, "banner:monitor-future", "future", "Плашка: время цикла монитора из будущего.")
    elif mon_age > STALE_MIN:
        add(alerts, "banner:monitor-stale", "older-than-2h",
            "Плашка «МОНИТОР НЕ ОТВЕЧАЕТ»: последний цикл старше 2 часов.")

    project = read_json(root, "project-status.json")
    if project and project.get("health") not in (None, "ok"):
        add(alerts, "banner:sync-error", str(project.get("health")),
            f"Красная плашка синхронизации: project-status health = {project.get('health')}.")
    instructions = read_json(root, "instruction-sync-status.json")
    if instructions.get("health") == "error":
        add(alerts, "banner:instruction-error", "error",
            "Красная плашка: проверка семи инструкций нашла расхождение.")
    return alerts


def signature(alerts):
    return sorted(f"{item['code']}|{item.get('detail', '')}" for item in alerts)


def render_text(alerts):
    lines = [
        "Сайт промтов: штатный робот GitHub нашёл ошибки или предупреждения.",
        "Это доклад. Запуск Topview, Create и очередь не менялись.",
        "",
    ]
    lines.extend(f"- {item['text']}" for item in alerts)
    lines.extend(["", "Повтор не придёт, пока этот набор не изменится. Info-заметки чистки сюда не входят."])
    return "\n".join(lines)


def load_state(root):
    data = read_json(root, STATE)
    return data if isinstance(data, dict) else {}


def save_state(root, signature_value, relay):
    path = Path(root) / STATE
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {"schema_version": 1, "signature": signature_value, "relay": relay,
            "rules": "scripts/site_alerts.py; dedup is this signature. Info notes are not included. "
                     "No Grok polling routine."}
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def notify(root, now=None, sender=None):
    """Returns a result dict. Writes the state file only after a confirmed send or a real clear."""
    now = now or datetime.now(timezone.utc)
    alerts = collect(root, now)
    sig = signature(alerts)
    prev = load_state(root)
    prev_sig = prev.get("signature") or []
    prev_status = (prev.get("relay") or {}).get("status")
    if sig == prev_sig and prev_status == "sent":
        return {"action": "unchanged", "count": len(alerts)}
    if not sig:
        if prev_sig:
            save_state(root, [], {"status": "cleared"})
            return {"action": "cleared", "count": 0}
        return {"action": "none", "count": 0}
    cfg = relay_wake.load_config(root)
    if not cfg.get("site_alert_enabled") or not cfg.get("site_alert_address"):
        return {"action": "disabled", "count": len(alerts),
                "detail": "ops/relay-wake.json site_alert_address is not set"}
    text = render_text(alerts)
    if sender is None:
        status, detail = relay_wake.send_dm(
            root, text, address=cfg["site_alert_address"], key_prefix="site-alert-", require_enabled=False)
    else:
        status, detail = sender(text)
    if status != "sent":
        # Do not remember the set: the next robot run retries. A missing token stays visible.
        return {"action": status, "detail": detail, "count": len(alerts)}
    save_state(root, sig, {"status": "sent", "detail": detail, "at": now.strftime("%Y-%m-%dT%H:%M:%SZ")})
    return {"action": "sent", "detail": detail, "count": len(alerts)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--notify", action="store_true")
    args = ap.parse_args(argv)
    result = notify(args.root) if args.notify else {"action": "dry", "count": len(collect(args.root, datetime.now(timezone.utc)))}
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
