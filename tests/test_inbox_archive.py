import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from datetime import timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import robot_site_actions as rsa
from tests.test_site_actions import NOW, files, iso, queue, row


class InboxArchiveTests(unittest.TestCase):
    def old(self, **changes):
        t = {'id': 'claude-old', 'source': 'claude', 'to': 'chatgpt', 'status': 'done',
             'closed_at': iso(NOW - timedelta(days=20)), 'text': 'full task', 'result': 'full result',
             'result_commit': 'abc123', 'unknown_field': {'must': ['survive']}}
        t.update(changes)
        return t

    def test_full_agent_record_and_site_record_archived_with_inbox(self):
        tasks = [self.old(), self.old(id='site-old', source='site'), self.old(id='active', status='taken')]
        f = files(inbox={'tasks': tasks})
        nf, _ = rsa.plan([], f, NOW)
        self.assertEqual(json.loads(nf[rsa.INBOX_ARCHIVE])['tasks'], tasks[:2])
        self.assertEqual(json.loads(nf[rsa.INBOX])['tasks'], tasks[2:])
        self.assertEqual(next(iter(nf)), rsa.INBOX_ARCHIVE)
        self.assertEqual(f[rsa.INBOX]['tasks'], tasks)  # pure plan, no input mutation

    def test_retry_after_archive_only_write_is_idempotent(self):
        task = self.old()
        f = files(inbox={'tasks': [task]})
        nf, _ = rsa.plan([], f, NOW)
        f[rsa.INBOX_ARCHIVE] = json.loads(nf[rsa.INBOX_ARCHIVE])
        retry, _ = rsa.plan([], f, NOW)
        self.assertNotIn(rsa.INBOX_ARCHIVE, retry)
        self.assertEqual(json.loads(retry[rsa.INBOX])['tasks'], [])
        f[rsa.INBOX] = json.loads(retry[rsa.INBOX])
        self.assertEqual(rsa.plan([], f, NOW)[0], {})

    def test_conflicting_archive_never_removes_live_task(self):
        f = files(inbox={'tasks': [self.old()]})
        f[rsa.INBOX_ARCHIVE] = {'tasks': [self.old(result='different')]}
        original = copy.deepcopy(f)
        with self.assertRaises(ValueError):
            rsa.plan([], f, NOW)
        self.assertEqual(f, original)

    def test_open_supabase_row_and_unknown_date_are_retained(self):
        tasks = [self.old(id='waiting-ack'), self.old(id='undated', closed_at='unknown'),
                 self.old(id='boundary', closed_at=iso(NOW - timedelta(days=14)))]
        f = files(inbox={'tasks': tasks})
        nf, _ = rsa.plan([row('waiting-ack', 'owner_task', status='in_progress', result_note=rsa.INBOX_CLAIM)], f, NOW)
        self.assertNotIn(rsa.INBOX, nf)
        self.assertNotIn(rsa.INBOX_ARCHIVE, nf)

    def test_archive_write_failure_keeps_disk_inbox_and_never_pushes_or_acks(self):
        class Store:
            def list_open(self): return []
            def mark(self, *args): raise AssertionError('must not acknowledge')
        class Git:
            def commit(self, *args): raise AssertionError('must not commit')
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / 'ops').mkdir()
            live = rsa.dumps({'tasks': [self.old()]})
            (root / rsa.INBOX).write_text(live)
            (root / rsa.QUEUE).write_text(rsa.dumps(queue()))
            with patch.object(rsa, 'atomic_json', side_effect=OSError('disk full')):
                with self.assertRaises(OSError):
                    rsa.run(root, Store(), Git(), now=NOW, sync=False)
            self.assertEqual((root / rsa.INBOX).read_text(), live)

    def test_rejected_push_replans_archive_and_keeps_all_records(self):
        class Store:
            def list_open(self): return []
            def mark(self, *args): raise AssertionError('no site rows')
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / 'ops').mkdir()
            tasks = [self.old()]
            (root / rsa.INBOX).write_text(rsa.dumps({'tasks': tasks}))
            (root / rsa.QUEUE).write_text(rsa.dumps(queue()))
            outer = self
            class Git:
                attempts = 0
                def sync(self): pass
                def commit(self, message, paths):
                    outer.assertIn(rsa.INBOX_ARCHIVE, paths)
                    outer.assertIn(rsa.INBOX, paths)
                    return 'candidate'
                def push(self):
                    self.attempts += 1
                    return self.attempts > 1
                def reset(self):
                    # A concurrent writer added a second task; rejected changes are discarded.
                    (root / rsa.INBOX).write_text(rsa.dumps({'tasks': tasks + [outer.old(id='concurrent')]}))
                    (root / rsa.INBOX_ARCHIVE).unlink()
                def head_is_on_remote(self): return True
            self.assertEqual(rsa.run(root, Store(), Git(), now=NOW), 0)
            archived = json.loads((root / rsa.INBOX_ARCHIVE).read_text())['tasks']
            self.assertEqual([t['id'] for t in archived], ['claude-old', 'concurrent'])
            self.assertEqual(json.loads((root / rsa.INBOX).read_text())['tasks'], [])
