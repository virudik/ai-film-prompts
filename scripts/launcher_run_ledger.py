#!/usr/bin/env python3
"""Durable one-Create budget per provider run and owner message.

Pure validation, NOT Telegram authentication. The adapter must obtain the original
message/run from its authenticated provider, never from page text. Publish the
returned ledger and queue intent atomically under the exact canon lease. Consumed
keys have no TTL and are never removed when an outcome is unknown or failed.
"""
import copy
import hashlib
import json
import re
from datetime import datetime, timezone

PATH = 'ops/launcher-run-ledger.json'

class LedgerBlocked(ValueError):
    pass


def required(config, actor):
    return actor.get('surface') in (config.get('run_ledger') or {}).get('required_surfaces', [])


def empty():
    return {'schema_version': 1, 'runs': {}, 'events': {}}


def opaque(value, label):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_./:@-]{1,200}', value):
        raise LedgerBlocked(label + '_required')
    return value


def key(parts):
    return hashlib.sha256(json.dumps(parts, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def validate(ledger):
    if (not isinstance(ledger, dict) or ledger.get('schema_version') != 1 or
            not isinstance(ledger.get('runs'), dict) or not isinstance(ledger.get('events'), dict)):
        raise LedgerBlocked('durable_run_ledger_missing_or_invalid')
    for rk, row in ledger['runs'].items():
        if (not isinstance(row, dict) or row.get('consumed') is not True or
                not row.get('submission_intent_id') or not row.get('item_id') or
                rk != key([row.get('surface'), row.get('provider_run_id')])):
            raise LedgerBlocked('durable_run_ledger_corrupt')
        for ek in row.get('event_keys', []):
            if ledger['events'].get(ek) != rk:
                raise LedgerBlocked('durable_event_index_corrupt')
    for ek, rk in ledger['events'].items():
        if rk not in ledger['runs'] or ek not in ledger['runs'][rk].get('event_keys', []):
            raise LedgerBlocked('durable_event_index_corrupt')
    return True


def identity(config, actor):
    surface = opaque(actor.get('surface'), 'surface')
    run = opaque(actor.get('provider_run_id'), 'real_provider_run_id')
    if run == actor.get('execution_instance_id'):
        raise LedgerBlocked('provider_run_id_must_not_be_local_execution_uuid')
    events = []
    event_record = None
    if actor.get('kind') == 'owner_command':
        command = actor.get('owner_command') or {}
        source = command.get('source')
        if source == 'telegram':
            update = command.get('telegram_update')
            if not isinstance(update, dict):
                raise LedgerBlocked('original_telegram_update_required')
            msg = update.get('message')
            if not isinstance(msg, dict) or any(k in update for k in ('edited_message', 'channel_post', 'edited_channel_post')):
                raise LedgerBlocked('original_private_message_required')
            policy = (config.get('grok_launcher') or {}).get('owner_command_launch') or {}
            owner = str(policy.get('telegram_chat_id') or '')
            chat, sender = msg.get('chat') or {}, msg.get('from') or {}
            if (not owner or chat.get('type') != 'private' or str(chat.get('id')) != owner or
                    str(sender.get('id')) != owner or sender.get('is_bot') is not False or
                    str(command.get('chat_id')) != owner):
                raise LedgerBlocked('telegram_owner_sender_mismatch')
            if any(k in msg for k in ('forward_origin', 'forward_from', 'forward_from_chat', 'forward_date', 'sender_chat', 'edit_date', 'via_bot', 'business_connection_id')):
                raise LedgerBlocked('forwarded_edited_or_indirect_command_forbidden')
            mid, uid, date = msg.get('message_id'), update.get('update_id'), msg.get('date')
            if (type(mid) is not int or mid < 1 or type(uid) is not int or uid < 0 or
                    type(date) is not int or date < 1):
                raise LedgerBlocked('telegram_message_and_update_ids_required')
            if msg.get('text') != command.get('quote'):
                raise LedgerBlocked('telegram_quote_mismatch')
            try:
                at = datetime.fromisoformat(command['at'].replace('Z', '+00:00'))
                if at.tzinfo is None or abs(at.timestamp() - date) > 1: raise ValueError()
            except (KeyError, TypeError, ValueError, AttributeError):
                raise LedgerBlocked('telegram_original_message_time_mismatch')
            events = [key(['telegram', owner, str(mid)]), key(['telegram_update', owner, str(uid)])]
            event_record = {'source': source, 'chat_id': owner, 'sender_id': owner, 'message_id': mid, 'update_id': uid}
        elif source == 'grok_chat':
            conv = opaque(command.get('conversation_id'), 'original_owner_conversation_id')
            mid = opaque(command.get('message_id'), 'original_owner_message_id')
            if command.get('sender_role') != 'owner':
                raise LedgerBlocked('original_owner_message_required')
            events = [key(['grok_chat', conv, mid])]
            event_record = {'source': source, 'conversation_id': conv, 'message_id': mid}
        else:
            raise LedgerBlocked('owner_event_source_not_allowed')
    return key([surface, run]), events, event_record


def check(config, actor, ledger):
    validate(ledger)
    rk, events, record = identity(config, actor)
    if rk in ledger['runs']:
        raise LedgerBlocked('provider_run_already_consumed_reconcile_without_Create')
    if any(ek in ledger['events'] for ek in events):
        raise LedgerBlocked('owner_message_already_consumed_reconcile_without_Create')
    return rk, events, record


def consume(config, actor, ledger, item):
    rk, events, record = check(config, actor, ledger)
    claim = item.get('claim') or {}
    if item.get('state') != 'submitting' or not claim.get('submission_intent_id'):
        raise LedgerBlocked('durable_submission_intent_required')
    out = copy.deepcopy(ledger)
    out['runs'][rk] = {
        'surface': actor['surface'], 'provider_run_id': actor['provider_run_id'],
        'automation_id': actor.get('automation_id'), 'execution_instance_id': actor['execution_instance_id'],
        'item_id': item['id'], 'submission_intent_id': claim['submission_intent_id'],
        'intent_at': claim['submission_intent_at'], 'consumed': True,
        'event_keys': events, 'owner_event': record,
        'note': 'One Create budget consumed before click; failed/unknown/expiry never reopens this key.'}
    for ek in events: out['events'][ek] = rk
    return out


def verify_binding(item, ledger):
    """Readback check before the single click, after publishing BOTH files."""
    validate(ledger)
    claim = item.get('claim') or {}
    rk = claim.get('provider_run_key')
    row = ledger['runs'].get(rk) or {}
    if (not rk or row.get('item_id') != item.get('id') or
            row.get('submission_intent_id') != claim.get('submission_intent_id') or
            row.get('execution_instance_id') != claim.get('execution_instance_id')):
        raise LedgerBlocked('queue_and_ledger_not_published_together')
    return True
