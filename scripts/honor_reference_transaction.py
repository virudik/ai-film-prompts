#!/usr/bin/env python3
"""One-shot owner-requested HONOR reference integration; no media or contest actions."""
import hashlib,json,os,re,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
P=Path('projects/raznoe'); E=Path('/tmp/honor-reference-evidence'); B=Path('/tmp/honor-reference-bundle/files')
sys.path.insert(0,str(Path('scripts').resolve()))
from resume_state import capture
from importlib.util import spec_from_file_location,module_from_spec
sp=spec_from_file_location('honor_integration',B/'integrate.py'); mod=module_from_spec(sp);sp.loader.exec_module(mod)
def now():return datetime.now(timezone.utc).isoformat(timespec='seconds')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
mod.lease(); head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
protected=['video-prompts.md','ops/topview-launch-queue.json','review-ledger.json',str(P/'ops/topview-launch-queue.json'),str(P/'review-ledger.json'),str(P/'references/scenes/scene-4/filmwide-voiceover-120s.json'),str(P/'references/scenes/scene-4/production-voiceover.json'),str(P/'references/scenes/scene-5/shooting-package.md')]
protected+=['NEW-CHAT-HANDOFF.md','SYNC-RUNBOOK.md','AI-PROJECT-GUIDE.md','PROMPT-STYLE-GUIDE.md','USER-GUIDE.md','README-AI-SYNC.md','BACKUP-AI-RUNBOOK.md']
before={p:sha(p) for p in protected}
master_before=(P/'video-prompts.md').read_text(); prefix=master_before.split('<a id="scene-4"></a>')[0]
reg_before=json.loads((P/'character-references.json').read_text())
mod.apply(B)
instr=P/'INSTRUCTIONS.md';text=instr.read_text();old='точный продукт отдельным композитным слоем по references/scenes/scene-4/production-package.md';new='реальная модель по официальным фото и карте references/scenes/scene-4/reference-bindings.json; точный композит остаётся запасным вариантом по production-package.md';assert old in text;text=text.replace(old,new,1);instr.write_text(text)
q=Path('tests/test_honor_real_model_references.py');text=(B/'qa.py').read_text().replace('R=Path.cwd();','R=Path(__file__).resolve().parents[1];');q.write_text(text)
assert before=={p:sha(p) for p in protected},'protected input changed'
assert (P/'video-prompts.md').read_text().split('<a id="scene-4"></a>')[0]==prefix
reg_after=json.loads((P/'character-references.json').read_text());assert reg_before['characters']==reg_after['characters']
assert reg_after['assets'][:len(reg_before['assets'])]==reg_before['assets']
results=[]
def run(name,args):
 r=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(E/(name+'.log')).write_text(r.stdout)
 results.append({'name':name,'exit_code':r.returncode});assert r.returncode==0,(name,r.stdout[-7000:]);return r.stdout
run('project-status',['python3','scripts/projects.py','.','status','--project','raznoe','--write'])
assert json.loads((P/'project-status.json').read_text())['health']=='ok'
run('resume',['python3','scripts/build_resume_packet.py','.','--project','raznoe'])
run('preflight-after',['python3','scripts/continue_preflight.py','.','--project','raznoe'])
run('reference-qa',['python3',str(B/'qa.py')])
logs=run('full-tests',['python3','-m','unittest','discover','-s','tests'])
m=re.search(r'Ran (\d+) tests? in',logs);assert m and int(m.group(1))>=548 and not re.search(r'skipped=\d+',logs)
count=int(m.group(1))
run('site',['python3','scripts/validate_site.py'])
run('certificate',['python3','scripts/cert_github.py','.'])
run('projects',['python3','scripts/projects.py','.','validate'])
report=P/'reports/honor-reference-integration.json';r=json.loads(report.read_text());r.update(source_head=head,workflow_run_id=os.environ['GITHUB_RUN_ID'],test_results={'checked_at':now(),'tests_run':count,'failures':0,'errors':0,'skipped':0,'all_tests_passed':True},validations=results,protected_files_unchanged=before,drive_readback=json.loads((P/'reports/honor-reference-drive-readback.json').read_text()),canonical_integration_complete=True,site_verified=False);dump(report,r)
anchor='# 11.11.2026 — реальные модели и шесть референсов HONOR4/5';cp=P/'reports/current-work-checkpoint.md';t=cp.read_text();t=t.replace('Результат ещё проходит проверки; публикацию не считать подтверждённой до live readback.',f'39 привязок проверены; {count} тестов и валидаторы пройдены. Проверка выдачи сайта ещё ожидается.',1);cp.write_text(t)
completed=f'Шесть существующих ИИ-PNG и6 превью привязаны к сценам4/5; все36+3 промпта используют реальные источники точной модели. Drive6/6 совпали. Тесты{count}/{count}; сайт ещё ждёт точного readback.'
next_action='Завершить Pages и точный readback всех файлов; не пересоздавать изображения. Затем только отдельно разрешённые видео, реальные хвосты/QC и конкурсная съёмка; приёмку не подменять.'
capture('.', 'RAZNOE-HONOR-X9EPRO-CONTEST-20261107',anchor,completed,next_action,[str(report),str(P/'reports/honor-reference-drive-readback.json')],[str(P/'references/scenes/scene-4/reference-bindings.json'),str(P/'references/scenes/scene-5/reference-bindings.json')],True,project='raznoe')
run('resume-final',['python3','scripts/build_resume_packet.py','.','--project','raznoe'])
run('preflight-final',['python3','scripts/continue_preflight.py','.','--project','raznoe'])
logs2=run('full-tests-final',['python3','-m','unittest','discover','-s','tests']);m2=re.search(r'Ran (\d+) tests? in',logs2);assert m2 and int(m2.group(1))==count and not re.search(r'skipped=\d+',logs2)
assert before=={p:sha(p) for p in protected},'protected files changed during verification'
files=[str(P/x) for x in ['video-prompts.md','character-references.json','INSTRUCTIONS.md','HANDOFF.md','project-status.json','reports/current-work-checkpoint.md','reports/honor-reference-integration.json','work-resume-register.json','shadow/resume-packet.md','shadow/resume-packet.json']]+[str(q)]
for sid in (4,5):files += [str(P/f'references/scenes/scene-{sid}'/n) for n in ['manifest.json','reference-bindings.json']]
files += [str(P/'references/scenes/scene-4'/n) for n in ['production-package.md','product-compositing.json']]
for a in r['assets']:files.extend([a['path'],a['preview']])
mod.lease();subprocess.run(['git','add','--',*files],check=True)
changed=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(changed)<=set(files)
(E/'changed-files.txt').write_text('\n'.join(changed)+'\n');(E/'integration-report.json').write_bytes(report.read_bytes());print('INTEGRATION_CHECKED',len(changed),r['test_results'])
