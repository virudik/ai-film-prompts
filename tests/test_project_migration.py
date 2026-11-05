"""Path split of Roscosmos and Raznoe (owner 02.11.2026). Offline."""
import json
import struct
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

    def test_terratech_prompts_are_horizontal_with_png(self):
        master = (ROOT / "projects/roscosmos/video-prompts.md").read_text(encoding="utf-8")
        for n in range(26, 31):
            self.assertIn(f'<a id="scene-{n}"></a>', master)
            folder = ROOT / f"projects/roscosmos/references/scenes/scene-{n}"
            expected = {26: 4, 27: 2, 28: 4, 29: 2, 30: 2}[n]
            prompts = list(folder.glob("*.image-prompt.txt"))
            self.assertEqual(len(prompts), expected, n)
            for path in prompts:
                text = path.read_text(encoding="utf-8")
                self.assertIn("1672×941", text)
                self.assertIn("16:9", text)
                self.assertNotIn("9:16", text)
            pngs = list(folder.glob("*.png"))
            live = [p for p in pngs if not p.name.endswith("-old.png")]
            self.assertEqual(len(live), {26: 4, 27: 2, 28: 4, 29: 2, 30: 2}[n], n)
            for png in pngs:
                head = png.read_bytes()[:24]
                self.assertEqual(head[:8], b"\x89PNG\r\n\x1a\n", png.name)
                self.assertEqual(struct.unpack(">II", head[16:24]), (1672, 941), png.name)
        tail = master[master.find('<a id="scene-26">'):]
        self.assertIn("Aspect ratio: 16:9", tail)
        self.assertNotIn("Aspect ratio: 9:16", tail)
        self.assertNotIn("1080×1920", tail)
        self.assertNotIn("authored vertical concepts", tail)
        self.assertNotIn("a landscape 16:9 crop", tail)
        self.assertNotIn("landscape crop", tail)
        self.assertNotIn("through the tall frame", tail)
        self.assertNotIn("set the tall print upright", tail)
        self.assertNotIn("set the print upright", tail)
        self.assertNotIn("Цифру на экране мы не обещаем", tail)
        self.assertIn("Выбираешь территорию и задачу. Сервис подбирает снимки и показывает результат.", tail)
        self.assertIn("No portrait crop", tail)
        refs = json.loads((ROOT / "projects/roscosmos/character-references.json").read_text(encoding="utf-8"))
        tt = [a for a in refs["assets"] if a["id"].startswith("roscosmos-tt-")]
        self.assertEqual(len(tt), 14)
        by_id = {a["id"]: a for a in tt}
        self.assertEqual(
            by_id["roscosmos-tt-26-tt26-delta-clean"]["images"][0]["sha256"],
            by_id["roscosmos-tt-26-tt26-orbit"]["images"][0]["sha256"],
        )
        self.assertEqual(
            by_id["roscosmos-tt-28-tt28-wipe-after"]["images"][0]["sha256"],
            by_id["roscosmos-tt-28-tt28-clearing"]["images"][0]["sha256"],
        )
        self.assertTrue(all(a["editorial_status"] == "not_approved" for a in tt))
        self.assertTrue(all(len(a["images"]) == 1 and a["images"][0]["width"] == 1672 and a["images"][0]["height"] == 941 for a in tt))


if __name__ == "__main__":
    unittest.main()
