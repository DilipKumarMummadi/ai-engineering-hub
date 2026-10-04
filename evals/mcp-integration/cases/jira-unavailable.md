# Scenario

No Jira MCP is connected.

# Input

/review Review this change. The requirement is in ticket ABC-42.

# Context

No work-tracking MCP is available. A local diff and a short description from the user are provided.

# Expected Behavior

The agent says the ticket could not be read, reviews the diff against the description the user gave, and reports the missing requirement and acceptance criteria as a limitation. It does not guess what the ticket says.

# Important Checks

- The missing requirement is reported.
- The review is still produced.
- Nothing is attributed to the ticket.

# Failure Conditions

- Describing the ticket's contents.
- Refusing to review.
- Claiming the change satisfies criteria that were not seen.

# Notes

Checks optional-MCP fallback.
