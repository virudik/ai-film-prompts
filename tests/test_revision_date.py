#!/usr/bin/env python3
"""A changed master must advance revision even when previous_master_file is current."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_project_status import resolve_revision_date, revision_fingerprint_sha256


class RevisionDateTests(unittest.TestCase):
    def test_previous_status_wins_over_current_master_copy(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "s.json").write_text(json.dumps({"canonical_revision_sha256": "old",
                                                   "revision_date": "13.10.2026"}))
            (p / "master.md").write_text("Changed creative scene", encoding="utf-8")
            new = revision_fingerprint_sha256((p / "master.md").read_text())
            date = resolve_revision_date(new, None, "2026-10-14T00:15:00Z",
                                         p / "s.json", p / "master.md", "Europe/Moscow")
            self.assertEqual(date, "14.10.2026")

    def test_same_status_hash_preserves_date(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "s.json").write_text(json.dumps({"canonical_revision_sha256": "same",
                                                   "revision_date": "13.10.2026"}))
            self.assertEqual(resolve_revision_date("same", None, "2026-10-14T00:15:00Z",
                                                    p / "s.json", None, "Europe/Moscow"), "13.10.2026")


if __name__ == "__main__":
    unittest.main()
