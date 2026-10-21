import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import canon_health as ch  # noqa: E402

NOW = datetime(2026, 10, 18, 6, 0, tzinfo=timezone.utc)


def repo(d, handoff="## Сейчас 18.10.2026\nвсё хорошо\n", extra=None):
    root = Path(d)
    (root / "ops").mkdir()
    (root / "scripts").mkdir()
    (root / "scripts" / "x.py").write_text("", encoding="utf-8")
    for name in ch.DOCS:
        (root / name).write_text("см. `scripts/x.py`\n", encoding="utf-8")
    (root / "NEW-CHAT-HANDOFF.md").write_text(handoff, encoding="utf-8")
    (root / "ops" / "A.md").write_text("# A\n\nСтатус: действует. Проверено: 17.10.2026.\n", encoding="utf-8")
    (root / "project-status.json").write_text(json.dumps({"scene_ids": [40, 41], "health": "ok"}), encoding="utf-8")
    for rel, text in (extra or {}).items():
        (root / rel).write_text(text, encoding="utf-8")
    return root


def codes(res):
    return sorted(p["code"] for p in res["problems"])


class CanonHealthTests(unittest.TestCase):
    def test_clean_repo_is_ok(self):
        with tempfile.TemporaryDirectory() as d:
            res = ch.check(repo(d), NOW)
            self.assertEqual(res["status"], "ok", res["problems"])

    def test_stale_now_block_and_size(self):
        with tempfile.TemporaryDirectory() as d:
            res = ch.check(repo(d, handoff="## Сейчас 10.10.2026\n" + "x" * 36000), NOW)
            self.assertEqual(codes(res), ["handoff-now-stale", "handoff-size"])

    def test_now_date_comes_from_current_heading_not_preamble(self):
        with tempfile.TemporaryDirectory() as d:
            handoff = (
                "> Схема принята решением владельца 10.10.2026.\n\n"
                "## СЕЙЧАС (обновлено 18.10.2026, 09:00 МСК)\n"
                "Текущее состояние.\n"
            )
            res = ch.check(repo(d, handoff=handoff), NOW)
            self.assertNotIn("handoff-now-stale", codes(res))

    def test_broken_ref_but_not_removed_or_external(self):
        with tempfile.TemporaryDirectory() as d:
            root = repo(d, extra={"USER-GUIDE.md": "`scripts/gone.py`\nУбран `scripts/old.py`\n`CURRENT-STATE.md`\n`x.py`\n"})
            res = ch.check(root, NOW)
            self.assertEqual([p["text"] for p in res["problems"] if p["code"] == "broken-ref"],
                             ["USER-GUIDE.md ссылается на файл `scripts/gone.py`, которого нет в репозитории."])

    def test_ops_header_and_stuck_task_and_queue(self):
        with tempfile.TemporaryDirectory() as d:
            inbox = {"tasks": [{"id": "t", "status": "open", "to": "claude", "created_at": "2026-10-13T00:00:00Z", "text": "сделать"},
                               {"id": "u", "status": "done", "created_at": "2026-10-01T00:00:00Z"}]}
            queue = {"items": [{"scene_id": 24, "state": "blocked_owner_decision"}, {"scene_id": 25, "state": "submitted"},
                               {"scene_id": 41, "state": "waiting_for_slot"}]}
            root = repo(d, extra={"ops/B.md": "# B\nбез шапки\n", "ops/owner-tasks.json": json.dumps(inbox),
                                  "ops/topview-launch-queue.json": json.dumps(queue)})
            res = ch.check(root, NOW)
            self.assertEqual(codes(res), ["ops-unchecked", "queue-scene-gone", "task-stuck"])
            self.assertIn("24", next(p["text"] for p in res["problems"] if p["code"] == "queue-scene-gone"))

    def test_fail_only_on_new_warning(self):
        with tempfile.TemporaryDirectory() as d:
            root = repo(d, handoff="## 10.10.2026\n")
            self.assertEqual(ch.main([str(root), "--write", "--fail-on-new"]), 0)   # first run: no baseline
            self.assertEqual(ch.main([str(root), "--write", "--fail-on-new"]), 0)   # same problem again: quiet
            (root / "USER-GUIDE.md").write_text("`scripts/gone.py`\n", encoding="utf-8")
            self.assertEqual(ch.main([str(root), "--write", "--fail-on-new"]), 1)   # new problem: one e-mail
            self.assertEqual(ch.main([str(root), "--write", "--fail-on-new"]), 0)


if __name__ == "__main__":
    unittest.main()
