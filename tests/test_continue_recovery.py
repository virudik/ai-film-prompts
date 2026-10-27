import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_takeover_brief as brief
import build_resume_packet as packet
import continue_preflight as preflight
import resume_state as state
from trim_service_files import trim_checkpoint

REPO = Path(__file__).resolve().parents[1]


class ContinueRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for p in list(brief.DOCS) + [brief.MASTER[0], "ops/CONTINUE-PROTOCOL.md"]:
            self.put(p, (REPO / p).read_bytes())
        self.js("instruction-sync-status.json", {"health": "ok", "source_of_truth": "github",
            "files": {p: {"mirror_sha256": state.digest((self.root / p).read_bytes())} for p in brief.DOCS}})
        self.js("project-status.json", {"health": "ok", "canonical_master_sha256": state.digest((self.root / brief.MASTER[0]).read_bytes())})
        self.js("monitor-role.json", {"primary": "robot"})
        self.js("topview-status.json", {})
        self.js("automation-monitor-status.json", {})
        self.js(state.QUEUE, {"items": [], "archived_items": []})
        self.put("reports/evidence.txt", b"actual saved result\n")
        self.put(state.CHECKPOINT, b"# Verified stage\n\nwork_id: WORK-1\nSaved artifact.\n")
        self.js(state.REGISTER, {"schema_version": 1, "active_work": [
            {"work_id": "WORK-1", "title": "User task", "status": "in_progress"},
            {"work_id": "MONITOR", "title": "Routine poll", "status": "in_progress", "updated_at": "2099-01-01T00:00:00Z"}]})
        state.capture(self.root, "WORK-1", "# Verified stage", "Saved result", "Review result",
                      ["reports/evidence.txt"], focus=True)
        with contextlib.redirect_stdout(io.StringIO()):
            brief.main(self.root, self.root / "shadow")

    def put(self, p, data):
        path = self.root / p
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def js(self, p, data):
        self.put(p, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())

    def read(self, p):
        return json.loads((self.root / p).read_bytes())

    def mutate_register(self, change):
        reg = self.read(state.REGISTER)
        change(reg)
        self.js(state.REGISTER, reg)

    def assertFull(self):
        r = preflight.evaluate(self.root)
        self.assertFalse(r["ready_for_short"], r)
        self.assertEqual(r["mode"], "full")

    def test_valid_task_and_monitor_does_not_steal_focus(self):
        r = preflight.evaluate(self.root)
        self.assertTrue(r["ready_for_short"], r["reasons"])
        self.assertEqual(r["selected_work"]["work_id"], "WORK-1")
        self.assertFalse(r["execution_authorized"])

    def test_shadow_checkpoint_missing(self):
        (self.root / "shadow/current-checkpoint.md").unlink()
        self.assertFull()

    def test_next_action_change_needs_checkpoint(self):
        self.mutate_register(lambda r: r["active_work"][0].update(next_action="Different action"))
        self.assertFull()

    def test_malformed_queue_fails_closed(self):
        for bad in ([], {"items": None}, {"items": [None]}, {"archived_items": None}):
            self.js(state.QUEUE, bad)
            result = packet.build(self.root)
            self.assertFalse(result["ready_for_resume"])
            self.assertFalse(result["execution_authorized"])

    def test_malformed_nested_certificate_falls_back(self):
        self.js("instruction-sync-status.json", {"files": ["invalid"]})
        self.assertFull()

    def test_malformed_brief_builds_nonready_packet(self):
        for bad in ([], {"sources": [{"file": None}]}, {"sources": [None]}):
            self.js("shadow/takeover-brief.json", bad)
            self.assertFalse(packet.build(self.root)["ready_for_resume"])

    def test_shadow_checkpoint_changed(self):
        self.put("shadow/current-checkpoint.md", b"stale\n")
        self.assertFull()

    def test_work_checkpoint_missing(self):
        (self.root / state.CHECKPOINT).unlink()
        self.assertFull()

    def test_work_checkpoint_changed(self):
        self.put(state.CHECKPOINT, b"# Verified stage\nwork_id: WORK-1\nInvented new result\n")
        self.assertFull()

    def test_duplicate_checkpoint_anchor(self):
        b = (self.root / state.CHECKPOINT).read_bytes()
        self.put(state.CHECKPOINT, b + b)
        self.assertFull()

    def test_other_checkpoint_prepend_keeps_bound_stage_valid(self):
        b = (self.root / state.CHECKPOINT).read_bytes()
        self.put(state.CHECKPOINT, b"# Monitor\nNo changes.\n\n---\n\n" + b)
        self.assertTrue(preflight.evaluate(self.root)["ready_for_short"])

    def test_missing_evidence(self):
        (self.root / "reports/evidence.txt").unlink()
        self.assertFull()

    def test_changed_evidence(self):
        self.put("reports/evidence.txt", b"a different result\n")
        self.assertFull()

    def test_no_focus_never_selects_newest(self):
        self.mutate_register(lambda r: r.pop("resume_focus"))
        self.assertFull()

    def test_finished_focus_not_restarted(self):
        self.mutate_register(lambda r: r["active_work"][0].update(status="completed"))
        self.assertFull()

    def test_missing_and_duplicate_work_ids(self):
        self.mutate_register(lambda r: r["active_work"].append(copy.deepcopy(r["active_work"][0])))
        self.assertFull()

    def test_redirect_cycle_fails_closed(self):
        self.mutate_register(lambda r: r["active_work"][0].update(continuation_work_id="WORK-1"))
        self.assertFull()

    def test_stale_instruction_hash(self):
        p = next(iter(brief.DOCS))
        self.put(p, (self.root / p).read_bytes() + b"\nnew instruction\n")
        self.assertFull()

    def test_duplicate_source_cannot_replace_a_required_doc(self):
        b = self.read("shadow/takeover-brief.json")
        b["sources"][0] = b["sources"][1]
        self.js("shadow/takeover-brief.json", b)
        self.assertFull()

    def test_capture_cannot_claim_another_tasks_checkpoint(self):
        with self.assertRaises(ValueError):
            state.capture(self.root, "MONITOR", "# Verified stage", "done", "next", ["reports/evidence.txt"])

    def test_unsafe_source_and_symlink_are_rejected(self):
        for p in ("../outside", "/etc/passwd", "https://example.com/file"):
            with self.assertRaises(ValueError):
                state.local_file(self.root, p)
        (self.root / "outside-link").symlink_to(REPO / "README.md")
        with self.assertRaises(ValueError):
            state.local_file(self.root, "outside-link")

    def test_observed_external_task_overrides_stale_waiting_flag(self):
        g = state.operation_guidance({"id": "VIDEO-1", "state": "waiting_for_slot", "task_id": "already-created"})
        self.assertEqual(g["recovery_action"], "observe_existing_task")
        self.assertFalse(g["submit_authorized"])

    def test_crash_after_claim_or_submit_without_receipt_never_retries(self):
        for item in ({"state": "waiting_for_slot", "claim": {"run_id": "interrupted"}},
                     {"state": "submission_unknown"}, {"state": "submitted"}):
            g = state.operation_guidance(item)
            self.assertEqual(g["recovery_action"], "reconcile_without_resubmitting")
            self.assertFalse(g["submit_authorized"])

    def test_packet_carries_archive_ids_and_unresolved_claims(self):
        self.js(state.QUEUE, {"items": [{"id": "uncertain", "state": "submission_unknown"}],
                             "archived_items": [{"id": "old", "state": "submitted", "task_id": "saved"}]})
        p = packet.build(self.root)
        self.assertEqual(p["queue_recovery"]["unresolved"][0]["item_id"], "uncertain")
        self.assertEqual(p["queue_recovery"]["existing_tasks"][0]["task_id"], "saved")
        self.assertFalse(p["execution_authorized"])

    def test_repeated_resume_is_read_only_and_packet_has_no_timestamp_churn(self):
        before = (self.root / state.REGISTER).read_bytes()
        one = packet.write(self.root)
        two = packet.write(self.root)
        self.assertEqual(one, two)
        self.assertEqual(before, (self.root / state.REGISTER).read_bytes())
        self.assertLess(one["packet_bytes"], 18000)

    def test_cleanup_keeps_bound_checkpoint(self):
        text = "".join("# Other " + str(n) + "\nold\n\n" for n in range(8))
        text += (self.root / state.CHECKPOINT).read_text()
        r = trim_checkpoint(text, "", "archive/checkpoint.md", protected_anchors={"# Verified stage"})
        self.assertIn("# Verified stage", r[0])
        self.assertNotIn("# Verified stage", r[1])
        self.assertEqual(state.section(text, "# Verified stage"), state.section(r[0], "# Verified stage"))


if __name__ == "__main__":
    unittest.main()
