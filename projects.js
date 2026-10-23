// Several film projects on one site (owner decision 20.10.2026). Rules: projects/README.md.
// Registry: projects/projects.json (this list must match it; tests/test_projects.py checks).
// «Серёгиус» lives in the repository root as before; every other project in projects/<id>/.
// The pages stay the same: this script runs first and, for another project (?p=<id>), points their
// data requests at the project's folder, filters the shared files (Topview telemetry, task inbox,
// owner-button list) by project and tags the owner buttons with the project. No generation, no approval.
(function(){
'use strict';
var PROJECTS=[
 {id:'seregius',name:'Серёгиус',emoji:'🎬',root:'',about:'основной фильм'},
 {id:'kotmonavty',name:'Котмонавты',emoji:'🐱🚀',root:'projects/kotmonavty/',about:'спин-офф про котов'},
 {id:'kot-detektiv',name:'Кот детектив',emoji:'🕵️🐈',root:'projects/kot-detektiv/',about:'кот-сыщик'},
 {id:'raznoe',name:'Роскосмос',emoji:'🚀',root:'projects/raznoe/',about:'космические организации'},
 {id:'misc',name:'Разное',emoji:'🎲',root:'projects/misc/',about:'независимые ролики'}
];
var ROOT='seregius',SLOTS=6;
var API_HOST='https://vzohfatqzyioydtgjiyd.supabase.co/functions/v1/owner-decision';
var want=null;try{want=new URLSearchParams(location.search).get('p')}catch(e){}
var P=PROJECTS.filter(function(x){return x.id===want})[0]||PROJECTS[0];
var OTHER=P.id!==ROOT;
// files every project has in its own folder (root path -> path inside projects/<id>/)
var MAP={'video-prompts.md':'video-prompts.md','project-status.json':'project-status.json','review-ledger.json':'review-ledger.json',
 'film-order.json':'film-order.json','character-references.json':'character-references.json',
 'ops/topview-launch-queue.json':'ops/topview-launch-queue.json','ops/canon-lock.json':'canon-lock.json'};
var origFetch=window.fetch.bind(window);
function fresh(u){return origFetch(u+'?fresh='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
function reply(obj){return new Response(JSON.stringify(obj),{status:obj?200:404,headers:{'content-type':'application/json'}})}
var telP=null,telAt=0;
function telemetry(){if(!telP||Date.now()-telAt>60000){telAt=Date.now();telP=fresh('projects/topview-projects.json').then(function(t){return t||{active:[],recent:[]}})}return telP}
function rowProject(r,tel){
 var tid=String((r&&r.task_id)||'');
 if(tid&&tel){var all=(tel.active||[]).concat(tel.recent||[]);for(var i=0;i<all.length;i++)if(all[i].task_id===tid&&all[i].project)return all[i].project}
 var v=String((r&&r.value)||'');if(v.indexOf('project:')===0)return v.slice(8).trim()||ROOT;
 var n=String((r&&r.note)||''),m=n.match(/^\s*\[проект:\s*([a-z0-9-]+)\]/i);if(m)return m[1].toLowerCase();
 if(r&&r.action==='ref_feedback'){m=n.match(/^\s*projects\/([a-z0-9-]+)\//);if(m)return m[1]}
 return ROOT}
function sharedSlots(rootTv,tel){
 var rootOcc=Number(rootTv&&rootTv.occupied_slots);if(!Number.isFinite(rootOcc))rootOcc=((rootTv&&rootTv.active_tasks)||[]).length;
 var others=(tel.active||[]).length,mine=(tel.active||[]).filter(function(t){return t.project===P.id}).length;
 return {occupied:rootOcc+others,free:Math.max(0,SLOTS-rootOcc-others),mine:OTHER?mine:rootOcc,others:OTHER?rootOcc+others-mine:others}}
var SHARED=null;
// ---- synthetic files for another project
function synthTopview(){return Promise.all([fresh('topview-status.json'),telemetry()]).then(function(x){
 var root=x[0]||{},tel=x[1];SHARED=sharedSlots(root,tel);
 var act=(tel.active||[]).filter(function(t){return t.project===P.id});
 var tasks=act.map(function(t){return {scene_id:Number(t.scene_id),task_id:t.task_id,model:t.model,topview_status:String(t.status||'init').toLowerCase(),
  started_at:t.started_at||null,queue_count:t.queue_count==null?null:t.queue_count,topview_estimated_wait_seconds:t.wait_seconds==null?null:t.wait_seconds,
  checked_at:tel.checked_at||root.checked_at||null,verified:true,mapping_confidence:t.confidence||'robot',part:t.part||null}});
 var scenes={};(tel.recent||[]).filter(function(t){return t.project===P.id}).forEach(function(t){var k=String(t.scene_id);
  if(!scenes[k]||String(t.finished_at||'')>String(scenes[k].completed_at||''))scenes[k]={task_id:t.task_id,topview_status:String(t.final_status||'').toLowerCase(),completed_at:t.finished_at||null,started_at:t.started_at||null,model:t.model||null}});
 return {schema_version:3,project:P.id,source:'projects/topview-projects.json',checked_at:root.checked_at||tel.checked_at||null,timezone:'MSK',
  scenes:scenes,slot_capacity:SLOTS,occupied_slots:tasks.length,free_slots:Math.max(0,SLOTS-tasks.length),active_tasks:tasks,task_parts:{},
  note:'Задачи проекта «'+P.name+'». Слоты Topview общие на все проекты: занято '+SHARED.occupied+' из '+SLOTS+'.'}})}
function synthTaskMap(){return telemetry().then(function(tel){
 return {schema_version:3,project:P.id,active_by_scene:{},processed_tasks:(tel.recent||[]).filter(function(t){return t.project===P.id}).map(function(t){
  return {scene_id:Number(t.scene_id),task_id:t.task_id,final_status:t.final_status,finished_at:t.finished_at||null,model:t.model||null}}),slot_capacity:SLOTS}})}
// ---- shared files filtered by project (also in Серёгиус: it no longer sees the other projects' rows)
function synthInbox(q){return origFetch('ops/owner-tasks.json'+q,{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null}).then(function(j){
 if(!j)return null;j.tasks=(j.tasks||[]).filter(function(t){return (t.project||ROOT)===P.id});return j})}
function synthRobot(q){return Promise.all([origFetch('shadow/topview-robot-status.json'+q,{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null}),telemetry()]).then(function(x){
 var s=x[0],tel=x[1];if(!s)return null;var mine=new Set((tel.active||[]).filter(function(t){return t.project===P.id}).map(function(t){return t.task_id}));
 var anyProj=new Set((tel.active||[]).map(function(t){return t.task_id}));
 s.active_tasks=(s.active_tasks||[]).filter(function(t){return OTHER?mine.has(t.task_id):!anyProj.has(t.task_id)});return s})}
function ownerCall(input,init){
 var body=null;try{body=JSON.parse(init.body)}catch(e){}
 if(!body)return origFetch(input,init);
 if(body.op==='decide'&&OTHER){
  if(body.action==='owner_task'){if(!/^\s*\[проект:/i.test(body.note||''))body.note='[проект: '+P.id+'] '+String(body.note||'')}
  else if(body.action!=='ref_feedback'&&body.action!=='tv_mark_status')body.value='project:'+P.id; // ref: by image path; «Брак»/«Готово»: by task
  init=Object.assign({},init,{body:JSON.stringify(body)});
 }
 if(body.op!=='list')return origFetch(input,init);
 return Promise.all([origFetch(input,init),telemetry()]).then(function(x){var r=x[0],tel=x[1];
  return r.clone().json().then(function(j){
   j.decisions=(j.decisions||[]).filter(function(d){return rowProject(d,tel)===P.id}).map(function(d){d=Object.assign({},d);
    if(String(d.value||'').indexOf('project:')===0)d.value=null;if(d.note)d.note=String(d.note).replace(/^\s*\[проект:\s*[a-z0-9-]+\]\s*/i,'');return d});
   return new Response(JSON.stringify(j),{status:r.status,headers:{'content-type':'application/json'}})}).catch(function(){return r})})}
window.fetch=function(input,init){
 try{
  if(typeof input==='string'){
   if(input.indexOf(API_HOST)===0&&init&&String(init.method||'').toUpperCase()==='POST')return ownerCall(input,init);
   if(!/^[a-z]+:|^\/\//i.test(input)){
    var i=input.search(/[?#]/),path=(i<0?input:input.slice(0,i)).replace(/^\.\//,''),q=i<0?'':input.slice(i);
    if(path==='ops/owner-tasks.json')return synthInbox(q).then(reply);
    if(path==='shadow/topview-robot-status.json')return synthRobot(q).then(reply);
    if(OTHER){
     if(MAP[path])return origFetch(P.root+MAP[path]+q,init);
     if(path==='topview-status.json')return synthTopview().then(reply);
     if(path==='topview-task-map.json')return synthTaskMap().then(reply);
     if(path==='topview-video-archive.json')return Promise.resolve(reply({schema_version:1,project:P.id,videos:{}}));
    }else if(path==='topview-status.json'){
     telemetry().then(function(tel){return fresh('topview-status.json').then(function(root){SHARED=sharedSlots(root||{},tel);showSlots()})});
    }
   }
  }
 }catch(e){}
 return origFetch(input,init);
};
// ---- page helpers
function href(page){return page+(OTHER?'?p='+encodeURIComponent(P.id):'')}
function fixLinks(scope){
 if(!OTHER)return;
 (scope||document).querySelectorAll('a[href]').forEach(function(a){
  var h=a.getAttribute('href');if(!h||/^[a-z]+:|^\/\/|^#/i.test(h))return;
  var m=h.match(/^(index|references|film|videos)\.html(\?[^#]*)?(#.*)?$/);
  if(m){if(/[?&]p=/.test(m[2]||''))return;a.setAttribute('href',m[1]+'.html'+(m[2]?m[2]+'&':'?')+'p='+encodeURIComponent(P.id)+(m[3]||''));return}
  var i=h.search(/[?#]/),path=i<0?h:h.slice(0,i);
  if(MAP[path])a.setAttribute('href',P.root+MAP[path]+(i<0?'':h.slice(i)));
 })}
function showSlots(){
 var cap=document.getElementById('topviewCapacity');if(!cap||!SHARED)return;
 var old=cap.querySelector('.proj-slots');if(old)old.remove();
 var f=cap.firstChild;if(OTHER&&f&&f.nodeType===3)f.nodeValue=f.nodeValue.replace(/^занято (\d+) из \d+ · свободно \d+/,'в проекте занято $1');
 if(!OTHER&&!SHARED.others)return;
 var s=document.createElement('span');s.className='proj-slots';
 s.textContent=OTHER?(' · на всех проектах занято '+SHARED.occupied+' из '+SLOTS+', свободно '+SHARED.free):(' · ещё '+SHARED.others+' в других проектах, на всех свободно '+SHARED.free);
 s.title='Аккаунт Topview один, 6 слотов на все проекты (projects/README.md).';cap.appendChild(s)}
function metric(){
 if(!OTHER||!SHARED)return;var v=document.getElementById('metricSlow'),m=document.getElementById('metricSlowMeta');
 var tv=SHARED.occupied+' из '+SLOTS,tm='все проекты · в этом '+SHARED.mine+' · свободно '+SHARED.free;
 if(v&&v.textContent!==tv)v.textContent=tv;if(m&&m.textContent!==tm)m.textContent=tm}
function switcher(el){
 var sel=document.createElement('select');sel.className='project-switch';sel.setAttribute('aria-label','Проект');sel.title='Проект: у каждого свои сцены, промты, референсы, хендоф и очередь';
 PROJECTS.forEach(function(x){var o=document.createElement('option');o.value=x.id;o.textContent=x.emoji+' '+x.name;if(x.id===P.id)o.selected=true;sel.appendChild(o)});
 sel.onchange=function(){var page=(location.pathname.split('/').pop()||'index.html');if(!/\.html$/.test(page))page='index.html';
  location.href=page+(sel.value===ROOT?'':'?p='+encodeURIComponent(sel.value))};
 el.appendChild(sel)}
function projectFiles(){
 var grid=document.querySelector('.service-project-grid');if(!grid||!OTHER)return;
 var t=grid.parentNode.querySelector('.service-file-title');if(t)t.textContent='Файлы проекта «'+P.name+'»';
 grid.innerHTML=[[P.root+'video-prompts.md','Мастер промтов проекта'],[P.root+'HANDOFF.md','Хендоф проекта'],[P.root+'INSTRUCTIONS.md','Инструкция проекта'],
  [P.root+'character-references.json','Референсы (реестр)'],['projects/README.md','Как устроены проекты']].map(function(x){return '<a href="'+x[0]+'" target="_blank">'+x[1]+'</a>'}).join('')}
var css='.project-switch{font:inherit;font-size:13px;font-weight:700;color:var(--text,#edf2f7);background:var(--panel2,#151b22);border:1px solid var(--accent,#7dbbff);border-radius:9px;padding:5px 8px;cursor:pointer;max-width:100%}'+
 '.project-switch-wrap{display:flex;align-items:center;gap:6px;margin:6px 0 8px}.project-switch-wrap small{color:var(--muted,#8f9aa6);font-size:11px}'+
 'html.proj-other [data-only-root]{display:none!important}html:not(.proj-other) [data-only-project]{display:none!important}.proj-slots{color:var(--muted,#8f9aa6)}';
document.documentElement.classList.toggle('proj-other',OTHER);document.documentElement.dataset.project=P.id;
var st=document.createElement('style');st.textContent=css;(document.head||document.documentElement).appendChild(st);
function ready(){
 document.querySelectorAll('[data-project-switch]').forEach(function(el){if(!el.querySelector('select'))switcher(el)});
 document.querySelectorAll('[data-project-name]').forEach(function(el){el.textContent=P.name});
 document.querySelectorAll('[data-project-about]').forEach(function(el){el.textContent=P.about});
 if(OTHER&&document.title.indexOf(P.name)<0)document.title=P.name+' — '+document.title;
 projectFiles();fixLinks();
 var t=null;new MutationObserver(function(){clearTimeout(t);t=setTimeout(function(){fixLinks();var c=document.getElementById('topviewCapacity');if(c&&!c.querySelector('.proj-slots'))showSlots();metric()},120)}).observe(document.body,{childList:true,subtree:true});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready);else ready();
window.AIFP={id:P.id,name:P.name,root:P.root,isRoot:!OTHER,projects:PROJECTS.slice(),rowProject:rowProject,href:href};
})();
