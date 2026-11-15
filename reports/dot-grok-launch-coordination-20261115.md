# Dot / Grok launch coordination — 2026-11-15

## Scope and owner decision

Owner asks that the first executor to safely claim a ready launch performs it, and the other provides backup without duplicate videos. No scene edits, queue reorder, paid generation, changed schedules, or interception of a foreign lease are part of this implementation.

## Observed incident

Dot's full live scan at 15:15:27Z found S89B task `90db5dd309db477eb346e8d82676f7b5`, created 15:11:23Z, Unlimited0, Wan 3.0, 30s, 720p, 16:9, audio, five images. Full normalized prompt SHA256: `819be4464fa3119384833cd5e8ef675186deb8a9b1b7b0952755b2ddf063ef20`. Canonical queue had not yet caught up. At the original observation the originating executor was not established. Before publication, fresh main `8937f88` contained merged Grok PR #704 and the matching S89B receipt; the queue is now `submitted`. This receipt and task are preserved without modification. Dot did not submit S89B. Missing canonical receipt cannot establish that no Create happened.

## Changes

- `launcher_coordination.py prepare-claim`: common first-writer claim for all existing surfaces, exact lease/route, next authorized ready item from fresh snapshot, verified preflight and explicit live duplicate reconciliation. Local helper does not publish or launch; remote main-head CAS determines the winner.
- Claims v2 are bound to the exact lease. Reacquiring a lease does not revive an old claim.
- `verify-before-create`: exact fresh readback of claim+intent+lease+route; complete item payload SHA256; current hold/music/continuity/refusal checks; fresh global capacity and item reconciliation; required ledger binding. Stale intent (>120 seconds), existing task, ambiguous scan, changed payload, or foreign lease fail closed.
- Both claim and intent remain separate CAS transactions. One uninterrupted intent permits at most one UI Create. Unknown submission and interrupted execution require reconciliation, never TTL-based reset.
- Coordination instructions explicitly include Dot, Grok and hourly backups, short write-only lease for read-only checks, and adoption evidence rather than assumptions.

## Limitations / rollout

This is cooperative cross-agent fencing, not a server-enforced Topview idempotency mechanism. A GUI action that bypasses the common guard cannot be technically prevented here. Old recorded intents are not retroactively converted into fresh permissions. The new final gate requires v2. Existing lower-level intent preparation remains compatible for reconciliation/history and is not evidence that another agent adopted the new entry path.

Before declaring both executors covered, obtain Grok's own read-only acceptance receipt proving it uses fresh main, refuses foreign lease/claim, and uses the common entry path before any future Create. No such acceptance was fabricated, and no message or test video was sent by this implementation task.

## Verification

Final local verification: 571 Python tests passed under `/usr/bin/python3` (including 85 focused launcher tests); `git diff --check` passed. See completion report for publication SHA and CI status. Tests are local, with no Topview Create. The race test is an explicit CAS model, not a live concurrent GitHub/Topview integration test. Existing lease, route, Grok, retry and run-ledger tests remain included.
