# Source audit — wave1 rejects → postqc v2

Evidence paths are on this box. Relative timecodes are **inside each MP4 file** (not timeline of the whole film).

## A04_shred-v1 → A04_shred-v2

| Field | Value |
|---|---|
| File | `/workspace/RESOURCE-video/expanded-wave1/A04_shred-v1.mp4` |
| Duration | ~8.04 s |
| Relative TC | **0:02–0:04** whole bottles pass through solid metal discs; no nip capture / no deformation |
| Parent re-review | confirmed reject |
| Executed prompt | `/workspace/RESOURCE-native-wave1-2026-11-06/prompts/A04_shred.txt` |
| Executed ref | `FAC-shredder-45736.png` (flying fragments / ambiguous intake) |
| Classification | **Input weakness + video failure**: still asks for ingestion but authority image is mid-air shard chaos; model fall-through |
| v2 fix | `PROP-shredder-ingestion-v2.png` bottle in nip; 7s; one physics beat |

## A05_material-v1 → A05_material-v2

| Field | Value |
|---|---|
| File | `/workspace/RESOURCE-video/expanded-wave1/A05_material-v1.mp4` |
| Duration | ~5.04 s |
| Relative TC | **0:00–0:02** sharp clear/blue shards pour into a pile; **0:02–0:03** without hard cut, stream + settled pile smoothly morph into smooth round granules; **0:03–0:05** spheres only |
| Parent re-review | **FINAL reject** — internal morph, not allowed hard cut, not cross-file splice |
| Executed prompt | flakes + optional cut to pellets |
| Executed refs | `FAC-flakes-45733.png` + `A-recycled-pet-pellets.png` |
| Classification | **Input defect**: two material end-states in one short continuous clip invited morph; **video defect**: confirmed in-frame metamorphosis |
| v2 fix | flakes-only; pellets removed from this slot |

## C01_orbit-v1 → C01_orbit-v2

| Field | Value |
|---|---|
| File | `/workspace/RESOURCE-video/expanded-wave1/C01_orbit-v1.mp4` |
| Relative TC | **0:00–0:03** cross-shaped 4-panel growth; white arm mount drifts on flyaround |
| Executed refs | `PROP-satellite-manipulator-02.png` (capture/partial) + `B-satellite-assembly-stand.png` (2 wings, folded arm) |
| Classification | **Input defect**: two conflicting geometries + deploy language |
| v2 fix | `PROP-satellite-orbit-locked-v2.png` matching 2-wing assembly family; panels already deployed; 02 removed from C01 |

## C06_cycle-v1 → C06_cycle-v2

| Field | Value |
|---|---|
| File | `/workspace/RESOURCE-video/expanded-wave1/C06_cycle-v1.mp4` |
| Relative TC | throw **~0:02–0:04**; hard cut **~0:04** to other hand (no cuff) + second throw; bottle stretch/float ~3s; **MOU...** on uniform |
| Executed ref | multi-panel `ID-engineer-blue-form-01.png` with readable РОСКОСМОС |
| Classification | **Input defect**: letters on sheet vs “blank patch” text; **video**: double throw + stretch + garbage text |
| v2 fix | `ID-engineer-blue-form-CLEAN-single.png` blank chest; one continuous deposit; 5s |

## QC candidates (no regen)
- A03_sort-v1 — minor PET instability; readable hands
- B05_pad-v1 — no material defects reported

## Wave2 in flight — not modified
A01_drop, A02_retrieve, A02_blue, A06_print, B01_pickup, B02_install
