#!/usr/bin/env python3
"""Topview robot scanner (shadow mode): offline tests with a fake API client. No network, no keys."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import topview_api_scan as scan  # noqa: E402

MAIN = scan.MAIN_BOARD
OTHER = "db4b4d6d0abc4cb4b278ea80738639f2"
NOW = datetime(2026, 10, 11, 12, 0, 0, tzinfo=timezone.utc)
T_MAPPED, T_NEW, T_OLD, T_ELSE = "1" * 32, "2" * 32, "3" * 32, "4" * 32


def stamp(minutes_ago):
    return (NOW - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%d %H:%M:%S")


def task(tid, status, minutes_ago, unlimited=True, board=MAIN, model="Wan 3.0", completed=None):
    return {"boardTaskId": tid, "boardId": board, "status": status, "gmtCreate": stamp(minutes_ago),
            "completedAt": stamp(completed) if completed is not None else None,
            "parameters": {"modelName": model, "useUnlimitMode": unlimited, "positivePrompt": "prompt of " + tid[:4]},
            "useUnlimitMode": unlimited}


class FakeClient:
    """Mimics Client.get(); records every call so tests can prove which endpoints were touched."""

    def __init__(self, boards, tasks, details=None, shape="data"):
        self.boards, self.tasks, self.details, self.shape = boards, tasks, details or {}, shape
        self.calls, self.requests = [], 0

    def _wrap(self, items, total):
        return {self.shape: items, "total": total}

    def get(self, path, query=None):
        self.calls.append((path, dict(query or {})))
        self.requests += 1
        if path == "/boards/list":
            return self._wrap(self.boards, len(self.boards))
        if path == "/boards/tasks/list":
            allt = self.tasks.get(query["boardId"], [])
            size, no = query["pageSize"], query["pageNo"]
            return self._wrap(allt[(no - 1) * size:no * size], len(allt))
        if path == "/boards/tasks/detail":
            if query["taskId"] not in self.details:
                raise scan.ApiError("detail: HTTP 404")
            return self.details[query["taskId"]]
        raise AssertionError("unexpected endpoint " + path)

    def list_calls(self, page_size=None):
        return [q for p, q in self.calls if p == "/boards/tasks/list" and (page_size is None or q["pageSize"] == page_size)]


def make_repo(tmp, *, monitor_active=(), monitor_age_min=200):
    repo = Path(tmp)
    tm = {"last_scan_at": (NOW - timedelta(minutes=monitor_age_min)).strftime("%Y-%m-%dT%H:%M:%SZ"),
          "scan_cursor": {}, "active_by_scene": {"16": [T_MAPPED]},
          "processed_tasks": [{"task_id": T_OLD, "scene_id": 13, "final_status": "success", "finished_at": "2026-10-01T00:00:00Z"}]}
    (repo / "topview-task-map.json").write_text(json.dumps(tm))
    active = [{"task_id": t, "scene_id": 16, "topview_status": "running"} for t in monitor_active]
    (repo / "topview-status.json").write_text(json.dumps({
        "checked_at": tm["last_scan_at"], "occupied_slots": len(active), "active_tasks": active}))
    return repo


def world(extra_main=()):
    boards = [{"boardId": MAIN, "name": "main", "taskCount": 3 + len(extra_main)},
              {"boardId": OTHER, "name": "other", "taskCount": 1}]
    tasks = {MAIN: [*extra_main, task(T_MAPPED, "running", 90), task(T_OLD, "success", 3000, completed=2900)],
             OTHER: [task(T_ELSE, "success", 5000, board=OTHER, completed=4900)]}
    return boards, tasks


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(self.tmp.name, monitor_active=(T_MAPPED,))

    def tearDown(self):
        self.tmp.cleanup()

    def run_scan(self, client, prev=None, **kw):
        return scan.scan(client, self.repo, prev or {}, now=NOW, **kw)

    def test_first_run_is_full_and_maps_only_through_the_task_map(self):
        boards, tasks = world(extra_main=[task(T_NEW, "init", 5)])
        detail = {T_MAPPED: dict(task(T_MAPPED, "running", 90), estimateInfo={"queueCount": 2, "estimatedWaitSeconds": 40}),
                  T_NEW: task(T_NEW, "init", 5)}
        c = FakeClient(boards, tasks, detail)
        st = self.run_scan(c)
        self.assertEqual(st["scan"]["mode"], "full")
        self.assertIn("no recorded full scan", st["scan"]["reasons"])
        self.assertEqual(st["slots"]["occupied"], 2)
        self.assertEqual(st["slots"]["free"], 4)
        self.assertEqual(st["slots"]["capacity"], 6)
        by_id = {a["task_id"]: a for a in st["active_tasks"]}
        self.assertEqual(by_id[T_MAPPED]["scene_id"], 16)
        self.assertEqual(by_id[T_MAPPED]["mapping"], "task_map")
        self.assertEqual((by_id[T_MAPPED]["queue_count"], by_id[T_MAPPED]["wait_seconds"]), (2, 40))
        self.assertIsNone(by_id[T_NEW]["scene_id"])                      # a Scene ID is never invented
        self.assertEqual(by_id[T_NEW]["mapping"], "unknown_new")
        self.assertEqual([u["task_id"] for u in st["unknown_new"]], [T_NEW])
        self.assertEqual(st["unknown_new"][0]["prompt_head"], "prompt of 2222")
        self.assertEqual(len(c.list_calls(100)), 2)                      # both boards, all pages
        self.assertEqual(st["cursor"]["last_full_scan_at"], "2026-10-11T12:00:00Z")
        self.assertEqual(st["cursor"]["board_task_counts"], {MAIN: 4, OTHER: 1})

    def test_only_unlimited_tasks_occupy_slots(self):
        boards, tasks = world(extra_main=[task(T_NEW, "running", 5, unlimited=False)])
        c = FakeClient(boards, tasks, {T_MAPPED: task(T_MAPPED, "running", 90), T_NEW: task(T_NEW, "running", 5, unlimited=False)})
        st = self.run_scan(c)
        self.assertEqual(st["slots"]["occupied"], 1)
        self.assertEqual(st["slots"]["active_not_unlimited"], 1)

    def prev_after_full(self, boards, tasks, details):
        return self.run_scan(FakeClient(boards, tasks, details))

    def test_light_scan_touches_only_the_newest_page_and_known_active_tasks(self):
        boards, tasks = world()
        details = {T_MAPPED: task(T_MAPPED, "running", 90)}
        prev = self.prev_after_full(boards, tasks, details)
        prev["checked_at"] = "2026-10-11T11:30:00Z"
        prev["cursor"]["last_full_scan_at"] = "2026-10-11T11:30:00Z"
        c = FakeClient(boards, tasks, details)
        st = self.run_scan(c, prev)
        self.assertEqual(st["scan"]["mode"], "light", st["scan"]["reasons"])
        self.assertEqual(c.list_calls(100), [])
        self.assertEqual([q["pageSize"] for q in c.list_calls()], [20])
        self.assertEqual(st["slots"]["occupied"], 1)

    def test_known_task_finishing_is_reported_with_the_mapped_scene(self):
        boards, tasks = world()
        tasks[MAIN][1] = task(T_MAPPED, "success", 90, completed=10)
        details = {T_MAPPED: task(T_MAPPED, "success", 90, completed=10)}
        prev = {"checked_at": "2026-10-11T11:30:00Z", "cursor": {"last_full_scan_at": "2026-10-11T11:30:00Z",
                                                                  "board_task_counts": {MAIN: 3, OTHER: 1}}}
        st = self.run_scan(FakeClient(boards, tasks, details), prev)
        self.assertEqual(st["slots"]["occupied"], 0)
        self.assertEqual([(f["task_id"], f["scene_id"], f["final_status"]) for f in st["finished_known"]],
                         [(T_MAPPED, 16, "success")])
        self.assertTrue(any(r["task_id"] == T_MAPPED and r["scene_id"] == 16 for r in st["recent_completions"]))

    def test_counter_change_on_another_board_forces_full(self):
        boards, tasks = world()
        prev = {"checked_at": "2026-10-11T11:30:00Z", "cursor": {"last_full_scan_at": "2026-10-11T11:30:00Z",
                                                                  "board_task_counts": {MAIN: 3, OTHER: 0}}}
        st = self.run_scan(FakeClient(boards, tasks, {T_MAPPED: task(T_MAPPED, "running", 90)}), prev)
        self.assertEqual(st["scan"]["mode"], "full")
        self.assertTrue(any("count" in r for r in st["scan"]["reasons"]))

    def test_stale_full_scan_forces_full_and_forced_mode(self):
        boards, tasks = world()
        prev = {"checked_at": "2026-10-11T08:00:00Z", "cursor": {"last_full_scan_at": "2026-10-11T08:00:00Z",
                                                                  "board_task_counts": {MAIN: 3, OTHER: 1}}}
        self.assertEqual(self.run_scan(FakeClient(boards, tasks, {T_MAPPED: task(T_MAPPED, "running", 90)}), prev)["scan"]["mode"], "full")
        fresh = dict(prev, checked_at="2026-10-11T11:50:00Z", cursor=dict(prev["cursor"], last_full_scan_at="2026-10-11T11:50:00Z"))
        self.assertEqual(self.run_scan(FakeClient(boards, tasks, {T_MAPPED: task(T_MAPPED, "running", 90)}), fresh, mode="full")["scan"]["mode"], "full")

    def test_api_reference_shape_result_list_is_accepted_too(self):
        boards, tasks = world()
        st = self.run_scan(FakeClient(boards, tasks, {T_MAPPED: task(T_MAPPED, "running", 90)}, shape="list"))
        self.assertEqual(st["scan"]["boards"], 2)

    def test_a_missing_detail_makes_the_scan_incomplete_not_invented(self):
        boards, tasks = world()
        st = self.run_scan(FakeClient(boards, tasks, {}))               # detail endpoint fails for the active task
        self.assertFalse(st["slots"]["complete"])
        self.assertEqual(st["scan"]["detail_failed"], [T_MAPPED])
        self.assertEqual(st["slots"]["occupied"], 1)                    # still counted from the list entry

    def test_known_active_task_that_vanished_is_reported_as_missing(self):
        boards, tasks = world()
        tasks[MAIN] = [t for t in tasks[MAIN] if t["boardTaskId"] != T_MAPPED]
        st = self.run_scan(FakeClient(boards, tasks, {}))
        self.assertEqual(st["missing_known_active"], [T_MAPPED])


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def result(self, monitor_active, monitor_age, robot_active=True):
        repo = make_repo(self.tmp.name, monitor_active=monitor_active, monitor_age_min=monitor_age)
        boards, tasks = world()
        if not robot_active:
            tasks[MAIN][1] = task(T_MAPPED, "success", 90, completed=10)
        det = {T_MAPPED: task(T_MAPPED, "running" if robot_active else "success", 90)}
        return scan.scan(FakeClient(boards, tasks, det), repo, {}, now=NOW)["comparison"]

    def test_consistent(self):
        c = self.result((T_MAPPED,), 20)
        self.assertTrue(c["consistent"])
        self.assertFalse(c["monitor_may_lag"])
        self.assertEqual((c["monitor_occupied"], c["robot_occupied"]), (1, 1))

    def test_monitor_still_shows_a_finished_task_flagged_as_possible_lag(self):
        c = self.result((T_MAPPED,), 200, robot_active=False)
        self.assertFalse(c["consistent"])
        self.assertTrue(c["monitor_may_lag"])
        self.assertEqual({d["type"] for d in c["differences"]}, {"only_in_monitor", "occupied_differs"})

    def test_robot_sees_a_task_the_monitor_does_not(self):
        c = self.result((), 10)
        self.assertEqual([d["type"] for d in c["differences"]], ["only_in_robot", "occupied_differs"])
        self.assertFalse(c["monitor_may_lag"])


class ClientAndOutputTests(unittest.TestCase):
    def test_http_errors_never_leak_the_key_and_5xx_is_retried(self):
        key = "SECRET-KEY-VALUE"
        calls = []

        class Resp:
            def __init__(self, body): self.body = body
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self, n): return self.body

        def flaky(req, timeout):
            calls.append(req.headers)
            if len(calls) == 1:
                raise HTTPError(req.full_url, 503, "busy", {}, None)
            return Resp(json.dumps({"code": "200", "result": {"data": [], "total": 0}}).encode())

        c = scan.Client(key, "uid-1", opener=flaky, sleep=lambda s: None)
        self.assertEqual(c.get("/boards/list", {"pageNo": 1}), {"data": [], "total": 0})
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]["Authorization"], "Bearer " + key)
        self.assertEqual(calls[0]["Topview-uid"], "uid-1")

        def denied(req, timeout):
            raise HTTPError(req.full_url, 401, "no", {}, None)

        with self.assertRaises(scan.ApiError) as ctx:
            scan.Client(key, "uid-1", opener=denied, sleep=lambda s: None).get("/boards/list")
        self.assertNotIn(key, str(ctx.exception))
        self.assertIn("401", str(ctx.exception))

    def test_write_only_when_content_changes_not_timestamps(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "shadow" / "s.json"
            base = {"checked_at": "a", "cursor": {"last_full_scan_at": "x"}, "scan": {"api_requests": 5, "mode": "full"},
                    "comparison": {"monitor_age_minutes": 3}, "slots": {"occupied": 1}}
            self.assertTrue(scan.write_if_changed(p, base))
            later = json.loads(json.dumps(base))
            later["checked_at"], later["cursor"]["last_full_scan_at"] = "b", "y"
            later["scan"]["api_requests"], later["comparison"]["monitor_age_minutes"] = 9, 33
            before = p.read_text()
            self.assertFalse(scan.write_if_changed(p, later))
            self.assertEqual(p.read_text(), before)
            later["slots"]["occupied"] = 2
            self.assertTrue(scan.write_if_changed(p, later))

    def test_not_configured_is_a_clean_noop(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"TOPVIEW_API_KEY": "", "TOPVIEW_UID": ""}), \
                patch.object(sys, "argv", ["x", "--repo", d]):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = scan.main()
            self.assertEqual(rc, 0)
            self.assertIn("not configured", buf.getvalue())
            self.assertFalse((Path(d) / scan.OUTPUT).exists())

    def test_notice_has_no_secrets_and_is_compact(self):
        with tempfile.TemporaryDirectory() as d:
            repo = make_repo(d, monitor_active=(T_MAPPED,), monitor_age_min=20)
            boards, tasks = world()
            st = scan.scan(FakeClient(boards, tasks, {T_MAPPED: task(T_MAPPED, "running", 90)}), repo, {}, now=NOW)
        line = scan.notice(st)
        self.assertTrue(line.startswith("::notice title=topview-robot-shadow::"))
        self.assertIn('"occupied": "1/6"', line)
        self.assertLess(len(line), 1000)

    def test_scanner_is_get_only(self):
        src = (ROOT / "scripts" / "topview_api_scan.py").read_text(encoding="utf-8")
        import re
        self.assertEqual(set(re.findall(r'method="(\w+)"', src)), {"GET"})
        self.assertNotRegex(src, r"urlopen\([^)]*data=")
        for path in re.findall(r'"(/[a-z]+/[a-z/]+)"', src):
            self.assertIn(path, ("/boards/list", "/boards/tasks/list", "/boards/tasks/detail"))


if __name__ == "__main__":
    unittest.main()
