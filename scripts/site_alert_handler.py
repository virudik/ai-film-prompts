#!/usr/bin/env python3
"""Receiving side of SITE_ALERT_V2 / SITE_ALERT_V2_TEST for Dot or Grok.

Contract: ops/SITE-ALERT-V2-RECEIVER.md. Builds on the read-only admission gate
``site_alert_receiver.validate`` (PR 747) and adds what the gate deliberately
leaves to the receiving agent:

* fresh canonical main (fetch; HEAD must equal origin/main, clean tree);
* duplicate suppression by the authenticated Relay message ID;
* the agent's own canon lease (``ops/canon-lock.json``, holder ``<actor>:<UUID4>``)
  taken with a CAS push and read back before writing;
* the receipt row in ``reports/site-alert-receipts.json`` written together with
  the lease release, pushed with CAS and read back from origin/main;
* SITE_ALERT_V2_TEST: read-only terminal report only, exact allowlist from the
  caller's saved routine prompt (empty by default), no repository writes.

Every result is terminal for a site event: the caller must not fall through to
the Topview/slot handler, launch video, touch the queue or call Topview.
Any mismatch fails closed with ``ok=false`` and an explicit ``reason``.
No network calls besides ``git fetch``/``git push`` of the given checkout.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import canon_lock  # noqa: E402
import site_alert_receiver  # noqa: E402
import site_alerts  # noqa: E402

RECEIPTS = site_alerts.RECEIPTS
LOCK = canon_lock.LOCK
LEASE_MINUTES = 10
MAX_ATTEMPTS = 6
MAX_EVENTS = 200
STATES = ("acknowledged", "in_progress", "blocked", "resolved")
ID_RE = re.compile(r"[A-Za-z0-9_.:@-]{1,160}")
TERMINAL_NOTE = "terminal: site event; do not continue to Topview/slot handler; no Create/queue/lease for video"


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(repo, *args, check=False):
    proc = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    if check and proc.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {(proc.stderr or proc.stdout).strip()[:300]}")
    return proc


class GitError(RuntimeError):
    pass


def head_sha(repo, ref="HEAD"):
    return git(repo, "rev-parse", ref, check=True).stdout.strip()


def is_clean(repo):
    return git(repo, "status", "--porcelain", check=True).stdout.strip() == ""


def fresh_main(repo, sync):
    """Fetch origin/main; optionally fast-reset a clean dedicated checkout. Returns SHA."""
    git(repo, "fetch", "--quiet", "origin", "main", check=True)
    if not is_clean(repo):
        raise GitError("dirty_checkout")
    remote = head_sha(repo, "origin/main")
    if head_sha(repo) != remote:
        if not sync:
            raise GitError("not_fresh_main")
        git(repo, "reset", "--quiet", "--hard", "origin/main", check=True)
    if head_sha(repo) != remote:
        raise GitError("not_fresh_main")
    return remote


def read_json(repo, rel):
    try:
        data = json.loads((Path(repo) / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data


def write_json(repo, rel, data):
    path = Path(repo) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def receipts(repo):
    data = read_json(repo, RECEIPTS)
    if data is None:
        return {"schema_version": 1, "events": []}
    if not isinstance(data, dict) or not isinstance(data.get("events"), list):
        raise ValueError("invalid_receipts_file")
    return data


def commit_push(repo, paths, message):
    git(repo, "add", "--", *paths, check=True)
    ident = []
    if not git(repo, "config", "user.email").stdout.strip():
        ident = ["-c", "user.name=site-alert-handler", "-c", "user.email=site-alert-handler@users.noreply.github.com"]
    c = subprocess.run(["git", "-C", str(repo), *ident, "commit", "--quiet", "-m", message],
                       text=True, capture_output=True)
    if c.returncode != 0:
        raise GitError("commit_failed: " + (c.stderr or c.stdout).strip()[:300])
    # Plain push: a non-fast-forward rejection is the CAS failure. Never force.
    return git(repo, "push", "--quiet", "origin", "HEAD:main").returncode == 0


def classify(text):
    if not isinstance(text, str) or not text:
        return None
    first = text.splitlines()[0]
    if not first.startswith("SITE_ALERT"):
        return None
    if first == "SITE_ALERT_V2_TEST":
        return "test"
    if first.startswith("SITE_ALERT_V2 "):
        return "production"
    return "unknown"


def result(ok, outcome, **extra):
    body = {"ok": ok, "outcome": outcome, "terminal": True, "topview": "not_called",
            "note": TERMINAL_NOTE}
    body.update(extra)
    return body


def handle(repo, text, *, actor, authenticated_sender_id, message_id, event_id=None,
           run_id=None, allowed_test_ids=(), state="acknowledged", evidence=None,
           sync=False, now=None, clock=None, hooks=None):
    """Process one authenticated Relay event. Never raises; always terminal."""
    hooks = hooks or {}
    clock = clock or (lambda: now or datetime.now(timezone.utc))
    kind = classify(text)
    if kind is None:
        # Not a site event at all: the only non-terminal answer.
        return {"ok": False, "outcome": "not_site_alert", "terminal": False}
    base = {"actor": actor, "message_id": message_id, "event_id": event_id, "run_id": run_id}
    if actor not in ("dot", "grok"):
        return result(False, "rejected", reason="invalid_actor", **base)
    if not isinstance(message_id, str) or not ID_RE.fullmatch(message_id):
        return result(False, "rejected", reason="missing_authenticated_message_id", **base)
    if kind == "unknown":
        return result(False, "rejected", reason="unknown_site_marker", **base)
    if state not in STATES:
        return result(False, "rejected", reason="invalid_state", **base)
    if kind == "test" and state != "acknowledged":
        return result(False, "rejected", reason="test_is_read_only", **base)
    try:
        main_sha = fresh_main(repo, sync)
    except GitError as exc:
        return result(False, "rejected", reason=str(exc) if str(exc) in ("dirty_checkout", "not_fresh_main") else "fetch_failed",
                      detail=str(exc), **base)
    received_at = iso(clock())
    gate = site_alert_receiver.validate(repo, text, actor=actor, authenticated_sender_id=authenticated_sender_id,
                                        allowed_test_ids=tuple(allowed_test_ids), now=clock())
    base.update(main_sha=main_sha, received_at_utc=received_at)
    if kind == "test":
        if not gate.get("accepted"):
            return result(False, "rejected", reason=gate.get("reason", "rejected"), kind="test", writes="none", **base)
        unchanged = is_clean(repo) and head_sha(repo) == main_sha
        return result(unchanged, "test_received" if unchanged else "rejected",
                      reason=None if unchanged else "checkout_changed_during_test",
                      kind="test", test_id=gate["test_id"], role=gate["role"], writes="none",
                      read_only=True, **base)
    if state == "resolved":
        return _write_receipt(repo, text, gate, base, state, evidence, sync, clock, hooks, resolved=True,
                              allowed_test_ids=allowed_test_ids, authenticated_sender_id=authenticated_sender_id)
    if not gate.get("accepted"):
        return result(False, "rejected", reason=gate.get("reason", "rejected"), kind="production",
                      writes="none", receipt="not_saved", **base)
    return _write_receipt(repo, text, gate, base, state, evidence, sync, clock, hooks, resolved=False,
                          allowed_test_ids=allowed_test_ids, authenticated_sender_id=authenticated_sender_id)


def _incident_from(text):
    return text.splitlines()[0].split(" ", 1)[1].strip()


def _field(text, key):
    for line in text.splitlines()[1:]:
        if line.startswith(key + "="):
            return line.split("=", 1)[1]
    return None


def _dedup(rows, incident_id, actor, message_id, state):
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("incident_id") == incident_id and row.get("actor") == actor:
            if row.get("message_id") == message_id and row.get("state") == state:
                return "duplicate_message"
            if state == "acknowledged" and row.get("state") == "acknowledged":
                return "already_acknowledged"
    return None


def _write_receipt(repo, text, gate, base, state, evidence, sync, clock, hooks, *, resolved,
                   allowed_test_ids, authenticated_sender_id):
    actor = base["actor"]
    incident_id = gate.get("incident_id") or _incident_from(text)
    if state != "acknowledged" and not (isinstance(evidence, str) and evidence.strip()):
        return result(False, "rejected", reason="evidence_required", kind="production", receipt="not_saved", **base)
    holder = f"{actor}:{uuid.uuid4()}"
    out = dict(base, kind="production", incident_id=incident_id, state=state, holder=holder)
    lease_pushed = False
    try:
        # Count only rejected pushes (real CAS losses). Taking the lease and the
        # follow-up re-validation pass do not consume the retry budget.
        cas_failures = 0
        out["cas_retries"] = 0
        for step in range(2 * MAX_ATTEMPTS + 2):  # hard safety bound
            if cas_failures >= MAX_ATTEMPTS:
                break
            if step > 0:
                out["main_sha"] = fresh_main(repo, True)
            now = clock()
            # Re-run the gate on every fresh main: incident must still be current.
            if resolved:
                gate_reason = _resolved_gate(repo, incident_id, actor, authenticated_sender_id)
            else:
                g = site_alert_receiver.validate(repo, text, actor=actor, authenticated_sender_id=authenticated_sender_id,
                                                 allowed_test_ids=tuple(allowed_test_ids), now=now)
                gate_reason = None if g.get("accepted") and g.get("kind") == "production" else g.get("reason", "rejected")
                if gate_reason is None:
                    out["role"] = g["role"]
            if gate_reason:
                return _finish_fail(repo, out, gate_reason, lease_pushed, holder, clock)
            try:
                rows = receipts(repo)["events"]
            except ValueError as exc:
                return _finish_fail(repo, out, str(exc), lease_pushed, holder, clock)
            dup = _dedup(rows, incident_id, actor, base["message_id"], state)
            if dup:
                return _finish_fail(repo, out, dup, lease_pushed, holder, clock, outcome="duplicate")
            lock = canon_lock.read(repo)
            ours = canon_lock.is_held(lock, now) and lock.get("holder") == holder
            if canon_lock.is_held(lock, now) and not ours:
                return _finish_fail(repo, out, "blocked_lock", lease_pushed, holder, clock,
                                    lock_holder=lock.get("holder"), lock_expires_at=lock.get("expires_at"))
            if not ours:
                new = canon_lock.acquire(lock, holder, f"SITE_ALERT_V2 receipt {incident_id}", LEASE_MINUTES, now)
                write_json(repo, LOCK, new)
                if not commit_push(repo, [LOCK], f"Site alert V2: {actor} lease for receipt {incident_id}"):
                    cas_failures += 1
                    out["cas_retries"] = cas_failures
                    continue  # CAS lost: re-read main and decide again.
                lease_pushed = True
                if "after_lease" in hooks:
                    hooks["after_lease"]()
                fresh_main(repo, True)
                lock = canon_lock.read(repo)
                if not (canon_lock.is_held(lock, clock()) and lock.get("holder") == holder):
                    return _finish_fail(repo, out, "lease_readback_failed", False, holder, clock)
                continue  # Re-validate the incident on the main that contains our lease.
            row = {"incident_id": incident_id, "actor": actor, "role": out.get("role") or _field(text, "recipient_role"),
                   "state": state, "updated_at": iso(clock()),
                   "evidence": (evidence or "").strip() or (
                       f"admission gate passed on main {out['main_sha'][:12]}: authenticated robot sender, "
                       f"{actor} is current {out.get('role')} by wake_roles, incident current, occurrence_set "
                       f"{_field(text, 'occurrence_set')}"),
                   "message_id": base["message_id"], "event_id": base["event_id"], "run_id": base["run_id"],
                   "occurrence_set": _field(text, "occurrence_set"), "read_main_sha": out["main_sha"],
                   "holder": holder}
            data = receipts(repo)
            data["schema_version"] = 1
            data["rules"] = "ops/SITE-ALERT-V2-RECEIVER.md"
            data["events"] = (data["events"] + [row])[-MAX_EVENTS:]
            write_json(repo, RECEIPTS, data)
            write_json(repo, LOCK, canon_lock.release(lock, holder, clock()))
            if "before_receipt_push" in hooks:
                hooks["before_receipt_push"]()
            if not commit_push(repo, [RECEIPTS, LOCK], f"Site alert V2: {actor} {state} {incident_id}; lease released"):
                cas_failures += 1
                out["cas_retries"] = cas_failures
                continue
            lease_pushed = False
            fresh_main(repo, True)
            back = receipts(repo)["events"]
            found = any(r.get("message_id") == base["message_id"] and r.get("holder") == holder and
                        r.get("state") == state for r in back if isinstance(r, dict))
            lock = canon_lock.read(repo)
            if not found or canon_lock.is_held(lock, clock()):
                return result(False, "receipt_readback_failed", reason="receipt_readback_failed", **out)
            out["receipt_commit"] = head_sha(repo)
            return result(True, state, receipt="saved", lease="released", **out)
        return _finish_fail(repo, out, "cas_exhausted", lease_pushed, holder, clock)
    except (GitError, ValueError, OSError) as exc:
        return _finish_fail(repo, out, "git_error", lease_pushed, holder, clock, detail=str(exc)[:300])


def _resolved_gate(repo, incident_id, actor, authenticated_sender_id):
    cfg = site_alert_receiver.relay_wake.load_config(repo)
    if not isinstance(cfg, dict) or authenticated_sender_id != cfg.get("sender_agent_id"):
        return "wrong_authenticated_sender"
    try:
        rows = receipts(repo)["events"]
    except ValueError:
        return "invalid_receipts_file"
    if not any(isinstance(r, dict) and r.get("incident_id") == incident_id and r.get("actor") == actor and
               r.get("state") == "acknowledged" for r in rows):
        return "no_own_ack_for_incident"
    state = site_alerts.load_state(repo)
    if state.get("incident_id") == incident_id and state.get("signature"):
        return "problem_still_open"
    return None


def _finish_fail(repo, out, reason, lease_pushed, holder, clock, outcome="rejected", **extra):
    """Fail closed. If our lease is on main, try one release commit; never touch others' locks."""
    released = None
    if lease_pushed:
        released = False
        try:
            fresh_main(repo, True)
            lock = canon_lock.read(repo)
            if canon_lock.is_held(lock, clock()) and lock.get("holder") == holder:
                write_json(repo, LOCK, canon_lock.release(lock, holder, clock()))
                released = commit_push(repo, [LOCK], f"Site alert V2: release unused lease {holder}")
        except (GitError, ValueError, OSError):
            released = False
    return result(False, outcome, reason=reason, receipt="not_saved",
                  lease=("released" if released else "expires_by_itself" if released is False else "not_taken"),
                  **dict(out, **extra))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--repo", required=True, help="dedicated checkout of virudik/ai-film-prompts")
    ap.add_argument("--actor", required=True, choices=("dot", "grok"))
    ap.add_argument("--sender-id", required=True, help="authenticated Relay sender agent ID (from event metadata, never from text)")
    ap.add_argument("--message-id", required=True, help="authenticated Relay message ID")
    ap.add_argument("--event-id")
    ap.add_argument("--run-id")
    ap.add_argument("--message-file", required=True, help="file with the complete message text, or - for stdin")
    ap.add_argument("--allow-test-id", action="append", default=[], help="exact allowlisted test ID from the saved prompt")
    ap.add_argument("--state", default="acknowledged", choices=STATES)
    ap.add_argument("--evidence")
    ap.add_argument("--sync", action="store_true", help="reset the clean dedicated checkout to origin/main")
    a = ap.parse_args(argv)
    text = sys.stdin.read() if a.message_file == "-" else Path(a.message_file).read_text(encoding="utf-8")
    out = handle(a.repo, text, actor=a.actor, authenticated_sender_id=a.sender_id, message_id=a.message_id,
                 event_id=a.event_id, run_id=a.run_id, allowed_test_ids=a.allow_test_id, state=a.state,
                 evidence=a.evidence, sync=a.sync)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") else (3 if out.get("outcome") == "not_site_alert" else 2)


if __name__ == "__main__":
    sys.exit(main())
