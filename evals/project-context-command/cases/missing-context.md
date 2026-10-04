# Scenario

`/context inspect` and `/context drift` with no PROJECT-CONTEXT.md.

# Input

/context inspect, then /context drift

# Context

A valid repository with no `PROJECT-CONTEXT.md` and no generator configuration.

# Expected Behavior

Inspect says there is no context and suggests `/context generate`, without generating. Drift reports that there is nothing to compare, as the tool does, and does not create a context or guess.

# Important Checks

- Neither operation writes a file.
- The next step is suggested, not taken.

# Failure Conditions

- Generating during inspect or drift.
- Summarizing a context that does not exist.

# Notes

Checks read-only operations and honest absence.
