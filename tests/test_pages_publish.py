import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import pages_publish as pages  # noqa: E402


class PagesPublishTests(unittest.TestCase):
    def test_workflow_mode_drops_unreferenced_stills_and_keeps_thumbs(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "references" / "scenes").mkdir(parents=True)
            (root / "references" / "thumbs").mkdir()
            (root / "references" / "scenes" / "big.png").write_bytes(b"x" * 1000)
            (root / "references" / "thumbs" / "big.webp").write_bytes(b"y" * 10)
            (root / "index.html").write_text('<img src="references/thumbs/big.webp">', encoding="utf-8")
            (root / "keep.txt").write_text("status", encoding="utf-8")
            self.assertEqual(pages.deploy_mode(root), "legacy")
            self.assertGreater(pages.published_bytes(root, "legacy"), pages.published_bytes(root, "workflow"))
            dest = root / "out"
            pages.assemble(root, dest, "workflow")
            self.assertTrue((dest / ".nojekyll").is_file())
            self.assertTrue((dest / "references" / "thumbs" / "big.webp").is_file())
            self.assertTrue((dest / "keep.txt").is_file())
            self.assertFalse((dest / "references" / "scenes" / "big.png").exists())

    def test_an_image_named_by_html_stays(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "references" / "full").mkdir(parents=True)
            (root / "references" / "full" / "face.jpg").write_bytes(b"z" * 20)
            (root / "parodies.html").write_text('<img src="references/full/face.jpg">', encoding="utf-8")
            selected = pages.selected_files(root, "workflow")
            self.assertIn("references/full/face.jpg", selected)


if __name__ == "__main__":
    unittest.main()
