"""Execute the production shell control flow with fake git/Python, never network."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/site_alert_publish.sh'


class PublishTests(unittest.TestCase):
    def run_flow(self, mode):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            driver = root / 'driver.py'
            driver.write_text('''#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
p=Path(os.environ['STATE'])
s=json.loads(p.read_text()) if p.exists() else {'pushes':0,'sends':0,'published':False,'log':[]}
cmd=Path(sys.argv[0]).name
args=sys.argv[1:]
s['log'].append([cmd]+args)
code=0
mode=os.environ['MODE']
if cmd=='git':
 if args[0]=='fetch' and mode=='fetch_fail':code=1
 if args[0]=='reset' and mode=='reset_fail':code=1
 if args[0]=='status':print(' M ops/site-alert-state.json')
 if args[0]=='push':
  s['pushes']+=1
  code=int(mode=='all_reject' or (mode=='first_reject' and s['pushes']==1))
  if not code:s['published']=True
elif '--prepare' in args:s['published']=False
elif '--notify' in args:
 if not s['published']:code=90
 else:s['sends']+=1
p.write_text(json.dumps(s))
sys.exit(code)
''')
            driver.chmod(0o755)
            for command in ('git', 'python3'):
                # Use real interpreter explicitly; PATH python3 is the test shim.
                (root / command).write_text('#!/bin/sh\nexec ' + os.sys.executable + ' ' + str(driver) + ' "$@"\n')
                (root / command).chmod(0o755)
            # driver must distinguish git/python3, so pass it via env from wrappers.
            text=driver.read_text().replace("cmd=Path(sys.argv[0]).name", "cmd=os.environ['TEST_COMMAND']")
            driver.write_text(text)
            for command in ('git','python3'):
                (root/command).write_text('#!/bin/sh\nTEST_COMMAND='+command+' exec '+os.sys.executable+' '+str(driver)+' "$@"\n')
            env=dict(os.environ, PATH=str(root)+os.pathsep+os.environ['PATH'], MODE=mode, STATE=str(root/'state.json'), BRANCH='main')
            result=subprocess.run(['bash',str(SCRIPT)],cwd=root,env=env,capture_output=True,text=True)
            return result, json.loads((root/'state.json').read_text())

    def test_prepare_is_published_before_only_send(self):
        result, state=self.run_flow('ok')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(state['sends'],1)
        self.assertEqual(state['pushes'],2)

    def test_rejected_prepare_recomputes_without_sending(self):
        result,state=self.run_flow('first_reject')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(state['sends'],1)
        self.assertEqual(state['pushes'],3)

    def test_fetch_or_reset_failure_stops_without_send(self):
        for mode in ('fetch_fail','reset_fail'):
            with self.subTest(mode=mode):
                result,state=self.run_flow(mode)
                self.assertNotEqual(result.returncode,0)
                self.assertEqual(state['sends'],0)

    def test_exhausted_cas_is_visible_failure_and_never_sends(self):
        result,state=self.run_flow('all_reject')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(state['pushes'],4)
        self.assertEqual(state['sends'],0)
