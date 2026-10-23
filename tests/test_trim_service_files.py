import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import canon_health as ch  # noqa: E402
import trim_service_files as tsf  # noqa: E402

NOW = datetime(2026, 10, 23, 14, 0, tzinfo=timezone.utc)


def write(root, rel, data):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")


class CheckpointTests(unittest.TestCase):
    def test_keeps_newest_sections_and_archives_rest_verbatim(self):
        text = "".join(f"# Запись {i}\n\nтекст {i}\n\n---\n\n" for i in range(8))
        live, arch, n = tsf.trim_checkpoint(text, "", tsf.CHECKPOINT_ARCHIVE, keep=3)
        self.assertEqual(n, 5)
        self.assertIn("# Запись 0", live)
        self.assertIn("# Запись 2", live)
        self.assertNotIn("# Запись 3", live)
        self.assertNotIn("---\n\n---", live)
        for i in range(3, 8):
            self.assertIn(f"# Запись {i}\n\nтекст {i}", arch)
        self.assertIn(tsf.CHECKPOINT_ARCHIVE, live)

    def test_second_run_prepends_and_is_idempotent(self):
        text = "".join(f"# Запись {i}\n\nтекст\n\n" for i in range(5))
        live, arch, _ = tsf.trim_checkpoint(text, "", "a.md", keep=3)
        self.assertIsNone(tsf.trim_checkpoint(live, arch, "a.md", keep=3))
        newer = "# Новая\n\nx\n\n" + live
        live2, arch2, n = tsf.trim_checkpoint(newer, arch, "a.md", keep=3)
        self.assertEqual(n, 1)
        self.assertLess(arch2.index("# Запись 2"), arch2.index("# Запись 3"))
        self.assertEqual(arch2.count("# Архив контрольных точек"), 1)
        self.assertEqual(live2.count("Более ранние записи"), 1)


class RegisterTests(unittest.TestCase):
    def test_finished_work_leaves_active_and_old_completed_is_archived(self):
        reg = {"schema_version": 1, "active_work": [
            {"work_id": "A", "status": "in_progress", "done": [f"d{i}" for i in range(14)]},
            {"work_id": "B", "status": "completed_verified", "updated_at": "2026-10-22T00:00:00Z"}],
            "completed_work": [{"work_id": f"C{i}", "status": "completed", "updated_at": f"2026-10-{10 + i}T00:00:00Z"}
                               for i in range(3)]}
        new, arch, moved, archived = tsf.trim_register(reg, None, keep=2, keep_done=10)
        self.assertEqual([w["work_id"] for w in new["active_work"]], ["A"])
        self.assertEqual(new["active_work"][0]["done"], [f"d{i}" for i in range(4, 14)])
        self.assertEqual(new["active_work"][0]["done_archived_points"], 4)
        self.assertEqual([w["work_id"] for w in new["completed_work"]], ["B", "C2"])
        self.assertEqual({w["work_id"] for w in arch["completed_work"]}, {"C0", "C1"})
        self.assertEqual(arch["trimmed_done"][0]["done"], ["d0", "d1", "d2", "d3"])
        self.assertEqual(moved, 1)
        self.assertEqual(archived, 3)

    def test_nothing_to_do(self):
        reg = {"active_work": [{"work_id": "A", "status": "in_progress", "done": ["x"]}], "completed_work": []}
        self.assertIsNone(tsf.trim_register(reg, None))


class QueueTests(unittest.TestCase):
    def queue(self):
        return {"items": [
            {"id": "W", "scene_id": 1, "state": "waiting_for_slot"},
            {"id": "BL", "scene_id": 1, "state": "blocked_inputs"},
            {"id": "H", "scene_id": 1, "state": "held_owner_site"},
            {"id": "SUP", "scene_id": 2, "state": "superseded_owner_model_selection", "canonical_block_label": "2"},
            {"id": "CAN", "scene_id": 3, "state": "cancelled_owner"},
            {"id": "OLD", "scene_id": 4, "state": "submitted", "submitted_at": "2026-10-10T00:00:00Z",
             "task_id": "t" * 32, "canonical_block_label": "4", "canonical_prompt_sha256": "s", "references": [1, 2]},
            {"id": "NEW", "scene_id": 5, "state": "submitted", "submitted_at": "2026-10-22 01:00:00Z"},
            {"id": "NODATE", "scene_id": 6, "state": "submitted"}]}

    def test_moves_only_finished_and_old(self):
        q, arch, n = tsf.trim_queue(self.queue(), None, NOW)
        self.assertEqual([i["id"] for i in q["items"]], ["W", "BL", "H", "NEW", "NODATE"])
        self.assertEqual(n, 3)
        self.assertEqual({i["id"] for i in arch["items"]}, {"SUP", "CAN", "OLD"})
        stub = [s for s in q["archived_items"] if s["id"] == "OLD"][0]
        self.assertEqual(stub["task_id"], "t" * 32)
        self.assertEqual(stub["canonical_prompt_sha256"], "s")
        self.assertNotIn("references", stub)
        self.assertEqual(q["archived_items_file"], tsf.QUEUE_ARCHIVE)

    def test_run_writes_root_and_projects(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, tsf.QUEUE, self.queue())
            write(d, "projects/projects.json", {"projects": [{"id": "seregius"}, {"id": "p1"}]})
            write(d, "projects/p1/" + tsf.QUEUE, self.queue())
            write(d, "projects/p1/" + tsf.CHECKPOINT, "".join(f"# R{i}\n\nx\n\n" for i in range(7)))
            report = tsf.run(d, write=True, now=NOW)
            self.assertEqual(len(report), 3)
            self.assertTrue((Path(d) / tsf.QUEUE_ARCHIVE).is_file())
            pq = json.loads((Path(d) / "projects/p1" / tsf.QUEUE).read_text(encoding="utf-8"))
            self.assertEqual(pq["archived_items_file"], "projects/p1/" + tsf.QUEUE_ARCHIVE)
            self.assertTrue((Path(d) / "projects/p1" / tsf.CHECKPOINT_ARCHIVE).is_file())
            self.assertEqual(tsf.run(d, write=True, now=NOW), [])


class CanonHealthServiceSizeTests(unittest.TestCase):
    def test_oversized_service_file_warns(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "ops").mkdir()
            for name in ch.DOCS:
                (root / name).write_text("x\n", encoding="utf-8")
            (root / "NEW-CHAT-HANDOFF.md").write_text("## Сейчас 23.10.2026\nok\n", encoding="utf-8")
            (root / "project-status.json").write_text(json.dumps({"scene_ids": [1], "health": "ok"}), encoding="utf-8")
            write(d, "reports/current-work-checkpoint.md", "x" * 90_000)
            res = ch.check(root, NOW)
            self.assertIn("service-file-size", [p["code"] for p in res["problems"]])
            write(d, "reports/current-work-checkpoint.md", "x" * 1000)
            res = ch.check(root, NOW)
            self.assertNotIn("service-file-size", [p["code"] for p in res["problems"]])


if __name__ == "__main__":
    unittest.main()
