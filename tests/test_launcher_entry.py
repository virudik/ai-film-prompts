import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import launcher_entry as entry
import test_launcher_coordination as fixtures


class EntryTests(unittest.TestCase):
    def setUp(self):
        f=fixtures.CoordinationTests();f.setUp()
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'repo';(self.root/'ops').mkdir(parents=True)
        self.request={'actor':f.actor,'item_id':'S-example','preflight':f.item['claim']['preflight'],
                      'scan':dict(f.scan,item_reconciliation={'S-example':{
                          'complete':True,'matched_task_ids':[],'ambiguous':False}})}
        self.queue={'items':[{'id':'S-example','state':'waiting_for_slot'}]}
        for p,body in [(entry.lc.CONFIG,f.cfg),(entry.lc.LOCK,f.lock),(entry.lc.QUEUE,self.queue)]:
            (self.root/p).write_text(json.dumps(body))
        self.selection=patch.object(entry.lc.queue_readiness,'launch_candidates',return_value={'chosen':['S-example']})
        self.selection.start();self.addCleanup(self.selection.stop)
    def step(self,phase,session=None,request=None):
        return entry.step(self.root,phase,request or self.request,session,fixtures.NOW,'a'*40)
    def publish(self,transaction):
        # Model readback only; no GitHub/Topview call.
        for path,body in transaction['files'].items():(self.root/path).write_text(json.dumps(body))
    def intent(self):
        claim,session=self.step('claim');self.publish(claim)
        intent,session=self.step('intent',session);self.publish(intent)
        return intent,session
    def test_all_phases_keep_distinct_cas_boundaries(self):
        plan,_=self.step('plan');self.assertFalse(plan['create_allowed'])
        claim,session=self.step('claim');self.assertEqual(claim['expected_main_sha'],'a'*40)
        with self.assertRaises(entry.lc.Blocked):self.step('intent',session)
        self.publish(claim)
        intent,session=self.step('intent',session);self.assertFalse(intent['create_allowed'])
        with self.assertRaises(entry.lc.Blocked):self.step('verify',session)
        self.publish(intent)
        verified,session=self.step('verify',session)
        self.assertTrue(verified['checks_passed']);self.assertFalse(verified['replay_permitted'])
        with self.assertRaises(entry.lc.Blocked):self.step('verify',session)
    def test_same_entry_works_for_registered_grok(self):
        f=fixtures.GrokHelperTests();f.setUp()
        self.request['actor']=f.actor
        self.request['scan']['checked_at']=entry.lc.stamp(fixtures.GROK_NOW)
        self.queue['board_id']=fixtures.BOARD
        self.queue['items'][0]['board_id']=fixtures.BOARD
        for path,body in [(entry.lc.CONFIG,f.cfg),(entry.lc.LOCK,f.lock),(entry.lc.QUEUE,self.queue)]:
            (self.root/path).write_text(json.dumps(body))
        session=None
        for phase in ['claim','intent','verify']:
            result,session=entry.step(self.root,phase,self.request,session,fixtures.GROK_NOW,'a'*40)
            if phase!='verify':self.publish(result)
        self.assertTrue(result['checks_passed'])

    def test_original_actor_and_payload_are_required(self):
        intent,session=self.intent()
        request=copy.deepcopy(self.request);request['actor']['execution_instance_id']=fixtures.B
        with self.assertRaises(entry.lc.Blocked):self.step('verify',session,request)
        queue=json.loads((self.root/entry.lc.QUEUE).read_text());queue['items'][0]['prompt']='changed'
        (self.root/entry.lc.QUEUE).write_text(json.dumps(queue))
        with self.assertRaises(entry.lc.Blocked):self.step('verify',session)
    def test_foreign_lock_and_paid_cost_block(self):
        request=copy.deepcopy(self.request);request['preflight']['credits_cost']=18
        with self.assertRaises(entry.lc.Blocked):self.step('claim',request=request)
        lock=json.loads((self.root/entry.lc.LOCK).read_text());lock['holder']='grok:'+fixtures.B
        (self.root/entry.lc.LOCK).write_text(json.dumps(lock))
        with self.assertRaises(entry.lc.Blocked):self.step('claim')
    def test_unknown_and_duplicate_scan_block(self):
        request=copy.deepcopy(self.request);request['scan']['item_reconciliation']['S-example']['matched_task_ids']=['task']
        with self.assertRaises(entry.lc.Blocked):self.step('claim',request=request)
        self.queue['items'][0]['state']='submission_unknown'
        (self.root/entry.lc.QUEUE).write_text(json.dumps(self.queue))
        with self.assertRaises(entry.lc.Blocked):self.step('claim')
    def test_no_reconstruction_or_session_reuse(self):
        with self.assertRaises(entry.lc.Blocked):self.step('intent')
        with self.assertRaises(entry.lc.Blocked):self.step('verify')
        _,session=self.step('claim')
        with self.assertRaises(entry.lc.Blocked):self.step('claim',session)
    def test_atomic_local_marker_blocks_concurrent_or_crashed_invocation(self):
        p=Path(self.tmp.name)/'session.busy'
        entry.write_exclusive(p,{'first':True})
        with self.assertRaises(FileExistsError):entry.write_exclusive(p,{'second':True})
    def test_snapshot_rejection_does_not_consume_unstarted_claim_session(self):
        request = Path(self.tmp.name)/'request.json';request.write_text(json.dumps(self.request))
        session = Path(self.tmp.name)/'session.json'
        argv=['launcher_entry.py',str(self.root),'claim','--request',str(request),'--session',str(session)]
        for snapshots in ([entry.lc.Blocked('checkout_must_equal_fresh_origin_main')],
                          ['a'*40, entry.lc.Blocked('checkout_must_equal_fresh_origin_main')],
                          ['a'*40, 'b'*40]):
            with self.subTest(snapshots=snapshots), patch.object(sys,'argv',argv), \
                 patch.object(entry,'snapshot',side_effect=snapshots), \
                 patch.object(entry,'materialize_snapshot'), patch.object(entry,'step') as step, \
                 patch('sys.stdout',new_callable=io.StringIO):
                self.assertEqual(entry.main(),2)
                step.assert_not_called()
                self.assertFalse(session.exists())
                self.assertFalse(session.with_name(session.name+'.busy').exists())

    def test_existing_busy_marker_survives_snapshot_failure_and_success(self):
        request=Path(self.tmp.name)/'request.json';request.write_text(json.dumps(self.request))
        session=Path(self.tmp.name)/'session.json'
        busy=session.with_name(session.name+'.busy');busy.write_text('original crash marker')
        argv=['launcher_entry.py',str(self.root),'claim','--request',str(request),'--session',str(session)]
        for snapshots in ([entry.lc.Blocked('checkout_must_equal_fresh_origin_main')], ['a'*40,'a'*40]):
            with self.subTest(snapshots=snapshots), patch.object(sys,'argv',argv), \
                 patch.object(entry,'snapshot',side_effect=snapshots), \
                 patch.object(entry,'materialize_snapshot'), patch.object(entry,'step') as step, \
                 patch('sys.stdout',new_callable=io.StringIO):
                self.assertEqual(entry.main(),2)
                step.assert_not_called()
                self.assertEqual(busy.read_text(),'original crash marker')

    def test_error_after_exclusive_marker_retains_anti_replay_guard(self):
        request=Path(self.tmp.name)/'request.json';request.write_text(json.dumps(self.request))
        session=Path(self.tmp.name)/'session.json'
        argv=['launcher_entry.py',str(self.root),'claim','--request',str(request),'--session',str(session)]
        with patch.object(sys,'argv',argv), patch.object(entry,'snapshot',return_value='a'*40), \
             patch.object(entry,'materialize_snapshot'), \
             patch.object(entry,'step',side_effect=entry.lc.Blocked('after_phase_entry')), \
             patch('sys.stdout',new_callable=io.StringIO):
            self.assertEqual(entry.main(),2)
            self.assertTrue(session.with_name(session.name+'.busy').exists())

    def test_unpublished_claim_rejects_intent_before_creating_marker(self):
        import shutil
        _,session=self.step('claim')
        request=Path(self.tmp.name)/'request.json';request.write_text(json.dumps(self.request))
        session_path=Path(self.tmp.name)/'session.json';session_path.write_text(json.dumps(session))
        argv=['launcher_entry.py',str(self.root),'intent','--request',str(request),'--session',str(session_path)]
        def materialize(root,sha,destination):shutil.copytree(root,destination,dirs_exist_ok=True)
        with patch.object(sys,'argv',argv),patch.object(entry,'snapshot',return_value='a'*40), \
             patch.object(entry,'materialize_snapshot',side_effect=materialize),patch('sys.stdout',new_callable=io.StringIO) as out:
            self.assertEqual(entry.main(),2)
            self.assertIn('original_payload_not_published_exactly',out.getvalue())
            self.assertFalse(session_path.with_name(session_path.name+'.busy').exists())
            self.assertEqual(json.loads(session_path.read_text()),session)

    def test_publication_precheck_is_repeated_after_exclusive_marker(self):
        import shutil
        transaction,session=self.step('claim');self.publish(transaction)
        request=Path(self.tmp.name)/'request.json';request.write_text(json.dumps(self.request))
        session_path=Path(self.tmp.name)/'session.json';session_path.write_text(json.dumps(session))
        argv=['launcher_entry.py',str(self.root),'intent','--request',str(request),'--session',str(session_path)]
        def materialize(root,sha,destination):shutil.copytree(root,destination,dirs_exist_ok=True)
        original_write=entry.write_exclusive
        def race(path,value):
            original_write(path,value)
            if path.name.endswith('.busy'):
                changed=dict(session,actor_sha='another-execution');session_path.write_text(json.dumps(changed))
        with patch.object(sys,'argv',argv),patch.object(entry,'snapshot',return_value='a'*40), \
             patch.object(entry,'materialize_snapshot',side_effect=materialize), \
             patch.object(entry,'write_exclusive',side_effect=race),patch('sys.stdout',new_callable=io.StringIO) as out:
            self.assertEqual(entry.main(),2)
            self.assertIn('original_session_actor_and_item_required',out.getvalue())
            self.assertTrue(session_path.with_name(session_path.name+'.busy').exists())
            self.assertEqual(json.loads(session_path.read_text())['phase'],'claim_prepared')

    def refresh_request(self,session,sha='b'*40):
        request=copy.deepcopy(self.request)
        request['_claim_history']={'base_main_sha':session['claim_base_main_sha'],
                                  'readback_main_sha':sha,'session_sha':entry.digest(session),
                                  'item_unchanged':True,'ledger_unchanged':True}
        return request

    def test_refresh_claim_rebuilds_current_queue_and_preserves_unpublished_identity(self):
        _,session=self.step('claim')
        self.queue['items'].append({'id':'other','state':'completed','task_id':'peer-task'})
        (self.root/entry.lc.QUEUE).write_text(json.dumps(self.queue))
        out,new=entry.step(self.root,'refresh-claim',self.refresh_request(session),session,fixtures.NOW,'b'*40)
        self.assertEqual(new['claim_id'],session['claim_id'])
        self.assertEqual(out['expected_main_sha'],'b'*40)
        self.assertEqual(out['files'][entry.lc.QUEUE]['items'][1]['task_id'],'peer-task')
        self.assertFalse(out['create_allowed'])
        self.assertEqual(new['claim_base_main_sha'],'b'*40)

    def test_refresh_requires_history_and_full_original_guards(self):
        _,session=self.step('claim')
        for change in ('history','phase','base','paid','scan','lease'):
            request=self.refresh_request(session);candidate=copy.deepcopy(session)
            if change=='history':request.pop('_claim_history')
            if change=='phase':candidate['phase']='intent_prepared'
            if change=='base':candidate['base_item_sha']='changed'
            if change=='paid':request['preflight']['credits_cost']=18
            if change=='scan':request['scan']['complete']=False
            if change=='lease':request['actor']['execution_instance_id']=fixtures.B
            with self.subTest(change=change),self.assertRaises(entry.lc.Blocked):
                entry.step(self.root,'refresh-claim',request,candidate,fixtures.NOW,'b'*40)

    def test_claim_history_detects_publish_then_revert_not_just_current_item(self):
        import subprocess
        root=Path(self.tmp.name)/'history';(root/'ops').mkdir(parents=True)
        def git(*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
        git('init','-q');git('config','user.email','test@example.invalid');git('config','user.name','test')
        q=root/entry.lc.QUEUE;q.write_text(json.dumps(self.queue))
        (root/entry.ledger_tools.PATH).write_text(json.dumps({'runs':{}}))
        def commit():git('add','.');git('commit','-qm','fixture');return git('rev-parse','HEAD')
        base=commit();session={'claim_base_main_sha':base,'base_item_sha':entry.digest(self.queue['items'][0]),'item_id':'S-example'}
        (root/'unrelated').write_text('robot telemetry');head=commit()
        self.assertTrue(entry.unchanged_claim_history(root,session,head)['item_unchanged'])
        changed=copy.deepcopy(self.queue);changed['items'][0]['claim']={'claim_id':'possibly-published'}
        q.write_text(json.dumps(changed));commit()
        q.write_text(json.dumps(self.queue));head=commit()
        with self.assertRaisesRegex(entry.lc.Blocked,'claim_item_changed_in_main_history'):
            entry.unchanged_claim_history(root,session,head)

    def abort_fixture(self):
        session=Path(self.tmp.name)/'aborted-session.json'
        session.with_name(session.name+'.busy').write_text(json.dumps({'phase':'claim'}))
        failure=Path(self.tmp.name)/'failure.json'
        failure.write_text(json.dumps({'checks_passed':False,'create_allowed':False,
                                       'reason':'checkout_must_equal_fresh_origin_main'}))
        (self.root/entry.lc.LOCK).write_text(json.dumps({'state':'free'}))
        process={'exited':True,'exit_code':2,'output_complete':True,'phase':'claim',
                 'session_path':str(session.resolve())}
        original=Path(self.tmp.name)/'original-request.json';original.write_text(json.dumps(self.request))
        process['provenance']={'argv_request_path':str(original.resolve()),
            'captured_request_sha256':entry.hashlib.sha256(original.read_bytes()).hexdigest(),
            'runner_record_id':'actual-command-record',
            'execution_instance_id':self.request['actor']['execution_instance_id'],
            'legacy_source_sha256':'76b2b7e15a8394e70ad1338148f50ee03006fc0c89d8ef552a0bfd95e76fca31',
            'marker_absent_before_invocation':True,'marker_created_by_this_invocation':True,
            'no_remaining_orchestrator':True,'argv_phase':'claim','argv_session_path':str(session.resolve()),
            'captured_stdout_sha256':entry.hashlib.sha256(failure.read_bytes()).hexdigest()}
        (self.root/entry.ledger_tools.PATH).write_text(json.dumps({'runs':{}}))
        return session,failure,process

    def abort_report(self, session, failure, process, scan=None):
        return entry.assess_preclaim_abort(self.root,session,failure,process,self.request['actor'],
                   'S-example',scan or self.request['scan'],fixtures.NOW,'a'*40,Path(self.tmp.name)/'original-request.json')

    def test_proven_preclaim_abort_is_only_report_and_preserves_marker(self):
        session,failure,process=self.abort_fixture()
        marker=session.with_name(session.name+'.busy');before=marker.read_bytes()
        report=self.abort_report(session,failure,process)
        self.assertTrue(report['eligible_for_abort_record'])
        self.assertFalse(report['create_allowed'])
        self.assertFalse(report['new_session_allowed_by_this_report'])
        self.assertNotIn(str(session),json.dumps(report))
        self.assertNotIn('process_result',report)
        self.assertEqual(marker.read_bytes(),before)
        self.assertFalse(session.exists())

    def test_abort_assessment_rejects_incomplete_process_or_session_evidence(self):
        session,failure,process=self.abort_fixture()
        for changes in ({'exited':False},{'exit_code':0},{'output_complete':False},
                        {'phase':'verify'},{'session_path':'other'}):
            with self.subTest(changes=changes),self.assertRaises(entry.lc.Blocked):
                self.abort_report(session,failure,dict(process,**changes))
        for suffix in ('','.pending'):
            path=session.with_name(session.name+suffix);path.write_text('{}')
            with self.assertRaises(entry.lc.Blocked):self.abort_report(session,failure,process)
            path.unlink()
        for body in ({'phase':'intent'},{'phase':'verify'}):
            session.with_name(session.name+'.busy').write_text(json.dumps(body))
            with self.assertRaises(entry.lc.Blocked):self.abort_report(session,failure,process)

    def test_abort_assessment_rejects_peer_action_unknown_or_unavailable_scan(self):
        session,failure,process=self.abort_fixture()
        for lock in ({'state':'held','expires_at':'invalid'}, {'state':'held','expires_at':'2000-01-01T00:00:00Z'}, {}):
            (self.root/entry.lc.LOCK).write_text(json.dumps(lock))
            with self.assertRaises(entry.lc.Blocked):self.abort_report(session,failure,process)
        (self.root/entry.lc.LOCK).write_text(json.dumps({'state':'free'}))
        for changes in ({'claim':{'holder':'grok'}},{'state':'submission_unknown'},
                        {'state':'submitted','task_id':'new-task'}):
            changed=copy.deepcopy(self.queue);changed['items'][0].update(changes)
            (self.root/entry.lc.QUEUE).write_text(json.dumps(changed))
            with self.assertRaises(entry.lc.Blocked):self.abort_report(session,failure,process)
        (self.root/entry.lc.QUEUE).write_text(json.dumps(self.queue))
        for changes in ({'complete':False},{'free_slots':0},{'checked_at':'2000-01-01T00:00:00Z'},
                        {'item_reconciliation':{'S-example':{'complete':True,'matched_task_ids':['peer-task'],'ambiguous':False}}}):
            with self.subTest(changes=changes),self.assertRaises(entry.lc.Blocked):
                self.abort_report(session,failure,process,dict(self.request['scan'],**changes))

    def test_abort_assessment_rejects_lost_output_or_possible_transaction(self):
        session,failure,process=self.abort_fixture()
        for body in ({'checks_passed':False,'create_allowed':False,'reason':'other_error'},
                     {'checks_passed':True,'create_allowed':True},
                     {'checks_passed':False,'create_allowed':False,
                      'reason':'checkout_must_equal_fresh_origin_main','files':{}}):
            failure.write_text(json.dumps(body))
            process['provenance']['captured_stdout_sha256']=entry.hashlib.sha256(failure.read_bytes()).hexdigest()
            with self.assertRaisesRegex(entry.lc.Blocked,'captured_pre_step_snapshot_rejection_required'):
                self.abort_report(session,failure,process)

    def test_abort_assessment_fails_closed_on_missing_provenance_history_or_ledger(self):
        session,failure,process=self.abort_fixture()
        for key in process['provenance']:
            changed=copy.deepcopy(process);del changed['provenance'][key]
            with self.subTest(missing=key),self.assertRaises(entry.lc.Blocked):
                self.abort_report(session,failure,changed)
        for key in ('submission_history','archive_file','retry_control'):
            changed=copy.deepcopy(self.queue);changed['items'][0][key]={'prior':'task'}
            (self.root/entry.lc.QUEUE).write_text(json.dumps(changed))
            with self.assertRaises(entry.lc.Blocked):self.abort_report(session,failure,process)
        (self.root/entry.lc.QUEUE).write_text(json.dumps(self.queue))
        ledger=self.root/entry.ledger_tools.PATH
        ledger.write_text(json.dumps({'runs':{'old':{'item_id':'S-example','consumed':True}}}))
        with self.assertRaises(entry.lc.Blocked):self.abort_report(session,failure,process)
        ledger.unlink()
        with self.assertRaises(entry.lc.Blocked):self.abort_report(session,failure,process)

    def test_abort_requires_original_item_and_actor_not_another_ready_item(self):
        session,failure,process=self.abort_fixture()
        original=Path(self.tmp.name)/'original-request.json'
        for changes in ({'item_id':'another-item'},{'actor':dict(self.request['actor'],execution_instance_id=fixtures.B)}):
            changed=copy.deepcopy(self.request);changed.update(changes);original.write_text(json.dumps(changed))
            process['provenance']['captured_request_sha256']=entry.hashlib.sha256(original.read_bytes()).hexdigest()
            with self.assertRaisesRegex(entry.lc.Blocked,'original_request_actor_and_item_required'):
                self.abort_report(session,failure,process)

    def test_delayed_final_fetch_cannot_authorize_expired_lease(self):
        import shutil
        from datetime import timedelta
        _,session=self.intent()
        request_path=Path(self.tmp.name)/'request.json';request_path.write_text(json.dumps(self.request))
        session_path=Path(self.tmp.name)/'session.json';session_path.write_text(json.dumps(session))
        clock={'now':fixtures.NOW,'fetches':0}
        def fetched(root):
            clock['fetches']+=1
            if clock['fetches']==2:clock['now']+=timedelta(minutes=10)
            return 'a'*40
        def materialized(root,sha,destination):shutil.copytree(root,destination,dirs_exist_ok=True)
        output=io.StringIO()
        argv=['launcher_entry.py',str(self.root),'verify','--request',str(request_path),'--session',str(session_path)]
        with patch.object(sys,'argv',argv),patch.object(entry,'snapshot',side_effect=fetched), \
             patch.object(entry,'materialize_snapshot',side_effect=materialized), \
             patch.object(entry,'datetime') as dt,patch('sys.stdout',output):
            dt.now.side_effect=lambda tz:clock['now']
            self.assertEqual(entry.main(),2)
        self.assertFalse(json.loads(output.getvalue())['create_allowed'])
        self.assertEqual(json.loads(session_path.read_text())['phase'],'intent_prepared')

    def test_snapshot_rejects_local_unpublished_commit_and_dirty_tree(self):
        for responses in [['','a'*40,'b'*40],['','a'*40,'a'*40,' M ops/topview-launch-queue.json']]:
            with patch.object(entry.subprocess,'check_output',side_effect=responses):
                with self.assertRaises(entry.lc.Blocked):entry.snapshot(self.root)

if __name__=='__main__':unittest.main()

class GitSnapshotTests(unittest.TestCase):
    def test_hidden_local_changes_do_not_become_readback(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'repo';root.mkdir();isolated=Path(d)/'snapshot';isolated.mkdir()
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL,text=True).strip()
            git('init');git('config','user.email','test@example.com');git('config','user.name','test')
            (root/'ops').mkdir()
            for path,value in [(entry.lc.CONFIG,{}),(entry.lc.LOCK,{}),(entry.lc.QUEUE,{'items':[]})]:
                (root/path).write_text(json.dumps(value))
            git('add','.');git('commit','-m','snapshot');sha=git('rev-parse','HEAD')
            git('update-index','--assume-unchanged',entry.lc.QUEUE)
            (root/entry.lc.QUEUE).write_text(json.dumps({'items':[{'id':'unpublished'}]}))
            self.assertEqual(git('status','--porcelain'),'')
            entry.materialize_snapshot(root,sha,isolated)
            self.assertEqual(json.loads((isolated/entry.lc.QUEUE).read_text()),{'items':[]})
            # Later mutable checkout changes also cannot alter the guard snapshot.
            (root/entry.lc.QUEUE).write_text('{}')
            self.assertEqual(json.loads((isolated/entry.lc.QUEUE).read_text()),{'items':[]})
