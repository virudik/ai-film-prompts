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
    tasks.update({t['task_id']: t.get('status') for t in tv.get('active_tasks', [])})
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
        if code == 'ready' and music_dance_new_launch_blocked(q, i):
            code = 'owner_hold'
            reasons.append('По решению владельца 08.11.2026 20:16 МСК: новые музыкально-танцевальные запуски и их связки отложены; уже идущие не отменяются')
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


def music_dance_new_launch_blocked(queue, item):
    """Owner t364u, 08.11.2026 20:16 MSK: do not Create new music/dance items.

    Scenes 28, 49, 50 and 51, including their linked parts. Submitted, submitting
    and submission_unknown rows stay as they are. A claim that has no task and no
    submission intent is not a running render. The record is absent until this
    one decision is written on the queue; this is not a standing global filter.
    """
    hold = queue.get('owner_hold_20261108_t364u') if isinstance(queue, dict) else None
    if not isinstance(hold, dict) or hold.get('effect') != 'no_new_launches':
        return False
    if not isinstance(item, dict):
        return False
    scenes = hold.get('scenes')
    if not isinstance(scenes, list) or item.get('scene_id') not in scenes:
        return False
    if item.get('task_id'):
        return False
    state = str(item.get('state') or '')
    if state in ('submitted', 'submitting', 'submission_unknown', 'completed') or state.startswith(('cancelled', 'superseded')):
        return False
    claim = item.get('claim') if isinstance(item.get('claim'), dict) else {}
    if claim.get('submission_intent_id'):
        return False
    return state in ('waiting_for_slot', 'claimed')


def launch_candidates(root, limit=None):
    """Priority order of items that are actually ready to Create. Read-only."""
    root = Path(root)
    queue = read(root / 'ops/topview-launch-queue.json', {})
    derived = {row['id']: row for row in derive(root)['items']}
    items = [item for item in queue.get('items', []) if isinstance(item, dict)]

    def priority(item):
        value = item.get('priority')
        return (value if type(value) in (int, float) else 10 ** 9, str(item.get('id')))

    chosen, skipped = [], []
    if limit is not None and limit <= 0:
        return {'chosen': chosen, 'skipped': skipped}
    for item in sorted(items, key=priority):
        item_id = item.get('id')
        row = derived.get(item_id) or {}
        if item.get('state') != 'waiting_for_slot' or row.get('code') != 'ready' or row.get('ready') is not True:
            reason = row.get('code') or item.get('state') or 'not_ready'
        elif substantive_refusal(item):
            reason = 'substantive_refusal'
        elif continuity_blocks_launch(item, root):
            reason = 'continuity_excerpt_missing'
        elif music_dance_new_launch_blocked(queue, item):
            reason = 'owner_hold'
        else:
            reason = None
        if reason:
            skipped.append({'id': item_id, 'reason': reason})
            continue
        chosen.append(item_id)
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
