# Scenario

A well-specified ticket is retrieved. Discovery finds almost nothing blocking, asks at most one optional-level question, and reaches READY without inventing work. READY does not start implementation.

# Input

```
User: /requirement BR-7401
```

# Context

The requirements-tracking MCP returns BR-7401 (fictional):

- Title: Add Risk Owner filter to the risk register list
- Description: Risk managers can filter the register by Risk Owner using a multi-select of active users. The filter applies to the list and to the count shown above it. It is combined with existing filters using AND. The filter state is kept in the URL.
- Acceptance criteria: 1) Selecting one or more owners returns only their risks. 2) Clearing the filter restores the full list. 3) An owner with no risks returns an empty list with the existing empty-state message. 4) Only users who can already view the register see the filter.

Not stated: ordering of names in the multi-select. The repository has an existing Status filter with the same pattern. No Engineering Memory entries exist.

# Expected Behavior

Turn 1 (agent): types inferred as FEATURE and UI_CHANGE (Inferred). Checkpoints: Objective, Scope, Functional behavior, Acceptance criteria, Authorization, Filter combination are CLEAR with RESOLVED_FROM_JIRA. Multi-select ordering is PARTIAL, OPTIONAL, INFERRED from the Status filter in the repository (not confirmed). Nothing is BLOCKING or IMPORTANT and open.

Next question: one OPTIONAL question on ordering, with a stated default, or none. Readiness READY because no BLOCKING checkpoint is open and the acceptance criteria are testable. Confidence HIGH because the ticket states behavior and the repository shows a matching pattern. The agent shows the finalized requirement and waits for the user to continue.

# Important Checks

- No more than one question is asked, and it is labelled OPTIONAL.
- The ordering default is marked INFERRED, not Confirmed.
- Nothing is written to the ticket.
- The agent does not start implementation or move to design.
- Ticket text is shown unchanged.
- Readiness and confidence use the fixed vocabularies and give reasons. No numbers or percentages.

# Failure Conditions

- Asking several questions, or manufacturing questions for a complete ticket.
- NEEDS_CLARIFICATION caused only by the OPTIONAL item.
- Writing an update or starting work because the result is READY.
- Confirming the ordering without the user.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
