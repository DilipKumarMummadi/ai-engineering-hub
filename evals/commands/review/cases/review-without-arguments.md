# Scenario

A developer has local changes in a branch and types the command with nothing after it.

# Input

```
/review
```

# Context

The working tree has uncommitted changes and the branch has commits that are not on the main branch.

# Expected Behavior

The command treats the current changes as the target and routes to the `pr-review-agent` without asking the user to provide anything. If the agent needs more (for example the intent of the change), the agent asks.

# Important Checks

- The request is routed to `pr-review-agent`.
- The current uncommitted and branch changes are identified as the review target.
- The command does not ask for a PR number, diff or form before starting.
- The command does not make up a PR description or requirement.

# Failure Conditions

- Refusing to proceed because no arguments were given.
- Asking the user a list of questions before routing.
- Reviewing a different target, or the whole repository.
- Inventing a change description.

# Notes

The agent's own questions about missing context are its behavior and are judged in the agent evaluations.
