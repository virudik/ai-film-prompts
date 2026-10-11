#!/usr/bin/env python3
"""Unit tests for owner panel's deterministic, non-creative GitHub runner."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import process_owner_decisions as app


def blank():
    return {"reviewed": None, "reviewed_at": None, "accepted": None,
            "needs_redo": None, "inserted_into_film": None,
            "montage_note": None, "last_human_update_at": None}


class TransformTests(unittest.TestCase):
    def test_accept_only_from_explicit_button(self):
        old = blank()
        row = app.transform(old, "accept", "2026-10-11T00:00:00Z")
        self.assertEqual(old["reviewed"], None)
        self.assertIs(row["reviewed"], True)
        self.assertIs(row["accepted"], True)
        self.assertIs(row["needs_redo"], False)
        self.assertIsNone(row["inserted_into_film"])

    def test_redo_does_not_start_render(self):
        row = app.transform(blank(), "redo", "2026-10-11T00:00:00Z")
        self.assertIs(row["accepted"], False)
        self.assertIs(row["needs_redo"], True)

    def test_film_accept_cannot_be_undone_automatically(self):
        row = blank()
        row["inserted_into_film"] = True
        with self.assertRaises(ValueError):
            app.transform(row, "redo", "2026-10-11T00:00:00Z")

    def test_montage_is_not_in_film(self):
        row = app.transform(blank(), "to_montage", "2026-10-11T00:00:00Z")
        self.assertEqual(row["montage_note"], "в монтаж")
        self.assertIsNone(row["inserted_into_film"])

    def test_unknown_action_blocked(self):
        with self.assertRaises(ValueError):
            app.transform(blank(), "in_film", "2026-10-11T00:00:00Z")

    def test_no_secret_fails_closed(self):
        with patch.dict(os.environ, {"SUPABASE_SERVICE_ROLE_KEY": ""}):
            with self.assertRaises(RuntimeError):
                app.api("GET", {"select": "id"})


class PrepareTests(unittest.TestCase):
    def _run(self, decisions):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "review-ledger.json").write_text(
                json.dumps({"schema_version": 2, "scenes": {"13": blank()}}),
                encoding="utf-8",
            )
            patches = []
            def fake_patch(row_id, before, after, note):
                patches.append((row_id, before, after, note))
                return True
            with patch.object(app, "ROOT", root), patch.object(app, "api", return_value=decisions), patch.object(app, "patch_status", side_effect=fake_patch):
                app.prepare(root / "plan.json")
            ledger = json.loads((root / "review-ledger.json").read_text(encoding="utf-8"))
            plan = json.loads((root / "plan.json").read_text(encoding="utf-8"))
            return patches, ledger, plan

    def test_prepare_reserves_then_applies_explicit_accept(self):
        decisions = [{"id": "a", "scene_id": 13, "action": "accept",
                      "status": "pending", "result_note": None}]
        patches, ledger, plan = self._run(decisions)
        self.assertEqual([x[:3] for x in patches], [("a", "pending", "in_progress")])
        self.assertTrue(ledger["scenes"]["13"]["accepted"])
        self.assertEqual(len(plan["updates"]), 1)

    def test_conflicting_buttons_need_owner_and_do_not_change_ledger(self):
        decisions = [
            {"id": "a", "scene_id": 13, "action": "accept", "status": "pending"},
            {"id": "b", "scene_id": 13, "action": "redo", "status": "pending"},
        ]
        patches, ledger, plan = self._run(decisions)
        self.assertEqual(len(plan["updates"]), 0)
        self.assertIsNone(ledger["scenes"]["13"]["accepted"])
        self.assertEqual([(x[0], x[2]) for x in patches], [("a", "needs_owner"), ("b", "needs_owner")])


if __name__ == "__main__":
    unittest.main()


class SlowOwnerReleaseTests(unittest.TestCase):
    def test_owner_drop_does_not_falsely_free_physical_slot(self):
        import robot_master_actions as robot
        task_id = "a" * 32
        st = {
            "topview-task-map.json": {"active_by_scene": {"24": [task_id]}, "processed_tasks": []},
            "topview-status.json": {"active_tasks": [{"task_id": task_id, "scene_id": 24}],
                                    "occupied_slots": 1, "free_slots": 5, "slot_capacity": 6},
            "topview-checkpoint.json": {"checked_at": "2026-10-11T16:10:48Z",
                                       "occupied_slots": 1, "active_task_ids": [task_id]},
            "topview-operation-journal.json": {"events": [], "retention_max_events": 500},
        }
        robot.drop_task_telemetry(st, 24, task_id, "2026-10-11T16:40:00Z")
        self.assertEqual(st["topview-status.json"]["occupied_slots"], 1)
        self.assertEqual(st["topview-status.json"]["free_slots"], 5)
        self.assertEqual(st["topview-task-map.json"]["active_by_scene"], {"24": [task_id]})
        self.assertEqual(st["topview-task-map.json"]["processed_tasks"], [])
        self.assertIn(task_id, st["topview-task-map.json"]["owner_released_task_ids"])
        self.assertEqual(st["topview-checkpoint.json"]["checked_at"], "2026-10-11T16:10:48Z")
