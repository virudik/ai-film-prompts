import copy
import json
import sys
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import launcher_coordination as lc
import launcher_run_ledger as run_ledger

NOW = datetime(2026, 11, 18, 20, 45, tzinfo=timezone.utc)
A = '11111111-1111-4111-8111-111111111111'
B = '22222222-2222-4222-8222-222222222222'
BOARD = '1a6244cf1ae747ef847d949a80d6133c'
REPO = Path(__file__).resolve().parents[1]

MINIMAX_POLICY = {
    'enabled': True,
    'transport': 'interactive_chat',
    'board_id': BOARD,
    'unlimited_zero_only': True,
    'slot_capacity': 6,
    'max_submissions_per_wake': 6,
    'first_real_create': {'owner_go_ahead': True},
    'retry_budget': {'enabled': False},
    'wake_issue': None,
}


class MinimaxPeerTests(unittest.TestCase):
    """Regressions required by 00-START-HERE.md §5 for the new Minimax peer."""

    def setUp(self):
        self.cfg = {
            'enabled': True, 'route_generation': 7,
            'peers': {
                'ordinary': {'enabled': True, 'automation_ids': ['ordinary-task']},
                'work': {'enabled': True, 'automation_ids': ['work-task']},
                'grok': {'enabled': True, 'automation_ids': ['topview-grok']},
                'minimax': {'enabled': True, 'automation_ids': [], 'receipt': 'reports/topview-minimax-cycle.json'},
            },
            'minimax_launcher': copy.deepcopy(MINIMAX_POLICY),
            'grok_launcher': {
                'board_id': BOARD, 'max_submissions_per_wake': 6, 'slot_capacity': 6,
                'first_real_create': {'owner_go_ahead': True},
                'launch_window': {'timezone': 'Europe/Amsterdam', 'first_hour': 8, 'last_hour': 23,
                                  'first_minute': 10, 'last_minute': 40},
            },
            'run_ledger': {'required_surfaces': ['grok', 'minimax']},
            'foreground_owners': {'minimax': {'session_id': 'minimax-session-1', 'epoch': 1}},
        }
        self.actor = {
            'execution_instance_id': A, 'surface': 'minimax', 'kind': 'interactive',
            'route_generation': 7, 'transport': 'interactive_chat',
            'provider_run_id': 'minimax-session-464814249484626-run-1',
            'submissions_this_wake': 0,
            'session_id': 'minimax-session-1', 'foreground_epoch': 1,
            'lease_acquired_at': lc.stamp(NOW - timedelta(minutes=1)),
        }
        self.lock = {'state': 'held', 'holder': lc.holder(self.actor),
                     'acquired_at': self.actor['lease_acquired_at'],
                     'expires_at': lc.stamp(NOW + timedelta(minutes=5))}
        self.scan = {'complete': True, 'checked_at': lc.stamp(NOW), 'free_slots': 1,
                     'item_reconciliation': {'S-example': {'complete': True,
                                                          'matched_task_ids': [], 'ambiguous': False}}}
        p = dict.fromkeys(('owner_authorized', 'prompt_match', 'input_sha_match',
                           'input_order_match', 'qc_passed', 'website_unlimited'), True)
        p.update(credits_cost=0, quantity=1, resolution=720, aspect_ratio='16:9')
        self.item = {'id': 'S-example', 'state': 'claimed', 'board_id': BOARD,
                     'claim': {'claim_id': 'unique-claim', 'execution_instance_id': A,
                               'route_generation': 7, 'preflight': p}}

    def intent(self, **over):
        return lc.prepare_intent(over.get('cfg', self.cfg), over.get('lock', self.lock),
                                 over.get('item', self.item), over.get('actor', self.actor),
                                 over.get('scan', self.scan), over.get('now', NOW),
                                 queue_board_id=over.get('queue_board_id'),
                                 ledger=over.get('ledger', run_ledger.empty()))

    # --- identity -----------------------------------------------------------
    def test_holder_is_own_unique_minimax_namespace(self):
        self.assertEqual(lc.holder(self.actor), 'minimax:' + A)
        self.assertNotIn('chatgpt', lc.holder(self.actor))
        self.assertNotEqual(lc.holder(self.actor), lc.holder(dict(self.actor, execution_instance_id=B)))

    def test_minimax_is_a_known_surface(self):
        self.assertIn('minimax', lc.SURFACES)

    def test_runtime_run_id_must_be_real_not_local_uuid(self):
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, dict(self.actor, provider_run_id=A))
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, dict(self.actor, provider_run_id=''))
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, {k: v for k, v in self.actor.items() if k != 'provider_run_id'})

    def test_transport_must_match_own_policy(self):
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, dict(self.actor, transport='grok_chat'))

    # --- route / peer / lease guards ---------------------------------------
    def test_disabled_peer_blocks_create(self):
        self.cfg['peers']['minimax']['enabled'] = False
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, self.actor)

    def test_disabled_launcher_policy_blocks_create(self):
        self.cfg['minimax_launcher']['enabled'] = False
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, self.actor)

    def test_route_generation_change_blocks_create(self):
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, dict(self.actor, route_generation=6))

    def test_foreign_lease_blocks_create(self):
        with self.assertRaises(lc.Blocked):
            lc.check_lease(self.lock, dict(self.actor, execution_instance_id=B), NOW)

    def test_expired_lease_blocks_create(self):
        self.lock['expires_at'] = lc.stamp(NOW)
        with self.assertRaises(lc.Blocked):
            lc.check_lease(self.lock, self.actor, NOW)

    def test_generic_lock_holder_is_not_own_lease(self):
        self.lock['holder'] = 'chatgpt'
        with self.assertRaises(lc.Blocked):
            lc.check_lease(self.lock, self.actor, NOW)

    def test_interactive_shift_must_be_transferred_to_this_session(self):
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, dict(self.actor, session_id='other-session', foreground_epoch=1))
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, dict(self.actor, foreground_epoch=0))

    # --- launch policy ------------------------------------------------------
    def test_first_real_create_needs_owner_go_ahead(self):
        self.cfg['minimax_launcher']['first_real_create'] = {'owner_go_ahead': False}
        with self.assertRaises(lc.Blocked):
            self.intent(lock=self.lock, item=self.item, actor=self.actor, scan=self.scan, now=NOW)

    def test_board_outside_own_scope_is_blocked(self):
        item = dict(self.item, board_id='other-board')
        with self.assertRaises(lc.Blocked):
            self.intent(lock=self.lock, item=item, actor=self.actor, scan=self.scan, now=NOW)

    def test_paid_price_blocks_create(self):
        item = copy.deepcopy(self.item)
        item['claim']['preflight']['credits_cost'] = 1
        with self.assertRaises(lc.Blocked):
            self.intent(lock=self.lock, item=item, actor=self.actor, scan=self.scan, now=NOW)

    def test_incomplete_inputs_block_create(self):
        for key in ('owner_authorized', 'prompt_match', 'input_sha_match',
                    'input_order_match', 'qc_passed', 'website_unlimited'):
            item = copy.deepcopy(self.item)
            item['claim']['preflight'][key] = False
            with self.subTest(key=key), self.assertRaises(lc.Blocked):
                self.intent(lock=self.lock, item=item, actor=self.actor, scan=self.scan, now=NOW)

    def test_per_wake_budget_is_enforced(self):
        actor = dict(self.actor, submissions_this_wake=6)
        with self.assertRaises(lc.Blocked):
            self.intent(lock=self.lock, item=self.item, actor=actor, scan=self.scan, now=NOW)

    def test_no_budget_without_owner_granted_cap(self):
        self.cfg['minimax_launcher']['max_submissions_per_wake'] = None
        with self.assertRaises(lc.Blocked):
            self.intent(lock=self.lock, item=self.item, actor=self.actor, scan=self.scan, now=NOW)

    # --- replay / unknown outcome ------------------------------------------
    def test_single_durable_intent_is_not_replayed(self):
        out = self.intent(lock=self.lock, item=self.item, actor=self.actor, scan=self.scan, now=NOW)
        self.assertEqual(out['state'], 'submitting')
        with self.assertRaises(lc.Blocked):
            self.intent(lock=self.lock, item=out, actor=self.actor, scan=self.scan, now=NOW)

    def test_unknown_submission_outcome_is_never_repeated(self):
        for state in ('submission_unknown', 'submitted', 'completed'):
            with self.subTest(state=state), self.assertRaises(lc.Blocked):
                self.intent(item=dict(self.item, state=state))

    def test_other_claim_is_blocked(self):
        item = copy.deepcopy(self.item)
        item['claim']['execution_instance_id'] = B
        with self.assertRaises(lc.Blocked):
            self.intent(lock=self.lock, item=item, actor=self.actor, scan=self.scan, now=NOW)

    def test_minimax_interactive_shift_requires_owner_takeover(self):
        actor = dict(self.actor, kind='interactive', session_id='minimax-session-2')
        out = lc.takeover(self.cfg, self.lock, actor, NOW, 'Прими смену')
        self.assertEqual(out['foreground_owners']['minimax']['epoch'], 2)
        self.assertEqual(out['peers'], self.cfg['peers'])
        self.assertEqual(out['route_generation'], self.cfg['route_generation'])
        with self.assertRaises(lc.Blocked):
            lc.check_route(out, dict(actor, foreground_epoch=1))
        self.assertTrue(lc.check_route(out, dict(actor, foreground_epoch=2)))

    # --- no inheritance from Grok ------------------------------------------
    def test_owner_command_is_grok_only(self):
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, dict(self.actor, kind='owner_command',
                                          owner_command={'source': 'grok_chat'}))

    def test_grok_window_and_wake_issue_do_not_apply_to_minimax(self):
        self.cfg['grok_launcher'] = {
            'launch_window': {'timezone': 'Europe/Amsterdam', 'first_hour': 8, 'last_hour': 23,
                              'first_minute': 10, 'last_minute': 40},
            'first_real_create': {'owner_go_ahead': True},
            'board_id': BOARD, 'max_submissions_per_wake': 6, 'slot_capacity': 6,
        }
        # Outside the Grok window (23:59 Europe/Amsterdam) Minimax is unaffected by it.
        late = datetime(2026, 11, 18, 22, 59, tzinfo=timezone.utc)
        lock = {'state': 'held', 'holder': lc.holder(self.actor),
                'acquired_at': lc.stamp(late - timedelta(minutes=1)),
                'expires_at': lc.stamp(late + timedelta(minutes=5))}
        scan = dict(self.scan, checked_at=lc.stamp(late))
        actor = dict(self.actor, lease_acquired_at=lock['acquired_at'])
        self.assertTrue(lc.check_route(self.cfg, actor))
        out = self.intent(lock=lock, item=self.item, actor=actor, scan=scan, now=late)
        self.assertEqual(out['state'], 'submitting')

    def test_minimax_never_uses_the_grok_wake_issue_shortcut(self):
        """A Grok wake issue is dead data for Minimax: it grants no window bypass and no trigger."""
        self.assertIsNone(self.cfg['minimax_launcher']['wake_issue'])
        out = self.intent(actor=dict(self.actor, wake_issue=42))
        self.assertEqual(out['state'], 'submitting')
        self.assertNotIn('trigger', out['claim'])
        self.assertNotIn('wake_issue', out['claim'])

    def test_minimax_retry_budget_is_not_inherited(self):
        self.cfg['minimax_launcher']['retry_budget'] = {'enabled': False}
        item = copy.deepcopy(self.item)
        item['submission_history'] = [{'task_id': 'x'}]
        with self.assertRaises(lc.Blocked):
            self.intent(lock=self.lock, item=item, actor=self.actor, scan=self.scan, now=NOW)


class MinimaxRegistryTests(unittest.TestCase):
    """The live registry must keep every existing peer, claim, intent and budget intact."""

    def setUp(self):
        self.cfg = json.loads((REPO / 'ops' / 'slot-backup.json').read_text(encoding='utf-8'))

    def test_minimax_peer_is_registered_as_read_only(self):
        peer = self.cfg['peers']['minimax']
        self.assertIs(peer['enabled'], True)
        self.assertEqual(peer['role'], 'read_only')
        self.assertEqual(peer['automation_ids'], [])
        self.assertEqual(peer['receipt'], 'reports/slack-events.json')
        self.assertIsNone(peer['runtime_run_id'])
        self.assertTrue(peer['runtime_run_id_unavailable_reason'])
        for forbidden in ('claim', 'lease', 'intent', 'create', 'site_submit'):
            self.assertIn(forbidden, peer['forbidden'])

    def test_minimax_launcher_policy_starts_disabled(self):
        policy = self.cfg['minimax_launcher']
        self.assertIs(policy['enabled'], False)
        self.assertIs(policy['first_real_create']['owner_go_ahead'], False)
        self.assertIsNone(policy['max_submissions_per_wake'])
        self.assertIs(policy['unlimited_zero_only'], True)
        self.assertEqual(policy['board_id'], BOARD)

    def test_read_only_peer_is_not_a_required_ledger_surface(self):
        # The ledger records real submission attempts; a read-only peer makes none.
        self.assertNotIn('minimax', self.cfg['run_ledger']['required_surfaces'])
        self.assertIn('grok', self.cfg['run_ledger']['required_surfaces'])
        self.assertTrue(self.cfg['run_ledger'].get('required_surfaces_note'))

    def test_read_only_policy_is_registered_and_bounded(self):
        policy = self.cfg['minimax_read_only']
        self.assertIs(policy['enabled'], True)
        self.assertEqual(policy['role'], 'read_only')
        self.assertIsNone(policy['max_submissions_per_wake'])
        self.assertEqual(policy['new_video_submissions'], 0)
        command = policy['owner_command']
        self.assertIs(command['enabled'], True)
        self.assertEqual(command['sources'], ['slack'])
        self.assertIs(command['require_mention'], True)
        self.assertIs(command['accept_unaddressed'], False)
        self.assertEqual(command['max_age_minutes'], 60)

    def test_existing_peers_and_budgets_are_untouched(self):
        self.assertIs(self.cfg['peers']['ordinary']['enabled'], True)
        self.assertIs(self.cfg['peers']['work']['enabled'], True)
        self.assertIs(self.cfg['peers']['grok']['enabled'], True)
        self.assertEqual(self.cfg['grok_launcher']['max_submissions_per_wake'], 6)
        self.assertEqual(self.cfg['grok_launcher']['slot_capacity'], 6)
        self.assertEqual(self.cfg['route_generation'], 7)

    def test_holder_template_names_the_minimax_namespace(self):
        self.assertIn('minimax:', self.cfg['ownership']['holder_template'])


SLACK_CHANNEL = 'C0CBQT4H50E'
SLACK_OWNER = 'U0CBWH0DXKN'
SLACK_BOT = 'U0CJWT05HBM'

READ_ONLY_POLICY = {
    'enabled': True,
    'role': 'read_only',
    'transport': ['interactive_chat', 'slack'],
    'owner_command': {
        'enabled': True,
        'sources': ['slack'],
        'require_mention': True,
        'accept_unaddressed': False,
        'slack_channel_id': SLACK_CHANNEL,
        'slack_owner_user_id': SLACK_OWNER,
        'slack_bot_user_id': SLACK_BOT,
        'max_age_minutes': 60,
    },
}


class MinimaxReadOnlyPeerTests(unittest.TestCase):
    """Owner decision 19.11.2026: the Minimax peer is read-only and answers Slack commands."""

    def setUp(self):
        self.cfg = {
            'enabled': True, 'route_generation': 7,
            'peers': {
                'ordinary': {'enabled': True, 'automation_ids': ['ordinary-task']},
                'work': {'enabled': True, 'automation_ids': ['work-task']},
                'grok': {'enabled': True, 'automation_ids': ['topview-grok']},
                'minimax': {'enabled': True, 'role': 'read_only', 'automation_ids': [],
                            'receipt': 'reports/slack-events.json'},
            },
            'minimax_read_only': copy.deepcopy(READ_ONLY_POLICY),
            'minimax_launcher': {'enabled': False},
            'run_ledger': {'required_surfaces': ['grok']},
        }
        self.actor = {
            'execution_instance_id': A, 'surface': 'minimax', 'kind': 'owner_read',
            'route_generation': 7, 'transport': 'slack',
            'owner_command': {
                'quote': '<@U0CJWT05HBM> кто на связи?',
                'source': 'slack', 'at': lc.stamp(NOW - timedelta(minutes=2)),
                'channel_id': SLACK_CHANNEL, 'user_id': SLACK_OWNER,
                'message_id': '1795053600.000100',
            },
        }

    def test_read_only_command_passes_the_route(self):
        self.assertTrue(lc.check_route(self.cfg, self.actor, NOW))

    def test_read_only_command_needs_no_provider_run_id(self):
        actor = {k: v for k, v in self.actor.items() if k != 'provider_run_id'}
        self.assertTrue(lc.check_route(self.cfg, actor, NOW))

    def test_command_from_another_channel_is_blocked(self):
        actor = copy.deepcopy(self.actor)
        actor['owner_command']['channel_id'] = 'C0OTHER'
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_route(self.cfg, actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_owner_command_channel_mismatch')

    def test_command_from_another_sender_is_blocked(self):
        actor = copy.deepcopy(self.actor)
        actor['owner_command']['user_id'] = 'U0CBQTGARUN'
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_route(self.cfg, actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_owner_command_sender_mismatch')

    def test_stale_command_is_blocked(self):
        actor = copy.deepcopy(self.actor)
        actor['owner_command']['at'] = lc.stamp(NOW - timedelta(minutes=90))
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_route(self.cfg, actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_owner_command_stale_or_future')

    def test_owner_read_kind_exists_only_for_minimax(self):
        actor = copy.deepcopy(self.actor)
        actor['surface'] = 'ordinary'
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_route(self.cfg, actor, NOW)
        self.assertEqual(str(raised.exception), 'owner_read_only_for_minimax')

    def test_owner_read_kind_is_refused_for_grok_too(self):
        actor = copy.deepcopy(self.actor)
        actor['surface'] = 'grok'
        with self.assertRaises(lc.Blocked):
            lc.check_route(self.cfg, actor, NOW)

    def test_read_only_peer_cannot_reach_the_launcher_route(self):
        actor = copy.deepcopy(self.actor)
        actor['kind'] = 'interactive'
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_route(self.cfg, actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_launcher_disabled')

    def test_read_only_peer_cannot_create(self):
        item = {'id': 'S-example', 'state': 'claimed', 'board_id': BOARD, 'claim': {'claim_id': 'c'}}
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_minimax_launch(self.cfg, item, self.actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_launcher_disabled')

    def test_disabled_read_only_policy_blocks_the_command(self):
        self.cfg['minimax_read_only']['enabled'] = False
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_route(self.cfg, self.actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_read_only_disabled')

    def test_transport_outside_the_policy_is_blocked(self):
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_route(self.cfg, dict(self.actor, transport='telegram'), NOW)
        self.assertEqual(str(raised.exception), 'minimax_transport_mismatch')

    def test_published_slot_backup_keeps_the_launcher_closed(self):
        config = json.loads((REPO / 'ops/slot-backup.json').read_text(encoding='utf-8'))
        peer = config['peers']['minimax']
        self.assertIs(peer['enabled'], True)
        self.assertEqual(peer['role'], 'read_only')
        self.assertIs(config['minimax_launcher']['enabled'], False)
        self.assertIs(config['minimax_read_only']['enabled'], True)
        command = config['minimax_read_only']['owner_command']
        self.assertIs(command['enabled'], True)
        self.assertIs(command['require_mention'], True)
        self.assertIs(command['accept_unaddressed'], False)
        self.assertEqual(command['slack_channel_id'], SLACK_CHANNEL)
        self.assertEqual(command['slack_owner_user_id'], SLACK_OWNER)
        self.assertEqual(command['slack_bot_user_id'], SLACK_BOT)
        self.assertNotIn('minimax', config['run_ledger']['required_surfaces'])
        for forbidden in ('claim', 'lease', 'intent', 'create', 'site_submit'):
            self.assertIn(forbidden, peer['forbidden'])


if __name__ == '__main__':
    unittest.main()
