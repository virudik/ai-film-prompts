#!/usr/bin/env python3
"""Offline integration/self-recovery tests for AI Film state invariants.

No network calls, no Topview renders, and no production artifact writes.
"""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "scripts" / "build_project_status.py"
MASTER = ROOT / "video-prompts.md"
TOPVIEW = ROOT / "topview-status.json"
TASKMAP = ROOT / "topview-task-map.json"
INSTR = ROOT / "instruction-sync-status.json"


def run_validator(master=MASTER, topview=TOPVIEW, taskmap=TASKMAP):
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "status.json"
        p = subprocess.run(
            [
                "python3", str(BUILD), str(master), "--output", str(out),
                "--synced-at", "2026-09-23T13:30:00Z",
                "--instruction-status-file", str(INSTR),
                "--topview-status-file", str(topview),
                "--topview-task-map-file", str(taskmap),
            ],
            cwd=ROOT, text=True, capture_output=True,
        )
        status = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
        return p, status


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class IntegrationRecoveryTests(unittest.TestCase):
    def test_production_snapshot_is_green(self):
        p, status = run_validator()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(status["health"], "ok")

    def test_multi_task_one_scene_counts_slots_not_unique_scenes(self):
        top = json.loads(TOPVIEW.read_text(encoding="utf-8"))
        task = json.loads(TASKMAP.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(task["active_by_scene"]["20"]), 2)
        self.assertEqual(top["occupied_slots"], len(top["active_tasks"]))
        self.assertEqual(top["occupied_slots"], sum(len(v) for v in task["active_by_scene"].values()))
        self.assertEqual(status_slow := set(run_validator()[1]["slow_scenes"]), {3, 4, 17, 19, 20})
        self.assertIn(20, status_slow)

    def test_terminal_transition_keeps_scene_slow_until_last_task(self):
        top = json.loads(TOPVIEW.read_text(encoding="utf-8"))
        task = json.loads(TASKMAP.read_text(encoding="utf-8"))
        scene20 = list(task["active_by_scene"]["20"])
        self.assertGreaterEqual(len(scene20), 2)
        completed = scene20[0]
        task["active_by_scene"]["20"] = scene20[1:]
        top["active_tasks"] = [x for x in top["active_tasks"] if x["task_id"] != completed]
        top["scenes"]["20"]["active_task_ids"] = scene20[1:]
        top["scenes"]["20"]["task_id"] = scene20[-1]
        top["occupied_slots"] = len(top["active_tasks"])
        top["free_slots"] = max(0, top["slot_capacity"] - top["occupied_slots"])
        with tempfile.TemporaryDirectory() as td:
            tp, mp = Path(td)/"top.json", Path(td)/"map.json"
            write_json(tp, top); write_json(mp, task)
            p, status = run_validator(topview=tp, taskmap=mp)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn(20, status["slow_scenes"])

    def test_terminal_last_task_requires_slow_removal(self):
        top = json.loads(TOPVIEW.read_text(encoding="utf-8"))
        task = json.loads(TASKMAP.read_text(encoding="utf-8"))
        remove = set(task["active_by_scene"]["20"])
        task["active_by_scene"].pop("20")
        top["active_tasks"] = [x for x in top["active_tasks"] if x["task_id"] not in remove]
        top["scenes"].pop("20")
        top["occupied_slots"] = len(top["active_tasks"])
        top["free_slots"] = max(0, top["slot_capacity"] - top["occupied_slots"])
        task["processed_tasks"].append({
            "task_id": "synthetic-terminal-scene20",
            "scene_id": 20,
            "final_status": "success",
            "finished_at": "2026-09-23T13:30:00Z",
        })
        with tempfile.TemporaryDirectory() as td:
            tp, mp = Path(td)/"top.json", Path(td)/"map.json"
            write_json(tp, top); write_json(mp, task)
            p, status = run_validator(topview=tp, taskmap=mp)
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(status["checks"]["no_terminal_only_topview_scene_is_slow"])

    def test_stale_conflicting_topview_snapshot_is_rejected(self):
        top = json.loads(TOPVIEW.read_text(encoding="utf-8"))
        top["occupied_slots"] += 1
        with tempfile.TemporaryDirectory() as td:
            tp = Path(td)/"top.json"; write_json(tp, top)
            p, status = run_validator(topview=tp)
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(status["checks"]["topview_occupied_matches_active_tasks"])

    def test_watcher_watchdog_contract_is_present(self):
        # Static integration guard: Recovery automation prompt is external, so repository
        # docs must retain the permanent watchdog + preserve-enabled contract.
        handoff = (ROOT / "NEW-CHAT-HANDOFF.md").read_text(encoding="utf-8")
        self.assertIn("Recovery is watchdog for watcher", handoff)
        self.assertIn("is_enabled:true", handoff)


if __name__ == "__main__":
    unittest.main()
