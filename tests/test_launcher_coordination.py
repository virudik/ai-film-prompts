import copy
import sys
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import launcher_coordination as lc

NOW = datetime(2026, 10, 31, 17, tzinfo=timezone.utc)
A = '11111111-1111-4111-8111-111111111111'
B = '22222222-2222-4222-8222-222222222222'

class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {'enabled': True, 'route_generation': 2, 'preferred_executor': 'ordinary',
                    'peers': {'ordinary': {'enabled': True, 'automation_ids': ['ordinary-task']},
                              'work': {'enabled': True, 'automation_ids': ['work-task']}},
                    'work_capacity': {'state': 'exhausted', 'reported_at': lc.stamp(NOW-timedelta(hours=1))},
                    'foreground_owners': {'ordinary': {'session_id': 'old', 'epoch': 1}}}
        self.actor = {'execution_instance_id': A, 'surface': 'ordinary', 'kind': 'scheduled',
                      'automation_id': 'ordinary-task', 'route_generation': 2,
                      'lease_acquired_at': lc.stamp(NOW-timedelta(minutes=1))}
        self.lock = {'state': 'held', 'holder': lc.holder(self.actor), 'acquired_at': self.actor['lease_acquired_at'],
                     'expires_at': lc.stamp(NOW+timedelta(minutes=5))}
        self.scan = {'complete': True, 'checked_at': lc.stamp(NOW), 'free_slots': 1}
        p = dict.fromkeys(('owner_authorized','prompt_match','input_sha_match','input_order_match','qc_passed','website_unlimited'), True)
        p.update(credits_cost=0, quantity=1, resolution=720, aspect_ratio='16:9')
        self.item = {'id': 'S-example', 'state': 'claimed', 'claim': {'claim_id': 'unique-claim',
                     'execution_instance_id': A, 'route_generation': 2, 'preflight': p}}
    def test_both_peers_run_independently(self):
        self.assertTrue(lc.check_route(self.cfg, self.actor))
        actor = dict(self.actor, surface='work', automation_id='work-task', execution_instance_id=B)
        self.assertTrue(lc.check_route(self.cfg, actor))
    def test_preference_does_not_disable_other_peer(self):
        self.cfg['preferred_executor'] = 'work'
        self.assertTrue(lc.check_route(self.cfg, self.actor))
    def test_other_execution_cannot_use_same_surface_lease(self):
        with self.assertRaises(lc.Blocked): lc.check_lease(self.lock, dict(self.actor, execution_instance_id=B), NOW)
    def test_generic_chatgpt_is_not_own_lease(self):
        self.lock['holder'] = 'chatgpt'
        with self.assertRaises(lc.Blocked): lc.check_lease(self.lock, self.actor, NOW)
    def test_expiry_never_grants_write(self):
        self.lock['expires_at'] = lc.stamp(NOW)
        with self.assertRaises(lc.Blocked): lc.prepare_intent(self.cfg,self.lock,self.item,self.actor,self.scan,NOW)
    def test_replaced_lease_not_released_even_if_expired(self):
        self.lock.update(holder='chatgpt:ordinary:'+B, expires_at=lc.stamp(NOW-timedelta(minutes=1)))
        with self.assertRaises(lc.Blocked): lc.release_exact(self.lock, self.actor, NOW)
    def test_single_durable_intent_not_replayed(self):
        out = lc.prepare_intent(self.cfg,self.lock,self.item,self.actor,self.scan,NOW)
        self.assertEqual(out['state'],'submitting')
        self.assertEqual(self.item['state'],'claimed')
        with self.assertRaises(lc.Blocked): lc.prepare_intent(self.cfg,self.lock,out,self.actor,self.scan,NOW)
    def test_existing_and_unknown_tasks_never_repeated(self):
        for state in ('submitted','completed','submission_unknown','submitting','waiting_for_slot'):
            with self.subTest(state=state), self.assertRaises(lc.Blocked):
                lc.prepare_intent(self.cfg,self.lock,dict(self.item,state=state),self.actor,self.scan,NOW)
    def test_other_claim_denied(self):
        self.item['claim']['execution_instance_id']=B
        with self.assertRaises(lc.Blocked): lc.prepare_intent(self.cfg,self.lock,self.item,self.actor,self.scan,NOW)
    def test_stale_route_denied(self):
        with self.assertRaises(lc.Blocked): lc.check_route(self.cfg,dict(self.actor,route_generation=1))
    def test_full_partial_old_future_scan_denied(self):
        for scan in (dict(self.scan,free_slots=0),dict(self.scan,complete=False),
                     dict(self.scan,checked_at=lc.stamp(NOW-timedelta(minutes=3))),
                     dict(self.scan,checked_at=lc.stamp(NOW+timedelta(seconds=1)))):
            with self.subTest(scan=scan), self.assertRaises(lc.Blocked):
                lc.prepare_intent(self.cfg,self.lock,self.item,self.actor,scan,NOW)
    def test_paid_or_unchecked_inputs_denied(self):
        for key,value in (('credits_cost',1),('input_sha_match',False),('quantity',2),('resolution',1080)):
            item=copy.deepcopy(self.item); item['claim']['preflight'][key]=value
            with self.subTest(key=key), self.assertRaises(lc.Blocked):
                lc.prepare_intent(self.cfg,self.lock,item,self.actor,self.scan,NOW)
    def test_continue_retires_old_foreground_not_schedules(self):
        actor=dict(self.actor,kind='interactive',session_id='new')
        out=lc.takeover(self.cfg,self.lock,actor,NOW,'Продолжай')
        self.assertEqual(out['foreground_owners']['ordinary']['epoch'],2)
        self.assertEqual(out['peers'],self.cfg['peers'])
        self.assertEqual(out['route_generation'],2)
        with self.assertRaises(lc.Blocked): lc.check_route(out,dict(actor,session_id='old',foreground_epoch=1))
        self.assertTrue(lc.check_route(out,dict(actor,foreground_epoch=2)))
        self.assertTrue(lc.check_route(out,self.actor))
        self.assertEqual(lc.takeover(out,self.lock,actor,NOW,'Продолжай'),out)
    def test_takeover_does_not_steal_other_lock(self):
        with self.assertRaises(lc.Blocked):
            lc.takeover(self.cfg,self.lock,dict(self.actor,kind='interactive',session_id='new',execution_instance_id=B),NOW,'Продолжай')
    def test_no_recovery_from_enabled_no_update_or_old_success(self):
        for evidence in ({'checked_at':lc.stamp(NOW),'source':'enabled'},
                         {'checked_at':lc.stamp(NOW),'source':'verified_work_runtime','recorded_status':'no_update'},
                         {'checked_at':lc.stamp(NOW-timedelta(days=1)),'source':'direct_owner_confirmation','reference':'owner'}):
            with self.subTest(evidence=evidence), self.assertRaises(lc.Blocked):
                lc.restore_work_preference(self.cfg,evidence,NOW)
    def test_verified_work_recovery_changes_preference_not_peer_authority(self):
        evidence={'checked_at':lc.stamp(NOW),'source':'verified_work_runtime','surface':'work','run_id':'real-runtime-id',
                  'recorded_status':'completed','browser_controls_verified':True,'quota_available_verified':True,'reference':'actual receipt'}
        out=lc.restore_work_preference(self.cfg,evidence,NOW)
        self.assertEqual(out['preferred_executor'],'work')
        self.assertEqual(out['route_generation'],3)
        self.assertEqual(out['peers'],self.cfg['peers'])
    def test_no_quota_independence_inferred(self):
        evidence={'checked_at':lc.stamp(NOW),'source':'verified_work_runtime','surface':'work','run_id':'r',
                  'recorded_status':'completed','browser_controls_verified':True,'reference':'receipt'}
        with self.assertRaises(lc.Blocked): lc.restore_work_preference(self.cfg,evidence,NOW)
    def test_replaced_automation_denied(self):
        with self.assertRaises(lc.Blocked): lc.check_route(self.cfg,dict(self.actor,automation_id='retired'))

if __name__=='__main__': unittest.main()
