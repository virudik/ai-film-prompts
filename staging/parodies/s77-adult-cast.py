from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, sys
sys.path.insert(0, str(Path.cwd()/'scripts'))
from resume_state import capture
from trim_service_files import trim_register

def digest(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def save(p,j): Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat()
lock=load('ops/canon-lock.json')
assert lock['state']=='held' and lock['holder']==os.environ['EXPECTED_HOLDER']
assert lock['acquired_at']==os.environ['EXPECTED_ACQUIRED_AT']
assert datetime.fromisoformat(lock['expires_at'].replace('Z','+00:00'))>datetime.now(timezone.utc)
master=Path('video-prompts.md'); text=master.read_text()
pat=re.compile(r'(?ms)(^## Сцена (\d+) — .*?)(?=\n---\n\n<a id="scene-\d+"></a>|\Z)')
blocks={int(m[2]):m[1] for m in pat.finditer(text)}
old=blocks[77]
assert digest(old.encode())=='1004e550c2df0a22a9536adc75f2bdc9dca1b63b209c5b6f4a2f1b6d5d728a79', 'S77 changed: reread instead of replay'
queue_hash=digest(Path('ops/topview-launch-queue.json').read_bytes())
refs=['references/full/vitalik.jpg','references/full/lesha.jpg','references/scenes/scene-67/S67-Masha-R-tatooine-sheet.png']
ids=['vitalik','lesha','masha-r']
for p in refs: assert Path(p).is_file(),p
names=['Виталик','Алексей (Лёша)','Маша Р']
wardrobe='VITALIK @Image1: adult fair man, round face, short light-brown hair, light stubble; navy casual jacket, light grey shirt and dark trousers. ALEXEY / LESHA @Image2: adult slim fair man, short wavy brown hair and distinct brown moustache; olive corduroy jacket, cream shirt and dark trousers. MASHA R @Image3: adult fair woman, long wavy copper-red hair and bangs; modest teal wool coat and burgundy scarf. Preserve the exact facial identities from their individual sheets ONLY, not the source Jedi/Tatooine clothing. Exactly three ADULT actors. No Alina, no child, no Serega, no alien substitute, no kiss or erotic action. Never blend faces.'
t=old.replace('@Image3','@Image4').replace(refs[0],refs[0]).replace('references/full/serega.jpg',refs[1])
t=t.replace('Serega','TEMP_FIRST').replace('SEREGA','TEMP_FIRST').replace('Vitalik','Alexey').replace('TEMP_FIRST','Vitalik')
t=t.replace('Серёга и Виталик играют роли; новая взрослая инопланетянка — вымышленная эпизодическая героиня, не новая биография канонических персонажей.','Виталик, взрослый Алексей (Лёша) и Маша Р играют роли. Решение владельца 09.11: в любовной сцене вместо Алины — Алексей; детей здесь нет. Только лица из референсов, одежда новая по сцене. Это постановка, не биография участников.')
t=t.replace('Серёга трагически сообщает Виталику об отказе девушки. Виталик столь же трагически отрицает её чувства. Из-за обычного садового забора поднимается зелёная инопланетянка и перекрикивает обоих признанием. После паузы Серёга достаёт ложку: «А я люблю майонез». Виталик смотрит в камеру, не понимая, кто тут снимал мелодраму.','Виталик сообщает Алексею об отказе Маши Р. Алексей отрицает её чувства. Маша Р появляется из-за садового забора и сама говорит Алексею: «Да я люблю тебя!» После паузы Виталик достаёт ложку: «А я люблю майонез». Алексей недоумённо смотрит в камеру. Сохранены исходные роли реплик: признание произносит третий персонаж, Маша Р.')
t=t.replace('adult green woman','adult Masha R').replace('green woman','Masha R').replace('third woman','adult Masha R').replace('the woman silently waits','Masha R silently waits').replace('from his robe','from his jacket pocket')
t=re.sub(r'CHARACTER APPEARANCE / IDENTITY LOCK:\n.*?\n\nSCENE / SPACE:', 'CHARACTER APPEARANCE / IDENTITY LOCK:\n'+wardrobe+'\n\nSCENE / SPACE:',t,flags=re.S)
t=t.replace('exact vitalik face and body; wardrobe follows the explicit scene costume.','exact Vitalik facial identity only; new clothing as explicitly described below.').replace('exact serega face and body; wardrobe follows the explicit scene costume.','exact adult Alexey / Lesha facial identity only; wavy brown hair and moustache, new clothing below.')
t=t.replace('@Image4 = references/scenes/scene-77/', '@Image3 = '+refs[2]+' — exact adult Masha R facial identity only; new modest clothing below.\n@Image4 = references/scenes/scene-77/')
t=t.replace('; @Image4 —','; @Image3 — `'+refs[2]+'`; @Image4 —')
gallery='<div class="scene-ref-gallery">\n'+'\n'.join('<figure><a href="'+p+'" target="_blank" rel="noopener"><img src="'+p+'" alt="@Image'+str(i)+' — '+name+'"></a><figcaption>@Image'+str(i)+' — '+name+', только лицо; одежда по сцене</figcaption></figure>' for i,(p,name) in enumerate(zip(refs,names),1))+'\n</div>'
t=re.sub(r'<div class="scene-ref-gallery">.*?</div>',lambda m:gallery,t,count=1,flags=re.S)
assert t.count('```text')==3
assert all(t.count('@Image'+str(i)+' = '+p)==3 for i,p in enumerate(refs,1))
assert 'references/full/serega.jpg' not in t and 'green-skinned' not in t and 'No Alina, no child' in t
master.write_text(text.replace(old,t,1))
new_blocks={int(m[2]):m[1] for m in pat.finditer(master.read_text())}
assert all(new_blocks[n]==b for n,b in blocks.items() if n!=77)
manifest=load('references/scenes/scene-77/manifest.json')
manifest['references']=[{'path':p,'asset_id':p,'caption':'@Image'+str(i)+' — '+name+'; facial identity only; scene-specific clothing','role':'identity','sha256':digest(Path(p).read_bytes()),'bytes':Path(p).stat().st_size,'media_type':'image','status':'available','owner_approval':'user_supplied_identity','reused_from_existing_pack':True} for i,(p,name) in enumerate(zip(refs,names),1)]
manifest['pending_reference'].update(slot='@Image4',status='needs_generation',caption='Виталик, взрослый Алексей и Маша Р у забора; Алины нет')
manifest['updated_at']=now
save('references/scenes/scene-77/manifest.json',manifest)
image_prompt='ONE standalone photoreal landscape 16:9 film still for scene 77 ONLY, not a collage, poster, panel grid or illustrated report. Exactly three adults: Vitalik at left (round fair face, short light-brown hair and light stubble), Alexey / Lesha at right (slim fair face, wavy brown hair and distinct moustache), Masha R behind the waist-high wooden garden fence between them (copper-red wavy hair and bangs). Use the three individually supplied canonical face sheets; only facial identity, not their old costumes. Vitalik wears a navy casual jacket and grey shirt, Alexey an olive corduroy jacket and cream shirt, Masha a modest teal wool coat and burgundy scarf. Two men stand apart in exaggerated telenovela disbelief. Masha has just appeared over the fence and calls her confession toward Alexey. Warm overcast apple-garden daylight, one distant fictional spaceport antenna; medium-wide 50mm three-shot, all faces legible. No Alina, no children, no embrace or kissing, no erotic posing, no wet transparent clothes. No lettering, labels, inset portraits, product bags, fish, moon or logo. Save S77-love-triangle.png. It is a scene reference, never a completion claim.\n'
Path('references/scenes/scene-77/S77-love-triangle.image-prompt.txt').write_text(image_prompt)
characters=load('character-references.json')
for c in characters['characters']:
 if c['id'] in ids: c['scenes']=sorted(set(c.get('scenes',[])+[77]))
 elif c['id'] in ('serega','alina'): c['scenes']=[x for x in c.get('scenes',[]) if x!=77]
save('character-references.json',characters)
report=load('reports/parody-scenes-2026-11-09.json')
quote='Доделывай. Вместо Алины на любовных сценах сделай Алексея'
next_action='Сцены 74–80/21 промпт не создавать заново. S77 уже исправлена: Виталик, взрослый Алексей (Лёша), Маша Р; только лица, новая одежда. Алина только в семейных эпизодах. Новые отдельные PNG ещё требуют проверки и сохранения: не использовать коллажи или кадры с посторонними лицами как референсы. Каждый пригодный PNG сохранить с SHA/manifest/слотом до следующего. Видео не запускать.'
report.update(state='adult_cast_corrected_scene_images_pending',updated_at=now,next_action=next_action)
report['owner_casting_correction']={'quote':quote,'recorded_at':now,'scene_id':77,'cast':ids,'alina_in_romantic_scene':False,'faces_only':True,'clothing':'scene_specific','all_three_prompt_variants_updated':True,'new_accepted_image_claim':False}
report['existing_identity_references']=[x for x in report.get('existing_identity_references',[]) if x['scene_id']!=77]+[{'scene_id':77,'path':p,'sha256':digest(Path(p).read_bytes())} for p in refs]
report['existing_identity_reference_bindings']=len(report['existing_identity_references'])
report['publication']['master_sha256']=digest(master.read_bytes())
report['publication']['live_master_verification_pending_after_casting']=True
save('reports/parody-scenes-2026-11-09.json',report)
plan=Path('ops/FUTURE-PLANS.md'); ps=plan.read_text(); marker='## Прямое поручение 09.11 — пародии Серёгиуса'
assert marker in ps
ps=ps.replace(marker,marker+'\n\n- **Состав S77 исправлен 09.11:** Виталик + взрослый Алексей (Лёша) + Маша Р, новые костюмы; Алины в любовной сцене нет. Три варианта промпта и ссылки на лица обновлены. Это НЕ готовый постановочный PNG; коллажи и ошибочные лица не прикреплять. Остальные картинки/заставки остаются открытыми.',1)
plan.write_text(ps)
cp=Path('reports/current-work-checkpoint.md')
anchor='# 09.11.2026 — S77: взрослый Алексей вместо Алины, изображения ещё не готовы'
cp.write_text(anchor+'\n\nwork_id: SEREGIUS-PARODIES-20261109\n\n- Решение владельца: '+quote+'.\n- Во всех трёх промптах S77: Виталик, Алексей (Лёша), Маша Р; три точных лица, новая одежда. Алины и других детей в любовном сюжете нет.\n- Изменены только S77 и связанные учётные файлы; сцены 74–76/78–80, очередь и генерации не менялись.\n- Новых принятых/прикреплённых PNG этим исправлением нет; показанные коллажи не подтверждают выполнение.\n- Следующий шаг: '+next_action+'\n\nchecked_at: '+now+'\n\n---\n\n'+cp.read_text())
reg=load('work-resume-register.json')
entry=next(w for w in reg['active_work'] if w['work_id']=='SEREGIUS-PARODIES-20261109')
entry['status']='images_pending'
save('work-resume-register.json',reg)
capture(Path.cwd(),'SEREGIUS-PARODIES-20261109',anchor,'S77: все три промпта и три лицевых референса исправлены на Виталик/Алексей/Маша Р; новых принятых PNG нет.',next_action,['reports/parody-scenes-2026-11-09.json'],['video-prompts.md','references/scenes/scene-77/manifest.json','references/scenes/scene-77/S77-love-triangle.image-prompt.txt'],focus=False)
a=Path('archive/work-resume-register-archive.json'); trimmed=trim_register(load('work-resume-register.json'),load(a) if a.exists() else {})
if trimmed:
 reg,ar,*_=trimmed;save('work-resume-register.json',reg);save(a,ar)
assert digest(Path('ops/topview-launch-queue.json').read_bytes())==queue_hash
Path('SYNC-TRIGGER.txt').write_text('Owner S77 adult casting correction; '+now+'\n')
print(json.dumps({'scene':77,'prompt_variants':3,'cast':ids,'other_scene_blocks_unchanged':True,'queue_unchanged':True,'new_images_published':0,'master_sha256':digest(master.read_bytes())},ensure_ascii=False))
