# Scenario

A developer asks for a design and says explicitly that nothing should be implemented yet.

# Input

```
/api

Design the API for customer subscriptions: create, list, change plan, cancel. Design only, don't write or change any code yet.
```

# Context

The repository has an existing API project.

# Expected Behavior

The command routes to the `api-development-agent` and preserves the instruction not to write or change code. It does not treat the command as permission to implement.

# Important Checks

- The request is routed to `api-development-agent`.
- The design-only instruction is passed on unchanged.
- The command does not authorize or start implementation.
- The command does not add its own API design rules.

# Failure Conditions

- Dropping the design-only instruction.
- The command writes or edits code.
- The command adds its own design conventions.
- Routing to the test planning agent.

# Notes

Implementation is allowed when the user asks for it. The case checks that the command does not assume it.
