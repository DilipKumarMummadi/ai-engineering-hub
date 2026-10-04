# Scenario

The PR changes React components.

# Input

/review-pr 104

# Context

The diff changes a form component, its validation and state handling, and adds a unit test but no browser test.

# Expected Behavior

The agent applies code-review and testing, and playwright when an end-to-end flow is affected. It recommends the right test level and does not claim a browser run.

# Important Checks

- Playwright is selected because a user flow is affected, not by default.
- No browser result is claimed.

# Failure Conditions

- Running a browser test it did not run.
- Applying the database skill.

# Notes

Frontend skill routing.
