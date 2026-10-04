# Scenario

The user ignores the question and writes a long explanation. The agent resolves every checkpoint the text supports and does not re-ask any.

# Input

```
User: /requirement BR-7368
Agent: (asks about input format)
User: Let me explain. Risk managers upload an Excel file with one action per row:
title, owner email, due date, risk id. Emails are checked against the identity
provider. Only risk managers can upload. If some rows are bad, valid rows are
saved and the bad ones come back in a downloadable report. Max 5000 rows.
```

# Context

BR-7368 (fictional): "Add bulk upload support." No acceptance criteria. No Engineering Memory entries.

# Expected Behavior

Turn 2 (agent): the text is stored as user input beside the unchanged ticket. Checkpoints resolved as RESOLVED_BY_USER: Input format (Excel), Columns (title, owner email, due date, risk id), Owner lookup (identity provider), Authorization (risk managers), Failure handling (valid rows saved, invalid reported), Size limit (5000 rows). New checkpoints raised: Duplicate rows (BLOCKING), Report format and retention (IMPORTANT), Audit (IMPORTANT, UNKNOWN), Acceptance criteria (MISSING, IMPORTANT once behavior exists), Owner not found (covered by the invalid-row rule; recorded CLEAR, RESOLVED_BY_USER).

Next question: one, Duplicate rows. Readiness NEEDS_CLARIFICATION because Duplicate rows is BLOCKING. Confidence MEDIUM because the main flow and failure behavior are now stated by the user.

# Important Checks

- No answered checkpoint is asked again.
- The agent does not add anything the user did not say (no template, no retry rule).
- The report lists resolved checkpoints and the reason for the new ones.
- Exactly one next question. No numeric scores.

# Failure Conditions

- Re-asking the format, the role or the size limit.
- Asking a list of follow-ups.
- Marking Audit CLEAR without the user.
- Ignoring the free text and repeating the original question.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
