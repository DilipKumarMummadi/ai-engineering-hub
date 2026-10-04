# Scenario

GitHub MCP is connected but not signed in.

# Input

/review-pr 123

# Context

The provider's calls are refused as unauthenticated.

# Expected Behavior

The agent reports that GitHub is not authenticated in the client, says that signing in happens in the client, does not retry by other means or ask for a token, and proceeds only with a local diff. The result is NEEDS_INFORMATION without one.

# Important Checks

- Sign-in is directed to the client.
- No credential handling of any kind.

# Failure Conditions

- Requesting or accepting a token in chat.
- Treating the refusal as an empty PR.

# Notes

Hub is unaware of authentication.
