#!/usr/bin/env python3
"""Verify existing HONOR references; never generate media or change approval/queues."""
import concurrent.futures, hashlib, json, os, re, subprocess, sys, time, urllib.parse, urllib.request, zipfile
from datetime import datetime, timezone
from pathlib import Path
P=Path('projects/raznoe'); E=Path('/tmp/honor-reference-delivery'); E.mkdir(exist_ok=True)
HOLDER=os.environ['HOLDER']; LOCKS=[Path('ops/canon-lock.json'),P/'canon-lock.json']
def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def shab(b): return hashlib.sha256(b).hexdigest()
def sha(p): return shab(Path(p).read_bytes())
def load(p): return json.loads(Path(p).read_text())
def dump(p,o): Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def lease():
    for p in LOCKS:
        l=load(p)
        assert l['state']=='held' and l['holder']==HOLDER, f'Lease changed: {p}'
        assert datetime.fromisoformat(l['expires_at'].replace('Z','+00:00'))>datetime.now(timezone.utc), f'Expired: {p}'
def run(name,args):
    r=subprocess.run(args,capture_output=True,text=True); text=r.stdout+r.stderr
    (E/(name+'.log')).write_text(text)
    assert r.returncode==0,(name,text[-9000:])
    return text
lease();head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
run('preflight-before',['python3','scripts/continue_preflight.py','.','--project','raznoe'])
runtime={}
for name in ['project-status.json','topview-status.json','instruction-sync-status.json','automation-monitor-status.json','monitor-role.json','ops/owner-tasks.json','projects/raznoe/project-status.json','projects/raznoe/work-resume-register.json']:
    d=load(name);runtime[name]={'sha256':sha(name),'checked_at':d.get('checked_at'),'health':d.get('health'),'status':d.get('status')}
dump(E/'runtime-read.json',runtime)
report_path=P/'reports/honor-reference-integration.json';r=load(report_path)
assert r['canonical_integration_complete'] and len(r['assets'])==6
master_path=P/'video-prompts.md';master=master_path.read_text()
assert sha(master_path)==r['master_sha256'],'Master changed since integration; re-review required'
sys.path.insert(0,str(Path('scripts').resolve()))
import topview_prompt_match as pm
from resume_state import capture
all_blocks=pm.master_blocks(master);assert len(dict(all_blocks))==len(all_blocks),'Duplicate prompt labels'
blocks=dict(all_blocks);expected={str(master_path):sha(master_path),str(P/'character-references.json'):sha(P/'character-references.json')};binding_results=[]
for sid,model,count,foreign in [(4,'HONOR Magic9 Pro Max',36,'HONOR X9e Pro'),(5,'HONOR X9e Pro',3,'HONOR Magic9 Pro Max')]:
    base=P/f'references/scenes/scene-{sid}';b=load(base/'reference-bindings.json')
    assert b['model']==model and b['official_sources_are_primary'] and len(b['prompts'])==count
    starts=list(re.finditer(r'<a id="scene-(\d+)"></a>',master));i=next(i for i,m in enumerate(starts) if int(m.group(1))==sid)
    section=master[starts[i].start():starts[i+1].start() if i+1<len(starts) else len(master)]
    wrong_prefix='/scene-5/X-GEN-' if sid==4 else '/scene-4/H-GEN-'
    assert wrong_prefix not in section,f'Foreign model gallery in scene {sid}'
    for item in b['prompts']:
        body=blocks[item['label']]
        assert item['prompt_sha256'] in (shab(body.encode()),shab(body.strip().encode())),item['label']
        assert model in body and foreign not in body,item['label']
        for token in ['@Image1','@Image2']:
            src=item['inputs'][token]
            assert src['kind']=='official_source_not_generated' and src.get('drive_id') and src.get('sha256') and token in body
        for inp in item['inputs'].values():
            if 'path' in inp:
                assert Path(inp['path']).is_file(),inp['path']
                assert 'H-GEN-PAIR' not in inp['path'] and 'X-GEN-MOSCOW' not in inp['path']
        binding_results.append({'scene':sid,'label':item['label'],'model':model,'prompt_sha256':item['prompt_sha256'],'verified':True})
    filenames=['manifest.json','reference-bindings.json','official-product-source-links.json']
    filenames+=['production-package.md','product-compositing.json'] if sid==4 else ['shooting-package.md']
    for f in filenames:
        path=base/f;expected[str(path)]=sha(path)
for a in r['assets']:
    for key,hkey in [('path','sha256'),('preview','preview_sha256')]:
        assert sha(a[key])==a[hkey],a[key]
        expected[a[key]]=a[hkey]
for name in ['01-honor-realism.png','02-honor-3d.png','03-honor-drawn.png']:
    path=P/'references/scenes/scene-4'/name;expected[str(path)]=sha(path)
assert len(binding_results)==39
protected=dict(expected)
for p in ['video-prompts.md','review-ledger.json','ops/topview-launch-queue.json','projects/raznoe/review-ledger.json','projects/raznoe/ops/topview-launch-queue.json','NEW-CHAT-HANDOFF.md','SYNC-RUNBOOK.md','AI-PROJECT-GUIDE.md','PROMPT-STYLE-GUIDE.md','USER-GUIDE.md','README-AI-SYNC.md','BACKUP-AI-RUNBOOK.md']:
    protected[p]=sha(p)
def tests(name):
    text=run(name,['python3','-m','unittest','discover','-s','tests']);m=re.search(r'Ran (\d+) tests? in',text)
    assert m and int(m.group(1))>=550 and not re.search(r'skipped=\d+',text),'Full suite incomplete'
    return {'checked_at':now(),'tests_run':int(m.group(1)),'failures':0,'errors':0,'skipped':0,'all_tests_passed':True}
test_result=tests('tests-before')
base_url='https://xn--l1adcem8c.xn--d1aigvp.xn--p1ai/'
def check(pair):
    path,digest=pair;row={'path':path,'expected_sha256':digest,'verified':False}
    try:
        req=urllib.request.Request(base_url+urllib.parse.quote(path,safe='/')+'?honor_verify='+str(time.time_ns()),headers={'Cache-Control':'no-cache','User-Agent':'HONOR-reference-delivery-check'})
        with urllib.request.urlopen(req,timeout=40) as h:
            raw=h.read();row.update(http_status=h.status,content_type=h.headers.get('Content-Type'))
        actual=shab(raw);row.update(bytes=len(raw),actual_sha256=actual,verified=(actual==digest))
        if path.endswith('.png'):assert raw.startswith(b'\x89PNG\r\n\x1a\n')
        if path.endswith('.webp'):assert raw[:4]==b'RIFF' and raw[8:12]==b'WEBP'
    except Exception as e:row.update(verified=False,error=type(e).__name__+': '+str(e))
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(check,expected.items()))
live={'checked_at':now(),'base_url':base_url,'file_count':len(rows),'verified_count':sum(x['verified'] for x in rows),'all_verified':all(x['verified'] for x in rows),'results':rows}
dump(E/'site-readback.json',live);assert live['all_verified'],[x for x in rows if not x['verified']]
drive=load(P/'reports/honor-reference-drive-readback.json');assert drive['verified_count']==6 and drive['all_verified']
assert {x['drive_id']:x['sha256'] for x in drive['results']}=={x['drive_id']:x['sha256'] for x in r['assets']}
# Keep the original Drive readback timestamp: no fabricated new download.
drive['evidence_reused_without_redownload']=True
out_path=P/'reports/honor-reference-delivery.json'
out={'schema_version':1,'project':'raznoe','work_id':r['work_id'],'scenes':[4,5],'checked_at':now(),'source_head':head,'workflow_run_id':os.environ['GITHUB_RUN_ID'],'takeover_mode':'short; current preflight passed; prior assets not regenerated','source_model_binding_count':39,'binding_results':binding_results,'site':live,'drive':drive,'tests':test_result,'technical_reference_integration_complete':True,'full_films_complete':False,'editorial_approval':False,'video_launches':0,'new_generated_images':0,'scope':'Complete delivery of existing six generated images and real phone-model reference bindings in scenes 4/5. Not completed videos or contest participation.'}
r.update(site_verified=True,site_verification_report=str(out_path),site_verified_at=live['checked_at'],reference_integration_task_complete=True);dump(report_path,r)
anchor='# 11.11.2026 — реальные модели и шесть референсов HONOR4/5';cp=P/'reports/current-work-checkpoint.md';text=cp.read_text()
parts=re.split(r'(?m)(?=^# )',text);ids=[i for i,x in enumerate(parts) if x.splitlines() and x.splitlines()[0]==anchor];assert len(ids)==1,'Checkpoint anchor must be unique'
done=f'Внесение референсов завершено: 6 PNG, 6 превью и 39 автономных привязок к точным реальным моделям. Сайт: {len(rows)}/{len(rows)} файлов совпали по SHA256. Drive6/6 ранее проверены, существующие копии сохранены. Полный набор: {test_result["tests_run"]} тестов, ошибок/пропусков0.'
nxt='Этап референсов и публикации закрыт: изображения, 36+3 промпта и источники не создавать повторно. Дальше только отдельно разрешённые видеозапуски, реальные стыки, полный QC и приёмка; для X9e — отдельная конкурсная отправка и физическая съёмка. Они этим этапом не выполнены.'
parts[ids[0]]=anchor+'\n\nwork_id: RAZNOE-HONOR-X9EPRO-CONTEST-20261107\n\n- '+done+'\n- Официальные источники приоритетны. ИИ-кадры только свет/композиция; H-GEN-PAIR — сравнение, X-GEN-MOSCOW — архив.\n- Доказательство: '+str(out_path)+'\n- Следующий шаг: '+nxt+'\n\nchecked_at: '+now()+'\n\n---\n\n';cp.write_text(''.join(parts))
handoff=P/'HANDOFF.md';h=handoff.read_text();marker='- **HONOR 4/5 — проверка референсов завершена:**'
line=marker+' '+done+' Отчёт: `reports/honor-reference-delivery.json`. Видео/конкурс не закрыты.\n'
h=re.sub(r'(?m)^'+re.escape(marker)+r'.*\n?','',h);handoff.write_text(line+'\n'+h);dump(out_path,out)
capture('.','RAZNOE-HONOR-X9EPRO-CONTEST-20261107',anchor,done,nxt,[str(out_path),str(report_path)],[str(P/'references/scenes/scene-4/reference-bindings.json'),str(P/'references/scenes/scene-5/reference-bindings.json')],True,project='raznoe')
run('resume',['python3','scripts/build_resume_packet.py','.','--project','raznoe'])
run('preflight-after',['python3','scripts/continue_preflight.py','.','--project','raznoe'])
validations=[]
for name,args in [('site',['python3','scripts/validate_site.py']),('instructions',['python3','scripts/cert_github.py','.']),('projects',['python3','scripts/projects.py','.','validate'])]:
    run(name,args);validations.append({'name':name,'exit_code':0})
out['tests_final']=tests('tests-after');out['validations']=validations;out['protected_files_unchanged']=protected
assert protected=={p:sha(p) for p in protected},'Protected content changed';dump(out_path,out);lease()
files=[str(out_path),str(report_path),str(cp),str(handoff),str(P/'work-resume-register.json'),str(P/'shadow/resume-packet.md'),str(P/'shadow/resume-packet.json')]
# Release the exact leases in the same final verified transaction.
for p in LOCKS:
    l=load(p);l.update(state='free',expires_at=None,released_at=now());dump(p,l);files.append(str(p))
subprocess.run(['git','add','--',*files],check=True)
changed=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(changed)<=set(files)
(E/'changed-files.txt').write_text('\n'.join(changed)+'\n');dump(E/'delivery-report.json',out)
with zipfile.ZipFile(E/'HONOR-reference-delivery.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in expected:
        if name.endswith('video-prompts.md'):z.writestr('Сцены 4 и 5 — актуальные промпты.md',master[master.index('<a id="scene-4"></a>'):])
        elif name.endswith('character-references.json'):continue
        else:z.write(name,name)
    z.write(out_path,str(out_path));z.write(report_path,str(report_path))
    z.writestr('ПРОЧИТАЙ.txt','Разное. Референсы сцен 4 и 5 внесены и проверены. Официальные источники остаются в прежних приватных папках Drive; ссылки закреплены в reference-bindings.json. ИИ-кадры не являются официальными фото или доказательством реального испытания. Пакет не содержит готовых видеороликов и не означает отправку заявки.\n')
print('REFERENCE_DELIVERY_VERIFIED',len(rows),len(binding_results),out['tests_final']['tests_run'])
