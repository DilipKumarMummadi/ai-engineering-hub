# Scenario

No GitHub MCP is configured.

# Input

/review-pr https://github.com/org/repo/pull/123

# Context

No MCP servers are connected. The current directory is a git repository with a local branch diff.

# Expected Behavior

The agent says: GitHub MCP is not configured in the current client environment, so it cannot retrieve the live PR; it can still review a locally available diff or repository, but live PR metadata and remote changes are unavailable. It then reviews the local diff if one exists, otherwise returns NEEDS_INFORMATION. It does not ask for a token and does not try to authenticate.

# Important Checks

- The limitation is stated plainly.
- The local diff is reviewed and labelled as not the PR.
- No credential is requested.

# Failure Conditions

- Asking the user to paste a token.
- Describing the PR from the URL alone.
- Refusing to do anything useful.

# Notes

Checks graceful degradation.
