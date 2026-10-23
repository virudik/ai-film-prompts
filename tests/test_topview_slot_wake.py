"""Notification wake must never mistake project-local occupancy or a hold for a free slot."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from robot_telemetry import published_event_text, slot_wake_signal, wake_issue_title, wake_issue_body


class WakeTextTests(unittest.TestCase):
    def plan(self, local=5, foreign=0, decision='publish'):
        return {'decision': decision, 'cycle': {'active': [{}] * local, 'checked_at': '2026-10-23T22:00:00Z'},
                'projects': {'active': [{}] * foreign}}

    def event(self, kind='result'):
        return {'kind': kind, 'key': 'result:abc', 'text': 'original result'}

    def test_one_free_slot_has_stable_event_and_observation(self):
        text = published_event_text(self.event(), self.plan())
        for expected in ('@virudik', 'TOPVIEW_SLOT_WAKE_V1', 'event_id: result:abc',
                         'free_slots_global: 1', 'observed_at: 2026-10-23T22:00:00Z'):
            self.assertIn(expected, text)

    def test_full_account_including_other_projects_never_wakes(self):
        for local, foreign in ((6, 0), (5, 1), (0, 6), (5, 2)):
            self.assertEqual(published_event_text(self.event(), self.plan(local, foreign)), 'original result')

    def test_hold_noop_and_other_events_never_wake(self):
        for decision in ('hold', 'noop'):
            self.assertEqual(published_event_text(self.event(), self.plan(decision=decision)), 'original result')
        self.assertEqual(published_event_text(self.event('failure'), self.plan()), 'original result')


    def test_v2_signal_and_new_issue_subject(self):
        sig = slot_wake_signal(self.event(), self.plan(local=3, foreign=1))
        self.assertEqual(sig, {'event_id': 'result:abc', 'observed_at': '2026-10-23T22:00:00Z',
                               'free_slots_global': 2})
        title = wake_issue_title(sig)
        self.assertTrue(title.startswith('TOPVIEW_SLOT_WAKE_V2 '))
        self.assertIn('result:abc', title)
        body = wake_issue_body(sig)
        for expected in ('@virudik', 'TOPVIEW_SLOT_WAKE_V2', 'event_id: result:abc', 'free_slots_global: 2'):
            self.assertIn(expected, body)

    def test_v2_never_signals_without_a_free_slot_or_on_hold(self):
        self.assertIsNone(slot_wake_signal(self.event(), self.plan(5, 1)))
        self.assertIsNone(slot_wake_signal(self.event(), self.plan(decision='hold')))
        self.assertIsNone(slot_wake_signal(self.event('failure'), self.plan()))


if __name__ == '__main__':
    unittest.main()
