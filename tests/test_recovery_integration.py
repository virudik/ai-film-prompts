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
CHECKPOINT = ROOT / "topview-checkpoint.json"
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

    def test_task_map_drift_is_nonblocking_maintenance(self):
        task = json.loads(TASKMAP.read_text(encoding="utf-8"))
        sid = next(iter(task["active_by_scene"]))
        task["active_by_scene"][sid] = []
        with tempfile.TemporaryDirectory() as td:
            mp = Path(td) / "map.json"
            write_json(mp, task)
            p, status = run_validator(taskmap=mp)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(status["health"], "ok")
            self.assertEqual(status["maintenance"]["topview_task_map"]["state"], "drift")
            self.assertFalse(status["maintenance"]["topview_task_map"]["blocking"])

    def test_stable_topview_checkpoint_matches_public_snapshot(self):
        top = json.loads(TOPVIEW.read_text(encoding="utf-8"))
        checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        self.assertEqual(checkpoint["checked_at"], top["checked_at"])
        self.assertEqual(checkpoint["occupied_slots"], top["occupied_slots"])
        self.assertEqual(
            sorted(checkpoint["active_task_ids"]),
            sorted(x["task_id"] for x in top["active_tasks"]),
        )
        self.assertEqual(
            sorted(checkpoint["active_scene_ids"]),
            sorted({x["scene_id"] for x in top["active_tasks"]}),
        )

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
        self.assertIn("$('metricSlow').textContent=runtimeTopview.occupied+' из '+runtimeTopview.capacity;", html)
        self.assertIn("$('metricSlowMeta').textContent='Свободно '+runtimeTopview.free+' · '+runtimeTopview.slowSceneIds.length+' сцен';", html)
        self.assertNotIn("metricSlowIds", html)
        self.assertIn("cap.innerHTML='занято '+occupied+' из '+capacity+' · свободно '+free", html)
        self.assertNotIn('id="metricWorkIds"', html)
        self.assertIn('id="backToTop"', html)
        self.assertIn('id="filterPanel"', html)
        self.assertIn('id="analysisPicker"', html)
        self.assertIn('>Монтажный разбор</summary>', html)
        self.assertNotIn('>Монтажный разбор фильма<', html)
        self.assertIn('Seregius_montazhny_razbor.html', html)
        self.assertIn('Seregius_montazhny_razbor-2.html', html)
        self.assertTrue((ROOT / "Seregius_montazhny_razbor.html").exists())
        self.assertTrue((ROOT / "Seregius_montazhny_razbor-2.html").exists())
        self.assertIn("$('projectStatus').textContent=`${s.scenes} активных сцен · ${s.prompt_texts} промтов · ${s.work_items_count} рабочих направлений`;", html)
        self.assertNotIn('id="schema"', html)
        self.assertIn("instruction!=='error'", html)
        self.assertIn("const authoritativeHealthy=s.health==='ok'&&instruction!=='error'&&masterHashMatches;", html)
        self.assertIn("✓ ПРОЕКТ СИНХРОНИЗИРОВАН", html)
        self.assertIn("✕ ОШИБКА КАНОНИЧЕСКОЙ СИНХРОНИЗАЦИИ", html)
        self.assertIn("Topview telemetry временно устарела", html)

    def test_watcher_watchdog_contract_is_present(self):
        # Static integration guard: Recovery automation prompt is external, so repository
        # docs must retain the permanent watchdog + preserve-enabled contract.
        handoff = (ROOT / "NEW-CHAT-HANDOFF.md").read_text(encoding="utf-8")
        self.assertIn("Recovery is watchdog for watcher", handoff)
        self.assertIn("is_enabled:true", handoff)


if __name__ == "__main__":
    unittest.main()
