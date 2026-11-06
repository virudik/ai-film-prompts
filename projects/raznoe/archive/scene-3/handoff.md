# RESOURCE — scene 3 site-ready handoff

**Project:** «Разное» (raznoe) on https://github.com/virudik/ai-film-prompts  
**Site scene:** scene 3 «RESOURCE» — ONE site scene (do **not** split into 10 separate site scenes for each PNG).  
**Source:** Yandex Disk public folder part **1 of 3** only (`https://disk.yandex.ru/d/ikegeH83rmpK1g`). Parts 2–3 were unavailable; do not invent them.  
**User decision (verbatim):** «Клади сцену 3 на сайт и перерисуй финал 45737 под полимер»  
**Authorization:** only **one** new image authorized (corrected finale `45737.png`). All other source PNGs kept byte-identical to the provided originals.  
**This bundle:** prep only. Parent adapts site + Topview via CloudAgent. Do **not** launch video / Topview queue from this folder. No repo edits in this step.

---

## Narrative (from Prompt.docx — plot intent)

BLOCK 1 “RESOURCE”: ~30 s photoreal sci-tech promo, two 15 s Grok Imagine Video generations.

**Video 1 — idea and first step (workshop):**  
Engineer (mid-30s, curly dark brown hair, short beard, black T-shirt with existing red band graphic, black trousers, black watch, no glasses) studies a technical drawing; carelessly drops a transparent PET water bottle into ordinary waste; rethinks; retrieves it; throws it into a blue recycling container. Continuity end-frame: bottle entering the blue container for Video 2 start.

**Video 2 — waste → new material (industrial, no main engineer):**  
Match-cut from bottle in blue bin → industrial sorting (female worker in dark blue coveralls, gloves, safety glasses) → shredder → recycled plastic flakes → **industrial 3D printer manufacturing an open-frame mechanical gripper for a future satellite manipulator from recycled polymer**. Finale must read as additive polymer, not metal CNC.

Visual progression: ordinary waste → separate collection → sorting → shredding → flakes → 3D-printed engineering component for space tech.

---

## Source → shot mapping (internal shot IDs ≠ site scenes)

| File | Role in Prompt.docx | Use |
|------|---------------------|-----|
| `45726.png` | Character sheet | Identity only for workshop; not a scene background |
| `45728.png` | Workshop / drawing study | Video 1 0–4 s |
| `45729.png` | Bottle into ordinary bin | Video 1 4–7 s |
| `45731.png` | Bottle near blue recycling container | Video 1 10–15 s |
| `45732.png` | Bottle thrown into blue container | Video 1 end / continuity |
| `45734.png` | Facility worker / compressed bottles | Video 2 sorting |
| `45735.png` | Worker inspecting bottle on line | Video 2 sorting |
| `45736.png` | Industrial plastic shredder | Video 2 shredding |
| `45733.png` | Processed plastic flakes | Video 2 recycled material |
| `45737-old.png` | Original finale (metal CNC — **wrong material**) | Kept for audit only; do not publish as finale |
| `45737.png` | **Corrected** finale — polymer AM / 3D print of gripper | Video 2 11–15 s; site gallery finale |

Internal numbering (45726…45737) is source asset IDs. On the site this remains **one** scene 3 card with a multi-shot gallery / timeline, not ten scene pages.

---

## Image aspect / size

- Story rule: **16:9 landscape**.  
- Most originals: **1672×941** PNG (~16:9). Character sheet `45726`: **1536×1024**.  
- Corrected `45737.png`: **1280×720** PNG (exact 16:9), photoreal industrial cinematic, consistent with factory grading.  
- Preview: `45737-preview.jpg` (same pixels as generation source).

---

## Material correction (45737)

**Problem:** original `45737` = shiny metal milling/CNC with chips in cold factory.  
**Required by doc:** industrial 3D printer; open-frame mechanical **gripper** for satellite manipulator; **recycled polymer** with visible deposition layers, heterogeneous texture, subtle blue/transparent inclusions; metal rails/head OK; object must be matte polymer; no chips/sparks.  
**Done:** regenerated once with original + flake/shredder refs; visual check: extruder nozzle + filament, layered polymer body with blue flecks, open-truss gripper-like frame on build plate, metal gantry retained, no metal swarf. Passes key material requirement (no second revise needed).

**Caution:** do not claim literal real-world recycled-traceability certification; images are cinematic fiction. No logos/watermarks. No new people in the corrected finale.

---

## Verbatim source vs suggestions

- **Verbatim:** `Prompt.docx` and `source-prompt.txt` (extracted plain text of the doc). Preserve Russian VO / plot when adapting; this English block is the generation brief in the source doc.  
- **Suggestions only (executor — optional for parent/CloudAgent; do not treat as source):**  
  1. Explicit Topview/model negative: *no CNC milling, no metal chips, no brushed aluminum workpiece, no sparks*.  
  2. Positive lock: *FDM/FFF or pellet extrusion, visible layer lines, matte recycled PET-like polymer, blue flake inclusions, open-frame satellite manipulator gripper*.  
  3. Continuity: extract Video 1 last frame as mandatory Video 2 first frame (already in doc).  
  4. Site: one scene 3 «RESOURCE»; gallery order matching progression table above; show corrected `45737`, archive `45737-old` off-gallery or as “replaced”.  
  5. Parts 2–3 of Yandex folder missing — ship part 1 only; no placeholder invents.

---

## Bundle contents

- Unchanged originals: `45726`, `45728`, `45729`, `45731`–`45736` PNG  
- `45737-old.png` (backup of metal CNC original)  
- `45737.png` (corrected polymer finale) + `45737-preview.jpg`  
- `Prompt.docx`, `source-prompt.txt`, `handoff.md`, `SHA256SUMS.txt`  
- Zip(s) under 25 MB each for attachment

Parent: adapt site + Topview prompts from this; do not start video generation from this handoff alone.
