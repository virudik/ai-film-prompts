/* Read-only continuation readiness. No model-context counter and no task submission. */
(function (root) {
'use strict';
function safePath(path) {
 return typeof path === 'string' && /^[A-Za-z0-9_./-]+$/.test(path) && !path.startsWith('/') && !path.split('/').includes('..');
}
// How long a just-rebuilt packet may lag the files it hashes (handoff commit,
// then shadow-brief, then Pages). Inside this window a hash miss is not a fault.
const PACKET_LAG_MIN = 180;
function assess(packet, hashes, now, project="seregius") {
 const issues = [];
 if (!packet || packet.generator !== 'continue-2.0' || packet.schema_version !== 1 || !Array.isArray(packet.sources) || !packet.sources.length) {
  return {ready:false, tone:'alarm', issues:['Пакет восстановления недоступен или имеет неизвестный формат.']};
 }
 const t = Date.parse(packet.checked_at);
 if (!Number.isFinite(t) || t > now + 600000) issues.push('Время проверки не подтверждено.');
 const prefix=project==='seregius'?'':'projects/'+project+'/';
 if((packet.project||'seregius')!==project)issues.push('Пакет принадлежит другому проекту.');
 const required = [prefix+'work-resume-register.json',prefix+'reports/current-work-checkpoint.md','shadow/current-checkpoint.md','shadow/takeover-brief.json',prefix+'ops/topview-launch-queue.json'];
 if(prefix)required.push('projects/projects.json','projects/README.md',prefix+'HANDOFF.md',prefix+'INSTRUCTIONS.md',prefix+'project-status.json',prefix+'video-prompts.md');
 if (!required.every(p=>packet.sources.some(s=>s.file===p))) issues.push('В пакете отсутствуют обязательные источники.');
 let hashMismatch=false;
 for (const source of packet.sources) {
  if (!safePath(source.file) || hashes[source.file] !== source.sha256) {hashMismatch=true;issues.push('Сохранённые данные изменились или недоступны: '+String(source.file));}
 }
 if (packet.execution_authorized !== false) issues.push('Точка продолжения требует восстановления.');
 const hard=issues.some(i=>!i.startsWith('Сохранённые данные изменились'));
 // No selected work and the packet itself says it is not a resume point: nothing to continue, not a fault.
 const idle=!packet.selected_work && packet.ready_for_resume===false && packet.execution_authorized===false && !hard;
 if (idle) return {ready:false, tone:'idle', issues};
 if (!packet.ready_for_resume || !packet.selected_work) issues.push('Точка продолжения требует восстановления.');
 const onlyHash=hashMismatch && issues.every(i=>i.startsWith('Сохранённые данные изменились'));
 const ageMin=(now-t)/60000;
 if (onlyHash && packet.selected_work && ageMin<=PACKET_LAG_MIN) return {ready:false, tone:'pending', issues};
 return {ready:issues.length===0, tone:issues.length?'alarm':'ready', issues};
}
if (typeof module !== 'undefined' && module.exports) module.exports = {assess,safePath,PACKET_LAG_MIN};
if (!root.document) return;
const box = root.document.getElementById('continueReadiness');
if (!box) return;
const project=root.AIFP?.id||'seregius';
const prefix=root.AIFP?.root||'';
const rawURL=path=>new URL(path,document.baseURI).href; // absolute URL bypasses project fetch remapping
function freshURL(path){const u=new URL(rawURL(path));u.searchParams.set('fresh',String(Date.now()));return u.href}
const packetPath=prefix+'shadow/resume-packet';
let running = false;
function el(tag, text, parent) {const e=document.createElement(tag);if(text)e.textContent=text;if(parent)parent.appendChild(e);return e;}
function render(packet, result) {
 const wasOpen=box.querySelector('details')?.open;
 const tone=result.tone||(result.ready?'ready':'alarm');
 box.replaceChildren();box.dataset.state=tone==='ready'?'ready':tone==='alarm'?'needs-recovery':tone;
 const details=el('details','',box);details.open=!!wasOpen;
 const label=tone==='ready'?(packet?.selected_work?.status==='waiting_for_owner'?'готово · ждёт владельца':'готово'):tone==='idle'?'продолжать нечего':tone==='pending'?'сверка обновляется':'нужна проверка';
 const summary=el('summary','↪ Продолжение: '+label,details);
 if(tone==='alarm')summary.className='warnc';
 const w=packet?.selected_work;
 if(w){el('div',w.title,details);el('p','Сохранённый этап: '+w.last_completed,details);el('p','Далее: '+w.next_action,details);}
 if(packet?.checked_at){const d=new Date(packet.checked_at);if(Number.isFinite(d.getTime()))el('small','Проверка '+d.toLocaleString('ru-RU',{timeZone:'Europe/Moscow'})+' МСК',details);}
 if(packet?.packet_bytes)el('p','Пакет для нового чата: '+(packet.packet_bytes/1024).toFixed(1)+' КБ.',details);
 for(const issue of result.issues)el('p',issue,details);
 const uncertain=packet?.queue_recovery?.unresolved?.length||0;
 if(uncertain)el('p','Отправок без подтверждённого результата: '+uncertain+'. Перед продолжением нужно сверить существующие задачи.',details);
 const receipt=packet?.handoff_receipt;
 if(receipt){
  const label=receipt.work_id===w?.work_id?'Последняя квитанция этой работы: ':'Последняя квитанция другой работы: ';
  const outcome={accepted:'принято',waiting_for_owner:'ожидание владельца',blocked:'приём заблокирован'}[receipt.outcome]||receipt.outcome;
  el('p',label+(receipt.chat?.label||'не указан')+' · '+receipt.accepted_at+' · '+outcome,details);
  if(receipt.chat?.chat_id)el('small','Чат: '+receipt.chat.chat_id,details);
  else el('small','Точный ID чата недоступен; сессия: '+(receipt.chat?.session_id||'не указана'),details);
  el('p','Работа '+receipt.work_id+'. Первое действие: '+(receipt.first_action?.description||''),details);
 }else el('p','Квитанции приёма ещё нет: готовность пакета не означает, что новый чат уже принял работу.',details);
 const receiptLink=el('a','Журнал приёма смены',details);receiptLink.href=prefix+'reports/handoff-receipts.json';receiptLink.target='_blank';receiptLink.rel='noopener';
 el('p','В новом чате назови проект «'+(root.AIFP?.name||'Серёгиус')+'» и напиши «Продолжай». Агент проверит текущие решения и доступы.',details);
 const a=el('a','Открыть пакет восстановления',details);a.href=packetPath+'.md';a.target='_blank';a.rel='noopener';
 const button=el('button','Проверить снова',details);button.type='button';button.className='owner-btn';button.addEventListener('click',load);
}
async function readPacket() {
 const response=await fetch(freshURL(packetPath+'.json'),{cache:'no-store'});
 if(!response.ok)throw Error('packet unavailable');
 const packet=await response.json();
 if(!Array.isArray(packet.sources)||packet.sources.length>50)throw Error('invalid sources');
 const hashes={};
 const pending=packet.sources.slice();
 await Promise.all(Array.from({length:4},async()=>{
  while(pending.length){const source=pending.shift();if(!safePath(source.file))continue;
   try{const r=await fetch(freshURL(source.file),{cache:'no-store'});if(!r.ok)continue;const bytes=await r.arrayBuffer();
    hashes[source.file]=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');
   }catch(_){/* Missing source remains unverified. */}
  }
 }));
 return {packet,result:assess(packet,hashes,Date.now(),project)};
}
async function load() {
 if(running||document.hidden)return;running=true;
 let packet=null;
 try {
  // One retry: Pages can briefly serve the packet and a source it hashes from different publishes.
  let read=await readPacket();
  if(read.result.tone==='pending'){await new Promise(r=>setTimeout(r,2000));if(document.hidden){render(read.packet,read.result);return}read=await readPacket();}
  packet=read.packet;render(packet,read.result);
 } catch (_) {render(packet,{ready:false,tone:'alarm',issues:['Не удалось проверить сохранённую точку продолжения.']});}
 finally{running=false;}
}
load();setInterval(load,120000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)load();});
root.addEventListener('online',load);
})(typeof window !== 'undefined' ? window : globalThis);
