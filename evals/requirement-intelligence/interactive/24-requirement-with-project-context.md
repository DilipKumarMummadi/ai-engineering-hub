# Scenario

Project Context makes a checkpoint relevant and informs it, but never confirms it. Only the user or the ticket confirms a value.

# Input

Turn 1 (user): `/requirement BR-9110`
Turn 2 (user): `Yes, send it through the existing notification service.`

# Context

BR-9110 (fictional) reads:

- Title: Alert owners when a risk score crosses a threshold
- Description: "Send the owner an alert when a risk score goes above the threshold."
- Acceptance criteria: none.

Project Context (current) describes a shared notification service used by other features and a scheduled job runner. It says nothing about thresholds or alert rules. Threshold value and recipients are not in the ticket.

# Expected Behavior

Turn 1: types FEATURE and INTEGRATION (Inferred). Project Context makes Delivery channel relevant and the agent proposes the notification service as a plausible value: Delivery channel PARTIAL, resolution REQUIRES_CONFIRMATION, source Project Context, class Inferred. It is not treated as decided. Other checkpoints: Threshold value (BLOCKING, MISSING), Recipients (BLOCKING, MISSING), Repeat alerts and deduplication (IMPORTANT, MISSING), Acceptance criteria (BLOCKING, MISSING). Readiness NEEDS_CLARIFICATION, confidence LOW. First question: the threshold value, as the blocking item; the channel confirmation is folded in or asked after.

Turn 2: the user confirms the channel. Delivery channel becomes CLEAR, CONFIRMED_BY_USER, source user input with Project Context as supporting evidence. Threshold and recipients remain BLOCKING and open. Readiness NEEDS_CLARIFICATION, confidence LOW.

# Important Checks

- Project Context is cited as the source of relevance and of the proposed value.
- The value stays REQUIRES_CONFIRMATION until the user confirms.
- Confirmation changes the resolution to CONFIRMED_BY_USER.
- Project Context does not lower any BLOCKING item.
- One question per turn.

# Failure Conditions

- Marking the channel CLEAR in turn 1 from Project Context alone.
- Inventing a threshold value from context.
- Using Project Context to raise confidence past what the ticket and user support.
- Asking about channel options Project Context rules out as if unknown.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.
