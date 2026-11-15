# Dot primary, Grok backup · 15.11.2026

Owner requested one initial AI wake, not two competing full scans. This change routes notifications only; it never grants ownership or permission to Create.

## Activation status

Implementation staged behind `ops/relay-wake.json.dispatch.enabled=false`. The working legacy route remains unchanged until current-dot runtime ACK has been independently verified. Do not describe staged code as a completed switch. Existing HH:55/HH:00 insurance is unchanged and can still consume model quota.

## Enabled behavior

- New demand episode (active global task set) first wakes only dot through the existing configured ChatGPT Relay inbox. The audit issue has **no assignee**, so it does not also wake Grok through issue-assigned.
- A subsequent fresh complete robot scan checks the exact event receipt. Missing ACK after 10 minutes allows a backup wake. A real dated receipt/`execution.updated_at` suppresses another AI wake until 20 minutes without progress. Checks occur on actual robot runs, not exact promised deadlines.
- Any held unexpired/malformed global lease suppresses competing wakes. An expired lease does not clear claim/intent or authorize Create.
- Backup wake uses the existing Grok GitHub issue-assigned route, **without a duplicate dot DM**. Further backup checks are paced at 60 minutes while demand remains.
- Both workers obey the shared CAS/lease/claim/intent/verify protocol. Any claimed/submitting/unknown item first requires reconciliation; the wake's text explicitly prohibits retrying an unknown Create. The robot never edits queues or launches videos.
- Route decision is saved in `automation-monitor-status.json.notification_state.robot_dispatch` and CAS pushed/read back **before** external notification. `attempted_at` proves an attempt, not delivery or work. A failed CAS causes no wake.

## ACK contract

The genuine worker writes its exact business `event_id` in `reports/topview-event-wake.json.events[]`, under own lease/CAS/readback. Before long work: `outcome=started`, `retryable=true`, `execution.state=started`, `execution.stage=intake`, actual `execution.updated_at`. Update stage/time as real work advances. A test may use an explicitly read-only test event and must never create video/claim. Do not manufacture a worker receipt from an interactive coordinator. Runtime run ID is null if unavailable, never invented.

## Acceptance and rollback

Before enable: verify primary bot delivery into the current dot and its genuine early ACK; test primary-no-assignment, no-ACK backup, fresh ACK suppression, held lease suppression, backup-no-primary-DM and rejected-CAS-no-send without Topview. Confirm Grok still receives the unchanged issue-assigned backup. Record evidence, then flip only `dispatch.enabled=true` under own canon lease/CAS. Rollback is `false`: restores legacy simultaneous issue-assigned + primary DM, preserving the backup and queue safeguards.

Do not disable the hourly insurance until primary and backup runtime behavior is proven. No paid generation is part of acceptance.
