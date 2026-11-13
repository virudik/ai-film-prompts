#!/usr/bin/env python3
"""Derived, read-only launch readiness. Never grants approval, modifies queue or submits.

Run by existing canonical-sync and telemetry robot; semantic changes only are saved.
Actual result success means prepare/QC an input, never that the input already exists.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FINAL = {'submitted', 'completed', 'cancelled_owner', 'held_owner_site'}
CONTINUITY_ROLES = {'previous_part_end', 'continuity'}
SUBSTANTIVE_OUTCOMES = {'content_refusal', 'copyright_refusal', 'moderation_refusal', 'substantive_refusal'}

def read(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return default

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def label(item):
    text = item.get('canonical_block_label') or item.get('id', '')
    part = re.search(r'часть\s+(\d+)', text)
    return 'Часть ' + part[1] if part else text

def derive(root):
    root = Path(root)
    q = read(root / 'ops/topview-launch-queue.json', {})
    tm = read(root / 'topview-task-map.json', {})
    tv = read(root / 'topview-status.json', {})
    items = q.get('items', [])
    byid = {i['id']: i for i in q.get('archived_items', []) + items}
    tasks = {t['task_id']: t.get('final_status', t.get('status')) for t in tm.get('processed_tasks', [])}
    # A delayed telemetry snapshot must not overwrite a terminal task-map result.
    # Some active-task rows expose topview_status instead of status.
    for active in tv.get('active_tasks', []):
        tid = active.get('task_id')
        status = active.get('status') or active.get('topview_status')
        if tid and status and tasks.get(tid) not in ('success', 'fail', 'failed', 'cancelled'):
            tasks[tid] = status
    for ids in tm.get('active_by_scene', {}).values():
        for tid in ids:
            tasks.setdefault(tid, 'running')
    rows = []
    for i in items:
        state = i.get('state', '')
        if state in FINAL or state.startswith(('cancelled', 'superseded')):
            continue
        reasons = []
        missing_sources = set()
        code = 'ready'
        if i.get('owner_decision_20261023') and i.get('scene_id') == 44:
            code = 'owner_hold'
            reasons.append('По решению владельца: сначала оценка результата 52P1; запуск 44 отложен')
        elif state in ('blocked_owner_decision', 'blocked_test_review', 'blocked_model_preparation'):
            code = state
            reasons.append({'blocked_owner_decision':'Нужно решение владельца', 'blocked_test_review':'Нужна оценка теста', 'blocked_model_preparation':'Нужна подготовка промта'}[state])
        for ref in i.get('references', []):
            if ref.get('required') is False:
                continue
            slot = ref.get('slot', 'Вход')
            path = ref.get('path')
            available = ref.get('input_status') in (None, 'available')
            if path:
                p = root / path
                available = available and p.is_file() and (not ref.get('sha256') or digest(p) == ref['sha256'])
            else:
                available = available and bool((ref.get('drive_file_id') or ref.get('library_file_id')) and ref.get('sha256'))
            if available:
                continue
            source_id = ref.get('source_item_id')
            if source_id:
                missing_sources.add(source_id)
            source = byid.get(source_id, {})
            task = ref.get('source_task_id') or source.get('task_id')
            task_state = tasks.get(task)
            if source_id or task:
                source_label = source.get('canonical_block_label') or source_id or task
                if i.get('launch_readiness') == 'blocked_continuity_qc':
                    reasons.append(f'{slot}: исходный результат получен, но не прошёл проверку стыка')
                    if code == 'ready': code = 'continuity_qc_failed'
                elif task_state == 'success':
                    reasons.append(f'{slot}: результат {source_label} получен — подготовить и проверить стык')
                    if code == 'ready': code = 'prepare_continuity'
                elif task_state in ('fail', 'failed', 'cancelled'):
                    reasons.append(f'{slot}: исходный результат {source_label} — {task_state}; нужно решение')
                    if code == 'ready': code = 'source_failed'
                else:
                    reasons.append(f'{slot}: ждёт результат {source_label}' + (' (ещё не запущен)' if not task else ''))
                    if code == 'ready': code = 'waiting_result'
            else:
                reasons.append(f'{slot}: нужен референс или проверка его файла/SHA256')
                if code == 'ready': code = 'missing_reference'
        # Explicit ordering dependencies remain binding even with all references available.
        for dep in i.get('depends_on_submitted', []):
            parent = byid.get(dep, {})
            if parent.get('state') not in ('submitted', 'completed') and dep not in missing_sources:
                reasons.append(f'Ждёт запуск {dep}')
                if code == 'ready': code = 'waiting_order'
        for dep in i.get('depends_on_completed', []):
            parent = byid.get(dep, {})
            if tasks.get(parent.get('task_id')) != 'success' and dep not in missing_sources:
                reasons.append(f'Ждёт подтверждённый результат {dep}')
                if code == 'ready': code = 'waiting_result'
        if code == 'ready' and state != 'waiting_for_slot':
            code = 'preflight_required'
            reasons.append('Входы найдены; требуется снять записанный блокер после проверки')
        rows.append({'id':i['id'], 'scene_id':i['scene_id'], 'part_label':label(i), 'code':code,
                     'ready':code == 'ready', 'text':'Готова по входам, ждёт свободный слот' if code == 'ready' else '; '.join(reasons),
                     'queue_state':state})
    return {'schema_version':1, 'source_queue_sha256':digest(root/'ops/topview-launch-queue.json'),
            'source_task_map_sha256':digest(root/'topview-task-map.json') if (root/'topview-task-map.json').exists() else None,
            'topview_checked_at':tv.get('checked_at'), 'items':rows,
            'rule':'Derived readiness only; actual free slot, latest owner decisions, exact input materialization/QC and Unlimited0 preflight still required.'}

def is_continuity_ref(ref):
    """A previous-part excerpt. A dependency id alone is not this reference."""
    if not isinstance(ref, dict) or ref.get('required') is False:
        return False
    return (str(ref.get('slot') or '').startswith('@Video') or bool(ref.get('source_item_id')) or
            ref.get('canonical_role') in CONTINUITY_ROLES or ref.get('source_kind') == 'actual_topview_result_trim')


def excerpt_materialized(ref, root=None):
    """The excerpt is loaded only when its bytes or a saved private id match the recorded SHA."""
    if not isinstance(ref, dict) or ref.get('input_status') not in (None, 'available'):
        return False
    sha = ref.get('sha256')
    if not isinstance(sha, str) or len(sha) < 8:
        return False
    path = ref.get('path')
    if path:
        if root is None:
            return False
        file = Path(root) / path
        return file.is_file() and digest(file) == sha
    return bool(ref.get('drive_file_id') or ref.get('library_file_id'))


def continuity_blocks_launch(item, root=None):
    """Linked work needs every required previous-part excerpt. depends_on_* is not the file."""
    if not isinstance(item, dict):
        return True
    refs = [ref for ref in (item.get('references') or []) if isinstance(ref, dict) and ref.get('required') is not False]
    linked_refs = [ref for ref in refs if is_continuity_ref(ref)]
    linked = bool(linked_refs) or bool(item.get('depends_on_completed')) or bool(item.get('depends_on_submitted'))
    if not linked:
        return False
    if not linked_refs:
        return True
    return any(not excerpt_materialized(ref, root) for ref in linked_refs)


def substantive_refusal(item):
    """Content/copyright/moderation refusal is not a technical retry without a separate owner yes."""
    if not isinstance(item, dict) or item.get('owner_retry_authorized') is True:
        return False
    if item.get('substantive_refusal') is True or str(item.get('provider_error_code') or '') == '7000':
        return True
    for row in item.get('submission_history') or []:
        if isinstance(row, dict) and (row.get('outcome') in SUBSTANTIVE_OUTCOMES or str(row.get('error_code') or '') == '7000'):
            return True
    return False


def music_consent_policy(queue):
    """t369u, 08.11.2026 20:40 MSK. Absent unless this decision is on the queue."""
    policy = queue.get('owner_policy_20261108_t369u') if isinstance(queue, dict) else None
    if not isinstance(policy, dict) or policy.get('effect') != 'music_requires_owner_consent':
        return None
    if not isinstance(policy.get('scenes'), list):
        return None
    return policy


def is_music_dance(queue, item):
    policy = music_consent_policy(queue)
    return bool(policy) and isinstance(item, dict) and item.get('scene_id') in policy['scenes']


def music_create_blocked(queue, item):
    """New music/dance Create needs a separate owner consent. Submitted work stays.

    A consumed submitting intent is not consent and is not cleared here.
    Consent that says after_all_story stays closed while a story part is still to launch.
    """
    if not is_music_dance(queue, item):
        return False
    if item.get('owner_music_consent') is True:
        record = item.get('owner_music_consent_record') or {}
        if record.get('condition') == 'after_all_story' and story_still_to_launch(queue):
            return True
        return False
    if item.get('task_id'):
        return False
    state = str(item.get('state') or '')
    if state in ('submitted', 'completed', 'submission_unknown') or state.startswith(('cancelled', 'superseded')):
        return False
    return state in ('waiting_for_slot', 'claimed', 'submitting')


def t422_policy(queue):
    """t422u, 09.11.2026 13:06 MSK. Absent unless this decision is on the queue."""
    policy = queue.get('owner_policy_20261109_t422u') if isinstance(queue, dict) else None
    if not isinstance(policy, dict) or policy.get('effect') != 'tatooine_chain_first':
        return None
    if not isinstance(policy.get('tatooine_chain'), list):
        return None
    return policy


def story_still_to_launch(queue):
    """A story part that is not yet sent. Held 13 and 62 do not keep S49B closed forever."""
    if not isinstance(queue, dict):
        return False
    for item in queue.get('items') or []:
        if not isinstance(item, dict) or is_music_dance(queue, item):
            continue
        if item.get('scene_id') in (13, 62):
            continue
        if str(item.get('state') or '') in ('waiting_for_slot', 'blocked_inputs', 'claimed', 'submitting'):
            return True
    return False


def link_rank(item):
    """Independent ready work before a part whose join is already verified."""
    linked = bool(item.get('depends_on_completed') or item.get('depends_on_submitted'))
    if not linked:
        linked = any(is_continuity_ref(ref) for ref in (item.get('references') or []) if isinstance(ref, dict))
    return 1 if linked else 0


def t601_order(queue):
    """t601u, 13.11.2026 14:40 MSK. Absent unless this decision is on the queue.

    Named items launch in this list order, ahead of the t422u bands. A missing
    excerpt, an unmet dependency or missing music consent still skips the item.
    """
    policy = queue.get('owner_policy_20261113_t601u') if isinstance(queue, dict) else None
    if not isinstance(policy, dict) or policy.get('effect') != 'explicit_front_order':
        return None
    order = policy.get('order')
    if not isinstance(order, list) or not all(isinstance(item_id, str) and item_id for item_id in order):
        return None
    return order


def launch_band(queue, item):
    """t601u named order, then t422u: Tatooine chain, linked story, singles, music.

    Without t422u the older order remains: unlinked story, then a ready join.
    """
    order = t601_order(queue)
    item_id = item.get('id') if isinstance(item, dict) else None
    if order and item_id in order:
        return (-1, order.index(item_id))
    policy = t422_policy(queue)
    if policy is None:
        return (link_rank(item), 0)
    chain = policy['tatooine_chain']
    if item.get('scene_id') in (policy.get('hold_scenes') or []):
        return (9, 0)
    if item.get('id') in chain:
        return (0, chain.index(item['id']))
    if is_music_dance(queue, item):
        return (3, 0)
    if link_rank(item) == 1:
        return (1, 0)
    return (2, 0)


def launch_candidates(root, limit=None):
    """Priority order of items that are actually ready to Create. Read-only.

    With t601u: the named front order, then the t422u bands.
    With t422u: the Tatooine chain, then other linked story, then singles, then music.
    Otherwise: story with no link, then story whose join is already ready.
    Music and dance are not a fallback: t369u requires a new owner consent.
    A missing excerpt or an unmet dependency is never skipped past by a priority number.
    """
    root = Path(root)
    queue = read(root / 'ops/topview-launch-queue.json', {})
    derived = {row['id']: row for row in derive(root)['items']}
    items = [item for item in queue.get('items', []) if isinstance(item, dict)]
    held = set((t422_policy(queue) or {}).get('hold_scenes') or [])

    def priority(item):
        value = item.get('priority')
        return (value if type(value) in (int, float) else 10 ** 9, str(item.get('id')))

    chosen, skipped, eligible = [], [], []
    if limit is not None and limit <= 0:
        return {'chosen': chosen, 'skipped': skipped}
    for item in sorted(items, key=priority):
        item_id = item.get('id')
        row = derived.get(item_id) or {}
        if item.get('scene_id') in held:
            reason = 'owner_hold'
        elif item.get('state') != 'waiting_for_slot' or row.get('code') != 'ready' or row.get('ready') is not True:
            reason = row.get('code') or item.get('state') or 'not_ready'
        elif substantive_refusal(item):
            reason = 'substantive_refusal'
        elif continuity_blocks_launch(item, root):
            reason = 'continuity_excerpt_missing'
        elif music_create_blocked(queue, item):
            reason = 'music_owner_consent_required'
        else:
            reason = None
        if reason:
            skipped.append({'id': item_id, 'reason': reason})
            continue
        eligible.append(item)
    ordered = sorted(eligible, key=lambda item: (launch_band(queue, item), priority(item)))
    for item in ordered:
        chosen.append(item.get('id'))
        if limit is not None and len(chosen) >= limit:
            break
    return {'chosen': chosen, 'skipped': skipped}


def write(root):
    root = Path(root)
    if not (root/'ops/topview-launch-queue.json').exists(): return False
    body = derive(root)
    p = root/'ops/queue-readiness.json'
    old = read(p, {})
    if {k:v for k,v in old.items() if k != 'checked_at'} == body: return False
    body['checked_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    p.write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n')
    return True

if __name__ == '__main__':
    print('Queue readiness updated' if write(sys.argv[1] if len(sys.argv)>1 else '.') else 'Queue readiness unchanged')
