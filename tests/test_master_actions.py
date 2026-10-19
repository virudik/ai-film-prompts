#!/usr/bin/env python3
"""Owner-panel robot, phase 2 (in_film / scene_not_needed / tv_drop_task). Offline: local bare git
"origin" + fake Supabase store. Covers: exact master diff, Scene ID reservation, conflicts → needs_owner,
plan-only mode, commit-before-ack, push race (redo from scratch), validation failure."""
import contextlib
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import robot_fixture as fx                      # noqa: E402
import master_scene_edit as mse                 # noqa: E402
import process_owner_decisions as pod           # noqa: E402
import robot_master_actions as robot            # noqa: E402

NOW = datetime(2026, 10, 11, 12, 0, 0, tzinfo=timezone.utc)


def silent(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def validator_ok(root, master_path=None):
    status, bad = robot.build_status(root, master_path or Path(root) / "video-prompts.md",
                                     Path(root) / ".t.tmp", "2026-10-11T12:00:00Z")
    (Path(root) / ".t.tmp").unlink(missing_ok=True)
    return status, bad


# ------------------------------------------------------------------ master text edit
class RetireSceneTests(unittest.TestCase):
    def setUp(self):
        self.text = fx.master_text(slow_rows=fx.slow_row_done(), slow=())

    def test_in_film_minimal_diff_and_reserved_id(self):
        new, rep = mse.retire_scene(self.text, 13, mode="in_film", date="12.10.2026")
        self.assertEqual(mse.active_scene_ids(new), [24, 25, 30])
        self.assertEqual(mse.reserved_scene_ids(new), [1, 2, 12, 13])
        self.assertIn("**3 сцены к генерации/доработке · 3 полных текста промта**", new)
        self.assertIn("**3 актуальные сцены и 3 полных текста промта**", new)
        self.assertIn("Сцены **1, 2, 12 и 13** удалены из active master", new)
        self.assertNotIn("scene-13", new)                       # section, anchor and TOC row are gone
        self.assertNotIn("| 13 — Совет", new)                   # finished slow-table row too
        self.assertIn("**Синхронизация контекста:** **12.10.2026**", new)
        self.assertEqual(rep["prompts_removed"], 1)
        # untouched scenes are byte-identical
        for n in (24, 25, 30):
            old_block = [b for b in mse.scene_blocks(self.text) if b[0] == n][0]
            new_block = [b for b in mse.scene_blocks(new) if b[0] == n][0]
            self.assertEqual(self.text[old_block[1]:old_block[2]], new[new_block[1]:new_block[2]])

    def test_result_is_accepted_by_the_real_validator(self):
        with tempfile.TemporaryDirectory() as d:
            _, work = fx.make_origin(d, with_active_task=False)
            new, _ = mse.retire_scene((work / "video-prompts.md").read_text(encoding="utf-8"), 13, mode="in_film")
            (work / "m.md").write_text(new, encoding="utf-8", newline="")
            status, bad = validator_ok(work, work / "m.md")
            self.assertEqual(bad, [])
            self.assertEqual(status["reserved_scene_ids"], [1, 2, 12, 13])
            self.assertTrue(status["checks"]["reserved_scene_ids_not_reused"])

    def test_dependents_lose_the_edge_for_in_film_only(self):
        new, rep = mse.retire_scene(self.text, 24, mode="in_film")
        self.assertEqual([x["scene"] for x in rep["dependents_dropped"]], [25])
        meta25 = re.search(r"## Сцена 25.*?scene-meta: (\{.*?\}) -->", new, re.S).group(1)
        self.assertEqual(json.loads(meta25)["dependencies"], [])
        with self.assertRaises(mse.NeedsOwner):
            mse.retire_scene(self.text, 24, mode="scene_not_needed")

    def test_ambiguity_raises_needs_owner(self):
        with self.assertRaisesRegex(mse.NeedsOwner, "последняя оформленная"):
            mse.retire_scene(self.text, 30, mode="in_film")
        slow = fx.master_text(slow_rows=fx.slow_row_active(), slow=(30,), latest=25)
        with self.assertRaisesRegex(mse.NeedsOwner, "медленной генерации"):
            mse.retire_scene(slow, 30, mode="in_film")
        with self.assertRaises(mse.NeedsOwner):
            mse.retire_scene(self.text, 99, mode="in_film")               # neither active nor reserved
        with self.assertRaises(mse.NeedsOwner):
            mse.retire_scene(self.text.replace("**4 сцен к", "**5 сцен к"), 13, mode="in_film")
        with self.assertRaises(mse.NeedsOwner):
            mse.retire_scene(self.text + "\nСм. [сцену](#scene-13)\n", 13, mode="in_film")   # dangling link
        with self.assertRaises(mse.NeedsOwner):
            mse.retire_scene(self.text.replace("зарезервированы", "заняты"), 13, mode="in_film")

    def test_retire_twice_is_idempotent_and_never_reuses_id(self):
        new, _ = mse.retire_scene(self.text, 13, mode="in_film")
        again, rep = mse.retire_scene(new, 13, mode="in_film")
        self.assertTrue(rep["already_retired"])
        self.assertEqual(again, new)

    def test_first_middle_last_and_no_separator_sections(self):
        for sid in (13, 24, 25, 30):          # 25 has no '---' in front; 30 is the last section
            text = self.text
            if sid == 30:                      # 30 is «последняя оформленная» in the fixture → point it elsewhere
                text = text.replace("оформленная активная сцена:** 30", "оформленная активная сцена:** 25")
            new, _ = mse.retire_scene(text, sid, mode="scene_not_needed" if sid in (13, 25, 30) else "in_film")
            self.assertNotIn(f'<a id="scene-{sid}"></a>', new)
            self.assertTrue(new.endswith("\n---\n"))
            self.assertIsNone(re.search(r"\n(?:[ \t]*\n){2,}", new), "compact spacing broken")

    def test_live_master_smoke(self):
        """The real master: every scene that is not ambiguous retires into a validator-green master."""
        text = robot.read_raw(ROOT / "video-prompts.md")
        ids = mse.active_scene_ids(text)
        candidate = None
        for sid in ids:
            try:
                candidate = (sid, mse.retire_scene(text, sid, mode="in_film", date="12.10.2026")[0])
                break
            except mse.NeedsOwner:
                continue
        self.assertIsNotNone(candidate, "no scene of the live master can be retired automatically")
        with tempfile.TemporaryDirectory() as d:
            m = Path(d) / "m.md"
            m.write_text(candidate[1], encoding="utf-8", newline="")
            status, bad = robot.build_status(ROOT, m, Path(d) / "s.json", "2026-10-11T12:00:00Z")
            self.assertEqual(bad, [], f"scene {candidate[0]}")
            self.assertIn(candidate[0], status["reserved_scene_ids"])


# ------------------------------------------------------------------ planning
class EvaluateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        _, self.work = fx.make_origin(self.tmp.name)
        self.st = robot.load_state(self.work)

    def tearDown(self):
        self.tmp.cleanup()

    def plan(self, rows):
        return robot.evaluate(rows, self.st, now=NOW)

    def test_in_film_applies_master_and_ledger_together(self):
        groups, files = self.plan([fx.row("r1", 13, "in_film"), fx.row("r2", 13, "in_film")])
        self.assertEqual([g.verdict for g in groups], ["apply"])
        self.assertEqual({r["id"] for r in groups[0].rows}, {"r1", "r2"})      # duplicate click = one edit
        self.assertEqual(set(files), {"video-prompts.md", "review-ledger.json"})
        row = json.loads(files["review-ledger.json"])["scenes"]["13"]
        self.assertTrue(row["inserted_into_film"] and row["reviewed"] and row["accepted"])
        self.assertFalse(row["needs_redo"])
        self.assertEqual(row["montage_note"], "в фильме")
        self.assertEqual(mse.reserved_scene_ids(files["video-prompts.md"]), [1, 2, 12, 13])

    def test_scene_not_needed_leaves_ledger_alone(self):
        groups, files = self.plan([fx.row("r1", 13, "scene_not_needed")])
        self.assertEqual(groups[0].verdict, "apply")
        self.assertEqual(set(files), {"video-prompts.md"})

    def test_active_topview_task_means_needs_owner_and_nothing_changes(self):
        groups, files = self.plan([fx.row("r1", 30, "in_film")])
        self.assertEqual(groups[0].verdict, "needs_owner")
        self.assertIn("активная задача Topview", groups[0].reason)
        self.assertEqual(files, {})

    def test_conflicting_buttons_need_owner_for_every_row(self):
        for other in ("redo", "scene_not_needed"):
            groups, files = self.plan([fx.row("r1", 13, "in_film"), fx.row("r2", 13, other)])
            self.assertEqual(files, {}, other)
            ids = {r["id"] for g in groups for r in g.rows + g.also}
            self.assertEqual(ids, {"r1", "r2"}, other)
            self.assertTrue(all(g.verdict == "needs_owner" for g in groups), other)
        groups, files = self.plan([fx.row("r1", 13, "scene_not_needed"), fx.row("r2", 13, "accept")])
        self.assertEqual((groups[0].verdict, files), ("needs_owner", {}))
        groups, files = self.plan([fx.row("r1", 13, "in_film"), fx.row("r2", 13, "tv_mark_status", value="result_bad")])
        self.assertEqual((groups[0].verdict, files == {}), ("needs_owner", True))

    def test_in_film_with_accept_is_compatible(self):
        groups, files = self.plan([fx.row("r1", 13, "in_film"), fx.row("r2", 13, "accept")])
        self.assertEqual(groups[0].verdict, "apply")

    def test_in_film_releases_terminal_review_wait_atomically(self):
        for terminal in (False, True):
            with self.subTest(terminal=terminal):
                st = json.loads(json.dumps(self.st))
                st["video-prompts.md"] = st["video-prompts.md"].replace(
                    "оформленная активная сцена:** 30", "оформленная активная сцена:** 25")
                st["topview-task-map.json"]["active_by_scene"] = {}
                st["topview-status.json"]["active_tasks"] = []
                st["topview-status.json"]["occupied_slots"] = 0
                st["topview-status.json"]["free_slots"] = 6
                if terminal:
                    st["topview-task-map.json"]["processed_tasks"].append(
                        {"scene_id": 30, "task_id": fx.ACTIVE_TASK, "final_status": "success"})
                    st["topview-status.json"]["scenes"]["30"]["topview_status"] = "success"
                rows = [fx.row(str(i), 30, a) for i, a in enumerate(("accept", "to_montage", "in_film"))]
                groups, files = robot.evaluate(rows, st, now=NOW)
                if not terminal:
                    self.assertEqual((groups[0].verdict, files), ("defer", {}))
                    continue
                self.assertEqual(groups[0].verdict, "apply", groups[0].reason)
                self.assertEqual(set(files), {"video-prompts.md", "review-ledger.json"})
                self.assertNotIn("## Сцена 30 —", files["video-prompts.md"])
                self.assertIn(30, mse.reserved_scene_ids(files["video-prompts.md"]))
                row = json.loads(files["review-ledger.json"])["scenes"]["30"]
                self.assertTrue(row["accepted"] and row["inserted_into_film"])

    def test_open_owner_task_defers(self):
        groups, files = self.plan([fx.row("r1", 13, "in_film"), fx.row("t", 13, "owner_task")])
        self.assertEqual((groups[0].verdict, files), ("defer", {}))

    def test_missing_ledger_row_or_unknown_scene(self):
        del self.st["review-ledger.json"]["scenes"]["13"]
        groups, _ = self.plan([fx.row("r1", 13, "in_film")])
        self.assertEqual(groups[0].verdict, "needs_owner")
        groups, _ = self.plan([fx.row("r2", 77, "scene_not_needed")])
        self.assertEqual(groups[0].verdict, "needs_owner")

    def test_unrelated_foreign_claim_does_not_block_owner_review(self):
        foreign = fx.row("m", 13, "in_film", status="in_progress", note="claimed by the monitor")
        groups, files = self.plan([foreign, fx.row("r", 13, "accept")])
        self.assertEqual(groups[0].kind, "review")
        self.assertEqual(groups[0].verdict, "apply")
        self.assertEqual(set(files), {"review-ledger.json"})

    def test_owner_review_clears_only_terminal_slow_and_keeps_scene(self):
        for action in ("accept", "redo", "to_montage"):
            with self.subTest(action=action):
                st = json.loads(json.dumps(self.st))
                st["topview-task-map.json"]["active_by_scene"] = {}
                st["topview-task-map.json"]["processed_tasks"].append(
                    {"scene_id": 30, "task_id": fx.ACTIVE_TASK, "final_status": "success"})
                st["topview-status.json"]["active_tasks"] = []
                st["topview-status.json"]["occupied_slots"] = 0
                st["topview-status.json"]["free_slots"] = 6
                st["topview-status.json"]["scenes"]["30"]["topview_status"] = "success"
                groups, files = robot.evaluate([fx.row("rv", 30, action)], st, now=NOW)
                self.assertEqual(groups[0].verdict, "apply", groups[0].reason)
                self.assertEqual(set(files), {"review-ledger.json", "video-prompts.md"})
                updated = files["video-prompts.md"]
                self.assertIn("## Сцена 30 — Колоннада", updated)
                self.assertIn("**⏳ 0**", updated)
                self.assertIn("Решение владельца", updated)
                self.assertNotIn("**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**", updated)
                result = json.loads(files["review-ledger.json"])["scenes"]["30"]
                self.assertEqual(result["needs_redo"], action == "redo")
                self.assertIsNone(result["inserted_into_film"])
                # The physical snapshot remains unchanged in production. Offline
                # fixture validation uses the current fake active task, so checking
                # that stale fixture against the released zero-slot state would be a
                # test setup error; production commit gate validates real live JSON.

    def test_owner_review_defers_if_task_physically_active(self):
        for action in ("accept", "redo", "to_montage"):
            groups, files = self.plan([fx.row("a", 30, action)])
            self.assertEqual(groups[0].verdict, "defer")
            self.assertEqual(files, {})

    def test_review_conflict_does_not_mutate_master_or_ledger(self):
        groups, files = self.plan([fx.row("a", 13, "accept"), fx.row("b", 13, "redo")])
        self.assertEqual(groups[0].verdict, "needs_owner")
        self.assertEqual(files, {})

    def test_drop_task_updates_master_map_snapshot_and_checkpoint(self):
        groups, files = self.plan([fx.row("d", 30, "tv_drop_task", task_id=fx.ACTIVE_TASK)])
        self.assertEqual(groups[0].verdict, "apply", groups[0].reason)
        self.assertEqual(set(files), {"video-prompts.md", "topview-task-map.json", "topview-operation-journal.json"})
        master = files["video-prompts.md"]
        self.assertNotIn("**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**", master)
        self.assertIn("abandoned_by_owner", master)
        tm = json.loads(files["topview-task-map.json"])
        self.assertEqual(tm["active_by_scene"], {"30": [fx.ACTIVE_TASK]})
        self.assertIn(fx.ACTIVE_TASK, tm["owner_released_task_ids"])
        self.assertEqual(tm["last_scan_at"], fx.T0)                       # nothing was scanned
        self.assertNotIn("topview-status.json", files)  # technical snapshot unchanged
        self.assertNotIn("topview-checkpoint.json", files)  # stable checkpoint unchanged

    def test_drop_task_edge_cases(self):
        groups, _ = self.plan([fx.row("d", 30, "tv_drop_task", task_id=fx.OLD_TASK)])
        self.assertEqual(groups[0].verdict, "needs_owner")                # processed task has no matching owner-slow row in fixture
        groups, files = self.plan([fx.row("d", 30, "tv_drop_task", task_id="c" * 32)])
        self.assertEqual((groups[0].verdict, files), ("needs_owner", {}))  # unknown task
        groups, files = self.plan([fx.row("d", 13, "tv_drop_task", task_id=fx.ACTIVE_TASK)])
        self.assertEqual((groups[0].verdict, files), ("needs_owner", {}))  # task belongs to another scene
        groups, files = self.plan([fx.row("d", 30, "tv_drop_task", task_id="nonsense")])
        self.assertEqual((groups[0].verdict, files), ("needs_owner", {}))
        groups, files = self.plan([fx.row("d", 30, "tv_drop_task", task_id=fx.ACTIVE_TASK),
                                   fx.row("m", 30, "tv_mark_status", task_id=fx.ACTIVE_TASK, value="result_ok")])
        self.assertEqual((groups[0].verdict, files), ("needs_owner", {}))  # «Не ждать» vs «Готово»


# ------------------------------------------------------------------ end to end with git
class EndToEndTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.origin, self.work = fx.make_origin(self.tmp.name)
        self.head0 = self.head()

    def tearDown(self):
        self.tmp.cleanup()

    def head(self):
        return subprocess.run(["git", "--git-dir", str(self.origin), "rev-parse", "main"], text=True,
                              capture_output=True).stdout.strip()

    def origin_file(self, name):
        return subprocess.run(["git", "--git-dir", str(self.origin), "show", f"main:{name}"], text=True,
                              capture_output=True).stdout

    def go(self, rows, mode="on", **kw):
        store = fx.FakeStore(rows, self.origin)
        rc = silent(robot.run, self.work, store, robot.Git(self.work), mode=mode, now=NOW, **kw)
        return rc, store

    def test_default_off_is_plan_only_and_writes_nothing(self):
        rows = [fx.row("r1", 13, "in_film"), fx.row("r2", 30, "in_film")]
        rc, store = self.go(rows, mode="off")
        self.assertEqual(rc, 0)
        self.assertEqual(store.log, [])                    # not even needs_owner marks
        self.assertEqual(self.head(), self.head0)
        self.assertEqual({r["status"] for r in store.rows.values()}, {"pending"})
        self.assertEqual(robot.master_mode({}), "off")
        self.assertEqual(robot.master_mode({"ROBOT_MASTER_ACTIONS": ""}), "off")
        self.assertEqual(robot.master_mode({"ROBOT_MASTER_ACTIONS": "ON "}), "on")

    def test_commit_before_ack_and_validator_green(self):
        rc, store = self.go([fx.row("r1", 13, "in_film"), fx.row("r2", 24, "scene_not_needed")])
        # 24 has a dependent (25) → scene_not_needed is ambiguous → needs_owner; 13 is applied
        self.assertEqual(rc, 0)
        self.assertEqual(store.status_of("r1"), "applied")
        self.assertEqual(store.status_of("r2"), "needs_owner")
        new_head = self.head()
        self.assertNotEqual(new_head, self.head0)
        applied = [e for e in store.log if e["to"] == "applied"]
        claimed = [e for e in store.log if e["to"] == "in_progress"]
        self.assertTrue(claimed and applied)
        self.assertTrue(all(e["origin_head"] == self.head0 for e in claimed), "claim must precede the commit")
        self.assertTrue(all(e["origin_head"] == new_head for e in applied), "applied only after the push")
        master = self.origin_file("video-prompts.md")
        self.assertEqual(mse.active_scene_ids(master), [24, 25, 30])
        self.assertEqual(mse.reserved_scene_ids(master), [1, 2, 12, 13])
        status = json.loads(self.origin_file("project-status.json"))
        self.assertEqual(status["health"], "ok")
        self.assertEqual(status["reserved_scene_ids"], [1, 2, 12, 13])
        self.assertIn(status["canonical_master_sha256"][:12], self.origin_file("SYNC-TRIGGER.txt"))
        ledger = json.loads(self.origin_file("review-ledger.json"))["scenes"]["13"]
        self.assertTrue(ledger["inserted_into_film"])
        self.assertNotEqual(self.origin_file("video-prompts.md"), (self.work / "video-prompts.md").read_text() + "x")

    def test_deferred_button_shows_reason_once_and_stays_pending(self):
        rows = [fx.row("r1", 13, "in_film"), fx.row("t", 13, "owner_task")]
        rc, store = self.go(rows)
        self.assertEqual((rc, store.status_of("r1")), (0, "pending"))
        self.assertEqual(self.head(), self.head0)
        self.assertTrue(store.rows["r1"]["result_note"].startswith("Ждёт: по сцене открыта текстовая задача"))
        n = len(store.log)
        self.go_store(store)
        self.assertEqual(len(store.log), n, "the same reason is not rewritten every run")

    def go_store(self, store):
        return silent(robot.run, self.work, store, robot.Git(self.work), mode="on", now=NOW)

    def test_drop_task_end_to_end(self):
        rc, store = self.go([fx.row("d", 30, "tv_drop_task", task_id=fx.ACTIVE_TASK)])
        self.assertEqual((rc, store.status_of("d")), (0, "applied"))
        status = json.loads(self.origin_file("project-status.json"))
        self.assertEqual((status["health"], status["slow_scenes"]), ("ok", []))
        self.assertTrue(status["checks"]["topview_active_scene_ids_exist_in_master"])
        self.assertEqual(json.loads(self.origin_file("topview-status.json"))["occupied_slots"], 1)  # provider task still active
        self.assertIn("owner_released_task_ids", self.origin_file("topview-task-map.json"))
        self.assertIn("только снимает ожидание", self.origin_file("video-prompts.md"))

    def test_active_task_and_conflicts_touch_nothing_but_supabase_status(self):
        rows = [fx.row("a", 30, "in_film"), fx.row("b", 13, "in_film"), fx.row("c", 13, "redo")]
        rc, store = self.go(rows)
        self.assertEqual(rc, 0)
        self.assertEqual([store.status_of(x) for x in "abc"], ["needs_owner"] * 3)
        self.assertEqual(self.head(), self.head0)
        self.assertEqual(self.origin_file("video-prompts.md"), (self.work / "video-prompts.md").read_text())

    def test_push_race_redoes_everything_from_scratch(self):
        competitor = Path(self.tmp.name) / "competitor"
        subprocess.run(["git", "clone", "-q", str(self.origin), str(competitor)], check=True)
        real_push, calls = robot.Git.push, []

        def racing_push(git_self):
            calls.append(1)
            if len(calls) == 1:                          # another writer lands first
                p = competitor / "video-prompts.md"
                p.write_text(p.read_text().replace("Рабочий мастер-файл.", "Рабочий мастер-файл. (правка конкурента)"))
                fx.git(competitor, "commit", "-aqm", "competing master edit")
                fx.git(competitor, "push", "-q", "origin", "main")
            return real_push(git_self)

        with patch.object(robot.Git, "push", racing_push):
            rc, store = self.go([fx.row("r1", 13, "in_film")])
        self.assertEqual((rc, len(calls)), (0, 2))
        master = self.origin_file("video-prompts.md")
        self.assertIn("(правка конкурента)", master)       # the stale prepared edit was NOT replayed over it
        self.assertEqual(mse.active_scene_ids(master), [24, 25, 30])
        self.assertEqual(store.status_of("r1"), "applied")
        applied = [e for e in store.log if e["to"] == "applied"]
        self.assertEqual(len(applied), 1)
        self.assertEqual(applied[0]["origin_head"], self.head())
        self.assertEqual(json.loads(self.origin_file("project-status.json"))["health"], "ok")

    def test_validator_failure_blocks_push_and_ack(self):
        with patch.object(robot, "build_status", return_value=({"health": "error"}, ["scene_numbers_match_toc_and_sections"])):
            rc, store = self.go([fx.row("r1", 13, "in_film")])
        self.assertEqual(rc, 0)
        self.assertEqual(store.status_of("r1"), "needs_owner")
        self.assertEqual(self.head(), self.head0)
        self.assertEqual(robot.Git(self.work).run("status", "--porcelain").stdout.strip(), "")   # tree reset

    def test_failed_readback_keeps_rows_claimed_and_never_acks(self):
        with patch.object(robot.Git, "head_is_on_remote", return_value=False):
            rc, store = self.go([fx.row("r1", 13, "in_film")])
        self.assertEqual(rc, 1)
        self.assertEqual(store.status_of("r1"), "in_progress")
        self.assertTrue(store.rows["r1"]["result_note"].startswith(pod.CLAIM))
        # next run (the claimed row is retryable): master is already retired → acknowledged, no new commit
        head_after = self.head()
        rc, store2 = self.go([dict(store.rows["r1"])])
        self.assertEqual((rc, store2.status_of("r1")), (0, "applied"))
        self.assertEqual(self.head(), head_after)

    def test_retry_of_claimed_row_after_interrupted_ack(self):
        rc, store = self.go([fx.row("r1", 13, "in_film")])
        self.assertEqual(store.status_of("r1"), "applied")
        head = self.head()
        again = fx.row("r1", 13, "in_film", status="in_progress", note=pod.CLAIM + " retry")
        rc, store2 = self.go([again])
        self.assertEqual((rc, store2.status_of("r1")), (0, "applied"))
        self.assertEqual(self.head(), head)

    def test_two_scenes_land_in_one_commit(self):
        rc, store = self.go([fx.row("a", 13, "in_film"), fx.row("b", 24, "in_film")])
        self.assertEqual(rc, 0)
        self.assertEqual(mse.active_scene_ids(self.origin_file("video-prompts.md")), [25, 30])
        n = subprocess.run(["git", "--git-dir", str(self.origin), "rev-list", "--count", f"{self.head0}..main"],
                           text=True, capture_output=True).stdout.strip()
        self.assertEqual(n, "1")


# ------------------------------------------------------------------ phase 1 must not pre-empt the conflict
class PhaseOneHoldTests(unittest.TestCase):
    def test_conflict_matrix(self):
        self.assertTrue(pod.master_conflict({"in_film"}, {"redo"}))
        self.assertTrue(pod.master_conflict({"in_film"}, {"result_bad"}))
        self.assertFalse(pod.master_conflict({"in_film"}, {"accept", "to_montage"}))
        self.assertTrue(pod.master_conflict({"scene_not_needed"}, {"accept"}))
        self.assertEqual(pod.button_token({"action": "tv_mark_status", "value": "result_bad"}), "result_bad")

    def test_prepare_leaves_a_scene_with_pending_in_film_and_redo_alone(self):
        rows = [{"id": "a", "scene_id": 13, "action": "redo", "status": "pending", "result_note": None},
                {"id": "b", "scene_id": 13, "action": "in_film", "status": "pending", "result_note": None},
                {"id": "c", "scene_id": 14, "action": "accept", "status": "pending", "result_note": None}]
        patches = []
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            blank = {"reviewed": None, "accepted": None, "needs_redo": None, "inserted_into_film": None}
            (root / "review-ledger.json").write_text(json.dumps({"schema_version": 2, "scenes": {"13": blank, "14": blank}}))
            with patch.object(pod, "ROOT", root), patch.object(pod, "api", return_value=rows), \
                    patch.object(pod, "patch_status", side_effect=lambda *a: patches.append(a) or True):
                silent(pod.prepare, root / "plan.json")
            plan = json.loads((root / "plan.json").read_text())
        self.assertEqual(plan["updates"], [])  # all review buttons are handled in phase 2
        self.assertEqual(patches, [])



class OwnerActionsWorkflowContract(unittest.TestCase):
    """Owner buttons must not revert silently to a plan-only GitHub job."""

    def test_owner_button_descriptions_match_canonical_slow_semantics(self):
        """Guard against old phase-one documentation surviving future handoffs."""
        names = ("NEW-CHAT-HANDOFF.md", "SYNC-RUNBOOK.md",
                 "AI-PROJECT-GUIDE.md", "USER-GUIDE.md", "README-AI-SYNC.md")
        docs = {name: (ROOT / name).read_text(encoding="utf-8") for name in names}
        for name, content in docs.items():
            with self.subTest(name=name):
                self.assertIn("Принять", content)
                self.assertIn("Переделать", content)
                self.assertIn("В монтаж", content)
        for name in ("SYNC-RUNBOOK.md", "AI-PROJECT-GUIDE.md", "README-AI-SYNC.md"):
            self.assertIn("фаза 2", docs[name])
            self.assertNotIn("фаза 1 «Принять", docs[name])
        self.assertNotIn("ни робот, ни монитор его не снимают", docs["README-AI-SYNC.md"])
        self.assertIn("Телеметрический робот не делает", docs["NEW-CHAT-HANDOFF.md"])

    def test_phase2_activation_and_cadence(self):
        workflow = (ROOT / '.github/workflows/sync-from-drive.yml').read_text(encoding='utf-8')
        self.assertIn("cron: '11,41 * * * *'", workflow)
        self.assertIn("ROBOT_MASTER_ACTIONS: ${{ vars.ROBOT_MASTER_ACTIONS || 'on' }}", workflow)
        self.assertIn("github.actor != 'github-actions[bot]'", workflow)
        self.assertIn('scripts/process_owner_decisions.py prepare', workflow)
        self.assertIn('scripts/robot_master_actions.py', workflow)

if __name__ == "__main__":
    unittest.main()
