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
    "runtimeTopview.occupied+' из '+runtimeTopview.capacity",
    "runtimeTopview.slowSceneIds.length+' сцен · '+runtimeSceneMultiplicityLabel()",
)
for required in contracts:
    if required not in html:
        raise SystemExit("missing fail-safe health contract: "+required)

# Slow summary is intentionally shown once in the metric; machine-status pill
# must not duplicate the same scene/task summary.
if "медленная генерация ${runtimeTopview.slowSceneIds.length}" in html:
    raise SystemExit("duplicate slow summary returned to projectStatus")

print("site contract ok; duplicate ids=0; inline JS syntax ok; fail-safe health contract ok")
