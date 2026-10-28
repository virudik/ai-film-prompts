import json, shutil, subprocess, sys, tempfile, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = "1a6244cf1ae747ef847d949a80d6133c"
OTHER = "db4b4d6d0abc4cb4b278ea80738639f2"


def iso(dt):
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


class LightCheckTests(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        for f in ("topview-task-map.json", "topview-status.json", "topview-operation-journal.json",
                  "review-ledger.json", "topview-checkpoint.json"):
            shutil.copy(ROOT / f, self.d / f)
        journal = json.loads((self.d / "topview-operation-journal.json").read_text(encoding="utf-8"))
        if journal.get("events_archive"):
            archive = Path(journal["events_archive"])
            (self.d / archive).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / archive, self.d / archive)
        self.addCleanup(shutil.rmtree, self.d)
        self.now = datetime.now(timezone.utc)
        tm = json.loads((self.d / "topview-task-map.json").read_text(encoding="utf-8"))
        tm["last_scan_at"] = iso(self.now - timedelta(minutes=60))
        tm["scan_cursor"]["last_full_scan_at"] = iso(self.now - timedelta(minutes=60))
        tm["scan_cursor"]["board_task_counts"] = {MAIN: 604, OTHER: 32}
        (self.d / "topview-task-map.json").write_text(json.dumps(tm), encoding="utf-8")

    def run_check(self, counts, page, extra=()):
        b = self.d / "boards.json"; p = self.d / "page.json"
        b.write_text(json.dumps({"result": {"data": [{"boardId": k, "taskCount": v} for k, v in counts.items()]}}))
        p.write_text(json.dumps({"result": {"data": page}}))
        out = subprocess.run([sys.executable, str(ROOT / "scripts/topview_light_check.py"), str(self.d), str(b), str(p), *extra],
                             capture_output=True, text=True, check=True).stdout
        return json.loads(out)

    def old_task(self, tid="a" * 32):
        return {"boardTaskId": tid, "status": "success", "gmtCreate": "2026-10-01 10:00:00", "parameters": {}}

    def new_task(self, tid="b" * 32):
        return {"boardTaskId": tid, "status": "init", "gmtCreate": (self.now - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
                "parameters": {"modelName": "Wan 3.0", "positivePrompt": "x", "useUnlimitMode": True}}

    def test_light_when_nothing_changed(self):
        r = self.run_check({MAIN: 604, OTHER: 32}, [self.old_task()])
        self.assertEqual(r["mode"], "light", r)

    def test_new_task_on_main_page_stays_light_and_is_reported(self):
        r = self.run_check({MAIN: 605, OTHER: 32}, [self.new_task(), self.old_task()])
        self.assertEqual(r["mode"], "light", r)
        self.assertEqual(len(r["unknown_new"]), 1)

    def test_main_grew_more_than_visible_forces_full(self):
        r = self.run_check({MAIN: 607, OTHER: 32}, [self.new_task(), self.old_task()])
        self.assertEqual(r["mode"], "full")

    def test_other_board_change_forces_full(self):
        r = self.run_check({MAIN: 604, OTHER: 33}, [self.old_task()])
        self.assertEqual(r["mode"], "full")

    def test_stale_full_scan_forces_full(self):
        tm = json.loads((self.d / "topview-task-map.json").read_text(encoding="utf-8"))
        tm["scan_cursor"]["last_full_scan_at"] = iso(self.now - timedelta(minutes=200))
        (self.d / "topview-task-map.json").write_text(json.dumps(tm), encoding="utf-8")
        self.assertEqual(self.run_check({MAIN: 604, OTHER: 32}, [self.old_task()])["mode"], "full")

    def test_publish_light_keeps_full_totals_and_records_mode(self):
        tm0 = json.loads((self.d / "topview-task-map.json").read_text(encoding="utf-8"))
        total = tm0["scan_cursor"].get("total_video_tasks")
        st = json.loads((self.d / "topview-status.json").read_text(encoding="utf-8"))
        act = [{"scene_id": a["scene_id"], "task_id": a["task_id"], "model": a.get("model", "Wan 3.0"), "status": "init",
                "started_at": a.get("started_at"), "queue_count": 1, "wait_seconds": 2} for a in st.get("active_tasks", [])]
        cyc = {"checked_at": iso(self.now), "scan_mode": "light", "board_task_counts": {MAIN: 604, OTHER: 32},
               "active": act, "finished": [], "canonical": {"verified_at": iso(self.now), "master_sha256": "x", "health": "ok"}}
        cf = self.d / "cycle.json"; cf.write_text(json.dumps(cyc))
        subprocess.run([sys.executable, str(ROOT / "scripts/monitor_publish.py"), str(self.d), str(cf)], check=True, capture_output=True)
        tm = json.loads((self.d / "topview-task-map.json").read_text(encoding="utf-8"))
        self.assertEqual(tm["scan_cursor"]["scan_mode"], "light")
        self.assertEqual(tm["scan_cursor"].get("total_video_tasks"), total)
        self.assertEqual(tm["scan_cursor"]["last_full_scan_at"], tm0["scan_cursor"]["last_full_scan_at"])
        ao = json.loads((self.d / "topview-status.json").read_text(encoding="utf-8"))["account_observation"]
        self.assertEqual(ao["scan_mode"], "light_board_counts_verified")


if __name__ == "__main__":
    unittest.main()
