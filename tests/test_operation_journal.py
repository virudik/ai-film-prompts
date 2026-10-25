import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import operation_journal as oj
import robot_fixture as fx
import robot_master_actions as rma
import robot_telemetry as rt
from test_robot_telemetry import scan, steady, FakeNotifier, T0_PLUS_2H, write_role


class RetentionTests(unittest.TestCase):
    def journal(self):
        return {"retention_max_events": 2, "events": [{"n": 1}, {"n": 1}, {"n": 3}, {"n": 4}],
                "other": {"preserve": True}}

    def test_lossless_including_identical_events_and_metadata(self):
        source = self.journal()
        original = copy.deepcopy(source)
        live, archive = oj.trim(source)
        self.assertEqual(archive["events"] + live["events"], original["events"])
        self.assertEqual(live["archived_event_count"], 2)
        self.assertEqual(live["other"], original["other"])
        self.assertEqual(source, original)
        self.assertIsNone(oj.trim(live, archive))
        live["events"].append({"n": 5})
        live, archive = oj.trim(live, archive)
        self.assertEqual(archive["events"] + live["events"], original["events"] + [{"n": 5}])

    def test_interruption_between_archive_and_live_is_safe_to_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.journal()
            oj.atomic_json(root / oj.JOURNAL, source)
            real = oj.atomic_json
            def fail_live(path, data):
                if Path(path).name == oj.JOURNAL:
                    raise OSError("simulated interrupted live write")
                real(path, data)
            with patch.object(oj, "atomic_json", side_effect=fail_live):
                with self.assertRaises(OSError):
                    oj.write(root, source)
            self.assertEqual(json.loads((root / oj.JOURNAL).read_text()), source)
            oj.write(root, source)
            archive = json.loads((root / oj.ARCHIVE).read_text())
            live = json.loads((root / oj.JOURNAL).read_text())
            self.assertEqual(archive["events"] + live["events"], source["events"])

    def test_failed_atomic_archive_replace_leaves_both_original_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            oj.atomic_json(root / oj.JOURNAL, self.journal())
            with patch.object(oj.os, "replace", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    oj.write(root, self.journal())
            self.assertFalse((root / oj.ARCHIVE).exists())
            self.assertEqual(json.loads((root / oj.JOURNAL).read_text()), self.journal())
            self.assertEqual(list(root.rglob("*.tmp")), [])

    def test_conflicting_or_missing_history_and_bad_limits_fail_closed(self):
        for archive in ({"events": [{"unexpected": 1}]}, {"events": None}):
            with self.assertRaises(ValueError):
                oj.trim(self.journal(), archive)
        with self.assertRaises(ValueError):
            oj.trim(dict(self.journal(), archived_event_count=20))
        for keep in (0, -1, True, "2"):
            with self.assertRaises(ValueError):
                oj.trim(dict(self.journal(), retention_max_events=keep))


class WriterTests(unittest.TestCase):
    def seed(self, work):
        journal = {"retention_max_events": 2, "events": [{"old": 1}, {"old": 2}]}
        oj.atomic_json(work / oj.JOURNAL, journal)
        fx.git(work, "add", oj.JOURNAL)
        fx.git(work, "commit", "-m", "full operation journal")
        fx.git(work, "push", "origin", "main")
        return journal

    def test_telemetry_publishes_archive_with_live_journal_after_rejected_push(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin, work = fx.make_origin(tmp)
            write_role(work)
            (work / "automation-monitor-status.json").write_text(json.dumps({"notification_state": {}}))
            fx.git(work, "add", "-A")
            fx.git(work, "commit", "-m", "robot role")
            source = self.seed(work)
            git = rma.Git(work)
            real_push = git.push
            attempts = []
            def reject_once():
                attempts.append(True)
                return False if len(attempts) == 1 else real_push()
            with patch.object(git, "push", side_effect=reject_once):
                self.assertEqual(rt.run_on(work, scan(steady()), git, now=T0_PLUS_2H,
                                           resolver=None, notifier=FakeNotifier()), 0)
            self.assertEqual(len(attempts), 2)
            live = json.loads(fx.git(origin, "show", "main:" + oj.JOURNAL).stdout)
            archive = json.loads(fx.git(origin, "show", "main:" + oj.ARCHIVE).stdout)
            self.assertEqual((archive["events"] + live["events"])[:2], source["events"])
            self.assertEqual(len(archive["events"] + live["events"]), 3)
            self.assertIn(oj.ARCHIVE, fx.git(origin, "diff-tree", "--no-commit-id", "--name-only", "-r", "main").stdout)

    def test_owner_action_publishes_archive_before_ack(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin, work = fx.make_origin(tmp)
            source = self.seed(work)
            store = fx.FakeStore([fx.row("drop", 30, "tv_drop_task", task_id=fx.ACTIVE_TASK)], origin)
            self.assertEqual(rma.run(work, store, rma.Git(work), mode="on", now=T0_PLUS_2H), 0)
            live = json.loads(fx.git(origin, "show", "main:" + oj.JOURNAL).stdout)
            archive = json.loads(fx.git(origin, "show", "main:" + oj.ARCHIVE).stdout)
            self.assertEqual((archive["events"] + live["events"])[:2], source["events"])
            self.assertEqual(store.status_of("drop"), "applied")
            self.assertEqual(store.log[-1]["origin_head"], fx.git(origin, "rev-parse", "main").stdout.strip())


if __name__ == "__main__":
    unittest.main()
