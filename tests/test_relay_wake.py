"""Robot → Agent Relay DM bridge: exact request, clean no-op without config/token, errors never raise."""
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import relay_wake                                           # noqa: E402
from robot_telemetry import wake_dm_text                    # noqa: E402

CFG = {'enabled': True, 'api_base': 'https://cast.agentrelay.com/v1/', 'address': 'chatgpt@cloud-1'}


class Resp(io.BytesIO):
    status = 201

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class RelayWakeTests(unittest.TestCase):
    def repo(self, cfg):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        (Path(d.name) / 'ops').mkdir()
        if cfg is not None:
            (Path(d.name) / 'ops' / 'relay-wake.json').write_text(json.dumps(cfg))
        return d.name

    def test_sends_one_dm_to_the_configured_address(self):
        seen = []

        def opener(req, timeout):
            seen.append(req)
            return Resp(b'{"ok":true,"data":{"message":{"id":"12345"}}}')
        status, detail = relay_wake.send_dm(self.repo(CFG), 'TOPVIEW_SLOT_WAKE_V2 test', {'event_id': 'result:a'},
                                            token='at_live_x', opener=opener)
        self.assertEqual((status, detail), ('sent', 'message_id=12345'))
        self.assertEqual(len(seen), 1)
        req = seen[0]
        self.assertEqual(req.full_url, 'https://cast.agentrelay.com/v1/dm')
        self.assertEqual(req.get_method(), 'POST')
        self.assertEqual(req.get_header('Authorization'), 'Bearer at_live_x')
        self.assertEqual(json.loads(req.data), {'address': 'chatgpt@cloud-1', 'text': 'TOPVIEW_SLOT_WAKE_V2 test',
                                                'data': {'event_id': 'result:a'}})

    def test_no_config_disabled_or_no_token_is_a_clean_noop(self):
        def boom(*a, **k):
            raise AssertionError('must not call the network')
        self.assertEqual(relay_wake.send_dm(self.repo(None), 't', token='x', opener=boom)[0], 'disabled')
        self.assertEqual(relay_wake.send_dm(self.repo(dict(CFG, enabled=False)), 't', token='x', opener=boom)[0],
                         'disabled')
        self.assertEqual(relay_wake.send_dm(self.repo(CFG), 't', token='  ', opener=boom)[0], 'no_token')

    def test_http_and_network_errors_are_reported_not_raised(self):
        def http_err(req, timeout):
            raise urllib.error.HTTPError(req.full_url, 404, 'nf', {}, io.BytesIO(b'address_not_found'))

        def net_err(req, timeout):
            raise urllib.error.URLError('down')
        st, detail = relay_wake.send_dm(self.repo(CFG), 't', token='at_live_x', opener=http_err)
        self.assertEqual(st, 'error')
        self.assertIn('404', detail)
        self.assertEqual(relay_wake.send_dm(self.repo(CFG), 't', token='at_live_x', opener=net_err)[0], 'error')

    def test_false_success_and_missing_receipt_are_errors(self):
        for payload in (b'{"ok":false}', b'{}', b'[]', b'{"ok":true,"data":{}}', b'not-json'):
            with self.subTest(payload=payload):
                result = relay_wake.send_dm(self.repo(CFG), 't', token='at_live_x',
                                            opener=lambda *a, **k: Resp(payload))
                self.assertEqual(result[0], 'error')

    def test_same_request_has_same_idempotency_key(self):
        a = relay_wake.build_request(CFG, 'at_live_x', 't', {'event_id':'result:a'})
        b = relay_wake.build_request(CFG, 'at_live_x', 't', {'event_id':'result:a'})
        c = relay_wake.build_request(CFG, 'at_live_x', 't', {'event_id':'result:b'})
        self.assertEqual(a.get_header('Idempotency-key'), b.get_header('Idempotency-key'))
        self.assertNotEqual(a.get_header('Idempotency-key'), c.get_header('Idempotency-key'))

    def test_wrong_host_and_admin_token_never_reach_network(self):
        def boom(*a, **k):
            raise AssertionError('must not call the network')
        for cfg, token in ((dict(CFG, api_base='https://other.example/v1'), 'at_live_x'),
                           (CFG, 'rk_live_admin')):
            result = relay_wake.send_dm(self.repo(cfg), 't', token=token, opener=boom)
            self.assertEqual(result[0], 'error')

    def test_error_body_does_not_leak_token(self):
        def fail(req, timeout):
            raise urllib.error.HTTPError(req.full_url, 401, 'bad', {}, io.BytesIO(b'at_live_secret'))
        result = relay_wake.send_dm(self.repo(CFG), 't', token='at_live_secret', opener=fail)
        self.assertEqual(result, ('error', 'HTTP 401'))

    def test_dm_text_carries_marker_event_and_issue(self):
        text = wake_dm_text({'event_id': 'result:abc', 'observed_at': 'T', 'free_slots_global': 1},
                            'https://github.com/virudik/ai-film-prompts/issues/40')
        for expected in ('TOPVIEW_SLOT_WAKE_V2', 'event_id: result:abc', 'issues/40', 'free_slots_global: 1'):
            self.assertIn(expected, text)


if __name__ == '__main__':
    unittest.main()
