# QC preflight — postqc fixes pack

## Four corrective replacements (READY_TO_SEND for next bounded wave)

| v2 | replaces | s | key change |
|---|---|---:|---|
| A04_shred-v2 | A04_shred | 7 | nip-ingestion ref; no fall-through |
| A05_material-v2 | A05_material | 5 | flakes only; no pellets; no morph |
| C01_orbit-v2 | C01_orbit | 5 | one 2-wing locked craft; no panel growth |
| C06_cycle-v2 | C06_cycle | 5 | clean blank-chest identity; one throw |

## Stage3 candidates (geometry-aligned, not yet waved)

C02_debris-v2, C03_capture-v2 (same polymer gripper product), C04_recycle-v2, C05_station-v2

## Unchanged
B03_build, B04_check, B06_liftoff — no real finding forcing rewrite
A03_sort, B05_pad — QC candidates, do not regenerate
Wave2 six — do not race

## Policy
references-only; no image_path/last_frame/keyframes/resolution; 16:9
