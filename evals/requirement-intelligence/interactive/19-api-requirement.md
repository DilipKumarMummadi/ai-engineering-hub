# Scenario

An API requirement gets type-specific checkpoints, and the first question is the one with the highest blocking impact.

# Input

Turn 1 (user): `/requirement BR-9105`
Turn 2 (user): `Only risk managers may call it, and results are paginated.`

# Context

BR-9105 (fictional) reads:

- Title: Endpoint to list overdue risk actions
- Description: "Add an endpoint that returns overdue actions for a portfolio."
- Acceptance criteria: none.

The repository already has a versioned actions endpoint and a role check used by other endpoints. Project Context agrees. Consumers of the new endpoint are not stated.

# Expected Behavior

Turn 1: types FEATURE and API_CHANGE (Inferred). Checkpoints: Contract (request and response), Authorization (BLOCKING, MISSING), Validation, Pagination, Error responses, Compatibility and versioning, Definition of overdue (BLOCKING, MISSING), Acceptance criteria. Readiness NEEDS_CLARIFICATION, confidence LOW. The security-relevant blocking item comes first: who may call it. One question with options and Other.

Turn 2: one answer resolves Authorization (RESOLVED_BY_USER, BLOCKING cleared) and Pagination (PARTIAL: style and page size still open, IMPORTANT). The repository's existing role check is cited as Confirmed evidence of the mechanism; it does not confirm the rule for this endpoint beyond what the user said. Next question: definition of overdue. Readiness NEEDS_CLARIFICATION, confidence MEDIUM.

# Important Checks

- Authorization is asked before response-field detail.
- One answer resolves several checkpoints and none is re-asked.
- Repository evidence informs; the user's statement resolves.
- Consumers are flagged as unknown for compatibility, not invented.
- Allowed vocabulary only, no numbers.

# Failure Conditions

- Asking all API questions in one message.
- Designing the contract or writing code.
- Marking Compatibility CLEAR with no consumer information.
- READY while Definition of overdue is unresolved.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.
