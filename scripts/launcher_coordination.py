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

CONFIG = 'ops/slot-backup.json'
LOCK = 'ops/canon-lock.json'
QUEUE = 'ops/topview-launch-queue.json'

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
    if actor.get('surface') not in ('ordinary', 'work'):
        raise Blocked('unknown_execution_surface')
    return value

def holder(actor):
    return 'chatgpt:' + actor['surface'] + ':' + instance(actor)

def check_route(config, actor):
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
    if kind == 'scheduled':
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

def check_lease(lock, actor, now):
    expiry, acquired = ts(lock.get('expires_at')), ts(lock.get('acquired_at'))
    if (lock.get('state') != 'held' or lock.get('holder') != holder(actor) or
            not acquired or acquired > now or not expiry or expiry <= now or
            actor.get('lease_acquired_at') != lock.get('acquired_at')):
        raise Blocked('exact_current_unexpired_lease_required')
    return True

def prepare_intent(config, lock, item, actor, scan, now):
    """Transition claimed -> submitting once. Persist and read back before one click."""
    check_route(config, actor)
    check_lease(lock, actor, now)
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
    if (type(p.get('credits_cost')) not in (int, float) or p.get('credits_cost') != 0 or
            type(p.get('quantity')) is not int or p.get('quantity') != 1 or
            p.get('resolution') != 720 or p.get('aspect_ratio') != '16:9'):
        raise Blocked('unlimited_zero_credit_parameters_required')
    out = copy.deepcopy(item)
    out['state'] = 'submitting'
    out['claim']['submission_intent_id'] = str(uuid.uuid4())
    out['claim']['submission_intent_at'] = stamp(now)
    out['claim']['lease_holder'] = holder(actor)
    out['claim']['lease_acquired_at'] = lock['acquired_at']
    out['claim']['replay_forbidden'] = True
    return out

def takeover(config, lock, actor, now, owner_command):
    """Transfer only this surface's interactive shift; scheduled peers survive."""
    if owner_command not in ('Продолжай', 'Прими смену'):
        raise Blocked('direct_owner_continue_command_required')
    instance(actor)
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
    out['reserve_automation_ids'] = list(out['peers']['ordinary']['automation_ids'])
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
    ap.add_argument('--write', action='store_true', help='Write local files only; caller must CAS-publish and read back')
    args = ap.parse_args()
    now = datetime.now(timezone.utc)
    try:
        cfg = read(args.root / CONFIG)
        if args.action == 'status':
            print(json.dumps(cfg, ensure_ascii=False, indent=2)); return 0
        actor = read(args.actor) if args.actor else {}
        lock = read(args.root / LOCK)
        path = None
        if args.action == 'check':
            check_route(cfg, actor); check_lease(lock, actor, now)
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
            result = prepare_intent(cfg, lock, matches[0], actor, read(args.scan), now)
            queue['items'][queue['items'].index(matches[0])] = result
            if args.write:
                (args.root / QUEUE).write_text(json.dumps(queue, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        if args.write and path:
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'allowed': False, 'reason': str(error)}, ensure_ascii=False)); return 2

if __name__ == '__main__':
    raise SystemExit(main())
