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
