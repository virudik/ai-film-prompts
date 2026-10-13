#!/usr/bin/env python3
"""Read-only D7 'Продолжай' preflight. Never invents conversational memory.

Reads a fresh local checkout of GitHub main and verifies generated brief *against
current bytes*, not only against its at-generation validity claim.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(root, name):
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def evaluate(root):
    root = Path(root)
    reasons, warnings = [], []
    try:
        brief = load(root, "shadow/takeover-brief.json")
        status = load(root, "project-status.json")
        cert = load(root, "instruction-sync-status.json")
        roles = load(root, "monitor-role.json")
        work = load(root, "work-resume-register.json")
    except (OSError, ValueError) as e:
        return {"schema_version": 1, "mode": "full", "ready_for_short": False,
                "reasons": ["required JSON missing or invalid: " + type(e).__name__],
                "read": ["7 canonical instructions", "video-prompts.md", "live status", "open owner_decisions"]}

    if brief.get("generator") != "d7-1.0":
        reasons.append("unknown brief generator")
    if brief.get("valid_at_generation") is not True:
        reasons.append("brief was invalid at generation")
    inv = brief.get("invariants") or []
    if len(inv) != 15 or not all(i.get("anchor_ok") is True for i in inv):
        reasons.append("D7 invariant anchors are not 15/15")

    sources = brief.get("sources") or []
    seen = set()
    for entry in sources:
        name = entry.get("file", "")
        seen.add(name)
        path = root / name
        if not name or name.startswith("/") or ".." in Path(name).parts or not path.is_file():
            reasons.append("source missing or unsafe: " + str(name))
            continue
        actual = sha(path.read_bytes())
        if actual != entry.get("sha256"):
            reasons.append("stale brief source: " + name)
        if name.endswith(".md") and name != "video-prompts.md":
            declared = (cert.get("files") or {}).get(name, {}).get("mirror_sha256")
            if declared != actual:
                reasons.append("instruction certificate mismatch: " + name)

    if len(sources) != 8 or "video-prompts.md" not in seen:
        reasons.append("incomplete canonical source list")
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
    warnings += [
        "Always query live owner_decisions; stale cached state is not approval",
        "Check full task-specific sections; never execute a paid generation from a resume hint",
        "A checkpoint is a recovery aid, not retained chat memory",
    ]
    return {
        "schema_version": 1,
        "mode": "full" if reasons else "short",
        "ready_for_short": not reasons,
        "reasons": reasons,
        "warnings": warnings,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "read": (["7 canonical instructions", "video-prompts.md", "all relevant live status",
                  "open owner_decisions"] if reasons else [
                  "shadow/takeover-brief.md (15/15 anchors)",
                  "shadow/current-checkpoint.md verbatim",
                  "project-status.json + topview-status.json + instruction-sync-status.json",
                  "automation-monitor-status.json + monitor-role.json",
                  "work-resume-register.json",
                  "open owner_decisions via Supabase",
                  "full task-specific sections from D7 read_sets"]),
        "active_work": work.get("active_work", []),
        "authority": roles.get("primary"),
        "next_step": ("Read canonical sources in full, reconcile incident, then resume safely" if reasons
                      else "Select most recent still-open verified task and continue its next reversible step"),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("repo", nargs="?", default=".")
    p.add_argument("--output", default="")
    args = p.parse_args()
    result = evaluate(Path(args.repo))
    content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        dest = Path(args.output)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    print(content)
    # A full-read fallback is a safe valid outcome, not a CI failure.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
