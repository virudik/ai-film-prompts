#!/usr/bin/env python3
"""Owner-requested HONOR 4/5 completion; no media launch, contest submission or approval."""
import copy, hashlib, io, json, os, re, subprocess, sys, unittest
from datetime import datetime, timezone
from pathlib import Path
P=Path('projects/raznoe');R4=P/'references/scenes/scene-4';R5=P/'references/scenes/scene-5'
HOLDER='chatgpt:ordinary:79b0c146-b9a1-46f2-8187-6be9bd781ec4'
DECISION='https://docs.google.com/document/d/1XGoOGxapUSm8Kf_uDY7W4HoSkNsORTV3ezDhkdAVooc/edit'
OUT=Path('/tmp/honor-completion');OUT.mkdir(exist_ok=True)
REPORT=str(P/'reports/honor-scenes-4-5-completion.json')
def now():return datetime.now(timezone.utc).isoformat(timespec='seconds')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,o):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def save(p,s):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def lease():
 for p in ['ops/canon-lock.json',str(P/'canon-lock.json')]:
  x=json.loads(Path(p).read_text());assert x['state']=='held' and x['holder']==HOLDER,p
  assert datetime.fromisoformat(x['expires_at'])>datetime.now(timezone.utc),p+' expired'
def run(name,args):
 x=subprocess.run(args,text=True,capture_output=True);(OUT/(name+'.log')).write_text(x.stdout+x.stderr)
 assert x.returncode==0,name+': '+(x.stdout+x.stderr)[-2000:]
 return {'name':name,'exit_code':x.returncode}
def blocks(s):return re.findall(r'```text\n(.*?)```',s,re.S)
CONTRACT='''PRODUCT / COMPOSITING LOCK — CRITICAL:
This generation is a BACKGROUND PLATE, not the final product advertisement. The selected product is HONOR Magic9 Pro Max, Moss Green. When a rectangle is called for, keep a featureless matte tracking placeholder and clean separation from foreground ribbons. Do not generate handset details, lenses, lettering or a fictional phone.
EDITOR SOURCES (not extra generator image slots): H-BACK is the exact 3000x3000 RGBA rear original, Drive file 19QIyFClHQWCy5zfMsVe1oaW2dhXwpzPI. H-FRONT-ANGLE is the exact 3000x3000 RGBA front-left original, Drive file 1XinDbUtQmpMhNc7PW9PnM-KFD4nFfKxg. It is oblique, NOT an orthographic front. Source URLs and SHA256 are registered in projects/raznoe/references/scenes/scene-4/official-product-source-links.json. These are private technical sources, not cleared commercial artwork.
FINAL COMPOSITE: remove the placeholder and place exact source product pixels in editing. Rear source for the reveal; straight editorial cut to the existing front-left perspective at film time 105s. No invented 360-degree rotation, hidden side, stretched phone, mirrored labels or doubled handset. Camera close-up comes only from the rear source. Final 105–120s product layer is stable and the last 5s remain readable. Brand title is a separate editing layer, not a counterfeit official vector. Rights clearance and editorial acceptance are still required.
Gold, rain and ink are metaphors, not proof of durability, camera performance or battery life. No finished output may retain a placeholder or claim that an unmade composite is complete.'''
S4INFO='''<a id="honor-4-production"></a>
### Доводка: точный продукт вместо пустого финала

**Модель определена:** HONOR Magic9 Pro Max, Moss Green. Во всех 36 промптах разделены фоновая генерация и точный продуктовый слой. [Полная карта монтажа и проверки](projects/raznoe/references/scenes/scene-4/production-package.md) описывает все 24 участка трёх вариантов по 120 с.

**Технические исходники есть:** [H-BACK — сзади](https://drive.google.com/file/d/19QIyFClHQWCy5zfMsVe1oaW2dhXwpzPI/view), [H-FRONT-ANGLE — передний левый ракурс](https://drive.google.com/file/d/1XinDbUtQmpMhNc7PW9PnM-KFD4nFfKxg/view), [H-34 — сравнение двух сторон](https://drive.google.com/file/d/1pYRa-H6rsA5-1kncKAejE7JGkTAskAMN/view). Это официальные PNG для приватной технической работы, не новые картинки генератора и не лицензия на рекламу. Публичных канонических продуктовых PNG нет; источники не копируются на открытый сайт. Старое задание `H-BACK.image-prompt.txt` сохранено, но неудачные перерисовки повторять не требуется.

H-CAM — деталь из того же H-BACK, без выдуманных линз. H-FRONT используется под исходным углом, не как искусственный анфас. H-34 не является кадром одного телефона. H-LOGO не имитируется: название модели набирается отдельно в монтаже. [Слоты и точный метод](projects/raznoe/references/scenes/scene-4/product-compositing.json).

Исходные 15 реплик сохранены дословно. [Активная редакционная карта](projects/raznoe/references/scenes/scene-4/production-voiceover.json) меняет четыре строки для именного финала. Это предложение автора, не утверждено; старый и новый финал одновременно не звучат.

**Граница готовности:** тексты, источники и монтажный план подготовлены; MP4, настоящие стыки, продуктовые композиты, записанный голос и полный просмотр ещё не выполнены. DRAFT / not_approved остаётся. Очереди и разрешения запуска не изменены.

'''
def main():
 lease();source_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
 master=P/'video-prompts.md';old=master.read_text();a=old.index('<a id="scene-4"></a>');b=old.index('<a id="scene-5"></a>');s4=old[a:b];s5=old[b:]
 assert 'id="honor-4-production"' not in s4,'Already applied; verify existing publication, do not duplicate'
 assert len(blocks(s4))==36 and len(blocks(s5))==3
 protected_paths=[Path('video-prompts.md'),Path('review-ledger.json'),Path('ops/topview-launch-queue.json'),P/'review-ledger.json',P/'ops/topview-launch-queue.json',R4/'filmwide-voiceover-120s.json']+list(R4.glob('0*.png'))
 protected={str(p):sha(p) for p in protected_paths}
 for p in ['NEW-CHAT-HANDOFF.md','SYNC-RUNBOOK.md','AI-PROJECT-GUIDE.md','PROMPT-STYLE-GUIDE.md','USER-GUIDE.md','README-AI-SYNC.md','BACKUP-AI-RUNBOOK.md']:protected[p]=sha(p)
 oldlock=re.search(r'PRODUCT / PROXY LOCK — CRITICAL:\n.*?(?=\n\n)',s4,re.S).group(0);assert s4.count(oldlock)==36;s4=s4.replace(oldlock,CONTRACT)
 i=s4.index('**Чего нет, без пустых ссылок:**');j=s4.index('<a id="honor-4-3d"></a>',i);s4=s4[:i]+S4INFO+s4[j:]
 s4=s4.replace('**Статус:** DRAFT, not_approved. Не снято и не готово к производству без модели и слотов ниже.','**Статус:** DRAFT, not_approved. Модель и технические источники закреплены; реальное видео, композит, права выпуска и приёмка остаются открыты.')
 s4=s4.replace('**Монтаж:** слот H-FRONT ставится на финальное удержание. Логотип и титр — отдельным слоем. Пока файлов нет, в кадре остаётся пустой прокси.','**Монтаж:** H-BACK и H-FRONT-ANGLE ставятся по product-compositing.json. Исходники доступны в приватной папке. Прокси допустим только на фоновой пластине, не в выпускном ролике. Финальные титры и реплики — по production-package.md и production-voiceover.json.')
 s4=s4.replace('**Границы 10.11.2026.**','**Границы до доработки (история 10.11.2026).**',1)
 s4=s4.replace('**Кадр за кадром.**','**Кадр за кадром — фоновая пластина; конечный продуктовый слой по карте выше.**')
 s4=s4.replace('**Закадр — предложение автора, не утверждено, не факт о товаре.**','**Исходный закадр для истории — предложение автора, не утверждено, не факт о товаре. Активные четыре замены — в production-voiceover.json.**')
 match=re.search(r'<!-- scene-meta: (\{.*?\}) -->',s4);meta=json.loads(match.group(1));meta['target_engine']='Wan 3.0';meta['tags']=[x for x in meta['tags'] if x!='mood_refs_only']+['exact_product_compositing','private_technical_sources','final_video_pending'];s4=s4.replace(match.group(0),'<!-- scene-meta: '+json.dumps(meta,ensure_ascii=False,separators=(',',':'))+' -->',1)
 original_voice=json.loads((R4/'filmwide-voiceover-120s.json').read_text());active=copy.deepcopy(original_voice)
 for fi,li,text in [(0,4,'HONOR Magic9 Pro Max. В центре вашего кадра.'),(1,3,'Город движется. Ваш кадр остаётся.'),(1,4,'HONOR Magic9 Pro Max. Свой ритм. Свой кадр.'),(2,4,'HONOR Magic9 Pro Max. Продолжение — в ваших руках.')]:
  x=active['films'][fi]['voice_lines'][li];x['previous_text_ru']=x['text_ru'];x['text_ru']=text
 active.update(source='Editorial completion: 11 original lines kept, four named-product revisions proposed; all original15 preserved in filmwide-voiceover-120s.json',updated_at=now(),editorial_status='not_approved',original_source_sha256=sha(R4/'filmwide-voiceover-120s.json'));dump(R4/'production-voiceover.json',active)
 src4=json.loads((R4/'official-product-source-links.json').read_text());by_slot={x['slot']:x for x in src4['private_source_copies']['items']}
 mapping={'schema_version':1,'project':'raznoe','scene_id':4,'product':'HONOR Magic9 Pro Max','color':'Moss Green','method':'background_generation_plus_exact_source_pixel_compositing','updated_at':now(),'films':3,'seconds_per_film':120,'generation_prompts':36,'slots':{'H-BACK':{'drive_id':'19QIyFClHQWCy5zfMsVe1oaW2dhXwpzPI','sha256':by_slot['H-BACK']['sha256'],'state':'private_source_available','role':'rear product pixel layer'},'H-FRONT':{'drive_id':'1XinDbUtQmpMhNc7PW9PnM-KFD4nFfKxg','sha256':by_slot['H-FRONT']['sha256'],'state':'private_source_available','role':'front-left perspective, not orthographic front','working_alias':'H-FRONT-ANGLE'},'H-CAM':{'source_slot':'H-BACK','state':'source_region_available_crop_not_exported'},'H-34':{'drive_id':'1pYRa-H6rsA5-1kncKAejE7JGkTAskAMN','state':'comparison_only','not_single_frame_input':True},'H-LOGO':{'state':'not_supplied_not_required_for_plain_model_name'}},'composite_timeline':{'3d':[{'start':30,'end':90,'source':'H-BACK'},{'start':90,'end':105,'source':'H-CAM'},{'start':105,'end':120,'source':'H-FRONT-ANGLE'}],'realism':[{'start':75,'end':105,'source':'H-BACK'},{'start':105,'end':120,'source':'H-FRONT-ANGLE'}],'drawn':[{'start':90,'end':105,'source':'H-BACK'},{'start':105,'end':120,'source':'H-FRONT-ANGLE'}]},'rights_cleared':False,'final_composites_created':False,'video_created':False,'editorial_approval':False,'paid_actions_allowed':False};dump(R4/'product-compositing.json',mapping)
 m4=json.loads((R4/'manifest.json').read_text());m4.update(title='HONOR Magic9 Pro Max',status='editorial_package_with_private_product_sources',updated_at=now(),production_ready=False,product_compositing=str(R4/'product-compositing.json'),technical_source_slots=mapping['slots'],missing_slots=[],unresolved_deliverables=['commercial_source_rights','actual_video_clips_and_tails','product_composites','recorded_voice_and_sound','full_motion_audio_QC','owner_acceptance']);dump(R4/'manifest.json',m4)
 plan5=(R5/'shooting-package.md').read_text();comment=next(line[2:] for line in plan5.splitlines() if line.startswith('> Город: Москва.'))
 s5=s5.replace('· «Город проверяет» (конкурс','· «Дворовая машина Голдберга» (конкурс',1)
 s5=s5.replace('Публикация без подтверждённого города и согласования участия не выполняется.','Город и идея — Москва / «Дворовая машина Голдберга» по сохранённому согласованию t529. Отправка и допуск организатора остаются отдельными действиями.')
 s5=s5.replace('Сцена 4 Magic9 Pro Max и RESOURCE не изменены.','Это отдельный конкурсный ролик, не реклама Magic9 и не RESOURCE.')
 i=s5.index('**Ждёт владельца.**');j=s5.index('**Навигация:**',i)
 insert='''<a id="honor-5-production"></a>
### Согласованный замысел и рабочий пакет

**Москва — «Дворовая машина Голдберга».** Источник: [согласованная заявка от 10.11.2026](DECISION). Одиночная горка ранее отклонена как скучная. Решение владельца не равно техническому допуску организатора. Заявка не отправлена: источник требует отдельной команды «отправляй».

[Полный сценарий 90 с, заявка и лист проверки](projects/raznoe/references/scenes/scene-5/shooting-package.md) · [источники и SHA](projects/raznoe/references/scenes/scene-5/official-product-source-links.json) · [папка сцены5 в «Хонор»](https://drive.google.com/drive/folders/1h6Jfpznn_CME22IReM8VjLempjkQjgpm).

**Технические виды:** [X-BACK](https://drive.google.com/file/d/19VmU-oOfN91PTR2QE5t4YZsRhEDbh3yf/view) и [X-FRONT](https://drive.google.com/file/d/1DVs38N_X58mSOT-cjJyHlpChRPvZcKHL/view). Оригинальные 255×532 пикселя производителя без синтеза деталей. Это сверка формы, не кадры теста и не крупный рекламный план. Реальный цвет определяется выданным телефоном, не фиолетовым примером.

**Физика не доказана:** песок сам не отправляет аппарат в жёлоб; траектория качелей и вся цепочка требуют репетиции муляжом и согласования. Непрерывный звонок под водой не обещается. Повреждение/нагрев — стоп, без воды и зарядки. Дождь, мороз, удачный результат и экран не подделывать. Реальное видео остаётся неснятым.

'''.replace('DECISION',DECISION)
 s5=s5[:i]+insert+s5[j:]
 s5=s5.replace('07.11.2026 прочитан полный текст','Полный текст повторно перечитан при доработке; ранее 07.11.2026 прочитан полный текст',1)
 i=s5.index('<a id="honor-5-idea"></a>');j=s5.index('<a id="honor-5-vk"></a>',i)
 s5=s5[:i]+'''<a id="honor-5-idea"></a>
### Идея — Москва, «Дворовая машина Голдберга»

Согласованный замысел: горка на ледянке → качели → песочница → жёлоб → задуманный водный финиш. Это идея, не доказательство работающей механики или прочности телефона. Репетиция муляжом и разрешение организатора обязательны. Самовольно менять цепь на одиночную горку нельзя.

<a id="honor-5-plan"></a>
### Реальная съёмка · 90 с · 9:16

| Время | Кадр | Проверка |
|---|---|---|
| 0–10 | Автор: Москва, цепь Голдберга, общий маршрут | Закрытая нейтральная площадка без детей, чужих лиц/логотипов |
| 10–22 | Один телефон до теста: корпус, экран, камера, статус звонка | Настоящий аппарат; никаких ИИ-экранов и подмен |
| 22–52 | Отрепетированная согласованная цепь одним контрольным дублем | Аппарат виден; без склейки в воздействии, скрытой помощи и выдуманных переходов |
| 52–75 | Первая проверка в том же дубле | Только реальный результат; дефект или обрыв связи не скрывать |
| 75–90 | Честный итог | «Это результат одного сегодняшнего испытания, а не обещание для любых условий» |

[Все реплики и требования сдачи](projects/raznoe/references/scenes/scene-5/shooting-package.md). Погода настоящая, музыки нет. Лабораторный рейтинг не является разрешением на цепь «удары, затем ледяная вода». После повреждения/нагрева — стоп, без воды/зарядки. Сухой запасной финал — предложение для согласования, а не незаметная замена выбранного замысла.

'''+s5[j:]
 i=s5.index('### Черновик комментария для ВК');j=s5.index('<a id="honor-5-preview"></a>',i)
 s5=s5[:i]+'### Согласованный текст для ВК — НЕ отправлен\n\n> '+comment+'\n\nИсточник: [t529]('+DECISION+'). Перед отправкой отдельно согласовать выявленные механические и водные ограничения. Не публиковать автоматически и не выдавать правку за уже согласованную.\n\n'+s5[j:]
 s5=s5.replace('Официальных фото X9e Pro в этих блоках нет.','Официальные источники сохранены отдельно для технической сверки. В эти генеративные блоки они не подаются: муляж и схема площадки не подменяют конкурсный аппарат.')
 bb=blocks(s5);assert len(bb)==3
 flows=[
 '0–8s: anonymous adult holds a blank dummy in the right gloved hand beside a closed empty rehearsal set. 8–20s: lateral survey reveals the planned slide exit, stationary swing, sand tray and gutter in order. The dummy stays held; no mechanism is activated. 20–30s: return to the adult and a neutral inspection surface. This is set planning, not proof of a working chain or device durability. No impacts, immersion or call UI.',
 'One portrait tracking shot surveys the closed rehearsal set. The same anonymous adult holds a blank dummy in the right gloved hand. Reveal the slide exit and stationary swing; begin a lateral move toward the sand tray and gutter. No launching, impact or actuation. The real concept is a Moscow Goldberg chain; this illustration does not prove feasibility.',
 'Continue the actual part-1 lateral camera move past the stationary sand tray and gutter to a neutral inspection surface. The same adult still holds the same dummy in the right hand. End on a steady layout view. No chain reaction, impact, immersion, generated product UI or claimed successful test.'
 ]
 for idx,body in enumerate(bb):
  if idx==0:body=re.sub(r'STORY / CAMERA:\n.*?(?=\n\nPERFORMANCE:)','STORY / CAMERA:\n'+flows[idx],body,flags=re.S)
  else:body=re.sub(r'STORY FLOW:\n.*?(?=\n\nEND STATE:)','STORY FLOW:\n'+flows[idx],body,flags=re.S)
  body=body.replace('No official product reference exists.','Official product source images are kept separately for technical review, not used to fake a real test.')
  body=body.replace('The place is a plausible GENERIC Russian town, not footage of a particular real city.','Moscow is the planned real city; this generic closed set contains no identifiable architecture and is not documentary Moscow footage.')
  body=body.replace('One continuous generic city environment in cool natural weather.','One continuous closed unbranded rehearsal set in natural overcast weather.')
  body=body.replace('and the same generic wet city walkway direction.','and the same closed rehearsal set and lateral camera direction.')
  if idx>0:
   start='Anonymous adult holds the blank dummy near the closed set; dark jacket, black gloves, no identifiable face.' if idx==1 else 'Continue actual last three seconds of part 1 beside the stationary sand tray and gutter. Dummy in the right gloved hand; no repeated action.'
   end='Camera begins passing the stationary sand tray toward the gutter. Adult still holds the dummy; readable last three seconds for handoff.' if idx==1 else 'Steady portrait view of the adult holding the dummy above a neutral inspection surface; no test result claimed.'
   body=re.sub(r'START STATE:\n.*?(?=\n\n)','START STATE:\n'+start,body,flags=re.S);body=re.sub(r'END STATE:\n.*?(?=\n\n)','END STATE:\n'+end,body,flags=re.S)
  s5=s5.replace('```text\n'+bb[idx]+'```','```text\n'+body+'```',1)
 match=re.search(r'<!-- scene-meta: (\{.*?\}) -->',s5);meta=json.loads(match.group(1));meta['tags']+=['moscow_goldberg_owner_concept','physical_rehearsal_pending'];meta['dialogue']={'enabled':True,'language':'ru'};s5=s5.replace(match.group(0),'<!-- scene-meta: '+json.dumps(meta,ensure_ascii=False,separators=(',',':'))+' -->',1)
 assert '[ГОРОД]' not in s5
 save(master,old[:a]+s4+s5)
 src=json.loads((R5/'official-product-source-links.json').read_text());src.pop('drive_readback_verified_at',None);src['drive_readback_verified_on']='2026-11-10';dump(R5/'official-product-source-links.json',src)
 dump(R5/'manifest.json',{'schema_version':2,'project_id':'raznoe','scene_id':5,'title':'HONOR X9e Pro — Москва, Дворовая машина Голдберга','production_state':'DRAFT','editorial_approval':False,'video_launch_approval':False,'contest_submitted':False,'real_shoot_complete':False,'references':[],'technical_sources':src['items'],'official_sources_are_not_test_footage':True,'approved_concept_record':{'city':'Москва','concept':'Дворовая машина Голдберга','source':DECISION,'source_record_date':'2026-11-10','source_owner_message':'t529','organizer_technical_approval':False},'drive_folder':src['drive_folder'],'required_actual_material':['received_test_phone','approved_rehearsed_physical_chain','real_uninterrupted_control_take','actual_after_test_checks'],'optional_ai_preview':{'prompts':3,'duration_s':30,'competition_entry':False,'part_2_requires_actual_part_1_tail':True},'updated_at':now()})
 assert old[:a]==master.read_text()[:master.read_text().index('<a id="scene-4"></a>')]
 assert len(blocks(s4))==36 and len(blocks(s5))==3 and all(sha(p)==v for p,v in protected.items())
 # Test the new approved city/source-directory contract without disabling unrelated checks.
 test=Path('tests/test_raznoe_honor_scene4.py');tt=test.read_text();tt=tt.replace('self.assertIn("[ГОРОД]", contest)','self.assertNotIn("[ГОРОД]", contest)\n        self.assertIn("Москва", contest)\n        self.assertIn("Дворовая машина Голдберга", contest)');tt=tt.replace('self.assertNotIn("scene-5/", contest)','self.assertIn("scene-5/shooting-package.md", contest)');tt=tt.replace('self.assertFalse((ROOT / "projects/raznoe/references/scenes/scene-5").exists())','self.assertTrue((ROOT / "projects/raznoe/references/scenes/scene-5/manifest.json").is_file())\n        manifest = json.loads((ROOT / "projects/raznoe/references/scenes/scene-5/manifest.json").read_text())\n        self.assertFalse(manifest["contest_submitted"])\n        self.assertFalse(manifest["real_shoot_complete"])\n        self.assertEqual(len(manifest["technical_sources"]), 2)\n        self.assertTrue(all(x["drive_readback_match"] for x in manifest["technical_sources"]))\n        self.assertEqual(scene.count("PRODUCT / COMPOSITING LOCK"), 36)');save(test,tt)
 done='HONOR4: 36 фоновых промптов связаны с точными исходниками и картой продуктового композита; 15 исходных реплик сохранены, 4 редакционные замены отдельно. HONOR5: Москва/машина Голдберга перенесены из согласования t529; два источника X9e сохранены и проверены на Drive, сценарий90с и технические ограничения опубликованы. Это подготовка, не реальные видео/конкурсная отправка.'
 next4='Не повторять 36 промптов и загрузку существующих официальных источников. Выпуск Magic9 требует прав, разрешённого выбора сетки генерации, реальных клипов/стыков, композита, записи голоса, полного QC и приёмки. RESOURCE этим проходом не закрыт.'
 next5='Не спрашивать заново город: Москва. Сохранённая идея — Дворовая машина Голдберга. Нужны отдельная команда отправки, принятие правил владельцем, согласование нагрузки/воды организатором, рабочая репетиция муляжом, получение аппарата и настоящая съёмка90с без музыки. ИИ не доказывает результат.'
 report={'schema_version':1,'project':'raznoe','scope':[4,5],'checked_at':now(),'source_head':source_head,'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'source_master_sha256':hashlib.sha256(old.encode()).hexdigest(),'master_sha256':sha(master),'scene4':{'prompt_count':36,'production_method':mapping['method'],'existing_official_source_images':3,'original_voice_lines_preserved':15,'proposed_voice_line_revisions':4,'new_generated_product_images':0,'final_videos':0,'rights_cleared':False,'owner_approved':False},'scene5':{'city':'Москва','concept':'Дворовая машина Голдберга','decision_source':DECISION,'official_source_images_with_drive_readback':2,'shooting_script_duration_s':90,'ai_preview_prompts':3,'contest_submitted':False,'physical_test_done':False},'no_video_launches':True,'credits_spent':0,'protected_files':protected,'scenes1_2_3_unchanged':True,'editorial_preparation_done':True,'full_task_complete':False,'remaining':[next4,next5],'live_publication_verified':False}
 dump(REPORT,report)
 hand=P/'HANDOFF.md';h=hand.read_text();note='**HONOR: актуальная доработка.** '+done+' Подробности `reports/honor-scenes-4-5-completion.json`; состояние продолжения — в checkpoint/register. Старые строки ниже не возвращают город к [ГОРОД] и не отменяют новые источники.\n\n';save(hand,note+h)
 # Project-specific overview only; shared seven instructions stay byte-identical.
 ins=P/'INSTRUCTIONS.md';it=ins.read_text();it=it.replace('Сцена 4 HONOR — три ролика по 120 с, модель не выбрана;','Сцена 4 HONOR Magic9 Pro Max — три ролика по120с, точный продукт отдельным композитным слоем по references/scenes/scene-4/production-package.md; сцена5 HONOR X9e Pro — Москва, Дворовая машина Голдберга, реальное90с без музыки;');save(ins,it)
 anchor='# HONOR 4–5 — доработка пакетов, Москва и точные продуктовые источники'
 cp=P/'reports/current-work-checkpoint.md';assert anchor not in cp.read_text();save(cp,anchor+'\n\nwork_id: RAZNOE-HONOR-X9EPRO-CONTEST-20261107\n\n- '+done+'\n- Доказательство: '+REPORT+'\n- Следующий шаг: '+next5+'\n- Сцена4: '+next4+'\n\nchecked_at: '+now()+'\n\n---\n\n'+cp.read_text())
 sys.path.insert(0,str(Path('scripts').resolve()));from resume_state import capture
 capture('.', 'RAZNOE-HONOR-X9EPRO-CONTEST-20261107',anchor,done,next5,[REPORT],[str(R5/'shooting-package.md'),str(R4/'production-package.md')],True,project='raznoe')
 rp=P/'work-resume-register.json';reg=json.loads(rp.read_text())
 for w in reg['active_work']:
  if w['work_id']=='RAZNOE-HONOR-X9EPRO-CONTEST-20261107':w['status']='preproduction_updated_waiting_submission_rehearsal_and_real_phone';w['next_action']=next5
  if w['work_id']=='RAZNOE-RESOURCE-HONOR-SASHA-20261106':w['latest_update']={'checked_at':now(),'result':done,'evidence':[REPORT],'next_action':next4};w['next_action']=next4
 reg['last_updated_at']=now();dump(rp,reg)
 validations=[run('project-status',['python3','scripts/projects.py','.','status','--project','raznoe','--write']),run('resume-packet',['python3','scripts/build_resume_packet.py','.','--project','raznoe']),run('preflight',['python3','scripts/continue_preflight.py','.','--project','raznoe']),run('site',['python3','scripts/validate_site.py','.']),run('instructions',['python3','scripts/check_instruction_consistency.py','.']),run('projects',['python3','scripts/projects.py','.','validate'])]
 sys.path.insert(0,str(Path('.').resolve()));stream=io.StringIO();suite=unittest.defaultTestLoader.discover('tests');result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite);(OUT/'tests.log').write_text(stream.getvalue())
 tests={'checked_at':now(),'tests_run':result.testsRun,'failures':[t.id() for t,_ in result.failures],'errors':[t.id() for t,_ in result.errors],'skipped':[t.id() for t,_ in result.skipped],'all_tests_passed':result.wasSuccessful()}
 dump(OUT/'tests.json',tests);assert result.wasSuccessful() and result.testsRun>=538 and not result.skipped,tests
 assert all(sha(p)==v for p,v in protected.items()),'unrelated protected file changed';lease()
 report.update(checked_at=now(),validations=validations,tests=tests);report['files']={str(p):sha(p) for p in [master,R4/'manifest.json',R4/'production-package.md',R4/'product-compositing.json',R4/'production-voiceover.json',R5/'manifest.json',R5/'shooting-package.md',R5/'official-product-source-links.json']};dump(REPORT,report)
 run('resume-packet-final',['python3','scripts/build_resume_packet.py','.','--project','raznoe']);run('preflight-final',['python3','scripts/continue_preflight.py','.','--project','raznoe'])
 # Explicit stage list, never git add .
 paths=[str(master),str(R4/'manifest.json'),str(R4/'product-compositing.json'),str(R4/'production-voiceover.json'),str(R5/'manifest.json'),str(R5/'official-product-source-links.json'),REPORT,str(hand),str(ins),str(cp),str(rp),str(P/'project-status.json'),str(P/'shadow/resume-packet.md'),str(P/'shadow/resume-packet.json'),str(test)]
 subprocess.run(['git','add','--',*paths],check=True)
 dump(OUT/'publication-report.json',report)
 print(json.dumps({'tests':tests,'scope':[4,5],'prepared':True,'final_videos':False,'contest_submitted':False}))
if __name__=='__main__':main()
