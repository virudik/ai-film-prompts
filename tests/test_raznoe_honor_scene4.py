#!/usr/bin/env python3
"""Разное scene 4 HONOR: mood stills only, full prompt package, queue untouched."""
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import topview_prompt_match as pm  # noqa: E402

SCENE = ROOT / "projects/raznoe/references/scenes/scene-4"
EXPECT = {
    "01-honor-realism.png": "db0c1517d55c460eb78e698c7c4eddb5737fe3e0462d90d7c68502b629a5081e",
    "02-honor-3d.png": "b661000edd39577bf516c5c7a3567b21597b96108cffe4ddddeaf611d0e04c24",
    "03-honor-drawn.png": "2279000421fef277e1e7555498009f983f7a47e6943e549c75111b2ddf3b3e1d",
}


class HonorScene4(unittest.TestCase):
    def test_mood_frames_and_package(self):
        for name, digest in EXPECT.items():
            path = SCENE / name
            data = path.read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
            self.assertEqual(struct.unpack(">II", data[16:24]), (1280, 720))
        master = (ROOT / "projects/raznoe/video-prompts.md").read_text(encoding="utf-8")
        self.assertIn('id="scene-3"', master)
        self.assertNotIn("</pr<a", master)
        before = master[:master.find("## Сцена 4 — HONOR")]
        self.assertEqual(before.count("<pre") - before.count("</pre>"), 0)
        start = master.find('id="scene-4"')
        end = master.find('id="scene-5"')
        scene = master[start:end]
        contest = master[end:]
        self.assertIn("## Сцена 4 — HONOR", scene)
        self.assertIn("HONOR Magic9 Pro Max", scene)
        self.assertIn("канонических продуктовых PNG нет", scene)
        self.assertIn("H-FRONT", scene)
        self.assertIn("H-CAM", scene)
        self.assertIn("H-BACK.image-prompt.txt", scene)
        self.assertIn('id="honor-4-3d"', scene)
        self.assertIn('id="honor-4-real"', scene)
        self.assertIn('id="honor-4-ink"', scene)
        self.assertIn("11ZlXyZwAVpcKymg8vM9qjziKrbop3wZA", scene)
        self.assertIn("1u1lCAo2bRKL1qth5GU3FZC1eGx-GUksC", scene)
        self.assertIn("предложение автора, не утверждено", scene)
        self.assertIn("Aspect ratio: 16:9", scene)
        self.assertIn("No portrait crop", scene)
        self.assertIn("4 × 30 = 120", scene)
        self.assertIn("8 × 15 = 120", scene)
        self.assertIn("1:45–2:00", scene)
        self.assertNotIn("Duration: 120", scene)
        self.assertNotIn("9:16", scene)
        self.assertNotIn("landscape crop", scene.lower())
        self.assertNotIn("honor-contact-sheet", scene)
        self.assertNotIn("production-ready", scene.lower())
        self.assertIn("not_approved", scene)
        self.assertEqual(scene.count("Duration: 30s"), 12)
        self.assertEqual(scene.count("Duration: 15s"), 24)
        self.assertIn("## Сцена 5 — HONOR X9e Pro", contest)
        self.assertIn("[ГОРОД]", contest)
        self.assertIn("Заявка не отправлена", contest)
        self.assertIn("9:16", contest)
        self.assertIn("п. 4.3.3", contest)
        self.assertIn("Серёгиус", contest)
        self.assertNotIn("scene-5/", contest)
        self.assertFalse((ROOT / "projects/raznoe/references/scenes/scene-5").exists())
        labels = [label for label, _ in pm.master_blocks(master) if str(label).startswith("4")]
        self.assertEqual(labels[0], "4")
        self.assertEqual(len(labels), 36)
        self.assertEqual(len(labels), len(set(labels)))
        self.assertIn("4 · реализм · Wan 3.0 часть 1", labels)
        self.assertIn("4 · рисовка · Seedance 2.0 часть 8", labels)
        queue = json.loads((ROOT / "projects/raznoe/ops/topview-launch-queue.json").read_text(encoding="utf-8"))
        self.assertEqual(queue["items"], [])
        refs = json.loads((ROOT / "projects/raznoe/character-references.json").read_text(encoding="utf-8"))
        moods = [a for a in refs["assets"] if str(a.get("id", "")).startswith("honor-mood-")]
        self.assertEqual(len(moods), 3)
        self.assertTrue(all(a["editorial_status"] == "not_approved" for a in moods))


if __name__ == "__main__":
    unittest.main()
