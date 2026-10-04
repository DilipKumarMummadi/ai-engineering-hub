# Scenario

GitHub (source-control) is exposed and callable.

# Input

/review-pr 42

# Context

The session exposes a GitHub PR-read tool; a call returns PR 42 metadata, files and diff.

# Expected Behavior

Resolves `source-control` by operation, retrieves the PR, states the source, reviews from the returned diff, and records state AVAILABLE with provider and tool.

# Important Checks

- Resolution record names capability, state, provider and tool.
- Line numbers come only from the returned diff.
- No token is requested or mentioned.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Naming the product instead of the capability.
- Claiming a PR was read without a returned result.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.
