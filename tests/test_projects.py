"""Several projects in one repository (owner decision 20.10.2026): registry, detection, owner rows,
robot telemetry for tasks of the other projects. Offline, no secrets."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import projects as prj                # noqa: E402
import robot_fixture as fx            # noqa: E402
import robot_master_actions as rma    # noqa: E402
import robot_telemetry as rt          # noqa: E402
from test_robot_telemetry import FakeNotifier, active, scan, steady, write_role, T0_PLUS_10, T0_PLUS_2H  # noqa: E402

KM_TASK = "e" * 32
OTHER = "f" * 32
KM_PROMPT = "Mode: reference-to-video | Котмонавты, сцена 1: Лучик и Рыжик взлетают"


def km_master(prompt=KM_PROMPT):
    return ("# Котмонавты\n\n**1 сцен к генерации/доработке · 1 полных текстов промта**\n\n"
            "- **🛠️ 0** рабочих направлений.\n- **⏳ 0** сцен сейчас в медленной генерации: **нет**.\n"
            "- **Последняя полная синхронизация:** **20.10.2026 · тест**.\n\n"
            "| ID | Сцена | Персонажи | Что |\n|---|---|---|---|\n| 1 | [Взлёт](#scene-1) | коты | взлёт |\n\n"
            '<a id="scene-1"></a>\n\n## Сцена 1 — Взлёт\n\n```text\n' + prompt + "\n```\n")


def add_projects(work, prompt=KM_PROMPT):
    work = Path(work)
    (work / "projects" / "kotmonavty").mkdir(parents=True, exist_ok=True)
    reg = {"schema_version": 1, "default_project": "seregius",
           "projects": [{"id": "seregius", "name": "Серёгиус", "root": ".", "aliases": ["серёгиус"]},
                        {"id": "kotmonavty", "name": "Котмонавты", "root": "projects/kotmonavty",
                         "master": "projects/kotmonavty/video-prompts.md", "aliases": ["котмонавт"]}]}
    (work / "projects" / "projects.json").write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
    (work / "projects" / "kotmonavty" / "video-prompts.md").write_text(km_master(prompt), encoding="utf-8")


class RegistryTests(unittest.TestCase):
    def test_live_registry_and_project_folders_are_consistent(self):
        self.assertEqual(prj.validate(ROOT), [])
        ids = [p["id"] for p in prj.projects(ROOT, include_root=True)]
        self.assertEqual(ids[0], "seregius")
        self.assertEqual(prj.get(ROOT, "seregius")["root"], ".")    # the film stays where it always was

    def test_site_switcher_lists_the_same_projects_as_the_registry(self):
        js = (ROOT / "projects.js").read_text(encoding="utf-8")
        for p in prj.projects(ROOT, include_root=True):
            self.assertIn(f"id:'{p['id']}'", js)
            self.assertIn(p["name"], js)

    def test_project_master_builds_a_healthy_status(self):
        for pid in prj.other_ids(ROOT):
            st, _ = prj.build_status(ROOT, pid)
            self.assertEqual(st["health"], "ok", (pid, [k for k, v in st["checks"].items() if not v]))
            self.assertEqual(st["project"], pid)


class DetectTests(unittest.TestCase):
    reg = prj.load(ROOT)

    def d(self, text):
        return prj.detect(text, self.reg)

    def test_named_project_wins(self):
        self.assertEqual(self.d("В проекте Котмонавты сделай сцену взлёта")["project"], "kotmonavty")
        self.assertEqual(self.d("в коте детективе добавь сцену в кабинете")["project"], "kot-detektiv")
        self.assertEqual(self.d("Для Кот-детектива перенеси картинки")["project"], "kot-detektiv")
        self.assertEqual(self.d("в разном сделай ролик про море")["project"], "raznoe")
        self.assertEqual(self.d("в Серёгиусе поправь сцену 44")["project"], "seregius")

    def test_no_project_means_seregius(self):
        r = self.d("поправь сцену 44, Лучик и Рыжик в кабине")
        self.assertEqual((r["project"], r["default"]), ("seregius", True))

    def test_roskotmos_and_cats_alone_do_not_switch_the_project(self):
        self.assertEqual(self.d("сцена 57 РосКОТмоса: коты выбегают")["project"], "seregius")

    def test_two_projects_are_not_guessed(self):
        r = self.d("в котмонавтах сделай взлёт, а в детективе погоню")
        self.assertIsNone(r["project"])
        self.assertEqual(r["mentions"], ["kotmonavty", "kot-detektiv"])


class OwnerRowTests(unittest.TestCase):
    def test_rows_are_routed_by_tag(self):
        self.assertEqual(prj.project_of_row({"action": "accept", "scene_id": 3}), "seregius")
        self.assertEqual(prj.project_of_row({"action": "accept", "scene_id": 3, "value": "project:kotmonavty"}), "kotmonavty")
        self.assertEqual(prj.project_of_row({"action": "owner_task", "note": "[проект: kot-detektiv] сделай кадр"}), "kot-detektiv")
        self.assertEqual(prj.project_of_row({"action": "ref_feedback", "value": "ok",
                                             "note": "projects/kotmonavty/references/luchik.jpg"}), "kotmonavty")
        self.assertEqual(prj.project_of_row({"action": "ref_feedback", "value": "ok", "note": "references/luchik.jpg"}), "seregius")
        self.assertEqual(prj.strip_note_tag("[проект: raznoe] море"), "море")

    def test_task_buttons_follow_the_task_owner(self):
        tel = {"active": [{"project": "kotmonavty", "task_id": KM_TASK, "scene_id": 1}]}
        row = {"action": "tv_mark_status", "value": "result_bad", "task_id": KM_TASK, "scene_id": 1}
        self.assertEqual(prj.project_of_row(row, tel), "kotmonavty")
        self.assertEqual(prj.project_of_row(dict(row, task_id=OTHER), tel), "seregius")


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.origin, self.work = fx.make_origin(self.tmp.name)
        add_projects(self.work)


class RobotPlanTests(Base):
    def km_resolver(self, prompt=KM_PROMPT):
        return rt.make_project_resolver(lambda tid: (prompt, "Seedance 2.0") if tid == KM_TASK else ("unrelated", None), self.work)

    def test_task_of_another_project_does_not_hold_and_never_touches_the_film_master(self):
        p = rt.plan_cycle(scan(steady() + [active(KM_TASK, None, "init", "Seedance 2.0")]), self.work, T0_PLUS_10,
                          resolver=None, project_resolver=self.km_resolver())
        self.assertEqual(p["decision"], "publish", p["reasons"])
        self.assertEqual(p["master_plan"]["add"], [])                    # root master untouched
        self.assertEqual([a["task_id"] for a in p["cycle"]["active"]], [fx.ACTIVE_TASK])
        self.assertEqual(p["master_plan"]["occupied_slots"], 1)          # root validator contract unchanged
        self.assertEqual([(a["project"], a["scene_id"], a["task_id"]) for a in p["projects"]["active"]],
                         [("kotmonavty", 1, KM_TASK)])
        self.assertEqual(p["changes"]["projects"]["new"], [KM_TASK])

    def test_unknown_task_still_holds(self):
        p = rt.plan_cycle(scan(steady() + [active(OTHER, None, "init")]), self.work, T0_PLUS_10,
                          project_resolver=self.km_resolver())
        self.assertEqual(p["decision"], "hold")
        self.assertTrue(p["reasons"][0].startswith("unmapped_active:"))

    def test_known_project_task_needs_no_prompt_and_finishes_with_an_event(self):
        tel = {"active": [{"project": "kotmonavty", "scene_id": 1, "task_id": KM_TASK, "status": "running",
                           "model": "Seedance 2.0", "label": "1", "confidence": "x"}], "recent": []}
        (self.work / rt.PROJECTS_TELEMETRY).write_text(json.dumps(tel), encoding="utf-8")
        p = rt.plan_cycle(scan(steady() + [active(KM_TASK, None, "running", "Seedance 2.0")], checked="2026-10-11T10:10:00Z"),
                          self.work, T0_PLUS_10)
        self.assertEqual((p["decision"], p["reasons"]), ("noop", []))
        fin = [{"task_id": KM_TASK, "scene_id": None, "final_status": "success", "completed_at": "2026-10-11 10:05:00"}]
        p = rt.plan_cycle(scan(steady(), fin), self.work, T0_PLUS_10)
        self.assertEqual(p["decision"], "publish", p["reasons"])
        self.assertEqual(p["projects"]["active"], [])
        self.assertEqual([(r["task_id"], r["final_status"], r["project"]) for r in p["projects"]["recent"]],
                         [(KM_TASK, "success", "kotmonavty")])
        self.assertIn("Проект kotmonavty, сцена 1", p["events"][-1]["title"])
        self.assertEqual(p["master_plan"]["finish"], [])

    def test_vanished_project_task_holds(self):
        tel = {"active": [{"project": "kotmonavty", "scene_id": 1, "task_id": KM_TASK, "status": "running"}], "recent": []}
        (self.work / rt.PROJECTS_TELEMETRY).write_text(json.dumps(tel), encoding="utf-8")
        p = rt.plan_cycle(scan(steady()), self.work, T0_PLUS_10)
        self.assertEqual(p["decision"], "hold")
        self.assertTrue(any(r.startswith("project_task_gone_without_result") for r in p["reasons"]))

    def test_project_resolver_is_strict(self):
        res = self.km_resolver()
        self.assertEqual(res(KM_TASK)["project"], "kotmonavty")
        self.assertIsNone(self.km_resolver(KM_PROMPT + " и ещё слова")(KM_TASK))
        # the same prompt in two project scenes is ambiguous
        add_projects(self.work, KM_PROMPT)
        twin = km_master() + '\n<a id="scene-2"></a>\n\n## Сцена 2 — Копия\n\n```text\n' + KM_PROMPT + "\n```\n"
        (self.work / "projects" / "kotmonavty" / "video-prompts.md").write_text(twin, encoding="utf-8")
        self.assertIsNone(self.km_resolver()(KM_TASK))


class RobotPublishTests(Base):
    def setUp(self):
        super().setUp()
        write_role(self.work)
        (self.work / "automation-monitor-status.json").write_text(json.dumps(
            {"schema_version": 1, "notification_state": {}, "last_scheduled_cycle": {}}), encoding="utf-8")
        fx.git(self.work, "add", "-A")
        fx.git(self.work, "commit", "-q", "-m", "roles, monitor status, projects")
        fx.git(self.work, "push", "-q", "origin", "main")
        self.git = rma.Git(self.work)
        self.n = FakeNotifier()

    def test_publish_writes_project_telemetry_next_to_the_film_telemetry(self):
        res = rt.make_project_resolver(lambda tid: (KM_PROMPT, "Seedance 2.0"), self.work)
        rc = rt.run_on(self.work, scan(steady() + [active(KM_TASK, None, "init", "Seedance 2.0")]), self.git,
                       now=T0_PLUS_2H, resolver=None, notifier=self.n, project_resolver=res)
        self.assertEqual(rc, 0)
        self.git.run("fetch", "origin", "main")
        files = set(self.git.run("show", "--name-only", "--format=", "FETCH_HEAD").stdout.split())
        self.assertIn(rt.PROJECTS_TELEMETRY, files)
        tel = json.loads((self.work / rt.PROJECTS_TELEMETRY).read_text(encoding="utf-8"))
        self.assertEqual([t["task_id"] for t in tel["active"]], [KM_TASK])
        ts = json.loads((self.work / "topview-status.json").read_text(encoding="utf-8"))
        self.assertEqual([t["task_id"] for t in ts["active_tasks"]], [fx.ACTIVE_TASK])
        self.assertEqual(json.loads((self.work / "project-status.json").read_text(encoding="utf-8"))["health"], "ok")
        self.assertNotIn(KM_TASK, (self.work / "video-prompts.md").read_text(encoding="utf-8"))


import robot_project_actions as rpa    # noqa: E402

NOW = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)


def two_scene_master():
    return ("# Котмонавты\n\n**2 сцены к генерации/доработке · 2 полных текста промта**\n\n"
            "- **🛠️ 0** рабочих направлений.\n- **⏳ 0** сцен сейчас в медленной генерации: **нет**.\n"
            "- **Последняя полная синхронизация:** **20.10.2026 · тест**.\n\n"
            "| ID | Сцена | Персонажи | Что |\n|---|---|---|---|\n| 1 | [Взлёт](#scene-1) | коты | взлёт |\n"
            "| 2 | [Посадка](#scene-2) | коты | посадка |\n\n"
            '<a id="scene-1"></a>\n\n## Сцена 1 — Взлёт\n\n```text\nпромт 1\n```\n\n'
            '<a id="scene-2"></a>\n\n## Сцена 2 — Посадка\n\n```text\nпромт 2\n```\n')


def km_state(lock=None, queue_items=None):
    return {"kotmonavty": {
        "queue": {"project": "kotmonavty", "items": queue_items or [], "owner_site_actions": []},
        "ledger": {"schema_version": 1, "project": "kotmonavty", "scenes": {}},
        "lock": lock or {"state": "free"}, "master": two_scene_master(),
        "paths": {"queue": "projects/kotmonavty/ops/topview-launch-queue.json",
                  "ledger": "projects/kotmonavty/review-ledger.json",
                  "master": "projects/kotmonavty/video-prompts.md",
                  "status": "projects/kotmonavty/project-status.json"}}}


def row(i, action, sid, value="project:kotmonavty", **kw):
    return dict({"id": f"r{i}", "created_at": f"2026-10-20T10:0{i}:00Z", "scene_id": sid, "action": action,
                 "task_id": None, "value": value, "note": None, "status": "pending", "result_note": None}, **kw)


class ProjectButtonTests(unittest.TestCase):
    def test_remove_scene_reserves_the_number_and_keeps_the_master_valid(self):
        new = rpa.remove_scene(two_scene_master(), 1)
        self.assertNotIn("## Сцена 1", new)
        self.assertNotIn("| 1 | [", new)
        self.assertIn("## Сцена 2", new)
        self.assertIn("**1 сцена к генерации/доработке · 1 полный текст промта**", new)
        self.assertIn("Сцены 1 удалены из active master; их Scene ID зарезервированы", new)
        again = rpa.remove_scene(new, 2)
        self.assertIn("Сцены 1, 2 удалены из active master", again)
        self.assertIsNone(rpa.remove_scene(new, 7))

    def test_removed_scene_master_still_passes_the_validator(self):
        with tempfile.TemporaryDirectory() as d:
            add_projects(d)
            work = Path(d)
            reg = json.loads((work / "projects/projects.json").read_text(encoding="utf-8"))
            reg["projects"][1]["status"] = "projects/kotmonavty/project-status.json"
            (work / "projects/projects.json").write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
            (work / "projects/kotmonavty/video-prompts.md").write_text(rpa.remove_scene(two_scene_master(), 1),
                                                                     encoding="utf-8")
            st, _ = prj.build_status(work, "kotmonavty")
            self.assertEqual(st["health"], "ok", st.get("checks"))
            self.assertEqual(st.get("scene_ids"), [2])

    def test_scene_decisions_go_to_the_project_ledger_only(self):
        changed, acks, inbox = rpa.plan([row(1, "accept", 1), row(2, "in_film", 2)], km_state(), {}, NOW)
        self.assertEqual(set(changed), {"projects/kotmonavty/review-ledger.json", "projects/kotmonavty/video-prompts.md"})
        led = json.loads(changed["projects/kotmonavty/review-ledger.json"])["scenes"]
        self.assertTrue(led["1"]["accepted"])
        self.assertTrue(led["2"]["inserted_into_film"])
        self.assertNotIn("## Сцена 2", changed["projects/kotmonavty/video-prompts.md"])
        self.assertEqual([a[1] for a in acks], ["applied", "applied"])
        self.assertEqual(inbox, [])

    def test_contradicting_buttons_go_to_the_owner(self):
        changed, acks, _ = rpa.plan([row(1, "accept", 1), row(2, "redo", 1)], km_state(), {}, NOW)
        self.assertEqual(changed, {})
        self.assertEqual({a[1] for a in acks}, {"needs_owner"})

    def test_scene_still_generating_waits(self):
        tel = {"active": [{"task_id": KM_TASK, "project": "kotmonavty", "scene_id": 1}], "recent": []}
        changed, acks, _ = rpa.plan([row(1, "accept", 1)], km_state(), tel, NOW)
        self.assertEqual(changed, {})
        self.assertEqual(acks[0][1], "pending")

    def test_queue_waits_for_the_project_lock_and_unknown_scene_goes_to_the_inbox(self):
        held = {"state": "held", "holder": "chatgpt", "expires_at": "2026-10-20T12:30:00Z"}
        changed, acks, _ = rpa.plan([row(1, "queue_add", 1)], km_state(lock=held), {}, NOW)
        self.assertEqual(changed, {})
        self.assertEqual(acks[0][1], "pending")
        changed, acks, inbox = rpa.plan([row(1, "queue_add", 1)], km_state(), {}, NOW)
        self.assertIn("projects/kotmonavty/ops/topview-launch-queue.json", changed)
        self.assertEqual(acks[0][1], "in_progress")
        self.assertEqual(inbox[0]["project"], "kotmonavty")

    def test_buttons_of_the_film_are_not_taken(self):
        self.assertTrue(prj.is_root_row(row(1, "accept", 1, value=None)))
        changed, acks, _ = rpa.plan([row(1, "accept", 1, value="project:nope")], km_state(), {}, NOW)
        self.assertEqual(changed, {})
        self.assertEqual(acks[0][1], "needs_owner")


if __name__ == "__main__":
    unittest.main()
