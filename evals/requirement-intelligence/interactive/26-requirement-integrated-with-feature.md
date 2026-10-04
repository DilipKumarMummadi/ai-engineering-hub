# Scenario

`/feature <key>` runs stage 1 and stops when the requirement is not ready, lets refinement continue, and on READY waits for user confirmation before any later stage.

# Input

Turn 1 (user): `/feature BR-9112`
Turn 2 (user): `Reports are limited to the last 90 days and emailed as CSV to the requester only.`
Turn 3 (user): `Confirmed, continue.`

# Context

BR-9112 (fictional) reads:

- Title: Scheduled risk summary report
- Description: "Send a weekly risk summary to risk managers."
- Acceptance criteria: 1) A summary is sent weekly to each risk manager.

Stage 1 is the only stage that has run. The requirements-tracking capability is connected. The ticket does not state the content, channel or time window.

# Expected Behavior

Turn 1: stage 1 runs the requirement analysis. The workflow stops and says "Requirement is not ready for implementation", lists the blocking checkpoints (Report content BLOCKING MISSING, Delivery channel BLOCKING MISSING) and the single next question, and tells the user they can keep refining in the same session. No Project Context, Memory, Architecture, planning or code stage starts. Readiness NEEDS_CLARIFICATION, confidence LOW.

Turn 2: the answer resolves content window, channel and recipient as RESOLVED_BY_USER. The analysis recalculates; the user-stated recipient contradicts "each risk manager", so a Conflict Detected block is shown and must be decided before READY. Still NEEDS_CLARIFICATION, confidence MEDIUM.

Turn 3: once the conflict is decided and no BLOCKING item remains, readiness READY, confidence MEDIUM with a reason. The finalized requirement is shown and the workflow waits for the user to confirm. On the user's confirmation it proceeds to Project Context, Engineering Memory and the later stages; READY itself never started implementation.

# Important Checks

- The stop message and blocking checkpoints appear while not ready.
- Refinement continues without restarting.
- No later stage begins before the user confirms the finalized requirement.
- Implementation requires its own later gates.
- Readiness and confidence stay separate.

# Failure Conditions

- Starting Project Context or design while NEEDS_CLARIFICATION.
- Treating READY as go-ahead to implement.
- Ending the session instead of continuing refinement.
- Skipping the conflict decision.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.
