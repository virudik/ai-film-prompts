import json
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import launcher_coordination as lc
import launcher_run_ledger as lr
import test_launcher_coordination as fixtures

GROK_NOW = fixtures.GROK_NOW
CONV = '1c1bf697-3c93-4068-b457-e90efdd5ef8f'
REQ = 'b74dd093-bb7c-4974-a448-a3ad21fc5241'
OLD_REQ = '92ef90b4-eece-48e7-aa5b-8f0c2ba3ef48'
ADDRESS = 't402u'
TEXT = 'Ну и сидишь и ничо не делаешь?'


def packet(at=None, request_id=REQ, conversation_id=CONV, address=ADDRESS, role='user', text=TEXT,
           observation='parent_shell_os_environ'):
    return {
        'observation_source': observation,
        'raw_host_fields': {
            'CURSOR_CONVERSATION_ID': conversation_id,
            'CURSOR_REQUEST_ID': request_id,
        },
        'owner_native_message': {
            'host_address': address, 'role': role, 'text': text,
            'at': at or lc.stamp(GROK_NOW),
        },
    }


class CursorHostOwnerCommandTests(unittest.TestCase):
    def setUp(self):
        base = fixtures.GrokHelperTests('test_holder_format')
        base.setUp()
        self.cfg, self.actor, self.lock, self.scan, self.item = (
            base.cfg, base.actor, base.lock, base.scan, base.item)
        self.cfg['run_ledger'] = {'required_surfaces': ['grok']}
        self.cfg['grok_launcher']['owner_command_launch'] = {
            'enabled': True, 'sources': ['grok_chat', 'telegram', 'cursor_host'],
            'telegram_chat_id': '215961273', 'max_age_minutes': 60, 'bypass_launch_window': True}
        self.actor.pop('provider_run_id', None)
        self.ledger = lr.empty()
        self.local_execution = self.actor['execution_instance_id']

    def actor_for(self, body):
        message = body['owner_native_message']
        return dict(self.actor, kind='owner_command', owner_command={
            'source': 'cursor_host', 'quote': message['text'], 'at': message['at'],
            'host_context': {
                'namespace': 'cursor_host',
                'observation_source': body['observation_source'],
                'raw_host_fields': body['raw_host_fields'],
                'owner_native_message': {
                    'host_address': message['host_address'],
                    'role': message['role'],
                    'text': message['text'],
                },
            },
        })

    def test_observed_parent_packet_dry_run_does_not_consume(self):
        body = packet()
        out = lc.dry_run_cursor_host(self.cfg, body, GROK_NOW, self.local_execution, self.ledger)
        self.assertTrue(out['allowed'])
        self.assertFalse(out['consumes'])
        self.assertEqual(out['host_run']['field'], 'CURSOR_REQUEST_ID')
        self.assertEqual(out['host_run']['value'], REQ)
        self.assertEqual(out['host_run']['conversation_field'], 'CURSOR_CONVERSATION_ID')
        self.assertEqual(out['host_run']['conversation_id'], CONV)
        self.assertEqual(out['host_run']['owner_host_address'], ADDRESS)
        self.assertEqual(out['host_run']['owner_host_role'], 'user')
        self.assertNotIn('provider_run_id', out['host_run'])
        self.assertEqual(self.ledger, lr.empty())
        self.assertNotEqual(REQ, OLD_REQ)
        spoken = packet(observation='parent Shell os.environ, not executor or cloud environment')
        again = lc.dry_run_cursor_host(self.cfg, spoken, GROK_NOW, self.local_execution, self.ledger)
        self.assertEqual(again['host_run']['value'], REQ)

    def test_fixture_intent_keeps_host_names_and_blocks_replay(self):
        actor = self.actor_for(packet())
        item, ledger = lc.prepare_transaction(
            self.cfg, self.lock, self.item, actor, self.scan, GROK_NOW, ledger=self.ledger)
        self.assertTrue(lr.verify_binding(item, ledger))
        self.assertIsNone(item['claim']['provider_run_id'] if 'provider_run_id' in item['claim'] else None)
        self.assertEqual(item['claim']['host_run']['value'], REQ)
        self.assertEqual(item['claim']['owner_command']['host_address'], ADDRESS)
        row = next(iter(ledger['runs'].values()))
        self.assertIsNone(row['provider_run_id'])
        self.assertEqual(row['host_run']['field'], 'CURSOR_REQUEST_ID')
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(self.cfg, self.lock, self.item, actor, self.scan, GROK_NOW, ledger=ledger)

    def test_same_address_on_another_request_is_denied(self):
        actor = self.actor_for(packet())
        _, ledger = lc.prepare_transaction(
            self.cfg, self.lock, self.item, actor, self.scan, GROK_NOW, ledger=self.ledger)
        other = self.actor_for(packet(request_id='aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee'))
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(
                self.cfg, self.lock, dict(self.item, id='other-item'), other, self.scan, GROK_NOW, ledger=ledger)

    def test_child_cloud_and_non_owner_packets_are_denied(self):
        denied = [
            packet(conversation_id='sand-subagent-1c1bf697'),
            packet(request_id='bc-b6c53856-e99b-58a2-a5e3-54a898cb355c'),
            packet(role='assistant'),
            packet(address='t399s1924'),
            packet(observation='page_text'),
        ]
        for body in denied:
            body['owner_native_message']['text'] = body['owner_native_message']['text']
            with self.subTest(body=body['raw_host_fields']['CURSOR_REQUEST_ID']), self.assertRaises(lc.Blocked):
                lc.dry_run_cursor_host(self.cfg, body, GROK_NOW, self.local_execution)

    def test_quote_must_match_host_text(self):
        body = packet()
        body['owner_native_message']['text'] = 'скопированный текст'
        actor = self.actor_for(body)
        actor['owner_command']['quote'] = TEXT
        with self.assertRaises(lc.Blocked):
            lc.check_owner_command(self.cfg, actor, GROK_NOW)

    def test_substitute_provider_run_is_denied(self):
        actor = self.actor_for(packet())
        actor['provider_run_id'] = 'minted-backend-run'
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(self.cfg, self.lock, self.item, actor, self.scan, GROK_NOW, ledger=self.ledger)

    def test_stale_command_paid_scan_and_foreign_lease_still_fail(self):
        stale = packet(at=lc.stamp(GROK_NOW - timedelta(minutes=61)))
        with self.assertRaises(lc.Blocked):
            lc.dry_run_cursor_host(self.cfg, stale, GROK_NOW, self.local_execution)
        actor = self.actor_for(packet())
        paid = dict(self.item)
        paid['claim'] = dict(self.item['claim'])
        paid['claim']['preflight'] = dict(self.item['claim']['preflight'], credits_cost=18)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(self.cfg, self.lock, paid, actor, self.scan, GROK_NOW, ledger=self.ledger)
        old_scan = dict(self.scan, checked_at=lc.stamp(GROK_NOW - timedelta(seconds=121)))
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(self.cfg, self.lock, self.item, actor, old_scan, GROK_NOW, ledger=self.ledger)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(
                self.cfg, dict(self.lock, holder='grok:foreign'), self.item, actor, self.scan, GROK_NOW,
                ledger=self.ledger)

    def test_music_ban_and_cap_remain(self):
        live = json.loads((Path(__file__).resolve().parents[1] / 'ops' / 'slot-backup.json').read_text(encoding='utf-8'))
        self.assertEqual(live['grok_launcher']['max_submissions_per_wake'], 6)
        self.assertEqual(live['grok_launcher']['slot_capacity'], 6)
        root = Path(tempfile.mkdtemp())
        (root / 'ops').mkdir()
        (root / 'ops' / 'topview-launch-queue.json').write_text(json.dumps({
            'owner_policy_20261108_t369u': {
                'effect': 'music_requires_owner_consent', 'scenes': [28, 49, 50, 51]},
            'items': []}), encoding='utf-8')
        actor = self.actor_for(packet())
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(
                self.cfg, self.lock, dict(self.item, scene_id=51), actor, self.scan, GROK_NOW,
                ledger=self.ledger, root=root)


CARD = 't408s1979'
CARD_TEXT = 'Да, внеси PR 483 в основную версию и запускай 48 P2 и 52 P2.'
CARD_REQ = 'eb1533d4-dc87-4a0c-ad56-ae7f8fe88386'


def card_packet(request_id=CARD_REQ, role='user', text=CARD_TEXT, address=CARD, message_address=None,
                observation='parent_shell_os_environ', at=None):
    return {
        'observation_source': observation,
        'CURSOR_CONVERSATION_ID': CONV,
        'CURSOR_REQUEST_ID': request_id,
        'owner_response_role': role,
        'owner_response_text': text,
        'owner_response_to_card_address': address,
        'owner_response_at': at or lc.stamp(GROK_NOW),
        'current_owner_response_message_address': message_address,
    }


class AnsweredCardTests(unittest.TestCase):
    setUp = CursorHostOwnerCommandTests.setUp
    def test_real_card_answer_is_not_a_tnu_and_does_not_consume(self):
        body = card_packet()
        out = lc.dry_run_cursor_host(self.cfg, body, GROK_NOW, self.local_execution, self.ledger)
        self.assertTrue(out['allowed'])
        self.assertFalse(out['consumes'])
        self.assertEqual(out['host_run']['owner_response_kind'], 'answered_card')
        self.assertEqual(out['host_run']['owner_response_to_card_address'], CARD)
        self.assertIsNone(out['host_run']['current_owner_response_message_address'])
        self.assertEqual(out['host_run']['value'], CARD_REQ)
        self.assertEqual(out['host_run']['conversation_id'], CONV)
        self.assertNotIn('owner_host_address', out['host_run'])
        self.assertEqual(self.ledger, lr.empty())

    def test_card_value_is_still_rejected_as_an_owner_message_address(self):
        body = packet(address=CARD)
        with self.assertRaises(lc.Blocked):
            lc.dry_run_cursor_host(self.cfg, body, GROK_NOW, self.local_execution)

    def test_card_without_user_answer_page_child_and_fake_message_are_denied(self):
        denied = [
            card_packet(role='assistant'),
            card_packet(text=''),
            card_packet(observation='page_text'),
            card_packet(request_id='sand-subagent-eb1533d4'),
            card_packet(message_address='t408u'),
            card_packet(address='t408u'),
        ]
        for body in denied:
            with self.subTest(address=body['owner_response_to_card_address'], role=body['owner_response_role']), self.assertRaises(lc.Blocked):
                lc.dry_run_cursor_host(self.cfg, body, GROK_NOW, self.local_execution)

    def test_same_card_on_another_request_is_denied(self):
        actor = dict(self.actor)
        quote, at, context = lc._cursor_host_context(card_packet())
        actor['owner_command'] = {'source': 'cursor_host', 'quote': quote, 'at': at, 'host_context': context}
        actor['kind'] = 'owner_command'
        _, ledger = lc.prepare_transaction(
            self.cfg, self.lock, self.item, actor, self.scan, GROK_NOW, ledger=self.ledger)
        quote, at, context = lc._cursor_host_context(card_packet(request_id='aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee'))
        other = dict(actor, owner_command={'source': 'cursor_host', 'quote': quote, 'at': at, 'host_context': context})
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(
                self.cfg, self.lock, dict(self.item, id='other-item'), other, self.scan, GROK_NOW, ledger=ledger)

    def test_stale_card_answer_is_denied(self):
        body = card_packet(at=lc.stamp(GROK_NOW - timedelta(minutes=61)))
        with self.assertRaises(lc.Blocked):
            lc.dry_run_cursor_host(self.cfg, body, GROK_NOW, self.local_execution)


STANDING_QUOTE = 'Говорю запускай значит запускай. Зачем спрашивать по 10 раз если есть уже согласованная очередь запуска'


class StandingCommandTests(CursorHostOwnerCommandTests):
    def setUp(self):
        super().setUp()
        self.cfg['grok_launcher']['owner_command_launch']['standing_commands'] = [{
            'id': 't413u-20261109', 'enabled': True, 'host_address': 't413u',
            'recorded_at': '2026-11-09T09:25:00+01:00', 'quote': STANDING_QUOTE,
            'scope': {'ready_story_parts': True, 'free_unlimited': True, 'one_attempt': True,
                      'music_dance': False, 'excluded_scenes': [28, 49, 50, 51], 'hold_scenes': [62]}}]

    def story(self, **over):
        item = dict(self.item, scene_id=52, max_new_submissions=1, max_credits=0)
        item.update(over)
        return item

    def standing_actor(self, request_id='cccccccc-dddd-4eee-8fff-000000000001', at=None, standing_id='t413u-20261109'):
        body = {
            'observation_source': 'parent_shell_os_environ',
            'raw_host_fields': {'CURSOR_CONVERSATION_ID': CONV, 'CURSOR_REQUEST_ID': request_id},
            'standing_command': {'id': standing_id},
            'quote': STANDING_QUOTE,
            'at': at or lc.stamp(GROK_NOW - timedelta(days=8)),
        }
        quote, at, context = lc._cursor_host_context(body)
        return dict(self.actor, kind='owner_command', owner_command={
            'source': 'cursor_host', 'quote': quote, 'at': at, 'host_context': context})

    def test_old_standing_phrase_authorizes_a_fresh_parent_request(self):
        actor = self.standing_actor()
        out = lc.dry_run_cursor_host(self.cfg, {
            'observation_source': 'parent_shell_os_environ',
            'raw_host_fields': actor['owner_command']['host_context']['raw_host_fields'],
            'standing_command': {'id': 't413u-20261109'},
            'quote': STANDING_QUOTE,
            'at': actor['owner_command']['at'],
        }, GROK_NOW, self.local_execution, self.ledger)
        self.assertTrue(out['allowed'])
        self.assertEqual(out['host_run']['standing_command_id'], 't413u-20261109')
        self.assertNotIn('owner_host_address', out['host_run'])
        self.assertEqual(self.ledger, lr.empty())
        item, ledger = lc.prepare_transaction(
            self.cfg, self.lock, self.story(), actor, self.scan, GROK_NOW, ledger=self.ledger)
        self.assertEqual(item['claim']['owner_command']['standing_command_id'], 't413u-20261109')
        self.assertEqual(item['claim']['owner_command']['standing_host_address'], 't413u')
        self.assertTrue(lr.verify_binding(item, ledger))
        again = self.standing_actor(request_id='dddddddd-eeee-4fff-8aaa-111111111111')
        second, _ = lc.prepare_transaction(
            self.cfg, self.lock, self.story(id='S-next'), again, self.scan, GROK_NOW, ledger=ledger)
        self.assertEqual(second['claim']['host_run']['value'], 'dddddddd-eeee-4fff-8aaa-111111111111')

    def test_same_request_cannot_reset_its_counter(self):
        actor = self.standing_actor()
        _, ledger = lc.prepare_transaction(
            self.cfg, self.lock, self.story(), actor, self.scan, GROK_NOW, ledger=self.ledger)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(
                self.cfg, self.lock, self.story(id='S-other'), actor, self.scan, GROK_NOW, ledger=ledger)

    def test_original_address_stays_single_use(self):
        native = self.actor_for(packet(address='t413u', text='Говорю запускай значит запускай'))
        _, ledger = lc.prepare_transaction(
            self.cfg, self.lock, self.story(), native, self.scan, GROK_NOW, ledger=self.ledger)
        replay = self.actor_for(packet(
            address='t413u', text='Говорю запускай значит запускай',
            request_id='aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee'))
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(
                self.cfg, self.lock, self.story(id='S-other'), replay, self.scan, GROK_NOW, ledger=ledger)
        standing = self.standing_actor()
        item, _ = lc.prepare_transaction(
            self.cfg, self.lock, self.story(id='S-fresh'), standing, self.scan, GROK_NOW, ledger=ledger)
        self.assertEqual(item['claim']['host_run']['standing_command_id'], 't413u-20261109')

    def test_t601_consent_lets_scene_28_through_and_leaves_other_music_denied(self):
        actor = self.standing_actor()
        consent = {'owner_music_consent': True, 'owner_music_consent_record': {'id': 'owner-20261113-t601u'}}
        dance = self.story(scene_id=28, id='S28-A4-20261023', **consent)
        item, _ = lc.prepare_transaction(
            self.cfg, self.lock, dance, actor, self.scan, GROK_NOW, ledger=self.ledger)
        self.assertEqual(item['claim']['owner_command']['standing_command_id'], 't413u-20261109')
        denied = [
            self.story(scene_id=28, id='S28-bare'),
            self.story(scene_id=49, id='S49B', **consent),
            self.story(scene_id=51, id='S51E', **consent),
        ]
        for item in denied:
            with self.subTest(item=item['id']), self.assertRaises(lc.Blocked):
                lc.prepare_transaction(
                    self.cfg, self.lock, item, self.standing_actor(request_id='eeeeeeee-ffff-4000-8000-222222222222'),
                    self.scan, GROK_NOW, ledger=self.ledger)

    def test_music_hold_budget_scan_and_child_env_still_fail(self):
        actor = self.standing_actor()
        for item in (self.story(scene_id=51), self.story(scene_id=62),
                     self.story(max_new_submissions=2), self.story(max_credits=1)):
            with self.subTest(item=item.get('scene_id'), budget=item.get('max_new_submissions')), self.assertRaises(lc.Blocked):
                lc.prepare_transaction(self.cfg, self.lock, item, actor, self.scan, GROK_NOW, ledger=self.ledger)
        old_scan = dict(self.scan, checked_at=lc.stamp(GROK_NOW - timedelta(seconds=121)))
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(self.cfg, self.lock, self.story(), actor, old_scan, GROK_NOW, ledger=self.ledger)
        paid = self.story()
        paid['claim'] = dict(self.item['claim'])
        paid['claim']['preflight'] = dict(self.item['claim']['preflight'], credits_cost=18)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(self.cfg, self.lock, paid, actor, self.scan, GROK_NOW, ledger=self.ledger)
        with self.assertRaises(lc.Blocked):
            lc.dry_run_cursor_host(self.cfg, {
                'observation_source': 'parent_shell_os_environ',
                'raw_host_fields': {'CURSOR_CONVERSATION_ID': CONV, 'CURSOR_REQUEST_ID': 'bc-not-a-parent'},
                'standing_command': {'id': 't413u-20261109'},
                'quote': STANDING_QUOTE, 'at': lc.stamp(GROK_NOW)}, GROK_NOW, self.local_execution)
        future = self.standing_actor(at=lc.stamp(GROK_NOW + timedelta(minutes=5)))
        with self.assertRaises(lc.Blocked):
            lc.check_owner_command(self.cfg, future, GROK_NOW)
        unknown = self.standing_actor(standing_id='not-recorded')
        with self.assertRaises(lc.Blocked):
            lc.check_owner_command(self.cfg, unknown, GROK_NOW)

    def test_live_registry_records_t413u_and_the_t414u_yes(self):
        live = json.loads((Path(__file__).resolve().parents[1] / 'ops' / 'slot-backup.json').read_text(encoding='utf-8'))
        row = live['grok_launcher']['owner_command_launch']['standing_commands'][0]
        self.assertEqual(row['id'], 't413u-20261109')
        self.assertEqual(row['host_address'], 't413u')
        self.assertEqual(row['quote'], STANDING_QUOTE)
        self.assertEqual(row['owner_confirmation']['host_address'], 't414u')
        self.assertEqual(row['owner_confirmation']['quote'], 'Да')
        self.assertEqual(row['scope']['hold_scenes'], [62])
        self.assertEqual(row['scope']['excluded_scenes'], [28, 49, 50, 51])
        self.assertEqual(live['grok_launcher']['max_submissions_per_wake'], 6)


if __name__ == '__main__':
    unittest.main()
