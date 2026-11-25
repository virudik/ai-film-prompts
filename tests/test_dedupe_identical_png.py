import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dedupe_identical_png as dedupe  # noqa: E402


class DedupeIdenticalPngTests(unittest.TestCase):
    def test_keeps_the_cited_file_and_rewrites_the_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "references").mkdir()
            (root / "copies").mkdir()
            blob = b"\x89PNG same-bytes"
            (root / "references" / "kept.png").write_bytes(blob)
            (root / "copies" / "kept-copy.png").write_bytes(blob)
            (root / "scene.md").write_text("see copies/kept-copy.png and references/kept.png\n", encoding="utf-8")
            mapping = dedupe.plan(root)
            self.assertEqual(mapping, {"copies/kept-copy.png": "references/kept.png"})
            rewritten, deleted = dedupe.apply_plan(root, mapping, write=True)
            self.assertIn("scene.md", rewritten)
            self.assertEqual((root / "scene.md").read_text(encoding="utf-8"),
                             "see references/kept.png and references/kept.png\n")
            self.assertFalse((root / "copies" / "kept-copy.png").exists())
            self.assertTrue((root / "references" / "kept.png").is_file())
            self.assertEqual(deleted, ["copies/kept-copy.png"])
            self.assertEqual(dedupe.plan(root), {})


if __name__ == "__main__":
    unittest.main()
