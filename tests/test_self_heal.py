import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import self_heal as sh  # noqa: E402

NOW = datetime(2026, 10, 19, 10, 0, tzinfo=timezone.utc)


def ago(minutes, at=None):
    return sh.iso((at or NOW) - timedelta(minutes=minutes))


def healthy(at=None):
    ago_ = lambda m: ago(m, at)  # noqa: E731
    return {"project_status": {"synced_at": ago_(5), "health": "ok", "warnings": []},
            "scan_checked_at": ago_(5), "telemetry_checked_at": ago_(30), "lock": {"state": "free"},
            "runs": {"topview-robot.yml": {"id": 1, "status": "completed", "conclusion": "success", "run_attempt": 1,
                                           "updated_at": ago_(5)}},
            "pages_synced_at": ago_(10), "pages_build_status": "built", "robot_last_decision": "Topview telemetry"}


class SelfHeal(unittest.TestCase):
    def test_healthy_does_nothing_and_writes_nothing_twice(self):
        acts, st, inbox, changed = sh.plan(healthy(), {}, {"tasks": []}, NOW)
        self.assertEqual((acts, st["status"], inbox["tasks"]), ([], "ok", []))
        acts, st2, _, changed2 = sh.plan(healthy(NOW + timedelta(minutes=30)), st, {"tasks": []}, NOW + timedelta(minutes=30))
        self.assertFalse(changed2)
        self.assertEqual(st2["changed_at"], st["changed_at"])

    def test_stale_sync_restarts_once_then_hands_to_agent(self):
        f = healthy()
        # The status publisher intentionally emits an unchanged heartbeat every 180 minutes.
        # A normal 90-minute age must not trigger repair; one missed heartbeat plus grace must.
        f["project_status"]["synced_at"] = ago(90)
        self.assertEqual(sh.detect(f, NOW), {})
        f["project_status"]["synced_at"] = ago(240)
        acts, st, inbox, _ = sh.plan(f, {}, {"tasks": []}, NOW)
        self.assertEqual(acts, [{"kind": "dispatch", "workflow": "sync-from-drive.yml"}])
        self.assertEqual(st["status"], "fixing")
        # next run: still stale, the fix had its cycle -> one task for any agent, no second restart
        later = NOW + timedelta(minutes=30)
        acts, st, inbox, _ = sh.plan(f, st, inbox, later)
        self.assertEqual(acts, [])
        self.assertEqual(st["status"], "escalated")
        t = inbox["tasks"][-1]
        self.assertEqual((t["to"], t["source"], t["heal_key"], t["status"]), ("any", "self-heal", "sync-stale", "open"))
        # third run: no duplicate task
        acts, st, inbox, _ = sh.plan(f, st, inbox, later + timedelta(minutes=30))
        self.assertEqual(len(inbox["tasks"]), 1)
        # resolved -> logged, and the self-heal task closes itself
        when = later + timedelta(minutes=60)
        acts, st, inbox, _ = sh.plan(healthy(when), st, inbox, when)
        self.assertEqual(st["status"], "ok")
        self.assertEqual(st["log"][-1]["kind"], "resolved")
        closed = inbox["tasks"][0]
        self.assertEqual(closed["status"], "done")
        self.assertIn("прошло", closed["result"].lower())
        self.assertEqual(closed["closed_at"], sh.iso(when))
        again = sh.plan(healthy(when + timedelta(minutes=30)), st, inbox, when + timedelta(minutes=30))[2]
        self.assertEqual(again["tasks"][0]["closed_at"], closed["closed_at"])

    def test_resolved_self_heal_closes_only_its_own_task(self):
        inbox = {"tasks": [
            {"id": "self-heal-sync-stale-1", "heal_key": "sync-stale", "source": "self-heal",
             "status": "needs_owner", "text": "diagnose"},
            {"id": "chatgpt-same-key", "heal_key": "sync-stale", "source": "chatgpt",
             "status": "open", "text": "owner work"},
            {"id": "owner-task", "source": "owner", "status": "open", "text": "leave me"},
        ]}
        prev = {"problems": {"sync-stale": {"text": "stale", "since": ago(90)}}, "log": []}
        _, st, inbox, _ = sh.plan(healthy(), prev, inbox, NOW)
        by_id = {t["id"]: t for t in inbox["tasks"]}
        self.assertEqual(by_id["self-heal-sync-stale-1"]["status"], "done")
        self.assertEqual(by_id["chatgpt-same-key"]["status"], "open")
        self.assertEqual(by_id["owner-task"]["status"], "open")
        self.assertNotIn("result", by_id["chatgpt-same-key"])
        # A problem that is still current is not closed, even if an older pass is in the log.
        inbox = {"tasks": [{"id": "still", "heal_key": "sync-stale", "source": "self-heal", "status": "open"}]}
        prev = {"problems": {"sync-stale": {"text": "stale", "since": ago(10)}},
                "log": [{"kind": "resolved", "key": "sync-stale", "text": "Прошло: old"}]}
        facts = healthy()
        facts["project_status"]["synced_at"] = ago(240)
        _, _, inbox, _ = sh.plan(facts, prev, inbox, NOW)
        self.assertEqual(inbox["tasks"][0]["status"], "open")
        self.assertEqual(st["log"][-1]["kind"], "resolved")

    def test_failed_run_reruns_once_and_second_failure_goes_to_agent(self):
        f = healthy()
        f["runs"]["topview-robot.yml"].update(conclusion="failure", html_url="u")
        acts, st, inbox, _ = sh.plan(f, {}, {"tasks": []}, NOW)
        self.assertEqual(acts, [{"kind": "rerun", "run_id": 1}])
        f["runs"]["topview-robot.yml"]["run_attempt"] = 2
        acts, st, inbox, _ = sh.plan(f, {}, {"tasks": []}, NOW)
        self.assertEqual(acts, [])
        self.assertEqual(inbox["tasks"][0]["heal_key"], "run-failed-topview-robot")

    def test_old_failed_run_is_history(self):
        f = healthy()
        f["runs"]["topview-robot.yml"].update(conclusion="failure", updated_at=ago(400))
        self.assertEqual(sh.detect(f, NOW), {})

    def test_robot_on_hold_gets_full_scan(self):
        f = healthy()
        f["telemetry_checked_at"] = ago(180)
        f["robot_last_decision"] = "hold — unmapped_active:e33891d4"
        acts, st, _, _ = sh.plan(f, {}, {"tasks": []}, NOW)
        self.assertEqual(acts[0]["workflow"], "topview-robot.yml")
        self.assertIn("unmapped_active", st["problems"]["telemetry-stale"]["text"])

    def test_pages_lag_and_forgotten_lock(self):
        f = healthy()
        f["pages_synced_at"] = ago(80)
        f["lock"] = {"state": "held", "holder": "x", "expires_at": ago(60)}
        kinds = sorted(a["kind"] for a in sh.plan(f, {}, {"tasks": []}, NOW)[0])
        self.assertEqual(kinds, ["pages_build", "release_lock"])
        f["pages_build_status"] = "building"
        f["lock"]["expires_at"] = ago(5)
        self.assertEqual(sh.detect(f, NOW), {})

    def test_bad_health_restarts_canon_check(self):
        f = healthy()
        f["project_status"].update(health="error", warnings=["instruction_sync_error"])
        acts, st, _, _ = sh.plan(f, {}, {"tasks": []}, NOW)
        self.assertEqual(acts, [{"kind": "dispatch", "workflow": "sync-from-drive.yml"}])

    def test_cli_dry_run_with_facts_changes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "facts.json"
            p.write_text(json.dumps(healthy()), encoding="utf-8")
            r = subprocess.run([sys.executable, str(ROOT / "scripts/self_heal.py"), str(ROOT), "--dry", "--facts", str(p)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn('"status"', r.stdout)

    def test_workflow_and_site_wiring(self):
        wf = (ROOT / ".github/workflows/self-heal.yml").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/self_heal.py .", wf)
        self.assertIn("actions: write", wf)
        sync = (ROOT / ".github/workflows/sync-from-drive.yml").read_text(encoding="utf-8")
        self.assertIn("if: github.event_name != 'push' || github.actor != 'github-actions[bot]'", sync)
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("get('ops/self-heal.json')", html)
        self.assertIn('id="selfHeal"', html)


if __name__ == "__main__":
    unittest.main()
