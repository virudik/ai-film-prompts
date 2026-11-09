#!/usr/bin/env python3
"""Import ONE owner-requested, visually checked native image; never submit video."""
import json, hashlib, datetime, re, sys, urllib.request, io
from pathlib import Path
from PIL import Image
sys.path.insert(0, 'scripts')
import resume_state
WORK='SEREGIUS-PARODIES-20261109'
req=json.loads(Path('reports/parody-image-import.json').read_text())
assert req['work_id']==WORK and req['project']=='seregius'
assert req['scene_id'] in range(74,81) and req['qc']['passed'] is True
assert req['generation_method']=='ChatGPT imagegen (built-in)' and req['imagegen_generation_id']
now=datetime.datetime.now(datetime.timezone.utc)
l=json.loads(Path('ops/canon-lock.json').read_text())
assert l['state']=='held' and l['holder']==req['holder'] and l['acquired_at']==req['acquired_at']
assert datetime.datetime.fromisoformat(l['expires_at'])>now
n=req['scene_id'];folder=Path('references/scenes/scene-'+str(n));mp=folder/'manifest.json';m=json.loads(mp.read_text())
assert m['scene_id']==n
pending=m.get('pending_reference')
if not pending:
    assert any(x.get('sha256')==req['sha256'] for x in m['references'])
    print('Already saved with exact SHA; no replacement');raise SystemExit(0)
path=pending['path'];dest=Path(path)
assert dest.parent==folder and dest.name==req['file_name'] and not dest.exists()
assert re.fullmatch(r'[A-Za-z0-9_-]+',req['drive_file_id'])
assert req['drive_readback_sha256']==req['sha256']
url='https://drive.usercontent.google.com/download?id='+req['drive_file_id']+'&export=download&confirm=t'
with urllib.request.urlopen(url,timeout=60) as response:
    data=response.read(20000001)
assert 8<len(data)<=20000000 and data[:8]==b'\x89PNG\r\n\x1a\n','Drive did not return a PNG; do not publish HTML'
assert hashlib.sha256(data).hexdigest()==req['sha256'],'Remote bytes differ from verified local image'
image=Image.open(io.BytesIO(data));image.load();w,h=image.size
assert [w,h]==req['dimensions'] and w>=1024 and h>=576
assert abs(w/h-16/9)<0.02,'Reference must fill 16:9, not a hidden collage/bar crop'
queue_before=hashlib.sha256(Path('ops/topview-launch-queue.json').read_bytes()).hexdigest()
for r in req['reference_inputs']:
    assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256'],'Identity input changed'
prompt_file=pending['prompt_file'];prompt_sha=hashlib.sha256(Path(prompt_file).read_bytes()).hexdigest()
assert prompt_sha==req['prompt_sha256'],'Prompt changed since image generation'
dest.write_bytes(data)
thumb='references/thumbs/scenes/scene-'+str(n)+'/'+dest.name+'.webp'
tp=Path(thumb);tp.parent.mkdir(parents=True,exist_ok=True)
preview=image.convert('RGB');preview.thumbnail((480,270));preview.save(tp,'WEBP',quality=85)
entry={'path':path,'asset_id':path,'caption':pending['caption'],'slot':pending['slot'],'role':'scene_staging','sha256':req['sha256'],'bytes':len(data),'dimensions':[w,h],'media_type':'image','status':'available','owner_approval':'not_recorded','editorial_status':'not_approved','generation_method':req['generation_method'],'imagegen_generation_id':req['imagegen_generation_id'],'created_at':req['created_at'],'saved_at':now.isoformat(),'prompt_file':prompt_file,'prompt_sha256':prompt_sha,'reference_inputs':req['reference_inputs'],'technical_qc':req['qc'],'exchange_copy':{'drive_file_id':req['drive_file_id'],'sha256_readback_match':True},'site_published':{'path':path,'thumbnail':thumb,'linked_in_master':True}}
m['references'].append(entry);m.pop('pending_reference');m['updated_at']=now.isoformat();mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
cp=Path('character-references.json');chars=json.loads(cp.read_text());asset_id=dest.stem
assert not any(a.get('id')==asset_id for a in chars.get('assets',[]))
chars.setdefault('assets',[]).append({'id':asset_id,'name':pending['caption'],'kind':'scene_reference','scenes':[n],'editorial_status':'not_approved','images':[entry]});chars['updated_at']=now.isoformat();cp.write_text(json.dumps(chars,ensure_ascii=False,indent=2)+'\n')
masterp=Path('video-prompts.md');master=masterp.read_text();pattern=r'(<a id="scene-'+str(n)+r'"></a>.*?)(?=\n<a id="scene-\d+"></a>|\Z)';match=re.search(pattern,master,re.S);assert match
part=match[1];part=part.replace('отдельный новый постановочный PNG ещё требуется','отдельный постановочный PNG сохранён и технически проверен; художественная приёмка владельцем ещё требуется')
part=part.replace('Для нового PNG пока сохранено только точное задание; не выдавать его за изображение.','Новый PNG сохранён с SHA/manifest и привязан ниже; это постановочный референс, не реальный кадр фильма и не одобрение ролика.')
part=part.replace('"images_pending"','"reference_keyframe_saved"')
figure='<figure><a href="'+path+'" target="_blank" rel="noopener"><img src="'+thumb+'" alt="'+pending['caption']+'"></a><figcaption>'+pending['slot']+' — '+pending['caption']+'; технический QC, not_approved</figcaption></figure>\n'
assert 'scene-ref-gallery' in part and path not in re.findall(r'href="([^"]+)"',part)
part=part.replace('</div>',figure+'</div>',1)
master=master[:match.start()]+part+master[match.end():]
# Only the affected TOC row changes its pending-reference phrase.
lines=master.splitlines()
for i,line in enumerate(lines):
    if line.startswith('| '+str(n)+' | '):lines[i]=line.replace('новый постановочный PNG ожидается','постановочный PNG сохранён')
master='\n'.join(lines)+'\n';master=re.sub(r'\n{3,}','\n\n',master);masterp.write_text(master)
reportp=Path('reports/parody-scenes-2026-11-09.json');report=json.loads(reportp.read_text());saved=report.setdefault('saved_images',[])
assert not any(x['scene_id']==n for x in saved)
saved.append({'scene_id':n,'path':path,'sha256':req['sha256'],'dimensions':[w,h],'generation_id':req['imagegen_generation_id'],'saved_at':now.isoformat(),'technical_qc_passed':True,'editorial_approval':False})
saved.sort(key=lambda x:x['scene_id']);count=len(saved);remaining=[i for i in range(74,81) if i not in {x['scene_id'] for x in saved}]
report.update(images_created=count,reference_keyframes_saved=count,reference_keyframes_expected=7,remaining_image_scenes=remaining,state='scene_keyframes_saved_not_approved' if count==7 else 'images_in_progress',updated_at=now.isoformat())
report['next_action']=('Семь постановочных PNG сохранены; проверить художественное сходство, дополнительные ракурсы для смены локаций и монтажную позицию. Не повторять сцены/готовые PNG, не запускать видео без отдельного разрешения.' if not remaining else 'Продолжить только недостающие постановочные PNG сцен '+', '.join(map(str,remaining))+' по сохранённым заданиям. Сохранить каждый PNG/SHA/manifest до следующего. Видео не запускать.')
reportp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
anchor='# 09.11.2026 — пародии 74–80: сохранено '+str(count)+' из 7 постановочных PNG'
check=Path('reports/current-work-checkpoint.md');text=check.read_text();assert anchor not in text
check.write_text(anchor+'\n\nwork_id: '+WORK+'\n\n- Семь сцен и 21 видеопромпт уже существуют; в этом шаге сохранён только '+path+' с SHA '+req['sha256']+'.\n- Проверены изображение, точные входы, обратное скачивание Drive и файловая привязка; approval не назначен.\n- Сохранены сцены: '+', '.join(str(x['scene_id']) for x in saved)+'. Остались PNG: '+(', '.join(map(str,remaining)) or 'нет в стартовом наборе из семи')+'.\n- Следующий шаг: '+report['next_action']+'\n- Доказательство: reports/parody-scenes-2026-11-09.json. Очередь и видеозапуски не менялись.\n\n---\n\n'+text)
resume_state.capture('.',WORK,anchor,'Семь сцен/21 текст, постановочные PNG '+str(count)+'/7 сохранены с QC и SHA; not_approved.',report['next_action'],[str(reportp)],['video-prompts.md',str(reportp)],False)
rp=Path('work-resume-register.json');reg=json.loads(rp.read_text());record=next(x for x in reg['active_work'] if x['work_id']==WORK);record['status']='awaiting_editorial_qc' if count==7 else 'image_generation_in_progress';record['reference_keyframes_saved']=count;rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
plansp=Path('ops/FUTURE-PLANS.md');plans=plansp.read_text();plans=re.sub(r'(?m)^- \*\*SEREGIUS-PARODIES-20261109:\*\*.*$', '- **SEREGIUS-PARODIES-20261109:** семь сцен 74–80 / 21 текст готовы; постановочные PNG '+str(count)+'/7 сохранены с manifest/SHA/галереями. '+('Стартовый набор изображений выполнен; художественная приёмка и видео не выполнены.' if count==7 else 'Остались PNG сцен '+', '.join(map(str,remaining))+'.')+' Готовое не повторять. Доказательство: `reports/parody-scenes-2026-11-09.json`. Запуск видео не производился.', plans);plansp.write_text(plans)
handoffp=Path('NEW-CHAT-HANDOFF.md');handoff=handoffp.read_text();handoff=re.sub(r'(?m)^- \*\*09\.11 — пародии 74–80:\*\*.*$', '- **09.11 — пародии 74–80:** 7 сцен/21 текст, PNG '+str(count)+'/7 сохранены; not_approved, видео не запускались. Не повторять; `reports/parody-scenes-2026-11-09.json`.', handoff);assert len(handoff.encode())<35000;handoffp.write_text(handoff)
Path('SYNC-TRIGGER.txt').write_text(now.isoformat()+' parody image '+str(n)+' saved; master SHA256 '+hashlib.sha256(masterp.read_bytes()).hexdigest()+'\n')
assert hashlib.sha256(Path('ops/topview-launch-queue.json').read_bytes()).hexdigest()==queue_before
print(json.dumps({'saved':path,'sha256':req['sha256'],'count':count,'remaining':remaining,'queue_unchanged':True},ensure_ascii=False))
