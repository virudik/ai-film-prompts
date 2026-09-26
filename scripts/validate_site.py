#!/usr/bin/env python3
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
    "Topview telemetry временно устарела",
    "$('metricSlow').textContent=runtimeTopview.occupied+' из '+runtimeTopview.capacity;",
    "$('metricSlowMeta').textContent='Свободно '+runtimeTopview.free+' · '+runtimeTopview.slowSceneIds.length+' сцен';",
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
if 'Drive — канон · GitHub Pages — только чтение' not in html:
    raise SystemExit("sidebar authority subtitle must remain concise and one-line friendly")
if 'ПРОВЕРКА УСТАРЕЛА' in html:
    raise SystemExit("instruction freshness wording must clarify that the verification timestamp, not the instructions, is stale")
if 'id="metricWorkIds"' in html:
    raise SystemExit("work card must not dump raw W5…W15 identifiers")
if 'id="schema"' in html:
    raise SystemExit("internal schema_version must not be shown in owner-facing technical info")

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

print("site contract ok; duplicate ids=0; inline JS syntax ok; montage versions ok; fail-safe health contract ok")
