// Shared video source for every project (owner decision 26.11.2026): finished Topview videos play from
// Yandex Disk first, through each file's own public link (yandex_public_key in the project's
// topview-video-archive.json). The page asks the public Yandex API for a short-lived download link
// (about 4 hours) on every open, so no link is stored. Yandex answers 403 when the request carries a
// foreign Referer, so every page that plays these videos must have <meta name="referrer" content="no-referrer">.
// Fallback: the old Supabase drive-video stream (Google Drive file_id), then the Drive page.
// No keys or tokens: a public key only lets anyone read that one file.
(function(){
'use strict';
var API='https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key=';
var STREAM='https://vzohfatqzyioydtgjiyd.supabase.co/functions/v1/drive-video?id=';
var KEY_RE=/^https:\/\/(yadi\.sk|disk\.yandex\.(ru|com))\/(i|d)\/[A-Za-z0-9_-]{6,}$/;
var DRIVE_RE=/^[A-Za-z0-9_-]{15,}$/;
var cache={},TTL=3*3600e3;
function yandexKey(e){var k=String(e&&e.yandex_public_key||'');return KEY_RE.test(k)?k:null}
function driveStream(e){var id=String(e&&e.file_id||'');return DRIVE_RE.test(id)?STREAM+encodeURIComponent(id):null}
function playable(e){return !!(yandexKey(e)||driveStream(e))}
function yandexHref(key){
 var c=cache[key];if(c&&Date.now()-c.at<TTL)return Promise.resolve(c.href);
 return fetch(API+encodeURIComponent(key),{cache:'no-store',referrerPolicy:'no-referrer'}).then(function(r){
  if(!r.ok)throw new Error('Yandex '+r.status);return r.json()}).then(function(j){
  var h=String(j&&j.href||'');if(!/^https:\/\/[a-z0-9.-]+\.yandex\.(net|ru)\//.test(h))throw new Error('Yandex link');
  cache[key]={at:Date.now(),href:h};return h})}
// Ordered list of sources for one archive entry: [{kind,url}], Yandex first.
function sources(e){
 var out=[],k=yandexKey(e),d=driveStream(e);
 var tail=function(){var t=[];if(d)t.push({kind:'drive',url:d});return t};
 if(!k)return Promise.resolve(tail());
 return yandexHref(k).then(function(h){return [{kind:'yandex',url:h}].concat(tail())},function(){return tail()})}
// Put the first source into a <video>; on a playback error try the next one. onFail() when none works.
// A late answer for a player that was already replaced (another clip opened) is ignored, so the label,
// download link and error note always belong to the clip on screen.
function attach(video,e,onFail,onSource){
 var alive=function(){return video.isConnected&&video.dataset.aifpToken===token};
 var token=String(Date.now())+Math.random();video.dataset.aifpToken=token;
 return sources(e).then(function(list){
  if(!alive())return list;
  var i=0;
  function next(){
   if(!alive())return;
   if(i>=list.length){if(onFail)onFail();return}
   var s=list[i++];if(onSource)onSource(s);video.src=s.url;video.load()}
  video.addEventListener('error',function(){if(!alive())return;if(e&&yandexKey(e)&&list[i-1]&&list[i-1].kind==='yandex')delete cache[yandexKey(e)];next()});
  next();return list})}
window.AIFP_VIDEO={yandexKey:yandexKey,driveStream:driveStream,playable:playable,yandexHref:yandexHref,sources:sources,attach:attach,STREAM:STREAM};
})();
