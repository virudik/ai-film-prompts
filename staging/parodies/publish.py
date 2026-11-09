#!/usr/bin/env python3
import json, re, sys, hashlib, subprocess, datetime
from pathlib import Path
sys.path.insert(0, 'scripts')
import resume_state

HOLDER = 'chatgpt:ordinary:4ce5446d-f8c0-480f-b26c-fd639124c132'
WORK = 'SEREGIUS-PARODIES-20261109'
DATA = json.loads(Path(sys.argv[1]).read_text())
NOW = datetime.datetime.now(datetime.timezone.utc)
lock = json.loads(Path('ops/canon-lock.json').read_text())
assert lock['state'] == 'held' and lock['holder'] == HOLDER
assert lock['acquired_at'] == '2026-11-09T10:46:14+00:00'
assert datetime.datetime.fromisoformat(lock['expires_at']) > NOW
master_path = Path('video-prompts.md')
master = master_path.read_text()
status = json.loads(Path('project-status.json').read_text())
scenes = DATA['scenes']
assert [s['id'] for s in scenes] == list(range(74, 81))
existing = {int(n) for n in re.findall(r'^## Сцена (\d+)\s', master, re.M)}
assert not existing.intersection(range(74, 81)), 'New IDs already occupied; reread instead of duplicate'
assert not set(status.get('reserved_scene_ids', [])).intersection(range(74, 81))
assert max(existing) == 73, 'Unexpected latest scene; re-evaluate numbering'
queue_before = hashlib.sha256(Path('ops/topview-launch-queue.json').read_bytes()).hexdigest()
identity_paths = {'vitalik':'references/full/vitalik.jpg', 'serega':'references/full/serega.jpg'}


def identity_entries(s):
    return [{'slot':'@Image'+str(i+1),'path':identity_paths[k],'role':'exact '+k+' face and body; wardrobe follows the explicit scene costume','required':True} for i,k in enumerate(s['identities'])]


def image_path(s):
    return 'references/scenes/scene-{0}/S{0}-{1}.png'.format(s['id'],s['slug'])


def all_inputs(s, part=0):
    refs=identity_entries(s)
    refs.append({'slot':'@Image'+str(len(refs)+1),'path':image_path(s),'role':'single new scene staging and props, never overrides identity','required':True})
    if part==2:refs.insert(0,{'slot':'@Video1','path':'actual final 3 seconds of Scene '+str(s['id'])+' Seedance Part 1','role':'real motion/pose continuity, not a generated substitute','required':True})
    return refs


def copy_prompt(s, part=0):
    refs=all_inputs(s,part)
    sec=30 if part==0 else 15
    engine='Wan 3.0 / Seedance 2.5' if part==0 else 'Seedance 2.0'
    start=s['start'] if part in (0,1) else 'Continue the actual last moment of @Video1, without replaying it. Target continuity: '+s['mid']
    end=s['end'] if part in (0,2) else s['mid']
    if part==0:
        events=s['p1']+[re.sub(r'^(\d+)–(\d+)s:', lambda m:str(int(m[1])+15)+'–'+str(int(m[2])+15)+'s:',x) for x in s['p2']]
    else:events=s['p1'] if part==1 else s['p2']
    return '\n\n'.join([
        'Mode: reference-to-video | Duration: '+str(sec)+'s | Resolution: 720p | Aspect ratio: 16:9 | FPS: 24 | Native audio: on\nOptimized for '+engine+' | Photoreal cinematic parody with clear physical comedy',
        'REFERENCES / AUTHORITY:\n'+'\n'.join(x['slot']+' = '+x['path']+' — '+x['role']+'.' for x in refs)+'\nReference images define people, design and staging; do not display them as a slideshow. Generate actual motion.',
        'CHARACTER APPEARANCE / IDENTITY LOCK:\n'+s['appearance'],
        'SCENE / SPACE:\n'+s['location'],
        'START STATE:\n'+start,
        'STORY FLOW:\n'+'\n'.join(events),
        'END STATE:\n'+end,
        'CAMERA / LIGHT / PERFORMANCE:\n'+s['camera']+' Comedy comes from sincere performance, not mugging or ugly facial distortion.',
        'AUDIO:\n'+s['audio']+(' For this part, speak ONLY lines explicitly present in its STORY FLOW; do not preview or repeat another part\u0027s dialogue.' if part else ''),
        'NEGATIVE:\n'+s['negative']+'. No extra limbs, changing identity, clothing drift, new unlisted gag or repeated action loop.',
        'FRAME FILL / NO BARS:\nFull 16:9 landscape edge-to-edge. No letterboxing, pillarboxing, black bars, decorative borders or empty margins.'
    ])


def scene_block(s):
    n=s['id'];refs=all_inputs(s)
    meta={'target_engine':'Wan 3.0','production_state':'DRAFT','duration_s':30,'dialogue':{'enabled':s['dialogue'],'language':'ru' if s['dialogue'] else None},'dependencies':[],'tags':['parody','comedy','owner_authorized_creation','images_pending']}
    l=['<a id="scene-'+str(n)+'"></a>','','## Сцена '+str(n)+' — '+s['title'],'','<!-- scene-meta: '+json.dumps(meta,ensure_ascii=False,separators=(',',':'))+' -->','',
       '**Контекст использования:** '+s['context'],'',
       '**Что происходит:** '+s['summary'],'',
       '**Готовность:** DRAFT. Тексты подготовлены по команде 09.11; отдельный новый постановочный PNG ещё требуется. Это НЕ готовый ролик и НЕ запись в очередь. Основная версия — 30 с Wan 3.0; тот же текст на Seedance 2.5 только по выбору владельца. Альтернатива — 2×15 с Seedance 2.0: P2 ждёт настоящие последние 3 с своей P1. Редакционная приёмка не выполнена.','',
       '**Референсы:** '+'; '.join(x['slot']+' — `'+x['path']+'`' for x in refs)+'. Для нового PNG пока сохранено только точное задание; не выдавать его за изображение.','',
       '**Источники / авторская переработка:** `reports/parody-scenes-source-2026-11-09.json`. Реплики и гэги постановки не являются полной транскрипцией исходных роликов; непрерывный просмотр/звук всех оригиналов не подтверждены.','',
       '<div class="scene-ref-gallery">']
    for x in identity_entries(s):
        l += ['<figure><a href="'+x['path']+'" target="_blank" rel="noopener"><img src="'+x['path']+'" alt="'+x['slot']+' — точная внешность"></a><figcaption>'+x['slot']+' — точная внешность, существующий файл</figcaption></figure>']
    l += ['</div>','','<div class="engine-tabs" data-scene="'+str(n)+'">','','<div class="engine-pane" data-engine="wan30" data-main="1">','',
          '**Входы:** '+'; '.join(x['slot']+' — `'+x['path']+'`' for x in refs)+'.','','```text',copy_prompt(s),'```','','</div>','','<div class="engine-pane" data-engine="sd20x2">','']
    for part in (1,2):
        l += ['#### '+str(n)+' · Seedance 2.0 часть '+str(part),'','**Входы:** '+'; '.join(x['slot']+' — `'+x['path']+'`' for x in all_inputs(s,part))+'.','','```text',copy_prompt(s,part),'```','']
    return '\n'.join(l+['</div>','','</div>',''])

blocks=[scene_block(s) for s in scenes]
rows=['| '+str(s['id'])+' | ['+s['title']+'](#scene-'+str(s['id'])+') | Виталик'+('; Серёга' if 'serega' in s['identities'] else '')+'; новый постановочный PNG ожидается | '+s['summary']+' DRAFT; 30с и 2×15с; без видеозапуска. |' for s in scenes]
lines=master.splitlines();last=max(i for i,l in enumerate(lines) if re.match(r'^\|\s*\d+\s*\|.*\]\(#scene-',l))
lines[last+1:last+1]=rows
master='\n'.join(lines).rstrip()+'\n\n---\n\n'+'\n\n---\n\n'.join(blocks).rstrip()+'\n'
scene_count=len(re.findall(r'^## Сцена \d+\s',master,re.M))
prompt_count=len(re.findall(r'^```(?:text)?\s*$',master,re.M))//2
# Count using canonical fence parser semantics: all opening plain/text fences are prompts.
old_count=len(existing);new_count=old_count+7
old_prompt=int(re.search(r'\*\*\d+ сцен к генерации/доработке · (\d+) полных текстов промта\*\*',master)[1])
master=re.sub(r'\*\*\d+ сцен к генерации/доработке · \d+ полных текстов промта\*\*','**'+str(new_count)+' сцен к генерации/доработке · '+str(old_prompt+21)+' полных текстов промта**',master,count=1)
master=re.sub(r'В active master остаются \*\*\d+ актуальных сцен и \d+ полных текстов промта\*\*','В active master остаются **'+str(new_count)+' актуальных сцен и '+str(old_prompt+21)+' полных текстов промта**',master,count=1)
oldlatest=re.search(r'^- \*\*Последняя оформленная активная сцена:\*\*.*$',master,re.M)
assert oldlatest
master=master[:oldlatest.start()]+'- **Последняя оформленная активная сцена:** 80 — Люкс из кладовки. Новые пародии 74–80 созданы по прямой команде 09.11; DRAFT, референсы в подготовке, 21 новый текст. Видео не запускались; текущая очередь и монтажный порядок не менялись.\n'+oldlatest[0].replace('Последняя оформленная активная сцена:','История предыдущего оформления:',1)+master[oldlatest.end():]
master_path.write_text(master)
source_report=Path('reports/parody-scenes-source-2026-11-09.json')
source_report.write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
character_path=Path('character-references.json');chars=json.loads(character_path.read_text())
for s in scenes:
    n=s['id'];folder=Path('references/scenes/scene-'+str(n));folder.mkdir(parents=True,exist_ok=True)
    (folder/('S'+str(n)+'-'+s['slug']+'.image-prompt.txt')).write_text(s['image_prompt']+'\n')
    refs=[]
    for x in identity_entries(s):
        b=Path(x['path']).read_bytes()
        refs.append({'path':x['path'],'asset_id':x['path'],'caption':x['slot']+' — '+x['role'],'role':'identity','sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'media_type':'image','status':'available','owner_approval':'user_supplied_identity','reused_from_existing_pack':True})
    manifest={'schema_version':2,'project_id':'seregius','scene_id':n,'references':refs,'pending_reference':{'path':image_path(s),'slot':'@Image'+str(len(refs)+1),'status':'needs_generation','caption':s['caption'],'prompt_file':str(folder/('S'+str(n)+'-'+s['slug']+'.image-prompt.txt'))},'approved':[],'rejected':[],'technical_success_is_editorial_approval':False,'updated_at':NOW.isoformat()}
    (folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    for c in chars['characters']:
        if c.get('id') in s['identities'] and n not in c.get('scenes',[]):c.setdefault('scenes',[]).append(n)
character_path.write_text(json.dumps(chars,ensure_ascii=False,indent=2)+'\n')
report_path=Path('reports/parody-scenes-2026-11-09.json');report=json.loads(report_path.read_text())
report.update(state='scenes_authored_images_pending',scene_ids_finalized=True,scene_ids=list(range(74,81)),scene_titles={str(s['id']):s['title'] for s in scenes},prompt_blocks_created=21,source_report=str(source_report),images_created=0,queue_before_sha256=queue_before,updated_at=NOW.isoformat(),next_action='Получить и сохранить семь отдельных пригодных постановочных PNG по image-prompt, с QC/SHA/manifest и привязкой в мастере. Каждый — до следующего. Дополнительные ракурсы при необходимости. Не запускать видео и не выдавать исходный model sheet за новый кадр.')
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
anchor='# 09.11.2026 — пародии 74–80: сцены написаны, изображения ожидаются'
cp=Path('reports/current-work-checkpoint.md');cp.write_text(anchor+'\n\nwork_id: '+WORK+'\n\n- Созданы семь отдельных DRAFT сцен 74–80 и 21 автономный видеопромпт (30с + 2×15с на каждую). Существующие сцены и очередь не менялись.\n- Точные лица Виталика/Серёги повторно не рисуются; семь новых постановочных PNG пока НЕ созданы. Точные задания и manifest сохранены.\n- Источники мемов и границы их проверки: '+str(source_report)+'. Финальное признание в любовном меме — третий персонаж.\n- Следующий шаг: '+report['next_action']+'\n\n---\n\n'+cp.read_text())
resume_state.capture('.',WORK,anchor,'Семь новых сцен и 21 текст сохранены; новые PNG ещё отсутствуют.',report['next_action'],[str(report_path),str(source_report)],[str(source_report),'video-prompts.md'],False)
regp=Path('work-resume-register.json');reg=json.loads(regp.read_text());w=next(w for w in reg['active_work'] if w['work_id']==WORK);w['status']='awaiting_image_references';w['scene_ids']=list(range(74,81));regp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
hp=Path('NEW-CHAT-HANDOFF.md');h=hp.read_text();mark='### Новое с последней чистки (дописывать сюда, одной строкой с датой)'
assert mark in h
h=h.replace(mark,mark+'\n\n- **09.11 — пародии 74–80:** создано 7 DRAFT сцен/21 текст, PNG ещё ожидаются; не дублировать. `reports/parody-scenes-2026-11-09.json`; видео не разрешены этим поручением.',1)
assert len(h.encode())<35000,'Handoff size limit; shorten new line rather than archive unrelated history'
hp.write_text(h)
fp=Path('ops/FUTURE-PLANS.md');plans=fp.read_text();assert 'SEREGIUS-PARODIES-20261109' not in plans
plans += '\n\n## Прямое поручение 09.11 — пародии Серёгиуса\n\n- **SEREGIUS-PARODIES-20261109:** семь сцен 74–80 и 21 текст созданы; повторно не создавать. Семь новых постановочных PNG, их QA и публикация ещё открыты. Доказательства/последний этап — `reports/parody-scenes-2026-11-09.json`, `reports/current-work-checkpoint.md`. Запуск видео не выполнялся и очередь не расширялась.\n'
fp.write_text(plans)
sha=hashlib.sha256(master_path.read_bytes()).hexdigest()
Path('SYNC-TRIGGER.txt').write_text(NOW.isoformat()+' Owner parody scenes 74–80; SHA256 '+sha+'. Validate canonical master and publish Pages; no launches.\n')
assert hashlib.sha256(Path('ops/topview-launch-queue.json').read_bytes()).hexdigest()==queue_before
print(json.dumps({'scene_ids':list(range(74,81)),'new_prompts':21,'images_created':0,'master_sha256':sha,'queue_unchanged':True},ensure_ascii=False))
