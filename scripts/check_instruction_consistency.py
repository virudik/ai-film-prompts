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

# Exact leftovers of decisions a later owner record already replaced.
# Archive copies may keep the old sentences; these live files may not.
STALE_PHRASES = (
    ('ops/FUTURE-PLANS.md', 'сюжетную очередь не продолжать', 'stale-phrase:plot-ban-t512'),
    ('ops/FUTURE-PLANS.md', 'Следующие разрешённые запуски — музыка по A-36, не сюжет', 'stale-phrase:music-not-plot'),
    ('ops/FUTURE-PLANS.md', 'Следующее разрешённое — A-36', 'stale-phrase:next-is-a36'),
    ('ops/FUTURE-PLANS.md', 'Танцы 28 последними', 'stale-phrase:dances-last'),
    ('ops/FUTURE-PLANS.md', 'все заново и последними', 'stale-phrase:dances-last-again'),
    ('ops/FUTURE-PLANS.md', 'пока PR 516 не в main', 'stale-phrase:pr516-unmerged'),
    ('ops/FUTURE-PLANS.md', 'на момент 10.11 не в main', 'stale-phrase:parodies-unmerged'),
    ('ops/FUTURE-PLANS.md', 'ещё не отправленная в Topview', 'stale-phrase:t611-unsent'),
    ('ops/FUTURE-PLANS.md', 'PR 369, 370 и 371 не трогать', 'stale-phrase:pr369-open'),
    ('ops/FUTURE-PLANS.md', 'task нет — к запуску', 'stale-phrase:music-ready-to-launch'),
    ('ops/FUTURE-PLANS.md', 'ОЧЕРЕДЬ СЮЖЕТА ЗАКРЫТА', 'stale-phrase:plot-queue-closed'),
    ('ops/CONTINUE-PROTOCOL.md', 'начинается с `chatgpt-scheduled-`', 'stale-phrase:launch-by-name'),
    ('NEW-CHAT-HANDOFF.md', 'PR 369, 370 и 371 не трогать', 'stale-phrase:pr369-open'),
    ('shadow/current-checkpoint.md', 'PR 369, 370 и 371 не трогать', 'stale-phrase:pr369-open'),
)


def dot_current_task_gap(root):
    """Name Dot's current ordinary tasks without treating that as a live check.

    The automation snapshot still accepts only the previous Work pair. Reading
    the canon IDs makes the omission explicit; it does not prove prompt,
    enabled, schedule or subscription, and it does not change those routes.
    """
    root = Path(root)
    ids = []
    sources = []
    slot_path = root / 'ops/slot-backup.json'
    if slot_path.is_file():
        slot = json.loads(slot_path.read_text(encoding='utf-8'))
        ordinary = slot.get('peers', {}).get('ordinary', {}).get('automation_ids') or []
        for item in ordinary:
            if item and item not in ids:
                ids.append(item)
        active = slot.get('active_automation_id')
        if active and active not in ids:
            ids.append(active)
        sources.append('ops/slot-backup.json')
    wake_path = root / 'ops/relay-wake.json'
    if wake_path.is_file():
        handler = json.loads(wake_path.read_text(encoding='utf-8')).get('handler_automation_id')
        if handler and handler not in ids:
            ids.append(handler)
        sources.append('ops/relay-wake.json')
    return {
        'status': 'not_checked',
        'ids': ids,
        'sources': sources,
        'reason': 'No fresh Dot snapshot supplied; canonical IDs are not live verification.',
    }


def check_dot_tasks(root, snapshot, now):
    """Read-only configuration checks, never runtime or delivery certification."""
    result = dot_current_task_gap(root)
    result.update(runtime_status='not_checked', observations=[], problems=[])
    if snapshot is None:
        return result
    errors = result['problems']
    def require(ok, code):
        if not ok:
            errors.append(code)
    try:
        seen = datetime.fromisoformat(snapshot['checked_at'].replace('Z', '+00:00'))
        fresh = seen.tzinfo is not None and 0 <= (now - seen).total_seconds() <= 3600
    except (KeyError, ValueError, TypeError):
        fresh = False
    if not fresh or snapshot.get('source') != 'automations.get':
        result['reason'] = 'Fresh timestamp and automations.get source required.'
        errors.append('dot-observation-invalid-or-stale')
        return result
    root = Path(root)
    try:
        slot = json.loads((root / 'ops/slot-backup.json').read_text())
        wake = json.loads((root / 'ops/relay-wake.json').read_text())
        hourly, relay = slot['active_automation_id'], wake['handler_automation_id']
        allowed = slot['peers']['ordinary']['automation_ids']
        require(hourly != relay and {hourly, relay} <= set(allowed), 'dot-canonical-ids')
    except (OSError, ValueError, KeyError, TypeError):
        result['reason'] = 'Canonical Dot task registry unavailable.'
        errors.append('dot-registry-unavailable')
        return result
    items = snapshot.get('automations', [])
    require(isinstance(items, list) and len(items) == 2 and
            all(isinstance(a, dict) for a in items) and
            {a.get('id') for a in items} == {hourly, relay}, 'dot-automation-set')
    for a in items if isinstance(items, list) else []:
        if not isinstance(a, dict) or a.get('id') not in (hourly, relay):
            continue
        aid = a['id']; prompt = a.get('prompt', ''); schedule = a.get('schedule', '')
        if not isinstance(prompt, str):
            prompt = ''
        if not isinstance(schedule, str):
            schedule = ''
        enabled = a.get('is_enabled') is True
        require(enabled, 'dot-disabled:' + aid)
        required = ('PRIMARY-BACKUP-WAKE', 'LAUNCHER-COORDINATION', 'TOPVIEW-RETRY',
                    'CAS', 'readback', 'Unlimited', 'PROVENANCE')
        prompt_ok = isinstance(prompt, str) and all(x in prompt for x in required)
        require(prompt_ok, 'dot-prompt-invariants:' + aid)
        rules = []
        schedule_valid = True
        for line in schedule.splitlines():
            if line.startswith(('RDATE', 'EXDATE', 'EXRULE')):
                schedule_valid = False
            if line.startswith('RRULE:'):
                rule = {}
                for part in line[6:].split(';'):
                    if '=' not in part:
                        schedule_valid = False
                        continue
                    key, value = part.split('=', 1)
                    if key in rule or not key or not value:
                        schedule_valid = False
                    rule[key] = value
                rules.append(rule)
        if aid == hourly:
            schedule_ok = (schedule_valid and len(rules) == 1 and rules[0].get('FREQ') == 'HOURLY' and
                           rules[0].get('INTERVAL', '1') == '1' and rules[0].get('BYMINUTE') == '0' and
                           rules[0].get('BYSECOND') == '0' and
                           set(rules[0]) <= {'FREQ', 'INTERVAL', 'BYMINUTE', 'BYSECOND'} and
                           a.get('default_timezone') == slot.get('timezone') == 'Europe/Moscow' and
                           'X-UNSCHEDULED:1' not in schedule)
        else:
            schedule_ok = schedule_valid and 'X-UNSCHEDULED:1' in schedule.splitlines() and not rules and 'RDATE' not in schedule
        require(schedule_ok, 'dot-schedule:' + aid)
        result['observations'].append({'id': aid, 'enabled': 'ok' if enabled else 'warn',
            'prompt_invariants': 'ok' if prompt_ok else 'warn', 'schedule': 'ok' if schedule_ok else 'warn',
            'updated_at': a.get('updated_at'), 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest()})
    # Connector-wide subscription counts cannot establish task-specific binding.
    subs = snapshot.get('relay_subscriptions')
    if not isinstance(subs, list) or not any(isinstance(s, dict) and s.get('automation_id') == relay for s in subs):
        result['subscription_status'] = 'not_checked'
    else:
        bound = [s for s in subs if isinstance(s, dict) and s.get('automation_id') == relay and s.get('active') is True]
        ok = len(bound) == 1 and bound[0].get('event') == 'relay.message' and bound[0].get('arguments') == {}
        result['subscription_status'] = 'ok' if ok else 'warn'
        require(ok, 'dot-relay-subscription')
    result['status'] = 'warn' if errors else ('ok' if result['subscription_status'] == 'ok' else 'partial')
    result['reason'] = 'Selected configuration invariants only; subscription without exact task binding is not_checked. Runtime and delivery are not checked.'
    return result


def stale_phrases(root):
    root = Path(root)
    found = []
    for rel, needle, code in STALE_PHRASES:
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        haystack = text.casefold() if needle[:1].islower() else text
        probe = needle.casefold() if needle[:1].islower() else needle
        if probe in haystack:
            found.append(code)
    return found


def check(root, snapshot=None, now=None, dot_snapshot=None):
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
    problems.extend(stale_phrases(root))
    dot_result = check_dot_tasks(root, dot_snapshot, now)
    problems.extend(dot_result['problems'])
    return {'schema_version': 1, 'checked_at': now.isoformat(), 'status': 'warn' if problems else 'ok',
            'scope': 'Selected consistency invariants only; full semantic review and runtime success are separate.',
            'live_automations': live_status, 'automation_observations': observations,
            'dot_current_tasks': dot_result, 'problems': problems}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.')
    ap.add_argument('--automations', help='Fresh sanitized peek snapshot in a local temporary file')
    ap.add_argument('--dot-automations', help='Fresh read-only Dot get snapshot; independent of legacy Work pair')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    snapshot = json.loads(Path(a.automations).read_text()) if a.automations else None
    dot_snapshot = json.loads(Path(a.dot_automations).read_text()) if a.dot_automations else None
    result = check(a.root, snapshot, dot_snapshot=dot_snapshot)
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if a.write:
        path = Path(a.root) / 'reports/instruction-consistency.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    print(text, end='')
    return bool(result['problems'])


if __name__ == '__main__':
    raise SystemExit(main())
