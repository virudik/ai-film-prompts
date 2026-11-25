// Regression check for the Control Center status logic (A/C/D of the 08.10 audit task).
// Usage: python3 -m http.server 8765 -d <repo> &  then  node tests/site_status_check.js
// Needs Playwright with Chromium. Serves the real repo files and swaps individual JSON
// payloads per scenario; no network access beyond 127.0.0.1 is allowed.
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.env.BASE_URL || 'http://127.0.0.1:8765/';
const ROOT = path.resolve(__dirname, '..');
const read = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8').replace(/^﻿/, ''));
const iso = minAgo => new Date(Date.now() - minAgo * 60000).toISOString();

function scenarios() {
  const status = read('project-status.json');
  const tv = read('topview-status.json');
  const mon = read('automation-monitor-status.json');
  const clone = x => JSON.parse(JSON.stringify(x));
  const freshTv = () => { const t = clone(tv); t.checked_at = iso(10); return t; };
  const freshMon = () => { const m = clone(mon); m.last_scheduled_cycle = { ...(m.last_scheduled_cycle || {}), completed_at: iso(15), health: 'ok' }; m.last_successful_cycle_at = iso(15); return m; };
  const scanOf = (base, minAgo, differ) => ({
    checked_at: iso(minAgo),
    active_tasks: differ ? [{ task_id: 'ab'.repeat(16), unlimited: true }] : (base.active_tasks || []).filter(x => x && x.task_id).map(x => ({ task_id: x.task_id, unlimited: x.unlimited !== false })),
  });
  const oldMon = freshMon(); oldMon.last_scheduled_cycle = { ...oldMon.last_scheduled_cycle, completed_at: iso(180), health: 'ok' }; oldMon.last_successful_cycle_at = iso(180);
  const weekMon = freshMon(); weekMon.last_scheduled_cycle = { ...weekMon.last_scheduled_cycle, completed_at: iso(6 * 24 * 60), health: 'ok' }; weekMon.last_successful_cycle_at = iso(6 * 24 * 60);
  const tv50 = freshTv(); tv50.checked_at = iso(50);
  const tv180 = freshTv(); tv180.checked_at = iso(180);
  return [
    { name: 'fresh everything', tv: freshTv(), mon: freshMon(), expect: { cls: 'ok', text: 'ПРОЕКТ СИНХРОНИЗИРОВАН', ins: 'порог 48' } },
    { name: 'Topview 3 h old', tv: Object.assign(freshTv(), { checked_at: iso(180) }), mon: freshMon(), expect: { cls: 'warn', text: 'ДАННЫЕ TOPVIEW УСТАРЕЛИ' } },
    { name: 'Topview checked_at missing', tv: Object.assign(freshTv(), { checked_at: null }), mon: freshMon(), expect: { cls: 'warn', text: 'ДАННЫЕ TOPVIEW УСТАРЕЛИ' } },
    { name: 'Topview checked_at invalid', tv: Object.assign(freshTv(), { checked_at: 'not-a-date' }), mon: freshMon(), expect: { cls: 'warn', text: 'ДАННЫЕ TOPVIEW УСТАРЕЛИ' } },
    { name: 'Topview checked_at in the future', tv: Object.assign(freshTv(), { checked_at: iso(-90) }), mon: freshMon(), expect: { cls: 'warn', text: 'НЕВЕРНОЕ ВРЕМЯ ПРОВЕРКИ' } },
    { name: 'monitor cycle 3 h old', tv: freshTv(), mon: oldMon, scan: scanOf(freshTv(), 180), expect: { cls: 'warn', text: 'МОНИТОР НЕ ОТВЕЧАЕТ' } },
    { name: 'stale monitor copy but fresh robot scan', tv: freshTv(), mon: weekMon, scan: scanOf(freshTv(), 10), expect: { cls: 'ok', text: 'ПРОЕКТ СИНХРОНИЗИРОВАН', noDaysWarn: true } },
    { name: 'publish lag 50 min is not a stale look', tv: tv50, mon: freshMon(), scan: scanOf(tv50, 8), expect: { cls: 'ok', text: 'ПРОЕКТ СИНХРОНИЗИРОВАН', capStale: false, capHas: 'проверено', capLacks: 'устарела' } },
    { name: 'unpublished task delta within publish lag is not yellow', tv: tv50, mon: freshMon(), scan: scanOf(tv50, 8, true), expect: { cls: 'ok', text: 'ПРОЕКТ СИНХРОНИЗИРОВАН', capStale: false, capLacks: 'устарела', capHas: 'не выложены' } },
    { name: 'look older than 2 h is yellow', tv: tv180, mon: oldMon, scan: scanOf(tv180, 180), expect: { cls: 'warn', text: 'ДАННЫЕ TOPVIEW УСТАРЕЛИ', capStale: true, capHas: 'устарела' } },
    { name: 'monitor cycle unhealthy', tv: freshTv(), mon: (() => { const m = freshMon(); m.last_scheduled_cycle.health = 'degraded'; return m; })(), expect: { cls: 'warn', text: 'МОНИТОР: НЕПОЛНЫЙ ЦИКЛ' } },
    { name: 'monitor file missing (backward compatible)', tv: freshTv(), mon: 404, expect: { cls: 'ok', text: 'ПРОЕКТ СИНХРОНИЗИРОВАН' } },
    { name: 'wrong master SHA is never green', tv: freshTv(), mon: freshMon(), status: Object.assign(clone(status), { canonical_master_sha256: '0'.repeat(64) }), expect: { cls: 'bad', text: 'ОШИБКА', msg: 'Загруженный master не соответствует' } },
    { name: 'canonical health error is red even with fresh telemetry', tv: freshTv(), mon: freshMon(), status: Object.assign(clone(status), { health: 'error' }), expect: { cls: 'bad', text: 'ОШИБКА' } },
  ];
}

(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  let failures = 0;
  for (const sc of scenarios()) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    let externalRequests = 0;
    await page.route('**/*', route => {
      const u = route.request().url();
      if (!u.startsWith(BASE)) { if (!/supabase\.co\/rest\/v1\/comments/.test(u)) { externalRequests++; console.log('      external request:', u); } return route.abort(); }
      const f = u.slice(BASE.length).split('?')[0];
      const body = { 'topview-status.json': sc.tv, 'automation-monitor-status.json': sc.mon, 'project-status.json': sc.status, 'shadow/topview-robot-status.json': sc.scan }[f];
      if (body === 404) return route.fulfill({ status: 404, body: 'missing' });
      if (body !== undefined) return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
      return route.continue();
    });
    await page.goto(BASE + 'index.html', { waitUntil: 'networkidle' });
    if (sc.expect.capHas || sc.expect.capStale != null) await page.waitForFunction(() => /проверено|устарела|занято/.test(document.getElementById('topviewCapacity')?.textContent || ''), { timeout: 8000 }).catch(() => {});
    else await page.waitForTimeout(400);
    const r = await page.evaluate(() => ({
      cls: ['ok', 'warn', 'bad'].find(c => document.getElementById('health').classList.contains(c)),
      text: document.getElementById('health').textContent,
      fresh: document.getElementById('freshnessLine')?.innerText || '',
      warnText: [...document.querySelectorAll('#freshnessLine .fresh-warn')].map(n => n.textContent).join(' | '),
      ins: [...document.querySelectorAll('#freshnessLine [title]')].map(n => n.getAttribute('title')).join('\n'),
      cap: document.getElementById('topviewCapacity')?.textContent || '',
      capStale: document.getElementById('topviewCapacity')?.classList.contains('stale') || false,
      msg: document.getElementById('statusMessage')?.textContent || '',
      h2: document.querySelectorAll('#content h2').length,
      copy: [...document.querySelectorAll('button')].filter(b => /Копировать промт/.test(b.innerText)).length,
      galleries: document.querySelectorAll('.scene-ref-gallery img').length,
    }));
    const ex = sc.expect;
    const ok = r.cls === ex.cls && r.text.includes(ex.text) && errors.length === 0 && r.h2 > 10 && r.copy > 10 && externalRequests === 0
      && (ex.capStale == null || r.capStale === ex.capStale)
      && (ex.capHas == null || r.cap.includes(ex.capHas))
      && (ex.capLacks == null || !r.cap.includes(ex.capLacks))
      && (ex.ins == null || r.ins.includes(ex.ins))
      && (!ex.noDaysWarn || !/дн/.test(r.warnText))
      && (ex.msg == null || r.msg.includes(ex.msg));
    if (!ok) failures++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${sc.name.padEnd(56)} health=${r.cls} «${r.text}»  h2=${r.h2} copy=${r.copy} img=${r.galleries} ext=${externalRequests}${errors.length ? ' errors=' + errors.join(' | ') : ''}`);
    if (!ok && (ex.capHas || ex.capStale != null || ex.ins || ex.noDaysWarn || ex.msg)) console.log('      detail capStale=' + r.capStale + ' cap=«' + r.cap.replace(/\s+/g, ' ') + '» warn=«' + r.warnText + '» msg=«' + r.msg + '»');
    if (sc.name === 'Topview 3 h old') console.log('      freshness line:', r.fresh.replace(/\s+/g, ' '));
    await page.close();
  }
  // Projects (owner decision 20.10.2026): ?p=<id> reads the project folder, filters shared files and tags buttons.
  for (const pid of ['kotmonavty', 'seregius']) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errors = [], sent = [];
    page.on('pageerror', e => errors.push(String(e)));
    const tv = read('topview-status.json'); tv.checked_at = iso(10); tv.active_tasks = (tv.active_tasks || []).slice(0, 3); tv.occupied_slots = tv.active_tasks.length; tv.free_slots = 6 - tv.occupied_slots;
    const tel = { schema_version: 1, checked_at: iso(10), active: [{ project: 'kotmonavty', scene_id: 1, task_id: 'e'.repeat(32), status: 'running', model: 'Seedance 2.0' }], recent: [] };
    const rows = [{ id: 'a', scene_id: 3, action: 'accept', value: null, note: null, status: 'pending' },
      { id: 'b', scene_id: 1, action: 'accept', value: 'project:kotmonavty', note: null, status: 'pending' },
      { id: 'c', scene_id: null, action: 'owner_task', value: 'any', note: '[проект: kotmonavty] нарисовать корабль', status: 'pending' }];
    await page.route('**/*', route => {
      const u = route.request().url();
      if (/functions\/v1\/owner-decision/.test(u)) { const b = JSON.parse(route.request().postData() || '{}'); sent.push(b);
        return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(b.op === 'list' ? { decisions: rows } : { ok: true }) }); }
      if (!u.startsWith(BASE)) return route.abort();
      const f = u.slice(BASE.length).split('?')[0];
      const body = { 'topview-status.json': tv, 'projects/topview-projects.json': tel, 'automation-monitor-status.json': (() => { const m = read('automation-monitor-status.json'); m.last_scheduled_cycle = { ...(m.last_scheduled_cycle || {}), completed_at: iso(15), health: 'ok' }; return m; })() }[f];
      if (body !== undefined) return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
      return route.continue();
    });
    await page.goto(BASE + 'index.html' + (pid === 'seregius' ? '' : '?p=' + pid), { waitUntil: 'networkidle' });
    await page.waitForTimeout(600);
    const r = await page.evaluate(async () => {
      const o = window.aiFilmOwner;
      await o.call({ op: 'decide', action: 'accept', scene_id: 1 });
      await o.call({ op: 'decide', action: 'owner_task', note: 'тест', value: 'any' });
      const list = await o.call({ op: 'list' });
      return { sel: document.querySelector('.project-switch')?.value, cls: ['ok', 'warn', 'bad'].find(c => document.getElementById('health').classList.contains(c)),
        cap: document.getElementById('topviewCapacity')?.textContent || '', rows: document.querySelectorAll('#topviewMonitor tr[data-task-id]').length,
        h2: document.querySelectorAll('#content h2').length, list: (list.decisions || []).map(d => d.id).join(','), film: document.querySelector('a[href^="film.html"]')?.getAttribute('href') };
    });
    const dec = sent.filter(b => b.op === 'decide');
    const other = pid !== 'seregius';
    const ok = errors.length === 0 && r.sel === pid && r.cls !== 'bad' &&
      (other ? dec[0].value === 'project:kotmonavty' && /^\[проект: kotmonavty\] тест$/.test(dec[1].note) && r.list === 'b,c' && r.rows === 1 && new RegExp('на всех проектах занято ' + (tv.occupied_slots + 1) + ' из 6').test(r.cap) && r.film === 'film.html?project=kotmonavty' && r.h2 >= 2
        : dec[0].value === undefined && dec[1].note === 'тест' && r.list === 'a' && /ещё 1 в других проектах/.test(r.cap) && r.film === 'film.html' && r.h2 > 10);
    if (!ok) failures++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  project ${pid.padEnd(48)} health=${r.cls} rows=${r.rows} list=${r.list} cap=«${r.cap}»${errors.length ? ' errors=' + errors.join(' | ') : ''}`);
    await page.close();
  }
  await browser.close();
  console.log(failures ? `${failures} scenario(s) failed` : 'all scenarios passed');
  process.exit(failures ? 1 : 0);
})();
