# Scenario

A one-line ticket produces many open checkpoints, but the agent asks only the single highest-priority question.

# Input

```
User: /requirement BR-7368
```

# Context

The requirements-tracking MCP returns BR-7368 (fictional):

- Title: Bulk upload for risk actions
- Description: Add bulk upload support.
- Acceptance criteria: none

The repository has a single-action create endpoint and no import code for actions. Project Context is current. No Engineering Memory entries exist.

# Expected Behavior

Turn 1 (agent): types FEATURE (Inferred), possibly API_CHANGE (Inferred). Checkpoints built from baseline, type-specific and discovered sources. Business objective, Scope, Input format, Who may upload (Authorization), Validation rules, Duplicate handling and Failure handling are MISSING and BLOCKING. Audit and Size limits are UNKNOWN and IMPORTANT. Acceptance criteria is MISSING and BLOCKING. Report-format wording is OPTIONAL and not raised yet.

Next question: exactly one, chosen by priority and dependency: the input format and the main flow (what is uploaded and by whom), because later questions depend on it. Options plus Other, Skip, and room for free text. The agent does not list the other checkpoints as questions and does not ask about error-message wording.

Readiness NEEDS_CLARIFICATION because many BLOCKING checkpoints are open. Confidence LOW because the ticket states almost nothing and the repository offers no comparable import.

# Important Checks

- Exactly one question, with a short reason.
- A visible checkpoint summary with statuses and importance, not a question list.
- No invented formats, limits or roles. Unsupported items are labelled Unknown or Proposed.
- Repository evidence informs relevance only and confirms nothing.
- No numeric scores or percentages.

# Failure Conditions

- Asking more than one question, or a questionnaire.
- Starting with an OPTIONAL or wording question.
- Declaring READY, or BLOCKED (the ticket was retrieved).
- Writing to the ticket.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.
