import importlib.util, json, sys, tempfile, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

spec = importlib.util.spec_from_file_location(
    "launch_autonomy_check", Path(__file__).resolve().parents[1] / "scripts" / "launch_autonomy_check.py")
lac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lac)

NOW = datetime(2026, 10, 18, 5, 30, tzinfo=timezone.utc)


def item(i, run, at, state="submitted"):
    return {"id": i, "scene_id": 1, "state": state, "claim": {"run_id": run, "claimed_at": at}}


class LaunchAutonomyTest(unittest.TestCase):
    def test_classifies_schedule_and_chat(self):
        q = {"items": [item("A", "chatgpt-scheduled-20261018T010000Z", "2026-10-18T01:00:00Z"),
                       item("B", "chatgpt-cloud-20261017-B", "2026-10-17T12:00:00Z"),
                       item("old", "chatgpt-cloud-x", "2026-10-16T12:00:00Z")]}
        ll = lac.launches(q, NOW - timedelta(hours=24))
        self.assertEqual([x["source"] for x in ll], ["unknown", "schedule"])
        self.assertEqual(lac.verdict(ll, [], []), "schedule_launched")

    def test_reads_last_claim_after_verified_submission(self):
        q = {"items": [{"id": "S58", "scene_id": 58, "state": "submitted", "claim": None,
                         "last_claim": {"run_id": "chatgpt-scheduled-S58",
                                        "claimed_at": "2026-10-18T04:00:00Z"}}]}
        ll = lac.launches(q, NOW - timedelta(hours=24))
        self.assertEqual(len(ll), 1)
        self.assertEqual(ll[0]["item"], "S58")
        self.assertEqual(ll[0]["source"], "schedule")

    def test_idle_free_slots_detected(self):
        log = ["2026-10-18T02:00:00+00:00\tGitHub robot: Topview telemetry — 5/6 slots, +0 new, 1 finished",
               "2026-10-18T03:00:00+00:00\tGitHub robot: Topview telemetry — 6/6 slots, +0 new, 0 finished"]
        free = lac.free_slot_observations(log)
        self.assertEqual(len(free), 1)
        self.assertEqual(lac.verdict([], free, ["S36"]), "historical_free_slots_unverified")
        self.assertEqual(lac.verdict([], [], ["S36"]), "no_free_slots")

    def test_old_scheduled_launch_does_not_hide_current_unresolved_executor(self):
        # Real incident: S61 launched 30-Oct; on 31-Oct the 24h verdict stayed green through a 5h40 gap.
        ll = [{"source": "schedule", "claimed_at": "2026-10-30T15:37:29Z"}]
        free = [{"at": "2026-10-31T05:28:33Z", "occupied": 5, "capacity": 6}]
        for state in ("launch_stalled", "reconciliation_required", "observation_stale"):
            with self.subTest(state=state):
                self.assertEqual(lac.verdict(ll, free, ["S72-WAN30"],
                                            {"state": state, "unresolved": True}), "launch_stalled")
        self.assertEqual(lac.verdict(ll, free, ["S72-WAN30"],
                                    {"state": "capacity_full", "unresolved": False}), "schedule_launched")

    def test_build_preserves_stalled_diagnosis_and_marks_stale_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'ops').mkdir()
            (root / 'ops/topview-launch-queue.json').write_text(json.dumps({'items': [
                item('old-success', 'chatgpt-scheduled-old', '2026-10-18T01:00:00Z')]}))
            (root / 'automation-monitor-status.json').write_text(json.dumps({
                'health': 'ok', 'launcher_health': {'state': 'launch_stalled', 'unresolved': True,
                                                  'checked_at': '2026-10-18T03:00:00Z'}}))
            report = lac.build(root, 24, NOW, [])
            self.assertEqual(report['launches_by_schedule'], 1)
            self.assertEqual(report['verdict'], 'launch_stalled')
            self.assertTrue(report['launcher_observation_stale'])

    def test_notify_flag_routes_stalled_report_even_with_a_previous_scheduled_launch(self):
        report = {'schema_version': 1, 'verdict': 'launch_stalled', 'window_hours': 24,
                  'launches_by_schedule': 1, 'launches_by_chat': 0, 'ready_items_waiting': 33,
                  'free_slot_observations': [], 'launcher_observation_stale': False,
                  'launcher_health': {'state': 'launch_stalled', 'reason': 'no_handler_receipt',
                                      'checked_at': '2026-10-31T06:50:33Z'}}
        with tempfile.TemporaryDirectory() as tmp, patch.object(lac, 'build', return_value=report), \
                patch.object(lac, 'git_log', return_value=[]), patch.object(lac, 'notify') as notify:
            self.assertEqual(lac.main([tmp, '--notify']), 0)
            notify.assert_called_once_with(report)
        with patch('robot_telemetry.GhNotifier') as notifier:
            lac.notify(report)
            _title, text = notifier.return_value.post.call_args.args
            self.assertIn('расписания: 1', text)
            self.assertIn('unresolved', text)
            self.assertNotIn('ничего не запустило', text)

    def test_repository_queue_parses(self):
        repo = Path(__file__).resolve().parents[1]
        r = lac.build(repo, 24, NOW, [])
        self.assertIn(r["verdict"], ("schedule_launched", "chat_only", "no_free_slots", "nothing_ready",
                                     "historical_free_slots_unverified", "launch_stalled", "launches_observed"))
        self.assertIn("launcher_health", r)



class ModernLaunchEvidenceTest(unittest.TestCase):
    def fixture(self, root, trigger='scheduled'):
        it={'id':'S89E-WAN30','state':'completed','task_id':'9d4b3b177e6d452abe499537a05f454c',
            'submitted_at':'2026-10-18T04:00:00Z','receipt':'reports/task.json',
            'claim':{'claimed_at':'2026-10-16T04:00:00Z','execution_instance_id':'actual-uuid','run_id':None}}
        r={'item_id':it['id'],'task_id':it['task_id'],'execution_instance_id':'actual-uuid',
           'actual_trigger':trigger,'automation_id':'real-automation','run_id':None}
        (root/'reports').mkdir(exist_ok=True); (root/'reports/task.json').write_text(json.dumps(r))
        return it,r
    def test_null_id_with_bound_trigger_is_schedule_not_chat(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); it,_=self.fixture(root)
            ll=lac.launches({'items':[it]},NOW-timedelta(hours=24),repo=root,now=NOW)
            self.assertEqual(ll[0]['source'],'schedule'); self.assertIsNone(ll[0]['run_id'])
            self.assertEqual(ll[0]['time_basis'],'submitted_at')
    def test_manual_webhook_unknown_and_unbound(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for trigger,source in [('manual_run_now','manual_run_now'),('webhook','webhook'),('not_exposed','unknown')]:
                it,_=self.fixture(root,trigger)
                self.assertEqual(lac.launches({'items':[it]},NOW-timedelta(days=1),repo=root)[0]['source'],source)
            it,r=self.fixture(root); r['task_id']='wrong'; (root/'reports/task.json').write_text(json.dumps(r))
            self.assertEqual(lac.launches({'items':[it]},NOW-timedelta(days=1),repo=root)[0]['source'],'unknown')
    def test_s89e_historical_receipt_without_trigger_remains_unknown(self):
        root=Path(__file__).resolve().parents[1]
        r=json.loads((root/'reports/topview-queue-2026-10-16/S89E-WAN30-20261117.json').read_text())
        it={'id':r['item_id'],'task_id':r['task_id']}; claim={'execution_instance_id':r['execution_instance_id']}
        self.assertEqual(lac.launch_source(it,claim,r)[0],'unknown')
    def test_completed_archived_and_deduplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); it,_=self.fixture(root)
            (root/'ops').mkdir(); (root/'archive/ops').mkdir(parents=True)
            (root/'ops/topview-launch-queue.json').write_text(json.dumps({'items':[]}))
            (root/'archive/ops/topview-launch-queue-archive.json').write_text(json.dumps({'items':[it,it]}))
            r=lac.build(root,24,NOW,[])
            self.assertEqual(r['launches_by_schedule'],1)
    def test_old_slots_and_current_queue_do_not_prove_idle(self):
        self.assertEqual(lac.verdict([], [{'at':'old'}], ['ready_now'],
                                    {'state':'capacity_full','unresolved':False}), 'historical_free_slots_unverified')
    def test_claim_without_submission_is_not_launch(self):
        it=item('not-submitted',None,'2026-10-18T04:00:00Z','completed')
        self.assertEqual(lac.launches({'items':[it]},NOW-timedelta(days=1)),[])

    def test_unbound_or_conflicting_trigger_never_uses_legacy_prefix(self):
        it={'id':'x','task_id':'task'}
        cl={'execution_instance_id':'uuid','automation_id':'right','run_id':'chatgpt-scheduled-old'}
        for task,automation in [('wrong','right'),('task','wrong')]:
            receipt={'item_id':'x','task_id':task,'execution_instance_id':'uuid',
                     'actual_trigger':'scheduled','automation_id':automation}
            self.assertEqual(lac.launch_source(it,cl,receipt)[0],'unknown')

if __name__ == "__main__":
    unittest.main()
