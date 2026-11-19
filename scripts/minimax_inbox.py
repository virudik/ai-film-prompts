#!/usr/bin/env python3
"""Read-only Minimax inbox/slot hint for the Minimax peer routine. No wake, writes or Create."""
import argparse
import json
from pathlib import Path


def pending(root):
    root = Path(root)
    def read(p, default):
        path=root/p
        return json.loads(path.read_text()) if path.exists() else default
    inbox=read('ops/owner-tasks.json', {'tasks': []})
    cfg=read('ops/slot-backup.json', {})
    tv=read('topview-status.json', {})
    monitor=read('automation-monitor-status.json', {})
    policy=cfg.get('minimax_launcher', {}) or {}
    peer=(cfg.get('peers') or {}).get('minimax') or {}
    tasks=[t for t in inbox.get('tasks', []) if t.get('to')=='minimax' and t.get('status') in ('open','taken')]
    return {'schema_version':1, 'tasks':tasks,
            'peer_enabled': peer.get('enabled') is True,
            'launcher_enabled': policy.get('enabled') is True,
            'transport': policy.get('transport'),
            'runtime_run_id': policy.get('runtime_run_id'),
            'runtime_run_id_unavailable_reason': policy.get('runtime_run_id_unavailable_reason'),
            'telemetry_checked_at':tv.get('checked_at'),
            'launcher_health':monitor.get('launcher_health'),
            'receipt': peer.get('receipt'),
            'scope':'Hint only. Pull fresh main, take your own lease, live full global scan and intent before any Create.',
            'scheduled_runtime_verified': False}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('root',type=Path)
    print(json.dumps(pending(ap.parse_args().root),ensure_ascii=False,indent=2))
