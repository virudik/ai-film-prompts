import copy
import json
import subprocess
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import unittest
from tests import test_continue_recovery as fixture
import build_resume_packet as packet
import continue_preflight as preflight
import resume_state as state
import handoff_receipt as receipts


class ProjectRecoveryTests(unittest.TestCase):
    put = fixture.ContinueRecoveryTests.put
    js = fixture.ContinueRecoveryTests.js
    read = fixture.ContinueRecoveryTests.read
    mutate_register = fixture.ContinueRecoveryTests.mutate_register

    def setUp(self):
        fixture.ContinueRecoveryTests.setUp(self)
        self.pid = 'other'
        self.prefix = 'projects/other/'
        ctx = {'id': self.pid, 'name': 'Other', 'root': self.prefix.rstrip('/')}
        ctx.update({key: self.prefix + value for key, value in {
            'handoff': 'HANDOFF.md', 'instructions': 'INSTRUCTIONS.md', 'master': 'video-prompts.md',
            'status': 'project-status.json', 'queue': state.QUEUE, 'lock': 'canon-lock.json'}.items()})
        self.js('projects/projects.json', {'projects': [ctx]})
        self.put('projects/README.md', b'shared project rules')
        for p in ('HANDOFF.md', 'INSTRUCTIONS.md', 'video-prompts.md'):
            self.put(self.prefix + p, b'other project evidence')
        self.js(ctx['status'], {'health':'ok', 'canonical_master_sha256':state.digest(b'other project evidence')})
        self.js(ctx['queue'], {'items':[{'id':'p','state':'paused_by_owner'}]})
        self.js(self.prefix + state.REGISTER, {'schema_version':1,'project':self.pid,'active_work':[],
            'idle_state':{'work_id':'IDLE-OTHER','status':'waiting_for_owner'},
            'resume_focus':{'project':self.pid,'work_id':'IDLE-OTHER'}})
        self.put(self.prefix + state.CHECKPOINT, b'# Other stage\nwork_id: IDLE-OTHER\nWaiting for owner.\n')
        state.capture(self.root,'IDLE-OTHER','# Other stage','Saved project','Wait for owner',
            [ctx['handoff']],project=self.pid)

    def test_project_uses_own_focus_and_idle(self):
        r=preflight.evaluate(self.root,project=self.pid)
        self.assertTrue(r['ready_for_resume'],r['reasons'])
        self.assertEqual(r['selected_work']['work_id'],'IDLE-OTHER')
        self.assertIn(self.prefix+'HANDOFF.md',r['read'])
        self.assertIn('--project other',packet.markdown(packet.build(self.root,project=self.pid)))
        p=packet.build(self.root,project=self.pid)
        self.assertFalse(p['execution_authorized'])
        self.assertEqual(p['queue_recovery']['next_candidates'],[])
        self.assertIn(self.prefix+'HANDOFF.md',[s['file'] for s in p['sources']])

    def test_other_project_does_not_require_root_focus(self):
        self.mutate_register(lambda j:j.pop('resume_focus'))
        self.assertTrue(preflight.evaluate(self.root,project=self.pid)['ready_for_resume'])

    def test_unknown_project_fails_closed(self):
        self.assertFalse(preflight.evaluate(self.root,project='missing')['ready_for_resume'])

    def test_cross_project_checkpoint_rejected(self):
        reg=self.read(self.prefix+state.REGISTER)
        reg['idle_state']['recovery']['checkpoint']['file']=state.CHECKPOINT
        self.js(self.prefix+state.REGISTER,reg)
        self.assertFalse(preflight.evaluate(self.root,project=self.pid)['ready_for_resume'])

    def test_cross_project_focus_rejected(self):
        reg=self.read(self.prefix+state.REGISTER);reg['resume_focus']['project']='seregius'
        self.js(self.prefix+state.REGISTER,reg)
        self.assertFalse(preflight.evaluate(self.root,project=self.pid)['ready_for_resume'])

    def test_copied_foreign_entry_and_queue_rejected(self):
        reg=self.read(self.prefix+state.REGISTER)
        reg['idle_state']['project']='seregius'
        self.js(self.prefix+state.REGISTER,reg)
        self.assertFalse(preflight.evaluate(self.root,project=self.pid)['ready_for_resume'])
        reg['idle_state']['project']=self.pid
        self.js(self.prefix+state.REGISTER,reg)
        self.js(self.prefix+state.QUEUE,{'project':'seregius','items':[]})
        self.assertFalse(packet.build(self.root,project=self.pid)['ready_for_resume'])

    def test_changed_project_master_invalidates(self):
        self.put(self.prefix+'video-prompts.md',b'changed')
        self.assertFalse(preflight.evaluate(self.root,project=self.pid)['ready_for_resume'])

    def test_idle_never_hides_unfinished_work(self):
        reg=self.read(self.prefix+state.REGISTER);reg['active_work']=[{'work_id':'NEW','status':'in_progress'}]
        self.js(self.prefix+state.REGISTER,reg)
        self.assertFalse(preflight.evaluate(self.root,project=self.pid)['ready_for_resume'])

    def test_project_packet_noop(self):
        a=packet.write(self.root,project=self.pid)
        b=packet.write(self.root,project=self.pid)
        self.assertEqual(a,b)
        self.assertTrue((self.root/self.prefix/'shadow/resume-packet.json').exists())

    def test_cleanup_keeps_idle_checkpoint(self):
        from trim_service_files import run
        cp=self.root/self.prefix/state.CHECKPOINT
        cp.write_bytes((''.join('# Monitor %d\nChecked.\n\n---\n\n'%i for i in range(8))).encode()+cp.read_bytes())
        run(self.root,write=True)
        self.assertIn('# Other stage',cp.read_text())
        self.assertTrue(preflight.evaluate(self.root,project=self.pid)['ready_for_resume'])

    def receipt(self):
        now=datetime.now(timezone.utc); earlier=(now-timedelta(seconds=1)).isoformat()
        self.js(self.prefix+'canon-lock.json', {'state':'held','holder':'chatgpt','expires_at':(now+timedelta(hours=1)).isoformat()})
        return {'schema_version':1,'project':self.pid,'receipt_id':'receipt-0001','work_id':'IDLE-OTHER',
            'source_head':'a'*40,'started_at':earlier,'accepted_at':now.isoformat(),'outcome':'waiting_for_owner',
            'chat':{'agent':'chatgpt','label':'Test receiving chat','session_id':'test-session','chat_id':None,'identity_status':'unavailable'},
            'checks':[{'id':k,'result':'passed','evidence':'fixture observation'} for k in sorted(receipts.CHECKS)],
            'first_action':{'at':earlier,'state':'waiting','description':'Preserved owner pause','evidence':'project handoff'}}

    def record(self,r):
        with patch.object(subprocess,'check_output',return_value=b'a'*40):
            return receipts.record(self.root,r,project=self.pid)

    def test_receipt_idempotent_and_no_fake_identity(self):
        r=self.receipt();a=self.record(r);b=self.record(r)
        self.assertEqual(a,b)
        self.assertEqual(a['chat']['identity_status'],'unavailable')
        self.assertFalse(a['execution_authorized'])
        self.assertEqual(len(self.read(self.prefix+'reports/handoff-receipts.json')['receipts']),1)
        self.assertEqual(packet.build(self.root,project=self.pid)['handoff_receipt']['receipt_id'],r['receipt_id'])

    def test_receipt_conflict_rejected(self):
        r=self.receipt();self.record(r);r['first_action']['description']='different'
        with self.assertRaisesRegex(ValueError,'conflict'):self.record(r)

    def test_receipt_cannot_accept_blocked_checks(self):
        r=self.receipt();r['checks'][0]['result']='blocked'
        with self.assertRaisesRegex(ValueError,'blocked'):self.record(r)

    def test_receipt_requires_real_first_action(self):
        r=self.receipt();r['first_action']['state']='planned'
        with self.assertRaisesRegex(ValueError,'first action'):self.record(r)

    def test_receipt_requires_own_lock(self):
        r=self.receipt();self.js(self.prefix+'canon-lock.json',{'state':'free'})
        with self.assertRaisesRegex(ValueError,'lock'):self.record(r)

    def test_receipt_cannot_mix_work_or_head(self):
        for field,value in [('work_id','WORK-1'),('source_head','b'*40)]:
            r=self.receipt();r[field]=value
            with self.assertRaises(ValueError):self.record(r)

    def test_receipt_archives_and_retries_old_id(self):
        r=self.receipt()
        first=copy.deepcopy(r)
        for i in range(23):
            r['receipt_id']='receipt-%04d'%i
            if i==0:first=copy.deepcopy(r)
            self.record(r)
        live=self.read(self.prefix+'reports/handoff-receipts.json')['receipts']
        old=self.read(self.prefix+'archive/reports/handoff-receipts.json')['receipts']
        self.assertEqual((len(live),len(old)),(20,3))
        self.record(first)
        self.assertEqual(self.read(self.prefix+'reports/handoff-receipts.json')['receipts'],live)
