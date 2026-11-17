"""Role swaps change notification transport, never ownership or launch authority."""
import json
import unittest
from datetime import timedelta
from unittest.mock import patch

import test_primary_dispatch as dispatch_fixtures
from test_slot_rewake import NOW, z, FakeGit, FakeNotifier
import robot_telemetry as rt
import wake_roles


class RoleContractTests(unittest.TestCase):
    def test_missing_block_is_legacy_forward(self):
        self.assertEqual(wake_roles.resolve({}), {
            'primary_actor': 'dot', 'backup_actor': 'grok', 'explicit': False})

    def test_both_directions_and_invalid_blocks(self):
        for primary, backup in (('dot', 'grok'), ('grok', 'dot')):
            config = {'wake_roles': {'primary_actor': primary, 'backup_actor': backup}}
            self.assertEqual(wake_roles.actor_for(config, 'primary'), primary)
            self.assertEqual(wake_roles.actor_for(config, 'backup'), backup)
        for block in (None, False, [], 'dot', {}, {'primary_actor': 'dot'},
                      {'primary_actor': 'dot', 'backup_actor': 'dot'},
                      {'primary_actor': [], 'backup_actor': 'grok'},
                      {'primary_actor': 'other', 'backup_actor': 'grok'}):
            with self.subTest(block=block):
                self.assertIsNone(wake_roles.resolve({'wake_roles': block}))

    def test_receipt_actor_is_explicit_or_known_exact_legacy_alias(self):
        self.assertEqual(wake_roles.receipt_actor({'actor': 'grok'}), 'grok')
        self.assertEqual(wake_roles.receipt_actor({'runner': 'chatgpt_event_trigger'}), 'dot')
        self.assertIsNone(wake_roles.receipt_actor({'actor': 'other', 'runner': 'dot_event_handler'}))
        self.assertIsNone(wake_roles.receipt_actor({'runner': 'not_really_grok'}))


class VideoRoleTests(unittest.TestCase):
    setUp = dispatch_fixtures.PrimaryDispatchTests.setUp
    state = dispatch_fixtures.PrimaryDispatchTests.state
    receipts = dispatch_fixtures.PrimaryDispatchTests.receipts

    def configure(self, primary='grok', backup='dot'):
        self.cfg['wake_roles'] = {'primary_actor': primary, 'backup_actor': backup}
        (self.root / 'ops/relay-wake.json').write_text(json.dumps(self.cfg))

    def run_at(self, notifier, minute):
        now = NOW + timedelta(minutes=minute)
        rt.maybe_rewake(self.root, FakeGit(), notifier, now, z(now))

    def test_reverse_order_and_unchanged_twenty_minute_no_ack_threshold(self):
        self.configure()
        notifier = FakeNotifier()
        self.run_at(notifier, 0)
        self.assertEqual(notifier.wakes[0]['dispatch_actor'], 'grok')
        self.run_at(notifier, 10)
        self.assertEqual(len(notifier.wakes), 1)
        self.run_at(notifier, 20)
        self.assertEqual(notifier.wakes[-1]['dispatch_actor'], 'dot')
        self.assertEqual(notifier.wakes[-1]['dispatch_reason'], 'no_ack_after_20_minutes')

    def test_ack_only_current_primary_actor_and_thirty_minute_progress_threshold(self):
        for primary, backup in (('grok', 'dot'), ('dot', 'grok')):
            for receipt_actor in (primary, backup, None):
                with self.subTest(primary=primary, receipt_actor=receipt_actor):
                    (self.root / 'automation-monitor-status.json').write_text('{}')
                    self.configure(primary, backup)
                    notifier = FakeNotifier()
                    self.run_at(notifier, 0)
                    receipt = {'event_id': notifier.wakes[0]['event_id'], 'outcome': 'started',
                               'execution': {'updated_at': z(NOW + timedelta(minutes=9))}}
                    if receipt_actor:
                        receipt['actor'] = receipt_actor
                    self.receipts([receipt])
                    self.run_at(notifier, 20)
                    self.assertEqual(len(notifier.wakes), 1 if receipt_actor == primary else 2)
                    if receipt_actor == primary:
                        self.run_at(notifier, 40)
                        self.assertEqual(notifier.wakes[-1]['dispatch_actor'], backup)
                        self.assertEqual(notifier.wakes[-1]['dispatch_reason'], 'no_progress_for_30_minutes')

    def test_role_swap_resets_routing_episode_but_preserves_lease_guard(self):
        self.configure('dot', 'grok')
        notifier = FakeNotifier()
        self.run_at(notifier, 0)
        self.configure('grok', 'dot')
        (self.root / 'ops/canon-lock.json').write_text(json.dumps({
            'state': 'held', 'expires_at': z(NOW + timedelta(minutes=45))}))
        self.run_at(notifier, 10)
        self.assertEqual(len(notifier.wakes), 1)
        (self.root / 'ops/canon-lock.json').write_text('{}')
        self.run_at(notifier, 20)
        self.assertEqual(notifier.wakes[-1]['dispatch_target'], 'primary')
        self.assertEqual(notifier.wakes[-1]['dispatch_actor'], 'grok')

    def test_invalid_role_config_never_sends_even_with_legacy_dispatch(self):
        self.configure('dot', 'dot')
        for enabled in (True, False):
            self.cfg['dispatch']['enabled'] = enabled
            (self.root / 'ops/relay-wake.json').write_text(json.dumps(self.cfg))
            notifier = FakeNotifier()
            self.run_at(notifier, 0)
            self.assertEqual(notifier.wakes, [])

    def test_notifier_transports_follow_actor_not_role_and_reject_stale_actor(self):
        self.configure()
        calls = []

        def gh(args, **kwargs):
            calls.append(args)
            output = '42\nhttps://github.com/x/y/issues/42\n' if '.number, .html_url' in args else ''
            return rt.subprocess.CompletedProcess(args, 0, stdout=output, stderr='')

        base = {'event_id': 'slots:test:4', 'observed_at': z(NOW), 'free_slots_global': 1}
        for role, actor in (('primary', 'grok'), ('backup', 'dot')):
            calls.clear()
            with patch.object(rt.relay_wake, 'load_config', return_value=self.cfg), \
                 patch.object(rt.subprocess, 'run', side_effect=gh), \
                 patch.object(rt.relay_wake, 'send_dm', return_value=('sent', 'message_id=1')) as dm:
                self.assertTrue(rt.GhNotifier().wake(dict(base, dispatch_target=role, dispatch_actor=actor)))
                create = next(c for c in calls if '.number, .html_url' in c)
                self.assertEqual(any(s.startswith('assignees[]=') for s in create), actor == 'grok')
                self.assertEqual(dm.call_count, int(actor == 'dot'))
                calls.clear()
                self.assertFalse(rt.GhNotifier().wake(dict(base, dispatch_target=role,
                                                          dispatch_actor='dot' if actor == 'grok' else 'grok')))
                self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
