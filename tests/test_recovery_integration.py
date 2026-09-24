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
SYNCED_AT = json.loads((ROOT / "project-status.json").read_text(encoding="utf-8"))["synced_at"]


def run_validator(master=MASTER, topview=TOPVIEW, taskmap=TASKMAP, instr=INSTR):
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "status.json"
        p = subprocess.run(
            [
                "python3", str(BUILD), str(master), "--output", str(out),
                "--synced-at", SYNCED_AT,
                "--instruction-status-file", str(instr),
                "--topview-status-file", str(topview),
                "--topview-task-map-file", str(taskmap),
            ],
            cwd=ROOT, text=True, capture_output=True,
        )
        status = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
        if status is None:
            try:
                status = json.loads(p.stdout)
            except (json.JSONDecodeError, TypeError):
                status = None
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
        self.assertEqual(top["occupied_slots"], len(top["active_tasks"]))
        self.assertEqual(top["occupied_slots"], sum(len(v) for v in task["active_by_scene"].values()))
        status_slow = set(run_validator()[1]["slow_scenes"])
        self.assertEqual(status_slow, {int(s) for s in task["active_by_scene"]})
        self.assertLessEqual(len(status_slow), top["occupied_slots"])

    def test_terminal_transition_keeps_scene_slow_until_last_task(self):
        top = json.loads(TOPVIEW.read_text(encoding="utf-8"))
        task = json.loads(TASKMAP.read_text(encoding="utf-8"))
        sid = next(iter(task["active_by_scene"]))
        original = list(task["active_by_scene"][sid])
        base = original[0]
        synthetic = base + "-synthetic-second"
        task["active_by_scene"][sid] = [base, synthetic]
        base_row = next(x for x in top["active_tasks"] if str(x["scene_id"]) == sid)
        extra = copy.deepcopy(base_row); extra["task_id"] = synthetic
        top["active_tasks"].append(extra)
        top["scenes"][sid]["active_task_ids"] = [base, synthetic]
        top["scenes"][sid]["task_id"] = synthetic
        completed = base
        task["active_by_scene"][sid] = [synthetic]
        top["active_tasks"] = [x for x in top["active_tasks"] if x["task_id"] != completed]
        top["scenes"][sid]["active_task_ids"] = [synthetic]
        top["scenes"][sid]["task_id"] = synthetic
        top["occupied_slots"] = len(top["active_tasks"])
        top["free_slots"] = max(0, top["slot_capacity"] - top["occupied_slots"])
        with tempfile.TemporaryDirectory() as td:
            tp, mp = Path(td)/"top.json", Path(td)/"map.json"
            write_json(tp, top); write_json(mp, task)
            p, status = run_validator(topview=tp, taskmap=mp)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn(int(sid), status["slow_scenes"])

    def test_terminal_last_task_requires_slow_removal(self):
        top = json.loads(TOPVIEW.read_text(encoding="utf-8"))
        task = json.loads(TASKMAP.read_text(encoding="utf-8"))
        sid = next(iter(task["active_by_scene"]))
        terminal_id = task["active_by_scene"][sid][0]
        for row in top["active_tasks"]:
            if row["task_id"] == terminal_id:
                row["topview_status"] = "success"
        top["scenes"][sid]["topview_status"] = "success"
        with tempfile.TemporaryDirectory() as td:
            tp, mp = Path(td)/"top.json", Path(td)/"map.json"
            write_json(tp, top); write_json(mp, task)
            p, status = run_validator(topview=tp, taskmap=mp)
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(status["checks"]["topview_active_statuses_valid"])

    def test_stale_conflicting_topview_snapshot_is_rejected(self):
        top = json.loads(TOPVIEW.read_text(encoding="utf-8"))
        top["occupied_slots"] += 1
        with tempfile.TemporaryDirectory() as td:
            tp = Path(td)/"top.json"; write_json(tp, top)
            p, status = run_validator(topview=tp)
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(status["checks"]["topview_occupied_matches_active_tasks"])

    def test_stale_instruction_certificate_is_maintenance_not_sync_failure(self):
        instr = json.loads(INSTR.read_text(encoding="utf-8"))
        instr["checked_at"] = "2026-01-01T00:00:00Z"
        instr["health"] = "ok"
        instr["all_match"] = True
        with tempfile.TemporaryDirectory() as td:
            ip = Path(td) / "instruction.json"
            write_json(ip, instr)
            p, status = run_validator(instr=ip)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(status["health"], "ok")
            self.assertEqual(status["instruction_sync"]["health"], "stale")
            self.assertEqual(status["warnings"], [])
            self.assertFalse(status["maintenance"]["instruction_verification"]["blocking"])

    def test_control_center_separates_scenes_from_generation_slots(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("runtimeTopview.slowSceneIds.length+' сцен'", html)
        self.assertIn("runtimeTopview.occupied+' генераций · занято '", html)
        self.assertIn("instruction!=='error'", html)

    def test_watcher_watchdog_contract_is_present(self):
        # Static integration guard: Recovery automation prompt is external, so repository
        # docs must retain the permanent watchdog + preserve-enabled contract.
        handoff = (ROOT / "NEW-CHAT-HANDOFF.md").read_text(encoding="utf-8")
        self.assertIn("Recovery is watchdog for watcher", handoff)
        self.assertIn("is_enabled:true", handoff)


if __name__ == "__main__":
    unittest.main()
