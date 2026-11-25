const assert = require('node:assert/strict');
const {ageInfo, monitorEvidence, slowLineAlarm} = require('../status-freshness.js');
const STALE = 120, FUTURE = 10, SKEW = 360;
const now = Date.parse('2026-11-25T22:51:00Z');
const iso = minAgo => new Date(now - minAgo * 60000).toISOString();
const ev = (monitor, scanMin) => monitorEvidence(monitor, scanMin == null ? null : iso(scanMin), now, STALE, FUTURE, SKEW);
const cycle = (minAgo, health) => ({last_scheduled_cycle: {completed_at: iso(minAgo), health: health || 'ok'}, last_successful_cycle_at: iso(minAgo)});

assert.equal(ageInfo(iso(50), now, STALE, FUTURE).state, 'fresh', '50 min publish lag is inside the 2 h mark');
assert.equal(ageInfo(iso(121), now, STALE, FUTURE).state, 'stale');
assert.equal(slowLineAlarm('fresh', true), false, 'unpublished task delta must not yellow a fresh look');
assert.equal(slowLineAlarm('fresh'), false);
assert.equal(slowLineAlarm('stale'), true);
assert.equal(slowLineAlarm('missing'), true);
assert.equal(slowLineAlarm('future'), true);

const cached = ev(cycle(6 * 24 * 60, 'ok'), 10);
assert.equal(cached.unhealthy, false, 'fresh robot scan overrides a days-old monitor copy');
assert.equal(cached.copyStale, true);
assert.equal(cached.successAge.state, 'fresh');
assert.equal(cached.healthBad, false);

const cachedDegraded = ev(cycle(6 * 24 * 60, 'degraded'), 10);
assert.equal(cachedDegraded.unhealthy, false, 'a degraded flag on the stale copy is not a current failure');
assert.equal(cachedDegraded.healthBad, false);

const reallySilent = ev(cycle(180, 'ok'), 180);
assert.equal(reallySilent.copyStale, false);
assert.equal(reallySilent.unhealthy, true, 'scan and cycle both old: the monitor is not answering');

const noScan = ev(cycle(180, 'ok'), null);
assert.equal(noScan.unhealthy, true);

const freshOk = ev(cycle(15, 'ok'), 10);
assert.equal(freshOk.copyStale, false, 'a few minutes of scan-before-publish is not a stale copy');
assert.equal(freshOk.unhealthy, false);

const degradedNow = ev(cycle(15, 'degraded'), 10);
assert.equal(degradedNow.unhealthy, true);
assert.equal(degradedNow.healthBad, true);
const degradedWithinPublish = ev(cycle(45, 'degraded'), 5);
assert.equal(degradedWithinPublish.copyStale, false);
assert.equal(degradedWithinPublish.unhealthy, true, 'a degraded cycle inside the publish cadence stays a warning');

const errorNow = ev(cycle(12, 'error'), 8);
assert.equal(errorNow.healthBad, true);
assert.equal(errorNow.unhealthy, true);

assert.equal(ev(null, 10).unhealthy, false, 'missing monitor file stays quiet');

const future = ev({last_scheduled_cycle: {completed_at: iso(-90), health: 'ok'}, last_successful_cycle_at: iso(-90)}, null);
assert.equal(future.cycleAge.state, 'future');
assert.equal(future.unhealthy, true);

const successOnlyStale = monitorEvidence({
 last_scheduled_cycle: {completed_at: iso(20), health: 'ok'},
 last_successful_cycle_at: iso(6 * 24 * 60)
}, iso(10), now, STALE, FUTURE, SKEW);
assert.equal(successOnlyStale.unhealthy, false);
assert.equal(successOnlyStale.successAge.state, 'fresh', 'success chip must not stay on a 6-day copy when the scan is fresh');
assert.equal(successOnlyStale.copyStale, false);

console.log('Status freshness: stale monitor copy, real silence, degraded cycle, 50 min publish lag passed.');
