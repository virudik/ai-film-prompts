#!/usr/bin/env python3
"""Robot → Agent Relay bridge: one DM to the subscribed ChatGPT inbox per free-slot event.

Owner decision 25.10.2026: Agent Relay is the wake channel (ops/TOPVIEW-EVENT-WAKE.md). The DM only wakes the
executor; it is data, never permission. The executor re-reads main, rescans Topview and checks the GitHub issue
named in the DM before anything else.

Config (no secrets): ops/relay-wake.json. Credential: GitHub secret AGENT_RELAY_TOKEN (an Agent Relay agent token
of the robot's own identity). Without the token or with enabled=false this is a clean no-op.

CLI (used by topview-wake-test.yml):  relay_wake.py <repo> --text-file FILE [--data-json JSON]
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

CONFIG = "ops/relay-wake.json"
TIMEOUT_S = 20


def load_config(root):
    try:
        return json.loads((Path(root) / CONFIG).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def build_request(cfg, token, text, data=None):
    body = {"address": cfg["address"], "text": text}
    if data:
        body["data"] = data
    req = urllib.request.Request(cfg["api_base"].rstrip("/") + "/dm", method="POST",
                                 data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                                          "User-Agent": "ai-film-topview-robot"})
    return req


def send_dm(root, text, data=None, *, token=None, opener=urllib.request.urlopen):
    """Returns (status, detail). status: sent | disabled | no_token | error. Never raises."""
    cfg = load_config(root)
    if not cfg.get("enabled") or not cfg.get("address") or not cfg.get("api_base"):
        return "disabled", "ops/relay-wake.json disabled or incomplete"
    token = (token if token is not None else os.environ.get("AGENT_RELAY_TOKEN", "")).strip()
    if not token:
        return "no_token", "secret AGENT_RELAY_TOKEN is not set"
    try:
        with opener(build_request(cfg, token, text, data), timeout=TIMEOUT_S) as r:
            raw = r.read().decode("utf-8", "replace")
            code = getattr(r, "status", 200)
    except urllib.error.HTTPError as e:
        return "error", f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}"
    except (urllib.error.URLError, OSError, ValueError) as e:
        return "error", f"{type(e).__name__}: {str(e)[:200]}"
    if not 200 <= code < 300:
        return "error", f"HTTP {code}: {raw[:200]}"
    try:
        mid = (json.loads(raw) or {}).get("id") or (json.loads(raw).get("message") or {}).get("id")
    except (ValueError, AttributeError):
        mid = None
    return "sent", f"message_id={mid}" if mid else "accepted"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--text-file", required=True)
    ap.add_argument("--data-json", default="")
    a = ap.parse_args(argv)
    data = json.loads(a.data_json) if a.data_json else None
    status, detail = send_dm(a.repo, Path(a.text_file).read_text(encoding="utf-8"), data)
    print(f"relay_wake: {status} ({detail})")
    return 0 if status == "sent" else 1


if __name__ == "__main__":
    sys.exit(main())
