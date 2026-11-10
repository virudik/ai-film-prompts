#!/usr/bin/env python3
"""Разное scene 3 RESOURCE: supplied stills, horizontal prompts, queue untouched."""
import hashlib
import json
import re
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


def scene_block(master: str, scene_id: int) -> str:
    """Select exactly one scene; native subscene anchors are not boundaries."""
    anchor = f'<a id="scene-{scene_id}"></a>'
    start = master.index(anchor)  # A missing scene must fail, not select the last byte.
    rest = master[start + len(anchor):]
    following = re.search(r'^<a id="scene-\d+"></a>\s*$', rest, re.M)
    end = start + len(anchor) + following.start() if following else len(master)
    return master[start:end]


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
        scene = scene_block(master, 3)
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

    def test_native_116_cut_keeps_source_and_names_unaccepted_attempts(self):
        master = (ROOT / "projects/raznoe/video-prompts.md").read_text(encoding="utf-8")
        scene = scene_block(master, 3)
        self.assertIn("### Native Grok · 19 клипов · 114 с", scene)
        self.assertIn("A04_shred · 7 с", scene)
        self.assertIn("C06_cycle · 5 с", scene)
        self.assertIn("A04_shred-v2", scene)
        self.assertIn("не доказывает", scene)
        self.assertIn("монтажный пропуск", scene)
        self.assertTrue((ROOT / "projects/raznoe/references/scenes/scene-3/expansion/prompts/A04_shred.txt").is_file())
        self.assertTrue((ROOT / "projects/raznoe/references/scenes/scene-3/expansion/prompts/A04_shred-v2.txt").is_file())
        self.assertNotEqual(
            sha256(ROOT / "projects/raznoe/references/scenes/scene-3/expansion/prompts/A04_shred.txt"),
            sha256(ROOT / "projects/raznoe/references/scenes/scene-3/expansion/prompts/A04_shred-v2.txt"),
        )
        self.assertEqual(scene.count('class="native-prompt"'), 19)
        self.assertIn("A02_retrieve", scene)
        self.assertLess(scene.find('id="scene-3-native-A01_drop"'), scene.find('id="scene-3-native-A02_retrieve"'))
        self.assertLess(scene.find('id="scene-3-native-A02_retrieve"'), scene.find('id="scene-3-native-A02_blue"'))
        self.assertIn("https://drive.google.com/drive/folders/1FHwi_A1cpODMy2YAwggkkOneIdNA4vS2", scene)
        for name in (
            "A03_sort-v1",
            "A04_shred-v1",
            "A05_material-v1",
            "B05_pad-v1",
            "C01_orbit-v1",
            "C06_cycle-v1",
            "RESOURCE-part-1-15s.mp4",
        ):
            self.assertIn(name, scene)
        self.assertIn("Ассистентский QC: отклонить", scene)
        self.assertIn("не принят", scene.lower())
        self.assertNotIn("Новых девятнадцати роликов нет", scene)
        self.assertNotIn('src="projects/raznoe/archive/scene-3/expansion-2026-11-06/', scene)
        exp = ROOT / "projects/raznoe/references/scenes/scene-3/expansion"
        listed = json.loads((exp / "assets-sha256.json").read_text(encoding="utf-8"))
        self.assertEqual(len(listed), 24)
        for name, digest in listed.items():
            self.assertEqual(sha256(exp / "assets" / name), digest, name)
            self.assertIn(f'src="projects/raznoe/references/scenes/scene-3/expansion/assets/{name}"', scene)
        forbidden = {"resolution", "image_path", "last_frame_path", "keyframes"}
        for path in (exp / "requests").glob("*.json"):
            args = json.loads(path.read_text(encoding="utf-8"))["arguments"]
            self.assertTrue(forbidden.isdisjoint(args), path.name)
        names = {p.name for p in (exp / "prompts").glob("*.txt")}
        # Nineteen original prompts and eight retained v2 attempts remain history.
        # Additional active revisions are required by active-cut.json, not a stale
        # total of 27. Also reject missing files, unregistered extras and wrong bytes.
        original_ids = {
            "A01_drop", "A02_retrieve", "A02_blue", "A03_sort", "A04_shred",
            "A05_material", "A06_print", "B01_pickup", "B02_install", "B03_build",
            "B04_check", "B05_pad", "B06_liftoff", "C01_orbit", "C02_debris",
            "C03_capture", "C04_recycle", "C05_station", "C06_cycle",
        }
        retained_v2 = {"A04_shred", "A05_material", "C01_orbit", "C02_debris",
                       "C03_capture", "C04_recycle", "C05_station", "C06_cycle"}
        legacy = {f"{name}.txt" for name in original_ids}
        legacy.update(f"{name}-v2.txt" for name in retained_v2)
        cut = json.loads((exp / "active-cut.json").read_text(encoding="utf-8"))
        self.assertEqual(cut["clip_count"], 19)
        self.assertEqual(len(cut["clips"]), 19)
        self.assertEqual({clip["clip_id"] for clip in cut["clips"]}, original_ids)
        self.assertEqual(cut["total_duration_s"], 114)
        self.assertEqual(sum(clip["duration_s"] for clip in cut["clips"]), 114)
        self.assertEqual(cut["editorial_status"], "not_approved")
        self.assertFalse(cut["execution_authorized"])
        active = set()
        for clip in cut["clips"]:
            prompt = ROOT / clip["prompt_file"]
            self.assertEqual(prompt.parent, exp / "prompts")
            self.assertEqual(prompt.stem, clip["active_version"])
            self.assertEqual(sha256(prompt), clip["prompt_sha256"], prompt.name)
            self.assertEqual(clip["aspect_ratio"], "16:9")
            self.assertFalse(clip["execute"])
            active.add(prompt.name)
        self.assertEqual(names, legacy | active)

    def test_scene_boundary_ignores_native_anchors_and_neighbor_orientation(self):
        sample = ('<a id="scene-3"></a>\nAspect ratio: 16:9\n'
                  '<a id="scene-3-native-A01_drop"></a>\nnative prompt\n'
                  '<a id="scene-4"></a>\nAspect ratio: 9:16\n')
        resource = scene_block(sample, 3)
        self.assertIn("native prompt", resource)
        self.assertNotIn("9:16", resource)
        self.assertNotIn('id="scene-4"', resource)
        self.assertIn("9:16", scene_block(sample, 4))
        with self.assertRaises(ValueError):
            scene_block(sample, 99)


if __name__ == "__main__":
    unittest.main()
