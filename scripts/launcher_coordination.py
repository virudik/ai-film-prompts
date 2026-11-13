#!/usr/bin/env python3
"""Fail-closed launch coordination. No network, Topview call, or automatic git push.

All returned mutations must be published by the caller in a fresh-main CAS
transaction under the exact lease. A durable submitting intent permits ONE UI
click in its originating uninterrupted execution, never replay after a gap.
"""
import argparse
import copy
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import launcher_run_ledger as run_ledger
import queue_readiness

CONFIG = 'ops/slot-backup.json'
LOCK = 'ops/canon-lock.json'
QUEUE = 'ops/topview-launch-queue.json'
# 'grok' = Grok Bot, a helper launcher (owner decision 01.11.2026, see ops/LAUNCHER-COORDINATION.md).
# It launches either on its schedule (kind=scheduled) or on the owner's direct command (kind=owner_command).
SURFACES = ('ordinary', 'work', 'grok')
OWNER_COMMAND_SOURCES = ('grok_chat', 'telegram', 'cursor_host')

class Blocked(ValueError):
    pass

def ts(value):
    try:
        value = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return value if value.tzinfo is not None else None
    except (ValueError, TypeError):
        return None

def stamp(now):
    return now.astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def instance(actor):
    try:
        parsed = uuid.UUID(actor['execution_instance_id'])
        if parsed.version != 4: raise ValueError('UUID4 required')
        value = str(parsed)
    except (KeyError, ValueError, TypeError, AttributeError) as error:
        raise Blocked('unique_execution_instance_uuid_required') from error
    if actor.get('surface') not in SURFACES:
        raise Blocked('unknown_execution_surface')
    return value

def holder(actor):
    if actor.get('surface') == 'grok':
        return 'grok:' + instance(actor)
    return 'chatgpt:' + actor['surface'] + ':' + instance(actor)

def check_route(config, actor, now=None):
    instance(actor)
    if config.get('enabled') is not True:
        raise Blocked('launcher_disabled')
    if (type(config.get('route_generation')) is not int or config['route_generation'] < 1 or
            type(actor.get('route_generation')) is not int or actor['route_generation'] != config['route_generation']):
        raise Blocked('route_generation_changed')
    peer = (config.get('peers') or {}).get(actor['surface']) or {}
    if peer.get('enabled') is not True:
        raise Blocked('peer_not_enabled')
    kind = actor.get('kind')
    if actor['surface'] == 'grok' and kind not in ('scheduled', 'owner_command'):
        # Grok Bot has no foreground-shift (interactive/takeover) path; only schedule or a recorded owner command.
        raise Blocked('grok_interactive_not_authorized')
    if kind == 'owner_command':
        if actor['surface'] != 'grok':
            raise Blocked('owner_command_only_for_grok')
        check_owner_command(config, actor, now or datetime.now(timezone.utc))
    elif kind == 'scheduled':
        if actor.get('automation_id') not in peer.get('automation_ids', []):
            raise Blocked('retired_or_unregistered_automation')
    elif kind == 'interactive':
        owner = (config.get('foreground_owners') or {}).get(actor['surface']) or {}
        if (owner.get('session_id') != actor.get('session_id') or
                owner.get('epoch') != actor.get('foreground_epoch') or not owner.get('session_id')):
            raise Blocked('interactive_shift_transferred')
    else:
        raise Blocked('unknown_execution_kind')
    # Preferred executor is NOT an exclusivity gate: the other peer may help.
    return True

def standing_record(config, actor):
    """A recorded standing command, or None when this actor is an ordinary phrase."""
    command = actor.get('owner_command') or {}
    standing = (command.get('host_context') or {}).get('standing_command')
    if not isinstance(standing, dict) or not standing.get('id'):
        return None
    policy = (config.get('grok_launcher') or {}).get('owner_command_launch') or {}
    records = policy.get('standing_commands')
    if not isinstance(records, list):
        raise Blocked('standing_command_not_authorized')
    match = next((row for row in records
                  if isinstance(row, dict) and row.get('id') == standing.get('id') and row.get('enabled') is True),
                 None)
    if match is None:
        raise Blocked('standing_command_not_authorized')
    return match


def t601_dance_consent(item):
    """t601u, 13.11.2026. Only the named scene-28 dances. Other music stays closed."""
    if not isinstance(item, dict) or item.get('scene_id') != 28 or item.get('owner_music_consent') is not True:
        return False
    record = item.get('owner_music_consent_record')
    return isinstance(record, dict) and record.get('id') == 'owner-20261113-t601u'


def check_standing_scope(config, actor, item):
    """Standing authority is ready story, one free attempt. It does not open music or a held scene.

    t601u is the later owner yes for the listed scene-28 dances. That consent does not
    open scenes 49, 50 or 51, and a scene-28 item without it stays denied.
    """
    record = standing_record(config, actor)
    if record is None:
        return None
    scope = record.get('scope') or {}
    scene = item.get('scene_id')
    if scene in (scope.get('hold_scenes') or []):
        raise Blocked('standing_command_scene_held')
    if (scope.get('music_dance') is False and scene in (scope.get('excluded_scenes') or [])
            and not t601_dance_consent(item)):
        raise Blocked('standing_command_music_denied')
    if scope.get('one_attempt') is True and item.get('max_new_submissions') != 1:
        raise Blocked('standing_command_one_attempt')
    if scope.get('free_unlimited') is True and item.get('max_credits') != 0:
        raise Blocked('standing_command_free_unlimited_only')
    return record


def check_owner_command(config, actor, now):
    """Grok Bot launch on the owner's direct command: needs a recorded quote, source and fresh timestamp."""
    policy = (config.get('grok_launcher') or {}).get('owner_command_launch')
    if not isinstance(policy, dict) or policy.get('enabled') is not True:
        raise Blocked('grok_owner_command_not_authorized')
    command = actor.get('owner_command')
    if not isinstance(command, dict):
        raise Blocked('owner_command_record_required')
    quote = command.get('quote')
    if not isinstance(quote, str) or len(quote.strip()) < 2:
        raise Blocked('owner_command_quote_required')
    source = command.get('source')
    allowed = policy.get('sources') or OWNER_COMMAND_SOURCES
    if source not in OWNER_COMMAND_SOURCES or source not in allowed:
        raise Blocked('owner_command_source_not_allowed')
    if source == 'telegram':
        chat = str(policy.get('telegram_chat_id') or '')
        if not chat or str(command.get('chat_id')) != chat:
            raise Blocked('owner_command_telegram_chat_mismatch')
    elif source == 'cursor_host':
        try:
            run_ledger.parse_cursor_host(actor)
        except run_ledger.LedgerBlocked as error:
            raise Blocked(str(error)) from error
    at = ts(command.get('at'))
    record = standing_record(config, actor)
    if record is not None:
        if source != 'cursor_host' or quote != record.get('quote'):
            raise Blocked('standing_command_quote_mismatch')
        if not at or at > now:
            raise Blocked('owner_command_stale_or_future')
        return True
    max_age = policy.get('max_age_minutes')
    if not at or type(max_age) is not int or max_age < 1:
        raise Blocked('owner_command_timestamp_required')
    age = (now - at).total_seconds()
    if not 0 <= age <= max_age * 60:
        raise Blocked('owner_command_stale_or_future')
    return True

def unlimited_zero_cost_accepted(preflight):
    """credits_cost must be the number 0. A missing glyph is not a measurement.

    Owner 08.11.2026 23:03 MSK (t373s1831): an explicitly selected free Unlimited
    mode in the current form, labelled free, authorizes recording 0 even when the
    digit is not shown. Keep numeric_zero_displayed false. An advertised Unlimited,
    a pricing page, or an unselected free option does not. A selected paid mode,
    an unclear state, or any positive cost still fails.
    """
    if not isinstance(preflight, dict):
        return False
    if preflight.get('paid_credit_mode_selected') is True or preflight.get('paid_18_credit_mode_selected') is True:
        return False
    cost = preflight.get('credits_cost')
    if isinstance(cost, bool) or type(cost) not in (int, float) or cost != 0:
        return False
    if preflight.get('website_unlimited') is not True:
        return False
    displayed = preflight.get('numeric_zero_displayed')
    if displayed is True or displayed is None:
        return True
    if displayed is not False:
        return False
    label = preflight.get('ui_unlimited_label')
    return (preflight.get('unlimited_mode_selected') is True
            and preflight.get('credits_cost_evidence') == 'selected_free_unlimited_current_form'
            and isinstance(label, str) and 'бесплатн' in label.casefold())


def check_lease(lock, actor, now):
    expiry, acquired = ts(lock.get('expires_at')), ts(lock.get('acquired_at'))
    if (lock.get('state') != 'held' or lock.get('holder') != holder(actor) or
            not acquired or acquired > now or not expiry or expiry <= now or
            actor.get('lease_acquired_at') != lock.get('acquired_at')):
        raise Blocked('exact_current_unexpired_lease_required')
    return True

def check_grok_policy(config, item, actor, now, queue_board_id=None):
    """Extra fail-closed limits for the Grok Bot helper (config['grok_launcher']); other surfaces unaffected."""
    policy = config.get('grok_launcher')
    if not isinstance(policy, dict):
        raise Blocked('grok_launcher_policy_missing')
    window = policy.get('launch_window')
    if not isinstance(window, dict):
        raise Blocked('grok_launch_window_missing')
    try:
        local = now.astimezone(ZoneInfo(window['timezone']))
        first_hour, last_hour = int(window['first_hour']), int(window['last_hour'])
        first_minute, last_minute = int(window['first_minute']), int(window['last_minute'])
    except (KeyError, TypeError, ValueError) as error:
        raise Blocked('grok_launch_window_invalid') from error
    wake = actor.get('wake_issue')
    if wake is not None and (type(wake) is not int or wake < 1):
        raise Blocked('grok_wake_issue_invalid')
    if wake is not None:
        # Free-slot wake (topview-slot-wake issue): launch immediately, no :10-:40 window
        # (owner 04.11.2026 23:29 MSK, t278u). Lock, claim, intent, board, Unlimited0, ledger stay mandatory.
        pass
    elif actor.get('kind') == 'owner_command':
        # Owner-command launches bypass the :10-:40 window (the owner asked for it now), but never the lock,
        # claim/intent, board, Unlimited0 or per-run limits checked below and in prepare_intent.
        if (policy.get('owner_command_launch') or {}).get('bypass_launch_window') is not True:
            if not (first_hour <= local.hour <= last_hour and first_minute <= local.minute <= last_minute):
                raise Blocked('outside_grok_launch_window')
    elif not (first_hour <= local.hour <= last_hour and first_minute <= local.minute <= last_minute):
        raise Blocked('outside_grok_launch_window')
    if (policy.get('first_real_create') or {}).get('owner_go_ahead') is not True:
        raise Blocked('grok_first_real_create_pending_owner_go_ahead')
    # Some canonical parts inherit their board from the containing queue.
    # Never infer it from the policy alone, and reject any explicit conflict.
    board = item.get('board_id')
    if board in (None, ''):
        board = queue_board_id
    if (not policy.get('board_id') or board != policy['board_id'] or
            (queue_board_id is not None and queue_board_id != board)):
        raise Blocked('grok_board_not_authorized')
    try:
        limit = run_ledger.submission_cap(config)
    except run_ledger.LedgerBlocked as error:
        raise Blocked('grok_submission_limit_per_wake') from error
    done = actor.get('submissions_this_wake', 0)
    if type(done) is not int or done < 0 or done >= limit:
        raise Blocked('grok_submission_limit_per_wake')
    return True

def check_grok_retry(config, item):
    """A Grok Bot retry Create needs the owner-enabled policy and a persisted, in-budget shared counter."""
    policy = (config.get('grok_launcher') or {}).get('retries')
    if not isinstance(policy, dict) or policy.get('enabled') is not True:
        raise Blocked('grok_retries_not_authorized')
    control = item.get('retry_control')
    if not isinstance(control, dict) or control.get('policy_id') != policy.get('policy_id'):
        raise Blocked('retry_control_policy_mismatch')
    used, limit = control.get('retry_attempts_used'), control.get('max_retry_attempts')
    if (type(used) is not int or type(limit) is not int or type(policy.get('max_retry_attempts')) is not int or
            limit != policy['max_retry_attempts'] or not 1 <= used <= limit):
        raise Blocked('retry_budget_exhausted_or_counter_unclear')
    if not item.get('submission_history'):
        raise Blocked('retry_requires_prior_attempt_in_submission_history')
    if queue_readiness.substantive_refusal(item):
        raise Blocked('substantive_refusal_not_retried')
    return True

def wake_selection(root, config, free_slots):
    """Ids this real wake may Create, in queue priority, capped by free slots and account capacity."""
    try:
        cap = run_ledger.submission_cap(config)
    except run_ledger.LedgerBlocked as error:
        raise Blocked('grok_submission_limit_per_wake') from error
    if type(free_slots) is not int or not 0 <= free_slots <= run_ledger.ACCOUNT_SLOT_CAPACITY:
        raise Blocked('fresh_complete_global_capacity_required')
    return queue_readiness.launch_candidates(root, limit=min(cap, free_slots))


def prepare_intent(config, lock, item, actor, scan, now, queue_board_id=None, ledger=None, root=None):
    """Transition claimed -> submitting once. Persist and read back before one click."""
    check_route(config, actor, now)
    check_lease(lock, actor, now)
    if actor['surface'] == 'grok':
        check_grok_policy(config, item, actor, now, queue_board_id=queue_board_id)
        check_standing_scope(config, actor, item)
        if item.get('retry_control') is not None or item.get('submission_history'):
            check_grok_retry(config, item)
    if item.get('state') != 'claimed':
        raise Blocked('not_a_fresh_owned_claim; reconcile_without_Create')
    claim = item.get('claim') or {}
    if (claim.get('execution_instance_id') != instance(actor) or
            claim.get('route_generation') != config['route_generation'] or
            not claim.get('claim_id') or claim.get('submission_intent_id') or item.get('task_id')):
        raise Blocked('claim_foreign_or_already_consumed')
    observed = ts(scan.get('checked_at'))
    if (scan.get('complete') is not True or not observed or
            not 0 <= (now-observed).total_seconds() <= 120 or
            not isinstance(scan.get('free_slots'), int) or isinstance(scan.get('free_slots'), bool) or
            not 1 <= scan['free_slots'] <= 6):
        raise Blocked('fresh_complete_global_capacity_required')
    p = claim.get('preflight') or {}
    if not all(p.get(k) is True for k in ('owner_authorized', 'prompt_match', 'input_sha_match',
                                          'input_order_match', 'qc_passed', 'website_unlimited')):
        raise Blocked('required_preflight_not_verified')
    if (not unlimited_zero_cost_accepted(p) or
            type(p.get('quantity')) is not int or p.get('quantity') != 1 or
            p.get('resolution') != 720 or p.get('aspect_ratio') != '16:9'):
        raise Blocked('unlimited_zero_credit_parameters_required')
    if queue_readiness.substantive_refusal(item):
        raise Blocked('substantive_refusal_not_retried')
    if queue_readiness.continuity_blocks_launch(item, root):
        raise Blocked('continuity_excerpt_missing')
    if root is not None and queue_readiness.music_create_blocked(
            queue_readiness.read(Path(root) / QUEUE, {}), item):
        raise Blocked('music_owner_consent_required')
    run_identity = None
    if run_ledger.required(config, actor):
        try:
            run_identity = run_ledger.check(config, actor, ledger, item.get('id'))
        except run_ledger.LedgerBlocked as error:
            raise Blocked(str(error)) from error
    out = copy.deepcopy(item)
    out['state'] = 'submitting'
    out['claim']['submission_intent_id'] = str(uuid.uuid4())
    out['claim']['submission_intent_at'] = stamp(now)
    out['claim']['lease_holder'] = holder(actor)
    out['claim']['lease_acquired_at'] = lock['acquired_at']
    out['claim']['replay_forbidden'] = True
    if run_identity:
        host_run = (run_identity[2] or {}).get('host_run') if isinstance(run_identity[2], dict) else None
        if isinstance(host_run, dict):
            out['claim']['host_run'] = host_run
        else:
            out['claim']['provider_run_id'] = actor['provider_run_id']
        out['claim']['provider_run_key'] = run_identity[0]
        out['claim']['owner_event_keys'] = run_identity[1]
        out['claim']['ledger_path'] = run_ledger.PATH
    if actor['surface'] == 'grok' and actor.get('wake_issue') is not None:
        out['claim']['trigger'] = 'wake'
        out['claim']['wake_issue'] = actor['wake_issue']
    elif actor['surface'] == 'grok' and actor.get('kind') == 'owner_command':
        command = actor['owner_command']
        out['claim']['trigger'] = 'owner_command'
        recorded = {k: command.get(k) for k in ('quote', 'source', 'at', 'chat_id') if command.get(k) is not None}
        message = ((command.get('host_context') or {}).get('owner_native_message') or {})
        card = ((command.get('host_context') or {}).get('owner_card_response') or {})
        if message.get('host_address'):
            recorded['host_address'] = message['host_address']
            recorded['host_role'] = message.get('role')
        if card.get('owner_response_to_card_address'):
            recorded['owner_response_to_card_address'] = card['owner_response_to_card_address']
            recorded['owner_response_role'] = card.get('owner_response_role')
            recorded['current_owner_response_message_address'] = None
        standing = ((command.get('host_context') or {}).get('standing_command') or {})
        if standing.get('id'):
            recorded['standing_command_id'] = standing['id']
            record = standing_record(config, actor)
            if record is not None and record.get('host_address'):
                recorded['standing_host_address'] = record['host_address']
        out['claim']['owner_command'] = recorded
    return out


def _cursor_host_context(packet):
    """Keep the parent's field names. A card answer is not rewritten into tNu."""
    fields = packet.get('raw_host_fields')
    if not isinstance(fields, dict):
        fields = {name: packet.get(name) for name in ('CURSOR_CONVERSATION_ID', 'CURSOR_REQUEST_ID')}
    context = {
        'namespace': 'cursor_host',
        'observation_source': packet.get('observation_source'),
        'raw_host_fields': fields,
    }
    if isinstance(packet.get('standing_command'), dict):
        context['standing_command'] = {'id': packet['standing_command'].get('id')}
    if packet.get('owner_response_to_card_address') or packet.get('owner_card_response'):
        card = packet.get('owner_card_response') or {
            'owner_response_to_card_address': packet.get('owner_response_to_card_address'),
            'owner_response_role': packet.get('owner_response_role'),
            'owner_response_text': packet.get('owner_response_text'),
            'current_owner_response_message_address': packet.get('current_owner_response_message_address'),
        }
        context['owner_card_response'] = card
        quote, at = card.get('owner_response_text'), packet.get('owner_response_at') or card.get('owner_response_at')
    elif packet.get('owner_native_message'):
        message = packet.get('owner_native_message') or {}
        context['owner_native_message'] = {
            'host_address': message.get('host_address'),
            'role': message.get('role'),
            'text': message.get('text'),
        }
        quote, at = message.get('text'), message.get('at')
    elif isinstance(packet.get('standing_command'), dict):
        quote, at = packet.get('quote'), packet.get('at')
    else:
        context['owner_native_message'] = {'host_address': None, 'role': None, 'text': None}
        quote, at = None, None
    return quote, at, context


def dry_run_cursor_host(config, packet, now, execution_instance_id, ledger=None):
    """Validate one parent host packet. Does not consume, claim, or click Create."""
    quote, at, context = _cursor_host_context(packet)
    actor = {
        'surface': 'grok', 'kind': 'owner_command',
        'route_generation': config.get('route_generation'),
        'execution_instance_id': execution_instance_id,
        'owner_command': {
            'source': 'cursor_host', 'quote': quote, 'at': at,
            'host_context': context,
        },
    }
    check_owner_command(config, actor, now)
    rk, events, record = run_ledger.check(config, actor, run_ledger.empty() if ledger is None else ledger)
    return {'allowed': True, 'consumes': False, 'provider_run_key': rk,
            'event_keys': events, 'host_run': record['host_run']}

def prepare_transaction(config, lock, item, actor, scan, now, ledger=None, queue_board_id=None, root=None):
    """Return both files' mutations. CAS-publish queue+ledger together, then verify_binding."""
    out = prepare_intent(config, lock, item, actor, scan, now, queue_board_id=queue_board_id, ledger=ledger, root=root)
    updated = run_ledger.consume(config, actor, ledger, out) if run_ledger.required(config, actor) else ledger
    return out, updated


def takeover(config, lock, actor, now, owner_command):
    """Transfer only this surface's interactive shift; scheduled peers survive."""
    if owner_command not in ('Продолжай', 'Прими смену'):
        raise Blocked('direct_owner_continue_command_required')
    instance(actor)
    if actor['surface'] == 'grok':
        raise Blocked('grok_interactive_not_authorized')
    if config.get('enabled') is not True or actor.get('route_generation') != config.get('route_generation'):
        raise Blocked('route_changed_or_disabled')
    if ((config.get('peers') or {}).get(actor['surface']) or {}).get('enabled') is not True:
        raise Blocked('peer_not_enabled')
    if actor.get('kind') != 'interactive' or not actor.get('session_id'):
        raise Blocked('interactive_session_required')
    check_lease(lock, actor, now)
    out = copy.deepcopy(config)
    owners = out.setdefault('foreground_owners', {})
    previous = owners.get(actor['surface']) or {}
    if previous.get('session_id') == actor['session_id']:
        return out  # repeat Continue in the same chat is not a fresh takeover
    if previous:
        out.setdefault('foreground_owner_history', []).append(dict(previous, surface=actor['surface'], retired_at=stamp(now)))
    owners[actor['surface']] = {
        'session_id': actor['session_id'], 'epoch': int(previous.get('epoch', 0)) + 1,
        'conversation_id': actor.get('conversation_id'),
        'conversation_id_unavailable_reason': None if actor.get('conversation_id') else 'not_exposed_by_current_tools',
        'accepted_at': stamp(now), 'source': 'direct_owner_' + owner_command,
        'work_id': 'TOPVIEW-SLOT-PRIORITY-20261024'}
    return out

def restore_work_preference(config, evidence, now):
    """Evidence must be collected by the caller; flags do not independently prove quota."""
    reported = ts((config.get('work_capacity') or {}).get('reported_at'))
    checked = ts(evidence.get('checked_at'))
    if not reported or not checked or not reported < checked <= now:
        raise Blocked('fresh_recovery_evidence_required')
    owner = (evidence.get('source') == 'direct_owner_confirmation' and bool(evidence.get('reference')))
    runtime = (evidence.get('source') == 'verified_work_runtime' and evidence.get('surface') == 'work'
               and bool(evidence.get('run_id')) and evidence.get('recorded_status') == 'completed'
               and evidence.get('browser_controls_verified') is True
               and evidence.get('quota_available_verified') is True and bool(evidence.get('reference')))
    if not (owner or runtime):
        raise Blocked('enabled_no_update_old_success_or_elapsed_time_are_not_recovery')
    out = copy.deepcopy(config)
    if out.get('preferred_executor') == 'work':
        return out
    out.setdefault('role_history', []).append({'at': stamp(now), 'from': out.get('preferred_executor'),
                                              'to': 'work', 'evidence': copy.deepcopy(evidence)})
    out['preferred_executor'] = 'work'
    out['primary_automation_ids'] = list(out['peers']['work']['automation_ids'])
    # Restoring Work must not silently remove another registered enabled helper.
    out['reserve_automation_ids'] = list(dict.fromkeys(
        automation_id
        for surface, peer in out['peers'].items()
        if surface != 'work' and peer.get('enabled') is True
        for automation_id in peer.get('automation_ids', [])))
    out['route_generation'] = int(out['route_generation']) + 1
    out['work_capacity'] = {'state': 'available', 'reported_at': stamp(now), 'evidence': copy.deepcopy(evidence)}
    return out

def release_exact(lock, actor, now):
    # Never release a replacement lease, even if it has already expired.
    if lock.get('holder') != holder(actor) or lock.get('acquired_at') != actor.get('lease_acquired_at'):
        raise Blocked('not_own_lease')
    out = copy.deepcopy(lock)
    out.update(state='free', expires_at=None, released_at=stamp(now))
    return out

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', type=Path)
    ap.add_argument('action', choices=('status', 'check', 'takeover', 'prepare-intent', 'restore-work'))
    ap.add_argument('--actor', type=Path)
    ap.add_argument('--scan', type=Path)
    ap.add_argument('--evidence', type=Path)
    ap.add_argument('--item-id')
    ap.add_argument('--owner-command')
    ap.add_argument('--wake-issue', type=int, help='grok free-slot wake issue number: skip the :10-:40 window only')
    ap.add_argument('--write', action='store_true', help='Write local files only; caller must CAS-publish and read back')
    args = ap.parse_args()
    now = datetime.now(timezone.utc)
    try:
        cfg = read(args.root / CONFIG)
        if args.action == 'status':
            print(json.dumps(cfg, ensure_ascii=False, indent=2)); return 0
        actor = read(args.actor) if args.actor else {}
        if args.wake_issue is not None:
            actor['wake_issue'] = args.wake_issue
        lock = read(args.root / LOCK)
        path = None
        if args.action == 'check':
            check_route(cfg, actor, now); check_lease(lock, actor, now)
            result = {'allowed': True, 'scope': 'route_and_lease_only; full_UI_preflight_required'}
        elif args.action == 'takeover':
            result = takeover(cfg, lock, actor, now, args.owner_command); path = args.root / CONFIG
        elif args.action == 'restore-work':
            check_route(cfg, actor); check_lease(lock, actor, now)
            result = restore_work_preference(cfg, read(args.evidence), now); path = args.root / CONFIG
        else:
            queue = read(args.root / QUEUE)
            matches = [i for i in queue['items'] if i.get('id') == args.item_id]
            if len(matches) != 1: raise Blocked('item_not_unique')
            ledger = read(args.root / run_ledger.PATH) if run_ledger.required(cfg, actor) else None
            result, updated_ledger = prepare_transaction(cfg, lock, matches[0], actor, read(args.scan), now,
                                                        ledger=ledger, queue_board_id=queue.get('board_id'), root=args.root)
            queue['items'][queue['items'].index(matches[0])] = result
            if args.write:
                if updated_ledger is not None:
                    # Consume locally first: a local crash must fail closed. Git publication MUST include both paths.
                    (args.root / run_ledger.PATH).write_text(json.dumps(updated_ledger, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
                (args.root / QUEUE).write_text(json.dumps(queue, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        if args.write and path:
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'allowed': False, 'reason': str(error)}, ensure_ascii=False)); return 2

if __name__ == '__main__':
    raise SystemExit(main())
