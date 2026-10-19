#!/usr/bin/env python3
import json
import re
import subprocess
import tempfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
html=(root/"index.html").read_text(encoding="utf-8")
ids=re.findall(r'<[^>]+\bid=["\']([^"\']+)["\']',html,re.I)
dupes=sorted({x for x in ids if ids.count(x)>1})
if dupes:
    raise SystemExit("duplicate HTML ids: "+", ".join(dupes))
blocks=re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>",html,re.S|re.I)
inline="\n".join(blocks)
with tempfile.NamedTemporaryFile("w",suffix=".js",encoding="utf-8",delete=False) as f:
    f.write(inline); name=f.name
p=subprocess.run(["node","--check",name],text=True,capture_output=True)
if p.returncode:
    raise SystemExit(p.stderr or p.stdout)
for required in ("now-view","nowGrid","review-ledger.json","renderNowView","slow-monitor","topviewCapacity"):
    if required not in html:
        raise SystemExit("missing site contract: "+required)

# Prevent regressions that turn maintenance/telemetry degradation into a false
# owner-facing master-sync failure.
contracts = (
    "const authoritativeHealthy=s.health==='ok'&&instruction!=='error'&&masterHashMatches;",
    "const topviewWarning=authoritativeHealthy&&(!topviewFresh||!topviewContractHealthy);",
    "Проверка Topview устарела",
    "$('metricSlow').textContent=runtimeTopview.occupied+' из '+runtimeTopview.capacity;",
    "$('metricSlowMeta').textContent='Свободно '+runtimeTopview.free+' · '+runtimeSlowIds().length+' сцен ждут решения';",
    "cap.innerHTML='занято '+occupied+' из '+capacity+' · свободно '+free",
    "$('projectStatus').textContent=`${s.scenes} активных сцен · ${s.prompt_texts} промтов · ${s.work_items_count} рабочих направлений`;",
)
for required in contracts:
    if required not in html:
        raise SystemExit("missing fail-safe health contract: "+required)

# Owner-facing UI invariants: slot-aware Topview summary, comfortable sidebar,
# compact current-work panel, montage chooser, and scroll-to-top control.
for required in (
    'id="metricSlowMeta"',
    "Свободно '+runtimeTopview.free",
    'id="backToTop"',
    'id="sideResize"',
    '--sidebar-width:328px',
    'SIDEBAR_DEFAULT=328',
    '<div id="filters" class="filters"></div>',
    'now-card-head',
    '.now-card.now-next .now-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))',
    "'now-next'",
    'Инструкции: СВЕРКА >3 Ч НАЗАД',
    'id="analysisPicker"',
    '>Монтажный разбор</summary>',
    'Seregius_montazhny_razbor.html',
    'Seregius_montazhny_razbor-2.html',
    '>Первая версия<',
    '>Вторая версия<',
):
    if required not in html:
        raise SystemExit("missing compact owner UI contract: "+required)
if '>Монтажный разбор фильма<' in html:
    raise SystemExit("montage analysis chooser label must not contain the word фильма")
if 'id="filterPanel"' in html:
    raise SystemExit("left sidebar filters must remain directly visible, not collapsed")
if 'grid-template-columns:292px minmax(0,1fr)' in html:
    raise SystemExit("regressed to over-compacted sidebar width")
if 'GitHub main — канон · Drive — копия' not in html:
    raise SystemExit("sidebar authority subtitle must remain concise and one-line friendly")
if 'ПРОВЕРКА УСТАРЕЛА' in html:
    raise SystemExit("instruction freshness wording must clarify that the verification timestamp, not the instructions, is stale")
if 'id="metricWorkIds"' in html:
    raise SystemExit("work card must not dump raw W5…W15 identifiers")
if 'id="schema"' in html:
    raise SystemExit("internal schema_version must not be shown in owner-facing technical info")

# Monitor freshness: stale scheduler observation must not look like a new
# autonomous run; the owner should see the last verified healthy cycle.
for required in (
    "monSuccessAge=monitor?ageInfo(monitor?.last_successful_cycle_at)",
    "unreportedSchedulerRun=Number.isFinite(schedulerObservedMs)",
    "chip('Успешный цикл',monSuccessAge",
    "chip('Запуск без отчёта',ageInfo(schedulerObservedAt)",
):
    if required not in html:
        raise SystemExit("monitor freshness regression: "+required)
if "chip('Запуск задачи',ageInfo(monitor.scheduler_observation.last_run_time)" in html:
    raise SystemExit("old scheduler timestamp must not masquerade as current monitoring activity")

# Canonical authority is GitHub main: obsolete Drive-origin owner labels are forbidden.
for old_label in ('Drive — канон','Drive→GitHub','Drive ↔ GitHub','Канон остаётся в Google Drive','7 канонических Drive-инструкций'):
    if old_label in html:
        raise SystemExit('obsolete Drive-authority label returned: '+old_label)
for label in ('GitHub main — канон · Drive — копия',"chip('Проверка GitHub',",'Семь канонических инструкций GitHub main проверены'):
    if label not in html:
        raise SystemExit('GitHub canonical label is missing: '+label)

# Topview owner buttons must be placed inside the Scene column, not the narrow Status
# column, and should remain a horizontal group with the same styling as scene buttons.
for required in (
    "box.className='owner-btns tv-scene-actions'",
    "tr.cells[1]?.appendChild(box)",
    ".topview-table .tv-scene .tv-scene-actions{display:flex;flex-wrap:nowrap;",
    ".topview-table .tv-scene .tv-scene-actions .owner-btn{flex:0 0 auto;white-space:nowrap}",
    "(tr.dataset.finished?DONE_ACTIONS.filter(([a])=>!(a==='tv_drop_task'&&tr.querySelector('.tv-status.success'))):TV_ACTIONS)",
):
    if required not in html:
        raise SystemExit("Topview owner button layout regression: "+required)
if "tr.cells[3]?.appendChild(box)" in html:
    raise SystemExit("Topview owner buttons cannot be placed in Status column")

# Both montage-analysis versions must remain published. The second file is large
# and must never regress to an empty placeholder while the chooser still links to it.
analysis_v1=root/"Seregius_montazhny_razbor.html"
analysis_v2=root/"Seregius_montazhny_razbor-2.html"
if not analysis_v1.exists() or analysis_v1.stat().st_size < 10000:
    raise SystemExit("first montage analysis is missing or unexpectedly small")
if not analysis_v2.exists() or analysis_v2.stat().st_size < 1000000:
    raise SystemExit("second montage analysis is missing, empty or unexpectedly small")
analysis_v2_text=analysis_v2.read_text(encoding="utf-8")
for required in ("монтажно-сюжетный разбор новой сборки","01:03:42,848"):
    if required not in analysis_v2_text:
        raise SystemExit("second montage analysis content contract failed: "+required)

# 09.10 audit P0: honest freshness, pinned local Markdown renderer, no browser GitHub API.
for required in (
    '<script src="vendor/marked-15.0.12.min.js"></script>',
    "content.innerHTML=safeHtml(marked.parse(md),",
    "armThumbFallback(content)",
    "references/thumbs/manifest.json",
    'id="sideToggle"',
    'id="freshnessLine"',
    "const STALE_MIN=120",
    "healthClass='warn'",
    "fetch('ci-status.json'",
    "fetch('automation-monitor-status.json'",
):
    if required not in html:
        raise SystemExit("missing freshness/renderer contract: "+required)
for forbidden in ("api.github.com", "cdn.jsdelivr.net/npm/marked/marked.min.js"):
    if forbidden in html:
        raise SystemExit("forbidden dependency returned: "+forbidden)
if not (root/"vendor"/"marked-15.0.12.min.js").is_file():
    raise SystemExit("vendored marked 15.0.12 is missing")
if not (root/"ci-status.json").is_file():
    raise SystemExit("ci-status.json is missing")

print("site contract ok; duplicate ids=0; inline JS syntax ok; montage versions ok; fail-safe health contract ok")

if "link.textContent='▶ Ролик '+(i+1)" not in html or "videosRow(tools).appendChild(link)" not in html:
    raise SystemExit("Per-scene finished video link regression")
# 13.10.2026 owner site requests: video links on their own line, no technical rule text, no duplicate slow label
for required in (
    ".scene-videos{flex:0 0 100%",
    "videosRow(tools).appendChild(link)",
    "/^Правило владельца \\(11\\.10\\.2026\\)/",
    "технически завершён|снят[аоы]? с учёта|завершил\\S* ошибкой|Редакционная приёмка отдельно",
    "while(el.nextSibling)el.nextSibling.remove()",
    "mk.push(...n.querySelectorAll('strong.slow-status'))",
    "m0.textContent='✅ ГОТОВО — ждёт решения владельца'",
    "el.textContent.includes('В МЕДЛЕННОЙ ГЕНЕРАЦИИ')){const br=el.previousElementSibling",
    "['owner_task','✎ Задача','',null]",
    "const TIP={",
    "function sceneDoneState(sid)",
    "m.className='mini done';m.textContent='✅ готово'",
    "chips.push(ds==='done'?['✅ Готово','done']",
    ".scene-videos{flex:0 0 100%;order:3;",
    "<br><span class=\"tv-eta-date\">",
):
    if required not in html:
        raise SystemExit("Owner site request regression (13.10): " + required)
if "Ежечасная проверка подхватит" in html:
    raise SystemExit("Stale hourly-check text is back in the owner panel")
# Slow-result retention regression guard (13.10.2026):
# terminal rows are owner-controlled, not aged away or filtered by reviewed.
for required in (
    "function sceneResultAttempts(sceneId,tv){",
    "return runtimeSlowIds().filter(sid=>!active.has(sid)).map(sid=>{",
    "topviewResultLinks(sid,tv)",
    "topview-task-map.json?fresh=",
    "TOPVIEW_FILM_BOARD='1a6244cf1ae747ef847d949a80d6133c'",
    "else if(summary.finishedStatus==='success'){badge.classList.add('done')}",
    "const DONE_ACTIONS=[['tv_drop_task','Не ждать'",
):
    if required not in html:
        raise SystemExit("Topview completed slow retention/link regression: " + required)
for forbidden in ("now-done>21*864e5", "l&&l.reviewed===true"):
    if forbidden in html:
        raise SystemExit("Topview completed rows must never expire without owner decision: " + forbidden)

# Verified Topview MP4 Drive backup links are separate from Topview deep links.
for required in ("topview-video-archive.json?fresh=", "function archivedDriveUrl(taskId,sceneId){", "function syncArchivedSceneLinks(){", "💾 Drive ", "💾 MP4 ", "syncArchivedSceneLinks();"):
    if required not in html:
        raise SystemExit("Archived Drive MP4 link regression: " + required)
# Drive's own viewer cannot play these MP4s (written over text seed files, no video preview): links open video.html,
# which streams drive.usercontent download URLs (19.10.2026).
if "return 'video.html?task='" not in html or "return 'https://drive.google.com/file/d/'" in html:
    raise SystemExit("Archived MP4 links must open video.html, not the Drive viewer")
video_page = (root / "video.html").read_text(encoding="utf-8")
for required in ("topview-video-archive.json?fresh=", "drive.usercontent.google.com/download?id=", "<video controls playsinline", "/^[0-9a-f]{32}$/"):
    if required not in video_page:
        raise SystemExit("video.html regression: " + required)
# Status lines (owner 20.10.2026): canon lock, tasks, canon health and self-heal sit once, in the top status panel.
_ctl = html[html.index('<section class="control">'):html.index('<section id="now-view"')]
for required in ('id="canonLockLine"', 'id="inboxList"', 'id="canonHealth"', 'id="selfHeal"'):
    if html.count(required) != 1 or required not in _ctl:
        raise SystemExit("Status line must appear once, in the top status panel: " + required)

# Owner site panel and extra pages (18.10.2026): queue, lock, inbox, canon health, film order, reference buttons.
for page in ("film.html", "references.html"):
    ptxt = (root / page).read_text(encoding="utf-8")
    pjs = "\n".join(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", ptxt, re.S | re.I))
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(pjs); pname = f.name
    pp = subprocess.run(["node", "--check", pname], text=True, capture_output=True)
    if pp.returncode:
        raise SystemExit(page + ": " + (pp.stderr or pp.stdout))
for required in ('id="pult"', "ops/topview-launch-queue.json", "ops/canon-lock.json", "ops/owner-tasks.json",
                 "canon-health.json", "action:'queue_up'", "'redo_enqueue'", 'href="film.html"', "TO_SELECT("):
    if required not in html:
        raise SystemExit("owner site panel regression: " + required)
film = (root / "film.html").read_text(encoding="utf-8")
for required in ("film-order.json", "action:'queue_add'", "action:'owner_task'"):
    if required not in film:
        raise SystemExit("film.html regression: " + required)
refs = (root / "references.html").read_text(encoding="utf-8")
for required in ("action:'ref_feedback'", "references/reference-review.json"):
    if required not in refs:
        raise SystemExit("references.html regression: " + required)
json.loads((root / "film-order.json").read_text(encoding="utf-8"))
print("owner site panel, film.html and references.html ok")

