"""GitHub robot telemetry (scripts/robot_telemetry.py): offline tests on the compact validator-valid fixture."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import robot_fixture as fx            # noqa: E402
import robot_master_actions as rma    # noqa: E402
import robot_telemetry as rt          # noqa: E402

T0_PLUS_10 = datetime(2026, 10, 11, 10, 10, tzinfo=timezone.utc)
T0_PLUS_2H = datetime(2026, 10, 11, 12, 0, tzinfo=timezone.utc)
NEW_TASK = "c" * 32
UNKNOWN_TASK = "d" * 32


def active(task, scene, status="running", model="Wan 3.0", unlimited=True):
    return {"task_id": task, "board_id": "b", "status": status, "unlimited": unlimited,
            "created_at": "2026-10-11 09:30:00", "model": model, "scene_id": scene,
            "mapping": "task_map" if scene else "unknown_new", "queue_count": 1, "wait_seconds": 5,
            "process_seconds": None}


def scan(act=(), finished=(), mode="light", detail_failed=(), missing=(), checked="2026-10-11T12:00:00Z"):
    return {"schema_version": 1, "mode": "shadow", "checked_at": checked,
            "scan": {"mode": mode, "boards": 11, "board_task_counts": {"b": 3}, "pages_scanned": 1, "tasks_seen": 20,
                     "detail_failed": list(detail_failed)},
            "active_tasks": list(act), "unknown_new": [], "finished_known": list(finished),
            "missing_known_active": list(missing), "slots": {"capacity": 6}}


def steady():
    return [active(fx.ACTIVE_TASK, 30)]


class FakeNotifier:
    def __init__(self):
        self.posts = []
        self.wakes = []

    def post(self, title, text):
        self.posts.append((title, text))
        return True

    def wake(self, signal):
        self.wakes.append(signal)
        return True


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.origin, self.work = fx.make_origin(self.tmp.name)


class PlanTests(Base):
    def plan(self, s, now=T0_PLUS_10, resolver=None):
        return rt.plan_cycle(s, self.work, now, resolver=resolver)

    def test_unchanged_and_fresh_is_noop(self):
        p = self.plan(scan(steady(), checked="2026-10-11T10:10:00Z"))
        self.assertEqual((p["decision"], p["reasons"]), ("noop", []))

    def test_unchanged_but_old_telemetry_is_refreshed_by_heartbeat(self):
        p = self.plan(scan(steady()), now=T0_PLUS_2H)
        self.assertEqual(p["decision"], "publish")
        self.assertEqual((p["master_plan"]["add"], p["master_plan"]["finish"]), ([], []))
        self.assertEqual(p["master_plan"]["occupied_slots"], 1)
        self.assertEqual(p["cycle"]["active"][0]["task_id"], fx.ACTIVE_TASK)
        self.assertEqual(p["cycle"]["active"][0]["model_id"], "qwen-wan3.0-video")
        self.assertEqual(p["cycle"]["active"][0]["started_at"], "2026-10-11T09:30:00Z")
        self.assertNotIn("pages", p["cycle"])        # light scan keeps the last full-scan totals

    def test_new_task_for_idle_scene_plans_slow_add_with_scene_title(self):
        p = self.plan(scan(steady() + [active(NEW_TASK, 24, "init")]))
        self.assertEqual(p["decision"], "publish")
        self.assertEqual(p["changes"]["new"], [NEW_TASK])
        add = p["master_plan"]["add"]
        self.assertEqual([(a["scene"], a["task_id"], a["row_title"]) for a in add], [(24, NEW_TASK, "24 — Кабина")])

    def test_second_task_of_a_slow_scene_is_added_too(self):
        p = self.plan(scan(steady() + [active(NEW_TASK, 30, "init")]))
        self.assertEqual([a["scene"] for a in p["master_plan"]["add"]], [30])

    def test_status_change_publishes_without_master_edit(self):
        p = self.plan(scan([active(fx.ACTIVE_TASK, 30, "queued")]))
        self.assertEqual((p["decision"], p["changes"]["status_changed"]), ("publish", [fx.ACTIVE_TASK]))
        self.assertEqual((p["master_plan"]["add"], p["master_plan"]["finish"]), ([], []))

    def test_terminal_result_keeps_slow_and_plans_finish_line(self):
        fin = [{"task_id": fx.ACTIVE_TASK, "scene_id": 30, "final_status": "success", "completed_at": "2026-10-11 10:05:00",
                "error_code": None}]
        p = self.plan(scan([], fin))
        self.assertEqual(p["decision"], "publish")
        self.assertEqual(p["cycle"]["finished"], [{"scene_id": 30, "task_id": fx.ACTIVE_TASK, "final_status": "success",
                                                   "finished_at": "2026-10-11T10:05:00Z"}])
        self.assertEqual(p["master_plan"]["finish"][0]["finished_utc"], "11.10.2026 10:05:00 UTC")
        self.assertEqual([e["kind"] for e in p["events"]], ["result"])
        self.assertIn("не одобрение", p["events"][0]["text"])

    def test_already_processed_result_is_not_published_twice(self):
        fin = [{"task_id": fx.OLD_TASK, "scene_id": 13, "final_status": "success", "completed_at": "2026-10-11 10:05:00"}]
        p = self.plan(scan(steady(), fin), now=T0_PLUS_2H)
        self.assertEqual(p["cycle"]["finished"], [])

    def test_first_seen_terminal_is_resolved_without_consuming_a_slot(self):
        fin = {"task_id": UNKNOWN_TASK, "scene_id": None, "final_status": "success",
               "completed_at": "2026-10-11 10:05:00"}
        res = rt.make_resolver(lambda tid: ("Mode: reference-to-video | prompt 1 of scene 24", "Wan 3.0"))
        p = self.plan(scan(steady(), [fin]), resolver=res)
        self.assertEqual(p["decision"], "publish")
        self.assertEqual(p["cycle"]["finished"][0]["scene_id"], 24)
        self.assertEqual(p["master_plan"]["occupied_slots"], 1)
        self.assertIn(UNKNOWN_TASK, p["resolved_by_prompt"])
        self.assertIsNone(fin["scene_id"])

    def test_first_seen_terminal_with_changed_prompt_still_holds(self):
        fin = {"task_id": UNKNOWN_TASK, "scene_id": None, "final_status": "success"}
        res = rt.make_resolver(lambda tid: ("Mode: reference-to-video | prompt 1 of scene 24 EXTRA", "Wan 3.0"))
        p = self.plan(scan(steady(), [fin]), resolver=res)
        self.assertEqual(p["decision"], "hold")
        self.assertIn("finished_without_scene:" + UNKNOWN_TASK[:8], p["reasons"])

    def test_resolved_terminal_keeps_part_and_rejects_retired_scene(self):
        fin = {"task_id": UNKNOWN_TASK, "scene_id": None, "final_status": "success"}
        res = lambda tid, master, ids: {"scene": 24, "confidence": "exact", "label": "24 B3"}
        p = self.plan(scan(steady(), [fin]), resolver=res)
        self.assertEqual(p["cycle"]["finished"][0]["part"], "B3")
        fin["scene_id"] = 999
        p = self.plan(scan(steady(), [fin]))
        self.assertEqual(p["decision"], "hold")
        self.assertIn("scene_not_in_master:999", p["reasons"])

    def test_unmapped_active_task_holds_and_never_invents_a_scene(self):
        p = self.plan(scan(steady() + [active(UNKNOWN_TASK, None, "init")]))
        self.assertEqual(p["decision"], "hold")
        self.assertTrue(p["reasons"][0].startswith("unmapped_active:"))
        self.assertIsNone(p["cycle"])
        self.assertEqual(p["events"][0]["kind"], "unmapped")

    def test_exact_prompt_match_maps_unknown_task(self):
        master = (self.work / "video-prompts.md").read_text(encoding="utf-8")
        prompt = "Mode: reference-to-video | prompt 1 of scene 24"
        res = rt.make_resolver(lambda tid: (prompt, "Wan 3.0"))
        p = self.plan(scan(steady() + [active(UNKNOWN_TASK, None, "init")]), resolver=res)
        self.assertEqual(p["decision"], "publish")
        self.assertEqual(p["master_plan"]["add"][0]["scene"], 24)
        self.assertIn("exact match", p["cycle"]["active"][1]["mapping_confidence"])
        # resolver unit: a close-but-not-equal prompt is NOT accepted
        near = rt.make_resolver(lambda tid: (prompt + " extra words here", "Wan 3.0"))
        self.assertIsNone(near(UNKNOWN_TASK, master, {13, 24, 25, 30}))
        # identical text in two scenes is ambiguous
        twin = master.replace("prompt 1 of scene 25", "prompt 1 of scene 24")
        self.assertIsNone(res(UNKNOWN_TASK, twin, {13, 24, 25, 30}))
        # a scene that is not active in the master is refused
        self.assertIsNone(res(UNKNOWN_TASK, master, {13, 25, 30}))

    def test_sub_scene_code_is_kept_for_every_task(self):
        # 16.10.2026: the owner could not tell which part (A1, B6 …) of a multi-part scene was running or ready
        self.assertEqual(rt.part_from_label("28 B6"), "B6")
        self.assertEqual(rt.part_from_label("27 · Seedance 2.0 часть 2"), "Seedance 2.0 часть 2")
        self.assertIsNone(rt.part_from_label("16"))
        self.assertEqual(rt.part_from_confidence("prompt normalized match with master block 28 B2 (robot)"), "B2")
        self.assertIsNone(rt.part_from_confidence("prompt exact match with master block 24 (robot)"))
        self.assertIsNone(rt.part_from_confidence("Topview task map (exact Scene mapping from the monitor's map)"))
        m = ("## Сцена 28 — Финальные титры: имперский строевой танец\n\n#### B6 · Танец 6 — Маша, Лёша и Виталик\n\n"
             "```text\nx\n```\n\n## Сцена 30 — Колоннада\n\n#### B6 · чужая\n")
        self.assertEqual(rt.row_title(m, 28, "B6"), "28 · B6 · Танец 6 — Маша, Лёша и Виталик")
        self.assertEqual(rt.row_title(m, 28, "B9"), "28 · B9 — Финальные титры: имперский строевой танец")
        self.assertEqual(rt.row_title(m, 28, None), "28 — Финальные титры: имперский строевой танец")
        # a new task matched by its prompt carries the code into the slow row and the published telemetry
        res = lambda tid, master, ids: {"scene": 24, "confidence": "prompt exact match with master block 24 B3 (robot)",
                                        "label": "24 B3"}
        p = self.plan(scan(steady() + [active(UNKNOWN_TASK, None, "init")]), resolver=res)
        self.assertEqual(p["master_plan"]["add"][0]["row_title"], "24 · B3 — Кабина")
        self.assertEqual({a["task_id"]: a["part"] for a in p["cycle"]["active"]}, {fx.ACTIVE_TASK: None, UNKNOWN_TASK: "B3"})

    def test_incomplete_scan_or_vanished_task_holds(self):
        self.assertEqual(self.plan(scan(steady(), detail_failed=["x" * 32]))["decision"], "hold")
        self.assertEqual(self.plan(scan(steady(), missing=["x" * 32]))["decision"], "hold")
        gone = self.plan(scan([]))                     # published task disappeared without a terminal result
        self.assertEqual(gone["decision"], "hold")
        self.assertTrue(gone["reasons"][0].startswith("published_task_gone_without_result"))

    def test_scene_missing_from_master_holds(self):
        p = self.plan(scan(steady() + [active(NEW_TASK, 99, "init")]))
        self.assertEqual(p["decision"], "hold")
        self.assertIn("scene_not_in_master:99", p["reasons"])

    def test_non_unlimited_tasks_do_not_take_slots(self):
        p = self.plan(scan(steady() + [active(NEW_TASK, 24, "init", unlimited=False)]), now=T0_PLUS_2H)
        self.assertEqual([a["task_id"] for a in p["cycle"]["active"]], [fx.ACTIVE_TASK])


class MasterEditTests(Base):
    def test_marker_with_technical_tail_is_not_doubled(self):
        import master_slow_edit as mse
        master = (self.work / "video-prompts.md").read_text(encoding="utf-8")
        tail = f"**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ** · Wan 3.0 · task `{fx.ACTIVE_TASK}` (`init`, unlimited 0 credits). Редакционная приёмка отдельно.\n\n"
        s = master.index("\n## Сцена 30 —")
        master = master[:s] + master[s:].replace("**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**\n\n", tail, 1)
        plan = {"finish": [{"scene": 30, "task_id": fx.ACTIVE_TASK, "model": "Wan 3.0", "final_status": "success",
                            "finished_utc": "11.10.2026 10:05:00 UTC"}], "occupied_slots": 0}
        out, _ = mse.apply_plan(master, plan, "11.10.2026")
        sec = out[out.index("\n## Сцена 30 —"):]
        self.assertEqual(sec.count("**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**"), 1)
        self.assertIn("\n**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**\n\n", sec)                 # plain marker, stale tail dropped
        self.assertNotIn("unlimited 0 credits", sec)
        doubled = master[:s] + master[s:].replace(tail, tail + "**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**\n\n", 1)
        out2, _ = mse.apply_plan(doubled, plan, "11.10.2026")
        self.assertEqual(out2[out2.index("\n## Сцена 30 —"):].count("**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**"), 1)
        again, _ = mse.apply_plan(out.replace("✅ Технический результат получен · `success`", "`running`"), plan, "11.10.2026")
        self.assertEqual(again[again.index("\n## Сцена 30 —"):].count("технически завершён"), 1)


class RoleTests(Base):
    def test_robot_never_takes_over_by_itself(self):
        (self.work / "automation-monitor-status.json").write_text(json.dumps({"last_scheduled_cycle": {}}), encoding="utf-8")
        write_role(self.work, primary="chatgpt")
        ok, why = rt.role_allows(self.work)
        self.assertFalse(ok)
        write_role(self.work, primary="robot", standby="chatgpt")
        self.assertTrue(rt.role_allows(self.work)[0])


def write_role(work, primary="robot", standby="chatgpt"):
    role = {"schema_version": 1, "primary": primary, "standby": standby, "set_by": "test", "set_at": "2026-10-11T09:00:00Z",
            "failover_after_minutes": 180, "collision_guard_minutes": 50,
            "monitors": {"claude": {"commit_author": "Claude"}, "chatgpt": {"commit_author": "virudik"},
                         "robot": {"commit_author": "github-actions[bot]"}},
            "migration_state": {"chatgpt_writer_eligible": True}}
    (Path(work) / "monitor-role.json").write_text(json.dumps(role), encoding="utf-8")


class PublishTests(Base):
    def setUp(self):
        super().setUp()
        write_role(self.work)
        (self.work / "automation-monitor-status.json").write_text(json.dumps(
            {"schema_version": 1, "notification_state": {}, "last_scheduled_cycle": {}}), encoding="utf-8")
        fx.git(self.work, "add", "-A")
        fx.git(self.work, "commit", "-q", "-m", "roles and monitor status")
        fx.git(self.work, "push", "-q", "origin", "main")
        self.git = rma.Git(self.work)
        self.n = FakeNotifier()

    def go(self, s, now=T0_PLUS_2H, resolver=None):
        return rt.run_on(self.work, s, self.git, now=now, resolver=resolver, notifier=self.n)

    def head(self):
        self.git.run("fetch", "origin", "main")
        return self.git.run("rev-parse", "FETCH_HEAD").stdout.strip()

    def files(self, commit):
        return set(self.git.run("show", "--name-only", "--format=", commit).stdout.split())

    def load(self, name):
        return json.loads((self.work / name).read_text(encoding="utf-8"))

    def test_new_task_is_published_with_master_slow_row_and_valid_status(self):
        before = self.head()
        rc = self.go(scan(steady() + [active(NEW_TASK, 24, "init")]))
        self.assertEqual(rc, 0)
        after = self.head()
        self.assertNotEqual(before, after)
        self.assertTrue({"video-prompts.md", "topview-status.json", "topview-task-map.json", "topview-checkpoint.json",
                         "project-status.json", "SYNC-TRIGGER.txt", "automation-monitor-status.json"} <= self.files(after))
        master = (self.work / "video-prompts.md").read_text(encoding="utf-8")
        self.assertIn(f"task `{NEW_TASK}`", master)
        ps = self.load("project-status.json")
        self.assertEqual(ps["health"], "ok")
        self.assertEqual(sorted(ps["slow_scenes"]), [24, 30])
        ts = self.load("topview-status.json")
        self.assertEqual({r["task_id"] for r in ts["active_tasks"]}, {fx.ACTIVE_TASK, NEW_TASK})
        self.assertEqual(ts["occupied_slots"], 2)
        st = self.load("automation-monitor-status.json")
        self.assertEqual(st["last_scheduled_cycle"]["runner"], "robot_scheduled_task")
        self.assertEqual(st["last_scheduled_cycle"]["health"], "ok")
        self.assertEqual(st["last_successful_by_runner"]["robot"], st["last_scheduled_cycle"]["completed_at"])
        cp = self.load("topview-checkpoint.json")
        self.assertEqual(cp["canonical_validation"]["health"], "ok")
        self.assertEqual(self.n.posts, [])

    def test_terminal_result_never_clears_slow_and_is_announced_once(self):
        fin = [{"task_id": fx.ACTIVE_TASK, "scene_id": 30, "final_status": "success", "completed_at": "2026-10-11 10:30:00"}]
        self.assertEqual(self.go(scan([], fin)), 0)
        ps = self.load("project-status.json")
        self.assertEqual((ps["health"], ps["slow_scenes"]), ("ok", [30]))     # owner button only
        tm = self.load("topview-task-map.json")
        self.assertEqual(tm["active_by_scene"], {})
        self.assertIn(fx.ACTIVE_TASK, {p["task_id"] for p in tm["processed_tasks"]})
        self.assertTrue(self.load("review-ledger.json")["scenes"]["30"]["result_received"])
        self.assertIn("Технический результат получен", (self.work / "video-prompts.md").read_text(encoding="utf-8"))
        self.assertEqual(len(self.n.posts), 1)
        self.assertIn("Сцена 30", self.n.posts[0][0])
        self.assertIn("TOPVIEW_SLOT_WAKE_V1", self.n.posts[0][1])
        self.assertIn("@virudik", self.n.posts[0][1])
        # V2: exactly one new-issue wake with the stable event id
        self.assertEqual([w["event_id"] for w in self.n.wakes], ["result:" + fx.ACTIVE_TASK])
        self.assertEqual(self.n.wakes[0]["free_slots_global"], 6)
        # same scan again: nothing new to publish or announce
        before = self.head()
        self.assertEqual(self.go(scan([], fin), now=datetime(2026, 10, 11, 12, 5, tzinfo=timezone.utc)), 0)
        self.assertEqual(len(self.n.posts), 1)
        self.assertEqual(len(self.n.wakes), 1)
        self.assertEqual(self.head(), before)

    def test_stale_active_row_of_an_already_processed_task_is_repaired_once(self):
        # 13.10.2026: telemetry recorded the result, but the master row still said `running`
        tm = self.load("topview-task-map.json")
        tm["processed_tasks"].append({"task_id": fx.ACTIVE_TASK, "scene_id": 30, "final_status": "success",
                                      "finished_at": "2026-10-11T10:20:00Z"})
        tm["active_by_scene"] = {}
        (self.work / "topview-task-map.json").write_text(json.dumps(tm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ts = self.load("topview-status.json")
        ts["active_tasks"], ts["checked_at"] = [], "2026-10-11T11:50:00Z"
        (self.work / "topview-status.json").write_text(json.dumps(ts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        fx.git(self.work, "commit", "-qam", "result already recorded, master row stale")
        fx.git(self.work, "push", "-q", "origin", "main")
        p = rt.plan_cycle(scan([]), self.work, T0_PLUS_2H)
        self.assertEqual((p["decision"], p["changes"].get("repaired_rows")), ("publish", [fx.ACTIVE_TASK]))
        self.assertEqual(self.go(scan([])), 0)
        master = (self.work / "video-prompts.md").read_text(encoding="utf-8")
        row = next(l for l in master.split("\n") if f"task `{fx.ACTIVE_TASK}`" in l and l.startswith("| 30"))
        self.assertIn("Технический результат получен", row)
        self.assertNotIn("`running`", row)
        self.assertIn("**0 активных Topview-задач / 0 занятых слотов из 6**", master)   # physical slots, not rows
        sec = master[master.index("\n## Сцена 30 —"):]
        self.assertEqual(sec.count("**⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ**"), 1)                 # marker kept, never doubled
        self.assertEqual(sec.count(f"task `{fx.ACTIVE_TASK}` технически завершён"), 1)
        self.assertEqual(self.load("project-status.json")["health"], "ok")
        self.assertEqual(rt.plan_cycle(scan([]), self.work, T0_PLUS_2H)["changes"].get("repaired_rows"), None)

    def test_not_the_writer_means_no_write(self):
        write_role(self.work, primary="chatgpt", standby="claude")
        fx.git(self.work, "add", "-A")
        fx.git(self.work, "commit", "-q", "-m", "chatgpt is writer")
        fx.git(self.work, "push", "-q", "origin", "main")
        before = self.head()
        self.assertEqual(self.go(scan(steady() + [active(NEW_TASK, 24, "init")])), 0)
        self.assertEqual(self.head(), before)

    def test_hold_records_one_honest_degraded_cycle_and_notifies_once(self):
        s = scan(steady() + [active(UNKNOWN_TASK, None, "init")])
        before_ts = self.load("topview-status.json")["checked_at"]
        self.assertEqual(self.go(s), 0)
        st = self.load("automation-monitor-status.json")
        self.assertEqual(st["last_scheduled_cycle"]["health"], "degraded")
        self.assertEqual(st["last_scheduled_cycle"]["phases_missing"], ["telemetry_publish"])
        self.assertNotIn("last_successful_by_runner", st)                 # a hold is never a healthy heartbeat
        self.assertEqual(self.load("topview-status.json")["checked_at"], before_ts)   # no contradictory telemetry
        self.assertEqual(len(self.n.posts), 1)
        head = self.head()
        self.assertEqual(self.go(s, now=datetime(2026, 10, 11, 12, 10, tzinfo=timezone.utc)), 0)
        self.assertEqual((self.head(), len(self.n.posts)), (head, 1))

    def test_new_scene_without_ledger_row_does_not_block_publishing(self):
        # 16.10.2026: scenes 39–40 had no ledger row, the validator refused every robot publish for 3 h
        led = self.load("review-ledger.json")
        del led["scenes"]["25"]
        (self.work / "review-ledger.json").write_text(json.dumps(led, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        fx.git(self.work, "commit", "-qam", "new scene 25 without a ledger row")
        fx.git(self.work, "push", "-q", "origin", "main")
        self.assertEqual(self.go(scan(steady() + [active(NEW_TASK, 24, "init")])), 0)
        row = self.load("review-ledger.json")["scenes"]["25"]
        self.assertEqual(row, rt.LEDGER_BLANK)                              # empty: no decision inferred
        self.assertIn("review-ledger.json", self.files(self.head()))
        self.assertEqual(self.load("automation-monitor-status.json")["last_scheduled_cycle"]["health"], "ok")

    def test_part_survives_the_end_of_the_task(self):
        res = lambda tid, master, ids: {"scene": 24, "confidence": "prompt exact match with master block 24 B3 (robot)",
                                        "label": "24 B3"}
        self.assertEqual(self.go(scan(steady() + [active(UNKNOWN_TASK, None, "init")]), resolver=res), 0)
        ts = self.load("topview-status.json")
        self.assertEqual(ts["task_parts"], {UNKNOWN_TASK: "B3"})
        self.assertIn(f"| 24 · B3 — Кабина |", (self.work / "video-prompts.md").read_text(encoding="utf-8"))
        fin = [{"task_id": UNKNOWN_TASK, "scene_id": 24, "final_status": "success", "completed_at": "2026-10-11 12:30:00"}]
        self.assertEqual(self.go(scan(steady(), fin, checked="2026-10-11T12:40:00Z"),
                                 now=datetime(2026, 10, 11, 12, 40, tzinfo=timezone.utc)), 0)
        ts = self.load("topview-status.json")
        self.assertNotIn(UNKNOWN_TASK, {r["task_id"] for r in ts["active_tasks"]})
        self.assertEqual(ts["task_parts"], {UNKNOWN_TASK: "B3"})
        done = [x for x in self.load("topview-task-map.json")["processed_tasks"] if x["task_id"] == UNKNOWN_TASK]
        self.assertEqual(done[0]["part"], "B3")

    def test_validator_failure_commits_no_telemetry_and_is_reported_once(self):
        # scene 25 exists in master but the cycle references a task for an unknown scene id inside the plan
        s = scan(steady())
        s["active_tasks"][0]["scene_id"] = 30
        before = self.head()
        orig = rma.build_status
        rma.build_status = lambda *a, **k: (None, ["forced failure"])
        try:
            rc = self.go(s)
        finally:
            rma.build_status = orig
        self.assertEqual(rc, 1)
        after = self.head()
        self.assertNotEqual(after, before)
        self.assertEqual(self.files(after), {"automation-monitor-status.json"})   # telemetry untouched
        self.assertEqual(self.git.run("status", "--porcelain").stdout.strip(), "")
        st = self.load("automation-monitor-status.json")
        self.assertEqual(st["last_scheduled_cycle"]["health"], "degraded")
        self.assertTrue(st["last_scheduled_cycle"]["note"].startswith("publish failed: "))
        self.assertNotIn("last_successful_by_runner", st)
        self.assertEqual(len(self.n.posts), 1)
        # the same failure ten minutes later: no new commit, no second message
        rma.build_status = lambda *a, **k: (None, ["forced failure"])
        try:
            self.assertEqual(self.go(s, now=datetime(2026, 10, 11, 12, 10, tzinfo=timezone.utc)), 1)
        finally:
            rma.build_status = orig
        self.assertEqual((self.head(), len(self.n.posts)), (after, 1))


class ShadowTests(Base):
    def test_shadow_writes_only_its_own_preview_and_only_on_events(self):
        s = scan(steady() + [active(NEW_TASK, 24, "init")])
        plan = rt.plan_cycle(s, self.work, T0_PLUS_10)
        self.assertTrue(rt.write_preview(self.work, s, plan, T0_PLUS_10))
        data = json.loads((self.work / rt.PREVIEW).read_text(encoding="utf-8"))
        self.assertEqual((data["mode"], data["decision"]), ("shadow", "publish"))
        self.assertEqual(len(data["events"]), 1)
        # identical decision later: file content (apart from times) unchanged → no rewrite
        later = datetime(2026, 10, 11, 10, 20, tzinfo=timezone.utc)
        self.assertFalse(rt.write_preview(self.work, s, rt.plan_cycle(s, self.work, later), later))
        noop = scan(steady(), checked="2026-10-11T10:10:00Z")
        p2 = rt.plan_cycle(noop, self.work, T0_PLUS_10)
        rt.write_preview(self.work, noop, p2, T0_PLUS_10)
        self.assertEqual(len(json.loads((self.work / rt.PREVIEW).read_text(encoding="utf-8"))["events"]), 1)


if __name__ == "__main__":
    unittest.main()

