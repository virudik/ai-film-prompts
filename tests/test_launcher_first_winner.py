"""No network / Create. Simulate first main-head CAS winner and stale loser."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from datetime import timedelta
import test_launcher_coordination as fixtures
from test_launcher_coordination import NOW, B
import launcher_coordination as lc

class FirstWinnerTests(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.CoordinationTests(); fixture.setUp()
        self.cfg, self.actor, self.lock = fixture.cfg, fixture.actor, fixture.lock
        self.preflight = fixture.item['claim']['preflight']
        self.item = {'id': 'S-example', 'state': 'waiting_for_slot'}
        self.scan = dict(fixture.scan, item_reconciliation={'S-example': {
            'complete': True, 'matched_task_ids': [], 'ambiguous': False}})
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); (self.root/'ops').mkdir()
        (self.root/lc.QUEUE).write_text(json.dumps({'items':[self.item]}))
        self.selector = patch.object(lc.queue_readiness, 'launch_candidates', return_value={'chosen':['S-example']})
        self.selector.start(); self.addCleanup(self.selector.stop)
    def claim(self, **changes):
        args=dict(config=self.cfg, lock=self.lock, item=self.item, actor=self.actor,
                  scan=self.scan, now=NOW, preflight=self.preflight, source_sha='a'*40, root=self.root)
        args.update(changes); return lc.prepare_claim(**args)
    def intent(self):
        item=lc.prepare_intent(self.cfg,self.lock,self.claim(),self.actor,self.scan,NOW)
        (self.root/lc.QUEUE).write_text(json.dumps({'items':[item]}))
        return item
    def verify(self, item, **changes):
        args=dict(config=self.cfg,lock=self.lock,item=item,actor=self.actor,scan=self.scan,now=NOW,
                  expected_claim_id=item['claim']['claim_id'],expected_intent_id=item['claim']['submission_intent_id'],root=self.root,
                  expected_payload_sha=item['claim']['intent_payload_sha256'])
        args.update(changes);return lc.verify_before_create(**args)
    def test_first_cas_winner_other_execution_cannot_claim(self):
        winner=self.claim()
        other=dict(self.actor,execution_instance_id=B)
        with self.assertRaises(lc.Blocked): self.claim(actor=other)
        with self.assertRaises(lc.Blocked): self.claim(item=winner)
    def test_two_stale_main_snapshots_only_one_cas_wins(self):
        # The GitHub API expected_sha is the actual atomic arbiter. This model
        # checks callers never treat an unpublished locally prepared claim as owned.
        head = 'a' * 40
        snapshots = [head, head]
        winners = []
        for candidate, expected in enumerate(snapshots):
            if expected == head:
                winners.append(candidate)
                head = 'b' * 40
        self.assertEqual(winners, [0])
        # After winner publishes, even a backup with a NEW valid global lease
        # cannot reclaim the same item (including after TTL).
        claimed = self.claim()
        actor = dict(self.actor, execution_instance_id=B)
        lock = dict(self.lock, holder=lc.holder(actor))
        with self.assertRaises(lc.Blocked):self.claim(item=claimed, actor=actor, lock=lock)

    def test_durable_intent_and_exact_readback(self):
        item=self.intent(); self.assertTrue(self.verify(item))
        with self.assertRaises(lc.Blocked):self.verify(item,expected_intent_id='different')
    def test_changed_payload_with_same_ids_is_not_authorized(self):
        item=self.intent()
        for key,value in [('credits_cost',18),('input_sha_match',False),('owner_authorized',False)]:
            changed=copy.deepcopy(item);changed['claim']['preflight'][key]=value
            with self.assertRaises(lc.Blocked):self.verify(changed)
        changed=copy.deepcopy(item);changed['prompt']='changed prompt'
        with self.assertRaises(lc.Blocked):self.verify(changed)

    def test_expired_lease_never_grants_backup_create(self):
        item=self.intent()
        with self.assertRaises(lc.Blocked):self.verify(item,now=NOW+timedelta(minutes=6))
    def test_same_execution_reacquired_lease_does_not_resurrect_claim(self):
        item=self.claim();lock=dict(self.lock,acquired_at=lc.stamp(NOW))
        actor=dict(self.actor,lease_acquired_at=lock['acquired_at'])
        with self.assertRaises(lc.Blocked):lc.prepare_intent(self.cfg,lock,item,actor,self.scan,NOW)
    def test_unknown_and_submitted_never_reclaimed(self):
        for state in ['claimed','submitting','submission_unknown','submitted','completed']:
            with self.subTest(state=state),self.assertRaises(lc.Blocked):self.claim(item=dict(self.item,state=state))
    def test_duplicate_or_ambiguous_live_task_blocks(self):
        item=self.intent()
        for row in [{}, {'complete':True,'matched_task_ids':['task'],'ambiguous':False},
                    {'complete':True,'matched_task_ids':[],'ambiguous':True}]:
            scan=dict(self.scan,item_reconciliation={'S-example':row})
            with self.assertRaises(lc.Blocked):self.verify(item,scan=scan)
        (self.root/lc.QUEUE).write_text(json.dumps({'items':[self.item]}))
        with self.assertRaises(lc.Blocked):self.claim(scan=dict(self.scan,item_reconciliation={}))
    def test_stale_intent_and_changed_role_block(self):
        item=self.intent()
        with self.assertRaises(lc.Blocked):self.verify(item,now=NOW+timedelta(seconds=121))
        with self.assertRaises(lc.Blocked):self.verify(item,config=dict(self.cfg,route_generation=3))
    def test_final_readback_must_match_disk_and_original_payload(self):
        item=self.intent()
        with self.assertRaises(lc.Blocked):self.verify(item,expected_payload_sha='0'*64)
        (self.root/lc.QUEUE).write_text(json.dumps({'items':[self.item]}))
        with self.assertRaises(lc.Blocked):self.verify(item)

    def test_queue_order_and_snapshot_required(self):
        with patch.object(lc.queue_readiness,'launch_candidates',return_value={'chosen':['another']}):
            with self.assertRaises(lc.Blocked):self.claim()
        with self.assertRaises(lc.Blocked):self.claim(item=dict(self.item,priority=1))
    def test_paid_preflight_denied(self):
        with self.assertRaises(lc.Blocked):self.claim(preflight=dict(self.preflight,credits_cost=18))

if __name__ == '__main__':unittest.main()
