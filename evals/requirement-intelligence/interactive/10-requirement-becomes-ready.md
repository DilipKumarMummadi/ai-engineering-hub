# Scenario

After the last BLOCKING checkpoint is resolved and remaining items are stated or accepted, readiness moves to READY. The agent still does not start implementation.

# Input

```
User: /requirement BR-7415
Agent: (asks the last BLOCKING question: large exports)
User: Background job, the user gets an in-app notification with a download link.
Agent: (reports; offers to finalize)
User: Empty result: show a message, no file. File name is fine as default. Yes, finalize.
```

# Context

BR-7415 (fictional): "Risk managers can export the filtered list of actions to CSV. Only the Reporting role can export." Earlier turns resolved Columns and Authorization from Jira. The repository has a background export job and an in-app notification helper.

# Expected Behavior

Turn 2 (agent): Large exports moves MISSING to CLEAR, RESOLVED_BY_USER. New checkpoint: Notification content (IMPORTANT, INFERRED from the helper, REQUIRES_CONFIRMATION). The last BLOCKING item is closed. Next question: one, the empty-result behavior.

Turn 3 (agent): Empty result CLEAR, RESOLVED_BY_USER. File name: user accepts the default, CONFIRMED_BY_USER (OPTIONAL). Notification content CONFIRMED_BY_USER by implication only if the user says so; otherwise it is listed as an accepted assumption only when the user explicitly accepts it. Acceptance criteria are drafted (Proposed) from the stated behavior and the user confirms by finalizing.

Readiness READY: no BLOCKING open, no unresolved conflict, behavior and criteria are testable, and open IMPORTANT items are resolved or explicitly accepted. Confidence HIGH or MEDIUM with the reason. The finalized requirement is shown with Objective, Scope, Actors, Processing, Failure Handling, Security, Acceptance Criteria, Out of Scope, Open Questions. The agent waits for the user before any next stage and does not write to the ticket.

# Important Checks

- READY depends on the gate, not on the user saying finalize.
- Accepted assumptions are listed as accepted by the user.
- No implementation, no ticket write.
- Sections with nothing supplied say Unknown.

# Failure Conditions

- Starting implementation or design.
- Writing the ticket without the approval flow.
- Marking INFERRED items CLEAR without the user.
- Numeric scores.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
