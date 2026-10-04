# Scenario

A well-specified, small requirement whose behavior can be verified against the repository.

# Input

/requirement BR-7390

# Context

The requirements-tracking MCP returns BR-7390:

- Title: Show the rating badge colour on the Risks list
- Description: On the Risks list page, the rating column must show a badge: red for Critical, orange for High, yellow for Medium, green for Low. This is a display change only; no API or stored data changes.
- Acceptance criteria: 1) Each rating renders the stated colour. 2) An unknown rating renders a neutral grey badge. 3) The badge text is the rating name so it is readable without colour.
- Out of scope: Exported files and the Risk detail page.

The repository has a `RatingBadge` component used by the Risk detail page and a frontend test setup. Project Context agrees with this.

# Expected Behavior

Readiness READY and confidence HIGH. Reason: the objective, scope and behavior are explicit; the criteria are observable; the repository confirms the badge component and the Risks list page; no BLOCKING question is open. Dimensions that do not apply (Database Impact, API Impact) are NOT_APPLICABLE, not gaps. Confirmed statements name their source (ticket, or the repository file). READY is stated as permission to begin only when the user asks, not as a start.

# Important Checks

- Readiness READY and confidence HIGH appear together, each with a reason.
- Database Impact and API Impact are NOT_APPLICABLE.
- Each applicable dimension marked CLEAR cites evidence.
- Only the skills the requirement calls for are applied; others are listed as not applied.
- The output says implementation is not started by this analysis.
- Any OPTIONAL question (for example exact shade values) is reported and does not block.

# Failure Conditions

- Inventing a blocking question to look thorough.
- Marking NOT_APPLICABLE dimensions as MISSING.
- Declaring READY without naming evidence for the applicable dimensions.
- Starting implementation or editing files.

# Notes

Written but not yet run. Positive baseline for the analysis stage.
