import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import apply_launcher_policy as ap

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for path in ['ops','reports','.github/workflows']: (self.root/path).mkdir(parents=True,exist_ok=True)
        self.req={'request_id':'test','lease_holder':'unique-holder','lease_acquired_at':'2026-01-01T00:00:00Z',
                  'expected_route_generation':1,'interactive_session_id':'current-interactive',
                  'owner_reported_at':'2026-10-31T16:30:00Z','action':'ordinary-primary-after-owner-work-limit'}
        ap.jwrite(self.root,'ops/canon-lock.json',{'state':'held','holder':'unique-holder',
                   'acquired_at':self.req['lease_acquired_at'],
                   'expires_at':(datetime.now(timezone.utc)+timedelta(minutes=20)).isoformat()})
        for path in ap.DOCS:
            data='\ufeff# Title\r\n\r\nOld content remains.\r\n'
            if path=='NEW-CHAT-HANDOFF.md':
                data='# Handoff\n\n## СЕЙЧАС (обновлено 30.10.2026)\n\n### Новое с последней чистки (дописывать сюда, одной строкой с датой)\n\nOld decision.\n'
            (self.root/path).write_bytes(data.encode())
        for path in ['ops/CONTINUE-PROTOCOL.md','ops/CANON-LOCK.md','ops/TOPVIEW-EVENT-WAKE.md','ops/TOPVIEW-FREE-LAUNCH.md']:
            (self.root/path).write_text('# Original title\n\nExisting rules.\n')
        (self.root/'reports/current-work-checkpoint.md').write_text('# Previous checkpoint\n\nKeep evidence.\n')
        ap.jwrite(self.root,'work-resume-register.json',{'active_work':[{'work_id':ap.WORK,'canonical_refs':[],'recovery':{'old':True}}, {'work_id':'unrelated','value':42}]})
        ap.jwrite(self.root,'ops/slot-backup.json',{'enabled':True,'route_generation':1,'active_automation_id':'ordinary',
                     'ownership':{},'chat_replacement':{},'rules':['old-rule'],'unknown_retained':42})
        for path in ['video-prompts.md','ops/topview-launch-queue.json','monitor-role.json']: (self.root/path).write_text('protected '+path)
        (self.root/'.github/workflows/test-recovery-integration.yml').write_text("paths:\n      - 'tests/test_recovery_integration.py'\nrun: python3 -m unittest -v tests/test_recovery_integration.py\n")
    def test_apply_preserves_source_bytes_and_protected_files(self):
        protected={p:(self.root/p).read_bytes() for p in ['video-prompts.md','ops/topview-launch-queue.json','monitor-role.json']}
        ap.apply(self.root,self.req)
        cfg=ap.jread(self.root,'ops/slot-backup.json')
        self.assertEqual((cfg['preferred_executor'],cfg['route_generation'],cfg['unknown_retained']),('ordinary',2,42))
        for p,b in protected.items(): self.assertEqual((self.root/p).read_bytes(),b)
        for p in ap.DOCS[1:]:
            b=(self.root/p).read_bytes()
            self.assertTrue(b.startswith(b'\xef\xbb\xbf'))
            self.assertNotIn(b'\n',b.replace(b'\r\n',b''))
            self.assertIn(b'Old content remains.',b)
        self.assertEqual(ap.jread(self.root,'work-resume-register.json')['active_work'][1],{'work_id':'unrelated','value':42})
    def test_apply_repeat_is_idempotent(self):
        ap.apply(self.root,self.req)
        before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        ap.apply(self.root,self.req)
        after={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after)
    def test_changed_route_blocks(self):
        cfg=ap.jread(self.root,'ops/slot-backup.json'); cfg['route_generation']=99
        ap.jwrite(self.root,'ops/slot-backup.json',cfg)
        with self.assertRaises(RuntimeError):ap.apply(self.root,self.req)
    def test_foreign_lock_blocks(self):
        lock=ap.jread(self.root,'ops/canon-lock.json');lock['holder']='other'
        ap.jwrite(self.root,'ops/canon-lock.json',lock)
        with self.assertRaises(RuntimeError):ap.apply(self.root,self.req)
        with self.assertRaises(RuntimeError):ap.release(self.root,self.req)
    def test_checkpoint_updates_one_block_without_losing_history(self):
        for phase in ['planned','installed','tested']:ap.checkpoint(self.root,self.req,phase)
        text=(self.root/'reports/current-work-checkpoint.md').read_text()
        self.assertEqual(text.count('<!-- launcher-policy:test -->'),1)
        self.assertEqual(text.count('---'),1)
        self.assertIn('Previous checkpoint',text)
        w=ap.jread(self.root,'work-resume-register.json')['active_work'][0]
        self.assertEqual(len(w['recovery_history']),1)
        self.assertEqual(w['recovery']['checkpoint']['sha256'],ap.sha(self.root/'reports/current-work-checkpoint.md'))

if __name__=='__main__':unittest.main()
