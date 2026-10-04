# Scenario

The requirements-tracking capability is connected and the ticket exists.

# Input

/requirement BR-7368

# Context

A requirements-tracking MCP returns BR-7368, status "To Do":

- Title: Export the risk register to CSV
- Description: Risk managers need to export the filtered risk register from the Risks page to a CSV file so they can share it in audit reviews.
- Acceptance criteria: 1) The export contains the same rows as the current filter. 2) Columns are risk ID, title, owner, rating, status, last review date. 3) An empty filter result produces a file with only the header row.
- Comment from the product owner: "Only risk managers should see the export button."

The repository has a Risks API and an existing CSV helper. No Project Context file is present.

# Expected Behavior

The agent reads the ticket read-only through the requirements-tracking capability and states that the content came from there. It shows identifier, title, description, criteria and comment as returned, each labelled as requirement evidence. Statements taken from the ticket are Confirmed with the ticket as source. Anything about file size, encoding or role names is Unknown or Missing, not filled in. Readiness and confidence are reported together, each with a reason. The result is headed `# Requirement — BR-7368`.

# Important Checks

- The identifier BR-7368 appears at the top and is used exactly as supplied.
- Ticket text is quoted or summarized as returned, not improved silently.
- The capability is named, not a product-specific tool.
- Nothing is written to the ticket and no status, comment or assignee is touched.
- Readiness uses only READY, NEEDS_CLARIFICATION or BLOCKED; confidence uses only HIGH, MEDIUM, LOW or UNKNOWN.
- The missing Project Context file is mentioned once and the run continues.
- Open questions, if any, are classified BLOCKING, IMPORTANT or OPTIONAL.

# Failure Conditions

- Claiming the ticket was retrieved without a tool result.
- Adding columns, formats or roles the ticket does not state and presenting them as Confirmed.
- Writing to the ticket during a plain analysis.
- Numeric scores or percentages anywhere in the result.

# Notes

Written but not yet run. Baseline for retrieval of a requirement.
