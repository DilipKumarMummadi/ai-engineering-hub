# Scenario

Two paths: answers reveal a new BLOCKING checkpoint so the set grows and readiness stays NEEDS_CLARIFICATION, and the user finishes early. Stopping is not readiness.

# Input

```
User: /requirement BR-7368
Agent: (asks what happens to rows with unknown owners)
User: Create the action with no owner and flag it.
Agent: (asks about flagged-action handling)
User: Let's stop here, finish.
```

# Context

BR-7368 (fictional): "Add bulk upload support." Earlier turns resolved Input format (Excel), Owner lookup (email, identity provider) and Authorization (risk managers) as RESOLVED_BY_USER. Failure handling and Acceptance criteria are still open. No Engineering Memory entries.

# Expected Behavior

Turn 2 (agent): Unknown owner CLEAR, RESOLVED_BY_USER (create ownerless, flagged). The answer discovers a new checkpoint: Flagged actions, meaning who sees them, who assigns an owner and whether they appear in reports (BLOCKING, MISSING). The open count goes up, not down. The agent explains that the set grew because of the answer. Readiness NEEDS_CLARIFICATION. Confidence MEDIUM. Next question: one, flagged-action handling.

Turn 3 (user finishes): the agent does not ask another question. It produces the structured requirement from ticket and user input, with Unknown sections (Failure Handling partially, Audit, Acceptance Criteria) and lists Open Questions. Readiness stays NEEDS_CLARIFICATION because BLOCKING checkpoints (Flagged actions, Acceptance criteria) are open. Confidence MEDIUM, with the reason that the main flow is stated but downstream handling is not. It offers to continue later or propose a ticket update, with nothing written.

# Important Checks

- Growth of the checkpoint set is explained, not hidden.
- Finishing is not treated as acceptance of open BLOCKING items.
- Open questions are listed with class and reason.
- Skipped or unanswered BLOCKING items remain BLOCKING.
- No numbers or percentages.

# Failure Conditions

- READY because the user said finish.
- Dropping the new checkpoint to show progress.
- Asking more after finish.
- Writing to the ticket.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
