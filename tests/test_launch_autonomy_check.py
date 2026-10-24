import importlib.util, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

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

    def test_repository_queue_parses(self):
        repo = Path(__file__).resolve().parents[1]
        r = lac.build(repo, 24, NOW, [])
        self.assertIn(r["verdict"], ("schedule_launched", "chat_only", "no_free_slots", "nothing_ready",
                                     "free_slots_idle_no_schedule_launch"))


if __name__ == "__main__":
    unittest.main()
