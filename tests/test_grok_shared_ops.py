import copy
import json
import sys
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import launcher_coordination as lc
import launcher_run_ledger as lr
import shared_input_registry as si
import grok_inbox
import test_launcher_coordination as fixtures
GROK_NOW = fixtures.GROK_NOW
from test_site_actions import files, row, NOW
import robot_site_actions as rsa

class DurableRunTests(unittest.TestCase):
    def setUp(self):
        base = fixtures.GrokHelperTests('test_holder_format'); base.setUp()
        self.cfg, self.actor, self.lock, self.scan, self.item = base.cfg, base.actor, base.lock, base.scan, base.item
        self.cfg['run_ledger']={'required_surfaces':['grok']}
        self.actor['provider_run_id']='actual-provider-run-100'
        self.ledger=lr.empty()
    def transaction(self, **kw):
        return lc.prepare_transaction(kw.get('cfg',self.cfg),kw.get('lock',self.lock),kw.get('item',self.item),
                                      kw.get('actor',self.actor),self.scan,GROK_NOW,ledger=kw.get('ledger',self.ledger))
    def telegram(self):
        self.cfg['grok_launcher']['owner_command_launch']={'enabled':True,'telegram_chat_id':'215961273','max_age_minutes':60,'bypass_launch_window':True}
        self.actor.update(kind='owner_command',owner_command={'source':'telegram','quote':'Запусти готовую сцену','chat_id':'215961273','at':lc.stamp(GROK_NOW),
            'telegram_update':{'update_id':123,'message':{'message_id':99,'date':int(GROK_NOW.timestamp()),'chat':{'type':'private','id':215961273},'from':{'id':215961273,'is_bot':False},'text':'Запусти готовую сцену'}}})
    def test_ledger_missing_fails_closed(self):
        with self.assertRaises(lc.Blocked): self.transaction(ledger=None)
    def test_real_provider_run_required(self):
        del self.actor['provider_run_id']
        with self.assertRaises(lc.Blocked): self.transaction()
    def test_local_uuid_not_provider_run(self):
        self.actor['provider_run_id']=self.actor['execution_instance_id']
        with self.assertRaises(lc.Blocked): self.transaction()
    def test_returns_bound_intent_and_ledger(self):
        i,l=self.transaction();self.assertTrue(lr.verify_binding(i,l));self.assertEqual(len(l['runs']),1)
        self.assertEqual(self.ledger,lr.empty());self.assertEqual(self.item['state'],'claimed')
    def test_same_run_cannot_take_other_item_even_reset_counter(self):
        i,l=self.transaction()
        with self.assertRaises(lc.Blocked):self.transaction(item=dict(self.item,id='different'),ledger=l)
    def test_new_run_can_consume_new_item(self):
        i,l=self.transaction();a=dict(self.actor,provider_run_id='actual-provider-run-101')
        j,m=self.transaction(actor=a,item=dict(self.item,id='different'),ledger=l)
        self.assertEqual(len(m['runs']),2)
    def test_message_redelivery_new_run_denied(self):
        self.telegram();i,l=self.transaction();self.actor['provider_run_id']='another-run'
        with self.assertRaises(lc.Blocked):self.transaction(ledger=l)
    def test_duplicate_update_with_different_message_denied(self):
        self.telegram();i,l=self.transaction();self.actor['provider_run_id']='another-run'
        self.actor['owner_command']['telegram_update']['message']['message_id']=100
        with self.assertRaises(lc.Blocked):self.transaction(ledger=l)
    def test_unknown_does_not_release_budget(self):
        i,l=self.transaction();i['state']='submission_unknown'
        with self.assertRaises(lc.Blocked):self.transaction(ledger=l)
    def test_telegram_sender_must_be_owner(self):
        self.telegram();self.actor['owner_command']['telegram_update']['message']['from']['id']=1
        with self.assertRaises(lc.Blocked):self.transaction()
    def test_forwarded_or_edited_message_denied(self):
        for k in ['forward_origin','forward_date','edit_date','via_bot','business_connection_id']:
            self.telegram();self.actor['owner_command']['telegram_update']['message'][k]={}
            with self.subTest(k=k),self.assertRaises(lc.Blocked):self.transaction()
    def test_telegram_time_and_text_not_fabricated(self):
        self.telegram();self.actor['owner_command']['quote']='other quote'
        with self.assertRaises(lc.Blocked):self.transaction()
        self.telegram();self.actor['owner_command']['telegram_update']['message']['date']-=20
        with self.assertRaises(lc.Blocked):self.transaction()
    def test_wrong_chat_and_nonprivate_denied(self):
        self.telegram();self.actor['owner_command']['telegram_update']['message']['chat']['type']='group'
        with self.assertRaises(lc.Blocked):self.transaction()
    def test_message_ids_are_not_booleans(self):
        self.telegram();self.actor['owner_command']['telegram_update']['message']['message_id']=True
        with self.assertRaises(lc.Blocked):self.transaction()
    def test_grok_chat_stable_message_key(self):
        self.telegram();self.actor['owner_command']={'source':'grok_chat','quote':'Запусти сцену','at':lc.stamp(GROK_NOW),'conversation_id':'conv-1','message_id':'msg-1','sender_role':'owner'}
        i,l=self.transaction();self.actor['provider_run_id']='next-run'
        with self.assertRaises(lc.Blocked):self.transaction(ledger=l)
    def test_corrupted_indexes_denied(self):
        i,l=self.transaction();l['events']['bad']='unknown'
        with self.assertRaises(lc.Blocked):self.transaction(ledger=l)
    def test_readback_mismatch_denied(self):
        i,l=self.transaction();i['claim']['submission_intent_id']='different'
        with self.assertRaises(lr.LedgerBlocked):lr.verify_binding(i,l)
    def test_lease_and_price_gate_not_bypassed(self):
        with self.assertRaises(lc.Blocked):self.transaction(lock=dict(self.lock,holder='foreign'))
        self.item['claim']['preflight']['credits_cost']=1
        with self.assertRaises(lc.Blocked):self.transaction()
    def test_first_create_gate_remains(self):
        self.cfg['grok_launcher']['first_real_create']['owner_go_ahead']=False
        with self.assertRaises(lc.Blocked):self.transaction()
    def test_night_policy_requires_explicit_window(self):
        # The existing fixture still forbids night. Explicit owner-approved config opens hours, not permission gates.
        now=GROK_NOW.replace(hour=2)
        a=dict(self.actor,lease_acquired_at=lc.stamp(now-timedelta(minutes=1)))
        lock=dict(self.lock,acquired_at=a['lease_acquired_at'],expires_at=lc.stamp(now+timedelta(minutes=5)))
        scan=dict(self.scan,checked_at=lc.stamp(now))
        with self.assertRaises(lc.Blocked):lc.prepare_transaction(self.cfg,lock,self.item,a,scan,now,ledger=self.ledger)
        self.cfg['grok_launcher']['launch_window']['first_hour']=0
        i,l=lc.prepare_transaction(self.cfg,lock,self.item,a,scan,now,ledger=self.ledger)
        self.assertTrue(lr.verify_binding(i,l))
    def batch(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['grok_launcher']['max_submissions_per_wake']=6
        cfg['grok_launcher']['slot_capacity']=6
        return cfg
    def test_one_run_fills_capacity_and_does_not_need_a_new_run_id(self):
        cfg,ledger=self.batch(),self.ledger
        keys=[]
        for n in range(6):
            item=dict(self.item,id='READY-%d'%n)
            actor=dict(self.actor,submissions_this_wake=n)
            scan=dict(self.scan,free_slots=6-n)
            out,ledger=lc.prepare_transaction(cfg,self.lock,item,actor,scan,GROK_NOW,ledger=ledger)
            self.assertTrue(lr.verify_binding(out,ledger))
            keys.append(out['claim']['provider_run_key'])
        self.assertEqual(len(set(keys)),1)
        self.assertEqual(len(ledger['runs'][keys[0]]['submissions']),6)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,dict(self.item,id='READY-6'),
                                   dict(self.actor,submissions_this_wake=6),dict(self.scan,free_slots=1),
                                   GROK_NOW,ledger=ledger)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,dict(self.item,id='RESET'),
                                   dict(self.actor,submissions_this_wake=0),self.scan,GROK_NOW,ledger=ledger)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,dict(self.item,id='READY-0'),
                                   dict(self.actor,submissions_this_wake=1),self.scan,GROK_NOW,ledger=ledger)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,dict(self.item,id='SKIP'),
                                   dict(self.actor,submissions_this_wake=2),self.scan,GROK_NOW,ledger=ledger)
        legacy=copy.deepcopy(ledger)
        del legacy['runs'][keys[0]]['submissions']
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,dict(self.item,id='LEGACY'),
                                   dict(self.actor,submissions_this_wake=1),self.scan,GROK_NOW,ledger=legacy)
        for bad in (7,100,0,True):
            broken=self.batch();broken['grok_launcher']['max_submissions_per_wake']=bad
            with self.subTest(bad=bad),self.assertRaises(lc.Blocked):
                lc.prepare_transaction(broken,self.lock,dict(self.item,id='OVER'),self.actor,self.scan,GROK_NOW,ledger=lr.empty())
        broken=self.batch();broken['grok_launcher']['slot_capacity']=7
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(broken,self.lock,self.item,self.actor,self.scan,GROK_NOW,ledger=lr.empty())
    def test_fresh_zero_slots_paid_unknown_and_refusal_stay_blocked(self):
        cfg=self.batch()
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,self.item,dict(self.actor,submissions_this_wake=0),
                                   dict(self.scan,free_slots=0),GROK_NOW,ledger=lr.empty())
        paid=copy.deepcopy(self.item);paid['claim']['preflight']['credits_cost']=1
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,paid,self.actor,self.scan,GROK_NOW,ledger=lr.empty())
        for state in ('submission_unknown','submitted','submitting'):
            with self.subTest(state=state),self.assertRaises(lc.Blocked):
                lc.prepare_transaction(cfg,self.lock,dict(self.item,state=state),self.actor,self.scan,GROK_NOW,ledger=lr.empty())
        refused=dict(self.item,provider_error_code='7000',substantive_refusal=True)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,refused,self.actor,self.scan,GROK_NOW,ledger=lr.empty())
        linked=dict(self.item,depends_on_completed=['PREV'],references=[{'slot':'@Video1','required':True,'source_item_id':'PREV'}])
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,linked,self.actor,self.scan,GROK_NOW,ledger=lr.empty())
    def test_same_owner_message_can_fill_another_item_but_not_a_new_run(self):
        self.telegram();cfg=self.batch();i,l=lc.prepare_transaction(cfg,self.lock,self.item,self.actor,self.scan,GROK_NOW,ledger=self.ledger)
        second=dict(self.item,id='NEXT')
        actor=dict(self.actor,submissions_this_wake=1)
        out,ledger=lc.prepare_transaction(cfg,self.lock,second,actor,self.scan,GROK_NOW,ledger=l)
        self.assertEqual(out['claim']['provider_run_id'],self.actor['provider_run_id'])
        self.assertTrue(lr.verify_binding(out,ledger))
        self.actor['provider_run_id']='another-run'
        self.actor['submissions_this_wake']=0
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,dict(self.item,id='REPLAY'),self.actor,self.scan,GROK_NOW,ledger=ledger)
    def test_live_s49e_run_stays_legacy_one_create(self):
        root=Path(__file__).resolve().parents[1]
        ledger=json.loads((root/'ops/launcher-run-ledger.json').read_text(encoding='utf-8'))
        lr.validate(ledger)
        row=next(r for r in ledger['runs'].values() if r.get('item_id')=='S49E')
        self.assertNotIn('submissions', row)
        cfg=self.batch()
        actor=dict(self.actor, provider_run_id=row['provider_run_id'], submissions_this_wake=1)
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,dict(self.item,id='NOT-S49E'),actor,self.scan,GROK_NOW,ledger=ledger)
    def test_content_refusal_is_not_retried_without_separate_consent(self):
        cfg=self.batch()
        item=copy.deepcopy(self.item)
        item['submission_history']=[{'task_id':'old','outcome':'copyright_refusal','error_code':'7000'}]
        item['retry_control']={'policy_id':'owner-20261030-technical-retry','retry_attempts_used':1,'max_retry_attempts':2}
        with self.assertRaises(lc.Blocked):
            lc.prepare_transaction(cfg,self.lock,item,self.actor,self.scan,GROK_NOW,ledger=lr.empty())
        item['owner_retry_authorized']=True
        out,ledger=lc.prepare_transaction(cfg,self.lock,item,self.actor,self.scan,GROK_NOW,ledger=lr.empty())
        self.assertEqual(out['state'],'submitting')
        self.assertTrue(lr.verify_binding(out,ledger))

class SiteAndInputsTests(unittest.TestCase):
    def test_grok_target_roundtrip_and_no_duplicate(self):
        d=row('grok-test','owner_task',value='grok',note='Проверка маршрута Grok')
        nf,acks=rsa.plan([d],files(),NOW);inbox=json.loads(nf[rsa.INBOX])
        task=inbox['tasks'][-1];self.assertEqual(task['to'],'grok');self.assertIn('Grok',acks[0][2])
        nf2,acks2=rsa.plan([d],files(inbox=inbox),NOW)
        self.assertNotIn(rsa.INBOX,nf2)
        task.update(status='done',taken_by='grok:test',result='Тестовый ответ')
        d.update(status='in_progress',result_note=acks[0][2])
        nf3,acks3=rsa.plan([d],files(inbox=inbox),NOW)
        self.assertEqual(acks3[0][1],'applied');self.assertIn('grok:test',acks3[0][2])
    def test_site_and_edge_targets(self):
        root=Path(__file__).resolve().parents[1]
        for path in ['index.html','film.html']:
            self.assertIn('<option value="grok">', (root/path).read_text())
        self.assertIn('"chatgpt", "grok", "any"', (root/'ops/supabase/owner-decision/index.ts').read_text())
    def test_drive_input_no_library_required(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'ops').mkdir()
            ref={'slot':'@Video1','sha256':'a'*64,'drive_file_id':'drive-id','shared_readback_sha256':'a'*64,'input_status':'available'}
            (root/'ops/topview-launch-queue.json').write_text(json.dumps({'items':[{'id':'S1','state':'waiting_for_slot','references':[ref]}]}))
            out=si.derive(root);self.assertTrue(out['items'][0]['all_required_inputs_shared'])
    def test_future_result_not_faked_ready(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'ops').mkdir()
            (root/'ops/topview-launch-queue.json').write_text(json.dumps({'items':[{'id':'S1','state':'blocked_inputs','references':[{'slot':'@Video1','source_item_id':'S0'}]}]}))
            self.assertFalse(si.derive(root)['items'][0]['all_required_inputs_shared'])
    def test_grok_inbox_never_takes_claude_tasks(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'ops').mkdir()
            (root/'ops/owner-tasks.json').write_text(json.dumps({'tasks':[{'id':'c','to':'claude','status':'open'},{'id':'g','to':'grok','status':'open'}]}))
            self.assertEqual([x['id'] for x in grok_inbox.pending(root)['tasks']],['g'])
