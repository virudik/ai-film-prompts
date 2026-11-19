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
        t = NOW + timedelta(minutes=20)
        rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
        self.assertEqual(n.wakes[1]['dispatch_target'], 'backup')
        self.assertEqual(n.wakes[1]['dispatch_reason'], 'no_ack_after_20_minutes')
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
        t += timedelta(minutes=20)
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
                # Grok is woken by issue assignment, Dot by DM, whichever role each currently holds.
                actor = rt.wake_roles.actor_for(rt.relay_wake.load_config(rt.SCRIPTS.parent), target)
                self.assertEqual(any(s.startswith('assignees[]=') for s in create), actor=='grok')
                self.assertEqual(dm.call_count, 1 if actor=='dot' else 0)

    def test_multiple_active_heartbeats_refresh_suppression(self):
        n = FakeNotifier()
        rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
        event_id = n.wakes[0]['event_id']
        for minute, stage in ((9, 'intake'), (25, 'read_only_validation'), (45, 'finalization')):
            progress = NOW + timedelta(minutes=minute)
            receipt = {'event_id': event_id, 'outcome': 'started', 'checked_at': z(progress),
                       'execution': {'updated_at': z(progress), 'stage': stage}}
            self.receipts([receipt])
            self.assertEqual(rt.handler_receipt(self.root, event_id, progress), receipt)
            t = progress + timedelta(minutes=20)
            rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
            self.assertEqual(len(n.wakes), 1)
        t = NOW + timedelta(minutes=75)
        rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
        self.assertEqual(n.wakes[-1]['dispatch_target'], 'backup')

    def test_terminal_blocked_retryable_does_not_hide_behind_fresh_timestamp(self):
        for state, outcome in (('blocked', 'blocked'), ('completed', 'blocked_browser'),
                               ('started', 'blocked_browser')):
            with self.subTest(state=state, outcome=outcome):
                (self.root/'automation-monitor-status.json').write_text('{}')
                n = FakeNotifier()
                rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
                self.receipts([{'event_id': n.wakes[0]['event_id'], 'outcome': outcome,
                               'retryable': True, 'checked_at': z(NOW+timedelta(minutes=9)),
                               'execution': {'state': state, 'completed_at': z(NOW+timedelta(minutes=9))}}])
                t = NOW+timedelta(minutes=10)
                rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
                self.assertEqual(n.wakes[-1]['dispatch_reason'], 'primary_blocked_retryable')
                self.assertIn('never_repeat_unknown_Create', n.wakes[-1]['dispatch_policy'])
                rt.maybe_rewake(self.root, FakeGit(), n, t+timedelta(minutes=10), z(t+timedelta(minutes=10)))
                self.assertEqual(len(n.wakes), 2)  # backup remains paced, no wake loop

    def test_terminal_receipt_does_not_renew_active_progress_grace(self):
        for outcome in ('no_update', 'submitted', 'submission_unknown', 'read_only_test_complete'):
            with self.subTest(outcome=outcome):
                (self.root/'automation-monitor-status.json').write_text('{}')
                n = FakeNotifier()
                rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
                self.receipts([{'event_id': n.wakes[0]['event_id'], 'outcome': outcome,
                               'checked_at': z(NOW+timedelta(minutes=19)),
                               'execution': {'state': 'finished'}}])
                t = NOW+timedelta(minutes=20)
                rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
                self.assertEqual(n.wakes[-1]['dispatch_target'], 'backup')

    def test_blocked_receipt_never_overrides_live_or_malformed_lease_or_failed_cas(self):
        for expiry in (z(NOW+timedelta(minutes=45)), 'invalid', None):
            with self.subTest(expiry=expiry):
                (self.root/'automation-monitor-status.json').write_text('{}')
                (self.root/'ops/canon-lock.json').write_text('{}')
                n = FakeNotifier()
                rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
                self.receipts([{'event_id': n.wakes[0]['event_id'], 'outcome': 'blocked',
                               'retryable': True, 'checked_at': z(NOW+timedelta(minutes=9))}])
                if expiry is not None:
                    (self.root/'ops/canon-lock.json').write_text(json.dumps({'state':'held','expires_at':expiry}))
                t = NOW+timedelta(minutes=10)
                rt.maybe_rewake(self.root, FakeGit(push_ok=expiry is not None), n, t, z(t))
                self.assertEqual(len(n.wakes), 1)

    def test_untrustworthy_blocked_receipts_do_not_trigger_early_backup(self):
        for change in ({'checked_at': z(NOW-timedelta(minutes=1))},
                       {'checked_at': z(NOW+timedelta(minutes=30))},
                       {'event_id': 'other:event'}, {'actor': 'grok'}):
            with self.subTest(change=change):
                (self.root/'automation-monitor-status.json').write_text('{}')
                self.cfg['wake_roles'] = {'primary_actor':'dot', 'backup_actor':'grok'}
                (self.root/'ops/relay-wake.json').write_text(json.dumps(self.cfg))
                n = FakeNotifier()
                rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
                receipt = {'event_id': n.wakes[0]['event_id'], 'actor':'dot', 'outcome':'blocked',
                           'retryable': True, 'checked_at':z(NOW+timedelta(minutes=9))}
                receipt.update(change)
                self.receipts([receipt])
                t = NOW+timedelta(minutes=10)
                rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
                self.assertEqual(len(n.wakes), 1)

    def test_new_terminal_receipt_overrides_earlier_started_in_either_array_order(self):
        for reverse in (False, True):
            (self.root/'automation-monitor-status.json').write_text('{}')
            n = FakeNotifier()
            rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
            event_id = n.wakes[0]['event_id']
            receipts = [{'event_id':event_id, 'outcome':'started', 'checked_at':z(NOW+timedelta(minutes=5))},
                        {'event_id':event_id, 'outcome':'blocked', 'retryable':True,
                         'checked_at':z(NOW+timedelta(minutes=9))}]
            self.receipts(receipts[::-1] if reverse else receipts)
            t = NOW+timedelta(minutes=10)
            rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
            self.assertEqual(n.wakes[-1]['dispatch_reason'], 'primary_blocked_retryable')

    def test_no_ack_does_not_wake_backup_at_ten_minutes(self):
        n = FakeNotifier()
        rt.maybe_rewake(self.root, FakeGit(), n, NOW, z(NOW))
        t = NOW + timedelta(minutes=10)
        rt.maybe_rewake(self.root, FakeGit(), n, t, z(t))
        self.assertEqual(len(n.wakes), 1)
