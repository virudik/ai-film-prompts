#!/usr/bin/env python3
"""The scene-pack note points at existing canon and does not invent a second standard."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenePackCheck(unittest.TestCase):
    def test_pointer_is_not_an_eighth_instruction(self):
        text = (ROOT / "ops/SCENE-PACK-CHECK.md").read_text(encoding="utf-8")
        self.assertIn("восьмая инструкция", text)
        for needle in (
            "PROMPT-STYLE-GUIDE.md",
            "SYNC-RUNBOOK.md",
            "review-ledger.json",
            "production_state",
            "not_approved",
            "H-FRONT",
            "Сцена 36",
        ):
            self.assertIn(needle, text)
        self.assertNotIn("production_state`: `PACK_READY`", text)
        guide = (ROOT / "PROMPT-STYLE-GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("ops/SCENE-PACK-CHECK.md", guide)
        self.assertIn("QA §11", guide)


if __name__ == "__main__":
    unittest.main()
