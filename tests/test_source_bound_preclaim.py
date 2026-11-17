import importlib.util,json,tempfile,subprocess,sys,pathlib,unittest,os
REPO=pathlib.Path(__file__).resolve().parents[1]
class SourceBoundSemantics(unittest.TestCase):
 def test_foreground_shell_zero_does_not_erase_proven_pre_step_abort(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d);(d/'repo').mkdir();(d/'request.json').write_text('{}')
   legacy=d/'legacy.py'
   r_source=subprocess.run(['git','-C',str(REPO),'show','66e10dff8ba6a23ad6cf8bc02dc0a36b77b26265:scripts/launcher_entry.py'],capture_output=True)
   if r_source.returncode: self.skipTest('historical source object unavailable in shallow checkout')
   import hashlib
   self.assertEqual(hashlib.sha256(r_source.stdout).hexdigest(),'76b2b7e15a8394e70ad1338148f50ee03006fc0c89d8ef552a0bfd95e76fca31')
   legacy.write_bytes(r_source.stdout)
   wrapper=d/'invoke.py'
   wrapper.write_text("import sys,importlib.util\nsys.path.insert(0,"+repr(str(REPO/'scripts'))+")\ns=importlib.util.spec_from_file_location('legacy',"+repr(str(legacy))+");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\ndef fail(root): raise m.lc.Blocked('checkout_must_equal_fresh_origin_main')\ndef forbidden(*a,**k): raise AssertionError('step reached')\nm.snapshot=fail;m.step=forbidden\nraise SystemExit(m.main())\n")
   command=f'{sys.executable} {wrapper} {d}/repo claim --request {d}/request.json --session {d}/session.json > {d}/stdout.json; head -c 800 {d}/stdout.json'
   r=subprocess.run(command,shell=True,capture_output=True,text=True)
   self.assertEqual(r.returncode,0)
   expected={'checks_passed':False,'create_allowed':False,'reason':'checkout_must_equal_fresh_origin_main'}
   self.assertEqual(json.loads(r.stdout),expected)
   self.assertEqual(json.loads((d/'session.json.busy').read_text()),{'phase':'claim'})
   self.assertFalse((d/'session.json').exists())
   r2=subprocess.run(command,shell=True,capture_output=True,text=True)
   self.assertEqual(r2.returncode,0)
   self.assertIn('File exists',json.loads(r2.stdout)['reason'])
   self.assertFalse((d/'session.json').exists())
 def test_published_assessment_never_claims_strict_or_launch_authority(self):
  report=json.loads((REPO/'reports/preclaim-aborts/event770-source-assessment.json').read_text())
  self.assertEqual(report['observed']['shell_exit_code'],0)
  self.assertIsNone(report['observed']['python_exit_code'])
  self.assertFalse(report['strict_exit2_assessment_passed'])
  self.assertFalse(report['fresh_remote_and_live_reconciliation_complete'])
  self.assertFalse(report['new_session_allowed_by_this_report'])
  self.assertFalse(report['create_allowed'])
  self.assertNotIn('/tmp/',json.dumps(report))
if __name__=='__main__':unittest.main()
