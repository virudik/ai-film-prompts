# QC preflight — workshop repair

## Не тронуто (первая волна)
A03_sort, A04_shred, A05_material, B05_pad, C01_orbit, C06_cycle — prompts/refs/requests неизменны.

## Workshop — фактическая проверка (не «READY вместо проверки»)

### State chain
- A01 END = inside dark bin → A02_retrieve START = already inside dark bin ✓
- A02_retrieve END = bottle in hand clear of dark bin, no blue → A02_blue START = at blue holding bottle (montage OK) ✓
- A02_blue END = inside blue ✓
- Realization beat present in A02_retrieve (glance drawing → bin) ✓
- Retrieval is a visible completed action in its own clip ✓

### Refs / policy
- All workshop `reference_image_paths` exist on disk ✓
- `<IMAGE_n>` order matches args ✓
- No image_path / last_frame_path / keyframes / resolution ✓
- Bottle identity locked to blue-cap PET; LOC distractor called out ✓

### Residual (first-pass video risks, not story skips)
- Retrieve still can look like “hold over bin”; prompt forces START inside + lift-out direction
- Finger/PET fusion on retrieve/deposit

## Остальной пакет
Клипы вне workshop/first-wave не пересобирались в этом шаге; прежние READY_TO_SEND для них остаются из prior review, но **не** утверждаются заново здесь как «все идеальны».
