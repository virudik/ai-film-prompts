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
    if phase == 'claim':
        if session is not None:
            raise lc.Blocked('session_already_exists; reconcile_without_Create')
        item = one_item(queue, request['item_id'])
        ledger = lc.read(root / ledger_tools.PATH) if ledger_tools.required(cfg, actor) else None
        updated = lc.prepare_claim(cfg, lock, item, actor, scan, now,
                                   request['preflight'], main_sha, root, ledger, queue.get('board_id'))
        session = {'schema_version': 1, 'phase': 'claim_prepared', 'actor_sha': digest(actor),
                   'item_id': item['id'], 'claim_id': updated['claim']['claim_id'],
                   'expected_item_sha': digest(updated)}
        updated_ledger = None
    else:
        if (not isinstance(session, dict) or session.get('schema_version') != 1 or
                session.get('actor_sha') != digest(actor) or
                session.get('item_id') != request.get('item_id')):
            raise lc.Blocked('original_session_actor_and_item_required')
        required_phase = {'intent': 'claim_prepared', 'verify': 'intent_prepared'}[phase]
        if session.get('phase') != required_phase:
            raise lc.Blocked('phase_already_consumed_or_out_of_order; reconcile_without_Create')
        item = one_item(queue, session['item_id'])
        if digest(item) != session['expected_item_sha']:
            raise lc.Blocked('original_payload_not_published_exactly; reconcile_without_Create')
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


def write_exclusive(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', type=Path)
    ap.add_argument('phase', choices=('plan', 'claim', 'intent', 'verify'))
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
            write_exclusive(guard, {'phase': args.phase})
        # After a local crash the busy marker remains. Never delete to retry Create.
        sha = snapshot(root)
        request = lc.read(args.request)
        session = lc.read(args.session) if args.session and args.session.exists() else None
        with tempfile.TemporaryDirectory(prefix='launcher-readback-') as directory:
            isolated = Path(directory)
            materialize_snapshot(root, sha, isolated)
            # Network may be slow. Finish the final fetch BEFORE freshness checks.
            if snapshot(root) != sha:
                raise lc.Blocked('main_changed_during_phase; reconcile_without_Create')
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
