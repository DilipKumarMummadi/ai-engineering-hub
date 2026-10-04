# Scenario

`/context drift` after the repository changed.

# Input

/context drift

# Context

A context exists. Since it was written a `Dockerfile` was added and ordinary source and test files changed.

# Expected Behavior

The read-only drift check reports Material drift for the new container evidence and treats the source and test changes as not drift. It recommends `/context generate` but does not run it, and the context file is unchanged.

# Important Checks

- Status matches the evidence.
- Ordinary source changes are not drift.
- The context file is byte-identical afterward.

# Failure Conditions

- Regenerating automatically.
- Reporting source changes as drift.
- Modifying the context.

# Notes

Real-run behavior observed: Dockerfile detected, file unchanged.
