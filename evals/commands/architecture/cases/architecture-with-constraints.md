# Scenario

A team asks whether to split a module into its own service and lists their constraints.

# Input

```
/architecture

Should we move billing out of our monolith into its own service? We are 9 engineers, nobody has run multiple services in production, and we have an audit in 6 months that covers anything handling card data. Please compare options, not just recommend microservices.
```

# Context

No other state is needed.

# Expected Behavior

The command routes the request to the `architecture-agent` with the team size, experience, audit timeline and the request to compare options all preserved. It does not choose an architecture or add design guidance.

# Important Checks

- The request is routed to `architecture-agent`.
- Team size, experience and the audit timeline are passed unchanged.
- The instruction to compare options is preserved.
- The command does not favor or suggest any architecture.
- The command adds no design method or template.

# Failure Conditions

- Dropping any of the constraints.
- Routing to the API or database agent.
- The command recommends microservices or a monolith.
- The command adds its own analysis sections.

# Notes

Choosing supporting skills such as security is agent behavior.
