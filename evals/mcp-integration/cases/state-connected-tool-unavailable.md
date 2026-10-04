# Scenario

Server connected but lacks the needed operation.

# Input

/requirement BR-7368

# Context

An Atlassian server is exposed with Confluence tools but no Jira issue-read tool.

# Expected Behavior

Reports TOOL_NOT_AVAILABLE: the provider is available but the Jira retrieval tool is not exposed, and falls back to manual input.

# Important Checks

- Message names the missing operation.
- Does not substitute a different operation silently.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Collapsing the state into 'unavailable'.
- Using a guessed tool name.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.
