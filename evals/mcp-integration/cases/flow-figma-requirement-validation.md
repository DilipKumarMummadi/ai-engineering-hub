# Scenario

Design compared with the ticket.

# Input

/requirement BR-7400

# Context

Figma shows an error state and a loading state absent from Jira.

# Expected Behavior

Lists the design-only states as gaps, labels them Design evidence, and asks the user whether they are in scope.

# Important Checks

- Each gap is a question, not a requirement.
- Conflicts between Jira and Figma surfaced.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Silently adding states.
- Resolving a conflict without the user.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.
