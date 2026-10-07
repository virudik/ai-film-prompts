# Scene Reference Pack Plan — AI Film Серёгиус

Updated: 2026-10-07

Purpose: one deterministic reference pack per active Scene ID. Drive is authority; GitHub/site is the public thumbnail mirror; Library is recovery only; Topview task inputs are generation provenance/telemetry, not canonical story authority.

## Global workflow

1. Before a scene is created or launched, read fresh canonical master + prompt guide + scene pack manifest.
2. Reuse approved character sheets, exact location refs, exact props and exact first/last frames before making anything new.
3. Decide whether the scene needs additional scene-specific stills: pair/group blocking, pose, prop handoff, lighting state, or continuity state.
4. Generate one still at a time. After each result, visually compare identity, wardrobe, location, geometry, pose and character count. Reject drift/duplicates/merged faces/incorrect anatomy.
5. The moment a still is accepted as useful, SAVE IT BEFORE THE NEXT GENERATION: Drive Scene pack + Library recovery + GitHub/site thumbnail when it is part of the scene inputs.
6. Multi-character images are built from small verified groups/subgroups; individual sheets always outrank composition helpers for identity.
7. For scenes already rendered in Topview, recover and record the exact input-image S3 sources from the corresponding task; reuse them and propose only additive improvements.
8. On the site, scene-used reference images are shown as compact thumbnails linking to the full file. Do not let full-size images change the page scale.
9. Command `запускай сцену N` means: fresh-read master/status -> resolve scene pack -> ensure required references -> update prompt reference mapping if needed -> preflight Topview model/slots/cost -> submit only after the user's command. Technical success never means approval.
10. Never silently spend credits for a reference-image helper. Prefer an actually verified unlimited route when available; otherwise stop before submit and report the cost/path issue.

## Active-scene audit

| Scene | Priority | Existing inputs | Additional reference work |
|---|---|---|---|
| 10 | HIGH | cantina composition/Chewbacca + Han + Jedi | Create one clean identity-locked three-shot/axis anchor; optionally a reaction-state still shared with Scene 11. |
| 11 | HIGH | same as Scene 10 | Reuse Scene 10 pack; create only a continuation/end-state still if needed. |
| 13 | HIGH | council composition + Luchik + Black + Purple; Topview source inputs exist | Create clean council still with Luchik lying horizontally across Purple's lap + true cat close-up reference for speaking beat. |
| 16 | HIGH | desert-ruins video + 2 Jedi + Serega | Create clean three-character standoff in exact ruins + optional worm scale/composition still. |
| 17 | HIGH | Pasha + Sasha + Serega + cave + map + continuity video; Topview source inputs exist | Create post-battle seated composition + clear map-handoff pose/reference. |
| 19 | MEDIUM | start fishing comp + running end comp + Masha + Sasha + Pasha; Topview source inputs exist | Preserve current start/end; add face-to-face Masha/Sasha confrontation only if identity drift persists. |
| 20 | MEDIUM-HIGH | exact lake + exact Masha; Topview source inputs exist | Add 3 optional pose anchors for 11-part sequence: wide standing, side-walk/profile, close performance. Do not redesign Masha. |
| 21 | LOW/CONDITIONAL | exact first/last frames + Serega + Yulya; Topview source inputs exist | Existing first/last-frame workflow is sufficient unless identity drift is found; then create corrected bridge-start still only. |
| 22 | NONE/LOW | exact first and last frames; Topview source inputs exist | No new still required unless geometry mismatch is observed. |
| 23 | LOW | start people frame + pair-cat target + individual cats; Topview source inputs exist | Existing references are sufficient if pair target is clean; regenerate only if pair identity/scale is wrong. |
| 24 | LOW | cat pair + individual cats + approved exact cockpit; Topview source inputs exist | Already strong reference pack; no new still by default. |
| 25 | MEDIUM/CONDITIONAL | same cockpit/cats | Reuse Scene 24. Add battle-light cockpit still only if result shows interior/light drift. |
| 26 | MEDIUM | cat pair + individual cats + exact ruins; Topview source inputs exist | Prepare a clean two-cat dialogue staging still in exact ruins for future rerender only; do not interrupt current slow task. |
| 27 | HIGH | cat pair + Serega + individual cats + exact ruins; Topview source inputs exist | Prepare exact 3-subject confrontation/action-staging still; current video tasks remain untouched until result/decision. |
| 28 | HIGHEST | H28A/H28B + individual sheets + accepted P28/L28/F28; R28A/R28B composition-only | Correct S28 shoulder-carry pose; rebuild G28 without identity mixing/duplicates; keep accepted refs immutable unless user asks. |

## Current Topview provenance checkpoint

Scenes with proven Topview task-input recovery available from live board metadata: 13, 17, 19, 20, 21, 22, 23, 24, 26, 27. Their original input S3 paths can be bridged into an authorized Topview Canvas media node and downloaded/reused without asking the owner to upload the same images again.

Nano Banana 2 is visible in live Topview image-edit config. The AI Film board history contains successful Nano Banana 2 image-edit tasks marked `useUnlimitMode: true` and `creditsCost: 0`. However, the generic standalone connector submit route does not expose an explicit unlimited-mode switch, so automation must preflight and must never silently fall back to a credit-consuming route.