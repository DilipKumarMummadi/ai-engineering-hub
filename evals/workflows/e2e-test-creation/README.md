# E2E Test Creation Workflow Evaluations

Evaluations for the [`e2e-test-creation`](../../../.claude/workflows/e2e-test-creation.md) workflow. See the [workflow evaluation overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the workflow justifies browser E2E before creating a test, recommends a lower test level when appropriate, and runs and stabilizes a test honestly when it does create one.

## Expected Workflow Behavior

- Decides between browser E2E and a lower level in the first stage.
- Ends with a recommendation when E2E is not justified, without creating a test.
- Identifies preconditions, data, locators, assertions and authentication before implementing.
- Runs the test and investigates failures before accepting it.
- Avoids shared and production environments without authorization.

## Cases

- [validation-rule-lower-level.md](cases/validation-rule-lower-level.md): a rule better tested lower; checks the decline path.
- [checkout-flow-shared-environment.md](cases/checkout-flow-shared-environment.md): a real browser flow against a shared environment; checks stages and safety.

## Common Failure Modes

- Creating an E2E test for every request.
- Skipping the test-level decision.
- Using brittle selectors or arbitrary sleeps to get a pass.
- Reporting a test as working without running it.
- Running against shared data or production without authorization.
