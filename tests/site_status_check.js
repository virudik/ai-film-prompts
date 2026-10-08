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
  const freshMon = () => { const m = clone(mon); m.last_scheduled_cycle = { ...(m.last_scheduled_cycle || {}), completed_at: iso(15), health: 'ok' }; return m; };
  return [
    { name: 'fresh everything', tv: freshTv(), mon: freshMon(), expect: { cls: 'ok', text: 'ПРОЕКТ СИНХРОНИЗИРОВАН' } },
    { name: 'Topview 3 h old', tv: Object.assign(freshTv(), { checked_at: iso(180) }), mon: freshMon(), expect: { cls: 'warn', text: 'ДАННЫЕ TOPVIEW УСТАРЕЛИ' } },
    { name: 'Topview checked_at missing', tv: Object.assign(freshTv(), { checked_at: null }), mon: freshMon(), expect: { cls: 'warn', text: 'ДАННЫЕ TOPVIEW УСТАРЕЛИ' } },
    { name: 'Topview checked_at invalid', tv: Object.assign(freshTv(), { checked_at: 'not-a-date' }), mon: freshMon(), expect: { cls: 'warn', text: 'ДАННЫЕ TOPVIEW УСТАРЕЛИ' } },
    { name: 'Topview checked_at in the future', tv: Object.assign(freshTv(), { checked_at: iso(-90) }), mon: freshMon(), expect: { cls: 'warn', text: 'НЕВЕРНОЕ ВРЕМЯ ПРОВЕРКИ' } },
    { name: 'monitor cycle 3 h old', tv: freshTv(), mon: (() => { const m = freshMon(); m.last_scheduled_cycle.completed_at = iso(180); return m; })(), expect: { cls: 'warn', text: 'МОНИТОР НЕ ОТВЕЧАЕТ' } },
    { name: 'monitor cycle unhealthy', tv: freshTv(), mon: (() => { const m = freshMon(); m.last_scheduled_cycle.health = 'degraded'; return m; })(), expect: { cls: 'warn', text: 'МОНИТОР НЕ ОТВЕЧАЕТ' } },
    { name: 'monitor file missing (backward compatible)', tv: freshTv(), mon: 404, expect: { cls: 'ok', text: 'ПРОЕКТ СИНХРОНИЗИРОВАН' } },
    { name: 'wrong master SHA is never green', tv: freshTv(), mon: freshMon(), status: Object.assign(clone(status), { canonical_master_sha256: '0'.repeat(64) }), expect: { cls: 'bad', text: 'ОШИБКА' } },
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
      const body = { 'topview-status.json': sc.tv, 'automation-monitor-status.json': sc.mon, 'project-status.json': sc.status }[f];
      if (body === 404) return route.fulfill({ status: 404, body: 'missing' });
      if (body !== undefined) return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
      return route.continue();
    });
    await page.goto(BASE + 'index.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(400);
    const r = await page.evaluate(() => ({
      cls: ['ok', 'warn', 'bad'].find(c => document.getElementById('health').classList.contains(c)),
      text: document.getElementById('health').textContent,
      fresh: document.getElementById('freshnessLine')?.innerText || '',
      h2: document.querySelectorAll('#content h2').length,
      copy: [...document.querySelectorAll('button')].filter(b => /Копировать промт/.test(b.innerText)).length,
      galleries: document.querySelectorAll('.scene-ref-gallery img').length,
    }));
    const ok = r.cls === sc.expect.cls && r.text.includes(sc.expect.text) && errors.length === 0 && r.h2 > 10 && r.copy > 10 && externalRequests === 0;
    if (!ok) failures++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${sc.name.padEnd(56)} health=${r.cls} «${r.text}»  h2=${r.h2} copy=${r.copy} img=${r.galleries} ext=${externalRequests}${errors.length ? ' errors=' + errors.join(' | ') : ''}`);
    if (sc.name === 'Topview 3 h old') console.log('      freshness line:', r.fresh.replace(/\s+/g, ' '));
    await page.close();
  }
  await browser.close();
  console.log(failures ? `${failures} scenario(s) failed` : 'all scenarios passed');
  process.exit(failures ? 1 : 0);
})();
