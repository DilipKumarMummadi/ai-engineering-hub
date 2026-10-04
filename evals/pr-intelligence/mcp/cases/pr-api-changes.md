# Scenario

The PR changes API endpoints.

# Input

/review-pr 101

# Context

The diff adds an endpoint and changes a response model and status codes. Tests are updated for the new endpoint only.

# Expected Behavior

The agent applies code-review and adds api-development, testing and security as the change calls for them. It assesses contract and compatibility, reports consumers it cannot see as Unknown, and recommends tests for the changed status codes.

# Important Checks

- Skills follow the change.
- Unseen consumers are Unknown.
- Findings cite file and diff lines.

# Failure Conditions

- Running every skill.
- Claiming no consumers exist.
- Inventing line numbers.

# Notes

API skill routing.
