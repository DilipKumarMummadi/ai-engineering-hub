# Scenario

The requirement ID is carried from the readiness result through the workflow outputs, with no copy of the ticket stored anywhere.

# Input

```
/feature BR-7368
```

# Context

The requirements-tracking MCP returns BR-7368 (fictional): "Approval workflow for the risk register export", READY on first check with testable criteria. The repository has an approval status and an export service. Project Context is current. The user confirms the plan when PLAN READY is shown.

# Expected Behavior

The requirement analysis is headed `Requirement — BR-7368` and states when it was retrieved. Later outputs cite BR-7368: the plan names the requirement or criterion each change serves, the test plan maps tests to the acceptance criteria, the change-intelligence intent line names it, the review states what it reviewed against, and the final report lists the requirement, the readiness at the start and the criteria covered.

A criterion with no identified test is reported as such, for example "Criterion 3 has no identified test". The workflow does not create a requirement database or paste the full ticket into repository files. The tracker remains the source of truth.

# Important Checks

- BR-7368 appears consistently and is never altered or guessed.
- The plan and the test plan reference acceptance criteria by number or name.
- Missing links are stated as missing.
- No file containing the full ticket text is created.
- If the ticket changes during the work, the change is reported and readiness is assessed again.

# Failure Conditions

- Losing the ID between stages.
- Creating a copy or database of the ticket.
- Claiming coverage of a criterion with no evidence.
- Silently following a changed ticket.

# Notes

Written but not yet run. Traceability without a separate store.
