# Site alerts: staged acceptance, not activation

The V2 route is disabled. This document and the manual canary do not install an automation handler, enable routing, or authorize merge.

## Before merge

Run `python -m unittest discover -s tests -p 'test_site_alert*.py'` and the full suite. Canary tests inject a fake transport: they prove recipient selection, fail-closed input/config checks, stable retry text and absence of repository writes. They do **not** prove Relay delivery or agent execution.

Review the existing Relay automation's exact current saved prompt/version. Prepend a separate SITE_ALERT_V2 branch with terminal return before the existing slot handler. Preserve the slot branch unchanged. Required checks: fetch complete authenticated Relay event; respect its reply/notes settings; validate sender, primary role, exact current canonical incident and explicit V2 enablement. A valid production event writes genuine ACK/progress only under its own exact lease, CAS and readback, never slot receipts. No fabricated run ID or heartbeat; duplicate message IDs do not renew progress. A site event, including a rejected one, never falls through to Topview.

Add a separate SITE_ALERT_V2_TEST branch. Its allowed test-ID list starts empty. For an explicitly authorized exact ID, return actual event/message IDs, UTC time, run ID if exposed and freshly read main SHA in the original chat. No production ACK, lease, repository mutation or Topview call. The coordinator must install/review this saved-prompt change separately. No automation is changed by this PR.

## After separately approved merge, before activation

1. Keep `site_alert_routing.enabled=false`; legacy Grok delivery remains active.
2. Explicitly authorize one exact canary test ID and recipient; add the ID to the receiving handler's saved allowlist. For Grok, verify its independent receiving instructions before sending; Dot's handler does not configure Grok.
3. Manually dispatch **Site alert read-only canary** from main, with the authorized ID/recipient and `confirm_read_only=true`. Branch runs are blocked; default confirmation is false. The workflow has contents-read only, no schedule or push trigger, and calls only the existing Relay sender. Its robot credential stays in the GitHub secret.
4. Correlate the transport message ID with the actual received event and the receiving agent's canary reply. Sender success alone is not delivery/execution evidence. Repeating the same ID/recipient gives the same transport idempotency key. A second recipient or new test requires its own explicit authorization.
5. Remove the canary allowlist entry when done. Do not write a production site/slot ACK as acceptance evidence. Record actual outcomes and unresolved limits.

## Production acceptance and rollback

Only a separate explicit enablement decision may set the V2 flag true. Check an actual incident: real primary delivery, genuine exact-incident early ACK and progress, own-lease/CAS/readback, actual resolution. Verify the backup recipient independently. Local clock fixtures verify 30/120-minute logic; direct backup canary verifies transport only. Neither proves the production no-progress timer has delivered a backup. Do not invent failure, withhold a needed repair or manufacture ACKs merely to make a test pass.

Rollback sets only the V2 flag false, retaining legacy site_alert_enabled and Grok address. A schema-2 to schema-1 transition is tested and may send one current-set legacy notification. Queue/slot 20/30-minute routing and hourly insurance are unchanged.
