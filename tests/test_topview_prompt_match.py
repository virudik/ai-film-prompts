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
# Any active single-prompt scene (retired scenes leave the master, so do not hard-code one).
SINGLE = next(l for l, b in BLOCKS if l.isdigit() and "Photoreal" in b and "@Image1" in b)


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
        self.assertIn("42 · Seedance 2.0 часть 1", labels)
        self.assertIn("42 · Seedance 2.0 часть 2", labels)
        # Two engine versions per scene since 19.10 (PROMPT-STYLE-GUIDE §7А): one 30 s text for Wan 3.0 /
        # Seedance 2.5 and Seedance 2.0 2 × 15 s; the separate Seedance 2.5 tabs are gone.
        self.assertIn("42", labels)
        self.assertNotIn("42 · Seedance 2.5", labels)
        self.assertFalse([l for l in labels if "Seedance 2.5" in l])
        self.assertIn("49 · Wan 3.0 часть 3", labels)
        self.assertIn("28 B10", labels)
        for suffix in "ABCDEF":
            self.assertIn("49" + suffix, labels)
        self.assertIn("50A", labels)
        self.assertIn("50B", labels)
        self.assertIn("51A", labels)
        self.assertIn("51B", labels)
        project = json.loads((ROOT / "project-status.json").read_text(encoding="utf-8"))
        self.assertEqual(project["health"], "ok")
        self.assertNotIn("20 · песня 13", labels)  # scene 20 is retired and permanently reserved
        # The status publisher runs asynchronously after a master commit. Test the
        # canonical master unconditionally, and compare status counts only when
        # its recorded master checksum proves it is from the same revision.
        self.assertEqual(len(labels), sum(line.startswith("```text") for line in MASTER.splitlines()))
        import hashlib
        if project.get("canonical_master_sha256") == hashlib.sha256(MASTER.encode("utf-8")).hexdigest():
            self.assertEqual(len(labels), project["prompt_texts"])

    def test_topview_flavoured_text_matches_normalized(self):
        label, body = next((l, b) for l, b in BLOCKS if l == SINGLE)
        topview = pm.re.sub(r"@Image(\d)", r"<<<Image\1>>>", body).replace("\n", "\r\n")
        got = pm.classify(topview, BLOCKS)
        self.assertEqual(got[:2], (SINGLE, "normalized"))

    def test_token_padding_around_dash_matches_normalized(self):
        # S36, 19.10.2026: Topview read back "@Image1–@Image3" as "<<<Image1>>> –<<<Image3>>>".
        self.assertEqual(pm.normalise("Priority: <<<Image1>>> –<<<Image3>>> identities"),
                         pm.normalise("Priority: @Image1–@Image3 identities"))
        self.assertEqual(pm.normalise("<<<Image1>>> — <<<Image2>>>"), pm.normalise("@Image1—@Image2"))
        self.assertNotEqual(pm.normalise("@Image1 – opening"), pm.normalise("@Image1– opening"))  # prose dashes untouched

    def test_small_edit_is_high_and_unrelated_text_is_low(self):
        label, body = next((l, b) for l, b in BLOCKS if l == SINGLE)
        edited = body.replace("Photoreal", "Photo-real", 1)
        self.assertEqual(pm.classify(edited, BLOCKS)[:2], (SINGLE, "high"))
        self.assertEqual(pm.classify("A cat walks along a wall.", BLOCKS)[1], "low")

    def test_slash_padding_only_between_reference_tokens(self):
        self.assertEqual(pm.normalise("<<<Image3>>> /<<<Image4>>> identities"),
                         pm.normalise("@Image3/@Image4 identities"))
        self.assertEqual(pm.normalise("@Video1 / @Audio2 / @Image3"),
                         pm.normalise("@Video1/@Audio2/@Image3"))
        for changed in ("@Image4/@Image3", "@Image3/@Image5", "@Image3–@Image4"):
            self.assertNotEqual(pm.normalise(changed), pm.normalise("@Image3/@Image4"))
        self.assertNotEqual(pm.normalise("left /right"), pm.normalise("left/right"))
        self.assertNotEqual(pm.normalise("@Image3 / helper"), pm.normalise("@Image3/helper"))

    def test_s58_submission_receipt_resolves_without_lowering_match_threshold(self):
        import robot_telemetry as rt
        receipt = json.loads((ROOT / "reports/topview-queue-2026-10-16/S58-SEED20-P1-20261023.json").read_text())
        prompt = receipt["parameters"]["positivePrompt"]
        label = "58 · Seedance 2.0 часть 1"
        # A real provider serialization previously blocked every telemetry publish.
        self.assertEqual(pm.classify(prompt, BLOCKS)[:2], (label, "normalized"))
        resolver = rt.make_resolver(lambda tid: (prompt, "Seedance 2.0"))
        self.assertEqual(resolver(receipt["task_id"], MASTER, {58})["label"], label)
        altered = prompt.replace("No explosion in this part.", "An explosion in this part.")
        self.assertIsNone(rt.make_resolver(lambda tid: (altered, "Seedance 2.0"))(receipt["task_id"], MASTER, {58}))
        self.assertIsNone(resolver(receipt["task_id"], MASTER, {57}))

    def test_main_prints_only_task_id_scene_and_confidence_and_uses_get_detail_only(self):
        fake = Fake({"a" * 32: dict(BLOCKS)[SINGLE]})
        out = io.StringIO()
        env = {"TOPVIEW_API_KEY": "secret-key-xyz", "TOPVIEW_UID": "uid-123"}
        with patch.dict(os.environ, env), patch.object(pm.scan, "Client", lambda k, u: fake), \
                contextlib.redirect_stdout(out):
            self.assertEqual(self._run("a" * 32), 0)
        text = out.getvalue()
        self.assertIn("a" * 32 + " -> Scene " + SINGLE + " · exact", text)
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
