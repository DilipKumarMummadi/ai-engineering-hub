# Scenario

A developer uses the command for something that is really a small code cleanup.

# Input

```
/architecture

Can you rename the methods in OrderService to follow our naming convention?
```

# Context

No other state is needed.

# Expected Behavior

The command still routes to the `architecture-agent`, because the user chose that command. It does not reroute the request to another agent or skill, and does not decide for itself that the request is out of scope. The agent's own When NOT to Use guidance handles the mismatch.

# Important Checks

- The request is routed to `architecture-agent`.
- The command does not silently send the request elsewhere.
- The command does not add its own scope checks or redirect messages.
- The request text is passed unchanged.

# Failure Conditions

- The command routes to a refactoring skill or another agent on its own.
- The command refuses the request.
- The command performs the renaming.
- The command adds routing logic that duplicates the agent's scope rules.

# Notes

Redirecting the user is the agent's behavior and is evaluated in the agent evaluations. This case checks only that the command stays a thin router.
