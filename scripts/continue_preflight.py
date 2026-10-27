#!/usr/bin/env python3
"""Read-only D7 'Продолжай' preflight. Never invents conversational memory.

Reads a fresh local checkout of GitHub main and verifies generated brief *against
current bytes*, not only against its at-generation validity claim.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resume_project import context
from resume_state import verify_recovery, local_file
from build_takeover_brief import DOCS, MASTER, INVARIANTS, section


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def _evaluate(root, work_id=None, include_work=False, project="seregius"):
    ctx = context(root, project)
    root = Path(root)
    reasons, warnings = [], []
    try:
        brief = load(root, "shadow/takeover-brief.json")
        status = load(root, "project-status.json")
        cert = load(root, "instruction-sync-status.json")
        roles = load(root, "monitor-role.json")
        work = load(root, ctx["register"])
        if not all(isinstance(x, dict) for x in (brief, status, cert, roles, work)):
            raise ValueError("required JSON must be an object")
    except (OSError, ValueError) as e:
        return {"schema_version": 1, "mode": "full", "ready_for_short": False,
                "reasons": ["required JSON missing or invalid: " + type(e).__name__],
                "read": ["7 canonical instructions", "video-prompts.md", "live status", "open owner_decisions"]}

    if brief.get("generator") != "d7-1.0":
        reasons.append("unknown brief generator")
    if brief.get("valid_at_generation") is not True:
        reasons.append("brief was invalid at generation")
    inv = brief.get("invariants") or []
    if (not isinstance(inv, list) or len(inv) != 15
            or not all(isinstance(i, dict) and i.get("anchor_ok") is True for i in inv)):
        reasons.append("D7 invariant anchors are not 15/15")
    else:
        if {i.get("id") for i in inv} != {i[0] for i in INVARIANTS}:
            reasons.append("D7 invariant IDs are incomplete")
        for iid, _, doc, anchor, keywords in INVARIANTS:
            try:
                body = section(local_file(root, doc).read_text(encoding="utf-8-sig"), anchor)
                if body is None or not all(k.lower() in body.lower() for k in keywords):
                    reasons.append("D7 canonical anchor missing: " + iid)
            except (ValueError, OSError):
                reasons.append("D7 canonical source missing: " + doc)

    sources = brief.get("sources") or []
    seen = set()
    if not isinstance(sources, list):
        sources = []
        reasons.append("invalid source list")
    for entry in sources:
        if not isinstance(entry, dict):
            reasons.append("invalid source entry")
            continue
        name = entry.get("file", "")
        if not isinstance(name, str):
            reasons.append("invalid source name")
            continue
        seen.add(name)
        try:
            path = local_file(root, name)
        except ValueError:
            reasons.append("source missing or unsafe: " + str(name))
            continue
        actual = sha(path.read_bytes())
        if actual != entry.get("sha256"):
            reasons.append("stale brief source: " + name)
        if name.endswith(".md") and name != "video-prompts.md":
            declared = (cert.get("files") or {}).get(name, {}).get("mirror_sha256")
            if declared != actual:
                reasons.append("instruction certificate mismatch: " + name)

    if len(sources) != 8 or seen != set(DOCS) | {MASTER[0]}:
        reasons.append("incomplete canonical source list")
    try:
        cp = local_file(root, "shadow/current-checkpoint.md").read_bytes()
        declared = brief.get("current_checkpoint") or {}
        if not cp.strip() or declared.get("source") != "NEW-CHAT-HANDOFF.md":
            reasons.append("invalid shadow checkpoint")
        if sha(cp) != declared.get("sha256"):
            reasons.append("shadow checkpoint hash mismatch")
    except (ValueError, OSError):
        reasons.append("shadow checkpoint missing")
    if status.get("health") != "ok":
        reasons.append("project-status health not ok")
    if cert.get("health") != "ok" or cert.get("source_of_truth") != "github":
        reasons.append("instruction certificate health/authority not ok")
    master = root / "video-prompts.md"
    if master.is_file() and status.get("canonical_master_sha256") != sha(master.read_bytes()):
        reasons.append("master vs project-status sha256 mismatch")
    if work.get("schema_version") != 1 or not isinstance(work.get("active_work"), list):
        reasons.append("invalid work resume register")
    if roles.get("primary") not in ("robot", "chatgpt", "claude"):
        reasons.append("unknown monitor authority")
    if roles.get("primary") != "robot":
        warnings.append("telemetry role changed: consult live monitor-role before acting")
    if project != "seregius":
        ps = load(root, ctx["status"])
        if ps.get("health") != "ok" or ps.get("canonical_master_sha256") != sha(local_file(root, ctx["master"]).read_bytes()):
            reasons.append("project master/status mismatch: " + project)
        for key in ("handoff", "instructions", "checkpoint", "queue"):
            local_file(root, ctx[key])
    recovery = verify_recovery(root, work, work_id, project)
    reasons.extend(recovery["reasons"])
    warnings += [
        "Always query live owner_decisions; stale cached state is not approval",
        "Check full task-specific sections; never execute a paid generation from a resume hint",
        "A checkpoint is a recovery aid, not retained chat memory",
    ]
    return {
        "schema_version": 2, "project": project,
        "mode": "full" if reasons else "short",
        "ready_for_short": not reasons,
        "ready_for_resume": not reasons,
        "execution_authorized": False,
        "reasons": reasons,
        "warnings": warnings,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "read": (["7 canonical instructions", "video-prompts.md", "all relevant live status",
                  "open owner_decisions"] if reasons else [
                  "shadow/takeover-brief.md (15/15 anchors)",
                  "shadow/current-checkpoint.md verbatim",
                  "project-status.json + topview-status.json + instruction-sync-status.json",
                  "automation-monitor-status.json + monitor-role.json",
                  ctx["packet_dir"] + "/resume-packet.md + " + ctx["register"] + " selected entry; full register only if needed",
                  "open owner_decisions via Supabase",
                  "full task-specific sections from D7 read_sets"]) +
                 ([ctx[k] for k in ("handoff", "instructions", "status", "checkpoint", "queue", "lock")]
                  if project != "seregius" else []),
        "selected_work": recovery["selected_work"],
        "active_work": (work.get("active_work", []) if include_work else [
            {k: w.get(k) for k in ("work_id", "title", "status", "continuation_work_id") if w.get(k)}
            for w in work.get("active_work", []) if isinstance(w, dict)]),
        "authority": roles.get("primary"),
        "next_step": ("Read canonical sources in full, reconcile incident, then resume safely" if reasons
                      else recovery["selected_work"]["next_action"]),
    }


def evaluate(root, work_id=None, include_work=False, project="seregius"):
    try:
        return _evaluate(root, work_id, include_work, project)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as e:
        return {"schema_version": 2, "mode": "full", "ready_for_short": False,
                "ready_for_resume": False, "execution_authorized": False,
                "selected_work": None, "reasons": ["Malformed recovery data: " + str(e)],
                "read": ["7 canonical instructions", "live status", "open owner_decisions"]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("repo", nargs="?", default=".")
    p.add_argument("--project", default="seregius")
    p.add_argument("--output", default="")
    p.add_argument("--work-id", help="Explicit user-requested task; never inferred from update time")
    p.add_argument("--include-work", action="store_true", help="Include the full historical register")
    p.add_argument("--require-short", action="store_true", help="Return nonzero if short recovery fails")
    args = p.parse_args()
    result = evaluate(Path(args.repo), args.work_id, args.include_work, args.project)
    content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        dest = Path(args.output)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    print(content)
    # A full-read fallback is a safe valid outcome, not a CI failure.
    return 1 if args.require_short and not result["ready_for_short"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
