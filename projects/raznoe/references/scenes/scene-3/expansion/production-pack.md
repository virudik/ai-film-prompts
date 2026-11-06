# RESOURCE expansion — production pack (workshop repair 2026-11-06)

**Статус:** workshop-цепочка исправлена после отклонения ложного «all 18 READY».  
**Первая волна генератора не тронута:** A03_sort, A04_shred, A05_material, B05_pad, C01_orbit, C06_cycle (SHA совпали до/после).  
**Видео здесь не генерировались.**

## A_workshop — причинная цепь (обязательная)

| Clip | s | START | END |
|---|---:|---|---|
| **A01_drop** | 7 | чертёж; clear PET **синяя крышка** на столе | бутылка **внутри** тёмного бака |
| **A02_retrieve** | 8 | бутылка **уже внутри** тёмного бака | **видимое** извлечение завершено; бутылка в руке **вне** бака; синего нет |
| **A02_blue** | 7 | у синего, бутылка уже в руке (склейка перехода) | бутылка **внутри** синего |

Идентичность бутылки: clear PET + blue screw-cap во всех трёх. В LOC-45728 возможен distractor с другой крышкой — в промптах явно игнорировать.

Новый ref: `assets/PROP-bottle-retrieved-clear-of-bin.png` (end-state извлечения; не exact frame).

## Хронометраж пакета

**19 клипов · 116 с** (workshop 22 с вместо прежних 14 с с пропуском retrieval).

## t352

Генерации по мере готовности → Drive/Sasha → videoReview. Следующая волна после этой починки — на стороне generation executor.

## Политика

references-only; без image_path/last_frame_path/keyframes/resolution; 16:9.
