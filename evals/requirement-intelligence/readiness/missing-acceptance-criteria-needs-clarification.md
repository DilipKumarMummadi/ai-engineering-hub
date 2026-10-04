# Scenario

Readiness is assessed for a ticket whose missing criteria are the deciding gap.

# Input

/requirement BR-7368 readiness

# Context

The requirements-tracking MCP returns BR-7368:

- Title: Users can upload actions in bulk
- Description: Action owners upload a CSV of mitigation actions; each row creates an action; invalid rows are reported.
- Acceptance criteria: none.

The repository has the single-create endpoint, validation rules and a job runner. Project Context agrees. No upload roles are mentioned anywhere in the ticket.

# Expected Behavior

Overall NEEDS_CLARIFICATION. Confidence MEDIUM with the reason that the behavior is stated but the criteria are absent and the authorized roles are unknown. The table shows Business Objective CLEAR, Scope PARTIAL, Functional Behavior PARTIAL, Acceptance Criteria MISSING, Technical Context CLEAR, Security UNKNOWN, Database Impact PARTIAL, Testing PARTIAL. Blocking Questions names the role question with the reason that it decides authorization. The decision follows the gate order: an unresolved BLOCKING question, then a MISSING criteria dimension. Implementation Gate states that implementation should not begin until the blocking question is resolved and criteria are settled.

# Important Checks

- The gate outcome follows from a named BLOCKING question, not from a count.
- Acceptance Criteria is MISSING and is called out as a reason.
- Every status in the table comes from the allowed set (CLEAR, PARTIAL, MISSING, UNKNOWN, NOT_APPLICABLE).
- Recommendation names what to clarify and suggests `/requirement BR-7368 refine`.
- Confidence reason and readiness reason are separate statements.
- No numeric score is given.

# Failure Conditions

- Reporting READY because the description sounds clear.
- Calling the outcome BLOCKED (the ticket was readable; evidence was available).
- Inventing acceptance criteria inside the readiness report as if they were the ticket's.
- Omitting the Implementation Gate line.

# Notes

Written but not yet run. Checks the NEEDS_CLARIFICATION path and that BLOCKED is reserved for inability to assess.
