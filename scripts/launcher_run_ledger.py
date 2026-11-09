#!/usr/bin/env python3
"""Durable Create budget per real provider run and owner message.

One provider run may record several distinct items, never more than the account
slot capacity. Pure validation, NOT Telegram authentication. The adapter must
obtain the original message/run from its authenticated provider, never from page
text. Publish the returned ledger and queue intent atomically under the exact
canon lease. Consumed keys have no TTL and are never removed when an outcome is
unknown, failed, or a substantive refusal. A new provider_run_id does not reopen
a consumed item and is not how a wake exceeds its cap.
"""
import copy
import hashlib
import json
import re
from datetime import datetime, timezone

PATH = 'ops/launcher-run-ledger.json'
ACCOUNT_SLOT_CAPACITY = 6
HOST_NAMESPACE = 'cursor_host'
HOST_OBSERVATIONS = frozenset((
    'parent_shell_os_environ',
    'parent Shell os.environ, not executor or cloud environment',
))
HOST_FIELD_NAMES = ('CURSOR_CONVERSATION_ID', 'CURSOR_REQUEST_ID')
HOST_ADDRESS = re.compile(r'^t[1-9][0-9]*u$')
REJECTED_HOST_PREFIXES = ('sand-subagent-', 'bc-')

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


def submission_cap(config):
    """Finite per-wake cap. It cannot exceed the canonical account capacity of 6."""
    policy = (config or {}).get('grok_launcher') or {}
    limit, capacity = policy.get('max_submissions_per_wake'), policy.get('slot_capacity', ACCOUNT_SLOT_CAPACITY)
    if (type(limit) is not int or type(capacity) is not int or
            capacity != ACCOUNT_SLOT_CAPACITY or not 1 <= limit <= capacity):
        raise LedgerBlocked('wake_submission_cap_invalid')
    return limit


def submissions_of(row):
    """Read a batch row or a legacy one-item row. Legacy rows are not extended."""
    if not isinstance(row, dict):
        return []
    subs = row.get('submissions')
    if isinstance(subs, list):
        return subs
    if row.get('item_id') and row.get('submission_intent_id'):
        return [{'item_id': row.get('item_id'), 'submission_intent_id': row.get('submission_intent_id'),
                 'intent_at': row.get('intent_at'), 'execution_instance_id': row.get('execution_instance_id'),
                 'consumed': True}]
    return []


def validate(ledger):
    if (not isinstance(ledger, dict) or ledger.get('schema_version') != 1 or
            not isinstance(ledger.get('runs'), dict) or not isinstance(ledger.get('events'), dict)):
        raise LedgerBlocked('durable_run_ledger_missing_or_invalid')
    for rk, row in ledger['runs'].items():
        if (not isinstance(row, dict) or row.get('consumed') is not True or
                not row.get('submission_intent_id') or not row.get('item_id')):
            raise LedgerBlocked('durable_run_ledger_corrupt')
        host = row.get('host_run')
        if isinstance(host, dict):
            if (row.get('provider_run_id') is not None or
                    rk != key([row.get('surface'), HOST_NAMESPACE, host.get('field'), host.get('value')])):
                raise LedgerBlocked('durable_run_ledger_corrupt')
        elif rk != key([row.get('surface'), row.get('provider_run_id')]):
            raise LedgerBlocked('durable_run_ledger_corrupt')
        subs = row.get('submissions')
        if subs is not None:
            if not isinstance(subs, list) or not 1 <= len(subs) <= ACCOUNT_SLOT_CAPACITY:
                raise LedgerBlocked('durable_run_ledger_corrupt')
            seen = set()
            for entry in subs:
                if (not isinstance(entry, dict) or entry.get('consumed') is not True or
                        not entry.get('item_id') or not entry.get('submission_intent_id') or
                        entry['item_id'] in seen):
                    raise LedgerBlocked('durable_run_ledger_corrupt')
                seen.add(entry['item_id'])
            if (subs[0].get('item_id') != row.get('item_id') or
                    subs[0].get('submission_intent_id') != row.get('submission_intent_id')):
                raise LedgerBlocked('durable_run_ledger_corrupt')
        for ek in row.get('event_keys', []):
            if ledger['events'].get(ek) != rk:
                raise LedgerBlocked('durable_event_index_corrupt')
    for ek, rk in ledger['events'].items():
        if rk not in ledger['runs'] or ek not in ledger['runs'][rk].get('event_keys', []):
            raise LedgerBlocked('durable_event_index_corrupt')
    return True


def parse_cursor_host(actor):
    """Bind a parent Shell host packet. Field names stay the host's names.

    CURSOR_REQUEST_ID is not rewritten into a backend provider_run_id. A page,
    screenshot, attachment, or model result is not this packet.
    """
    command = actor.get('owner_command') or {}
    if actor.get('provider_run_id') not in (None, ''):
        raise LedgerBlocked('host_context_forbids_substitute_provider_run_id')
    ctx = command.get('host_context')
    if not isinstance(ctx, dict):
        raise LedgerBlocked('cursor_host_context_required')
    if (ctx.get('observation_source') not in HOST_OBSERVATIONS or ctx.get('namespace') != HOST_NAMESPACE or
            any(k in ctx for k in ('copied_from', 'attachment', 'page_text', 'screenshot', 'provider_run_id'))):
        raise LedgerBlocked('parent_shell_os_environ_required')
    fields = ctx.get('raw_host_fields')
    if not isinstance(fields, dict) or set(fields) != set(HOST_FIELD_NAMES):
        raise LedgerBlocked('cursor_host_fields_required')
    conv = opaque(fields.get('CURSOR_CONVERSATION_ID'), 'CURSOR_CONVERSATION_ID')
    req = opaque(fields.get('CURSOR_REQUEST_ID'), 'CURSOR_REQUEST_ID')
    if conv.startswith(REJECTED_HOST_PREFIXES) or req.startswith(REJECTED_HOST_PREFIXES):
        raise LedgerBlocked('executor_or_cloud_id_is_not_parent')
    if req == actor.get('execution_instance_id') or conv == actor.get('execution_instance_id'):
        raise LedgerBlocked('host_id_must_not_be_local_execution_uuid')
    msg = ctx.get('owner_native_message')
    if not isinstance(msg, dict):
        raise LedgerBlocked('owner_native_message_required')
    address = opaque(msg.get('host_address'), 'owner_host_address')
    if HOST_ADDRESS.fullmatch(address) is None:
        raise LedgerBlocked('owner_host_address_required')
    if msg.get('role') != 'user':
        raise LedgerBlocked('owner_host_role_required')
    if msg.get('text') != command.get('quote'):
        raise LedgerBlocked('host_quote_mismatch')
    host_run = {
        'namespace': HOST_NAMESPACE, 'observation_source': ctx.get('observation_source'),
        'field': 'CURSOR_REQUEST_ID', 'value': req,
        'conversation_field': 'CURSOR_CONVERSATION_ID', 'conversation_id': conv,
        'owner_host_address': address, 'owner_host_role': 'user'}
    events = [key([HOST_NAMESPACE, 'CURSOR_CONVERSATION_ID', conv, 'host_address', address])]
    return (key([actor.get('surface'), HOST_NAMESPACE, 'CURSOR_REQUEST_ID', req]), events,
            {'source': HOST_NAMESPACE, 'host_run': host_run})


def identity(config, actor):
    command = actor.get('owner_command') or {}
    if actor.get('kind') == 'owner_command' and command.get('source') == HOST_NAMESPACE:
        return parse_cursor_host(actor)
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


def check(config, actor, ledger, item_id=None):
    validate(ledger)
    rk, events, record = identity(config, actor)
    cap = submission_cap(config)
    done = actor.get('submissions_this_wake', 0)
    if type(done) is not int or done < 0 or done >= cap:
        raise LedgerBlocked('provider_run_submission_cap_reached')
    row = ledger['runs'].get(rk)
    existing = []
    if row is not None:
        # A row written before the bounded batch has no submissions list and stays one Create.
        if not isinstance(row.get('submissions'), list):
            raise LedgerBlocked('provider_run_already_consumed_reconcile_without_Create')
        existing = row['submissions']
    if len(existing) != done:
        raise LedgerBlocked('provider_run_already_consumed_reconcile_without_Create' if done < len(existing)
                            else 'wake_submission_counter_mismatch')
    if item_id and any(entry.get('item_id') == item_id for entry in existing):
        raise LedgerBlocked('provider_run_item_already_consumed_reconcile_without_Create')
    for ek in events:
        bound = ledger['events'].get(ek)
        if bound is not None and bound != rk:
            raise LedgerBlocked('owner_message_already_consumed_reconcile_without_Create')
    if row is not None and set(row.get('event_keys') or []) != set(events):
        raise LedgerBlocked('owner_message_already_consumed_reconcile_without_Create')
    if row is None and any(ek in ledger['events'] for ek in events):
        raise LedgerBlocked('owner_message_already_consumed_reconcile_without_Create')
    return rk, events, record


def consume(config, actor, ledger, item):
    rk, events, record = check(config, actor, ledger, item.get('id'))
    claim = item.get('claim') or {}
    if item.get('state') != 'submitting' or not claim.get('submission_intent_id'):
        raise LedgerBlocked('durable_submission_intent_required')
    entry = {'item_id': item['id'], 'submission_intent_id': claim['submission_intent_id'],
             'intent_at': claim['submission_intent_at'], 'execution_instance_id': actor['execution_instance_id'],
             'consumed': True}
    out = copy.deepcopy(ledger)
    row = out['runs'].get(rk)
    note = ('Bounded wake batch: one distinct Create per ready item, at most account slot capacity, '
            'before each click. Failed, unknown, expiry and substantive refusal never reopen that item or raise the cap.')
    if row is None:
        host_run = (record or {}).get('host_run') if isinstance(record, dict) else None
        out['runs'][rk] = {
            'surface': actor['surface'],
            'provider_run_id': None if isinstance(host_run, dict) else actor.get('provider_run_id'),
            **({'host_run': host_run} if isinstance(host_run, dict) else {}),
            'automation_id': actor.get('automation_id'), 'execution_instance_id': actor['execution_instance_id'],
            'item_id': item['id'], 'submission_intent_id': claim['submission_intent_id'],
            'intent_at': claim['submission_intent_at'], 'consumed': True,
            'submission_cap': submission_cap(config), 'submissions': [entry],
            'event_keys': events, 'owner_event': record, 'note': note}
    else:
        row['submissions'].append(entry)
        row['note'] = note
    for ek in events:
        out['events'][ek] = rk
    return out


def verify_binding(item, ledger):
    """Readback check before the single click of this item, after publishing BOTH files."""
    validate(ledger)
    claim = item.get('claim') or {}
    rk = claim.get('provider_run_key')
    row = ledger['runs'].get(rk) or {}
    match = next((entry for entry in submissions_of(row)
                  if entry.get('item_id') == item.get('id') and
                  entry.get('submission_intent_id') == claim.get('submission_intent_id')), None)
    if not rk or not match or match.get('execution_instance_id') != claim.get('execution_instance_id'):
        raise LedgerBlocked('queue_and_ledger_not_published_together')
    return True
