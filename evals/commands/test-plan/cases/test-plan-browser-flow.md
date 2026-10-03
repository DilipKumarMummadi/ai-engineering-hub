# Scenario

A developer asks for a plan for a user flow and describes the steps in the browser.

# Input

```
/test-plan

We're adding a coupon step to checkout: the user enters a code, presses Apply, sees the new total, then pays. The server validates coupons through POST /api/coupons/validate. What should we test?
```

# Context

No other state is needed.

# Expected Behavior

The command passes the flow description to the `test-planning-agent` as written. It does not itself decide that the flow needs browser tests, and does not invoke the `playwright` skill. The agent makes that decision.

# Important Checks

- The request is routed to `test-planning-agent`, not to a Playwright skill directly.
- The flow description, including the server validation detail, is passed unchanged.
- The command makes no decisions about test levels.
- The command adds no Playwright-specific guidance.

# Failure Conditions

- The command invokes the `playwright` skill directly.
- The command tells the agent to use browser tests for everything.
- Summarizing the flow and losing the validation endpoint detail.
- Routing to the `api-development-agent`.

# Notes

The architecture is Command, then Agent, then Skills. A command does not skip the agent.
