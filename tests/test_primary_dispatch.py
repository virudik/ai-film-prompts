"""Primary-only intake and delayed backup; no provider/network calls."""
import json
import unittest
from datetime import timedelta
from unittest.mock import patch
import test_slot_rewake as fixtures
from test_slot_rewake import NOW, z, FakeGit, FakeNotifier
import robot_telemetry as rt


class PrimaryDispatchTests(unittest.TestCase):
    state = fixtures.RewakeTests.state
    receipts = fixtures.RewakeTests.receipts
    def setUp(self):
        fixtures.RewakeTests.setUp(self)
        self.cfg = {'dispatch': {'mode': 'primary_then_backup', 'enabled': True}}
        (self.root / 'ops/relay-wake.json').write_text(json.dumps(self.cfg))

    def test_primary_then_missing_ack_backup_on_next_scan(self):
        n = FakeNotifier()
        rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
        self.assertEqual(n.wakes[0]['dispatch_target'], 'primary')
        t = NOW + timedelta(minutes=10)
        rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
        self.assertEqual(n.wakes[1]['dispatch_target'], 'backup')
        self.assertEqual(n.wakes[1]['dispatch_reason'], 'no_ack_after_10_minutes')
        t += timedelta(minutes=10)
        rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
        self.assertEqual(len(n.wakes), 2)

    def test_fresh_started_suppresses_backup_then_stale_progress_allows_it(self):
        n = FakeNotifier()
        rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
        self.receipts([{'event_id': n.wakes[0]['event_id'], 'outcome': 'started',
                       'execution': {'updated_at': z(NOW+timedelta(minutes=9)), 'stage': 'intake'}}])
        t = NOW+timedelta(minutes=20)
        rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
        self.assertEqual(len(n.wakes), 1)
        t += timedelta(minutes=10)
        rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
        self.assertEqual(n.wakes[-1]['dispatch_target'], 'backup')

    def test_held_or_malformed_lease_never_wakes_competitor(self):
        for expiry in (z(NOW+timedelta(minutes=45)), 'invalid'):
            (self.root/'ops/canon-lock.json').write_text(json.dumps({'state':'held','expires_at':expiry}))
            n = FakeNotifier()
            rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
            self.assertEqual(n.wakes, [])

    def test_disabled_gate_preserves_legacy(self):
        (self.root/'ops/relay-wake.json').write_text(json.dumps({'dispatch':{'enabled':False}}))
        n=FakeNotifier()
        rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
        self.assertNotIn('dispatch_target', n.wakes[0])

    def test_no_external_notification_after_rejected_cas(self):
        n=FakeNotifier()
        rt.maybe_rewake(self.root, FakeGit(push_ok=False), n, NOW, z(NOW))
        self.assertEqual(n.wakes, [])

    def test_assignment_exclusive_with_primary_dm(self):
        calls=[]
        def gh(args, **kw):
            calls.append(args)
            return rt.subprocess.CompletedProcess(args,0,stdout='42\nhttps://github.com/x/y/issues/42\n' if '--jq' in args and '.number, .html_url' in args else '',stderr='')
        base={'event_id':'slots:test:4','observed_at':z(NOW),'free_slots_global':1}
        for target in ('primary','backup'):
            calls.clear()
            with patch.object(rt.subprocess,'run',side_effect=gh), patch.object(rt.relay_wake,'send_dm',return_value=('sent','message_id=1')) as dm:
                self.assertTrue(rt.GhNotifier().wake(dict(base, dispatch_target=target)))
                create=next(c for c in calls if '.number, .html_url' in c)
                self.assertEqual(any(s.startswith('assignees[]=') for s in create), target=='backup')
                self.assertEqual(dm.call_count, 1 if target=='primary' else 0)
