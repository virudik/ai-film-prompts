#!/usr/bin/env python3
"""Yandex Disk video links (26.11.2026): offline tests, no network, no rclone, no credentials."""
import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import yandex_video_links as yl  # noqa: E402

KEY = "https://yadi.sk/i/AbCdEf123456"


class Args:
    pass


class YandexLinksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        patcher = patch.object(yl, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_archive_path_is_per_project(self):
        self.assertEqual(yl.archive_path("seregius"), self.root / "topview-video-archive.json")
        self.assertEqual(yl.archive_path("kot-detektiv"), self.root / "projects/kot-detektiv/topview-video-archive.json")

    def test_import_any_project(self):
        man = self.root / "m.json"
        man.write_text(json.dumps({"videos": [
            {"project": "kotmonavty", "scene": 3, "yandex_public_key": KEY,
             "yandex_path": "Нейровидео/Котмонавты/S3_x_" + "a" * 32 + ".mp4"},
            {"project": "kotmonavty", "scene": "x", "yandex_public_key": KEY, "task_id": "b" * 32},
        ]}), encoding="utf-8")
        a = Args(); a.manifest = str(man); a.write = True
        with patch.object(yl, "public_meta", return_value={"type": "file", "size": 10, "md5": "m", "sha256": "s"}), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = yl.import_manifest(a)
        self.assertEqual(rc, 1)  # the second row has no scene number
        data = json.loads(yl.archive_path("kotmonavty").read_text(encoding="utf-8"))
        e = data["videos"]["a" * 32]
        self.assertEqual((e["project"], e["scene_id"], e["yandex_public_key"], e["size_bytes"]), ("kotmonavty", 3, KEY, 10))
        self.assertNotIn("b" * 32, data["videos"])

    def test_pages_keep_no_referrer_and_shared_player(self):
        meta = '<meta name="referrer" content="no-referrer">'
        for page in ("videos.html", "film.html"):
            self.assertIn(meta, (ROOT / page).read_text(encoding="utf-8"), page)
        vs = (ROOT / "video-source.js").read_text(encoding="utf-8")
        self.assertIn("cloud-api.yandex.net/v1/disk/public/resources/download?public_key=", vs)
        self.assertIn("functions/v1/drive-video?id=", vs)

    def test_archive_keys_are_yandex_public_links(self):
        data = json.loads((ROOT / "topview-video-archive.json").read_text(encoding="utf-8"))
        for tid, e in data["videos"].items():
            if e.get("yandex_public_key"):
                self.assertTrue(yl.KEY_RE.match(e["yandex_public_key"]), tid)
                self.assertTrue(e.get("yandex_path"), tid)
                self.assertEqual(e.get("project"), "seregius", tid)


if __name__ == "__main__":
    unittest.main()
