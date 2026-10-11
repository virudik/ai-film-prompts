#!/usr/bin/env python3
"""Drive copy refresh (keyless): offline tests with an in-memory Drive. No network, no credentials."""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import drive_write as dw  # noqa: E402

FOLDER = dw.ALLOWED_PARENT


class Resp:
    def __init__(self, status=200, body=None, content=b""):
        self.status_code, self._body, self.content = status, body, content

    def json(self):
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeDrive:
    """files: id -> {name, parents, mime, data}. Records every write."""

    def __init__(self, files, corrupt_uploads=False):
        self.files, self.writes, self.corrupt = files, [], corrupt_uploads

    def get(self, url, params=None):
        params = params or {}
        if url.endswith("/files"):
            q = params["q"]
            name = q.split("name = '")[1].split("'")[0]
            hits = [{"id": i, "name": f["name"], "parents": f["parents"]} for i, f in self.files.items()
                    if f["name"] == name and FOLDER in f["parents"]]
            return Resp(body={"files": hits})
        fid = url.rsplit("/", 1)[1]
        f = self.files.get(fid)
        if f is None:
            return Resp(404)
        if params.get("alt") == "media":
            return Resp(content=f["data"])
        return Resp(body={"id": fid, "name": f["name"], "parents": f["parents"], "mimeType": f["mime"],
                          "modifiedTime": "2026-10-10T20:00:00.000Z"})

    def patch(self, url, params=None, data=None, headers=None):
        fid = url.rsplit("/", 1)[1]
        self.writes.append(fid)
        self.files[fid]["data"] = (data + b"!") if self.corrupt else data
        return Resp(body={"id": fid, "modifiedTime": "2026-10-11T08:00:00.000Z"})


def git(cwd, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=cwd, check=True,
                          text=True, capture_output=True)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        info = json.loads((ROOT / "instruction-sync-status.json").read_text(encoding="utf-8"))
        self.ids = {n: info["files"][n]["drive_file_id"] for n in dw.INSTRUCTIONS}
        self.ids["video-prompts.md"] = dw.KNOWN_IDS["video-prompts.md"]
        self.ids["film-backlog.md"] = dw.KNOWN_IDS["film-backlog.md"]
        self.ids["film-analysis.md"] = "ANALYSIS-ID"
        self.old, self.new = {}, {}
        for n in dw.COPY_FILES:
            self.old[n], self.new[n] = f"{n} old\n".encode(), f"{n} new\n".encode()
            (self.repo / n).write_bytes(self.old[n])
        shutil.copy(ROOT / "instruction-sync-status.json", self.repo / "instruction-sync-status.json")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", "v1")
        for n in dw.COPY_FILES:                       # main moves on: Drive copies are now stale
            (self.repo / n).write_bytes(self.new[n])
        git(self.repo, "commit", "-qam", "v2")
        self.files = {self.ids[n]: {"name": n, "parents": [FOLDER], "mime": "text/markdown", "data": self.old[n]}
                      for n in dw.COPY_FILES}

    def tearDown(self):
        self.tmp.cleanup()

    def run_sync(self, drive, **kw):
        copy_dir = Path(self.tmp.name) / "copies"
        res = dw.sync_copies(drive, self.repo, copy_dir=copy_dir, sleep=lambda s: None, **kw)
        return {r["name"]: r for r in res}, copy_dir


class SyncTests(Base):
    def test_stale_copies_are_refreshed_with_exact_bytes_and_read_back(self):
        drive = FakeDrive(self.files)
        res, copy_dir = self.run_sync(drive)
        self.assertEqual({r["status"] for r in res.values()}, {"written"})
        for n in dw.COPY_FILES:
            self.assertEqual(self.files[self.ids[n]]["data"], self.new[n])
            self.assertEqual(res[n]["drive_sha256"], res[n]["github_sha256"])
        self.assertEqual(sorted(p.name for p in copy_dir.iterdir()), sorted(dw.INSTRUCTIONS))
        self.assertEqual((copy_dir / "SYNC-RUNBOOK.md").read_bytes(), self.new["SYNC-RUNBOOK.md"])
        self.assertEqual(len(drive.writes), len(dw.COPY_FILES))
        self.assertIn(self.ids["film-analysis.md"], drive.writes)        # resolved by name, then same-ID update

    def test_equal_sha_means_no_write(self):
        for n in dw.COPY_FILES:
            self.files[self.ids[n]]["data"] = self.new[n]
        drive = FakeDrive(self.files)
        res, _ = self.run_sync(drive)
        self.assertEqual({r["status"] for r in res.values()}, {"current"})
        self.assertEqual(drive.writes, [])

    def test_hand_edited_drive_file_is_never_overwritten(self):
        self.files[self.ids["USER-GUIDE.md"]]["data"] = b"someone typed this on Drive\n"
        drive = FakeDrive(self.files)
        res, _ = self.run_sync(drive)
        self.assertEqual(res["USER-GUIDE.md"]["status"], "drift")
        self.assertEqual(self.files[self.ids["USER-GUIDE.md"]]["data"], b"someone typed this on Drive\n")
        self.assertNotIn(self.ids["USER-GUIDE.md"], drive.writes)
        self.assertEqual(res["SYNC-RUNBOOK.md"]["status"], "written")      # the others still refresh

    def test_bom_variant_of_a_past_version_counts_as_stale_not_drift(self):
        self.files[self.ids["SYNC-RUNBOOK.md"]]["data"] = b"\xef\xbb\xbf" + self.old["SYNC-RUNBOOK.md"]
        res, _ = self.run_sync(FakeDrive(self.files))
        self.assertEqual(res["SYNC-RUNBOOK.md"]["status"], "written")

    def test_probe_never_writes(self):
        drive = FakeDrive(self.files)
        res, copy_dir = self.run_sync(drive, dry_run=True)
        self.assertEqual({r["status"] for r in res.values()}, {"would_write"})
        self.assertEqual(drive.writes, [])
        self.assertFalse(copy_dir.exists())

    def test_readback_mismatch_is_an_error(self):
        res, copy_dir = self.run_sync(FakeDrive(self.files, corrupt_uploads=True))
        self.assertEqual(res["video-prompts.md"]["status"], "error")
        self.assertFalse((copy_dir / "SYNC-RUNBOOK.md").exists())          # unverified bytes never reach the cert

    def test_wrong_folder_or_name_is_rejected_and_ambiguous_name_not_guessed(self):
        self.files[self.ids["video-prompts.md"]]["parents"] = ["somewhere-else"]
        self.files["DUP"] = {"name": "film-analysis.md", "parents": [FOLDER], "mime": "text/markdown", "data": b"x"}
        drive = FakeDrive(self.files)
        res, _ = self.run_sync(drive)
        self.assertEqual(res["video-prompts.md"]["status"], "rejected")
        self.assertEqual(res["film-analysis.md"]["status"], "skipped")      # two hits: not guessing, not creating
        self.assertNotIn(self.ids["video-prompts.md"], drive.writes)
        self.assertNotIn("DUP", drive.writes)
        self.assertNotIn(self.ids["film-analysis.md"], drive.writes)


class ModeTests(Base):
    def run_main(self, args, env):
        cwd = os.getcwd()
        os.chdir(self.repo)
        try:
            buf = io.StringIO()
            with patch.dict(os.environ, env, clear=False), contextlib.redirect_stdout(buf):
                rc = dw.main(["drive_write.py", *args])
            return rc, buf.getvalue()
        finally:
            os.chdir(cwd)

    def test_without_credentials_every_mode_is_a_clean_noop(self):
        env = {"GOOGLE_APPLICATION_CREDENTIALS": ""}
        for mode in ("sync", "probe"):
            rc, out = self.run_main([mode], env)
            self.assertEqual(rc, 0)
            self.assertIn("not_configured", out)
        self.assertFalse((self.repo / "drive-write-results").exists())
        (self.repo / "drive-write-requests").mkdir()
        (self.repo / "drive-write-requests" / "r.json").write_text("{}")
        rc, out = self.run_main(["requests"], env)
        self.assertEqual(rc, 0)
        self.assertIn("not_configured", out)
        self.assertTrue((self.repo / "drive-write-requests" / "r.json").exists())     # untouched

    def test_no_key_file_path_remains(self):
        src = (ROOT / "scripts" / "drive_write.py").read_text(encoding="utf-8")
        self.assertNotIn("GDRIVE_SA_KEY", src)
        self.assertNotIn("service_account.Credentials", src)
        wf = (ROOT / ".github" / "workflows" / "drive-write.yml").read_text(encoding="utf-8")
        self.assertNotIn("GDRIVE_SA_KEY", wf)
        self.assertIn("google-github-actions/auth@v2", wf)
        self.assertIn("id-token: write", wf)
        self.assertIn("GCP_WORKLOAD_IDENTITY_PROVIDER", wf)

    def test_sync_through_main_writes_summary_and_certificate_input(self):
        drive = FakeDrive(self.files)
        copy_dir = Path(self.tmp.name) / "copies"
        with patch.object(dw, "session", return_value=drive):
            rc, out = self.run_main(["sync"], {"DRIVE_COPY_DIR": str(copy_dir)})
        self.assertEqual(rc, 0, out)
        summary = json.loads((self.repo / "drive-write-results" / "copy-sync.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["summary"], {"written": len(dw.COPY_FILES)})
        # the instruction certificate accepts the verified copies (drive_copy_match true)
        shutil.copy(ROOT / "scripts" / "cert_github.py", self.repo / "cert_github.py")
        subprocess.run([sys.executable, "cert_github.py", ".", "--drive-copy-dir", str(copy_dir)], cwd=self.repo,
                       check=True, capture_output=True)
        cert = json.loads((self.repo / "instruction-sync-status.json").read_text(encoding="utf-8"))
        self.assertTrue(all(cert["files"][n]["drive_copy_match"] for n in dw.INSTRUCTIONS))


if __name__ == "__main__":
    unittest.main()
