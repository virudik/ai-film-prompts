# Site alerts: staged acceptance, not activation

Status: in force. Checked: 23.11.2026.

The V2 route is disabled. This document and the manual canary do not install an automation handler, enable routing, or authorize merge.

## Before merge

Run `python -m unittest discover -s tests -p 'test_site_alert*.py'` and the full suite. Canary tests inject a fake transport: they prove recipient selection, fail-closed input/config checks, stable retry text and absence of repository writes. They do **not** prove Relay delivery or agent execution.

Review the existing Relay automation's exact current saved prompt/version. Prepend a separate SITE_ALERT_V2 branch with terminal return before the existing slot handler. Preserve the slot branch unchanged. Required checks: fetch complete authenticated Relay event; respect its reply/notes settings; validate sender, recipient_actor and its current configured role, exact current canonical incident and explicit V2 enablement. A valid production event writes genuine ACK/progress only under its own exact lease, CAS and readback, never slot receipts. No fabricated run ID or heartbeat; duplicate message IDs do not renew progress. A site event, including a rejected one, never falls through to Topview.

Add a separate SITE_ALERT_V2_TEST branch. Its allowed test-ID list starts empty. For an explicitly authorized exact ID, return actual event/message IDs, UTC time, run ID if exposed and freshly read main SHA in the original chat. No production ACK, lease, repository mutation or Topview call. The coordinator must install/review this saved-prompt change separately. No automation is changed by this PR.

## After separately approved merge, before activation

1. Keep `site_alert_routing.enabled=false`; legacy Grok delivery remains active.
2. Explicitly authorize one exact canary test ID and recipient; add the ID to the receiving handler's saved allowlist. For Grok, verify its independent receiving instructions before sending; Dot's handler does not configure Grok.
3. Manually dispatch **Site alert read-only canary** from main, with the authorized ID/recipient and `confirm_read_only=true`. Branch runs are blocked; default confirmation is false. The workflow has contents-read only, no schedule or push trigger, and calls only the existing Relay sender. Its robot credential stays in the GitHub secret.
4. Correlate the transport message ID with the actual received event and the receiving agent's canary reply. Sender success alone is not delivery/execution evidence. Repeating the same ID/recipient gives the same transport idempotency key. A second recipient or new test requires its own explicit authorization.
5. Remove the canary allowlist entry when done. Do not write a production site/slot ACK as acceptance evidence. Record actual outcomes and unresolved limits.

## Production acceptance and rollback

Only a separate explicit enablement decision may set the V2 flag true. Check an actual incident: real primary delivery, genuine exact-incident early ACK and progress, own-lease/CAS/readback, actual resolution. Verify the backup recipient independently. Local clock fixtures verify 120-minute site logic and configurable thresholds; direct backup canary verifies transport only. Neither proves the production no-progress timer has delivered a backup. Do not invent failure, withhold a needed repair or manufacture ACKs merely to make a test pass.

Rollback sets only the V2 flag false, retaining legacy site_alert_enabled and Grok address. A schema-2 to schema-1 transition is tested and may send one current-set legacy notification. Queue/slot 20/30-minute routing and hourly insurance are unchanged.


## Publication ordering and roles (PR completion)

Production sender uses `site_alert_publish.sh`: publish prepared incident/target/
recipient/occurrence-set/timeout with CAS, fetch/read back main, then notify, then
publish the transport result. `--notify` refuses an unprepared V2 decision.
Interrupted receipt pushes recompute from main; unchanged payload has the same
Relay key. Exhausted CAS and failed fetch/reset are visible failures. Rollback
retains the sequence so re-enabling cannot reuse an old incident/key.

A separate shared `wake_roles` pair controls site V2 and video routing. It is not
installed by default. Test both orders before activating it; verify each actual
receiver's role and actor-qualified ACK, not just delivery. The site addresses
remain actor-specific despite their historical primary_address/backup_address
names. Canary names a recipient actor, resolves its configured role, and remains
read-only. Site threshold is 120 minutes for all severities; video remains 20/30.

Merging this disabled draft alone does not install receiving prompts, enable V2,
or reverse production roles. Those steps remain separate acceptance gates.


`site_alert_receiver.validate` is the side-effect-free receiving gate shared by
both actors: pass the complete message, actor, authenticated sender ID from Relay,
explicit test allowlist and current time. It rejects wrong sender/role/incident,
changed or resolved problems, old occurrence tokens and duplicate fields.
Never copy a sender ID claimed inside text into authenticated_sender_id.
Even accepted production events have write_allowed=false: lease, CAS, dedup by
actual message ID and genuine progress must still be handled by the receiving
agent. The prepared-canonical-state test invokes this gate inside fake transport
before the sender records its receipt, proving the intended ordering offline.
This is not evidence that a saved receiving automation has been installed.


Приёмная сторона (lease/CAS/readback ACK, TEST read-only): `ops/SITE-ALERT-V2-RECEIVER.md`, `scripts/site_alert_handler.py`.


## Read-only completion probe · 18.11.2026

Owner requested completion and testing, not production activation. The temporary canary-only `--test-address` option accepts exactly test ID `site-v2-grok-canary-20261118-completion`, actor `grok`, and address `GrokBotWake@cloud-248663208472330240`. It still requires explicit confirmation and literal `site_alert_routing.enabled=false`. The default configured-address behavior and all production/legacy addresses remain unchanged. Workflow inputs are quoted through environment variables and a Bash array; permissions remain contents-read, manual main-only.

Before dispatch, verify the receiving routine has accepted this exact temporary ID. A peer's pending approval is not readiness; do not send until the receiver confirms. After the probe, remove the temporary sender allowlist entry and receiver allowlist entry, preserving the evidence. Do not reuse the older 17.11 ID. Dot probe `site-v2-dot-canary-20261118-completion` was dispatched in workflow run 44353666056; transport message 248854986484445184 is not by itself receiving-handler acceptance. No production ACK or 120-minute fallback is claimed by these tests.


## Completion evidence and cleanup · 18.11.2026

The one-time sender override is now removed (`TEST_ONLY_TARGETS = {}`). Its former test-ID/address is rejected before transport; fixture-only override tests remain. Production `ops/relay-wake.json` is not modified: V2 remains disabled, legacy Grok route and Dot-primary/Grok-backup roles remain unchanged.

Grok probe was dispatched exactly once by workflow [44364451274](https://github.com/virudik/ai-film-prompts/actions/runs/44364451274), job 135014319636, from main `ea4a60a6dfadd651e2b75ab4d9dfd94fcedf91a9`. Sender log records test `site-v2-grok-canary-20261118-completion`, recipient `grok`, test-only address `GrokBotWake@cloud-248663208472330240`, and robot message `248869574308257792` at 17:58:51Z. No resend was made.

Authenticated GrokBot (sender agent ID 242545579433959424) replied at 18:08:13Z in message `248871935960629248`, event `evt_9c901270a5aeeefed03654234b0937da`. Full receipt reports that exact test/message, incoming event `evt_975c93e312b4c4c8bdf90704e1fb34f4`, role `backup`, received_at_utc `2026-11-18T18:07:24Z`, main `aa454de97a5aad4b68a957140f8421234f4649c4`, run_id null, read-only and no writes. This is correlated peer-reported receiving evidence, not independent access to his runtime. A follow-up to GrokBotWake (`248873275626844160`) requests the exact handler outcome, explanation of the ordinary GrokBot reply identity, and readback of receiver temporary-ID removal. Pending until a separate confirmation is recorded; sender cleanup does not certify receiver cleanup.

Dot probe message `248854986484445184`, actual event `evt_2de1eaf37d3ea1aba07e49d5bbec525e`: after an initial isolated-clone failure a diagnostic worker ran the handler on the delivered event, reporting `ok=true`, `outcome=test_received`, `terminal=true`, `writes=none`, `read_only=true`, received at 17:06:28Z, main `038ae859`, run_id null. Root reports its temporary receiver allowlist removed after the result. This establishes diagnostic handler acceptance, NOT independently demonstrated autonomous webhook execution.

Cleanup validation: 93 site-alert tests passed on refreshed main; diff whitespace check passed. No production ACK/lease/Topview action was created by either read-only probe. The editorial cleanup lease is not a production incident ACK. Neither probe establishes a real 120-minute fallback, incident resolution, or production readiness. Enabling V2 and changing the production backup address remain separate explicit owner decisions.


### Receiver closure confirmation · 18:21:11Z

Authenticated GrokBotWake (agent ID 248663208472330240) replied in message `248875199016677376`, event `evt_1b6ded84ff7c3fce74bd02c7ba2ca979`, thread `248873275626844160`. Full response confirms `test_received`, `ok=true`, `terminal=true`, no writes, main `aa454de9`. It reports a saved-routine readback with an empty test-ID allowlist, no `--allow-test-id` argument, and the one-time ID marked used. It explains the reply identity: incoming events use GrokBotWake/agent-relay-events, outgoing replies use GrokBot/agent-relay, both in the same routine. Thus the previously pending receiver closure is confirmed by the authenticated peer; it is still peer-reported readback, not independent inspection of his saved prompt. Sender cleanup was independently read back in `9f24190d9efb7e0e6f00b73a368be05426d908a8`. No production activation or role/legacy change is implied.
