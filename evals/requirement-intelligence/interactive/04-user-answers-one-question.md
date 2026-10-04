# Scenario

The user answers the single question. Only the checkpoints the answer supports change, and the next question follows from it.

# Input

```
User: /requirement BR-7368
Agent: (analysis; asks about input format)
User: Excel. One row per action, uploaded by risk managers.
```

# Context

BR-7368 (fictional) reads "Add bulk upload support." with no acceptance criteria. The first agent turn asked for the input format and the main flow. No other input has been given.

# Expected Behavior

Turn 2 (agent): the user text is added to the workspace as user input and the ticket text stays unchanged beside it. The whole requirement is re-analyzed.

Changes: Input format moves MISSING to CLEAR, RESOLVED_BY_USER (Excel). Actors moves to CLEAR, RESOLVED_BY_USER (risk managers). Granularity (one row per action) is CLEAR. Authorization is still PARTIAL: who may upload is stated, enforcement is not. Nothing else is resolved; the agent does not add column lists, size limits or a template.

Next question: exactly one, the next dependent BLOCKING item, for example how each row identifies the action owner, or what happens when some rows are invalid. Readiness stays NEEDS_CLARIFICATION because BLOCKING checkpoints remain (validation, failure handling, acceptance criteria). Confidence moves from LOW to LOW or MEDIUM, with the reason given.

# Important Checks

- The report says what changed this cycle.
- The workspace version increases by one.
- "Excel" resolves the format and nothing beyond it.
- The next question is not one already answered.
- Exactly one question. No numeric scores.

# Failure Conditions

- Inferring .xlsx limits, a template or a sheet layout as Confirmed.
- Asking the format again.
- Asking two questions.
- Changing the ticket text.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
