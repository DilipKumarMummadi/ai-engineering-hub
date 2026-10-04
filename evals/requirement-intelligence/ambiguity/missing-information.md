# Scenario

A thin ticket that leaves out information the work depends on.

# Input

/requirement BR-7415

# Context

The requirements-tracking MCP returns BR-7415:

- Title: Risk register export
- Description: Add an export for the risk register.
- Acceptance criteria: none.
- Comments: none.

The repository has a Risks API, a list endpoint with filters and a shared CSV helper. It has no export endpoint. Project Context describes the API layering but says nothing about exports.

# Expected Behavior

The agent reports that the requirement is thin. Confirmed: a risk register exists and lists with filters. Missing: format, columns, who may export, whether filters apply, volume, delivery mode, acceptance criteria. Unknown: whether consumers besides the UI exist. Open questions are classified. BLOCKING: "Who may export, and does the export include confidential risks?" (decides security and data exposure). IMPORTANT: "Maximum number of rows?" and "Which format: CSV, XLSX or both?" (work could start with a stated default). OPTIONAL: "File name pattern?". Readiness is NEEDS_CLARIFICATION. Confidence is LOW because most of the behavior would be inferred from a title. The agent recommends refining the ticket.

# Important Checks

- Missing items are listed as Missing, not silently assumed.
- Each question has a class and BLOCKING has a stated reason.
- Confidence LOW is justified by thin explicitness, in words.
- Repository evidence is used to show what already exists without implying it decides the requirement.
- No format, column list or limit is presented as Confirmed.
- The result points to `/requirement BR-7415 refine` as a next step.

# Failure Conditions

- Writing a full requirement and presenting it as what the ticket says.
- Marking every question BLOCKING, or none.
- Reporting READY because the repository has a CSV helper.
- Numeric scores or percentages.

# Notes

Written but not yet run. Thin-ticket baseline.
