#!/usr/bin/env python3
"""topview_prompt_match: offline tests (fake API client, no network, no keys)."""
import contextlib
import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import topview_prompt_match as pm  # noqa: E402

MASTER = (ROOT / "video-prompts.md").read_text(encoding="utf-8")
BLOCKS = pm.master_blocks(MASTER)


class Fake:
    def __init__(self, prompts, model="Wan 3.0"):
        self.prompts, self.model, self.calls = prompts, model, []
        self.requests = 0

    def get(self, path, query=None):
        self.calls.append((path, query))
        assert path == "/boards/tasks/detail", path          # read-only: nothing else is ever touched
        return {"parameters": {"positivePrompt": self.prompts[query["taskId"]], "modelName": self.model}}


class PromptMatch(unittest.TestCase):
    def test_every_master_block_is_found_and_labelled(self):
        labels = [l for l, _ in BLOCKS]
        self.assertEqual(len(labels), len(set(labels)))
        self.assertIn("28 B1", labels)
        self.assertIn("27 · Seedance 2.0 часть 2", labels)
        for suffix in "ABCDEF":
            self.assertIn("49" + suffix, labels)
        self.assertIn("50A", labels)
        self.assertIn("50B", labels)
        project = json.loads((ROOT / "project-status.json").read_text(encoding="utf-8"))
        self.assertEqual(project["health"], "ok")
        self.assertNotIn("20 · песня 13", labels)  # scene 20 is retired and permanently reserved
        self.assertEqual(len(labels), project["prompt_texts"])  # match the live canonical master

    def test_topview_flavoured_text_matches_normalized(self):
        label, body = next((l, b) for l, b in BLOCKS if l == "24")
        topview = pm.re.sub(r"@Image(\d)", r"<<<Image\1>>>", body).replace("\n", "\r\n")
        got = pm.classify(topview, BLOCKS)
        self.assertEqual(got[:2], ("24", "normalized"))

    def test_small_edit_is_high_and_unrelated_text_is_low(self):
        label, body = next((l, b) for l, b in BLOCKS if l == "31")
        edited = body.replace("Photoreal", "Photo-real", 1)
        self.assertEqual(pm.classify(edited, BLOCKS)[:2], ("31", "high"))
        self.assertEqual(pm.classify("A cat walks along a wall.", BLOCKS)[1], "low")

    def test_main_prints_only_task_id_scene_and_confidence_and_uses_get_detail_only(self):
        body24 = dict(BLOCKS)["24"]
        fake = Fake({"a" * 32: body24})
        out = io.StringIO()
        env = {"TOPVIEW_API_KEY": "secret-key-xyz", "TOPVIEW_UID": "uid-123"}
        with patch.dict(os.environ, env), patch.object(pm.scan, "Client", lambda k, u: fake), \
                contextlib.redirect_stdout(out):
            self.assertEqual(self._run("a" * 32), 0)
        text = out.getvalue()
        self.assertIn("a" * 32 + " -> Scene 24 · exact", text)
        self.assertNotIn("secret-key-xyz", text)
        self.assertNotIn("uid-123", text)
        self.assertNotIn("Mode: reference-to-video", text)     # prompt text is never printed
        self.assertEqual({c[0] for c in fake.calls}, {"/boards/tasks/detail"})

    def _run(self, tid):
        with patch.object(sys, "argv", ["x", "--tasks", tid]):
            return pm.main()

    def test_not_configured_is_a_noop(self):
        out = io.StringIO()
        with patch.dict(os.environ, {"TOPVIEW_API_KEY": "", "TOPVIEW_UID": ""}), \
                patch.object(sys, "argv", ["x"]), contextlib.redirect_stdout(out):
            self.assertEqual(pm.main(), 0)
        self.assertIn("not configured", out.getvalue())


if __name__ == "__main__":
    unittest.main()
