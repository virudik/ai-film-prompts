#!/usr/bin/env python3
"""Inventory queued inputs shared by all executors; never grants launch/QC permission."""
import hashlib
import json
import re
import sys
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive(root):
    root = Path(root)
    qp = root / 'ops/topview-launch-queue.json'
    queue = json.loads(qp.read_text())
    assets, items = {}, []
    for item in queue['items']:
        state = item.get('state', '')
        if state in ('submitted', 'completed', 'failed', 'done') or state.startswith(('cancelled', 'superseded')):
            continue
        bindings = []
        for ref in item.get('references', []):
            path, digest = ref.get('path'), ref.get('sha256')
            required = ref.get('required') is not False
            aid = path or ('sha256:' + digest if digest else 'pending:' + item['id'] + ':' + ref.get('slot', '?'))
            available = ref.get('input_status') in (None, 'available')
            data = {'sha256': digest, 'media_type': 'video' if 'Video' in ref.get('slot', '') else 'image', 'available_to': []}
            if path:
                resolved = (root/path).resolve()
                safe = resolved.is_relative_to(root.resolve())
                actual = sha(resolved) if safe and resolved.is_file() else None
                valid = available and actual is not None and bool(digest) and actual == digest
                data.update(storage='github', path=path, actual_sha256=actual,
                            status='shared' if valid else 'missing_or_sha_mismatch',
                            available_to=['chatgpt', 'grok', 'claude'] if valid else [])
            elif ref.get('drive_file_id') and digest:
                valid = available and ref.get('shared_readback_sha256') == digest
                data.update(storage='google_drive', drive_file_id=ref['drive_file_id'],
                            web_view_link=ref.get('web_view_link'), filename=ref.get('filename'),
                            duration_seconds=ref.get('duration_seconds'),
                            status='shared_readback_verified' if valid else 'download_and_verify_required',
                            available_to=['authenticated_owner_agents_or_existing_link_access'] if valid else [],
                            permissions='Existing Drive permissions unchanged; no secrets or signed URLs in GitHub.')
            else:
                valid = False
                data.update(storage='pending_source', status='waiting_result_or_shared_materialization',
                            source_item_id=ref.get('source_item_id'), source_task_id=ref.get('source_task_id'))
            if aid in assets and assets[aid] != data:
                # Preserve individual binding states instead of silently sharing a conflicting definition.
                aid += ':' + item['id'] + ':' + ref.get('slot', '?')
            assets[aid] = data
            bindings.append({'slot': ref.get('slot'), 'asset_id': aid, 'required': required, 'shared_ready': valid})
        items.append({'id': item['id'], 'state': state, 'bindings': bindings,
                      'all_required_inputs_shared': all(x['shared_ready'] for x in bindings if x['required'])})
    return {'schema_version': 1, 'source_queue_sha256': sha(qp),
            'authority': 'GitHub main queue/master/manifests; this is a derived access inventory, not approval.',
            'storage_policy': 'GitHub images and canonical metadata; Google Drive video bytes; Library backup only.',
            'assets': assets, 'items': items}


def write(root):
    root = Path(root)
    out = derive(root)
    (root/'ops/shared-inputs.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    return out

if __name__ == '__main__':
    out = write(sys.argv[1] if len(sys.argv)>1 else '.')
    print(json.dumps({'assets': len(out['assets']), 'items': len(out['items']),
                      'all_required_inputs_shared': sum(i['all_required_inputs_shared'] for i in out['items'])}))
