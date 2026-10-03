# Scenario

A team is adding an endpoint and wants a test plan. They state a CI constraint and a preference.

# Input

```
/test-plan

Plan tests for the new POST /transfers endpoint. CI time is tight, so avoid browser tests unless they're really needed. Rules: amount must be greater than 0 and at most 10,000; source and destination must differ.
```

# Context

No other state is needed.

# Expected Behavior

The command routes the request to the `test-planning-agent` with the requirements and both constraints intact. The command does not choose test levels, decide whether to use Playwright, or add a test template.

# Important Checks

- The request is routed to `test-planning-agent`.
- The amount and account rules reach the agent unchanged.
- The CI time constraint and the preference to avoid browser tests are preserved.
- The command does not pick test levels or tools itself.
- No test plan structure is added by the command.

# Failure Conditions

- Routing to the `api-development-agent` because the request mentions an endpoint.
- Dropping the constraint about browser tests.
- The command includes its own list of test categories.
- The command writes or runs tests.

# Notes

Whether the agent then uses the `playwright` skill is agent behavior.
