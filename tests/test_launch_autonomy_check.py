import importlib.util, json, sys, tempfile, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

spec = importlib.util.spec_from_file_location(
    "launch_autonomy_check", Path(__file__).resolve().parents[1] / "scripts" / "launch_autonomy_check.py")
lac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lac)

NOW = datetime(2026, 10, 18, 5, 30, tzinfo=timezone.utc)


def item(i, run, at, state="submitted"):
    return {"id": i, "scene_id": 1, "state": state, "claim": {"run_id": run, "claimed_at": at}}


class LaunchAutonomyTest(unittest.TestCase):
    def test_classifies_schedule_and_chat(self):
        q = {"items": [item("A", "chatgpt-scheduled-20261018T010000Z", "2026-10-18T01:00:00Z"),
                       item("B", "chatgpt-cloud-20261017-B", "2026-10-17T12:00:00Z"),
                       item("old", "chatgpt-cloud-x", "2026-10-16T12:00:00Z")]}
        ll = lac.launches(q, NOW - timedelta(hours=24))
        self.assertEqual([x["source"] for x in ll], ["chat", "schedule"])
        self.assertEqual(lac.verdict(ll, [], []), "schedule_launched")

    def test_reads_last_claim_after_verified_submission(self):
        q = {"items": [{"id": "S58", "scene_id": 58, "state": "submitted", "claim": None,
                         "last_claim": {"run_id": "chatgpt-scheduled-S58",
                                        "claimed_at": "2026-10-18T04:00:00Z"}}]}
        ll = lac.launches(q, NOW - timedelta(hours=24))
        self.assertEqual(len(ll), 1)
        self.assertEqual(ll[0]["item"], "S58")
        self.assertEqual(ll[0]["source"], "schedule")

    def test_idle_free_slots_detected(self):
        log = ["2026-10-18T02:00:00+00:00\tGitHub robot: Topview telemetry — 5/6 slots, +0 new, 1 finished",
               "2026-10-18T03:00:00+00:00\tGitHub robot: Topview telemetry — 6/6 slots, +0 new, 0 finished"]
        free = lac.free_slot_observations(log)
        self.assertEqual(len(free), 1)
        self.assertEqual(lac.verdict([], free, ["S36"]), "free_slots_idle_no_schedule_launch")
        self.assertEqual(lac.verdict([], [], ["S36"]), "no_free_slots")

    def test_old_scheduled_launch_does_not_hide_current_unresolved_executor(self):
        # Real incident: S61 launched 30-Oct; on 31-Oct the 24h verdict stayed green through a 5h40 gap.
        ll = [{"source": "schedule", "claimed_at": "2026-10-30T15:37:29Z"}]
        free = [{"at": "2026-10-31T05:28:33Z", "occupied": 5, "capacity": 6}]
        for state in ("launch_stalled", "reconciliation_required", "observation_stale"):
            with self.subTest(state=state):
                self.assertEqual(lac.verdict(ll, free, ["S72-WAN30"],
                                            {"state": state, "unresolved": True}), "launch_stalled")
        self.assertEqual(lac.verdict(ll, free, ["S72-WAN30"],
                                    {"state": "capacity_full", "unresolved": False}), "schedule_launched")

    def test_build_preserves_stalled_diagnosis_and_marks_stale_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'ops').mkdir()
            (root / 'ops/topview-launch-queue.json').write_text(json.dumps({'items': [
                item('old-success', 'chatgpt-scheduled-old', '2026-10-18T01:00:00Z')]}))
            (root / 'automation-monitor-status.json').write_text(json.dumps({
                'health': 'ok', 'launcher_health': {'state': 'launch_stalled', 'unresolved': True,
                                                  'checked_at': '2026-10-18T03:00:00Z'}}))
            report = lac.build(root, 24, NOW, [])
            self.assertEqual(report['launches_by_schedule'], 1)
            self.assertEqual(report['verdict'], 'launch_stalled')
            self.assertTrue(report['launcher_observation_stale'])

    def test_notify_flag_routes_stalled_report_even_with_a_previous_scheduled_launch(self):
        report = {'schema_version': 1, 'verdict': 'launch_stalled', 'window_hours': 24,
                  'launches_by_schedule': 1, 'launches_by_chat': 0, 'ready_items_waiting': 33,
                  'free_slot_observations': [], 'launcher_observation_stale': False,
                  'launcher_health': {'state': 'launch_stalled', 'reason': 'no_handler_receipt',
                                      'checked_at': '2026-10-31T06:50:33Z'}}
        with tempfile.TemporaryDirectory() as tmp, patch.object(lac, 'build', return_value=report), \
                patch.object(lac, 'git_log', return_value=[]), patch.object(lac, 'notify') as notify:
            self.assertEqual(lac.main([tmp, '--notify']), 0)
            notify.assert_called_once_with(report)
        with patch('robot_telemetry.GhNotifier') as notifier:
            lac.notify(report)
            _title, text = notifier.return_value.post.call_args.args
            self.assertIn('расписания: 1', text)
            self.assertIn('unresolved', text)
            self.assertNotIn('ничего не запустило', text)

    def test_repository_queue_parses(self):
        repo = Path(__file__).resolve().parents[1]
        r = lac.build(repo, 24, NOW, [])
        self.assertIn(r["verdict"], ("schedule_launched", "chat_only", "no_free_slots", "nothing_ready",
                                     "free_slots_idle_no_schedule_launch", "launch_stalled"))
        self.assertIn("launcher_health", r)


if __name__ == "__main__":
    unittest.main()
