import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import launcher_coordination as lc
import slack_transport as st

OWNER = 'U0CBWH0DXKN'
OTHER = 'U0CBQTGARUN'
DOT = 'U0CJUKDTLJ2'
BOT = 'U0CJWT05HBM'
CHANNEL = 'C0CBQT4H50E'
POLICY = {'channel_id': CHANNEL, 'owner_user_id': OWNER, 'bot_user_id': BOT}
NOW = datetime(2026, 11, 19, 3, 0, tzinfo=timezone.utc)


def fake_http(responses):
    """A stand-in for http_post that records the calls and replays fixed bodies."""
    calls = []

    def call(method, token, payload=None, timeout=30):
        calls.append({'method': method, 'token': token, 'payload': payload or {}})
        body = responses.get(method)
        if body is None:
            raise st.TransportBlocked('slack_api_error_%s' % method)
        return body

    call.calls = calls
    return call


def owner_message(ts='1795053600.000100', text='<@U0CJWT05HBM> Запусти S89D-WAN30-R2', **extra):
    message = {
        'ts': ts, 'text': text, 'user': OWNER, 'channel': CHANNEL,
        'bot_id': None, 'subtype': None, 'thread_ts': None,
        'client_msg_id': 'cmid-' + ts,
    }
    message.update(extra)
    return message


class SlackTransportTests(unittest.TestCase):
    """The Slack transport must accept only the owner's own message in the agreed channel."""

    def test_auth_test_reports_identity_without_the_token(self):
        http = fake_http({'auth.test': {'ok': True, 'user_id': 'U0MINIMAX', 'bot_id': 'B0MINIMAX',
                                        'team_id': 'T0CBMHB1CS1', 'team': 'Vint', 'url': 'https://vint.slack.com/'}})
        identity = st.auth_test('xoxb-secret-token', http=http)
        self.assertEqual(identity['user_id'], 'U0MINIMAX')
        self.assertEqual(identity['team'], 'Vint')
        self.assertNotIn('xoxb-secret-token', json.dumps(identity))
        self.assertEqual(http.calls[0]['method'], 'auth.test')

    def test_read_channel_normalizes_and_sorts_by_ts(self):
        http = fake_http({'conversations.history': {'ok': True, 'messages': [
            {'ts': '1795053602.000100', 'text': 'later', 'user': OWNER},
            {'ts': '1795053601.000100', 'text': 'earlier', 'user': OWNER},
        ]}})
        messages = st.read_channel('tok', CHANNEL, http=http)
        self.assertEqual([m['text'] for m in messages], ['earlier', 'later'])
        self.assertEqual(messages[0]['channel'], CHANNEL)
        self.assertEqual(messages[0]['client_msg_id'], None)

    def test_owner_message_addressed_to_this_bot_is_a_command(self):
        decision = st.classify(owner_message(), POLICY)
        self.assertEqual(decision['kind'], 'owner_command')
        self.assertEqual(decision['reason'], 'owner_addressed_this_bot')

    def test_owner_message_addressed_to_another_bot_is_not_my_command(self):
        decision = st.classify(owner_message(text='<@U0CJUKDTLJ2> Dot, отвечай по очереди'), POLICY)
        self.assertEqual(decision['kind'], 'other_bot_addressed')
        self.assertEqual(decision['reason'], 'addressed_to_another_bot')

    def test_unaddressed_owner_message_stays_a_general_channel_message(self):
        decision = st.classify(owner_message(text='кто на связи?'), POLICY)
        self.assertEqual(decision['kind'], 'channel_general')
        self.assertEqual(decision['reason'], 'not_addressed_to_a_bot')

    def test_unaddressed_owner_message_becomes_a_command_only_when_the_owner_allows_it(self):
        policy = dict(POLICY, accept_unaddressed=True)
        decision = st.classify(owner_message(text='кто на связи?'), policy)
        self.assertEqual(decision['kind'], 'owner_command')
        self.assertEqual(decision['reason'], 'owner_unaddressed_message_allowed')

    def test_mention_of_me_and_of_another_bot_is_my_command(self):
        decision = st.classify(owner_message(text='<@U0CJUKDTLJ2> <@U0CJWT05HBM> оба отвечаем'), POLICY)
        self.assertEqual(decision['kind'], 'owner_command')

    def test_mentions_are_parsed_from_the_text(self):
        self.assertEqual(st.mentions('<@U0CJUKDTLJ2> <@U0CJWT05HBM> привет'), [DOT, BOT])
        self.assertEqual(st.mentions('без упоминаний'), [])

    def test_message_from_another_member_is_refused(self):
        decision = st.classify(owner_message(user=OTHER), POLICY)
        self.assertEqual(decision['kind'], 'foreign_user')
        self.assertEqual(decision['reason'], 'sender_not_owner')

    def test_bot_message_is_refused(self):
        decision = st.classify(owner_message(bot_id='B0MINIMAX'), POLICY)
        self.assertEqual(decision['kind'], 'bot_message')

    def test_edited_or_joined_message_is_refused(self):
        decision = st.classify(owner_message(subtype='message_changed'), POLICY)
        self.assertEqual(decision['kind'], 'subtype_message')

    def test_message_from_another_channel_is_refused(self):
        decision = st.classify(owner_message(channel='C0OTHER'), POLICY)
        self.assertEqual(decision['kind'], 'foreign_channel')

    def test_empty_text_is_refused(self):
        decision = st.classify(owner_message(text='   '), POLICY)
        self.assertEqual(decision['kind'], 'empty_text')

    def test_missing_owner_or_channel_configuration_blocks(self):
        with self.assertRaises(st.TransportBlocked):
            st.classify(owner_message(), {'owner_user_id': OWNER})
        with self.assertRaises(st.TransportBlocked):
            st.classify(owner_message(), {'channel_id': CHANNEL})
        with self.assertRaises(st.TransportBlocked):
            st.classify(owner_message(), {'channel_id': CHANNEL, 'owner_user_id': OWNER})

    def test_command_actor_carries_quote_channel_sender_and_message_id(self):
        actor = st.command_actor(owner_message(), st.classify(owner_message(), POLICY), POLICY, now=NOW)
        command = actor['owner_command']
        self.assertEqual(actor['surface'], 'minimax')
        self.assertEqual(actor['kind'], 'owner_command')
        self.assertEqual(command['source'], 'slack')
        self.assertEqual(command['quote'], '<@U0CJWT05HBM> Запусти S89D-WAN30-R2')
        self.assertEqual(command['channel_id'], CHANNEL)
        self.assertEqual(command['user_id'], OWNER)
        self.assertEqual(command['message_id'], '1795053600.000100')
        self.assertTrue(command['at'].endswith('Z'))

    def test_command_actor_refuses_a_foreign_message(self):
        decision = st.classify(owner_message(user=OTHER), POLICY)
        with self.assertRaises(st.TransportBlocked):
            st.command_actor(owner_message(user=OTHER), decision, POLICY)

    def test_poll_returns_each_message_once_and_writes_a_receipt(self):
        http = fake_http({'conversations.history': {'ok': True, 'messages': [
            {'ts': '1795053600.000100', 'text': '<@U0CJWT05HBM> Запусти', 'user': OWNER},
        ]}})
        messages, receipts = st.poll('tok', POLICY, state=None, http=http)
        self.assertEqual(len(messages), 1)
        self.assertEqual(len(receipts), 1)
        receipt = receipts[0]
        self.assertEqual(receipt['outcome'], 'owner_command')
        self.assertEqual(receipt['transport'], 'slack')
        self.assertEqual(receipt['channel_id'], CHANNEL)
        self.assertEqual(receipt['message_ts'], '1795053600.000100')
        self.assertTrue(receipt['event_id'].startswith('slack:'))
        self.assertNotIn('tok', json.dumps(receipt))

    def test_poll_never_reports_the_same_message_twice(self):
        http = fake_http({'conversations.history': {'ok': True, 'messages': [
            {'ts': '1795053600.000100', 'text': '<@U0CJWT05HBM> Запусти', 'user': OWNER},
        ]}})
        state = {'events': [{'message_ts': '1795053600.000100'}]}
        messages, receipts = st.poll('tok', POLICY, state=state, http=http)
        self.assertEqual(messages, [])
        self.assertEqual(receipts, [])
        # the second poll asks Slack only for messages after the known one
        self.assertEqual(http.calls[0]['payload'].get('oldest'), '1795053600.000100')

    def test_poll_records_foreign_speakers_without_treating_them_as_commands(self):
        http = fake_http({'conversations.history': {'ok': True, 'messages': [
            {'ts': '1795053600.000100', 'text': 'привет', 'user': OTHER},
        ]}})
        messages, receipts = st.poll('tok', POLICY, state=None, http=http)
        self.assertEqual(len(messages), 1)
        self.assertEqual(receipts[0]['outcome'], 'foreign_user')

    def test_post_message_uses_the_channel_and_thread(self):
        http = fake_http({'chat.postMessage': {'ok': True, 'ts': '1795053605.000100', 'channel': CHANNEL}})
        result = st.post_message('tok', CHANNEL, 'ACK', thread_ts='1795053600.000100', http=http)
        self.assertEqual(result['ts'], '1795053605.000100')
        payload = http.calls[0]['payload']
        self.assertEqual(payload['channel'], CHANNEL)
        self.assertEqual(payload['text'], 'ACK')
        self.assertEqual(payload['thread_ts'], '1795053600.000100')


class MinimaxSlackCommandGuardTests(unittest.TestCase):
    """A Slack command reaches the launcher only through a recorded, enabled policy."""

    def setUp(self):
        self.policy = {
            'enabled': True,
            'sources': ['slack'],
            'require_mention': True,
            'accept_unaddressed': False,
            'slack_channel_id': CHANNEL,
            'slack_owner_user_id': OWNER,
            'slack_bot_user_id': BOT,
            'max_age_minutes': 60,
        }
        self.actor = st.command_actor(owner_message(), st.classify(owner_message(), POLICY), POLICY, now=NOW)

    def test_disabled_policy_blocks_the_command(self):
        self.policy['enabled'] = False
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_minimax_owner_command(self.policy, self.actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_owner_command_not_authorized')

    def test_foreign_channel_blocks_the_command(self):
        self.actor['owner_command']['channel_id'] = 'C0OTHER'
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_minimax_owner_command(self.policy, self.actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_owner_command_channel_mismatch')

    def test_foreign_sender_blocks_the_command(self):
        self.actor['owner_command']['user_id'] = OTHER
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_minimax_owner_command(self.policy, self.actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_owner_command_sender_mismatch')

    def test_stale_command_blocks_the_command(self):
        old = dict(self.actor['owner_command'])
        old['at'] = '2026-11-18T20:00:00Z'
        self.actor['owner_command'] = old
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_minimax_owner_command(self.policy, self.actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_owner_command_stale_or_future')

    def test_message_without_id_blocks_the_command(self):
        self.actor['owner_command'].pop('message_id')
        with self.assertRaises(lc.Blocked) as raised:
            lc.check_minimax_owner_command(self.policy, self.actor, NOW)
        self.assertEqual(str(raised.exception), 'minimax_owner_command_message_id_required')

    def test_valid_command_passes(self):
        self.assertTrue(lc.check_minimax_owner_command(self.policy, self.actor, NOW))


if __name__ == '__main__':
    unittest.main()
