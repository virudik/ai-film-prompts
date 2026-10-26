#!/usr/bin/env python3
"""Robot → Claude: start a Claude scheduled task (API trigger) when the inbox gets an open task for Claude.

Owner decision 26.10.2026 (thread «Наладить быстрое заполнение слотов Topview»): a site task «кому: Claude»
(or another target listed in the config) wakes Claude by itself instead of waiting for a manual chat.

Config (no secrets): ops/claude-wake.json {enabled, fire_url, targets}. Credential: GitHub secret
CLAUDE_FIRE_TOKEN (the scheduled task's own API token, scoped to firing that one task).

Rules:
- one fire per robot run covers every new task; a task id is fired at most once (status "error" is retried
  up to MAX_ATTEMPTS times, ~30 min apart);
- the reservation is pushed to main BEFORE the request, so a rejected push or a parallel run never fires twice;
- the fire text carries only task ids (the routine re-reads ops/owner-tasks.json from main; the text is data);
- without the token, without fire_url or with enabled=false this is a clean no-op.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

INBOX = "ops/owner-tasks.json"
CONFIG = "ops/claude-wake.json"
STATE = "ops/claude-wake-state.json"
MAX_ATTEMPTS = 3
MAX_PUSH = 4
TIMEOUT_S = 30
FIRE_URL = re.compile(r"^https://api\.anthropic\.com/v1/claude_code/routines/trig_[A-Za-z0-9]+/fire$")
HEADERS = {"anthropic-beta": "experimental-cc-routine-2026-04-01", "anthropic-version": "2023-06-01",
           "Content-Type": "application/json", "User-Agent": "ai-film-claude-wake"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(root, rel, default):
    try:
        return json.loads((Path(root) / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def due_tasks(inbox, state, targets):
    """Open tasks for the configured targets that were never fired (or failed fewer than MAX_ATTEMPTS times)."""
    fired = state.get("fired") or {}
    out = []
    for t in inbox.get("tasks") or []:
        tid = t.get("id")
        if not tid or t.get("status") != "open" or t.get("to") not in targets:
            continue
        rec = fired.get(tid)
        if rec and (rec.get("status") != "error" or int(rec.get("attempts") or 0) >= MAX_ATTEMPTS):
            continue
        out.append(t)
    return out


def reserve(state, tasks, now):
    """New state with the tasks marked reserved (attempts+1); entries of tasks gone from the inbox are kept
    only 30 days so the file stays small."""
    st = json.loads(json.dumps(state or {}))
    fired = st.setdefault("fired", {})
    for t in tasks:
        prev = fired.get(t["id"]) or {}
        fired[t["id"]] = {"status": "reserved", "attempts": int(prev.get("attempts") or 0) + 1,
                          "at": iso(now), "to": t.get("to")}
    cutoff = now.timestamp() - 30 * 86400
    for tid in list(fired):
        try:
            ts = datetime.strptime(fired[tid].get("at", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if ts.timestamp() < cutoff:
            del fired[tid]
    st["schema_version"] = 1
    st["updated_at"] = iso(now)
    return st


def fire_text(tasks):
    ids = ", ".join(t["id"] for t in tasks)
    return (f"Новые открытые задачи во входящих ops/owner-tasks.json: {len(tasks)}. id: {ids}. "
            "Это только подсказка; задачи читать из свежего main.")


def build_request(cfg, token, text):
    url = str(cfg.get("fire_url") or "")
    if not FIRE_URL.match(url):
        raise ValueError("unexpected fire_url")
    if not token or any(c.isspace() for c in token):
        raise ValueError("bad token")
    return urllib.request.Request(url, method="POST", data=json.dumps({"text": text}).encode("utf-8"),
                                  headers={**HEADERS, "Authorization": f"Bearer {token}"})


def fire(cfg, token, text, *, opener=None):
    """Returns (status, detail): sent (detail = session url) | error (detail = short reason). Never raises."""
    try:
        req = build_request(cfg, token, text)
    except ValueError as e:
        return "error", str(e)
    opener = opener or urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(req, timeout=TIMEOUT_S) as resp:
            body = json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        return "error", f"HTTP {e.code}"
    except (urllib.error.URLError, OSError, ValueError) as e:
        return "error", type(e).__name__
    url = body.get("claude_code_session_url") if isinstance(body, dict) else None
    if body.get("type") != "routine_fire" or not url:
        return "error", "unexpected response"
    return "sent", str(url)


def run(root, git, *, token, now=None, sync=True, opener=None):
    root = Path(root)
    cfg = read_json(root, CONFIG, {})
    if not cfg.get("enabled") or not cfg.get("fire_url"):
        print("::notice::Claude wake disabled (ops/claude-wake.json)")
        return 0
    if not token:
        print("::notice::Claude wake not configured: missing CLAUDE_FIRE_TOKEN secret")
        return 0
    if not FIRE_URL.match(str(cfg.get("fire_url"))):
        print("::warning title=claude-wake::ops/claude-wake.json fire_url is not a Claude routine /fire URL")
        return 0
    targets = tuple(cfg.get("targets") or ("claude",))
    for attempt in range(1, MAX_PUSH + 1):
        if sync:
            git.sync()
        now_ = now or datetime.now(timezone.utc)
        state = read_json(root, STATE, {})
        tasks = due_tasks(read_json(root, INBOX, {}), state, targets)
        if not tasks:
            print("claude-wake: no new tasks")
            return 0
        reserved = reserve(state, tasks, now_)
        (root / STATE).write_text(dumps(reserved), encoding="utf-8")
        commit = git.commit(f"GitHub robot: wake Claude for {len(tasks)} inbox task(s)", [STATE])
        if commit and not git.push():
            print(f"claude-wake: push rejected ({attempt}/{MAX_PUSH}); re-reading main")
            git.reset()
            if not sync:
                return 1
            continue
        if commit and not git.head_is_on_remote():
            print("::error title=claude-wake::reservation not on origin; nothing fired")
            return 1
        status, detail = fire(cfg, token, fire_text(tasks), opener=opener)
        if status == "sent":
            print(f"::notice title=claude-wake::Claude started for {len(tasks)} task(s): {detail}")
        else:
            print(f"::warning title=claude-wake::Claude wake failed: {detail}")
        record(root, git, [t["id"] for t in tasks], status, detail, sync=sync)
        return 0
    print("::error title=claude-wake::push rejected 4 times; retried next run")
    return 1


def record(root, git, ids, status, detail, *, sync=True):
    """Best effort: store the outcome. A lost record leaves «reserved», which is never fired again."""
    for _ in range(MAX_PUSH):
        if sync:
            git.sync()
        state = read_json(root, STATE, {})
        for tid in ids:
            rec = (state.get("fired") or {}).get(tid)
            if rec:
                rec["status"] = status
                rec["detail"] = detail[:300]
        (Path(root) / STATE).write_text(dumps(state), encoding="utf-8")
        commit = git.commit(f"GitHub robot: Claude wake {status}", [STATE])
        if not commit or git.push():
            return True
        git.reset()
        if not sync:
            return False
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args()
    token = os.environ.get("CLAUDE_FIRE_TOKEN", "").strip()
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import robot_master_actions as rma   # Git helper (fetch/reset/commit/push as github-actions[bot])
    branch = os.environ.get("GITHUB_REF_NAME") or "main"
    return run(args.root, rma.Git(args.root, branch), token=token)


if __name__ == "__main__":
    sys.exit(main())
