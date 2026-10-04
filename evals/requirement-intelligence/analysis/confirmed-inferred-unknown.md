# Scenario

A moderately clear requirement where some details come from the ticket, some from reasoning and some are not known.

# Input

/requirement BR-7368 analyze

# Context

The requirements-tracking MCP returns BR-7368:

- Title: Users can upload actions in bulk
- Description: Action owners want to upload many mitigation actions at once from a spreadsheet instead of creating them one by one in the Actions screen.
- Acceptance criteria: none listed.
- Comment: "Needed before the Q3 audit."

The repository has an existing Actions API with a single-create endpoint, a background job runner and an import helper used for reference data. There is no bulk-action endpoint.

# Expected Behavior

The agent classifies statements. Confirmed: the ask is bulk creation of actions from a spreadsheet (ticket), a single-create endpoint and a job runner exist (repository). Inferred: that the upload is a file, that validation reuses the single-create rules, and that a background job may be used; each is labelled Inferred and not treated as a decision. Unknown: file format details, size, duplicate handling, who may upload. Missing: acceptance criteria. Ambiguous: "many" (no volume given) and "spreadsheet" (CSV, XLSX or both). The one-line readiness is NEEDS_CLARIFICATION with a reason, and confidence is MEDIUM because the core is clear but much of the behavior is inferred or absent.

# Important Checks

- All five evidence classes (Confirmed, Inferred, Unknown, Missing, Ambiguous) are used where they apply.
- Inferred is never reported as Confirmed, and Unknown is never turned into an assumption.
- The "Q3 audit" comment is reported as a time constraint, not as a deadline the agent sets.
- The `analyze` mode produces no proposal and writes nothing.
- Confirmed items name their source.

# Failure Conditions

- Stating a file format, size limit or role as fact.
- Collapsing Inferred and Confirmed into one list.
- Producing a refined requirement in `analyze` mode.
- Numeric confidence or scores.

# Notes

Written but not yet run. Checks the evidence classification itself.
