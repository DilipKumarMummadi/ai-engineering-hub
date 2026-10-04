# Scenario

A ticket with a clear objective and some behavior but gaps in failure handling and acceptance criteria. The agent resolves what the ticket states and asks only about the gap that matters most.

# Input

```
User: /requirement BR-7415
```

# Context

The requirements-tracking MCP returns BR-7415 (fictional):

- Title: Export risk actions to CSV
- Description: Risk managers can export the filtered list of actions to CSV from the actions page. Columns are the ones shown in the grid. Only users with the Reporting role can export.
- Acceptance criteria: none

Not stated: maximum rows, what happens on an empty result, file naming, whether the export is synchronous or background. The repository has an existing background export job for the risk register.

# Expected Behavior

Turn 1 (agent): FEATURE (Inferred). Objective, Scope, Columns and Authorization are CLEAR with RESOLVED_FROM_JIRA. Large exports is MISSING and BLOCKING (synchronous versus background changes the design). Empty result is PARTIAL and IMPORTANT. Acceptance criteria is MISSING and IMPORTANT. File naming is OPTIONAL. The existing export job is noted as evidence that makes the checkpoint relevant, not as an answer.

Next question: one BLOCKING question on how large exports are delivered, with options (immediate download, background with notification, limit with an error, Other). Readiness NEEDS_CLARIFICATION because one BLOCKING checkpoint is open. Confidence MEDIUM because the core behavior is stated but delivery is not.

# Important Checks

- Items already stated are not asked.
- Only the BLOCKING gap is asked first; IMPORTANT items wait.
- Repository evidence is cited but not treated as confirmation.
- The acceptance criteria gap is reported, not silently filled.
- Vocabulary is fixed: no numbers, no percentages.

# Failure Conditions

- Re-asking the role or columns.
- Asking the file-naming question first.
- Treating the background job as the chosen design.
- READY while a BLOCKING checkpoint is open.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
