"""Persistent, paced recovery of free capacity; processing ACK is distinct from a verified launch."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

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

    def health(self):
        return json.loads((self.root / 'automation-monitor-status.json').read_text())['launcher_health']

    def receipts(self, events, archived=()):
        (self.root / 'reports').mkdir(exist_ok=True)
        (self.root / 'reports' / 'topview-event-wake.json').write_text(json.dumps(
            {'events': [dict(checked_at=z(NOW), **e) if 'checked_at' not in e else e for e in events],
             'archived_event_ids': list(archived)}))

    def queue(self, items):
        p = self.root / 'ops/topview-launch-queue.json'
        p.write_text(json.dumps({'items': items}))
        return p

    def test_free_slot_with_ready_item_wakes_and_then_waits(self):
        g, n = FakeGit(), FakeNotifier()
        self.assertTrue(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.assertEqual(len(g.commits), 1)
        self.assertEqual(n.wakes[0]['free_slots_global'], 1)
        self.assertTrue(n.wakes[0]['event_id'].startswith('slots:') and n.wakes[0]['event_id'].endswith(':4'))
        # 10 minutes later: too soon
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW + timedelta(minutes=10), z(NOW)))
        # 20 minutes later: second re-wake with a new, distinct event id
        later = NOW + timedelta(minutes=20)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, later, z(later)))
        self.assertTrue(n.wakes[1]['event_id'].endswith(':5'))

    def test_three_fast_attempts_then_hourly_recovery_for_unchanged_tasks(self):
        g, n = FakeGit(), FakeNotifier()
        t = NOW
        for _ in range(rt.REWAKE_MAX + 2):
            rt.maybe_rewake(self.root, g, n, t, z(t))
            t += timedelta(minutes=rt.REWAKE_MIN)
        self.assertEqual(len(n.wakes), rt.REWAKE_MAX)
        # The absolute cap caused the 31-Oct gap. At 60 minutes after attempt 3, attempt 4 must run.
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(len(n.wakes), 4)
        self.assertTrue(n.wakes[-1]['event_id'].endswith(':7'))
        self.assertEqual(n.wakes[-1]['attempt_interval_min'], 60)
        t += timedelta(minutes=20)
        # the executor launched something, another slot is still free: a new episode may wake again
        self.state(active=4, foreign=1, codes=('ready',))
        self.state(active=5, foreign=0, codes=('ready',))
        (self.root / 'topview-status.json').write_text(json.dumps(
            {'checked_at': z(t), 'occupied_slots': 5, 'active_tasks': [{'task_id': f'n{i}'} for i in range(5)]}))
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(self.rw()['count'], 1)
        self.assertTrue(n.wakes[-1]['event_id'].endswith(':8'))

    def test_monotonic_sequence_survives_result_wakes_episode_return_and_archived_ids(self):
        g, n = FakeGit(), FakeNotifier()
        episode_a = rt.slot_state(self.root)['episode']
        self.receipts([], archived=[f'slots:{episode_a}:{i}' for i in range(1, 4)])
        self.assertTrue(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        first = n.wakes[-1]['event_id']
        self.assertEqual(first, f'slots:{episode_a}:4')
        self.receipts([], archived=[f'slots:{episode_a}:{i}' for i in range(1, 5)])
        self.state(active=4, foreign=1, codes=('ready',))
        episode_b = rt.slot_state(self.root)['episode']
        t = NOW + timedelta(minutes=20)
        rt.note_wake(self.root, episode_b, t, event_id='result:completed-a')
        self.assertEqual((self.rw()['count'], self.rw()['sequence']), (0, 4))
        t += timedelta(minutes=20)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(n.wakes[-1]['event_id'], f'slots:{episode_b}:5')
        self.state(active=5, foreign=0, codes=('ready',))
        t += timedelta(minutes=20)
        rt.note_wake(self.root, episode_a, t, event_id='result:completed-b')
        self.assertEqual((self.rw()['count'], self.rw()['sequence']), (0, 5))
        t += timedelta(minutes=20)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(n.wakes[-1]['event_id'], f'slots:{episode_a}:6')
        self.assertEqual((self.rw()['count'], self.rw()['sequence']), (1, 6))
        self.assertEqual(len({w['event_id'] for w in n.wakes}), 3)
        self.assertTrue(rt.handler_acked(self.root, first))
        self.assertFalse(rt.handler_acked(self.root, n.wakes[-1]['event_id']))

    def test_sequence_migration_cannot_go_below_legacy_count(self):
        episode = rt.slot_state(self.root)['episode']
        (self.root / 'automation-monitor-status.json').write_text(json.dumps({'notification_state': {
            'robot_rewake': {'episode': episode, 'count': 7, 'last_at': z(NOW),
                             'last_event_id': f'slots:{episode}:7'}}}))
        t = NOW + timedelta(minutes=60)
        g, n = FakeGit(), FakeNotifier()
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual((self.rw()['count'], self.rw()['sequence']), (8, 8))
        self.assertEqual(n.wakes[-1]['event_id'], f'slots:{episode}:8')

    def test_receipt_order_uses_latest_valid_timestamp_not_array_order(self):
        old = {'event_id': 'result:abc', 'outcome': 'started', 'checked_at': z(NOW)}
        new = {'event_id': 'result:abc', 'outcome': 'blocked_browser', 'checked_at': z(NOW),
               'updated_at': z(NOW + timedelta(minutes=5))}
        newer = {'event_id': 'result:abc', 'outcome': 'submission_unknown', 'checked_at': z(NOW),
                 'execution': {'updated_at': z(NOW + timedelta(minutes=7))}}
        t = NOW + timedelta(minutes=10)
        for events in ([old, new], [new, old]):
            self.receipts(events)
            self.assertEqual(rt.handler_receipt(self.root, 'result:abc', t), new)
        for events in ([old, new, newer], [newer, new, old]):
            self.receipts(events)
            self.assertEqual(rt.handler_receipt(self.root, 'result:abc', t), newer)

    def test_receipts_with_future_or_ambiguous_time_cannot_prove_a_launch(self):
        valid = {'event_id': 'result:abc', 'outcome': 'started', 'checked_at': z(NOW)}
        future = {'event_id': 'result:abc', 'outcome': 'submitted', 'checked_at': z(NOW),
                  'updated_at': z(NOW + timedelta(minutes=30)), 'task_ids': ['a' * 32], 'retryable': False}
        t = NOW + timedelta(minutes=10)
        self.receipts([valid, future])
        self.assertEqual(rt.handler_receipt(self.root, 'result:abc', t), valid)
        self.receipts([future, {'event_id': 'result:abc', 'checked_at': 'invalid', 'outcome': 'submitted'}])
        self.assertEqual(rt.handler_receipt(self.root, 'result:abc', t), {'event_id': 'result:abc'})
        self.assertTrue(rt.handler_acked(self.root, 'result:abc'))  # registered receipt, no reliable outcome
        conflicting = dict(valid, outcome='submitted', task_ids=['a' * 32], retryable=False)
        for events in ([valid, conflicting], [conflicting, valid]):
            self.receipts(events)
            self.assertEqual(rt.handler_receipt(self.root, 'result:abc', t), {'event_id': 'result:abc'})

    def test_superseded_wake_issue_is_not_marked_as_completed_handling(self):
        calls = []

        def gh(args, **_kwargs):
            calls.append(args)
            stdout = ''
            if 'repos/{owner}/{repo}/issues' in args:
                stdout = '199\n200\n' if 'GET' in args else '200\nhttps://github.com/virudik/ai-film-prompts/issues/200\n'
            return rt.subprocess.CompletedProcess(args, 0, stdout=stdout, stderr='')

        signal = {'event_id': 'slots:example:4', 'observed_at': z(NOW), 'free_slots_global': 1}
        with patch.object(rt.subprocess, 'run', side_effect=gh), \
                patch.object(rt.relay_wake, 'send_dm', return_value=('sent', 'message_id=123')):
            self.assertTrue(rt.GhNotifier().wake(signal))
        closed = [args for args in calls if 'state=closed' in args]
        self.assertEqual(len(closed), 1)
        self.assertIn('repos/{owner}/{repo}/issues/199', closed[0])
        self.assertIn('state_reason=not_planned', closed[0])
        self.assertNotIn('state_reason=completed', closed[0])

    def test_no_wake_when_full_nothing_actionable_or_scan_old(self):
        g, n = FakeGit(), FakeNotifier()
        self.state(active=5, foreign=1, codes=('ready',))                    # other project fills the 6th slot
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.state(active=4, foreign=0, codes=('waiting_result', 'owner_hold', 'blocked_owner_decision'))
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.state(active=4, foreign=0, codes=('prepare_continuity',))       # executor can cut the frame now
        self.assertFalse(rt.maybe_rewake(self.root, g, n, NOW, z(NOW - timedelta(minutes=30))))
        self.assertTrue(rt.maybe_rewake(self.root, g, n, NOW, z(NOW)))
        self.assertEqual(len(n.wakes), 1)
        self.assertTrue(all(paths == ['automation-monitor-status.json'] for _, paths in g.commits))

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

    def test_processing_ack_without_launch_does_not_make_executor_healthy(self):
        g, n = FakeGit(), FakeNotifier()
        (self.root / 'reports').mkdir()
        (self.root / 'reports' / 'topview-event-wake.json').write_text('{"events": [{"event_id": "result:abc"}]}')
        rt.note_wake(self.root, rt.slot_state(self.root)['episode'], NOW, event_id='result:abc')
        t = NOW + timedelta(minutes=rt.REWAKE_MIN)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(self.health()['state'], 'launch_stalled')
        self.assertTrue(self.health()['receipt_present'])
        self.assertEqual(self.health()['confirmed_launch_task_ids'], [])
        self.assertEqual(len(n.posts), 1)
        self.assertNotIn('no_handler_receipt', n.posts[0][1])

    def test_archived_answer_is_not_reported_as_silence(self):
        g, n = FakeGit(), FakeNotifier()
        (self.root / 'reports').mkdir()
        (self.root / 'reports' / 'topview-event-wake.json').write_text(
            json.dumps({'events': [], 'archived_event_ids': ['slots:older:1']}))
        rt.note_wake(self.root, rt.slot_state(self.root)['episode'], NOW, event_id='slots:older:1')
        t = NOW + timedelta(minutes=rt.REWAKE_MIN)
        self.assertTrue(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertTrue(self.health()['receipt_present'])
        self.assertEqual(self.health()['handler_outcome'], 'archived_processed')
        self.assertEqual(self.health()['confirmed_launch_task_ids'], [])
        self.assertNotIn('no_handler_receipt', n.posts[0][1])

    def test_last_fast_attempt_is_checked_before_next_hourly_attempt_is_due(self):
        # Migration from the real saved old schema, whose count=3 formerly stopped every code path.
        episode = rt.slot_state(self.root)['episode']
        data = {'health': 'ok', 'notification_state': {'robot_rewake': {
            'episode': episode, 'count': 3, 'last_at': z(NOW),
            'last_event_id': f'slots:{episode}:3', 'silence_reported': f'slots:{episode}:2'}}}
        (self.root / 'automation-monitor-status.json').write_text(json.dumps(data))
        g, n = FakeGit(), FakeNotifier()
        t = NOW + timedelta(minutes=20)
        self.assertFalse(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(n.wakes, [])
        self.assertEqual(self.health()['state'], 'launch_stalled')
        self.assertEqual(self.health()['last_event_id'], f'slots:{episode}:3')
        self.assertEqual(self.health()['unresolved_since'], z(NOW))  # no invented earlier start
        self.assertEqual(len(n.posts), 1)
        self.assertEqual(json.loads((self.root / 'automation-monitor-status.json').read_text())['health'], 'ok')
        for mins in (30, 40, 50, 60, 70, 120):
            t = NOW + timedelta(minutes=mins)
            rt.maybe_rewake(self.root, g, n, t, z(t))
        self.assertEqual(len(n.posts), 1)  # episode escalation is deduplicated independently of DM attempts
        self.assertEqual([w['event_id'] for w in n.wakes], [f'slots:{episode}:4', f'slots:{episode}:5'])

    def test_no_update_blocked_and_started_receipts_remain_unresolved(self):
        for outcome, retryable in [('no_update', False), ('blocked_browser', True), ('started', True)]:
            with self.subTest(outcome=outcome):
                (self.root / 'automation-monitor-status.json').write_text('{"notification_state": {}}')
                rt.note_wake(self.root, rt.slot_state(self.root)['episode'], NOW, event_id='result:abc')
                self.receipts([{'event_id': 'result:abc', 'outcome': outcome, 'retryable': retryable,
                                'task_ids': [], 'run_id': None,
                                'execution': {'stage': 'browser_preflight', 'updated_at': z(NOW)}}])
                g, n = FakeGit(), FakeNotifier()
                for mins in (20, 40, 60, 80, 120):
                    t = NOW + timedelta(minutes=mins)
                    rt.maybe_rewake(self.root, g, n, t, z(t))
                self.assertEqual(len(n.wakes), 4)
                self.assertEqual(len(n.posts), 1)
                self.assertTrue(self.health()['unresolved'])
                self.assertIsNone(self.health()['runtime_run_id'])

    def test_healthy_handler_launch_is_confirmed_by_queue_and_fresh_scan(self):
        g, n = FakeGit(), FakeNotifier()
        rt.maybe_rewake(self.root, g, n, NOW, z(NOW))
        t = NOW + timedelta(minutes=20)
        rt.maybe_rewake(self.root, g, n, t, z(t))
        self.assertTrue(self.health()['unresolved'])
        task = 'a' * 32
        self.receipts([{'event_id': n.wakes[-1]['event_id'], 'outcome': 'submitted',
                        'task_ids': [task], 'retryable': False}])
        self.queue([{'id': 'S0', 'state': 'submitted', 'task_id': task}])
        # Receipt alone, or receipt + queue alone, is not fresh task evidence.
        t += timedelta(minutes=10)
        rt.maybe_rewake(self.root, g, n, t, z(t))
        self.assertTrue(self.health()['unresolved'])
        ts = json.loads((self.root / 'topview-status.json').read_text())
        ts['active_tasks'].append({'task_id': task})
        ts['occupied_slots'] = 6
        (self.root / 'topview-status.json').write_text(json.dumps(ts))
        t += timedelta(minutes=10)
        self.assertFalse(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(self.health()['state'], 'launch_confirmed')
        self.assertFalse(self.health()['unresolved'])
        self.assertEqual(self.health()['confirmed_launch_task_ids'], [task])
        self.assertEqual(len(n.wakes), 2)

    def test_full_capacity_clears_demand_but_does_not_claim_handler_recovery(self):
        g, n = FakeGit(), FakeNotifier()
        rt.maybe_rewake(self.root, g, n, NOW, z(NOW))
        t = NOW + timedelta(minutes=20)
        rt.maybe_rewake(self.root, g, n, t, z(t))
        self.state(active=5, foreign=1, codes=('ready',), checked=t)
        self.assertFalse(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual(self.health()['state'], 'capacity_full')
        self.assertFalse(self.health()['unresolved'])
        self.assertEqual(self.health()['confirmed_launch_task_ids'], [])

    def test_newly_actionable_work_gets_grace_without_repeating_episode_escalation(self):
        g, n = FakeGit(), FakeNotifier()
        rt.maybe_rewake(self.root, g, n, NOW, z(NOW))
        t = NOW + timedelta(minutes=20)
        rt.maybe_rewake(self.root, g, n, t, z(t))
        self.assertEqual(len(n.posts), 1)
        self.state(active=5, foreign=0, codes=('owner_hold',), checked=t)
        t += timedelta(minutes=10)
        rt.maybe_rewake(self.root, g, n, t, z(t))
        self.assertEqual(self.health()['state'], 'no_actionable_work')
        self.state(active=5, foreign=0, codes=('ready',), checked=t)
        t += timedelta(minutes=10)
        rt.maybe_rewake(self.root, g, n, t, z(t))
        self.assertEqual(self.health()['state'], 'awaiting_execution')
        self.assertEqual(self.health()['unresolved_since'], z(t))
        t += timedelta(minutes=20)
        rt.maybe_rewake(self.root, g, n, t, z(t))
        self.assertEqual(self.health()['state'], 'launch_stalled')
        self.assertEqual(len(n.posts), 1)

    def test_stale_or_future_scan_neither_wakes_nor_clears_incident(self):
        g, n = FakeGit(), FakeNotifier()
        rt.maybe_rewake(self.root, g, n, NOW, z(NOW))
        t = NOW + timedelta(minutes=20)
        rt.maybe_rewake(self.root, g, n, t, z(t))
        self.state(active=6, foreign=0, codes=('ready',), checked=NOW)
        t += timedelta(minutes=30)
        self.assertFalse(rt.maybe_rewake(self.root, g, n, t, z(NOW)))
        self.assertEqual(self.health()['state'], 'observation_stale')
        self.assertTrue(self.health()['unresolved'])
        self.assertEqual(self.health()['unresolved_since'], z(NOW))
        self.assertFalse(rt.maybe_rewake(self.root, g, n, t, z(t + timedelta(minutes=1))))
        self.assertTrue(self.health()['unresolved'])

    def test_reservations_and_unknown_create_are_reconciled_never_reset_or_repeated(self):
        for state in ('claimed', 'submitting', 'submission_unknown'):
            with self.subTest(state=state):
                (self.root / 'automation-monitor-status.json').write_text('{"notification_state": {}}')
                p = self.queue([{'id': 'S0', 'state': state,
                                 'claim': {'run_id': 'saved-claim', 'expires_at': '2020-01-01T00:00:00Z'}}])
                before = p.read_bytes()
                lock = self.root / 'ops/canon-lock.json'
                lock.write_text('{"holder": "another-worker", "expires_at": "2020-01-01T00:00:00Z"}')
                lock_before = lock.read_bytes()
                g, n = FakeGit(), FakeNotifier()
                for mins in (0, 20, 40, 100, 160):
                    t = NOW + timedelta(minutes=mins)
                    rt.maybe_rewake(self.root, g, n, t, z(t))
                self.assertEqual(p.read_bytes(), before)
                self.assertEqual(lock.read_bytes(), lock_before)
                self.assertEqual(self.health()['state'], 'reconciliation_required')
                self.assertEqual(self.health()['actionable_items'], [])
                self.assertEqual(len(n.wakes), 5)
                self.assertTrue(all(w['ready'] == 0 and w['reconcile'] == ['S0'] for w in n.wakes))
                self.assertTrue(all(paths == ['automation-monitor-status.json'] for _, paths in g.commits))

    def test_diagnostic_push_failure_sends_no_wake_or_escalation(self):
        rt.note_wake(self.root, rt.slot_state(self.root)['episode'], NOW, event_id='result:abc')
        g, n = FakeGit(push_ok=False), FakeNotifier()
        t = NOW + timedelta(minutes=20)
        self.assertFalse(rt.maybe_rewake(self.root, g, n, t, z(t)))
        self.assertEqual((n.wakes, n.posts, g.resets), ([], [], 1))

    def test_31_october_history_keeps_recovery_alive_until_manual_slot_fill(self):
        f = json.loads((Path(__file__).parent / 'fixtures/topview-wake-gap-20261031.json').read_text())
        start = rt.parse_ts(f['result_observed_at'])
        ts = {'checked_at': z(start), 'occupied_slots': 5,
              'active_tasks': [{'task_id': tid} for tid in f['active_task_ids_during_gap']]}
        (self.root / 'topview-status.json').write_text(json.dumps(ts))
        episode = rt.slot_state(self.root)['episode']
        self.assertEqual(episode, f['episode'])
        self.assertEqual((rt.parse_ts(f['manual_launch_at']) - rt.parse_ts(f['source_task_completed_at'])).total_seconds(),
                         f['idle_seconds'])
        (self.root / 'automation-monitor-status.json').write_text(json.dumps(
            {'notification_state': {'robot_rewake': f['persisted_rewake_state']}}))
        self.receipts([])
        g, n = FakeGit(), FakeNotifier()
        diagnostic = f['counterfactual_diagnostic_check']
        self.assertFalse(rt.maybe_rewake(self.root, g, n, rt.parse_ts(diagnostic), diagnostic))
        self.assertEqual(self.health()['state'], 'launch_stalled')
        for stamp in f['counterfactual_hourly_checks']:
            t = rt.parse_ts(stamp)
            self.assertTrue(rt.maybe_rewake(self.root, g, n, t, stamp))
        self.assertEqual([w['event_id'] for w in n.wakes], [f'slots:{episode}:{i}' for i in range(4, 8)])
        self.assertEqual(len(n.posts), 1)
        self.assertTrue(self.health()['unresolved'])
        ts['active_tasks'].append({'task_id': f['manual_launch_task_id']})
        ts['occupied_slots'] = 6
        ts['checked_at'] = f['postscan_at']
        (self.root / 'topview-status.json').write_text(json.dumps(ts))
        self.assertFalse(rt.maybe_rewake(self.root, g, n, rt.parse_ts(f['postscan_at']), f['postscan_at']))
        self.assertEqual(self.health()['state'], 'capacity_full')
        self.assertEqual(self.health()['confirmed_launch_task_ids'], [])  # do not credit manual S72 to handler


if __name__ == '__main__':
    unittest.main()
