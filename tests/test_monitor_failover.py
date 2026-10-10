#!/usr/bin/env python3
"""Offline regression tests for healthy-heartbeat-only AI Film failover.

No network, no production writes, no Topview tasks, no real scheduler actions.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLE_SCRIPT = ROOT / "scripts" / "monitor_role.py"
STATUS_SCRIPT = ROOT / "scripts" / "monitor_status.py"


def timestamp(minutes_ago=0):
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class MonitorHeartbeatTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "test-fixture"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "fixture@example.invalid"], check=True)
        (self.repo / "seed.txt").write_text("fixture\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "seed.txt"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-q", "-m", "fixture"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "branch", "-M", "main"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "update-ref", "refs/remotes/origin/main", "HEAD"], check=True)
        write_json(self.repo / "monitor-role.json", {
            "primary": "claude",
            "standby": "chatgpt",
            "set_at": timestamp(300),
            "failover_after_minutes": 180,
            "collision_guard_minutes": 50,
            "standby_yield_minutes": 0,
            "monitors": {
                "claude": {"commit_author": "Claude"},
                "chatgpt": {"commit_author": "virudik"},
            },
        })

    def role_action(self):
        r = subprocess.run([sys.executable, str(ROLE_SCRIPT), str(self.repo),
                            "--me", "chatgpt", "--dry-run"],
                           text=True, capture_output=True, check=True)
        return json.loads(r.stdout)

    def test_recent_degraded_completion_does_not_prevent_takeover(self):
        write_json(self.repo / "automation-monitor-status.json", {
            "last_scheduled_cycle": {
                "completed_at": timestamp(5), "health": "degraded",
                "phases_missing": ["master_slow_edit"], "runner": "claude_scheduled_task",
            },
            "last_completed_by_runner": {"claude": timestamp(5)},
            "last_successful_by_runner": {"claude": timestamp(210)},
            "last_successful_cycle_at": timestamp(210),
        })
        result = self.role_action()
        self.assertEqual(result["action"], "failover")
        self.assertTrue(result["primary_age_minutes"] > 180)

    def test_recent_healthy_cycle_blocks_takeover(self):
        write_json(self.repo / "automation-monitor-status.json", {
            "last_scheduled_cycle": {
                "completed_at": timestamp(60), "health": "ok",
                "phases_missing": [], "runner": "claude_scheduled_task",
            },
            "last_completed_by_runner": {"claude": timestamp(60)},
            "last_successful_by_runner": {"claude": timestamp(60)},
        })
        self.assertEqual(self.role_action()["action"], "skip")

    def test_degraded_cycle_does_not_overwrite_success_time(self):
        original = timestamp(230)
        write_json(self.repo / "automation-monitor-status.json", {
            "last_successful_cycle_at": original,
            "last_successful_by_runner": {"claude": original},
        })
        r = subprocess.run([
            sys.executable, str(STATUS_SCRIPT), str(self.repo),
            "--started", timestamp(2), "--completed", timestamp(1),
            "--health", "degraded", "--phase", "topview_scan",
            "--missing", "master_slow_edit",
        ], text=True, capture_output=True, check=True)
        self.assertIn("degraded", r.stdout)
        status = json.loads((self.repo / "automation-monitor-status.json").read_text())
        self.assertEqual(status["last_successful_by_runner"]["claude"], original)
        self.assertEqual(status["last_successful_cycle_at"], original)
        self.assertEqual(status["last_scheduled_cycle"]["health"], "degraded")

    def test_complete_success_updates_healthy_clock(self):
        write_json(self.repo / "automation-monitor-status.json", {})
        finished = timestamp(1)
        subprocess.run([
            sys.executable, str(STATUS_SCRIPT), str(self.repo),
            "--started", timestamp(2), "--completed", finished,
            "--health", "ok", "--phase", "topview_scan",
        ], text=True, capture_output=True, check=True)
        status = json.loads((self.repo / "automation-monitor-status.json").read_text())
        self.assertEqual(status["last_successful_by_runner"]["claude"], finished)
        self.assertEqual(status["last_successful_cycle_at"], finished)


if __name__ == "__main__":
    unittest.main()
