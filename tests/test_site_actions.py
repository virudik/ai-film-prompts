import copy
import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import robot_site_actions as rsa  # noqa: E402

NOW = datetime(2026, 10, 18, 5, 0, tzinfo=timezone.utc)


def item(iid, scene, prio, state="waiting_for_slot", deps=None, **extra):
    d = {"id": iid, "scene_id": scene, "priority": prio, "state": state, "depends_on_submitted": deps or [],
         "canonical_prompt_sha256": "x" * 64, "engine_version": "seedance20"}
    d.update(extra)
    return d


def queue():
    return {"schema_version": 1, "selection_policy": "41 → 43 → 54", "new_scene_order": [43, 54, 36, 13],
            "items": [item("S41", 41, 0, "submitted"), item("S43", 43, 1), item("S54", 54, 2, deps=["S43"]),
                      item("S36-P1", 36, 3), item("S36-P2", 36, 3.1, "blocked_inputs", deps=["S36-P1"]),
                      item("S36-old", 36, 3, "superseded_owner_model_selection"),
                      item("S13", 13, 230, "blocked_owner_decision")]}


def files(q=None, lock=None, inbox=None, review=None):
    return {rsa.QUEUE: q or queue(), rsa.INBOX: inbox or copy.deepcopy(rsa.EMPTY_INBOX),
            rsa.REF_REVIEW: review or copy.deepcopy(rsa.EMPTY_REVIEW), rsa.LOCK: lock or {"state": "free"}}


def row(rid, action, scene=None, status="pending", value=None, note=None, result_note=None):
    return {"id": rid, "created_at": "2026-10-18T04:00:00Z", "action": action, "scene_id": scene,
            "status": status, "value": value, "note": note, "result_note": result_note}


def by_id(q, iid):
    return next(i for i in q["items"] if i["id"] == iid)


class QueueTests(unittest.TestCase):
    def test_up_swaps_with_neighbour_and_keeps_other_fields(self):
        nf, acks = rsa.plan([row("a", "queue_up", 36)], files(), NOW)
        q = json.loads(nf[rsa.QUEUE])
        self.assertEqual(by_id(q, "S36-P1")["priority"], 2)
        self.assertEqual(by_id(q, "S36-P2")["priority"], 2.1)
        self.assertEqual(by_id(q, "S54")["priority"], 3)
        self.assertEqual(by_id(q, "S36-old")["priority"], 3)        # superseded items never move
        self.assertEqual(by_id(q, "S41")["priority"], 0)            # launched items never move
        self.assertEqual(by_id(q, "S36-P1")["engine_version"], "seedance20")
        self.assertEqual(q["new_scene_order"], [43, 36, 54, 13])
        self.assertTrue(q["selection_policy"].startswith("OWNER SITE ORDER"))
        self.assertEqual(acks[0][1], "applied")
        self.assertEqual(q["owner_site_actions"][-1]["decision_id"], "a")

    def test_down_at_end_is_noop(self):
        nf, acks = rsa.plan([row("a", "queue_down", 13)], files(), NOW)
        self.assertEqual(acks[0][1], "applied")
        self.assertIn("последняя", acks[0][2])

    def test_dependency_note(self):
        _, acks = rsa.plan([row("a", "queue_up", 54)], files(), NOW)
        self.assertIn("S43", acks[0][2])

    def test_remove_and_add_back(self):
        nf, _ = rsa.plan([row("a", "queue_remove", 36)], files(), NOW)
        q = json.loads(nf[rsa.QUEUE])
        self.assertEqual(by_id(q, "S36-P1")["state"], rsa.HELD)
        self.assertEqual(by_id(q, "S36-P2")["previous_state_before_site_hold"], "blocked_inputs")
        nf2, acks = rsa.plan([row("b", "queue_add", 36)], files(q), NOW)
        q2 = json.loads(nf2[rsa.QUEUE])
        self.assertEqual(by_id(q2, "S36-P2")["state"], "blocked_inputs")
        self.assertEqual(by_id(q2, "S36-P1")["state"], "waiting_for_slot")
        self.assertEqual(acks[0][1], "applied")

    def test_add_releases_owner_gate(self):
        nf, acks = rsa.plan([row("a", "queue_add", 13)], files(), NOW)
        self.assertEqual(by_id(json.loads(nf[rsa.QUEUE]), "S13")["state"], "waiting_for_slot")

    def test_add_unknown_scene_becomes_inbox_task(self):
        nf, acks = rsa.plan([row("a", "queue_add", 99)], files(), NOW)
        inbox = json.loads(nf[rsa.INBOX])
        self.assertEqual(inbox["tasks"][0]["to"], "any")
        self.assertEqual(acks[0][1], "in_progress")
        self.assertTrue(acks[0][2].startswith(rsa.INBOX_CLAIM))

    def test_lock_held_waits_with_reason(self):
        lock = {"state": "held", "holder": "chatgpt", "expires_at": "2026-10-18T05:30:00Z"}
        nf, acks = rsa.plan([row("a", "queue_up", 36)], files(lock=lock), NOW)
        self.assertNotIn(rsa.QUEUE, nf)
        self.assertEqual(acks[0][1], "pending")
        self.assertIn("chatgpt", acks[0][2])
        # same reason already shown → no repeated write
        _, acks2 = rsa.plan([row("a", "queue_up", 36, result_note=acks[0][2])], files(lock=lock), NOW)
        self.assertEqual(acks2, [])

    def test_expired_lock_is_free(self):
        lock = {"state": "held", "holder": "chatgpt", "expires_at": "2026-10-18T04:00:00Z"}
        nf, acks = rsa.plan([row("a", "queue_up", 36)], files(lock=lock), NOW)
        self.assertIn(rsa.QUEUE, nf)


class InboxTests(unittest.TestCase):
    def test_task_goes_to_inbox_with_target(self):
        nf, acks = rsa.plan([row("t1", "owner_task", 42, value="chatgpt", note="поменять реплику")], files(), NOW)
        inbox = json.loads(nf[rsa.INBOX])
        self.assertEqual(inbox["tasks"][0]["to"], "chatgpt")
        self.assertEqual(inbox["tasks"][0]["status"], "open")
        self.assertIn("ChatGPT", acks[0][2])
        self.assertNotIn(rsa.QUEUE, nf)

    def test_default_target_any_and_idempotent(self):
        f = files()
        nf, _ = rsa.plan([row("t1", "owner_task", None, note="идея")], f, NOW)
        inbox = json.loads(nf[rsa.INBOX])
        self.assertEqual(inbox["tasks"][0]["to"], "any")
        nf2, acks = rsa.plan([row("t1", "owner_task", None, note="идея")], files(inbox=inbox), NOW)
        self.assertNotIn(rsa.INBOX, nf2)       # already there: only the ack is repeated
        self.assertEqual(acks[0][1], "in_progress")

    def test_back_flow_done(self):
        inbox = copy.deepcopy(rsa.EMPTY_INBOX)
        inbox["tasks"].append({"id": "t1", "status": "done", "taken_by": "claude:site", "result": "сделано",
                               "result_commit": "abcdef123", "closed_at": "2026-10-18T04:30:00Z"})
        _, acks = rsa.plan([row("t1", "owner_task", 42, status="in_progress", result_note=rsa.INBOX_CLAIM + " x")],
                           files(inbox=inbox), NOW)
        self.assertEqual(acks[0][1], "applied")
        self.assertIn("abcdef1", acks[0][2])

    def test_back_flow_taken_updates_note_once(self):
        inbox = copy.deepcopy(rsa.EMPTY_INBOX)
        inbox["tasks"].append({"id": "t1", "status": "taken", "taken_by": "chatgpt", "taken_at": "2026-10-18T04:10:00Z"})
        r = row("t1", "owner_task", 42, status="in_progress", result_note=rsa.INBOX_CLAIM + " x")
        _, acks = rsa.plan([r], files(inbox=inbox), NOW)
        self.assertIn("chatgpt", acks[0][2])
        _, acks2 = rsa.plan([dict(r, result_note=acks[0][2])], files(inbox=inbox), NOW)
        self.assertEqual(acks2, [])

    def test_prune_old_closed(self):
        inbox = copy.deepcopy(rsa.EMPTY_INBOX)
        inbox["tasks"] = [{"id": "old", "status": "done", "closed_at": iso(NOW - timedelta(days=20))},
                          {"id": "new", "status": "done", "closed_at": iso(NOW - timedelta(days=2))},
                          {"id": "open", "status": "open"}]
        nf, _ = rsa.plan([], files(inbox=inbox), NOW)
        ids = [t["id"] for t in json.loads(nf[rsa.INBOX])["tasks"]]
        self.assertEqual(ids, ["new", "open"])


class RefTests(unittest.TestCase):
    def test_ok_recorded(self):
        nf, acks = rsa.plan([row("r1", "ref_feedback", 45, value="ok", note="references/scenes/scene-45/a.png")], files(), NOW)
        rev = json.loads(nf[rsa.REF_REVIEW])
        self.assertEqual(rev["reviews"][0]["path"], "references/scenes/scene-45/a.png")
        self.assertEqual(acks[0][1], "applied")
        self.assertNotIn(rsa.INBOX, nf)

    def test_redraw_goes_to_chatgpt(self):
        nf, acks = rsa.plan([row("r1", "ref_feedback", 45, value="redraw",
                                 note="references/scenes/scene-45/a.png | корабль крупнее")], files(), NOW)
        t = json.loads(nf[rsa.INBOX])["tasks"][0]
        self.assertEqual(t["to"], "chatgpt")
        self.assertIn("корабль крупнее", t["text"])
        self.assertEqual(acks[0][1], "in_progress")


class RunTests(unittest.TestCase):
    def test_ack_only_after_push(self):
        class Store:
            def __init__(s): s.marks = []
            def list_open(s): return [row("t1", "owner_task", 42, note="x y z")]
            def mark(s, r, st, note): s.marks.append(st); return True

        class Git:
            def __init__(s, ok): s.ok, s.pushes = ok, 0
            def sync(s): pass
            def commit(s, m, p): return "c0ffee"
            def push(s): s.pushes += 1; return s.ok
            def head_is_on_remote(s): return True
            def reset(s): pass

        import tempfile
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "ops").mkdir()
            (Path(d) / rsa.QUEUE).write_text(rsa.dumps(queue()), encoding="utf-8")
            st, g = Store(), Git(False)
            self.assertEqual(rsa.run(d, st, g, now=NOW, sync=False), 1)
            self.assertEqual(st.marks, [])            # push never succeeded → nothing acknowledged
            st2 = Store()
            self.assertEqual(rsa.run(d, st2, Git(True), now=NOW, sync=False), 0)
            self.assertEqual(st2.marks, ["in_progress"])


def iso(dt):
    return rsa.iso(dt)


if __name__ == "__main__":
    unittest.main()
