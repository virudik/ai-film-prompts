from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,os,sys,shutil
sys.path.insert(0,str(Path.cwd()/'scripts'))
from resume_state import capture

def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def save(p,j): Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat()
lock=load('ops/canon-lock.json')
assert lock['state']=='held' and lock['holder']==os.environ['EXPECTED_HOLDER'] and lock['acquired_at']==os.environ['EXPECTED_ACQUIRED_AT']
assert datetime.fromisoformat(lock['expires_at'].replace('Z','+00:00'))>datetime.now(timezone.utc)
queue_hash=sha(Path('ops/topview-launch-queue.json').read_bytes())
source=Path('/tmp/S74-studio-roar.png');image_hash='ef65d3aae1a4bdeb4f49d19c576136a7dffa0b8852be06e0affac76b3c443b18'
assert source.is_file() and source.stat().st_size==2473956 and sha(source.read_bytes())==image_hash
assert source.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
image='references/scenes/scene-74/S74-studio-roar.png'
assert not Path(image).exists(), 'Image already exists; reread rather than replace'
master=Path('video-prompts.md');text=master.read_text()
pat=re.compile(r'(?ms)(^## Сцена (\d+) — .*?)(?=\n---\n\n<a id="scene-\d+"></a>|\Z)')
blocks={int(m[2]):m[1] for m in pat.finditer(text)}
old=blocks[74]
assert sha(old.encode())=='781b63802ce3ccbaa63aeab715c9db3d70c717735d2769ac64da877ef8300701','S74 changed; reread instead of replay'
t=old.replace('отдельный новый постановочный PNG ещё требуется','первый постановочный PNG с рыком сохранён; отдельные кадры факела, глобуса, горы и прожекторов ещё требуются')
t=t.replace('Для нового PNG пока сохранено только точное задание; не выдавать его за изображение.','PNG @Image2 сохранён и прошёл технический визуальный QC; он задаёт только кадр рыка. Одобрение владельца и остальные ракурсы не получены.')
t=t.replace('exact vitalik face and body; wardrobe follows the explicit scene costume.','exact Vitalik facial identity only; clothing is chosen for this staged parody, not copied from the model sheet.')
t=t.replace('Base outfit: black Jedi tunic and leather tabard, brown belt, brown trousers and tall boots. Only the explicitly staged curtain costume may cover this outfit.','Scene costume: opaque black theatrical jacket with subtle metallic shoulder panels, plain dark trousers and black shoes; no Jedi belt, lightsaber or source-sheet costume. The torch gag adds a cream curtain over fully covering dark stage clothes.')
t=t.replace('black Jedi tunic visible at shoulders','black theatrical jacket visible at shoulders')
figure='<figure><a href="'+image+'" target="_blank" rel="noopener"><img src="'+image+'" alt="@Image2 — постановочный кадр рыка"></a><figcaption>@Image2 — рычащий Виталик, технический QC; не редакционная приёмка</figcaption></figure>\n'
assert t.count('<div class="scene-ref-gallery">')==1
start=t.index('<div class="scene-ref-gallery">');end=t.index('</div>',start)
t=t[:end]+figure+t[end:]
assert t.count('```text')==3 and t.count('@Image2 = '+image)==3
master.write_text(text.replace(old,t,1));shutil.copyfile(source,image)
after={int(m[2]):m[1] for m in pat.finditer(master.read_text())}
assert all(after[n]==v for n,v in blocks.items() if n!=74)
m=load('references/scenes/scene-74/manifest.json');m.pop('pending_reference',None)
m['references'][0]['caption']='@Image1 — лицо Виталика; одежда отдельная по сцене'
m['references'].append({'path':image,'asset_id':image,'caption':'@Image2 — отдельный постановочный кадр рыка; только начало S74','role':'scene_staging','sha256':image_hash,'bytes':2473956,'width':1672,'height':941,'media_type':'image','status':'available','owner_approval':'not_reviewed','provenance':{'source':'ChatGPT native generated conversation image','generation_id':'ca55005c-c49d-471c-bfca-aee7b5997207','source_file_name':'ревущий_виталик_в_золотой_киноленте.png','drive_exchange_file_id':'1KUTkYLozDInRxvhRLd9eM7kcsxG_MDgi','download_sha256_verified':True},'qc':{'scope':'visual staging check of existing image; not video or owner approval','single_frame':True,'no_collage':True,'no_text':True,'human_roar':True,'facial_reference_compared':'references/full/vitalik.jpg','limitations':'Expression changes face geometry; final likeness acceptance belongs to owner. Only roar setup, not the entire five-gag scene.'}})
m['additional_references_pending']=['torch curtain pedestal','globe stage','potato mountain','searchlight crates'];m['updated_at']=now
save('references/scenes/scene-74/manifest.json',m)
source_report=load('reports/parody-scenes-source-2026-11-09.json')
for s in source_report.get('scenes',[]):
 if s.get('id')==77:
  s['identities']=['vitalik','lesha','masha-r'];s['appearance']='Exactly three adults: Vitalik, Alexey/Lesha and Masha R. Individual sheets supply faces only. Navy jacket/grey shirt; olive corduroy jacket/cream shirt; teal coat/burgundy scarf. No Alina or child in this scene.'
  s['summary']='Виталик сообщает Алексею об отказе Маши Р. Алексей не верит. Маша Р появляется за забором и сама признаётся Алексею. Виталик завершает сцену новой шуткой о майонезе.'
  s['context']='Пародийная постановка с тремя взрослыми; замена Алины на Алексея по прямому решению владельца. Оригинал и авторская постановка разделены. Это роли, не биография участников.'
  s['image_prompt']=Path('references/scenes/scene-77/S77-love-triangle.image-prompt.txt').read_text()
  for key in ('start','mid','end','location'):
   if key in s:s[key]=s[key].replace('Serega','TEMP_FIRST').replace('Vitalik','Alexey').replace('TEMP_FIRST','Vitalik').replace('green woman','Masha R').replace('adult alien woman','adult Masha R')
  for key in ('p1','p2'):
   if key in s:s[key]=[v.replace('Serega','TEMP_FIRST').replace('Vitalik','Alexey').replace('TEMP_FIRST','Vitalik').replace('green woman','Masha R').replace('from his robe','from his jacket pocket') for v in s[key]]
  s['owner_revision_recorded_at']=now
save('reports/parody-scenes-source-2026-11-09.json',source_report)
r=load('reports/parody-scenes-2026-11-09.json')
next_action='Не повторять 74–80/21 текст. S74: первый кадр рыка уже сохранён; дорисовать остальные заставки и 75–80, сначала проверять существующие файлы. S77 в main: Виталик/взрослый Алексей/Маша Р, новая одежда; Алины в любовной сцене нет. Старые изображения с неверными лицами и коллажи не использовать. Пригодный кадр сразу PNG/SHA/manifest/master, затем следующий. Не запускать видео.'
r.update(state='partial_references_saved_adult_cast_corrected',accepted_new_scene_images=1,images_created=1,images_generated_this_cycle=0,updated_at=now,next_action=next_action,remaining_image_scenes=[75,76,77,78,79,80],editorial_approval=False)
r['image_count_semantics']='images_created/accepted_new_scene_images counts saved technically reviewed scene stills, not new calls this cycle and not owner approval. Earlier generated_images_attempted is historical, not total conversation attempts.'
r['saved_scene_images']=[{'scene_id':74,'path':image,'sha256':image_hash,'generation_id':'ca55005c-c49d-471c-bfca-aee7b5997207','owner_approved':False}]
r['additional_reference_views_pending']={'74':m['additional_references_pending']}
r['old_unknown_actor_images_replaced_in_canon']=False
r['old_unknown_actor_images_note']='Old compositions are not canonical references. First corrected roar has now been saved, not all old images replaced. No old images deleted.'
r['exchange_folder']['files_uploaded']=1
r['publication']['master_sha256']=sha(master.read_bytes());r['publication']['live_master_verification_pending_after_casting']=True
save('reports/parody-scenes-2026-11-09.json',r)
fp=Path('ops/FUTURE-PLANS.md');f=fp.read_text()
f=re.sub(r'(?m)^- \*\*SEREGIUS-PARODIES-20261109:\*\*.*$','- **SEREGIUS-PARODIES-20261109:** 7 сцен/21 текст уже опубликованы. S77 исправлена: Виталик, взрослый Алексей и Маша Р; только лица, новая одежда. **Первый PNG S74 сохранён**, остальные постановки75–80 и дополнительные заставки74 открыты. Неверные лица/коллажи не прикреплять, всю задачу не закрывать. `reports/parody-scenes-2026-11-09.json`; видео/очередь не менялись.',f)
fp.write_text(f)
hp=Path('NEW-CHAT-HANDOFF.md');h=hp.read_text()
h,count=re.subn(r'(?m)^- \*\*09\.11 — пародии 74–80:\*\*.*$','- **09.11 — пародии 74–80:** S74 PNG сохранён; S77 Виталик/Алексей/Маша Р. Остальные кадры открыты; `reports/parody-scenes-2026-11-09.json`. Не повторять готовое.',h)
assert count==1 and len(h.encode())<35000
hp.write_text(h)
cp=Path('reports/current-work-checkpoint.md');anchor='# 09.11.2026 — сохранён первый PNG S74; исправлен взрослый состав S77'
assert anchor not in cp.read_text()
cp.write_text(anchor+'\n\nwork_id: SEREGIUS-PARODIES-20261109\n\n- Семь сцен/21 текст не создавались повторно. Во всех трёх вариантах S77 теперь Виталик, взрослый Алексей и Маша Р; точные лица, новая одежда, Алины здесь нет.\n- Существующий PNG рыка S74 сохранён без перекодирования с SHA/manifest/галереей и привязкой во всех трёх промптах. Это первый постановочный кадр, не вся сцена и не приёмка владельца.\n- Остальные пять заставок/ракурсы, сцены75–80 и замена всех прежних лиц ещё не закрыты. Непрерывный просмотр/звук оригиналов мемов не заявляется.\n- Сертификаты, перенос YouTube, HONOR/RESOURCE, конкурс и аудит старых чатов этим исправлением не закрывались.\n- Следующий шаг: '+next_action+'\n\nchecked_at: '+now+'\n\n---\n\n'+cp.read_text())
capture(Path.cwd(),'SEREGIUS-PARODIES-20261109',anchor,'S74: первый PNG сохранён; S77: все три промпта и три identity bindings исправлены.',next_action,['reports/parody-scenes-2026-11-09.json'],['video-prompts.md','references/scenes/scene-74/manifest.json','references/scenes/scene-77/manifest.json'],focus=False)
reg=load('work-resume-register.json');w=next(v for v in reg['active_work'] if v['work_id']=='SEREGIUS-PARODIES-20261109');w['status']='partially_completed_images_pending';w['recovery']['blockers']=['Remaining staged images and additional logo views not yet saved or reviewed.'];save('work-resume-register.json',reg)
assert sha(Path('ops/topview-launch-queue.json').read_bytes())==queue_hash
Path('SYNC-TRIGGER.txt').write_text('Save existing S74 still and owner S77 adult cast correction; '+now+'\n')
print(json.dumps({'s74_saved':image,'sha256':image_hash,'s77_adult_cast_applied':True,'new_image_generations_this_cycle':0,'queue_unchanged':True,'all_tasks_done':False},ensure_ascii=False))
