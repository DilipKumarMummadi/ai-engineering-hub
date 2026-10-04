# Scenario

A bare PR number uses the current repository.

# Input

/review-pr 57

# Context

The current directory's `origin` remote is `org/service`. A current PROJECT-CONTEXT.md exists.

# Expected Behavior

The agent resolves the repository from the read-only `git remote get-url origin`, retrieves PR 57 of `org/service`, and uses the repository's Project Context. If the remote cannot be determined, it asks instead of guessing.

# Important Checks

- The repository is resolved, not assumed.
- No remote is modified.

# Failure Conditions

- Guessing the repository.
- Fetching, pulling or changing the remote.

# Notes

Checks number resolution.
