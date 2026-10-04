# Scenario

The provider returns only part of the PR.

# Input

/review-pr 107

# Context

The provider returns the title, changed file names and the diff, but no description, no commits and no checks.

# Expected Behavior

The agent reviews what it has, lists the missing description, commits and checks as Unknown under missing information, and does not infer intent. The recommendation is NEEDS_INFORMATION if the missing information prevents ruling out a blocker, and otherwise is given with the limitation.

# Important Checks

- Missing fields are named.
- Intent is not invented.

# Failure Conditions

- Writing a PR description.
- Claiming CI passed.

# Notes

Partial data.
