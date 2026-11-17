#!/usr/bin/env python3
"""One interface for phased launch coordination. Never publishes or calls Topview."""
import argparse
import copy
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import launcher_coordination as lc
import launcher_run_ledger as ledger_tools


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


def snapshot(root):
    """Refresh remote main each phase. No local draft is a remote readback."""
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
    git('fetch', 'origin', 'main')
    head = git('rev-parse', 'HEAD')
    if head != git('rev-parse', 'refs/remotes/origin/main'):
        raise lc.Blocked('checkout_must_equal_fresh_origin_main')
    if git('status', '--porcelain', '--untracked-files=no'):
        raise lc.Blocked('tracked_checkout_must_be_clean')
    return head


def materialize_snapshot(root, sha, destination):
    """Read guards from immutable Git blobs, never mutable/skip-worktree bytes."""
    raw = subprocess.check_output(['git', '-C', str(root), 'ls-tree', '-rz', sha])
    tree = {}
    for row in raw.split(b'\0'):
        if not row:
            continue
        metadata, name = row.split(b'\t', 1)
        mode, kind, oid = metadata.decode().split()
        tree[name.decode()] = (mode, kind, oid)
    def copy_blob(path, required=False):
        relative = Path(path)
        if relative.is_absolute() or '..' in relative.parts:
            raise lc.Blocked('reference_path_outside_snapshot')
        meta = tree.get(path)
        if meta is None:
            if required:
                raise lc.Blocked('canonical_blob_missing:' + path)
            return
        mode, kind, oid = meta
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise lc.Blocked('canonical_regular_blob_required:' + path)
        data = subprocess.check_output(['git', '-C', str(root), 'cat-file', 'blob', oid])
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for path in (lc.CONFIG, lc.LOCK, lc.QUEUE):
        copy_blob(path, required=True)
    for path in (ledger_tools.PATH, 'topview-task-map.json', 'topview-status.json'):
        copy_blob(path)
    queue = lc.read(destination / lc.QUEUE)
    paths = {ref['path'] for item in queue.get('items', []) + queue.get('archived_items', [])
             for ref in item.get('references', []) if ref.get('path')}
    for path in sorted(paths):
        copy_blob(path)


def one_item(queue, item_id):
    found = [i for i in queue.get('items', []) if i.get('id') == item_id]
    if len(found) != 1:
        raise lc.Blocked('item_not_unique')
    return found[0]


def published_session_item(queue, phase, request, session):
    """Read-only boundary check. Repeat under exclusive marker before mutation."""
    if (not isinstance(session, dict) or session.get('schema_version') != 1
            or session.get('actor_sha') != digest(request['actor'])
            or session.get('item_id') != request.get('item_id')):
        raise lc.Blocked('original_session_actor_and_item_required')
    required = {'intent': 'claim_prepared', 'verify': 'intent_prepared'}[phase]
    if session.get('phase') != required:
        raise lc.Blocked('phase_already_consumed_or_out_of_order; reconcile_without_Create')
    item = one_item(queue, session['item_id'])
    if digest(item) != session['expected_item_sha']:
        raise lc.Blocked('original_payload_not_published_exactly; reconcile_without_Create')
    return item


def unchanged_claim_history(root, session, current_sha):
    """Local immutable Git history only; no inference from a connector error."""
    base = session.get('claim_base_main_sha')
    if not base or not session.get('base_item_sha'):
        raise lc.Blocked('original_claim_base_history_required')
    if subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', base, current_sha],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
        raise lc.Blocked('claim_base_not_ancestor_of_fresh_main')
    commits = subprocess.check_output(['git','-C',str(root),'rev-list','--ancestry-path',base+'..'+current_sha], text=True).split()
    if len(commits) > 100:
        raise lc.Blocked('claim_history_window_requires_manual_reconciliation')
    baseline_ledger = None
    for sha in [base] + list(reversed(commits)):
        queue = json.loads(subprocess.check_output(['git','-C',str(root),'show',sha+':'+lc.QUEUE]))
        if digest(one_item(queue, session['item_id'])) != session['base_item_sha']:
            raise lc.Blocked('claim_item_changed_in_main_history')
        ledger = subprocess.check_output(['git','-C',str(root),'show',sha+':'+ledger_tools.PATH])
        ledger_sha = hashlib.sha256(ledger).hexdigest()
        if baseline_ledger is not None and ledger_sha != baseline_ledger:
            raise lc.Blocked('ledger_changed_during_claim_publication')
        baseline_ledger = ledger_sha
    return {'base_main_sha':base, 'readback_main_sha':current_sha,
            'session_sha':digest(session), 'item_unchanged':True, 'ledger_unchanged':True}


def step(root, phase, request, session, now, main_sha):
    """Pure planning/validation except reads. Caller persists returned session first.

    Original identities are saved locally, never reconstructed from remote readback.
    This state is an anti-replay aid, not authority to resume interrupted execution.
    """
    cfg, lock, queue = (lc.read(root / p) for p in (lc.CONFIG, lc.LOCK, lc.QUEUE))
    actor = request['actor']
    lc.check_route(cfg, actor, now)
    scan = request.get('scan') or {}
    if phase == 'plan':
        candidates = lc.queue_readiness.launch_candidates(root, limit=1)
        return {'phase': 'plan', 'main_sha': main_sha, 'selection': candidates,
                'lock': lock, 'create_allowed': False,
                'next': 'prepare verified form and live scan; acquire own lease via separate CAS/readback'}, None
    if phase in ('claim', 'refresh-claim'):
        if phase == 'claim' and session is not None:
            raise lc.Blocked('session_already_exists; reconcile_without_Create')
        item = one_item(queue, request['item_id'])
        previous_claim_id = None
        if phase == 'refresh-claim':
            if (not isinstance(session, dict) or session.get('schema_version') != 1
                    or session.get('phase') != 'claim_prepared'
                    or session.get('actor_sha') != digest(actor) or session.get('item_id') != item['id']
                    or not session.get('base_item_sha') or digest(item) != session['base_item_sha']):
                raise lc.Blocked('unchanged_unpublished_claim_base_required')
            history = request.get('_claim_history') or {}
            if (history.get('base_main_sha') != session.get('claim_base_main_sha')
                    or history.get('readback_main_sha') != main_sha
                    or history.get('session_sha') != digest(session)
                    or history.get('item_unchanged') is not True or history.get('ledger_unchanged') is not True):
                raise lc.Blocked('fresh_unpublished_claim_history_required')
            previous_claim_id = session.get('claim_id')
            if not previous_claim_id:
                raise lc.Blocked('original_claim_identity_required')
        ledger = lc.read(root / ledger_tools.PATH) if ledger_tools.required(cfg, actor) else None
        updated = lc.prepare_claim(cfg, lock, item, actor, scan, now,
                                   request['preflight'], main_sha, root, ledger, queue.get('board_id'))
        if previous_claim_id:
            updated['claim']['claim_id'] = previous_claim_id
        session = {'schema_version': 1, 'phase': 'claim_prepared', 'actor_sha': digest(actor),
                   'item_id': item['id'], 'claim_id': updated['claim']['claim_id'],
                   'expected_item_sha': digest(updated), 'base_item_sha': digest(item),
                   'claim_base_main_sha': main_sha}
        updated_ledger = None
    else:
        item = published_session_item(queue, phase, request, session)
        ledger = lc.read(root / ledger_tools.PATH) if ledger_tools.required(cfg, actor) else None
        if phase == 'verify':
            lc.verify_before_create(cfg, lock, item, actor, scan, now,
                                    session['claim_id'], session['intent_id'], ledger, root,
                                    session['expected_payload_sha'])
            out = dict(session, phase='verify_consumed')
            return {'phase': 'verify', 'checks_passed': True, 'main_sha': main_sha,
                    'create_allowed': 'one_click_only_in_same_uninterrupted_execution',
                    'replay_permitted': False,
                    'next': 'one UI Create now; save task receipt or unknown, never retry ambiguous submission'}, out
        updated, updated_ledger = lc.prepare_transaction(cfg, lock, item, actor, scan, now,
                                                        ledger, queue.get('board_id'), root)
        session = dict(session, phase='intent_prepared', expected_item_sha=digest(updated),
                       intent_id=updated['claim']['submission_intent_id'],
                       expected_payload_sha=updated['claim']['intent_payload_sha256'])
    changed_queue = copy.deepcopy(queue)
    changed_queue['items'][queue['items'].index(item)] = updated
    files = {lc.QUEUE: changed_queue}
    if updated_ledger is not None:
        files[ledger_tools.PATH] = updated_ledger
    return {'phase': phase, 'expected_main_sha': main_sha, 'files': files,
            'publish_together': True, 'create_allowed': False,
            'next': 'CAS publish these files together; fetch/check out main; run next phase with fresh scan'}, session


def assess_preclaim_abort(root, session_path, failure_output, process_result,
                          actor, item_id, scan, now, main_sha, original_request=None):
    """Read-only eligibility for recording a proven pre-step abort, never a retry permit.

    root must be an immutable fresh snapshot; process_result must come from the
    actual command runner, not a PID guess. Existing markers are retained.
    """
    if (process_result.get('exited') is not True or process_result.get('exit_code') != 2
            or process_result.get('output_complete') is not True
            or process_result.get('phase') != 'claim'
            or process_result.get('session_path') != str(session_path.resolve())):
        raise lc.Blocked('complete_exited_initial_claim_evidence_required')
    if (not isinstance(main_sha, str) or len(main_sha) != 40
            or any(c not in '0123456789abcdef' for c in main_sha)):
        raise lc.Blocked('fresh_main_sha_required')
    provenance = process_result.get('provenance') or {}
    if (provenance.get('runner_record_id') in (None, '')
            or provenance.get('execution_instance_id') != actor.get('execution_instance_id')
            or provenance.get('legacy_source_sha256') != '76b2b7e15a8394e70ad1338148f50ee03006fc0c89d8ef552a0bfd95e76fca31'
            or provenance.get('marker_absent_before_invocation') is not True
            or provenance.get('marker_created_by_this_invocation') is not True
            or provenance.get('no_remaining_orchestrator') is not True
            or provenance.get('argv_phase') != 'claim'
            or provenance.get('argv_session_path') != str(session_path.resolve())):
        raise lc.Blocked('bound_legacy_invocation_and_marker_provenance_required')
    if (original_request is None or not original_request.is_file() or original_request.is_symlink()
            or provenance.get('argv_request_path') != str(original_request.resolve())
            or provenance.get('captured_request_sha256') != hashlib.sha256(original_request.read_bytes()).hexdigest()):
        raise lc.Blocked('unchanged_original_request_binding_required')
    original = lc.read(original_request)
    if original.get('actor') != actor or original.get('item_id') != item_id:
        raise lc.Blocked('original_request_actor_and_item_required')
    busy = session_path.with_name(session_path.name + '.busy')
    pending = session_path.with_name(session_path.name + '.pending')
    if (os.path.lexists(session_path) or os.path.lexists(pending) or busy.is_symlink()
            or not busy.is_file() or lc.read(busy) != {'phase': 'claim'}):
        raise lc.Blocked('unstarted_claim_marker_only_required')
    if provenance.get('captured_stdout_sha256') != hashlib.sha256(failure_output.read_bytes()).hexdigest():
        raise lc.Blocked('unchanged_complete_failure_output_required')
    failure = lc.read(failure_output)
    reasons = {'checkout_must_equal_fresh_origin_main', 'tracked_checkout_must_be_clean',
               'main_changed_during_phase; reconcile_without_Create'}
    if (set(failure) != {'checks_passed', 'create_allowed', 'reason'}
            or failure.get('checks_passed') is not False or failure.get('create_allowed') is not False
            or failure.get('reason') not in reasons):
        raise lc.Blocked('captured_pre_step_snapshot_rejection_required')
    cfg, lock, queue = (lc.read(root / p) for p in (lc.CONFIG, lc.LOCK, lc.QUEUE))
    lc.check_route(cfg, actor, now)
    # Do not infer idleness from expiry, absence or malformed lock. Reconcile the
    # actual current executor first; this assessment never takes/releases a lease.
    if lock.get('state') != 'free':
        raise lc.Blocked('explicitly_free_current_lease_required')
    item = one_item(queue, item_id)
    if (item.get('state') != 'waiting_for_slot' or item.get('claim') or item.get('task_id')
            or item.get('task_ids') or item.get('submission_intent_id')):
        raise lc.Blocked('item_already_owned_or_consumed; reconcile_without_Create')
    if any(value for key, value in item.items() if 'history' in key or 'archive' in key or key == 'retry_control'):
        raise lc.Blocked('first_attempt_without_history_required')
    if any(row.get('id') == item_id for row in queue.get('archived_items', []) if isinstance(row, dict)):
        raise lc.Blocked('archived_item_requires_general_reconciliation')
    ledger_path = root / ledger_tools.PATH
    if not ledger_path.is_file():
        raise lc.Blocked('fresh_ledger_required')
    ledger = lc.read(ledger_path)
    # Conservative: a mention in any retained ledger row is not an unused first attempt.
    if item_id in json.dumps(ledger, ensure_ascii=False):
        raise lc.Blocked('ledger_item_requires_general_reconciliation')
    lc.check_launch_observation(scan, item_id, now)
    return {'schema_version': 1, 'kind': 'proven_preclaim_abort_assessment',
            'checked_at': lc.stamp(now), 'main_sha': main_sha, 'item_id': item_id,
            'actor_sha': digest(actor), 'item_sha': digest(item),
            'marker_sha256': hashlib.sha256(busy.read_bytes()).hexdigest(),
            'failure_sha256': hashlib.sha256(failure_output.read_bytes()).hexdigest(),
            'failure_reason': failure['reason'],
            'process_evidence_sha256': digest(process_result),
            'request_sha256': hashlib.sha256(original_request.read_bytes()).hexdigest(),
            'scan_sha': digest(scan), 'marker_preserved': True,
            'eligible_for_abort_record': True, 'create_allowed': False,
            'new_session_allowed_by_this_report': False,
            'next': 'publish abort evidence under own exact lease/CAS/readback, then independently recheck live state; no old phase resume'}


def write_exclusive(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', type=Path)
    ap.add_argument('phase', choices=('plan', 'claim', 'refresh-claim', 'intent', 'verify'))
    ap.add_argument('--request', required=True, type=Path)
    ap.add_argument('--session', type=Path, help='Private local anti-replay file; outside checkout; never publish')
    args = ap.parse_args()
    guard = None
    try:
        root = args.root.resolve()
        if args.phase != 'plan':
            if args.session is None:
                raise lc.Blocked('private_session_path_required')
            path = args.session.resolve()
            if path == root or root in path.parents:
                raise lc.Blocked('session_must_be_outside_repository')
            guard = path.with_name(path.name + '.busy')
        # Snapshot validation is read-only: a clean pre-phase mismatch must not
        # consume the local session. Existing crash markers are never removed.
        sha = snapshot(root)
        request = lc.read(args.request)
        with tempfile.TemporaryDirectory(prefix='launcher-readback-') as directory:
            isolated = Path(directory)
            materialize_snapshot(root, sha, isolated)
            # Network may be slow. Finish the final fetch BEFORE freshness checks.
            if snapshot(root) != sha:
                raise lc.Blocked('main_changed_during_phase; reconcile_without_Create')
            if args.phase == 'refresh-claim':
                prior = lc.read(args.session) if args.session and args.session.exists() else {}
                request['_claim_history'] = unchanged_claim_history(root, prior, sha)
            if args.phase in ('intent', 'verify'):
                prior = lc.read(args.session) if args.session and args.session.exists() else None
                published_session_item(lc.read(isolated / lc.QUEUE), args.phase, request, prior)
            if guard:
                write_exclusive(guard, {'phase': args.phase})
            # Serialize before reading phase state; a concurrent caller must not
            # use a stale session read from before the exclusive marker.
            session = lc.read(args.session) if args.session and args.session.exists() else None
            result, updated = step(isolated, args.phase, request, session, datetime.now(timezone.utc), sha)
        if updated is not None:
            if args.phase == 'claim':
                write_exclusive(args.session, updated)
            else:
                pending = args.session.with_name(args.session.name + '.pending')
                write_exclusive(pending, updated)
                os.replace(pending, args.session)
        # Persist consuming state BEFORE returning any permission or transaction.
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
        if guard:
            guard.unlink()
        return 0
    except (lc.Blocked, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        # Keep marker on errors: ambiguous partial work must not be blindly replayed.
        print(json.dumps({'checks_passed': False, 'create_allowed': False, 'reason': str(error)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
