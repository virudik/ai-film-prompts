"""Bounded re-wake: a slot that stays free while the queue has actionable items wakes the executor again."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import robot_telemetry as rt            # noqa: E402

NOW = datetime(2026, 10, 26, 10, 0, tzinfo=timezone.utc)


def z(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class FakeGit:
    def __init__(self, push_ok=True):
        self.commits, self.push_ok, self.resets = [], push_ok, 0

    def commit(self, message, paths):
        self.commits.append((message, paths))
        return 'abc'

    def push(self):
        return self.push_ok

    def head_is_on_remote(self):
        return self.push_ok

    def reset(self):
        self.resets += 1


class FakeNotifier:
    def __init__(self):
        self.wakes, self.posts = [], []

    def wake(self, signal):
        self.wakes.append(signal)
        return True

    def post(self, title, text):
        self.posts.append((title, text))
        return True


class RewakeTests(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.root = Path(d.name)
        (self.root / 'ops').mkdir()
        (self.root / 'projects').mkdir()
        self.state(active=5, foreign=0, codes=('ready', 'waiting_result'))
        (self.root / 'automation-monitor-status.json').write_text(json.dumps({'notification_state': {}}))

    def state(self, active, foreign, codes, checked=NOW):
        (self.root / 'topview-status.json').write_text(json.dumps(
            {'checked_at': z(checked), 'occupied_slots': active,
             'active_tasks': [{'task_id': f't{i}'} for i in range(active)]}))
        (self.root / 'projects' / 'topview-projects.json').write_text(json.dumps(
            {'active': [{'task_id': f'f{i}'} for i in range(foreign)]}))
        (self.root / 'ops' / 'queue-readiness.json').write_text(json.dumps(
            {'items': [{'id': f'S{i}', 'code': c} for i, c in enumerate(codes)]}))

    def rw(self):
        return json.loads((self.root / 'automation-monitor-status.json').read_text())['notification_state'].get('robot_rewake')

    def test_free_slot_with_ready_item_wakes_and_then_waits(self):
        g, n = FakeGit(), FakeNotifier()
        self.assertTrue(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.assertEqual(len(g.commits), 1)
        self.assertEqual(n.wakes[0]['free_slots_global'], 1)
        self.assertTrue(n.wakes[0]['event_id'].startswith('slots:') and n.wakes[0]['event_id'].endswith(':1'))
        # 10 minutes later: too soon
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW + timedelta(minutes=10), z(NOW)))
        # 20 minutes later: second re-wake with a new, distinct event id
        later = NOW + timedelta(minutes=20)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, later, z(later)))
        self.assertTrue(n.wakes[1]['event_id'].endswith(':2'))

    def test_bounded_per_unchanged_set_of_active_tasks(self):
        g, n = FakeGit(), FakeNotifier()
        t = NOW
        for _ in range(rt.REWAKE_MAX + 2):
            rt.maybe_rewake(self.root, g, n, t, z(t))
            t += timedelta(minutes=rt.REWAKE_MIN)
        self.assertEqual(len(n.wakes), rt.REWAKE_MAX)
        # the executor launched something, another slot is still free: a new episode may wake again
        self.state(active=4, foreign=1, codes=('ready',))
        self.state(active=5, foreign=0, codes=('ready',))
        (self.root / 'topview-status.json').write_text(json.dumps(
            {'checked_at': z(t), 'occupied_slots': 5, 'active_tasks': [{'task_id': f'n{i}'} for i in range(5)]}))
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertTrue(n.wakes[-1]['event_id'].endswith(':1'))

    def test_no_wake_when_full_nothing_actionable_or_scan_old(self):
        g, n = FakeGit(), FakeNotifier()
        self.state(active=5, foreign=1, codes=('ready',))                    # other project fills the 6th slot
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.state(active=4, foreign=0, codes=('waiting_result', 'owner_hold', 'blocked_owner_decision'))
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.state(active=4, foreign=0, codes=('prepare_continuity',))       # executor can cut the frame now
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW, z(NOW - timedelta(minutes=30))))
        self.assertTrue(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.assertEqual((len(g.commits), len(n.wakes)), (1, 1))

    def test_recent_result_wake_postpones_the_re_wake(self):
        g, n = FakeGit(), FakeNotifier()
        rt.note_wake(self.root, rt.slot_state(self.root)['episode'], NOW)          # publish sent a result wake
        self.assertEqual(self.rw()['count'], 0)
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW + timedelta(minutes=10), z(NOW)))
        t = NOW + timedelta(minutes=rt.REWAKE_MIN)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))

    def test_rejected_push_sends_nothing(self):
        g, n = FakeGit(push_ok=False), FakeNotifier()
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.assertEqual((n.wakes, g.resets), ([], 1))

    def test_unanswered_signal_is_reported_once(self):
        g, n = FakeGit(), FakeNotifier()
        (self.root / 'reports').mkdir()
        (self.root / 'reports' / 'topview-event-wake.json').write_text('{"events": []}')
        rt.note_wake(self.root, rt.slot_state(self.root)['episode'], NOW, event_id='result:abc')
        t = NOW + timedelta(minutes=rt.REWAKE_MIN)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(len(n.posts), 1)
        self.assertIn('result:abc', n.posts[0][1])
        # the handler answered the re-wake: no further report
        (self.root / 'reports' / 'topview-event-wake.json').write_text(
            json.dumps({'events': [{'event_id': n.wakes[0]['event_id']}]}))
        t += timedelta(minutes=rt.REWAKE_MIN)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(len(n.posts), 1)

    def test_answered_signal_is_not_reported(self):
        g, n = FakeGit(), FakeNotifier()
        (self.root / 'reports').mkdir()
        (self.root / 'reports' / 'topview-event-wake.json').write_text('{"events": [{"event_id": "result:abc"}]}')
        rt.note_wake(self.root, rt.slot_state(self.root)['episode'], NOW, event_id='result:abc')
        t = NOW + timedelta(minutes=rt.REWAKE_MIN)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(n.posts, [])

    def test_archived_answer_is_not_reported_as_silence(self):
        g, n = FakeGit(), FakeNotifier()
        (self.root / 'reports').mkdir()
        (self.root / 'reports' / 'topview-event-wake.json').write_text(
            json.dumps({'events': [], 'archived_event_ids': ['slots:older:1']}))
        rt.note_wake(self.root, rt.slot_state(self.root)['episode'], NOW, event_id='slots:older:1')
        t = NOW + timedelta(minutes=rt.REWAKE_MIN)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(n.posts, [])


if __name__ == '__main__':
    unittest.main()
