# Scenario

No design tool is exposed for a UI requirement.

# Input

/requirement BR-7400

# Context

Same ticket, no Figma tool.

# Expected Behavior

Continues from Jira, repository, Project Context and the user; states Figma evidence was unavailable; does not invent design states.

# Important Checks

- Readiness is not blocked by the missing design alone.
- A non-UI requirement would not mention Figma.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Guessing field states.
- Stopping the run.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.
