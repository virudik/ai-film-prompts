import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import site_alert_canary as canary


class CanaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'ops').mkdir()
        self.cfg = {'site_alert_routing': {'enabled': False, 'primary_address': 'dot@example', 'backup_address': 'grok@example'}}
        self.save()
        self.calls = []

    def save(self):
        (self.root / 'ops/relay-wake.json').write_text(json.dumps(self.cfg))

    def sender(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return 'sent', 'message_id=123'

    def call(self, **kw):
        return canary.send(self.root, kw.get('test_id', 'site-test-123'), kw.get('recipient', 'dot'), kw.get('confirm', True), self.sender)

    def test_explicit_boolean_confirmation(self):
        for value in (False, None, 'true', 1):
            self.assertEqual(self.call(confirm=value)[0], 'disabled')
        self.assertEqual(self.calls, [])

    def test_bad_input_never_sends(self):
        for value in ('x', '../test', 'test\ninjection', 'a'*81):
            self.assertEqual(self.call(test_id=value)[0], 'error')
        self.assertEqual(self.call(recipient='other')[0], 'error')
        self.assertEqual(self.calls, [])

    def test_activation_or_missing_config_blocks(self):
        for value in (True, None, 'false', 0):
            self.cfg['site_alert_routing']['enabled'] = value
            self.save()
            self.assertEqual(self.call()[0], 'error')
        self.assertEqual(self.calls, [])

    def test_one_message_no_state_writes_and_stable_retry(self):
        before = {str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(self.call()[0], 'sent')
        self.assertEqual(len(self.calls), 1)
        self.call()
        self.assertEqual(self.calls[0], self.calls[1])
        args, kw = self.calls[0]
        self.assertTrue(args[1].startswith('SITE_ALERT_V2_TEST\n'))
        self.assertIn('recipient_role=primary', args[1])
        self.assertEqual(kw['address'], 'dot@example')
        self.assertEqual(kw['key_prefix'], 'site-canary-')
        self.assertEqual(before, {str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_grok_separate_recipient_and_delivery_key(self):
        self.call()
        self.call(recipient='grok')
        args, kw = self.calls[-1]
        self.assertIn('recipient_role=backup', args[1])
        self.assertEqual(kw['address'], 'grok@example')
        self.assertNotEqual(self.calls[0], self.calls[1])

    def test_transport_failure_is_not_claimed_as_delivery(self):
        def fail(*args, **kw): return 'error', 'HTTP 503'
        self.assertEqual(canary.send(self.root, 'site-test-123', 'dot', True, fail), ('error', 'HTTP 503'))
        self.assertFalse((self.root / 'reports').exists())

    def test_workflow_manual_main_only_and_no_write_permissions(self):
        text = (ROOT / '.github/workflows/site-alert-canary.yml').read_text()
        self.assertIn("github.ref == 'refs/heads/main' && inputs.confirm_read_only == true", text)
        self.assertIn('default: false', text)
        self.assertIn('contents: read', text)
        self.assertNotIn('schedule:', text)
        self.assertNotIn('push:', text)
        self.assertNotIn('contents: write', text)


if __name__ == '__main__':
    unittest.main()
