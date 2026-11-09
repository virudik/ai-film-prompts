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


if __name__ == '__main__':
    unittest.main()
