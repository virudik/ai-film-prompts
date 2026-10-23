// Exercise the real refresh function with network/DOM stubs; no browser or external network.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),{webcrypto}=require('crypto');
const html=fs.readFileSync(require('path').join(__dirname,'../index.html'),'utf8');
const body=html.slice(html.indexOf('async function refreshPublishedTelemetry(){'),html.indexOf('setInterval(()=>{if(!document.hidden)refreshPublishedTelemetry()}'));
const digest=async s=>Buffer.from(await webcrypto.subtle.digest('SHA-256',new TextEncoder().encode(s))).toString('hex');
(async()=>{
 const original='original prompts',updated='updated prompts';let failures=0;
 for(const kind of ['same master, new certificate','changed master','fetch failure','wrong published SHA']){
  const md=kind==='changed master'?updated:original,sha=await digest(md),oldHash=await digest(original),urls=[],renders=[],elements={};
  const c={s:{canonical_master_sha256:oldHash},md:original,loadedMasterHash:oldHash,instructions:{checked_at:'old'},masterHashMatches:true};
  const tv={checked_at:'2026-10-23T18:30:00Z',active_tasks:[]};
  const payload={'project-status.json':{canonical_master_sha256:kind==='wrong published SHA'?'bad':sha,synced_at:'new'},'video-prompts.md':md,'topview-status.json':tv,'instruction-sync-status.json':{checked_at:'new'},'topview-task-map.json':{updated_at:'new'}};
  const ctx={telemetryContext:c,telemetryRefreshPending:false,topview:{checked_at:'2026-10-23T18:00:00Z'},topviewVideoArchive:null,topviewTaskMap:null,crypto:webcrypto,TextEncoder,Date,
   fetch:async url=>{urls.push(url.split('?')[0]);if(kind==='fetch failure'&&url.startsWith('project-status'))throw Error('offline');const data=payload[url.split('?')[0]]??{};return{ok:true,json:async()=>data,text:async()=>data}},
   renderStatus:(...a)=>renders.push(a),renderTopview:()=>{},renderNowView:()=>{},syncActiveSceneStatuses:()=>{},syncArchivedSceneLinks:()=>{},syncSubScenes:()=>{},loadAux:()=>{},renderFilters:()=>{},applyView:()=>{},humanDate:x=>x,
   $:id=>elements[id]??(elements[id]={textContent:'',style:{}})};
  vm.createContext(ctx);vm.runInContext(body,ctx);await ctx.refreshPublishedTelemetry();
  try{
   assert.equal(c.md,original,'prompt DOM source must remain unchanged');assert.equal(ctx.telemetryRefreshPending,false);
   if(kind==='fetch failure'){assert.equal(renders.length,0);assert.match(elements.topviewChecked.textContent,/Не удалось/)}
   else{assert.equal(c.instructions.checked_at,'new');assert.equal(c.s.synced_at,'new');assert.equal(c.publishedMasterChanged,kind==='changed master');assert.equal(c.masterHashMatches,kind!=='wrong published SHA');assert.ok(urls.includes('project-status.json')&&urls.includes('video-prompts.md')&&urls.includes('instruction-sync-status.json'))}
   console.log('PASS',kind);
  }catch(e){failures++;console.error('FAIL',kind,e.message)}
 }
 process.exitCode=failures?1:0;
})().catch(e=>{console.error(e);process.exitCode=1});
