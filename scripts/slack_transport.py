#!/usr/bin/env python3
"""Slack transport for the Minimax peer (read-only command source).

The Minimax bot application A0CK6QV1VGU is installed in the workspace Vint and
invited to the channel C0CBQT4H50E (#all-vint) with read and write scopes.
The owner controls the bot token; it is read from the environment as
SLACK_BOT_TOKEN and is never printed, logged or written to the repository.

What this module does:

* reads the channel history through conversations.history;
* accepts a message as an owner command only when every identity check holds -
  the exact channel, the exact owner user id, a human sender (no bot_id), no
  message subtype, a non-empty text;
* turns such a message into an actor for the launcher guard, carrying the exact
  quote, the channel id, the sender id, the message ts and the client_msg_id;
* keeps a receipt for every message it saw, so a repeated poll never treats the
  same message as a new command.

This module never writes to the repository and never takes the canon lock. The
caller owns both: publish receipts under the lock, exactly like the Relay does.

Owner decision 19.11.2026: the bot exists and is in the channel. Whether a
Slack message counts as a direct owner command is a separate decision and stays
disabled until the owner grants it (ops/slot-backup.json ->
minimax_launcher.owner_command_launch).
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_BASE = 'https://slack.com/api/'
DEFAULT_CHANNEL_ID = 'C0CBQT4H50E'
DEFAULT_APP_ID = 'A0CK6QV1VGU'
# The Minimax bot account in the workspace Vint, confirmed live with auth.test
# and users.info on 19.11.2026.
DEFAULT_BOT_USER_ID = 'U0CJWT05HBM'
# Message subtypes that are not the owner speaking: edits, joins, leaves, bot
# notices, thread broadcasts and anything else the platform annotates.
NON_COMMAND_SUBTYPES = (
    'bot_message', 'channel_join', 'channel_leave', 'channel_topic', 'channel_purpose',
    'channel_name', 'message_changed', 'message_deleted', 'thread_broadcast',
    'bot_message_changed', 'group_join', 'group_leave', 'file_share',
)


class TransportBlocked(ValueError):
    """A Slack identity or policy check refused the message."""


def http_post(method, token, payload=None, timeout=30):
    """Call one Slack Web API method and return its JSON body.

    Kept as a single function so tests can inject a fake and never touch the
    network.
    """
    url = API_BASE + method
    data = urllib.parse.urlencode(payload or {}).encode('utf-8')
    request = urllib.request.Request(
        url, data=data, method='POST',
        headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        raise TransportBlocked('slack_http_%s' % error.code) from error
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise TransportBlocked('slack_unreachable') from error
    if not isinstance(body, dict):
        raise TransportBlocked('slack_bad_response')
    if body.get('ok') is not True:
        raise TransportBlocked('slack_api_error_%s' % (body.get('error') or 'unknown'))
    return body


def auth_test(token, http=None):
    """Confirm which identity the token speaks with. Never returns the token."""
    call = http or http_post
    body = call('auth.test', token)
    return {
        'user_id': body.get('user_id'),
        'bot_id': body.get('bot_id'),
        'team_id': body.get('team_id'),
        'team': body.get('team'),
        'url': body.get('url'),
        'is_authorized': True,
    }


def user_info(token, user_id, http=None):
    """Profile of one workspace member (id, display name, bot flag)."""
    call = http or http_post
    body = call('users.info', token, {'user': user_id})
    user = body.get('user') or {}
    return {
        'id': user.get('id'),
        'name': user.get('name'),
        'real_name': user.get('real_name'),
        'is_bot': bool(user.get('is_bot')),
        'deleted': bool(user.get('deleted')),
    }


def read_channel(token, channel_id, oldest=None, limit=200, http=None):
    """Normalized channel history, oldest first."""
    call = http or http_post
    payload = {'channel': channel_id, 'limit': str(min(int(limit), 1000))}
    if oldest:
        payload['oldest'] = str(oldest)
    body = call('conversations.history', token, payload)
    messages = []
    for raw in body.get('messages') or []:
        if not isinstance(raw, dict):
            continue
        messages.append({
            'ts': str(raw.get('ts') or ''),
            'text': raw.get('text') or '',
            'user': raw.get('user'),
            'bot_id': raw.get('bot_id'),
            'subtype': raw.get('subtype'),
            'thread_ts': raw.get('thread_ts'),
            'client_msg_id': raw.get('client_msg_id'),
            'channel': channel_id,
        })
    messages.sort(key=lambda item: float(item['ts'] or 0))
    return messages


def mentions(text):
    """User ids mentioned in a message body, in order, without duplicates."""
    found = []
    for match in re.findall(r'<@([A-Z0-9]+)(?:\|[^>]*)?>', str(text or '')):
        if match not in found:
            found.append(match)
    return found


def classify(message, policy):
    """Decide whether a message is an owner command, and say why not when it is not.

    policy needs: channel_id, owner_user_id, bot_user_id and optionally
    owner_name and accept_unaddressed.

    The channel holds several bots, so the author alone does not make a message
    a command: the message must also be addressed to this bot. A message that
    names another bot belongs to that bot. A message that names nobody stays a
    general channel message unless the owner allows unaddressed messages.
    """
    channel_id = str(policy.get('channel_id') or '')
    owner_user_id = str(policy.get('owner_user_id') or '')
    bot_user_id = str(policy.get('bot_user_id') or '')
    if not channel_id:
        raise TransportBlocked('slack_channel_not_configured')
    if not owner_user_id:
        raise TransportBlocked('slack_owner_not_configured')
    if not bot_user_id:
        raise TransportBlocked('slack_bot_not_configured')
    if str(message.get('channel') or '') != channel_id:
        return {'kind': 'foreign_channel', 'reason': 'channel_mismatch'}
    if message.get('bot_id'):
        return {'kind': 'bot_message', 'reason': 'sender_is_bot'}
    if message.get('subtype'):
        return {'kind': 'subtype_message', 'reason': 'subtype_%s' % message.get('subtype')}
    if not str(message.get('user') or ''):
        return {'kind': 'no_user', 'reason': 'sender_unknown'}
    if str(message.get('user')) != owner_user_id:
        return {'kind': 'foreign_user', 'reason': 'sender_not_owner'}
    if not str(message.get('text') or '').strip():
        return {'kind': 'empty_text', 'reason': 'no_text'}
    if not str(message.get('ts') or ''):
        return {'kind': 'no_ts', 'reason': 'no_message_id'}
    addressed = mentions(message.get('text'))
    if bot_user_id in addressed:
        return {'kind': 'owner_command', 'reason': 'owner_addressed_this_bot'}
    if addressed:
        return {'kind': 'other_bot_addressed', 'reason': 'addressed_to_another_bot'}
    if policy.get('accept_unaddressed') is True:
        return {'kind': 'owner_command', 'reason': 'owner_unaddressed_message_allowed'}
    return {'kind': 'channel_general', 'reason': 'not_addressed_to_a_bot'}


def message_id(message):
    """Stable identity of one Slack message for dedupe and receipts."""
    return str(message.get('ts') or '')


def receipt_for(message, decision, checked_at, run_id=None, receipt_id=None):
    """One receipt per message that was seen, exactly like the Relay does."""
    return {
        'event_id': receipt_id or ('slack:%s:%s' % (message.get('channel'), message_id(message))),
        'transport': 'slack',
        'channel_id': message.get('channel'),
        'message_ts': message_id(message),
        'client_msg_id': message.get('client_msg_id'),
        'sender_user_id': message.get('user'),
        'outcome': decision.get('kind'),
        'reason': decision.get('reason'),
        'checked_at': checked_at,
        'run_id': run_id,
    }


def command_actor(message, decision, policy, now=None):
    """Build the actor for the launcher guard from a verified owner message.

    Mirrors the Telegram adapter: the original quote, the source, the moment,
    the channel and the sender id travel together, and the guard checks them
    against the recorded policy.
    """
    if decision.get('kind') != 'owner_command':
        raise TransportBlocked('not_an_owner_command')
    when = now or datetime.now(timezone.utc)
    ts_value = message_id(message)
    try:
        at = datetime.fromtimestamp(float(ts_value), tz=timezone.utc)
    except (TypeError, ValueError) as error:
        raise TransportBlocked('slack_message_ts_unparsable') from error
    return {
        'surface': 'minimax',
        'kind': 'owner_command',
        'transport': 'slack',
        'owner_command': {
            'quote': str(message.get('text') or '').strip(),
            'source': 'slack',
            'at': at.isoformat().replace('+00:00', 'Z'),
            'channel_id': str(message.get('channel')),
            'user_id': str(message.get('user')),
            'message_id': ts_value,
            'client_msg_id': message.get('client_msg_id'),
            'read_at': when.isoformat().replace('+00:00', 'Z'),
        },
    }


def post_message(token, channel_id, text, thread_ts=None, http=None):
    """Post one message to the channel. Used for ACK and reports, never for Create."""
    call = http or http_post
    payload = {'channel': channel_id, 'text': text}
    if thread_ts:
        payload['thread_ts'] = str(thread_ts)
    body = call('chat.postMessage', token, payload)
    return {'ts': body.get('ts'), 'channel': body.get('channel')}


def seen_keys(state):
    """Message keys already processed, from the stored receipt state."""
    events = (state or {}).get('events') or []
    return {str(event.get('message_ts')) for event in events if isinstance(event, dict)}


def poll(token, policy, state=None, http=None, now=None, limit=200):
    """Read the channel and return (new_messages, new_receipts).

    A message that already has a receipt is never returned again: the same
    message must not become a second command.
    """
    call = http or http_post
    when = now or datetime.now(timezone.utc)
    checked_at = when.isoformat().replace('+00:00', 'Z')
    channel_id = str(policy.get('channel_id') or '')
    if not channel_id:
        raise TransportBlocked('slack_channel_not_configured')
    oldest = None
    known = seen_keys(state)
    if known:
        oldest = max(known, key=lambda value: float(value or 0))
    messages = read_channel(token, channel_id, oldest=oldest, limit=limit, http=call)
    new_messages, receipts = [], []
    for message in messages:
        decision = classify(message, policy)
        key = message_id(message)
        if key and key in known:
            continue
        new_messages.append(message)
        receipts.append(receipt_for(message, decision, checked_at))
    return new_messages, receipts


def main(argv=None):
    parser = argparse.ArgumentParser(description='Slack transport for the Minimax peer')
    parser.add_argument('command', choices=['verify', 'read', 'poll'])
    parser.add_argument('--channel-id', default=os.environ.get('SLACK_CHANNEL_ID') or DEFAULT_CHANNEL_ID)
    parser.add_argument('--owner-user-id', default=os.environ.get('SLACK_OWNER_USER_ID') or '')
    parser.add_argument('--bot-user-id', default=os.environ.get('SLACK_BOT_USER_ID') or DEFAULT_BOT_USER_ID)
    parser.add_argument('--accept-unaddressed', action='store_true',
                        help='treat owner messages without a mention as commands')
    parser.add_argument('--limit', default='200')
    parser.add_argument('--state', default='reports/slack-events.json')
    args = parser.parse_args(argv)

    token = os.environ.get('SLACK_BOT_TOKEN')
    if not token:
        print('SLACK_BOT_TOKEN is not set in the secret store.', file=sys.stderr)
        return 3

    if args.command == 'verify':
        identity = auth_test(token)
        print(json.dumps(identity, ensure_ascii=False, indent=2))
        return 0

    state = None
    if os.path.exists(args.state):
        try:
            with open(args.state, encoding='utf-8') as handle:
                state = json.load(handle)
        except (OSError, json.JSONDecodeError):
            state = None

    policy = {'channel_id': args.channel_id, 'owner_user_id': args.owner_user_id,
              'bot_user_id': args.bot_user_id, 'accept_unaddressed': args.accept_unaddressed}
    if args.command == 'read':
        messages = read_channel(token, args.channel_id, limit=args.limit)
        print(json.dumps(messages, ensure_ascii=False, indent=2))
        return 0

    try:
        new_messages, receipts = poll(token, policy, state=state, limit=args.limit)
    except TransportBlocked as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps({
        'channel_id': args.channel_id,
        'new_messages': len(new_messages),
        'receipts': receipts,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
