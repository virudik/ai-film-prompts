#!/usr/bin/env python3
"""Read-only lint of video-prompts.md production prompts against PROMPT-STYLE-GUIDE (sections 5, 6, 8, 11, 16A).

Writes nothing. Prints a JSON report to stdout. Heuristic: findings are leads for a human/ChatGPT, not verdicts.
usage: python3 reports/tools/prompt_lint.py [video-prompts.md]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import topview_prompt_match as pm  # noqa: E402

text = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "video-prompts.md").read_text(encoding="utf-8")
blocks = pm.master_blocks(text)


def scene_meta(scene):
    m = re.search(r'<a id="scene-%s"></a>.*?scene-meta:\s*(\{.*?\})\s*-->' % scene, text, re.S)
    return json.loads(m.group(1)) if m else {}


def to_s(h, m_, s):
    return int(h) * 3600 + int(m_) * 60 + int(s) if h is not None else int(m_) * 60 + int(s)


def timeline_spans(body):
    """Spans like [0:00–0:06], [00:00–00:05], 0–3s:, 2–9s: -> list of (start,end) seconds."""
    spans = []
    for a, b in re.findall(r"\[(\d+:\d{2})\s*[–-]\s*(\d+:\d{2})\]", body):
        f = lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1])
        spans.append((f(a), f(b)))
    if not spans:
        for a, b in re.findall(r"^\s*(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)s\b", body, re.M):
            spans.append((float(a), float(b)))
    return spans


out = []
for label, body in blocks:
    scene = int(re.match(r"\d+", label).group(0))
    meta = scene_meta(scene)
    f = []
    mode_line = body.split("\n")[0]
    dur = re.search(r"Duration:\s*(\d+)s", mode_line)
    dur = int(dur.group(1)) if dur else None
    native_on = "Native audio: on" in mode_line
    # sections
    up = body
    def has(*pats):
        return any(re.search(p, up, re.I) for p in pats)
    if not has(r"FRAME FILL"):
        f.append("no FRAME FILL / NO BARS")
    if not has(r"NEGATIVE"):
        f.append("no NEGATIVE PROMPT")
    if native_on and not has(r"\bAUDIO\b"):
        f.append("Native audio on but no AUDIO section")
    if not has(r"TIMELINE|STORY FLOW|\[\d+:\d{2}"):
        f.append("no timeline")
    if not has(r"CAMERA"):
        f.append("no CAMERA block")
    if not has(r"IDENTITY LOCK", r"identity (reference|authority|lock)", r"APPEARANCE"):
        f.append("no identity lock wording")
    if not has(r"START STATE", r"STARTING STATE"):
        f.append("no START STATE")
    if not has(r"END STATE"):
        f.append("no END STATE")
    # image refs
    used = sorted(set(re.findall(r"@(?:Image|image)(\d+)", body)), key=int)
    refsec = re.search(r"REFERENCES[^\n]*\n(.*?)(?:\n\n|\Z)", body, re.S)
    defined = sorted(set(re.findall(r"^@(?:Image|image)(\d+)\b", body, re.M)), key=int)
    undefined = [u for u in used if u not in defined]
    if undefined:
        f.append("@Image used but never defined at line start: " + ",".join(undefined))
    if re.search(r"@(?:Video)\d", body) and not re.search(r"^@Video\d", body, re.M):
        f.append("@Video used but not defined")
    # dependency leaks
    for pat, why in [(r"\b(see|follow)\b[^\n]{0,30}\babove\b", "'see/follow above'"),
                     (r"references/[\w/\-\.]+", "repo file path inside prompt"),
                     (r"\bPart ?1[0-3]?\b|Parts ?\d", "cross-reference to other Parts"),
                     (r"[Ee]ditorial cut|editorial operation", "editorial note inside prompt"),
                     (r"Use this prompt only", "operator instruction inside prompt"),
                     (r"older [A-Za-z\- ]*wording", "mentions 'older wording' the model never saw")]:
        mm = re.findall(pat, body)
        if mm:
            f.append(f"{why}: {len(mm)}x")
    prev = sorted(set(re.findall(r"Scene (\d+)", body)), key=int)
    prev = [p for p in prev if int(p) != scene]
    if prev:
        f.append("mentions other scenes: " + ",".join(prev))
    # duplication: repeated long sentences
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", body) if len(s.strip()) > 60]
    dup = len(sents) - len(set(sents))
    if dup:
        f.append(f"{dup} verbatim duplicate sentences")
    # timeline
    spans = timeline_spans(body)
    if spans and dur:
        if spans[0][0] != 0:
            f.append(f"timeline starts at {spans[0][0]}")
        end = max(e for _, e in spans)
        if abs(end - dur) > 1:
            f.append(f"timeline ends at {end}s but Duration {dur}s")
        for (a1, b1), (a2, b2) in zip(spans, spans[1:]):
            if a2 < b1 - 0.01:
                f.append(f"timeline overlap {b1}->{a2}")
            elif a2 > b1 + 0.01:
                f.append(f"timeline gap {b1}->{a2}")
    # engine
    opt = re.search(r"Optimized for ([A-Za-z0-9\. ]+?)(?:\s*\||\n|$)", body) or re.search(r"Target model: ([A-Za-z0-9\. ]+?)(?:\s*\||\n)", body)
    engine_prompt = opt.group(1).strip() if opt else None
    engine_meta = meta.get("target_engine")
    if label.startswith("28 "):
        engine_meta = "Seedance 2.0" if label.split()[1].startswith("A") else "Wan 3.0"
    if label.startswith("27 · Seedance 2.0"):
        engine_meta = "Seedance 2.0"
    if engine_prompt and engine_meta and engine_prompt.replace(" ", "").lower()[:8] != engine_meta.replace(" ", "").lower()[:8]:
        f.append(f"engine in prompt '{engine_prompt}' != scene-meta '{engine_meta}'")
    ru_dialogue = bool(re.search(r"[«»]", body)) and (meta.get("dialogue") or {}).get("language") == "ru"
    if ru_dialogue and engine_prompt and not engine_prompt.lower().startswith("wan"):
        f.append("Russian dialogue but engine is not Wan")
    out.append({"label": label, "chars": len(body), "duration": dur, "images_used": used,
                "images_defined": defined, "engine_prompt": engine_prompt, "engine_meta": engine_meta, "flags": f})
print(json.dumps(out, ensure_ascii=False, indent=1))
