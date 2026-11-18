import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cert_github as cg
import check_instruction_consistency as ci


class InstructionConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in cg.FILES + ['CLAUDE.md', 'ops/OWNER-TASKS.md', 'automation-monitor-status.json']:
            p = self.root / name; p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / name).read_bytes())
        self.old = json.loads((ROOT / 'archive/ops/instruction-certificate-legacy-2026-10-26.json').read_text())
        self.cert = cg.build(self.root, self.old)
        (self.root / 'instruction-sync-status.json').write_text(json.dumps(self.cert))
        self.now = datetime.now(timezone.utc)

    def snapshot(self):
        common = 'ops/OWNER-TASKS.md; строго больше 3 часов; только Claude'
        return {'checked_at': self.now.isoformat(), 'automations': [
            {'id': ci.HOURLY, 'is_enabled': True, 'default_timezone': 'Europe/Moscow',
             'schedule': 'BEGIN:VEVENT\nRRULE:FREQ=HOURLY;BYMINUTE=55\nEND:VEVENT',
             'prompt': common + '; ops/AUTOMATION-CONSISTENCY.md'},
            {'id': ci.RELAY, 'is_enabled': True, 'schedule': 'BEGIN:VEVENT\nX-UNSCHEDULED:1\nEND:VEVENT',
             'prompt': common + '; slots: no_update receipt_not_saved'}],
            'relay_subscriptions': [{'event': 'relay.message', 'active': True, 'arguments': {}}]}

    def test_recertify_drops_legacy_claims_and_refreshes_bootstrap(self):
        self.assertNotIn('error_prevention_architecture', self.cert)
        self.assertNotIn('control_center_owner_ui', self.cert)
        self.assertNotIn('semantic_check', self.cert)
        self.assertEqual(self.cert['claude_code_bootstrap']['github_blob'], cg.blob((self.root / 'CLAUDE.md').read_bytes()))
        self.assertEqual(self.cert['source_of_truth'], 'github')
        self.assertFalse(self.cert['automation_schedule']['execution_verified_by_this_certificate'])

    def test_drive_observation_age_preserved_but_match_recomputed(self):
        name = cg.FILES[0]
        before = self.old['files'][name]
        (self.root / name).write_text('changed canon')
        new = cg.build(self.root, self.old)['files'][name]
        self.assertFalse(new['drive_copy_match'])
        self.assertEqual(new['drive_copy_checked_at'], before['drive_copy_checked_at'])
        self.assertEqual(new['drive_file_id'], before['drive_file_id'])

    def test_live_snapshot_is_required_for_live_claim(self):
        result = ci.check(self.root, now=self.now)
        self.assertEqual(result['problems'], [])
        self.assertEqual(result['live_automations'], 'not_checked')
        self.assertEqual(ci.check(self.root, self.snapshot(), self.now)['problems'], [])

    def test_stale_dependency_and_changed_subscription_are_detected(self):
        snapshot = self.snapshot()
        snapshot['automations'][0]['prompt'] += '; 51B ждёт фактический51A'
        snapshot['relay_subscriptions'][0]['arguments'] = {'from': 'someone'}
        errors = ci.check(self.root, snapshot, self.now)['problems']
        self.assertTrue(any(x.startswith('automation-stale-dependency') for x in errors))
        self.assertIn('relay-subscription', errors)

    def test_removed_plot_ban_is_detected_if_it_returns(self):
        path = self.root / 'ops/FUTURE-PLANS.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('С 10.11 (t512u) сюжетную очередь не продолжать.\n', encoding='utf-8')
        self.assertIn('stale-phrase:plot-ban-t512', ci.check(self.root, now=self.now)['problems'])

    def test_launch_by_run_id_prefix_is_detected_if_it_returns(self):
        path = self.root / 'ops/CONTINUE-PROTOCOL.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('запуска начинается с `chatgpt-scheduled-`\n', encoding='utf-8')
        self.assertIn('stale-phrase:launch-by-name', ci.check(self.root, now=self.now)['problems'])

    def test_live_files_do_not_restore_replaced_decisions(self):
        self.assertEqual(ci.stale_phrases(ROOT), [])

    def test_dot_current_tasks_stay_named_and_unchecked(self):
        gap = ci.check(ROOT, now=self.now)['dot_current_tasks']
        self.assertEqual(gap['status'], 'not_checked')
        self.assertEqual(gap['ids'], [
            '6afc8b674794819192ba0b1415c5a220',
            '6afd1f83b1b08191b4b7c8ad55c132cf',
        ])
        doc = (ROOT / 'ops/AUTOMATION-CONSISTENCY.md').read_text(encoding='utf-8')
        self.assertIn('dot_current_tasks.status=not_checked', doc)
        for task_id in gap['ids']:
            self.assertIn(task_id, doc)
        sandbox = ci.check(self.root, self.snapshot(), self.now)
        self.assertEqual(sandbox['dot_current_tasks']['status'], 'not_checked')
        self.assertEqual(sandbox['dot_current_tasks']['ids'], [])
        self.assertNotIn('dot-current-tasks', sandbox['problems'])
        snapshot = self.snapshot()
        snapshot['automations'].append({
            'id': '6afd1f83b1b08191b4b7c8ad55c132cf', 'is_enabled': True,
            'schedule': 'BEGIN:VEVENT\nX-UNSCHEDULED:1\nEND:VEVENT',
            'prompt': 'ops/OWNER-TASKS.md; строго больше 3 часов; только Claude',
        })
        extra = ci.check(self.root, snapshot, self.now)
        self.assertIn('automation-set', extra['problems'])
        self.assertEqual(extra['dot_current_tasks']['status'], 'not_checked')

    def test_stale_observation_and_changed_canonical_bytes_are_detected(self):
        snapshot = self.snapshot(); snapshot['checked_at'] = (self.now - timedelta(hours=2)).isoformat()
        (self.root / cg.FILES[0]).write_text('new instructions')
        errors = ci.check(self.root, snapshot, self.now)['problems']
        self.assertIn('automation-observation-stale', errors)
        self.assertIn('certificate-bytes:' + cg.FILES[0], errors)
