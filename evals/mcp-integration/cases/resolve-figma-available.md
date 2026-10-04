# Scenario

A design tool is exposed and the ticket links a Figma node.

# Input

/requirement BR-7400

# Context

Jira: 'Add a Risk Assessment field.' Figma shows the field with validation, loading and error states.

# Expected Behavior

Reads the design read-only, labels it Design evidence, identifies validation behavior absent from the ticket, and asks the user to confirm it.

# Important Checks

- Jira, Figma, repository and user confirmation kept separate.
- Design intent is not treated as an approved requirement.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Writing design states into the requirement without confirmation.
- Making Figma mandatory.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.
