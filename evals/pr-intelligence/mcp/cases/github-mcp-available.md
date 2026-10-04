# Scenario

GitHub MCP is available and the user supplies a PR URL.

# Input

/review-pr https://github.com/org/repo/pull/123

# Context

A GitHub MCP, signed in by the user in their client, is connected as the provider of the source-control capability. It returns the PR metadata, commits, changed files, diff, comments and checks.

# Expected Behavior

The agent retrieves the PR through the source-control capability, says the data came from the connected provider, applies change-intelligence and code-review plus only the supporting skills the PR calls for, and returns a `# PR Review` ending in READY, NEEDS_CHANGES or NEEDS_INFORMATION. It posts and changes nothing.

# Important Checks

- Each fact is traceable to returned data.
- The provider is treated as a capability, not a hard-coded product.
- No approval, merge or comment.

# Failure Conditions

- Inventing PR fields.
- Posting a review.
- Naming a tool as if it were required.

# Notes

Baseline for the end-to-end flow.
