#!/usr/bin/env python3
"""Check selected operational invariants; never pretend this is a full semantic audit.

Live Automations data must come from a fresh peek, supplied locally with --automations.
Only hashes, IDs and outcomes are written to the public report, never full prompts/results.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from cert_github import FILES, blob

HOURLY = '6acae6ab433481919e88665c520b8ef2'
RELAY = '6adc585e7ac08191bb93825117dc7213'


def check(root, snapshot=None, now=None):
    root = Path(root)
    now = now or datetime.now(timezone.utc)
    problems = []
    def require(ok, code):
        if not ok:
            problems.append(code)
    def read(name):
        return (root / name).read_text(encoding='utf-8')
    cert = json.loads(read('instruction-sync-status.json'))
    require(cert.get('source_of_truth') == 'github', 'certificate-authority')
    require(cert.get('schema_version') == 3, 'certificate-legacy-schema')
    require(not any(k in cert for k in ('error_prevention_architecture', 'control_center_owner_ui',
                                      'topview_liveness', 'semantic_check')), 'certificate-legacy-metadata')
    for name in FILES:
        data = (root / name).read_bytes()
        info = cert.get('files', {}).get(name, {})
        require(info.get('github_blob') == blob(data) and
                info.get('mirror_sha256') == hashlib.sha256(data).hexdigest(), 'certificate-bytes:' + name)
    claude = read('CLAUDE.md')
    require(cert.get('claude_code_bootstrap', {}).get('github_blob') == blob((root / 'CLAUDE.md').read_bytes()),
            'claude-bootstrap-hash')
    require('ops/CANON-LOCK.md' in claude and 'ops/OWNER-TASKS.md' in claude, 'claude-routing')
    owner = read('ops/OWNER-TASKS.md')
    require('строго больше 3 часов' in owner and '«Только Claude»' in owner, 'owner-three-hour-rule')
    require('Ответ ChatGPT в тот же тред Claude' in owner, 'same-thread-reply')
    require('archive/ops/owner-tasks-archive.json' in owner, 'inbox-retention-rule')
    runtime = json.loads(read('automation-monitor-status.json')).get('automation', {})
    schedule = cert.get('automation_schedule', {})
    require(all(schedule.get(k) == runtime.get(v) for k, v in
                [('active_automation_id', 'id'), ('schedule', 'schedule'), ('timezone', 'timezone')]),
            'certificate-hourly-config')
    observations = []
    live_status = 'not_checked'
    if snapshot is not None:
        live_status = 'checked'
        try:
            seen = datetime.fromisoformat(snapshot['checked_at'].replace('Z', '+00:00'))
            require(seen.tzinfo is not None and 0 <= (now - seen).total_seconds() <= 3600,
                    'automation-observation-stale')
        except (KeyError, ValueError, TypeError):
            require(False, 'automation-observation-invalid-date')
        items = snapshot.get('automations', [])
        require(len(items) == 2 and {a.get('id') for a in items} == {HOURLY, RELAY}, 'automation-set')
        for a in items:
            prompt = a.get('prompt', '')
            flat = re.sub(r'\s+', '', prompt).lower()
            require(a.get('is_enabled') is True, 'automation-disabled:' + str(a.get('id')))
            require('ops/OWNER-TASKS.md' in prompt and 'строго больше 3 часов' in prompt and
                    'только Claude' in prompt, 'automation-owner-rule:' + str(a.get('id')))
            require('Новые строки в owner-tasks добавляет робот, не агент.' not in prompt,
                    'automation-agent-task-ban')
            if a.get('id') == HOURLY:
                require('FREQ=HOURLY' in a.get('schedule', '') and 'BYMINUTE=55' in a.get('schedule', '') and
                        a.get('default_timezone') == 'Europe/Moscow', 'automation-hourly-schedule')
                require('ops/AUTOMATION-CONSISTENCY.md' in prompt, 'automation-weekly-consistency')
                for stale in ('51bждётфактический51a', '56—42p2', '48—56p2'):
                    require(stale not in flat, 'automation-stale-dependency:' + stale)
            if a.get('id') == RELAY:
                require('X-UNSCHEDULED:1' in a.get('schedule', ''), 'relay-polling-added')
                require(all(s in prompt for s in ('slots:', 'no_update', 'receipt_not_saved')),
                        'relay-receipt-contract')
            observations.append({'id': a.get('id'), 'updated_at': a.get('updated_at'),
                                 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest()})
        subs = snapshot.get('relay_subscriptions', [])
        require(len(subs) == 1 and subs[0].get('event') == 'relay.message' and
                subs[0].get('active') is True and subs[0].get('arguments') == {}, 'relay-subscription')
    return {'schema_version': 1, 'checked_at': now.isoformat(), 'status': 'warn' if problems else 'ok',
            'scope': 'Selected consistency invariants only; full semantic review and runtime success are separate.',
            'live_automations': live_status, 'automation_observations': observations, 'problems': problems}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.')
    ap.add_argument('--automations', help='Fresh sanitized peek snapshot in a local temporary file')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    snapshot = json.loads(Path(a.automations).read_text()) if a.automations else None
    result = check(a.root, snapshot)
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if a.write:
        path = Path(a.root) / 'reports/instruction-consistency.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    print(text, end='')
    return bool(result['problems'])


if __name__ == '__main__':
    raise SystemExit(main())
