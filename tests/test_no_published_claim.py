import sys,unittest,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import no_published_claim as n
class InvariantTests(unittest.TestCase):
 def setUp(self): self.item={'id':'D','state':'waiting_for_slot'}
 def test_waiting_passes(self): n.check_snapshot(self.item,'a'*64)
 def test_hold_passes(self): n.check_snapshot(dict(self.item,state='blocked_recovery'),'a'*64)
 def test_expected_payload_rejected_even_without_claim(self):
  with self.assertRaises(n.EvidenceError):n.check_snapshot(self.item,n.digest(self.item))
 def test_claim_task_intent_rejected(self):
  for k in ['claim','task_id','task_ids','submission_intent_id']:
   with self.subTest(k=k),self.assertRaises(n.EvidenceError):n.check_snapshot(dict(self.item,**{k:'x'}),'a'*64)
 def test_other_states_rejected(self):
  for s in ['submitted','claimed','submitting','submission_unknown','failed','cancelled_owner']:
   with self.subTest(s=s),self.assertRaises(n.EvidenceError):n.check_snapshot(dict(self.item,state=s),'a'*64)
 def test_prior_attempt_not_reset(self):
  for k in ['submission_history','create_click_count','max_new_submissions_consumed','retry_control','submission_attempts','archived_attempts']:
   with self.subTest(k=k),self.assertRaises(n.EvidenceError):n.check_snapshot(dict(self.item,**{k:1}),'a'*64)
 def test_no_mutation(self):
  before=copy.deepcopy(self.item);n.check_snapshot(self.item,'a'*64);self.assertEqual(before,self.item)

import tempfile,json,subprocess,hashlib
from unittest.mock import patch
class GitHistoryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.git('init','-q');self.git('config','user.email','fixture@example.test');self.git('config','user.name','Fixture')
  (self.root/'scripts').mkdir();(self.root/'scripts/launcher_entry.py').write_text('fixture reviewed source')
  (self.root/'ops').mkdir();self.item={'id':'D','state':'waiting_for_slot'};self.base=self.commit(self.item)
  self.claim=dict(self.item,state='claimed',claim={'claim_id':'C'})
  self.session={'schema_version':1,'phase':'claim_prepared','item_id':'D','claim_id':'C','expected_item_sha':n.digest(self.claim)}
  self.prepared={'phase':'claim','create_allowed':False,'expected_main_sha':self.base,'files':{n.QUEUE:{'items':[self.claim]}}}
  self.source=hashlib.sha256(b'fixture reviewed source').hexdigest()
 def tearDown(self):self.tmp.cleanup()
 def git(self,*args):return subprocess.check_output(['git','-C',str(self.root),*args],stderr=subprocess.PIPE).decode().strip()
 def commit(self,item):
  (self.root/n.QUEUE).write_text(json.dumps({'items':[item]}));self.git('add','.');self.git('commit','-qm','fixture');return self.git('rev-parse','HEAD')
 def check(self,end):
  with patch.object(n,'SOURCE_SHA',self.source):return n.assess(self.root,self.session,self.prepared,end)
 def test_historical_report_never_grants_create(self):
  end=self.commit(dict(self.item,state='blocked_recovery'));r=self.check(end)
  self.assertEqual(r['commit_count'],2);self.assertIsNone(r['python_exit_code_observed']);self.assertFalse(r['create_allowed']);self.assertFalse(r['new_session_allowed_by_this_report'])
 def test_published_then_reverted_rejected(self):
  self.commit(self.claim);end=self.commit(self.item)
  with self.assertRaises(n.EvidenceError):self.check(end)
 def test_unknown_then_reverted_rejected(self):
  self.commit(dict(self.item,state='submission_unknown'));end=self.commit(self.item)
  with self.assertRaises(n.EvidenceError):self.check(end)
 def test_wrong_source_rejected(self):
  with self.assertRaises(n.EvidenceError):n.assess(self.root,self.session,self.prepared,self.base)
 def test_wrong_payload_rejected(self):
  self.session['expected_item_sha']='a'*64
  with self.assertRaises(n.EvidenceError):self.check(self.base)
 def test_changed_phase_rejected(self):
  self.session['phase']='intent_prepared'
  with self.assertRaises(n.EvidenceError):self.check(self.base)
 def test_missing_duplicate_and_archived_duplicate_rejected(self):
  for q in ({'items':[]},{'items':[self.item,self.item]},{'items':[self.item],'archived_items':[self.item]}):
   (self.root/n.QUEUE).write_text(json.dumps(q));self.git('add','.');self.git('commit','-qm','bad fixture');end=self.git('rev-parse','HEAD')
   with self.assertRaises(n.EvidenceError):self.check(end)
 def test_bad_fullsha_rejected(self):
  with self.assertRaises(n.EvidenceError):self.check('HEAD')
 def test_nonancestor_rejected(self):
  end=self.commit(dict(self.item,state='blocked_recovery'));self.prepared['expected_main_sha']=end
  with self.assertRaises(subprocess.CalledProcessError):self.check(self.base)
 def test_shallow_inside_range_rejected(self):
  end=self.commit(dict(self.item,state='blocked_recovery'));(self.root/'.git/shallow').write_text(end+'\n')
  with self.assertRaises((n.EvidenceError,subprocess.CalledProcessError)):self.check(end)
 def test_shallow_before_base_allowed(self):
  parent=self.base;self.base=self.commit(dict(self.item,recovery_note='not_an_attempt'));self.prepared['expected_main_sha']=self.base
  end=self.commit(dict(self.item,state='blocked_recovery'));(self.root/'.git/shallow').write_text(parent+'\n')
  self.assertEqual(self.check(end)['commit_count'],2)
 def test_claim_id_binding_rejected(self):
  self.session['claim_id']='wrong'
  with self.assertRaises(n.EvidenceError):self.check(self.base)
if __name__=='__main__':unittest.main()
