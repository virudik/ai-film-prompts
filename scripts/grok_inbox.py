#!/usr/bin/env python3
"""Read-only Grok inbox/slot hint for the existing provider routine. No wake, writes or Create."""
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
    tasks=[t for t in inbox.get('tasks', []) if t.get('to')=='grok' and t.get('status') in ('open','taken')]
    return {'schema_version':1, 'tasks':tasks, 'configuration': cfg.get('grok_launcher', {}).get('coverage'),
            'telemetry_checked_at':tv.get('checked_at'), 'launcher_health':monitor.get('launcher_health'),
            'scope':'Hint only. Pull fresh main, claim own task; live full global scan, lease and intent before any Create.',
            'scheduled_runtime_verified': False}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('root',type=Path)
    print(json.dumps(pending(ap.parse_args().root),ensure_ascii=False,indent=2))
