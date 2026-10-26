"""Robot → Claude wake: a new open inbox task «кому: Claude» fires the Claude scheduled task once."""
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import claude_task_wake as cw           # noqa: E402

NOW = datetime(2026, 10, 26, 10, 0, tzinfo=timezone.utc)
URL = 'https://api.anthropic.com/v1/claude_code/routines/trig_01ABCdef/fire'


class FakeGit:
    def __init__(self, push_ok=True):
        self.commits, self.push_ok, self.resets = [], push_ok, 0

    def commit(self, message, paths):
        self.commits.append(message)
        return 'abc'

    def push(self):
        return self.push_ok

    def head_is_on_remote(self):
        return self.push_ok

    def reset(self):
        self.resets += 1


class Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class Opener:
    def __init__(self, body=None, error=None):
        self.requests, self.body, self.error = [], body, error

    def open(self, req, timeout=None):
        self.requests.append(req)
        if self.error:
            raise self.error
        return Resp(json.dumps(self.body).encode())


OK = {'type': 'routine_fire', 'claude_code_session_id': 'session_1',
      'claude_code_session_url': 'https://claude.ai/code/session_1'}


def task(tid, to='claude', status='open'):
    return {'id': tid, 'to': to, 'status': status, 'text': 'сделай'}


class ClaudeWakeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'ops').mkdir()
        self.cfg({'enabled': True, 'fire_url': URL, 'targets': ['claude']})

    def tearDown(self):
        self.tmp.cleanup()

    def cfg(self, data):
        (self.root / cw.CONFIG).write_text(json.dumps(data), encoding='utf-8')

    def inbox(self, *tasks):
        (self.root / cw.INBOX).write_text(json.dumps({'tasks': list(tasks)}), encoding='utf-8')

    def state(self):
        return json.loads((self.root / cw.STATE).read_text(encoding='utf-8'))

    def go(self, opener, git=None, token='tok'):
        return cw.run(self.root, git or FakeGit(), token=token, now=NOW, sync=False, opener=opener)

    def test_new_claude_task_fires_once_with_ids_only(self):
        self.inbox(task('t1'), task('t2', to='chatgpt'), task('t3', to='any'), task('t4', status='taken'))
        op = Opener(OK)
        self.assertEqual(self.go(op), 0)
        self.assertEqual(len(op.requests), 1)
        req = op.requests[0]
        self.assertEqual(req.full_url, URL)
        self.assertEqual(req.get_header('Authorization'), 'Bearer tok')
        self.assertEqual(req.get_header('Anthropic-beta'), 'experimental-cc-routine-2026-04-01')
        text = json.loads(req.data)['text']
        self.assertIn('t1', text)
        self.assertNotIn('сделай', text)          # task text is never forwarded
        self.assertEqual(self.state()['fired']['t1']['status'], 'sent')
        self.assertNotIn('t2', self.state()['fired'])
        op2 = Opener(OK)
        self.go(op2)
        self.assertEqual(op2.requests, [])           # same task never fires twice

    def test_targets_any_is_opt_in(self):
        self.cfg({'enabled': True, 'fire_url': URL, 'targets': ['claude', 'any']})
        self.inbox(task('t3', to='any'))
        op = Opener(OK)
        self.go(op)
        self.assertEqual(len(op.requests), 1)

    def test_no_token_disabled_or_bad_url_is_noop(self):
        self.inbox(task('t1'))
        op = Opener(OK)
        self.assertEqual(self.go(op, token=''), 0)
        self.cfg({'enabled': False, 'fire_url': URL})
        self.assertEqual(self.go(op), 0)
        self.assertEqual(op.requests, [])
        self.assertFalse((self.root / cw.STATE).exists())
        self.cfg({'enabled': True, 'fire_url': 'https://evil.example/fire'})
        self.go(op)
        self.assertEqual(op.requests, [])
        self.assertFalse((self.root / cw.STATE).exists())

    def test_rejected_push_fires_nothing(self):
        self.inbox(task('t1'))
        op = Opener(OK)
        git = FakeGit(push_ok=False)
        self.assertEqual(self.go(op, git=git), 1)
        self.assertEqual(op.requests, [])

    def test_error_retried_then_given_up(self):
        self.inbox(task('t1'))
        for i in range(cw.MAX_ATTEMPTS):
            op = Opener(error=urllib.error.HTTPError(URL, 500, 'x', {}, None))
            self.go(op)
            self.assertEqual(len(op.requests), 1)
            self.assertEqual(self.state()['fired']['t1']['attempts'], i + 1)
        op = Opener(OK)
        self.go(op)
        self.assertEqual(op.requests, [])

    def test_unexpected_response_is_error(self):
        self.inbox(task('t1'))
        self.go(Opener({'type': 'other'}))
        self.assertEqual(self.state()['fired']['t1']['status'], 'error')

    def test_reserved_without_outcome_is_never_refired(self):
        self.inbox(task('t1'))
        (self.root / cw.STATE).write_text(json.dumps(
            {'fired': {'t1': {'status': 'reserved', 'attempts': 1, 'at': '2026-10-26T09:00:00Z'}}}), encoding='utf-8')
        op = Opener(OK)
        self.go(op)
        self.assertEqual(op.requests, [])


    def test_any_task_wakes_claude_only_after_nobody_took_it(self):
        self.cfg({'enabled': True, 'fire_url': URL, 'targets': ['claude'], 'any_after_hours': 3})
        fresh = dict(task('a1', to='any'), created_at='2026-10-26T08:30:00+00:00')
        old = dict(task('a2', to='any'), created_at='2026-10-26T06:59:00Z')
        taken = dict(task('a3', to='any', status='taken'), created_at='2026-10-25T06:00:00Z')
        nodate = task('a4', to='any')
        self.inbox(fresh, old, taken, nodate)
        op = Opener(OK)
        self.go(op)
        self.assertEqual(len(op.requests), 1)
        text = json.loads(op.requests[0].data)['text']
        self.assertIn('a2', text)
        for tid in ('a1', 'a3', 'a4'):
            self.assertNotIn(tid, text)

    def test_task_added_by_chatgpt_wakes_claude(self):
        self.inbox(dict(task('chatgpt-202610260900-refs', to='claude'), source='chatgpt'))
        op = Opener(OK)
        self.go(op)
        self.assertEqual(len(op.requests), 1)


if __name__ == '__main__':
    unittest.main()
