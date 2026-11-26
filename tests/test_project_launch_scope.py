"""Stakhiy Wan 3.0 parts in the shared queue (owner t980u, 27.11.2026): own board, 9:16, Unlimited 0, next in order."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import launcher_coordination as lc  # noqa: E402
import queue_readiness as qr  # noqa: E402

BOARD = 'e4156a8c422a4904b88b7bce6018b796'
IDS = [f'1-W{n:02d}-WAN30' for n in range(1, 11)]


class ProjectLaunchScopeTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / 'ops/slot-backup.json').read_text())
        self.queue = json.loads((ROOT / 'ops/topview-launch-queue.json').read_text())

    def test_scope_is_recorded_free_and_board_bound(self):
        scope = self.config['project_launch_scopes']['stikhiy']
        self.assertEqual((scope['enabled'], scope['unlimited_zero_only'], scope['board_id']), (True, True, BOARD))
        self.assertEqual((scope['aspect_ratios'], scope['resolution'], scope['quantity']), (['9:16'], 720, 1))
        self.assertNotEqual(scope['board_id'], self.config['grok_launcher']['board_id'])

    def test_aspect_ratio_open_only_for_scoped_project(self):
        self.assertEqual(lc.allowed_aspect_ratios(self.config, {'id': 'S1'}), ('16:9',))
        self.assertEqual(lc.allowed_aspect_ratios(self.config, {'project': 'seregius'}), ('16:9',))
        self.assertEqual(lc.allowed_aspect_ratios(self.config, {'project': 'stikhiy'}), ('9:16',))
        with self.assertRaisesRegex(lc.Blocked, 'project_launch_scope_not_authorized'):
            lc.allowed_aspect_ratios(self.config, {'project': 'roscosmos'})
        off = json.loads(json.dumps(self.config))
        off['project_launch_scopes']['stikhiy']['unlimited_zero_only'] = False
        with self.assertRaisesRegex(lc.Blocked, 'project_launch_scope_not_authorized'):
            lc.allowed_aspect_ratios(off, {'project': 'stikhiy'})

    def test_shared_queue_items_are_ready_free_and_on_own_board(self):
        items = {i['id']: i for i in self.queue['items'] if i['id'] in IDS}
        self.assertEqual(sorted(items), IDS)
        for item in items.values():
            self.assertEqual((item['project'], item['board_id'], item['aspect_ratio']), ('stikhiy', BOARD, '9:16'))
            self.assertEqual((item['actual_resolution'], item['quantity'], item['max_credits'], item['max_new_submissions']), (720, 1, 0, 1))
            self.assertEqual((item['model'], item['mode'], item['state']), ('Wan 3.0', 'omni_reference', 'waiting_for_slot'))
            for ref in item['references']:
                self.assertTrue(ref['path'].startswith('projects/stikhiy/references/'), ref['path'])
        project_queue = json.loads((ROOT / 'projects/stikhiy/ops/topview-launch-queue.json').read_text())
        self.assertEqual(project_queue['items'], [])

    def test_stakhiy_parts_go_next(self):
        order = qr.t601_order(self.queue)
        self.assertEqual(order[:10], IDS)
        self.assertLess(order.index(IDS[-1]), order.index('S28-A10-20261023'))
        self.assertEqual(len(order), len(set(order)))
        chosen = qr.launch_candidates(ROOT)['chosen']
        self.assertEqual([i for i in chosen if i in IDS], IDS)
        self.assertEqual(chosen[:len(IDS)], IDS)

    def test_board_guard_refuses_shared_or_inherited_board(self):
        from datetime import datetime, timezone
        config = json.loads(json.dumps(self.config))
        config['grok_launcher'].setdefault('first_real_create', {})['owner_go_ahead'] = True
        actor = {'wake_issue': 1, 'submissions_this_wake': 0}
        now = datetime(2026, 11, 27, 12, 0, tzinfo=timezone.utc)
        shared = config['grok_launcher']['board_id']
        for board, queue_board in ((None, shared), ('', shared), (shared, shared), ('other', shared), (None, BOARD)):
            with self.assertRaisesRegex(lc.Blocked, 'grok_board_not_authorized'):
                lc.check_grok_policy(config, {'project': 'stikhiy', 'board_id': board}, actor, now, queue_board_id=queue_board)
        self.assertTrue(lc.check_grok_policy(config, {'project': 'stikhiy', 'board_id': BOARD}, actor, now, queue_board_id=shared))
        with self.assertRaisesRegex(lc.Blocked, 'grok_board_not_authorized'):
            lc.check_grok_policy(config, {'board_id': BOARD}, actor, now, queue_board_id=shared)
        with self.assertRaisesRegex(lc.Blocked, 'project_launch_scope_not_authorized'):
            lc.check_grok_policy(config, {'project': 'raznoe', 'board_id': BOARD}, actor, now, queue_board_id=shared)

if __name__ == '__main__':
    unittest.main()
