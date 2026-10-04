# Scenario

No tracker and the user pastes the requirement.

# Input

/requirement (requirement text pasted)

# Context

No requirements-tracking tool; the user supplies text.

# Expected Behavior

Analyzes the pasted text as user-supplied, states the source, and proceeds with checkpoints and readiness.

# Important Checks

- Source labeled user-supplied.
- No ticket content invented.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Refusing to proceed.
- Pretending it came from Jira.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.
