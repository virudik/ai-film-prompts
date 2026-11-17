#!/usr/bin/env python3
"""Read-only admission check. Caller supplies authenticated Relay sender metadata.

Never interpret sender claims in message text as authentication. No ACK/write/
Topview action is performed here; the receiving agent owns lease/CAS/readback.
"""
import hashlib
import json
import re
from datetime import datetime, timezone

import relay_wake
import site_alerts
import wake_roles


def validate(root, text, *, actor, authenticated_sender_id, allowed_test_ids=(), now=None):
    def reject(reason):
        return {'accepted': False, 'reason': reason}
    if not isinstance(text, str) or actor not in ('dot', 'grok'):
        return reject('invalid_input')
    cfg = relay_wake.load_config(root)
    if (not isinstance(cfg, dict) or not cfg.get('sender_agent_id') or
            authenticated_sender_id != cfg['sender_agent_id']):
        return reject('wrong_authenticated_sender')
    roles = wake_roles.resolve(cfg)
    routing = cfg.get('site_alert_routing')
    if roles is None or not isinstance(routing, dict):
        return reject('invalid_config')
    lines = text.splitlines()
    if not lines:
        return reject('missing_marker')
    fields = {}
    for line in lines[1:]:
        if '=' in line and not line.startswith('- '):
            key, value = line.split('=', 1)
            if key in ('test_id', 'recipient_role', 'recipient_actor', 'occurrence_set', 'read_only'):
                if key in fields:
                    return reject('duplicate_field')
                fields[key] = value
    role = fields.get('recipient_role')
    if role not in ('primary', 'backup') or roles[role + '_actor'] != actor or fields.get('recipient_actor') != actor:
        return reject('wrong_current_recipient')
    if lines[0] == 'SITE_ALERT_V2_TEST':
        test_id = fields.get('test_id', '')
        if (routing.get('enabled') is not False or fields.get('read_only') != 'true' or
                not re.fullmatch(r'[A-Za-z0-9_-]{8,80}', test_id) or test_id not in allowed_test_ids):
            return reject('test_not_authorized')
        return {'accepted': True, 'kind': 'test', 'test_id': test_id, 'actor': actor, 'role': role,
                'write_allowed': False}
    if (routing.get('enabled') is not True or cfg.get('site_alert_enabled') is not True or
            routing.get('mode') not in ('dot_then_grok', 'primary_then_backup') or
            not lines[0].startswith('SITE_ALERT_V2 ')):
        return reject('production_disabled_or_wrong_marker')
    incident_id = lines[0].split(' ', 1)[1]
    state = site_alerts.load_state(root)
    if state.get('schema_version') != 2 or state.get('incident_id') != incident_id:
        return reject('stale_incident')
    if (state.get('primary_actor', 'dot') != roles['primary_actor'] or
            state.get('backup_actor', 'grok') != roles['backup_actor']):
        return reject('stale_roles')
    alerts = site_alerts.collect(root, now or datetime.now(timezone.utc))
    if not alerts or state.get('signature') != site_alerts.signature(alerts):
        return reject('problem_changed_or_resolved')
    versions = state.get('problem_versions', {})
    if not isinstance(versions, dict) or any(type(versions.get(a['code'])) is not int for a in alerts):
        return reject('invalid_occurrence_versions')
    occurrences = sorted(f"{a['code']}|critical={bool(a.get('critical'))}|{versions[a['code']]}" for a in alerts)
    token = hashlib.sha256(json.dumps(occurrences).encode()).hexdigest()[:20]
    if fields.get('occurrence_set') != token:
        return reject('stale_occurrence')
    return {'accepted': True, 'kind': 'production', 'incident_id': incident_id,
            'actor': actor, 'role': role, 'write_allowed': False,
            'next_gate': 'fresh_progress_and_exact_own_lease_CAS_readback'}
