"""Path split of Roscosmos and Raznoe (owner 02.11.2026). Offline."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "scripts"))
import projects as prj  # noqa: E402


class MigrationTests(unittest.TestCase):
    def test_folders_and_registry_match(self):
        space = prj.get(ROOT, "roscosmos")
        other = prj.get(ROOT, "raznoe")
        self.assertEqual(space["name"], "Роскосмос")
        self.assertEqual(space["root"], "projects/roscosmos")
        self.assertEqual(other["name"], "Разное")
        self.assertEqual(other["root"], "projects/raznoe")
        self.assertFalse((ROOT / "projects" / "misc").exists())
        self.assertTrue((ROOT / "projects/roscosmos/video-prompts.md").is_file())
        self.assertTrue((ROOT / "projects/raznoe/video-prompts.md").is_file())
        self.assertEqual(prj.validate(ROOT), [])

    def test_new_links_and_old_bookmarks(self):
        self.assertEqual(prj.resolve_project_code(ROOT, "roscosmos", kind="project"), "roscosmos")
        self.assertEqual(prj.resolve_project_code(ROOT, "raznoe", kind="project"), "raznoe")
        self.assertEqual(prj.resolve_project_code(ROOT, "misc", kind="project"), "raznoe")
        self.assertEqual(prj.resolve_project_code(ROOT, "raznoe", kind="p"), "roscosmos")
        self.assertEqual(prj.resolve_project_code(ROOT, "misc", kind="p"), "raznoe")
        self.assertEqual(prj.resolve_project_code(ROOT, "kotmonavty", kind="p"), "kotmonavty")
        self.assertEqual(prj.resolve_project_code(ROOT, "roscosmos", kind="p"), "roscosmos")

    def test_stored_decisions_keep_their_old_meaning(self):
        old = "2026-10-27T13:19:54Z"
        new = "2026-11-02T23:00:00Z"
        self.assertEqual(prj.resolve_project_code(ROOT, "raznoe", kind="stored", recorded_at=old), "roscosmos")
        self.assertEqual(prj.resolve_project_code(ROOT, "raznoe", kind="stored", recorded_at=None), "roscosmos")
        self.assertEqual(prj.resolve_project_code(ROOT, "raznoe", kind="stored", recorded_at=new), "raznoe")
        self.assertEqual(prj.resolve_project_code(ROOT, "misc", kind="stored", recorded_at=old), "raznoe")
        self.assertEqual(prj.resolve_project_code(ROOT, "misc", kind="stored", recorded_at=new), "raznoe")
        row = {"action": "accept", "value": "project:raznoe", "created_at": old}
        self.assertEqual(prj.project_of_row(row, None, ROOT), "roscosmos")
        fresh = {"action": "accept", "value": "project:raznoe", "created_at": new}
        self.assertEqual(prj.project_of_row(fresh, None, ROOT), "raznoe")
        note = {"action": "owner_task", "note": "[проект: misc] море", "created_at": old}
        self.assertEqual(prj.project_of_row(note, None, ROOT), "raznoe")

    def test_moved_reference_path_follows_the_file(self):
        old_space = "projects/" + "raznoe/references/scenes/scene-1/01-earth-work.png"
        self.assertEqual(prj.canonical_reference_project(ROOT, old_space, recorded_at="2026-10-01T00:00:00Z"), "roscosmos")
        live = "projects/raznoe/references/yarik.png"
        self.assertTrue((ROOT / live).is_file())
        self.assertEqual(prj.canonical_reference_project(ROOT, live, recorded_at="2026-11-02T23:00:00Z"), "raznoe")
        old_misc = "projects/" + "misc/references/yarik.png"
        self.assertEqual(prj.canonical_reference_project(ROOT, old_misc), "raznoe")

    def test_site_script_uses_the_same_migration_table(self):
        table = json.loads((ROOT / "projects/project-migrations.json").read_text(encoding="utf-8"))
        js = (ROOT / "projects.js").read_text(encoding="utf-8")
        self.assertIn("?project=", js)
        self.assertIn(table["migrated_at"], js)
        for row in table["migrations"]:
            self.assertIn(f"from_id:'{row['from_id']}'", js)
            self.assertIn(f"to_id:'{row['to_id']}'", js)
        self.assertNotIn("{id:'misc'", js)
        self.assertIn("id:'roscosmos'", js)
        self.assertIn("id:'raznoe'", js)

    def test_roscosmos_queue_stays_paused_and_board_is_unchanged(self):
        space = prj.get(ROOT, "roscosmos")
        q = json.loads((ROOT / space["queue"]).read_text(encoding="utf-8"))
        self.assertEqual(q["board_id"], "1cb8d0f6d11440ce9740bbafab36a6a5")
        self.assertEqual(q["board_name"], "Роскосмос")
        self.assertEqual(q["state"], "paused_by_owner")
        self.assertEqual(len(q["items"]), 29)
        self.assertTrue(all(i["state"] == "paused_by_owner" for i in q["items"]))
        ids = [i["id"] for i in q["items"]]
        self.assertEqual(ids, sorted(ids, key=ids.index))
        self.assertTrue(all(i["project"] == "roscosmos" for i in q["items"]))

    def test_terratech_stills_are_installed_and_not_approved(self):
        master = (ROOT / "projects/roscosmos/video-prompts.md").read_text(encoding="utf-8")
        for n in range(26, 31):
            self.assertIn(f'<a id="scene-{n}"></a>', master)
            folder = ROOT / f"projects/roscosmos/references/scenes/scene-{n}"
            pngs = list(folder.glob("*.png"))
            self.assertEqual(len(pngs), 2, n)
            man = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(man["assets"]), 2)
            for asset in man["assets"]:
                self.assertEqual(asset["editorial_status"], "not_approved")
                self.assertEqual(asset["asset_status"], "ready")
                self.assertEqual(asset["created_by"], "grok")
                self.assertEqual((asset["width"], asset["height"]), (1080, 1920))
                blob = (ROOT / asset["path"]).read_bytes()
                self.assertEqual(asset["sha256"], __import__("hashlib").sha256(blob).hexdigest())
        refs = json.loads((ROOT / "projects/roscosmos/character-references.json").read_text(encoding="utf-8"))
        ready = [a for a in refs["assets"] if str(a.get("id", "")).startswith("roscosmos-tt-")]
        self.assertEqual(len(ready), 10)
        self.assertTrue(all(a["editorial_status"] == "not_approved" and a["images"] for a in ready))
        q = json.loads((ROOT / "projects/roscosmos/ops/topview-launch-queue.json").read_text(encoding="utf-8"))
        self.assertTrue(all(i["scene_id"] < 26 for i in q["items"]))


if __name__ == "__main__":
    unittest.main()
