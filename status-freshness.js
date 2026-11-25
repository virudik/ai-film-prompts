/* Owner-facing freshness. Yellow is a real problem, not a normal publication lag.
   No network, no writes. Shared by index.html and tests/status_freshness_check.js. */
(function (root) {
'use strict';
function ageInfo(v, now, staleMin, futureMin) {
 const ms = Date.parse(v || '');
 if (!v || !Number.isFinite(ms)) return {state:'missing', min:Infinity};
 const min = (now - ms) / 60000;
 if (min < -futureMin) return {state:'future', min};
 return {state: min <= staleMin ? 'fresh' : 'stale', min: Math.max(0, min)};
}
// A shadow scan this much newer than automation-monitor-status.json means the
// page is holding an old copy of the monitor file. The robot looks every 10 min
// and republishes an unchanged cycle within 50 min, so a gap of a few hours is
// still a real missed cycle; only a much older copy is ignored.
const MONITOR_COPY_SKEW_MIN = 360;
function monitorEvidence(monitor, scanCheckedAt, now, staleMin, futureMin, skewMin) {
 const skew = skewMin == null ? MONITOR_COPY_SKEW_MIN : skewMin;
 const age = v => ageInfo(v, now, staleMin, futureMin);
 const cycle = monitor && monitor.last_scheduled_cycle || null;
 const cycleAt = cycle && cycle.completed_at || '';
 const successAt = monitor && monitor.last_successful_cycle_at || '';
 const scanMs = Date.parse(scanCheckedAt || '');
 const cycleMs = Date.parse(cycleAt || '');
 const successMs = Date.parse(successAt || '');
 const scanFresh = age(scanCheckedAt).state === 'fresh';
 const copyStale = scanFresh && (!Number.isFinite(cycleMs) || scanMs - cycleMs > skew * 60000);
 const successCopyStale = scanFresh && (!Number.isFinite(successMs) || scanMs - successMs > skew * 60000);
 const shownCycle = copyStale ? scanCheckedAt : cycleAt;
 const shownSuccess = successCopyStale ? scanCheckedAt : successAt;
 const cycleAge = monitor ? age(shownCycle) : {state:'unknown', min:Infinity};
 const successAge = monitor ? age(shownSuccess) : {state:'unknown', min:Infinity};
 const healthBad = !copyStale && Boolean(cycle && cycle.health && cycle.health !== 'ok');
 const unhealthy = Boolean(monitor) && (healthBad || cycleAge.state !== 'fresh');
 return {cycleAge, successAge, unhealthy, healthBad, copyStale};
}
// The «проверено» line. A differing task list during the 50-minute publish
// cadence is not a stale check; only the age of the look itself is.
function slowLineAlarm(ageState) {
 return ageState !== 'fresh';
}
const api = {ageInfo, monitorEvidence, slowLineAlarm, MONITOR_COPY_SKEW_MIN};
if (typeof module !== 'undefined' && module.exports) module.exports = api;
root.SF = api;
})(typeof window !== 'undefined' ? window : globalThis);
