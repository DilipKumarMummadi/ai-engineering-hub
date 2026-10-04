# Scenario

A UI requirement is refined for states, accessibility and behavior, and asks nothing about data or APIs that do not apply.

# Input

Turn 1 (user): `/requirement BR-9107`
Turn 2 (user): `Mark the API and database checkpoints not applicable, the data already exists.`

# Context

BR-9107 (fictional) reads:

- Title: Add a severity filter to the risk list
- Description: "Users can filter the risk list by severity."
- Acceptance criteria: 1) Choosing a severity shows only matching risks.

The repository shows that the list endpoint already accepts a severity parameter. The frontend has shared filter components.

# Expected Behavior

Turn 1: type UI_CHANGE (Inferred). Checkpoints: Filter behavior (CLEAR, RESOLVED_FROM_JIRA, criterion 1), Multiple selection (IMPORTANT, MISSING), Empty result state (IMPORTANT, MISSING), Loading and error states (OPTIONAL, MISSING), Accessibility and keyboard use (IMPORTANT, UNKNOWN), Persistence of the filter on reload (OPTIONAL, UNKNOWN), API support (CLEAR, evidence: existing parameter, Inferred for behavior). No BLOCKING checkpoint. Readiness READY, confidence MEDIUM because several IMPORTANT items are unsettled. Open questions are listed with classes; the first is multiple selection.

Turn 2: the user's not-applicable call on database is recorded as the user's decision (NOT_APPLICABLE). The API checkpoint is not dropped silently because the repository shows an existing parameter; the agent notes it as relevant evidence and keeps it CLEAR rather than NOT_APPLICABLE. Readiness READY, confidence MEDIUM.

# Important Checks

- Only BLOCKING items prevent READY, and none exists.
- User decisions are recorded as such and challenged only when evidence contradicts.
- Accessibility is raised without being blocking.
- Design, mockups and code are not produced.

# Failure Conditions

- NEEDS_CLARIFICATION caused by IMPORTANT or OPTIONAL items alone.
- Asking database or migration questions.
- Ignoring the existing API parameter evidence.
- Numeric scores.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.
