#!/usr/bin/env python3
"""Match Topview tasks to master prompts by parameters.positivePrompt — READ-ONLY helper.

Used by .github/workflows/topview-prompt-match.yml (workflow_dispatch). It performs GET
/boards/tasks/detail only, never submits/approves/reruns/deletes anything and never writes any file
of the repository (no telemetry, no task map, no scenes). Result = annotations only:

    task_id -> Scene/part + confidence

The prompt text, API key and uid are never printed. Task ↔ Scene mapping stays the monitor's /
ChatGPT's job: this script only produces evidence for the report.

Confidence levels (normalised text = CRLF→LF, <<<ImageN>>>/@imageN → @ImageN, whitespace collapsed):
  exact       byte-identical block (after CRLF→LF and strip)
  normalized  identical after normalisation (CRLF, image-token spelling, padding around tokens)
  high        >= 0.97 similarity and clearly ahead of the runner-up (edited by a few words)
  medium      >= 0.85
  low         below that / ambiguous runner-up -> owner/ChatGPT decide

usage: topview_prompt_match.py [--repo DIR] [--tasks id,id,...] [--from-shadow]
"""
import argparse
import difflib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import topview_api_scan as scan  # noqa: E402

HEAD_RE = re.compile(r"^(#{2,4})\s+(.*)$")


def master_blocks(text):
    """[(label, body)] for every fenced prompt block of video-prompts.md, in file order."""
    lines = text.split("\n")
    out, scene, in_block, start, body = [], None, False, 0, []
    heading = ""
    seen_in_scene = 0
    for line in lines:
        if line.startswith("```"):
            if not in_block:
                in_block, body = True, []
            else:
                in_block = False
                out.append((label_for(scene, heading, seen_in_scene), "\n".join(body)))
                seen_in_scene += 1
            continue
        if in_block:
            body.append(line)
            continue
        m = HEAD_RE.match(line)
        if not m:
            continue
        level, title = len(m.group(1)), m.group(2).strip()
        sm = re.match(r"Сцена\s+(\d+)\b", title) if level == 2 else None
        if sm:
            scene, seen_in_scene = int(sm.group(1)), 0
        heading = title
    return out


def label_for(scene, heading, index_in_scene):
    if scene == 20:
        m = re.search(r"Песня Маши\s+(\d+)", heading)
        return f"20 · песня {m.group(1)}" if m else "20"
    # Alternative engine versions of one scene (site tabs, see PROMPT-STYLE-GUIDE §7А):
    # "#### 37 · Seedance 2.5 · 30 с", "#### 16 · Wan 3.0", "#### 49 · Wan 3.0 часть 2 · 49C + 49D",
    # "#### 42 · Seedance 2.0 часть 1". The scene's first block keeps the bare label "N".
    m = re.match(rf"{scene}\s*·\s*(Wan 3\.0|Seedance 2\.5|Seedance 2\.0)(?:\s+часть\s+(\d+))?", heading)
    if m and index_in_scene > 0:
        return f"{scene} · {m.group(1)}" + (f" часть {m.group(2)}" if m.group(2) else "")
    if scene == 28:
        m = re.match(r"([ABC]\d+)\b", heading)
        return f"28 {m.group(1)}" if m else "28"
    if scene == 27:
        m = re.match(r"Часть\s+(\d+)", heading)
        return f"27 · Seedance 2.0 часть {m.group(1)}" if m else "27 · основной 30 с"
    # Scene 49 rock-band and Scene 50 Wookiee audience have independent A–F / A–B parts.
    # Keep each text block uniquely identifiable for matching and collision prevention.
    if scene in (49, 50, 51):
        m = re.match(rf"({scene}[A-Z])\b", heading)
        return m.group(1) if m else str(scene)
    return str(scene)


def normalise(s):
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"<<<\s*(Image|Video|Audio)\s*(\d+)\s*>>>", lambda m: "@" + m.group(1).capitalize() + m.group(2), s, flags=re.I)
    s = re.sub(r"@(image|video|audio)\s*(\d+)", lambda m: "@" + m.group(1).capitalize() + m.group(2), s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip()
    # Topview pads separators BETWEEN reference tokens: "@Image1 –@Image3" or
    # "@Image3 /@Image4". Preserve the separator, token IDs/order and all prose.
    s = re.sub(r"(@(?:Image|Video|Audio)\d+) ?([–—/]) ?(?=@(?:Image|Video|Audio)\d)", r"\1\2", s)
    return re.sub(r"\(\s+", "(", re.sub(r"\s+([,);.:])", r"\1", s))   # Topview pads image tokens: "<<<Image1>>> ,"


def similarity(a, b):
    """Word-level ratio of the normalised texts: robust to small edits, sensitive to reordering."""
    return difflib.SequenceMatcher(None, normalise(a).split(" "), normalise(b).split(" "), autojunk=False).ratio()


def classify(task_prompt, blocks):
    raw = task_prompt.replace("\r\n", "\n").strip()
    norm = normalise(task_prompt)
    exact = [l for l, b in blocks if b.replace("\r\n", "\n").strip() == raw]
    if exact:
        return exact[0], "exact", 1.0, None
    same = [l for l, b in blocks if normalise(b) == norm]
    if same:
        return same[0], "normalized", 1.0, None
    ranked = sorted(((similarity(task_prompt, b), l) for l, b in blocks), reverse=True)
    best, label = ranked[0]
    runner = ranked[1][0] if len(ranked) > 1 else 0.0
    if best >= 0.97 and best - runner >= 0.03:
        level = "high"
    elif best >= 0.85:
        level = "medium"
    else:
        level = "low"
    return label, level, round(best, 3), round(runner, 3)


def fetch_prompt(client, task_id):
    d = scan.task_detail(client, task_id)
    if not isinstance(d, dict):
        return None, None
    p = d.get("parameters") if isinstance(d.get("parameters"), dict) else {}
    return (p.get("positivePrompt") or ""), p.get("modelName")


def target_engine(text, label):
    """Engine the master names for the block's scene (informational only)."""
    scene = re.match(r"\d+", label).group(0)
    m = re.search(r'<a id="scene-%s"></a>.*?scene-meta:\s*(\{.*?\})\s*-->' % scene, text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1)).get("target_engine")
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--tasks", default="", help="comma-separated task ids; default: unknown_new of the shadow status")
    a = ap.parse_args()
    repo = Path(a.repo)
    key, uid = os.environ.get("TOPVIEW_API_KEY", ""), os.environ.get("TOPVIEW_UID", "")
    if not key.strip() or not uid.strip():
        print("::notice title=topview-prompt-match::not configured: TOPVIEW_API_KEY or TOPVIEW_UID absent; nothing done")
        return 0
    ids = [x.strip() for x in a.tasks.split(",") if x.strip()]
    if not ids:
        shadow = scan.read_json(repo / "shadow" / "topview-robot-status.json", {})
        ids = [u["task_id"] for u in shadow.get("unknown_new", []) if u.get("task_id")]
    if not ids:
        print("::notice title=topview-prompt-match::no tasks to match")
        return 0
    text = (repo / "video-prompts.md").read_text(encoding="utf-8")
    blocks = master_blocks(text)
    client = scan.Client(key, uid)
    for tid in ids:
        try:
            prompt, model = fetch_prompt(client, tid)
        except scan.ApiError as e:
            print(f"::error title=topview-prompt-match::{tid[:8]}: {e}")
            continue
        if not prompt:
            print(f"::warning title=topview-prompt-match::{tid} -> no positivePrompt in the detail answer")
            continue
        label, level, score, runner = classify(prompt, blocks)
        eng = target_engine(text, label)
        note = f"; runner-up {runner}" if runner is not None else ""
        engine = f"; task model {model} / master target {eng}" if eng and model and eng.split()[0].lower() not in str(model).lower() else ""
        print(f"::notice title=topview-prompt-match::{tid} -> Scene {label} · {level} (score {score}{note}){engine}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
