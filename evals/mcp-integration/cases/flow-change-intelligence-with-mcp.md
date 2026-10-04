# Scenario

Change Intelligence uses the PR and requirement.

# Input

/change-impact PR 42

# Context

GitHub tool returns the diff; Jira tool returns the ticket.

# Expected Behavior

Reports direct and indirect impact from the returned diff and repository, and relates it to the requirement without judging correctness.

# Important Checks

- Evidence classes kept apart.
- Unknowns listed.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Review verdicts.
- Impact claims not grounded in the diff.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.
