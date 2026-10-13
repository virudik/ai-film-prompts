import importlib.util
import unittest

spec = importlib.util.spec_from_file_location("archiver", "scripts/topview_video_archive.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class ArchiveGuards(unittest.TestCase):
    def test_only_verified_completed_mapped_tasks(self):
        good = "a" * 32
        wrong = "b" * 32
        items = [
            {"task_id": good, "scene_id": 24, "final_status": "success", "finished_at": "2026-10-12T00:00:00Z"},
            {"task_id": wrong, "scene_id": 25, "final_status": "fail"},
            {"task_id": "c" * 32, "scene_id": 31, "final_status": "running"},
            {"task_id": "invalid", "scene_id": 30, "final_status": "success"},
            {"task_id": "d" * 32, "scene_id": None, "final_status": "success"},
        ]
        self.assertEqual(a.candidates({"processed_tasks": items}, {"videos": {}}), [(24, good)])
        self.assertEqual(a.candidates({"processed_tasks": items}, {"videos": {good: {}}}), [])

    def test_pool_selects_only_allowlisted_unmodified_owner_seed(self):
        name = "reserved-slot-001.seed"
        seed = {"pool_slots": {name: "known-id"}}
        items = [{"id": "other-id", "name": name, "mimeType": "text/markdown",
                  "parents": [a.POOL_PARENT], "size": "8270"}]
        self.assertIsNone(a.choose_slot(items, seed))
        items.append({"id": "known-id", "name": name, "mimeType": "text/markdown",
                      "parents": [a.POOL_PARENT], "size": "8270"})
        self.assertEqual(a.choose_slot(items, seed), "known-id")

    def test_preserves_versions_of_same_scene(self):
        t1, t2 = "1" * 32, "2" * 32
        rows = [{"task_id": t1, "scene_id": 27, "final_status": "success", "finished_at": "2026-10-11T01:00:00Z"},
                {"task_id": t2, "scene_id": 27, "final_status": "success", "finished_at": "2026-10-12T01:00:00Z"}]
        self.assertEqual(a.candidates({"processed_tasks": rows}, {"videos": {}}), [(27, t2), (27, t1)])


if __name__ == "__main__":
    unittest.main()
