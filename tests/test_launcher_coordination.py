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

GROK_NOW = datetime(2026, 11, 1, 10, 15, tzinfo=timezone.utc)  # 11:15 Europe/Amsterdam (CET)
C = '33333333-3333-4333-8333-333333333333'
BOARD = '1a6244cf1ae747ef847d949a80d6133c'

class GrokHelperTests(unittest.TestCase):
    def setUp(self):
        base = CoordinationTests('test_both_peers_run_independently')
        base.setUp()
        self.cfg = copy.deepcopy(base.cfg)
        self.cfg['peers']['grok'] = {'enabled': True, 'automation_ids': ['grok-task']}
        self.cfg['grok_launcher'] = {
            'board_id': BOARD, 'max_submissions_per_wake': 1,
            'retries': {'enabled': True, 'policy_id': 'owner-20261030-technical-retry', 'max_retry_attempts': 2},
            'launch_window': {'timezone': 'Europe/Amsterdam', 'first_hour': 8, 'last_hour': 23,
                              'first_minute': 10, 'last_minute': 40}}
        self.actor = {'execution_instance_id': C, 'surface': 'grok', 'kind': 'scheduled',
                      'automation_id': 'grok-task', 'route_generation': 2,
                      'lease_acquired_at': lc.stamp(GROK_NOW-timedelta(minutes=1))}
        self.lock = {'state': 'held', 'holder': 'grok:'+C, 'acquired_at': self.actor['lease_acquired_at'],
                     'expires_at': lc.stamp(GROK_NOW+timedelta(minutes=5))}
        self.scan = {'complete': True, 'checked_at': lc.stamp(GROK_NOW), 'free_slots': 1}
        item = copy.deepcopy(base.item)
        item['board_id'] = BOARD
        item['claim']['execution_instance_id'] = C
        self.item = item
    def intent(self, **over):
        cfg = over.get('cfg', self.cfg)
        return lc.prepare_intent(cfg, over.get('lock', self.lock), over.get('item', self.item),
                                 over.get('actor', self.actor), self.scan, over.get('now', GROK_NOW))
    def test_holder_format(self):
        self.assertEqual(lc.holder(self.actor), 'grok:'+C)
        self.assertEqual(lc.holder(dict(self.actor, surface='work')), 'chatgpt:work:'+C)
    def test_grok_registered_as_independent_helper(self):
        self.assertTrue(lc.check_route(self.cfg, self.actor))
        self.assertEqual(self.cfg['preferred_executor'], 'ordinary')
        self.assertTrue(lc.check_route(self.cfg, dict(self.actor, surface='ordinary', automation_id='ordinary-task')))
    def test_grok_intent_in_window(self):
        out = self.intent()
        self.assertEqual(out['state'], 'submitting')
        self.assertEqual(out['claim']['lease_holder'], 'grok:'+C)
        with self.assertRaises(lc.Blocked): self.intent(item=out)
    def test_unregistered_disabled_or_unknown_grok_denied(self):
        cfg = copy.deepcopy(self.cfg); del cfg['peers']['grok']
        with self.assertRaises(lc.Blocked): lc.check_route(cfg, self.actor)
        cfg = copy.deepcopy(self.cfg); cfg['peers']['grok']['enabled'] = False
        with self.assertRaises(lc.Blocked): lc.check_route(cfg, self.actor)
        with self.assertRaises(lc.Blocked): lc.check_route(self.cfg, dict(self.actor, automation_id='other'))
        cfg = copy.deepcopy(self.cfg); cfg['peers']['grok']['automation_ids'] = []
        with self.assertRaises(lc.Blocked): lc.check_route(cfg, self.actor)
        with self.assertRaises(lc.Blocked): lc.instance(dict(self.actor, surface='claude'))
    def test_grok_lease_is_not_interchangeable(self):
        with self.assertRaises(lc.Blocked): lc.check_lease(dict(self.lock, holder='chatgpt:ordinary:'+C), self.actor, GROK_NOW)
        with self.assertRaises(lc.Blocked): lc.check_lease(dict(self.lock, holder='grok:'+A), self.actor, GROK_NOW)
        with self.assertRaises(lc.Blocked): lc.check_lease(self.lock, dict(self.actor, surface='ordinary'), GROK_NOW)
    def test_grok_release_only_own_lease(self):
        self.assertEqual(lc.release_exact(self.lock, self.actor, GROK_NOW)['state'], 'free')
        with self.assertRaises(lc.Blocked): lc.release_exact(dict(self.lock, holder='grok:'+A), self.actor, GROK_NOW)
    def test_grok_launch_window(self):
        local_minutes = {9: False, 10: True, 40: True, 41: False, 59: False, 0: False}
        for minute, allowed in local_minutes.items():
            now = datetime(2026, 11, 1, 10, minute, tzinfo=timezone.utc)
            lock = dict(self.lock, acquired_at=lc.stamp(now-timedelta(minutes=1)), expires_at=lc.stamp(now+timedelta(minutes=5)))
            actor = dict(self.actor, lease_acquired_at=lock['acquired_at'])
            scan = dict(self.scan, checked_at=lc.stamp(now))
            with self.subTest(minute=minute):
                if allowed:
                    lc.prepare_intent(self.cfg, lock, self.item, actor, scan, now)
                else:
                    with self.assertRaises(lc.Blocked): lc.prepare_intent(self.cfg, lock, self.item, actor, scan, now)
    def test_grok_hours_follow_amsterdam_time(self):
        for utc_hour, allowed in ((6, False), (7, True), (22, True), (23, False)):  # 07:xx UTC = 08:xx CET
            now = datetime(2026, 11, 1, utc_hour, 15, tzinfo=timezone.utc)
            lock = dict(self.lock, acquired_at=lc.stamp(now-timedelta(minutes=1)), expires_at=lc.stamp(now+timedelta(minutes=5)))
            actor = dict(self.actor, lease_acquired_at=lock['acquired_at'])
            scan = dict(self.scan, checked_at=lc.stamp(now))
            with self.subTest(utc_hour=utc_hour):
                if allowed:
                    lc.prepare_intent(self.cfg, lock, self.item, actor, scan, now)
                else:
                    with self.assertRaises(lc.Blocked): lc.prepare_intent(self.cfg, lock, self.item, actor, scan, now)
    def test_grok_only_authorized_board(self):
        for board in ('other-board', None):
            with self.subTest(board=board), self.assertRaises(lc.Blocked):
                self.intent(item=dict(self.item, board_id=board))
    def test_grok_one_submission_per_wake(self):
        with self.assertRaises(lc.Blocked): self.intent(actor=dict(self.actor, submissions_this_wake=1))
        with self.assertRaises(lc.Blocked): self.intent(actor=dict(self.actor, submissions_this_wake='0'))
        self.assertEqual(self.intent(actor=dict(self.actor, submissions_this_wake=0))['state'], 'submitting')
    def test_grok_policy_missing_fails_closed(self):
        cfg = copy.deepcopy(self.cfg); del cfg['grok_launcher']
        with self.assertRaises(lc.Blocked): self.intent(cfg=cfg)
        cfg = copy.deepcopy(self.cfg); del cfg['grok_launcher']['launch_window']['timezone']
        with self.assertRaises(lc.Blocked): self.intent(cfg=cfg)
    def test_grok_keeps_other_gates(self):
        item = copy.deepcopy(self.item); item['claim']['preflight']['credits_cost'] = 1
        with self.assertRaises(lc.Blocked): self.intent(item=item)
        with self.assertRaises(lc.Blocked): self.intent(item=dict(self.item, state='waiting_for_slot'))
        with self.assertRaises(lc.Blocked): self.intent(actor=dict(self.actor, route_generation=1))
    def retry_item(self, used=1, **over):
        item = copy.deepcopy(self.item)
        item['submission_history'] = [{'task_id': 'old-failed-task', 'outcome': 'failed'}]
        item['retry_control'] = {'policy_id': 'owner-20261030-technical-retry', 'retry_attempts_used': used,
                                 'max_retry_attempts': 2}
        item['retry_control'].update(over)
        return item
    def test_grok_retry_within_budget_allowed(self):
        for used in (1, 2):
            with self.subTest(used=used):
                self.assertEqual(self.intent(item=self.retry_item(used))['state'], 'submitting')
    def test_grok_retry_budget_and_counter_fail_closed(self):
        for bad in ({'retry_attempts_used': 3}, {'retry_attempts_used': 0}, {'retry_attempts_used': None},
                    {'retry_attempts_used': '1'}, {'max_retry_attempts': 3}, {'policy_id': 'other'}):
            with self.subTest(bad=bad), self.assertRaises(lc.Blocked):
                self.intent(item=self.retry_item(**bad))
    def test_grok_retry_requires_history_and_control(self):
        item = self.retry_item(); del item['submission_history']
        with self.assertRaises(lc.Blocked): self.intent(item=item)
        item = self.retry_item(); del item['retry_control']
        with self.assertRaises(lc.Blocked): self.intent(item=item)
    def test_grok_retry_denied_when_policy_disabled(self):
        cfg = copy.deepcopy(self.cfg); cfg['grok_launcher']['retries']['enabled'] = False
        with self.assertRaises(lc.Blocked): self.intent(cfg=cfg, item=self.retry_item())
        del cfg['grok_launcher']['retries']
        with self.assertRaises(lc.Blocked): self.intent(cfg=cfg, item=self.retry_item())
    def test_grok_retry_keeps_window_paid_and_wake_limits(self):
        with self.assertRaises(lc.Blocked): self.intent(item=self.retry_item(), actor=dict(self.actor, submissions_this_wake=1))
        with self.assertRaises(lc.Blocked): self.intent(item=self.retry_item(), now=datetime(2026, 11, 1, 10, 50, tzinfo=timezone.utc))
        item = self.retry_item(); item['claim']['preflight']['credits_cost'] = 1
        with self.assertRaises(lc.Blocked): self.intent(item=item)
    def test_grok_interactive_and_takeover_not_authorized(self):
        self.cfg['foreground_owners']['grok'] = {'session_id': 's', 'epoch': 1}
        actor = dict(self.actor, kind='interactive', session_id='s', foreground_epoch=1)
        with self.assertRaises(lc.Blocked): lc.check_route(self.cfg, actor)
        with self.assertRaises(lc.Blocked): lc.takeover(self.cfg, self.lock, dict(actor, session_id='new'), GROK_NOW, 'Продолжай')
    def test_registry_file_registers_grok_fail_closed(self):
        import json
        cfg = json.loads((Path(__file__).resolve().parents[1] / 'ops' / 'slot-backup.json').read_text(encoding='utf-8'))
        self.assertEqual(cfg['preferred_executor'], 'ordinary')
        self.assertIn('grok', cfg['peers'])
        policy = cfg['grok_launcher']
        self.assertEqual(policy['role'], 'helper')
        self.assertEqual(policy['board_id'], BOARD)
        self.assertEqual(policy['max_submissions_per_wake'], 1)
        self.assertEqual(policy['acceptance']['state'], 'configured_pending_dry_run')
        self.assertIs(policy['retries']['enabled'], True)
        self.assertEqual(policy['retries']['max_retry_attempts'], 2)
        self.assertEqual(policy['retries']['policy_id'], 'owner-20261030-technical-retry')
        self.assertEqual(policy['retries']['owner_quote'], 'Да, разрешаю тебе повторы по TOPVIEW-RETRY')
        # Not launch-capable until dry-run acceptance and an owner-approved routine ID.
        self.assertIs(cfg['peers']['grok']['enabled'], False)
        self.assertEqual(cfg['peers']['grok']['automation_ids'], [])
        with self.assertRaises(lc.Blocked):
            lc.check_route(cfg, {'execution_instance_id': C, 'surface': 'grok', 'kind': 'scheduled',
                                 'automation_id': 'anything', 'route_generation': cfg['route_generation']})

if __name__=='__main__': unittest.main()
