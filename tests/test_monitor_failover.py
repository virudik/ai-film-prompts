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
            # heartbeat tests model a ChatGPT standby that is allowed to write
            "migration_state": {"chatgpt_writer_eligible": True},
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

    def test_chatgpt_takeover_fails_closed_without_writer_eligibility(self):
        role = json.loads((self.repo / "monitor-role.json").read_text(encoding="utf-8"))
        role.pop("migration_state")
        write_json(self.repo / "monitor-role.json", role)
        write_json(self.repo / "automation-monitor-status.json", {
            "last_successful_by_runner": {"claude": timestamp(400)},
            "last_successful_cycle_at": timestamp(400),
        })
        result = self.role_action()
        self.assertEqual(result["action"], "skip")
        self.assertIn("read-only", result["reason"])

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

    def test_legacy_verified_success_survives_degraded_followup(self):
        # Upgrade path: old monitor snapshots have last_successful_cycle_at
        # but did not yet populate last_successful_by_runner.
        write_json(self.repo / "automation-monitor-status.json", {
            "last_scheduled_cycle": {
                "completed_at": timestamp(5), "health": "degraded",
                "phases_missing": ["master_slow_edit"], "runner": "claude_scheduled_task",
            },
            "last_completed_by_runner": {"claude": timestamp(5)},
            "last_successful_cycle_at": timestamp(45),
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



    def test_chatgpt_success_is_not_misattributed_to_claude(self):
        old_claude = timestamp(190)
        finished = timestamp(1)
        write_json(self.repo / "automation-monitor-status.json", {
            "last_successful_by_runner": {"claude": old_claude},
            "last_completed_by_runner": {"claude": old_claude},
        })
        subprocess.run([sys.executable, str(STATUS_SCRIPT), str(self.repo),
                        "--runner", "chatgpt", "--started", timestamp(2),
                        "--completed", finished, "--health", "ok",
                        "--phase", "topview", "--phase", "github_publication"],
                       check=True, text=True, capture_output=True)
        d = json.loads((self.repo / "automation-monitor-status.json").read_text())
        self.assertEqual(d["last_scheduled_cycle"]["runner"], "chatgpt_scheduled_task")
        self.assertEqual(d["last_successful_by_runner"]["chatgpt"], finished)
        self.assertEqual(d["last_successful_by_runner"]["claude"], old_claude)
        self.assertEqual(d["last_completed_by_runner"]["chatgpt"], finished)

    def test_chatgpt_degraded_cannot_become_fake_success(self):
        old = timestamp(210)
        write_json(self.repo / "automation-monitor-status.json", {
            "last_successful_by_runner": {"chatgpt": old},
            "last_successful_cycle_at": old,
        })
        subprocess.run([sys.executable, str(STATUS_SCRIPT), str(self.repo),
                        "--runner", "chatgpt", "--started", timestamp(2),
                        "--completed", timestamp(1), "--health", "degraded",
                        "--missing", "topview_direct_read"],
                       check=True, text=True, capture_output=True)
        d = json.loads((self.repo / "automation-monitor-status.json").read_text())
        self.assertEqual(d["last_scheduled_cycle"]["runner"], "chatgpt_scheduled_task")
        self.assertEqual(d["last_successful_by_runner"]["chatgpt"], old)
        self.assertEqual(d["last_successful_cycle_at"], old)
        self.assertEqual(d["health"], "degraded")

class RobotRoleTest(MonitorHeartbeatTest):
    """The GitHub robot is a third named writer: it runs only as primary and never takes over by silence;
    the AI standby takes over only after 180 minutes without a VERIFIED healthy robot cycle."""

    def set_roles(self, primary, standby):
        role = json.loads((self.repo / "monitor-role.json").read_text(encoding="utf-8"))
        role.update(primary=primary, standby=standby)
        role["monitors"]["robot"] = {"commit_author": "github-actions[bot]"}
        write_json(self.repo / "monitor-role.json", role)

    def action(self, me):
        r = subprocess.run([sys.executable, str(ROLE_SCRIPT), str(self.repo), "--me", me, "--dry-run"],
                           text=True, capture_output=True, check=True)
        return json.loads(r.stdout)

    def test_robot_runs_only_while_it_is_primary(self):
        write_json(self.repo / "automation-monitor-status.json", {"last_scheduled_cycle": {}})
        self.assertEqual(self.action("robot")["action"], "skip")          # primary is claude → robot stays silent
        self.set_roles("robot", "chatgpt")
        self.assertEqual(self.action("robot")["action"], "run")

    def test_standby_takes_over_after_180_minutes_of_robot_silence_only_if_healthy_clock_is_old(self):
        self.set_roles("robot", "chatgpt")
        write_json(self.repo / "automation-monitor-status.json", {
            "last_scheduled_cycle": {"completed_at": timestamp(5), "health": "degraded",
                                     "phases_missing": ["telemetry_publish"], "runner": "robot_scheduled_task"},
            "last_successful_by_runner": {"robot": timestamp(200)}})
        res = self.action("chatgpt")
        self.assertEqual(res["action"], "failover")                       # a recent DEGRADED robot hold is no proof of life
        write_json(self.repo / "automation-monitor-status.json", {
            "last_scheduled_cycle": {"completed_at": timestamp(5), "health": "ok", "phases_missing": [],
                                     "runner": "robot_scheduled_task"},
            "last_successful_by_runner": {"robot": timestamp(5)}})
        self.assertEqual(self.action("chatgpt")["action"], "skip")        # healthy robot cycle → standby yields

    def test_status_script_records_robot_cycle(self):
        write_json(self.repo / "automation-monitor-status.json", {})
        subprocess.run([sys.executable, str(STATUS_SCRIPT), str(self.repo), "--started", timestamp(1),
                        "--completed", timestamp(0), "--runner", "robot", "--health", "ok"], check=True, capture_output=True)
        d = json.loads((self.repo / "automation-monitor-status.json").read_text(encoding="utf-8"))
        self.assertEqual(d["last_scheduled_cycle"]["runner"], "robot_scheduled_task")
        self.assertIn("robot", d["last_successful_by_runner"])

    def commit_other_files(self, files):
        for name in files:
            (self.repo / name).write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "add", "--", *files], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-q", "--author",
                        "virudik <fixture@example.invalid>", "-m", "other work"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "update-ref",
                        "refs/remotes/origin/main", "HEAD"], check=True)

    def test_creative_and_derived_commits_do_not_silence_primary_robot(self):
        self.set_roles("robot", "chatgpt")
        write_json(self.repo / "automation-monitor-status.json", {})
        self.commit_other_files(["video-prompts.md", "review-ledger.json",
                                 "project-status.json", "SYNC-TRIGGER.txt"])
        self.assertEqual(self.action("robot")["action"], "run")

    def test_actual_telemetry_commit_still_blocks_primary_robot(self):
        self.set_roles("robot", "chatgpt")
        write_json(self.repo / "automation-monitor-status.json", {})
        self.commit_other_files(["topview-status.json", "video-prompts.md"])
        result = self.action("robot")
        self.assertEqual(result["action"], "skip")
        self.assertIn("other monitor", result["reason"])

    def test_unavailable_git_history_still_fails_closed(self):
        self.set_roles("robot", "chatgpt")
        write_json(self.repo / "automation-monitor-status.json", {})
        subprocess.run(["git", "-C", str(self.repo), "update-ref", "-d",
                        "refs/remotes/origin/main"], check=True)
        self.assertEqual(self.action("robot")["action"], "skip")


if __name__ == "__main__":
    unittest.main()
