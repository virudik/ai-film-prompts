"""Notification wake must never mistake project-local occupancy or a hold for a free slot."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from robot_telemetry import published_event_text


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


if __name__ == '__main__':
    unittest.main()
