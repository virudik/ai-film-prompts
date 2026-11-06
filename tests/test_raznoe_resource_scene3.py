#!/usr/bin/env python3
"""Разное scene 3 RESOURCE: supplied stills, horizontal prompts, queue untouched."""
import hashlib
import json
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "projects/raznoe/references/scenes/scene-3"

# Nine originals stay byte-identical. 45737.png is the corrected polymer finale.
UNCHANGED = {
    "01-45726.png": "01513f2f562a0123449194da6b0009724f5de6d7aea0bfde6a821e5d9e981447",
    "02-45728.png": "57f142e033008686a177724d4c72645d4f968ff56cee87a980f011b2c9298538",
    "03-45729.png": "d07e201c2bd080700a21d2764702ec1eb8aa1f9fa2b08d66e4d06ddcc7b6dcb5",
    "04-45731.png": "470f90373582c9964a3f8667d8d88477d0b83801bebdab94b55a44f0b6348de2",
    "05-45732.png": "a2930f221d1b8e1bf6e3ec8f51d81fc5d48a53bde596dd2f504a5d91c0a4c734",
    "06-45734.png": "f342d49694902f9ca53d273808d6ee9a88083a2b9a25b832f597ef0d60a8b884",
    "07-45735.png": "0e9351fcc64378f83ee67c6496119792217d2db38f1dcbb9e547559ee56c8341",
    "08-45736.png": "d5885fa641d8b823e84e85704f454f0023150400537167f2dbb9d1573d47efe5",
    "09-45733.png": "0602cb57b9029eea2966728f80cbeca75a663f5528f48ab1d4daaf8cc74f5776",
}
POLYMER = "802992aa667bd04bacb8e23e7a894a725eef8e1337951dc2feda0b94c2753736"
METAL = "a2b77312b07d7afca0dfd47752423624c8c1afc9424d2320fac21dcc18b3e977"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(path: Path):
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(path.name)
    return struct.unpack(">II", head[16:24])


class RaznoeResourceScene3(unittest.TestCase):
    def test_source_bytes_and_backup(self):
        for name, digest in UNCHANGED.items():
            self.assertEqual(sha256(SCENE / name), digest, name)
        finale = SCENE / "10-45737.png"
        self.assertEqual(sha256(finale), POLYMER)
        self.assertEqual(png_size(finale), (1280, 720))
        old = ROOT / "projects/raznoe/archive/scene-3/45737-old.png"
        self.assertEqual(sha256(old), METAL)
        self.assertEqual(png_size(old), (1672, 941))
        self.assertFalse((SCENE / "45737-old.png").exists())
        self.assertFalse(list(SCENE.rglob("*45737-old*")))
        brief = SCENE / "source/source-prompt.txt"
        self.assertEqual(sha256(brief), "5a6fd2783cfc7e263290c384b93c972af2297f073e3abfbb2507c41b54a3b80f")

    def test_scene_is_horizontal_and_not_approved(self):
        master = (ROOT / "projects/raznoe/video-prompts.md").read_text(encoding="utf-8")
        scene = master[master.find('<a id="scene-3"></a>'):]
        self.assertIn("## Сцена 3 — RESOURCE", scene)
        self.assertIn("Aspect ratio: 16:9", scene)
        self.assertIn("No portrait crop", scene)
        self.assertIn("Grok Imagine Video", scene)
        self.assertIn("exact final frame", scene)
        self.assertIn("@Video1", scene)
        self.assertNotIn("9:16", scene)
        self.assertNotIn("landscape crop", scene.lower())
        self.assertNotIn("45737-old.png\"", scene)  # backup path is text, not an image href
        self.assertNotIn('src="projects/raznoe/archive/scene-3/45737-old.png"', scene)
        self.assertIn("not_approved", scene)
        self.assertIn('"production_state":"DRAFT"', scene)
        # Scenes 1–2 stay vertical.
        head = master[:master.find('<a id="scene-3"></a>')]
        self.assertIn("Aspect ratio: 9:16", head)
        refs = json.loads((ROOT / "projects/raznoe/character-references.json").read_text(encoding="utf-8"))
        engineer = next(c for c in refs["characters"] if c["id"] == "resource-engineer")
        self.assertEqual(engineer["provenance"]["editorial_status"], "not_approved")
        self.assertEqual(engineer["provenance"]["sha256"], UNCHANGED["01-45726.png"])
        polymer = next(a for a in refs["assets"] if a["id"] == "resource-polymer-gripper")
        self.assertEqual(polymer["editorial_status"], "not_approved")
        self.assertEqual(polymer["images"][0]["sha256"], POLYMER)
        self.assertTrue(all("45737-old" not in im["path"] for a in refs["assets"] for im in a["images"]))

    def test_queue_untouched_and_labels_unique(self):
        queue = json.loads((ROOT / "projects/raznoe/ops/topview-launch-queue.json").read_text(encoding="utf-8"))
        self.assertEqual(queue["items"], [])
        self.assertEqual(queue["project"], "raznoe")
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        import topview_prompt_match as pm
        text = (ROOT / "projects/raznoe/video-prompts.md").read_text(encoding="utf-8")
        labels = [label for label, _ in pm.master_blocks(text) if label == "3" or label.startswith("3 ")]
        self.assertEqual(len(labels), len(set(labels)))
        self.assertIn("3", labels)
        self.assertIn("3 · Grok Imagine Video часть 2", labels)
        self.assertIn("3 · Wan 3.0", labels)
        self.assertIn("3 · Seedance 2.0 часть 1", labels)
        self.assertIn("3 · Seedance 2.0 часть 2", labels)


if __name__ == "__main__":
    unittest.main()
