#!/usr/bin/env python3
"""One explicitly confirmed, read-only site canary. Never writes repository state."""
import argparse
import re
import relay_wake


def send(root, test_id, recipient, confirm=False, sender=None):
    if confirm is not True:
        return 'disabled', 'explicit read-only confirmation required'
    if not isinstance(test_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]{8,80}', test_id):
        return 'error', 'invalid test ID'
    if recipient not in ('dot', 'grok'):
        return 'error', 'invalid recipient'
    cfg = relay_wake.load_config(root)
    routing = cfg.get('site_alert_routing') or {}
    # Acceptance precedes activation. Never change this flag as a test side effect.
    if routing.get('enabled') is not False:
        return 'error', 'reviewed disabled V2 config required'
    address = routing.get('primary_address' if recipient == 'dot' else 'backup_address')
    if not address:
        return 'error', 'reviewed recipient address required'
    role = 'primary' if recipient == 'dot' else 'backup'
    text = ('SITE_ALERT_V2_TEST\ntest_id=' + test_id + '\nrecipient_role=' + role +
            '\nread_only=true\nNo Topview, Create, queue, lease or production ACK writes. '
            'Report actual receipt metadata only; this is not production incident progress.')
    sender = sender or relay_wake.send_dm
    return sender(root, text, address=address, key_prefix='site-canary-', require_enabled=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--test-id', required=True)
    ap.add_argument('--recipient', choices=['dot', 'grok'], required=True)
    ap.add_argument('--confirm-read-only', action='store_true')
    a = ap.parse_args()
    status, detail = send(a.root, a.test_id, a.recipient, a.confirm_read_only)
    print(status, detail)
    return 0 if status == 'sent' else 1


if __name__ == '__main__':
    raise SystemExit(main())
