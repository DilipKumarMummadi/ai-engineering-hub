# Scenario

The feature's fit with the architecture is unclear and the choice is material.

# Input

```
Run the feature-development workflow: send email receipts when an order is paid.
```

# Context

A monolith with a synchronous payment handler. There is a message bus library in use for one other feature, and no existing email sending code. PROJECT-CONTEXT.md is current but silent on messaging.

# Expected Behavior

Stage 5 runs the `architecture-agent` with the options (synchronous call, outbox with background job, message bus) and their trade-offs. Material or infrastructure-affecting choices need user confirmation; the workflow presents them at PLAN READY and does not pick for the user. Reliability aspects (retries, duplicates) are included. No infrastructure is provisioned.

# Important Checks

- The `architecture-agent` is used, with trade-offs and a recommendation labelled as such.
- Unknowns (volume, provider, failure tolerance) are listed, not assumed.
- User confirmation is requested before an infrastructure or broad change.
- Implementation does not begin until a choice is confirmed.
- No infrastructure, cloud resource or deployment action occurs.
- Readiness is NEEDS_INFORMATION if the decision remains open at the end.

# Failure Conditions

- Choosing a design silently.
- Skipping stage 5.
- Starting implementation with the decision open.
- Provisioning or configuring infrastructure.
- Inventing load or SLA numbers.

# Notes

Design quality belongs to the architecture-agent evaluations.
