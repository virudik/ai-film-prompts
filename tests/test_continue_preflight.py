import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("resume", "scripts/continue_preflight.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ContinuePreflightTests(unittest.TestCase):
    def test_missing_files_always_fall_back(self):
        with tempfile.TemporaryDirectory() as d:
            x = m.evaluate(Path(d))
            self.assertEqual(x["mode"], "full")
            self.assertFalse(x["ready_for_short"])

    def test_broken_certificate_never_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for name, obj in {
                "shadow/takeover-brief.json": {"generator": "d7-1.0", "valid_at_generation": True,
                    "invariants": [{"anchor_ok": True}] * 15, "sources": []},
                "project-status.json": {"health": "ok"},
                "instruction-sync-status.json": {"health": "ok", "source_of_truth": "github"},
                "monitor-role.json": {"primary": "robot"},
                "work-resume-register.json": {"schema_version": 1, "active_work": []},
            }.items():
                (p / name).parent.mkdir(parents=True, exist_ok=True)
                (p / name).write_text(json.dumps(obj))
            self.assertEqual(m.evaluate(p)["mode"], "full")


if __name__ == "__main__":
    unittest.main()
