# Scenario

A developer wants to change an existing endpoint and lists who uses it.

# Input

```
/api

We want to split `name` into `firstName` and `lastName` in GET /api/v1/customers/{id}. Consumers: our web app, a mobile app (old versions stay in use for months), and a partner integration that has a 12-month support commitment for v1. Design the change.
```

# Context

No other state is needed.

# Expected Behavior

The command routes the request to the `api-development-agent` with the endpoint, the field change, all three consumers and the commitments preserved. The command does not decide how to version or whether the change is breaking.

# Important Checks

- The request is routed to `api-development-agent`.
- All three consumers and the 12-month commitment reach the agent unchanged.
- The command does not judge compatibility or propose a design.
- The command does not modify code or contracts.

# Failure Conditions

- Dropping any consumer or the commitment.
- Routing to the architecture agent.
- The command says the change is breaking or non-breaking.
- The command implements the change.

# Notes

Compatibility reasoning is the agent's job.
