---
name: testing
description: Plan, generate, review and improve software tests across languages and frameworks. Identifies meaningful scenarios, selects the right test type, finds missing or weak tests, and plans regression coverage with a behavior-first approach. Use when asked to test, add tests, review tests or analyze a failing test; not for browser-specific automation or for investigating a production failure.
---

# Testing

## Purpose

Help engineers validate behavior and prevent regressions. The skill helps to:

- Understand what needs to be tested
- Identify meaningful test scenarios
- Design test coverage and select an appropriate test type
- Generate tests
- Review existing tests, find missing tests and weak tests
- Analyze test quality and failing tests
- Plan regression coverage

It works across languages and stacks (for example .NET, Java, Python, JavaScript, TypeScript, React, Angular, Node.js, APIs, databases and microservices). Do not assume a language or framework unless the repository context shows it.

**Core principle:** testing is about validating behavior and preventing regressions. Do not optimize for test count or coverage percentage alone. A good test gives meaningful confidence in expected behavior.

Priorities, in order:

1. Business behavior
2. Critical paths
3. Failure scenarios
4. Edge cases
5. Boundary conditions
6. Integration behavior
7. Regression prevention

## When to Use

- The user asks to plan, design or generate tests for a feature, function, API or component.
- The user asks to review existing tests, find missing tests or improve weak tests.
- A bug was fixed and regression coverage is needed.
- A test is failing and it is unclear whether the test or the application is wrong.
- The user asks which type of test is appropriate.

## When NOT to Use

- The task is reviewing production code quality in general. Use the [`code-review`](../code-review/SKILL.md) skill.
- The task is investigating an application, build or runtime failure that is not test-related. Use the [`debugging`](../debugging/SKILL.md) skill.
- The task is browser automation specifics (locators, browser configuration, traces). This skill is generic and gives no browser-tool guidance.
- The user only wants a coverage number. This skill does not optimize for coverage percentage.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Code, feature or behavior to test | Required | Source code, requirement, ticket or description. |
| Requirements or acceptance criteria | Optional, strongly preferred | Needed to know the intended behavior. If absent, infer cautiously and state the assumption. |
| Existing tests and test utilities | Gathered as needed | Follow their frameworks and conventions. |
| Project conventions (naming, folder layout, frameworks) | Gathered as needed | From the repository. |
| Test output, failure details | Optional | Required when analyzing a failing test. |
| Bug description or original failure | Optional | Required for regression tests. |

If the intended behavior is unknown, ask for it rather than guess.

## Process

### 1. Understand the requirement

Identify expected behavior, inputs, outputs, business rules, constraints, dependencies and failure conditions. Do not write tests before understanding the intended behavior.

### 2. Identify testable behavior

Break the requirement into observable behaviors, for example Input → Validation → Processing → Output. Identify what should be observable at each meaningful boundary.

### 3. Identify test scenarios

Consider:

- **Happy path:** normal valid inputs.
- **Negative cases:** invalid input or expected failures.
- **Edge cases:** unusual but valid scenarios.
- **Boundary cases:** minimum and maximum values and limits.
- **State transitions:** where applicable.
- **Dependency failures:** API unavailable, database failure, timeout, message failure, external service failure.
- **Authorization (where applicable):** authorized user, unauthorized user, insufficient permissions.
- **Data integrity (where applicable):** duplicate data, missing data, invalid relationships, concurrency issues.

### 4. Select the appropriate test type

Choose among unit, integration, API, component, end-to-end, contract and regression tests. Prefer the lowest-level test that can reliably validate the behavior. Do not recommend an E2E test when a unit or integration test gives sufficient confidence.

### 5. Review existing tests

When tests exist, check:

- What behavior is covered, and what is missing?
- Are assertions meaningful?
- Are tests isolated and deterministic?
- Are mocks appropriate?
- Are edge cases covered?
- Are failures easy to diagnose?
- Is test setup unnecessarily complex?

### 6. Identify weak tests

Flag tests that:

- Assert implementation details unnecessarily
- Have weak assertions
- Test too many unrelated behaviors
- Depend on test ordering or shared mutable state
- Use excessive mocking
- Are flaky
- Are overly coupled to implementation
- Do not actually validate the intended behavior

### 7. Generate tests

When asked to generate tests:

- Follow existing repository conventions and naming.
- Reuse existing test utilities and frameworks.
- Keep tests focused and test observable behavior.
- Avoid unnecessary mocks and setup.
- Do not introduce a new testing framework unless explicitly requested.

### 8. Validate test quality

After generating or reviewing tests, verify that they compile (where possible), are logically correct, have meaningful assertions, cover the important scenarios, and are deterministic, isolated and maintainable. If execution is not available, state clearly that the tests were not executed.

### Type guidance

- **Unit tests:** test one meaningful behavior, isolate external dependencies, use focused setup, assert meaningful outcomes, cover important branches and edge cases. Do not require a test for every method or line purely for coverage.
- **Integration tests:** use when interaction between components matters, such as database interaction, repository behavior, API integration, messaging, serialization and authentication integration. Prefer realistic boundaries where they add meaningful confidence.
- **API tests:** consider HTTP method, status code, request validation, response contract, error response, authentication, authorization, boundary inputs, serialization and idempotency where relevant.
- **E2E tests:** use for important user or business journeys, critical workflows, cross-component behavior and high-value regression scenarios. Do not turn every scenario into an E2E test. Browser-specific guidance is out of scope for this skill.

### Regression testing (bug fixes)

1. Understand the original failure.
2. Identify the behavior that was broken.
3. Add or update a test that reproduces the failure.
4. Verify the test fails before the fix where practical.
5. Apply the fix.
6. Verify the test passes.
7. Consider related regression scenarios.

### Failing test analysis

When a test fails, separate: test defect, application defect, environment issue, dependency issue, timing issue, data issue and flaky behavior. Do not modify the test just because it is failing. First determine whether the application behavior or the test expectation is wrong. For deep investigation of the cause, use the `debugging` skill.

## Rules

- Understand requirements before generating tests.
- Prioritize behavior over coverage numbers.
- Prefer tests that are deterministic, independent, readable, focused, repeatable, fast where possible, behavior-oriented and easy to diagnose.
- Avoid testing implementation details unnecessarily, excessive mocking, duplicate tests, random test data without controlled expectations, time-dependent tests unless required, and dependence on external systems unless integration testing is the purpose.
- Avoid unnecessary E2E tests and unnecessary mocks.
- Follow existing project conventions and frameworks.
- Do not introduce new dependencies or frameworks unnecessarily.
- Identify missing edge cases.
- Distinguish test failures from application failures.
- Never claim tests passed unless they were actually executed.
- Never fabricate test output.
- Never fabricate coverage numbers.
- State clearly when execution was not possible.
- Do not change production code when asked only for tests, unless explicitly requested. If a test reveals a defect, report it.
- Do not delete or weaken existing tests without explicit reason and confirmation.
- Never put real secrets or personal data in test data.
- Do not assume a language or framework unless the context shows it.

## Output

Use the format matching the task.

### Test plan

```markdown
# Test Plan

## Behavior Under Test

## Test Strategy

## Test Scenarios

### Happy Path

### Negative Cases

### Edge Cases

### Boundary Cases

### Failure Scenarios

## Test Type

Why each scenario belongs to the selected test type.

## Regression Coverage

## Gaps

## Recommendations
```

### Test review

```markdown
# Test Review

## Coverage Summary

## Strengths

## Missing Scenarios

## Weak Tests

## Flakiness Risks

## Maintainability Issues

## Recommendations
```

### Generated tests

```markdown
# Generated Tests

## Scenarios Covered

## Test Files Changed

## Tests Added

## Coverage Gaps

## Execution Status

State clearly whether tests were actually executed, and the result if they were.
```

## Examples

Illustrative only, and technology-neutral.

**Feature:** `apply_coupon(cart_total, code)` gives 10% off when the code is valid and `cart_total` is at least 50. It looks up the code in an external coupon service. A past bug accepted coupons on the day after they expired. There is no test for that bug.

**Test plan (abridged):**

| Scenario | Input | Expected | Test type | Why |
| --- | --- | --- | --- | --- |
| Valid input | total 100, valid code | total 90 | Unit | Pure business rule. Fake the coupon lookup. |
| Invalid input | total 100, unknown code | rejected, total unchanged | Unit | Same rule, no real service needed. |
| Boundary input | total 50, valid code | discount applied | Unit | At the minimum. Also test 49.99, which is rejected. |
| Dependency failure | coupon service times out | clear error, no discount, no crash | Unit with a failing fake | Behavior on failure does not need the real service. |
| Missing regression test | coupon expired yesterday | rejected | Unit | Reproduces the past bug. Pin the date so the test is deterministic, and also test the last valid day. |
| Service contract | real service response shape | parsed correctly | Integration or contract | The only scenario that needs the real boundary. |

**Not recommended:** an E2E test for each row. The unit tests give the needed confidence at lower cost, and one E2E test for the checkout journey is enough.

**Gaps:** the regression scenario is currently missing and should be added first.

## Related Skills

- [`code-review`](../code-review/SKILL.md): review the production change together with its tests.
- [`debugging`](../debugging/SKILL.md): investigate the cause when a test failure is not explained by the test itself.
