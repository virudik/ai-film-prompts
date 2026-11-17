"""Receiving handler for SITE_ALERT_V2/TEST: lease, CAS, readback, fail-closed.

All transport is local: a temporary bare git repository plays origin/main and
messages are produced by the real site_alerts / site_alert_canary builders with an
in-memory sender. No Relay, GitHub or Topview call is made.
"""
import json
import os
import subprocess
import tempfile
import unittest
from unittest import mock
from datetime import timedelta
from pathlib import Path

from test_site_alerts import NOW, write
import canon_lock
import site_alert_canary
import site_alert_handler as handler
import site_alerts

ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example", GIT_COMMITTER_NAME="t",
           GIT_COMMITTER_EMAIL="t@example")


def sh(cwd, *args):
    proc = subprocess.run(["git", *args], cwd=cwd, env=ENV, text=True, capture_output=True)
    if proc.returncode != 0:
        raise AssertionError(proc.stderr)
    return proc.stdout.strip()


class HandlerTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {k: v for k, v in ENV.items() if k.startswith("GIT_")})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.origin = base / "origin.git"
        sh(base, "init", "--quiet", "--bare", "-b", "main", str(self.origin))
        self.seed = base / "seed"
        sh(base, "clone", "--quiet", str(self.origin), str(self.seed))
        sh(self.seed, "checkout", "--quiet", "-b", "main")
        self.repo = base / "grok"
        self.fixture(primary="dot", backup="grok", enabled=True)
        sh(base, "clone", "--quiet", str(self.origin), str(self.repo))

    # --- fixture helpers -------------------------------------------------
    def fixture(self, *, primary, backup, enabled, explicit=True):
        r = self.seed
        checked = (NOW - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        write(r, "topview-status.json", {"checked_at": checked})
        write(r, "automation-monitor-status.json", {"last_scheduled_cycle": {"completed_at": checked, "health": "ok"}})
        write(r, "project-status.json", {"health": "ok"})
        write(r, "instruction-sync-status.json", {"health": "ok"})
        write(r, "canon-health.json", {"problems": [{"level": "error", "code": "broken-ref", "text": "broken"}]})
        cfg = {"enabled": True, "sender_agent_id": "robot-test", "site_alert_enabled": True,
               "site_alert_address": "GrokBot@example",
               "site_alert_routing": {"enabled": enabled, "mode": "primary_then_backup",
                                      "critical_timeout_minutes": 120, "warning_timeout_minutes": 120,
                                      "primary_address": "chatgpt@example", "backup_address": "GrokBot@example"}}
        if explicit:
            cfg["wake_roles"] = {"primary_actor": primary, "backup_actor": backup}
        write(r, "ops/relay-wake.json", cfg)
        write(r, "ops/canon-lock.json", {"schema_version": 1, "state": "free", "holder": None, "expires_at": None})
        self.push_seed("fixture")

    def push_seed(self, msg):
        sh(self.seed, "add", "-A")
        sh(self.seed, "commit", "--quiet", "--allow-empty", "-m", msg)
        sh(self.seed, "push", "--quiet", "origin", "HEAD:main")

    def pull_seed(self):
        sh(self.seed, "fetch", "--quiet", "origin")
        sh(self.seed, "reset", "--quiet", "--hard", "origin/main")

    def publish(self, when=NOW):
        """Robot side: prepare+CAS publish, then build the exact message (fake transport)."""
        self.pull_seed()
        site_alerts.notify(self.seed, when, prepare_only=True)
        self.push_seed("prepare")
        sent = []
        site_alerts.notify(self.seed, when, lambda text, **kw: (sent.append(text), ("sent", "m"))[1],
                           require_prepared=True)
        self.push_seed("receipt")
        return sent[-1]

    def run_handler(self, text, actor="grok", message_id="msg-1", when=NOW, **kw):
        options = dict(actor=actor, authenticated_sender_id="robot-test", message_id=message_id,
                       event_id="evt-1", sync=True, now=when)
        options.update(kw)
        return handler.handle(self.repo, text, **options)

    def origin_json(self, rel):
        self.pull_seed()
        p = self.seed / rel
        return json.loads(p.read_text()) if p.exists() else None

    def origin_head(self):
        return sh(self.seed, "ls-remote", str(self.origin), "main").split()[0]

    # --- production ------------------------------------------------------
    def test_grok_backup_acks_with_lease_cas_and_readback(self):
        self.publish()
        later = NOW + timedelta(minutes=121)
        stamp = later.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.pull_seed()
        write(self.seed, "topview-status.json", {"checked_at": stamp})
        write(self.seed, "automation-monitor-status.json", {"last_scheduled_cycle": {"completed_at": stamp, "health": "ok"}})
        self.push_seed("fresh status")
        text = self.publish(later)
        self.assertIn("recipient_role=backup", text)
        self.assertEqual(self.run_handler(text, actor="dot", when=later)["reason"], "wrong_current_recipient")
        out = self.run_handler(text, when=later)
        self.assertTrue(out["ok"], out)
        self.assertEqual((out["outcome"], out["role"], out["receipt"], out["lease"]),
                         ("acknowledged", "backup", "saved", "released"))
        self.assertEqual(out["topview"], "not_called")
        rows = self.origin_json(site_alerts.RECEIPTS)["events"]
        self.assertEqual([(r["actor"], r["role"], r["state"], r["message_id"]) for r in rows],
                         [("grok", "backup", "acknowledged", "msg-1")])
        lock = self.origin_json(canon_lock.LOCK)
        self.assertEqual(lock["state"], "free")
        self.assertTrue(rows[0]["holder"].startswith("grok:"))
        log = sh(self.seed, "log", "--format=%s", "-3")
        self.assertIn("lease for receipt", log)
        self.assertIn("lease released", log)
        # Backup ACK is recorded but does not extend the primary (Dot) timer.
        state = site_alerts.load_state(self.seed)
        self.assertEqual(site_alerts.progress_at(self.seed, state, later), state["first_seen_at"])

    def test_grok_primary_ack_counts_as_primary_progress(self):
        self.fixture(primary="grok", backup="dot", enabled=True)
        text = self.publish()
        self.assertIn("recipient_actor=grok", text)
        self.assertIn("recipient_role=primary", text)
        self.assertEqual(self.run_handler(text, actor="dot")["reason"], "wrong_current_recipient")
        out = self.run_handler(text, when=NOW + timedelta(minutes=5))
        self.assertTrue(out["ok"], out)
        self.assertEqual(out["role"], "primary")
        self.pull_seed()
        state = site_alerts.load_state(self.seed)
        self.assertEqual(site_alerts.progress_at(self.seed, state, NOW + timedelta(minutes=6)),
                         (NOW + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ"))
        # Progress update by the same actor needs evidence, and is recorded once.
        self.assertEqual(self.run_handler(text, state="in_progress", when=NOW + timedelta(minutes=7))["reason"],
                         "evidence_required")
        prog = self.run_handler(text, state="in_progress", evidence="проверил broken-ref", when=NOW + timedelta(minutes=7))
        self.assertTrue(prog["ok"], prog)
        dup = self.run_handler(text, state="in_progress", evidence="x", when=NOW + timedelta(minutes=8))
        self.assertEqual((dup["outcome"], dup["reason"]), ("duplicate", "duplicate_message"))

    def test_wrong_sender_is_rejected_without_writes(self):
        text = self.publish()
        before = self.origin_head()
        for sender in ("fake", "chatgpt@cloud-239644772681871360", None):
            out = self.run_handler(text, actor="dot", authenticated_sender_id=sender)
            self.assertEqual((out["ok"], out["reason"], out["terminal"]), (False, "wrong_authenticated_sender", True))
        self.assertEqual(self.origin_head(), before)

    def test_role_mismatch_after_switch_is_rejected(self):
        text = self.publish()  # Dot primary
        self.pull_seed()
        cfg = json.loads((self.seed / "ops/relay-wake.json").read_text())
        cfg["wake_roles"] = {"primary_actor": "grok", "backup_actor": "dot"}
        write(self.seed, "ops/relay-wake.json", cfg)
        self.push_seed("switch roles")
        for actor in ("dot", "grok"):
            out = self.run_handler(text, actor=actor)
            self.assertFalse(out["ok"])
            self.assertIn(out["reason"], ("wrong_current_recipient", "stale_roles"))

    def test_stale_incident_and_resolved_problem_are_rejected(self):
        text = self.publish()
        forged = text.replace("SITE_ALERT_V2 site:", "SITE_ALERT_V2 old:", 1)
        self.assertEqual(self.run_handler(forged, actor="dot")["reason"], "stale_incident")
        self.pull_seed()
        write(self.seed, "canon-health.json", {"problems": []})
        self.push_seed("fixed")
        self.assertEqual(self.run_handler(text, actor="dot")["reason"], "problem_changed_or_resolved")
        self.assertIsNone(self.origin_json(site_alerts.RECEIPTS))

    def test_duplicate_ack_is_not_written_twice(self):
        text = self.publish()
        first = self.run_handler(text, actor="dot")
        self.assertTrue(first["ok"], first)
        head = self.origin_head()
        same = self.run_handler(text, actor="dot")
        self.assertEqual((same["outcome"], same["reason"], same["lease"]), ("duplicate", "duplicate_message", "not_taken"))
        other = self.run_handler(text, actor="dot", message_id="msg-2")
        self.assertEqual(other["reason"], "already_acknowledged")
        self.assertEqual(self.origin_head(), head)

    def test_foreign_lease_blocks_without_false_ack(self):
        text = self.publish()
        self.pull_seed()
        write(self.seed, "ops/canon-lock.json", {"schema_version": 1, "state": "held", "holder": "chatgpt:work:abc",
                                                 "expires_at": (NOW + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%SZ")})
        self.push_seed("foreign lock")
        out = self.run_handler(text, actor="dot")
        self.assertEqual((out["reason"], out["receipt"], out["lock_holder"]), ("blocked_lock", "not_saved", "chatgpt:work:abc"))
        self.assertIsNone(self.origin_json(site_alerts.RECEIPTS))

    def test_cas_rejection_rereads_main_and_retries(self):
        text = self.publish()
        hit = []

        def race():
            if not hit:
                hit.append(1)
                self.pull_seed()
                (self.seed / "unrelated.txt").write_text("concurrent")
                self.push_seed("concurrent unrelated commit")

        out = self.run_handler(text, actor="dot", hooks={"before_receipt_push": race})
        self.assertTrue(out["ok"], out)
        self.assertGreater(out["attempts"], 2)
        self.assertTrue((self.seed / "unrelated.txt").exists())
        self.assertEqual(len(self.origin_json(site_alerts.RECEIPTS)["events"]), 1)
        self.assertEqual(self.origin_json(canon_lock.LOCK)["state"], "free")

    def test_lease_stolen_between_steps_fails_closed(self):
        text = self.publish()

        def steal():
            self.pull_seed()
            write(self.seed, "ops/canon-lock.json", {"schema_version": 1, "state": "held", "holder": "chatgpt:work:x",
                                                     "expires_at": (NOW + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%SZ")})
            self.push_seed("other writer")

        out = self.run_handler(text, actor="dot", hooks={"after_lease": steal})
        self.assertEqual((out["ok"], out["reason"]), (False, "lease_readback_failed"))
        self.assertIsNone(self.origin_json(site_alerts.RECEIPTS))
        self.assertEqual(self.origin_json(canon_lock.LOCK)["holder"], "chatgpt:work:x")

    def test_production_is_rejected_while_v2_disabled(self):
        text = self.publish()
        self.pull_seed()
        cfg = json.loads((self.seed / "ops/relay-wake.json").read_text())
        cfg["site_alert_routing"]["enabled"] = False
        write(self.seed, "ops/relay-wake.json", cfg)
        self.push_seed("disable")
        out = self.run_handler(text, actor="dot")
        self.assertEqual((out["ok"], out["reason"]), (False, "production_disabled_or_wrong_marker"))

    def test_resolved_requires_own_ack_and_closed_incident(self):
        text = self.publish()
        self.assertEqual(self.run_handler(text, actor="dot", state="resolved", evidence="fixed")["reason"],
                         "no_own_ack_for_incident")
        self.assertTrue(self.run_handler(text, actor="dot")["ok"])
        self.assertEqual(self.run_handler(text, actor="dot", state="resolved", evidence="fixed")["reason"],
                         "problem_still_open")
        self.pull_seed()
        write(self.seed, "canon-health.json", {"problems": []})
        site_alerts.notify(self.seed, NOW, lambda *a, **k: ("sent", "m"))
        self.push_seed("cleared")
        out = self.run_handler(text, actor="dot", state="resolved", evidence="broken-ref исправлен")
        self.assertTrue(out["ok"], out)

    # --- canary ----------------------------------------------------------
    def canary(self, test_id, recipient):
        sent = []
        status, _ = site_alert_canary.send(self.seed, test_id, recipient, True,
                                           lambda root, text, **kw: (sent.append(text), ("sent", "m"))[1])
        self.assertEqual(status, "sent")
        return sent[0]

    def test_canary_both_roles_read_only_exact_allowlist(self):
        for primary, backup, role in (("dot", "grok", "backup"), ("grok", "dot", "primary")):
            with self.subTest(primary=primary):
                self.fixture(primary=primary, backup=backup, enabled=False)
                self.pull_seed()
                text = self.canary("site-test-grok-01", "grok")
                head = self.origin_head()
                out = self.run_handler(text, allowed_test_ids=["site-test-grok-01"], run_id=None)
                self.assertTrue(out["ok"], out)
                self.assertEqual((out["outcome"], out["role"], out["writes"], out["test_id"]),
                                 ("test_received", role, "none", "site-test-grok-01"))
                self.assertEqual(out["main_sha"], head)
                self.assertEqual(self.origin_head(), head)
                self.assertEqual(sh(self.repo, "status", "--porcelain"), "")

    def test_unknown_test_id_and_empty_allowlist_are_rejected(self):
        self.fixture(primary="dot", backup="grok", enabled=False)
        text = self.canary("site-test-grok-01", "grok")
        for allowed in ([], ["site-test-grok-02"], ["site-test-grok-0"]):
            out = self.run_handler(text, allowed_test_ids=allowed)
            self.assertEqual((out["ok"], out["reason"], out["terminal"]), (False, "test_not_authorized", True))
        self.assertEqual(self.run_handler(text, allowed_test_ids=["site-test-grok-01"], state="in_progress")["reason"],
                         "test_is_read_only")
        self.assertEqual(self.run_handler(text, actor="dot", allowed_test_ids=["site-test-grok-01"])["reason"],
                         "wrong_current_recipient")

    def test_canary_rejected_once_v2_enabled(self):
        self.fixture(primary="dot", backup="grok", enabled=False)
        text = self.canary("site-test-grok-01", "grok")
        self.fixture(primary="dot", backup="grok", enabled=True)
        self.assertEqual(self.run_handler(text, allowed_test_ids=["site-test-grok-01"])["reason"], "test_not_authorized")

    # --- framing ---------------------------------------------------------
    def test_non_site_message_is_not_terminal_and_unknown_marker_is(self):
        self.assertEqual(handler.handle(self.repo, "TOPVIEW_SLOT_WAKE_V2 x", actor="grok", authenticated_sender_id="robot-test",
                                        message_id="m"), {"ok": False, "outcome": "not_site_alert", "terminal": False})
        out = self.run_handler("SITE_ALERT_V3 x")
        self.assertEqual((out["reason"], out["terminal"], out["topview"]), ("unknown_site_marker", True, "not_called"))
        self.assertEqual(self.run_handler("SITE_ALERT_V2 x", message_id="")["reason"], "missing_authenticated_message_id")

    def test_stale_checkout_without_sync_is_rejected(self):
        text = self.publish()
        out = self.run_handler(text, actor="dot", sync=False)
        self.assertEqual(out["reason"], "not_fresh_main")
        (self.repo / "dirty.txt").write_text("x")
        self.assertEqual(self.run_handler(text, actor="dot")["reason"], "dirty_checkout")


if __name__ == "__main__":
    unittest.main()
