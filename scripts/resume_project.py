"""Validated repository-relative recovery paths; no implicit cross-project fallback."""
import json
from pathlib import Path


def context(root, project="seregius"):
    if project == "seregius":
        p = {"id": project, "name": "Серёгиус", "root": ".",
             "handoff": "NEW-CHAT-HANDOFF.md", "instructions": "AI-PROJECT-GUIDE.md",
             "master": "video-prompts.md", "status": "project-status.json",
             "queue": "ops/topview-launch-queue.json", "lock": "ops/canon-lock.json"}
    else:
        registry = json.loads((Path(root) / "projects/projects.json").read_bytes())
        matches = [p for p in registry["projects"] if p["id"] == project]
        if len(matches) != 1:
            raise ValueError("unknown or ambiguous project: " + str(project))
        p = dict(matches[0])
        if p["root"] != "projects/" + project or not all(c.isalnum() or c == "-" for c in project):
            raise ValueError("unsafe project root")
        for key in ("handoff", "instructions", "master", "status", "queue", "lock"):
            if not p[key].startswith(p["root"] + "/") or ".." in Path(p[key]).parts:
                raise ValueError("cross-project source: " + key)
    prefix = "" if project == "seregius" else p["root"] + "/"
    return dict(p, prefix=prefix, register=prefix + "work-resume-register.json",
                checkpoint=prefix + "reports/current-work-checkpoint.md",
                packet_dir=prefix + "shadow", receipts=prefix + "reports/handoff-receipts.json")
