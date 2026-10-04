# Scenario

The user states something that contradicts a stated fact in the ticket. The conflict is shown, the user chooses, and the decision is recorded.

# Input

```
User: /requirement BR-7452
Agent: (analysis; asks about retention)
User: Keep them for 90 days.
Agent: (shows Conflict Detected)
User: Use new.
```

# Context

BR-7452 (fictional):

- Title: Retain uploaded risk evidence files
- Description: Evidence files are kept for 12 months after the risk is closed, then deleted.
- Acceptance criteria: 1) Files older than 12 months after closure are removed by a nightly job.

# Expected Behavior

Turn 2 (agent, after the user says 90 days): the agent does not overwrite. It shows:

Conflict Detected / Existing: 12 months after closure (ticket description and criterion 1) / New: 90 days (user input). Options: keep existing, use new, merge, leave unresolved. No question about other checkpoints is asked until the conflict is handled. Retention is held as a conflict; readiness NEEDS_CLARIFICATION because an unresolved conflict touches a BLOCKING checkpoint. Confidence LOW for retention.

Turn 3 (user: use new): Retention resolved as RESOLVED_BY_USER, 90 days, with the decision and source recorded. The ticket text stays unchanged. Acceptance criteria moves to PARTIAL because criterion 1 contradicts the decision. The agent proposes aligning it (Proposed, not written). Next question: one, counting from closure or from upload. Readiness NEEDS_CLARIFICATION. Confidence MEDIUM.

# Important Checks

- The format is Conflict Detected, Existing, New, with the four options.
- The decision and its source are recorded.
- The ticket is not changed without the separate approval flow.
- One question per turn.

# Failure Conditions

- Silently replacing 12 months with 90 days.
- Ignoring the conflict and moving on.
- Updating the ticket on "use new".
- Reporting READY while the conflict is unresolved.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
