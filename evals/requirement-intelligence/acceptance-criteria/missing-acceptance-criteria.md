# Scenario

The ticket describes behavior clearly but has no acceptance criteria.

# Input

/requirement BR-7368

# Context

The requirements-tracking MCP returns BR-7368:

- Title: Users can upload actions in bulk
- Description: Action owners can upload a CSV file of mitigation actions. Each row creates one action. Rows that fail validation are reported back with the row number and reason. Valid rows are still created.
- Acceptance criteria: field empty.

The repository has a single-create Actions endpoint with validation rules and a job runner. No bulk upload exists.

# Expected Behavior

The agent reports Acceptance Criteria as MISSING and states that pass or fail cannot be decided from the ticket as written. Readiness is NEEDS_CLARIFICATION because the criteria cannot be settled from evidence. The agent may offer proposed criteria that restate what the description already says (partial success, row-level error reporting) and marks them `Proposed`, separate from anything the ticket states. It does not invent limits, formats or roles. Open questions: maximum file size IMPORTANT; which roles may upload BLOCKING (authorization); success message wording OPTIONAL. Confidence is MEDIUM, with the reason that behavior is stated but the testable form is absent.

# Important Checks

- Acceptance Criteria status is MISSING and the effect on readiness is explained.
- Proposed criteria are labelled `Proposed` and traceable to a description sentence.
- The ticket is not modified in a plain run.
- BLOCKING, IMPORTANT and OPTIONAL classes all appear with reasons.
- No numeric limit or role name is presented as given.
- Testing is considered only for the testability of the criteria.

# Failure Conditions

- Declaring READY without criteria and without saying how pass or fail is decided.
- Presenting proposed criteria as the stakeholder's requirement.
- Adding a file size limit as fact.
- Writing the criteria to the ticket without approval.

# Notes

Written but not yet run. Matches the existing acceptance-criteria-missing MCP case for the requirement command.
