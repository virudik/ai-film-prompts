#!/usr/bin/env python3
"""Report site problems to Dot first, then Grok after event-specific inactivity.

Uses existing robot invocations, never starts video or changes queue/lease.
All site problems wait 120 minutes. Exact current
incident ACK/progress can postpone backup; a historical commit cannot.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import relay_wake  # noqa: E402
import wake_roles  # noqa: E402

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


def add(alerts, code, detail, text, critical=False):
    alerts.append({"code": code, "detail": detail, "text": text, "critical": critical})


def collect(root, now):
    """Actionable problems only. Info notes are ignored on purpose."""
    root = Path(root)
    alerts = []
    health = read_json(root, "canon-health.json")
    for problem in health.get("problems") or []:
        if not isinstance(problem, dict) or problem.get("level") not in ("warn", "fail", "error"):
            continue
        text = str(problem.get("text") or "")
        add(alerts, f"canon:{problem.get('code')}:{problem.get('file') or ''}", text, text, problem.get("level") in ("fail", "error"))

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
            "Плашка «МОНИТОР: ОШИБКА ЦИКЛА»: " + (note or "цикл error."), True)
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
            f"Красная плашка синхронизации: project-status health = {project.get('health')}.", project.get('health') in ('fail', 'error'))
    instructions = read_json(root, "instruction-sync-status.json")
    if instructions.get("health") == "error":
        add(alerts, "banner:instruction-error", "error",
            "Красная плашка: проверка семи инструкций нашла расхождение.", True)
    return alerts


def signature(alerts):
    return sorted(f"{item['code']}|critical={bool(item.get('critical'))}" for item in alerts)


def render_text(alerts):
    lines = [
        "Сайт промтов: штатный робот GitHub нашёл ошибки или предупреждения.",
        "Это доклад. Запуск Topview, Create и очередь не менялись.",
        "",
    ]
    lines.extend(f"- {item['text']}" for item in alerts)
    lines.extend(["", "Повтор не придёт, пока этот набор не изменится. Info-заметки чистки сюда не входят."])
    return "\n".join(lines)


# Stable human-readable labels: dynamic timestamps/counts from collect() must not
# alter the transport idempotency key when a state push is rejected and retried.
PROBLEM_LABELS = {
    "topview-missing": "Нет времени проверки Topview",
    "topview-future": "Время проверки Topview из будущего",
    "topview-stale": "ДАННЫЕ TOPVIEW УСТАРЕЛИ: проверка старше двух часов",
    "monitor-degraded": "Монитор завершил неполный цикл",
    "monitor-error": "Ошибка цикла монитора",
    "monitor-missing": "Нет времени последнего цикла монитора",
    "monitor-future": "Время цикла монитора из будущего",
    "monitor-stale": "Монитор не отвечает больше двух часов",
    "sync-error": "Ошибка состояния синхронизации проекта",
    "instruction-error": "Проверка семи инструкций нашла расхождение",
    "handoff-size": "Хендоф превышает рекомендуемый размер",
    "handoff-now-undated": "Верхний блок хендофа без даты",
    "handoff-now-stale": "Верхний блок хендофа устарел",
    "instruction-missing": "Отсутствует обязательная инструкция",
    "broken-ref": "Инструкция ссылается на отсутствующий файл",
    "task-stuck": "Задача владельца долго не продвигается",
    "queue-scene-gone": "В очереди осталась сцена, отсутствующая в мастере",
    "status-health": "Проверка состояния проекта не прошла",
    "project-handoff-missing": "Отсутствует хендоф проекта",
    "project-handoff-size": "Хендоф проекта превышает рекомендуемый размер",
    "service-file-size": "Служебный файл превышает рекомендуемый размер",
}


def describe_problem(alert):
    parts = alert["code"].split(":", 2)
    label = PROBLEM_LABELS.get(parts[1] if len(parts) > 1 else "", "Проблема сайта")
    level = "ошибка" if alert.get("critical") else "предупреждение"
    return f"{label} [{level}; {alert['code']}]"


def load_state(root):
    data = read_json(root, STATE)
    return data if isinstance(data, dict) else {}


RECEIPTS = "reports/site-alert-receipts.json"


def stamp(now):
    return now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save_state(root, body):
    path = Path(root) / STATE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def progress_at(root, incident, now):
    """Only an explicit receipt for this incident and Dot is progress, not git activity."""
    baseline = incident["first_seen_at"]
    first_age = age_minutes(baseline, now)
    if first_age is None or first_age < 0:
        return None
    valid = [(first_age, baseline)]
    data = read_json(root, RECEIPTS)
    rows = data.get("events", []) if isinstance(data, dict) else []
    for row in rows if isinstance(rows, list) else []:
        if (not isinstance(row, dict) or row.get("incident_id") != incident["incident_id"] or
                row.get("actor") != incident.get("primary_actor", "dot") or row.get("state") not in ("acknowledged", "in_progress") or
                not row.get("evidence")):
            continue
        value = row.get("updated_at")
        age = age_minutes(value, now)
        # Require explicit timezone; never accept a future or pre-incident ACK.
        try:
            aware = datetime.fromisoformat(str(value).replace("Z", "+00:00")).tzinfo is not None
        except ValueError:
            aware = False
        if aware and age is not None and 0 <= age <= first_age:
            valid.append((age, value))
    return min(valid)[1]


def notify_legacy(root, now, sender, alerts, cfg):
    """Preserve the existing Grok route until V2 is explicitly enabled."""
    sig = sorted(f"{a['code']}|{a.get('detail', '')}" for a in alerts)
    prev = load_state(root)
    if sig == (prev.get("signature") or []) and (prev.get("relay") or {}).get("status") == "sent":
        return {"action": "unchanged", "count": len(alerts)}
    if not sig:
        if prev.get("signature"):
            save_state(root, {"schema_version": 1, "signature": [], "relay": {"status": "cleared"},
                              "sequence": prev.get("sequence", 0)})
            return {"action": "cleared", "count": 0}
        return {"action": "none", "count": 0}
    address = cfg.get("site_alert_address")
    if not cfg.get("site_alert_enabled") or not address:
        return {"action": "disabled", "count": len(alerts)}
    text = render_text(alerts)
    if sender is None:
        status, detail = relay_wake.send_dm(root, text, address=address, key_prefix="site-alert-", require_enabled=False)
    else:
        status, detail = sender(text, address=address, target="legacy")
    if status == "sent":
        save_state(root, {"schema_version": 1, "signature": sig, "sequence": prev.get("sequence", 0),
                          "relay": {"status": status, "detail": detail, "at": stamp(now)}})
    return {"action": status, "detail": detail, "count": len(alerts)}


def notify(root, now=None, sender=None, *, prepare_only=False, require_prepared=False):
    now = now or datetime.now(timezone.utc)
    alerts = collect(root, now)
    sig = signature(alerts)
    prev = load_state(root)
    cfg = relay_wake.load_config(root)
    routing = cfg.get("site_alert_routing")
    # A malformed optional rollout block must not break the existing Grok path.
    if not isinstance(routing, dict):
        routing = {}
    if routing.get("enabled") is not True:
        if prepare_only:
            return {"action": "legacy", "count": len(alerts)}
        return notify_legacy(root, now, sender, alerts, cfg)
    roles = wake_roles.resolve(cfg)
    if roles is None:
        return {"action": "disabled", "detail": "invalid wake roles", "count": len(alerts)}
    primary_actor, backup_actor = roles["primary_actor"], roles["backup_actor"]
    addresses = {"dot": routing.get("primary_address"), "grok": routing.get("backup_address")}
    primary, backup = addresses[primary_actor], addresses[backup_actor]
    same_roles = (prev.get("primary_actor", "dot") == primary_actor and
                  prev.get("backup_actor", "grok") == backup_actor)
    if not sig:
        if prev.get("signature"):
            save_state(root, {"schema_version": 2, "signature": [], "sequence": prev.get("sequence", 0),
                              "relay": {"status": "cleared"}})
            return {"action": "cleared", "count": 0}
        return {"action": "none", "count": 0}
    if not cfg.get("site_alert_enabled") or not primary or not backup or routing.get("mode") not in ("dot_then_grok", "primary_then_backup"):
        return {"action": "disabled", "count": len(alerts), "detail": "site routing incomplete"}
    if prev.get("schema_version") == 2 and prev.get("signature") == sig and same_roles:
        current = prev
    else:
        continuing = same_roles and prev.get("schema_version") == 2 and bool(set(prev.get("problem_since", {})) & {a["code"] for a in alerts})
        if continuing:
            current = dict(prev)
            current.update(signature=sig, critical=any(a.get("critical") for a in alerts))
        else:
            sequence = int(prev.get("sequence", 0)) + 1
            key = hashlib.sha256(json.dumps(sig, ensure_ascii=False).encode()).hexdigest()[:20]
            current = {"schema_version": 2, "signature": sig, "sequence": sequence,
                       "incident_id": f"site:{key}:{sequence}", "first_seen_at": stamp(now),
                       "critical": any(a.get("critical") for a in alerts)}
        # Changing unrelated warnings must not restart the clock of a persistent failure.
        old_since = (prev.get("problem_since") or {}) if continuing else {}
        current["problem_since"] = {a["code"]: old_since.get(a["code"], stamp(now)) for a in alerts}
        versions = dict(prev.get("problem_versions") or {}) if continuing else {}
        for a in alerts:
            code = a["code"]
            versions[code] = versions.get(code, 0) + (0 if code in old_since and code in versions else 1)
        current["problem_versions"] = versions
        relevant = [a for a in alerts if a.get("critical")] or alerts
        ages = [(age_minutes(current["problem_since"][a["code"]], now), current["problem_since"][a["code"]]) for a in relevant]
        valid_ages = [(age, value) for age, value in ages if age is not None and age >= 0]
        if valid_ages:
            current["first_seen_at"] = max(valid_ages)[1]
    current["primary_actor"], current["backup_actor"] = primary_actor, backup_actor
    timeout = routing.get("critical_timeout_minutes", 120) if current.get("critical") else routing.get("warning_timeout_minutes", 120)
    if type(timeout) is not int or not 5 <= timeout <= 1440:
        return {"action": "disabled", "detail": "invalid site timeout", "count": len(alerts)}
    target = "primary"
    primary_sent = ((current.get("primary") or {}).get("status") == "sent" and
                    (current.get("primary") or {}).get("signature") == sig)
    # Coverage is per problem occurrence, not a single forever-sent incident flag.
    # A new critical problem must have its own backup even in a continuing episode.
    def occurrence(alert):
        return f"{alert['code']}|critical={bool(alert.get('critical'))}|{current['problem_versions'][alert['code']]}"
    coverage = set(current.get("backup_coverage", []))
    uncovered = [a for a in alerts if occurrence(a) not in coverage]
    due = False
    for alert in uncovered:
        limit = routing.get("critical_timeout_minutes", 120) if alert.get("critical") else routing.get("warning_timeout_minutes", 120)
        if type(limit) is not int or not 5 <= limit <= 1440:
            return {"action": "disabled", "detail": "invalid site timeout", "count": len(alerts)}
        baseline = current["problem_since"][alert["code"]]
        progress = progress_at(root, dict(current, first_seen_at=baseline), now)
        elapsed = age_minutes(progress, now) if progress else None
        if elapsed is not None and elapsed >= limit:
            due = True
            timeout = limit
            break
    if due:
        target = "backup"
    elif primary_sent:
        if current != prev: save_state(root, current)
        return {"action": "unchanged", "count": len(alerts), "incident_id": current["incident_id"]}
    attempt = current.get(target) or {}
    attempt_age = age_minutes(attempt.get("at"), now)
    if attempt.get("status") != "sent" and attempt_age is not None and 0 <= attempt_age < 10:
        # The state commit itself can trigger canon-health. Avoid retry/commit loops.
        return {"action": "retry_deferred", "count": len(alerts), "incident_id": current["incident_id"]}
    occurrence_token = hashlib.sha256(json.dumps(sorted(occurrence(a) for a in alerts)).encode()).hexdigest()[:20]
    pending = {"target": target, "signature": sig, "occurrence_set": occurrence_token,
               "address": primary if target == "primary" else backup, "timeout_minutes": timeout,
               "actor": primary_actor if target == "primary" else backup_actor}
    if prepare_only:
        current["pending_delivery"] = pending
        save_state(root, current)
        return {"action": "prepared", "incident_id": current["incident_id"], "target": target}
    if require_prepared and (prev.get("incident_id") != current["incident_id"] or
                             prev.get("pending_delivery") != pending):
        return {"action": "prepare_required", "count": len(alerts)}
    # CLI callers must CAS-publish --prepare before --notify. This makes the exact
    # incident visible to the receiver before Relay can deliver its message.
    # Stable payload across simultaneous workflows/retries: no current timestamp in DM.
    lines = ["SITE_ALERT_V2 " + current["incident_id"], "recipient_role=" + target,
             "recipient_actor=" + (primary_actor if target == "primary" else backup_actor),
             "Предупреждения сайта. Это не запуск видео и не разрешение Create."]
    lines.append("occurrence_set=" + occurrence_token)
    lines += ["- " + describe_problem(item) for item in sorted(alerts, key=lambda a: a["code"])]
    lines += ["Подробности: canon-health.json и текущие файлы статуса в main.",
              f"Порог без ACK/прогресса {primary_actor}: {timeout} мин.",
              "Прочитайте свежий main, подтвердите текущий incident_id в reports/site-alert-receipts.json.",
              "Перед исправлениями проверьте точную lease и текущий результат; чужой замок не перехватывать."]
    if target == "backup":
        lines.append(f"{backup_actor}: проверьте проблему и сообщите владельцу результат; исторический started-коммит не доказывает живую работу {primary_actor}.")
    text = "\n".join(lines)
    address = primary if target == "primary" else backup
    if sender is None:
        status, detail = relay_wake.send_dm(root, text, address=address,
                                           key_prefix="site-alert-v2-", require_enabled=False)
    else:
        status, detail = sender(text, address=address, target=target)
    current.pop("pending_delivery", None)
    current[target] = {"status": status, "detail": detail, "at": stamp(now), "signature": sig}
    if target == "backup" and status == "sent":
        current["backup_coverage"] = sorted(coverage | {occurrence(a) for a in alerts})
    current["relay"] = current[target]
    # Failed delivery is recorded but never counted as ACK/sent; next robot run retries.
    save_state(root, current)
    return {"action": status, "detail": detail, "count": len(alerts),
            "incident_id": current["incident_id"], "target": target}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--notify", action="store_true")
    mode.add_argument("--prepare", action="store_true")
    args = ap.parse_args(argv)
    result = (notify(args.root, prepare_only=args.prepare, require_prepared=args.notify)
              if args.notify or args.prepare else
              {"action": "dry", "count": len(collect(args.root, datetime.now(timezone.utc)))})
    print(json.dumps(result, ensure_ascii=False))
    return 1 if result["action"] == "prepare_required" else 0


if __name__ == "__main__":
    sys.exit(main())
