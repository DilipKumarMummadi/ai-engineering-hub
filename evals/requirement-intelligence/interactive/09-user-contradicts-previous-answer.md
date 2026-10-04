# Scenario

A later user message contradicts an earlier user answer. The agent surfaces it as a conflict instead of taking the latest message as truth.

# Input

```
User: /requirement BR-7368
Agent: (asks what happens with invalid rows)
User: Reject the whole upload if any row is invalid.
Agent: (asks about duplicates)
User: Just save the valid rows and report the rest, and skip duplicates.
```

# Context

BR-7368 (fictional): "Add bulk upload support." No acceptance criteria. No Engineering Memory entries.

# Expected Behavior

Turn 2 (user: reject the whole upload): Failure handling CLEAR, RESOLVED_BY_USER (all-or-nothing). New checkpoint: Duplicates (BLOCKING). Next question: duplicates.

Turn 3 (agent): the user's new message would make Failure handling partial-success, which contradicts the earlier answer. The agent shows:

Conflict Detected / Existing: reject the whole upload if any row is invalid (user input, turn 2) / New: save valid rows and report the rest (user input, turn 3). Options: keep existing, use new, merge, leave unresolved. The duplicate answer (skip duplicates) is recorded as RESOLVED_BY_USER because it does not depend on the conflict. The conflict is the single next question.

Readiness NEEDS_CLARIFICATION because Failure handling is BLOCKING and in conflict. Confidence MEDIUM, reduced by the unresolved conflict.

# Important Checks

- Non-conflicting content from the same message is still used.
- The earlier answer is not silently replaced.
- The conflict names both sources and turns.
- The conflict is the only question.
- No numeric scores.

# Failure Conditions

- Taking the latest message as the answer without asking.
- Discarding the duplicate answer along with the conflicting one.
- Asking an unrelated question beside the conflict.
- Marking Failure handling CLEAR while in conflict.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
