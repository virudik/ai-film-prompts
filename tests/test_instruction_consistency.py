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

    def test_stale_observation_and_changed_canonical_bytes_are_detected(self):
        snapshot = self.snapshot(); snapshot['checked_at'] = (self.now - timedelta(hours=2)).isoformat()
        (self.root / cg.FILES[0]).write_text('new instructions')
        errors = ci.check(self.root, snapshot, self.now)['problems']
        self.assertIn('automation-observation-stale', errors)
        self.assertIn('certificate-bytes:' + cg.FILES[0], errors)
