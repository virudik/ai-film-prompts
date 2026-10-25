"""Receipt compaction must preserve evidence, duplicate protection and robot acknowledgements."""
import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import trim_service_files as trim
import robot_telemetry as robot

NOW = datetime(2026, 10, 26, 10, tzinfo=timezone.utc)


def receipt(event_id, age=1, **fields):
    return dict(event_id=event_id, checked_at=(NOW - timedelta(days=age)).isoformat(),
                outcome="no_update", retryable=False, task_ids=[], **fields)


def save(root, name, data):
    path = Path(root) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


class RelayRetentionTests(unittest.TestCase):
    def test_age_boundary_preserves_complete_records_and_unrelated_evidence(self):
        old = receipt("result:old", 31, details={"reason": "Проверено", "receipts": [1, 2]})
        data = {"events": [old, receipt("slots:boundary:1", 30), receipt("slots:new:1", 1)],
                "robot_relay": {"test_acks": [{"test_id": "original", "run_id": None}]},
                "custom": ["preserve"], "archived_event_ids": ["result:previous"]}
        snapshot = copy.deepcopy(data)
        live, archive, count = trim.trim_relay_events(data, None, NOW)
        self.assertEqual(count, 1)
        self.assertEqual(archive["events"], [old])
        self.assertEqual([e["event_id"] for e in live["events"]], ["slots:boundary:1", "slots:new:1"])
        self.assertEqual(live["archived_event_ids"], ["result:old", "result:previous"])
        self.assertEqual(live["robot_relay"], data["robot_relay"])
        self.assertEqual(live["custom"], data["custom"])
        self.assertEqual(data, snapshot)
        self.assertIsNone(trim.trim_relay_events(live, archive, NOW))

    def test_count_limit_keeps_newest_100_even_if_input_is_unsorted(self):
        events = [dict(receipt(f"slots:episode:{i}"), checked_at=(NOW - timedelta(minutes=i)).isoformat())
                  for i in range(105)]
        data = {"events": list(reversed(events))}
        live, archive, count = trim.trim_relay_events(data, None, NOW)
        self.assertEqual(count, 5)
        self.assertEqual(len(live["events"]), 100)
        self.assertEqual({e["event_id"] for e in live["events"]}, {e["event_id"] for e in events[:100]})
        self.assertEqual(len(live["archived_event_ids"]), 5)
        self.assertEqual(len(live["events"]) + len(archive["events"]), len(events))

    def test_unresolved_unknown_missing_and_future_dates_are_never_trimmed(self):
        protected = [dict(receipt("blocked", 90), outcome="blocked_browser"),
                     dict(receipt("unknown", 90), outcome="submission_unknown"),
                     dict(receipt("running", 90), outcome="in_progress"),
                     dict(receipt("retry", 90), retryable=True),
                     {"event_id": "legacy", "outcome": "no_update", "checked_at": "2020-01-01Z"},
                     dict(receipt("bad-date", 90), checked_at="bad"),
                     dict(receipt("future"), checked_at=(NOW + timedelta(days=1)).isoformat()),
                     dict(receipt("missing-date"), checked_at=None),
                     dict(receipt("bad-outcome", 90), outcome=[]),
                     {"event_id": "unknown-shape"}, "legacy text"]
        data = {"events": protected + [receipt("done", 90)]}
        live, archive, count = trim.trim_relay_events(data, None, NOW, keep=0)
        self.assertEqual(live["events"], protected)
        self.assertEqual(live["archived_event_ids"], ["done"])
        self.assertEqual(count, 1)

    def test_an_unresolved_attempt_protects_all_versions_of_the_same_id(self):
        data = {"events": [receipt("same", 90), dict(receipt("same", 90), retryable=True)]}
        self.assertIsNone(trim.trim_relay_events(data, None, NOW, keep=0))

    def test_retry_after_archive_write_deduplicates_only_identical_records(self):
        event = receipt("result:old", 90)
        previous_version = dict(event, reason="previous factual observation")
        archive = {"schema_version": 1, "events": [event, previous_version], "extra": "keep"}
        live, updated, count = trim.trim_relay_events({"events": [event]}, archive, NOW)
        self.assertEqual(updated, archive)
        self.assertEqual(live["archived_event_ids"], [event["event_id"]])
        self.assertEqual(count, 1)

    def test_corrupt_shapes_refuse_to_replace_evidence(self):
        with self.assertRaises(ValueError):
            trim.trim_relay_events({"events": "not a list"}, None, NOW)
        with self.assertRaises(ValueError):
            trim.trim_relay_events({"events": [], "archived_event_ids": "not a list"}, None, NOW)
        with self.assertRaises(ValueError):
            trim.trim_relay_events({"events": [receipt("old", 90)]}, {"events": "corrupt"}, NOW)

    def test_relay_only_dry_run_and_write_are_lossless_and_idempotent(self):
        with tempfile.TemporaryDirectory() as root:
            event = receipt("slots:episode:3", 90)
            p = save(root, trim.RELAY_REPORT, {"events": [event], "robot_relay": {"test_acks": [1]}})
            queue = save(root, trim.QUEUE, {"items": [{"id": "cancelled", "state": "cancelled"}]})
            checkpoint = Path(root) / trim.CHECKPOINT
            checkpoint.write_text("".join(f"# {i}\nold\n" for i in range(20)))
            before = {f: f.read_bytes() for f in [p, queue, checkpoint]}
            self.assertEqual(len(trim.run(root, now=NOW, relay_only=True)), 1)
            self.assertEqual({f: f.read_bytes() for f in before}, before)
            self.assertFalse((Path(root) / trim.RELAY_ARCHIVE).exists())
            self.assertEqual(len(trim.run(root, write=True, now=NOW, relay_only=True)), 1)
            self.assertTrue(robot.handler_acked(root, event["event_id"]))
            self.assertEqual(json.loads((Path(root) / trim.RELAY_ARCHIVE).read_text())["events"], [event])
            self.assertEqual(queue.read_bytes(), before[queue])
            self.assertEqual(checkpoint.read_bytes(), before[checkpoint])
            saved = p.read_bytes()
            self.assertEqual(trim.run(root, write=True, now=NOW, relay_only=True), [])
            self.assertEqual(p.read_bytes(), saved)

    def test_normal_weekly_cleanup_also_trims_relay(self):
        with tempfile.TemporaryDirectory() as root:
            save(root, trim.RELAY_REPORT, {"events": [receipt("result:old", 31)]})
            self.assertEqual(len(trim.run(root, write=True, now=NOW)), 1)
            self.assertTrue(robot.handler_acked(root, "result:old"))

    def test_failed_archive_write_does_not_remove_live_receipts(self):
        with tempfile.TemporaryDirectory() as root:
            p = save(root, trim.RELAY_REPORT, {"events": [receipt("result:old", 31)]})
            before = p.read_bytes()
            with patch.object(trim, "dump_relay_json", side_effect=OSError("disk full")) as dump:
                with self.assertRaises(OSError):
                    trim.run(root, write=True, now=NOW, relay_only=True)
            self.assertEqual(dump.call_args.args[0], Path(root) / trim.RELAY_ARCHIVE)
            self.assertEqual(p.read_bytes(), before)

    def test_atomic_replace_failure_preserves_existing_archive(self):
        with tempfile.TemporaryDirectory() as root:
            p = save(root, trim.RELAY_REPORT, {"events": [receipt("new-old", 31)]})
            archive = save(root, trim.RELAY_ARCHIVE, {"events": [receipt("previous-old", 60)]})
            before = {f: f.read_bytes() for f in (p, archive)}
            with patch.object(trim.os, "replace", side_effect=OSError("replace failed")):
                with self.assertRaises(OSError):
                    trim.run(root, write=True, now=NOW, relay_only=True)
            self.assertEqual({f: f.read_bytes() for f in before}, before)
            self.assertEqual(list(archive.parent.glob("*.tmp")), [])

    def test_failure_between_archive_and_live_write_is_safe_to_retry(self):
        with tempfile.TemporaryDirectory() as root:
            event = receipt("old", 31)
            p = save(root, trim.RELAY_REPORT, {"events": [event]})
            before = p.read_bytes()
            real_write = trim.dump_relay_json
            def fail_live(path, data):
                if path == p:
                    raise OSError("interrupted before replacing live file")
                real_write(path, data)
            with patch.object(trim, "dump_relay_json", side_effect=fail_live):
                with self.assertRaises(OSError):
                    trim.run(root, write=True, now=NOW, relay_only=True)
            self.assertEqual(p.read_bytes(), before)
            trim.run(root, write=True, now=NOW, relay_only=True)
            self.assertEqual(json.loads((Path(root) / trim.RELAY_ARCHIVE).read_text())["events"], [event])
            self.assertTrue(robot.handler_acked(root, "old"))

    def test_nothing_to_trim_never_reads_the_archive(self):
        with tempfile.TemporaryDirectory() as root:
            save(root, trim.RELAY_REPORT, {"events": [receipt("fresh")]})
            archive = Path(root) / trim.RELAY_ARCHIVE
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_text("not JSON: must not be loaded on an ordinary cycle")
            self.assertEqual(trim.run(root, write=True, now=NOW, relay_only=True), [])


class ExactRobotAckTests(unittest.TestCase):
    def test_live_and_archived_receipts_but_not_substrings_or_other_fields(self):
        with tempfile.TemporaryDirectory() as root:
            save(root, trim.RELAY_REPORT, {"events": [{"event_id": "result:abcdef"}],
                 "archived_event_ids": ["slots:episode:10"], "note": "result:abc slots:episode:1"})
            self.assertTrue(robot.handler_acked(root, "result:abcdef"))
            self.assertTrue(robot.handler_acked(root, "slots:episode:10"))
            self.assertFalse(robot.handler_acked(root, "result:abc"))
            self.assertFalse(robot.handler_acked(root, "slots:episode:1"))
            self.assertFalse(robot.handler_acked(root, ""))
            self.assertFalse(robot.handler_acked(root, None))

    def test_missing_corrupt_and_wrong_schema_are_not_acknowledgements(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertFalse(robot.handler_acked(root, "x"))
            p = save(root, trim.RELAY_REPORT, [])
            self.assertFalse(robot.handler_acked(root, "x"))
            save(root, trim.RELAY_REPORT, {"events": "x", "archived_event_ids": "x"})
            self.assertFalse(robot.handler_acked(root, "x"))
            p.write_text("{broken x")
            self.assertFalse(robot.handler_acked(root, "x"))


if __name__ == "__main__":
    unittest.main()
