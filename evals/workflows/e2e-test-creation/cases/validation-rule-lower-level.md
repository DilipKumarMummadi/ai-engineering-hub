# Scenario

A request for an E2E test on behavior that belongs at a lower level.

# Input

```
Run the e2e-test-creation workflow: add a Playwright test checking that the signup form rejects emails without an @ sign.
```

# Context

A web application with an existing unit-test suite and a component test for the signup form. An email validation function already exists.

# Expected Behavior

The workflow, through the `test-planning-agent`, identifies this as a pure input validation rule that can be verified by a unit or component test, which is faster and more stable than a browser test. It recommends that level, explains why, offers the plan for it, and ends without creating a Playwright test. If the user still wants a browser test after seeing the recommendation, the workflow continues.

# Important Checks

- Stage 1 states the test-level decision and the reason.
- No Playwright test is created by default.
- The recommended lower-level test is described.
- Stages 2 to 11 are recorded as not run, with the reason.
- The user's option to proceed anyway is preserved.

# Failure Conditions

- Creating the E2E test because it was requested.
- Declining without explaining or recommending an alternative.
- Refusing to proceed when the user insists after the recommendation.
- Running the remaining stages after deciding E2E is not justified.

# Notes

The workflow is judged on the decision and its handling, not on the quality of the alternative test plan.
