#!/usr/bin/env python3
"""Canonical history archival only, with exact lease and preserved recovery."""
import copy, hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'scripts'))
from trim_service_files import trim_register, REGISTER_ARCHIVE
from resume_state import verify_recovery,select_work
from build_resume_packet import write as packet_write
HOLDER='chatgpt:ordinary:c1dec76d-aeb0-485b-a474-4112f8727b2c'
ACQUIRED='2026-11-08T06:24:53Z'
REPORT='reports/register-archive-2026-11-08.json'
def now():return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(p,x):
    (ROOT/p).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def owned():
    x=read('ops/canon-lock.json');return x.get('holder')==HOLDER and x.get('acquired_at')==ACQUIRED and x.get('state')=='held'
def guard():
    assert owned(),'Foreign lease'
    assert datetime.fromisoformat(read('ops/canon-lock.json')['expires_at'].replace('Z','+00:00'))>datetime.now(timezone.utc),'Expired lease'
    x=read('ops/slot-backup.json');f=x['foreground_owners']['ordinary']
    assert x['route_generation']==3 and f['epoch']==4 and f['session_id']=='chatgpt-ordinary-continue-20261107-4aa338af-9488-4a37-a1c3-60993ed108ec','Foreground changed'
def release():
    if owned():
        x=read('ops/canon-lock.json');x.update(state='free',expires_at=None,released_at=now());save('ops/canon-lock.json',x)
if sys.argv[1]=='release':release();raise SystemExit(0)
guard()
assert not (ROOT/REPORT).exists(),'Existing archive receipt: inspect rather than rerun'
raw=(ROOT/'work-resume-register.json').read_bytes();reg=read('work-resume-register.json')
recovery=copy.deepcopy(select_work(reg,project='seregius')['recovery']);focus=copy.deepcopy(reg['resume_focus'])
protected=['ops/topview-launch-queue.json','video-prompts.md','monitor-role.json','ops/slot-backup.json']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in protected}
archive=read(REGISTER_ARCHIVE) if (ROOT/REGISTER_ARCHIVE).exists() else {}
result=trim_register(reg,archive)
assert result,'Nothing to archive; fresh-read before changes'
new_reg,new_archive,moved_done,moved_groups=result
save(REGISTER_ARCHIVE,new_archive);save('work-resume-register.json',new_reg)
assert new_reg['resume_focus']==focus
assert select_work(new_reg,project='seregius')['recovery']==recovery
assert not verify_recovery(ROOT,new_reg,project='seregius')['reasons']
size=(ROOT/'work-resume-register.json').stat().st_size
assert size<100000,'Register still exceeds safe size'
checks=[]
for cmd in [['python3','-m','unittest','-v','tests.test_trim_service_files','tests.test_continue_recovery'],['python3','scripts/validate_site.py','.'],['python3','scripts/canon_health.py','.','--write']]:
    p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);print(p.stdout)
    checks.append({'command':cmd,'exit_code':p.returncode,'output_tail':p.stdout[-1000:]})
    assert p.returncode==0,'Validation failed'
health=read('canon-health.json')
assert health['warnings']==0,'Other warning remains; do not claim healthy'
report={'schema_version':1,'project':'seregius','holder':HOLDER,'checked_at':now(),'before_bytes':len(raw),'after_bytes':size,'finished_work_moved':moved_done,'archived_entry_groups':moved_groups,'archive':REGISTER_ARCHIVE,'recovery_unchanged':True,'queue_unchanged':True,'validation':checks,'canon_health':{'status':health['status'],'warnings':health['warnings'],'checked_at':health['checked_at']}}
save(REPORT,report)
plans=(ROOT/'ops/FUTURE-PLANS.md').read_text(encoding='utf-8').splitlines()
ix=[i for i,s in enumerate(plans) if s.startswith('| A-17 |')];assert len(ix)==1
cells=plans[ix[0]].split('|');assert len(cells)==6
cells[3]=f' СДЕЛАНО: 08.11 штатный trim_register перенёс старые выполненные записи в архив, {len(raw)} → {size} байт; текущая recovery/очередь сохранены. canon-health status=ok, warnings=0; доказательство {REPORT}. Регулярное обслуживание остаётся. '
plans[ix[0]]='|'.join(cells)
(ROOT/'ops/FUTURE-PLANS.md').write_text('\n'.join(plans)+'\n',encoding='utf-8')
packet=packet_write(ROOT,project='seregius');assert packet['ready_for_resume'] and not packet['reasons']
for p,h in hashes.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,'Protected source changed'
guard();release()
for p in ['scripts/archive_register_once.py','.github/workflows/archive-register-once.yml']:(ROOT/p).unlink(missing_ok=True)
print(json.dumps(report,ensure_ascii=False,indent=2))
