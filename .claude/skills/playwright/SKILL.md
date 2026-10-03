---
name: playwright
description: Plan, generate, review and debug Playwright browser and E2E tests. Covers stable locators, web-first assertions, synchronization, authentication, test data, smoke vs regression suites, flaky tests, headless/CI failures and report analysis. Use for any Playwright or browser-automation task; for general test strategy use the testing skill.
---

# Playwright

## Purpose

Help engineers plan, write, review, debug and stabilize Playwright tests for web applications. The skill helps to:

- Plan E2E tests and design smoke and regression suites
- Generate Playwright tests
- Review Playwright tests
- Debug Playwright failures, including CI and headless-only failures
- Improve test reliability and diagnose flakiness
- Design stable locators
- Handle authentication and test data
- Analyze Playwright reports

It specializes the principles of the [`testing`](../testing/SKILL.md) skill for browser automation. It does not repeat generic test strategy, scenario design, test quality or regression principles. Follow the `testing` skill for those.

It works with modern Playwright projects and any web application stack (React, Angular, Vue, .NET, Java, Node.js, Python or others). Do not assume an application framework unless the repository shows it.

**Tool requirement:** this skill is about Playwright, so it names Playwright APIs (for example `getByRole`, `expect`, `storageState`). It does not depend on any particular AI assistant.

## When to Use

- The user asks to plan or write Playwright or browser E2E tests.
- The user asks to review a Playwright test or suite.
- A Playwright test fails, is flaky, or passes locally but fails in CI or headless mode.
- The user asks about locators, authentication, test data, fixtures or Playwright reports.
- The user asks how to split tests into smoke and regression suites.

## When NOT to Use

- The task is general test strategy, unit or integration tests, or test quality that is not browser-specific. Use the [`testing`](../testing/SKILL.md) skill.
- The failure is not test-related (for example an application or infrastructure problem with no browser test involved). Use the [`debugging`](../debugging/SKILL.md) skill.
- A lower-level test would give the same confidence. Recommend that instead of an E2E test.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The user journey, feature or test to work on | Required | A description, requirement, or existing test file. |
| Existing Playwright config, tests, fixtures, page objects | Gathered as needed | Follow the existing structure and conventions. |
| Playwright report, trace, screenshot, video, console or network logs | Required for failure analysis | Use only what is actually available. |
| Test output and CI logs | Required for CI failure analysis | Include browser and Playwright versions if available. |
| Environment information (base URL, viewport, env vars, runner) | Optional | Needed for environment differences. |
| Authentication method (storageState, SSO, OAuth/OIDC, etc.) | Optional | Needed when the journey requires login. |

If information needed for a conclusion is missing, say what is missing and do not guess.

## Process

Use these steps for the task at hand. Apply the `testing` skill for the generic parts.

### 1. Design a Playwright test

1. Understand the user or business workflow.
2. Identify preconditions.
3. Identify required test data.
4. Identify the user actions.
5. Identify observable outcomes.
6. Define assertions.
7. Define cleanup requirements.
8. Classify the test: smoke, regression, critical user journey or negative scenario.

Prefer testing meaningful user behavior over implementation details.

### 2. Choose locators

Prefer stable, user-facing locators, in this priority:

1. `getByRole`
2. `getByLabel`
3. `getByPlaceholder`
4. `getByText` where appropriate
5. `getByTestId`
6. CSS selectors when necessary
7. XPath only as a last resort

Avoid selectors based on generated class names, DOM hierarchy, unstable IDs, styling implementation, or `nth-child` unless genuinely required. If the application forces a less stable locator, explain the trade-off (and, where the team owns the application, suggest adding an accessible name or a test ID).

### 3. Write assertions

Prefer web-first assertions (`expect(locator)...`) that auto-wait and retry. Assert meaningful user-visible or application-visible behavior: element visible or enabled, URL changed, navigation completed, expected text visible, API-driven state reflected in the UI, expected row or item exists, expected error shown. Avoid assertions that only verify implementation details.

### 4. Synchronize deterministically

Strongly avoid arbitrary waits such as `page.waitForTimeout(...)`. Prefer:

- Locator assertions
- `waitForURL`
- `waitForResponse` when justified
- `waitForLoadState` when appropriate
- Waiting on an explicit application state

Do not add waits to hide flaky behavior. If a timeout is genuinely required, explain why.

### 5. Handle authentication

Consider `storageState`, an authenticated browser context, login fixtures, reusable authentication setup and session reuse, including SSO, OAuth/OIDC and Azure authentication. Read credentials from environment variables or an approved secret-management mechanism. When authentication fails, determine whether the cause is credentials, authentication state, session expiration, a redirect, SSO, the browser context, or environment configuration.

### 6. Manage test data

Test data should be deterministic, isolated where possible, reusable, easy to clean up and appropriate for the environment. Avoid depending on data created by another test, and avoid test-order dependencies. If the application needs existing shared data, document that dependency.

### 7. Structure smoke vs regression suites

Smoke tests validate critical functionality quickly. Regression tests cover broader behavior. Do not put every test in the smoke suite. Classify every test when proposing a suite.

### 8. Respect project structure, page objects and fixtures

Respect the existing layout (for example `tests/`, `e2e/`, `playwright/`, `fixtures/`, `pages/`, `utils/`, `test-data/`). Do not introduce a new architecture unnecessarily.

- **Page objects:** use them when they improve maintainability and the repository already follows that approach. Do not create one for every page. Do not hide test intent behind abstraction. Prefer readable tests.
- **Fixtures:** use them for shared setup such as authentication, shared configuration, test data or common application setup. Avoid giant fixtures that hide behavior.

### 9. Handle network and API interaction

Where relevant, consider `waitForResponse`, route interception, `APIRequestContext`, mocking and request validation. Do not mock APIs unnecessarily. Prefer real integration behavior when the purpose of the test requires it.

### 10. Handle cookie and consent dialogs

Detect whether the dialog is application behavior or third-party behavior. Prefer a stable strategy, isolate handling of third-party consent systems, avoid brittle DOM manipulation, and do not permanently disable important application behavior just to make tests pass.

### 11. Analyze failures

**Headless or CI-only failures:** when a test passes locally in headed mode but fails headless or in CI, investigate timing assumptions, viewport differences, browser differences, missing dependencies, authentication state, environment variables, cookie or consent dialogs, network availability, race conditions, rendering differences, and display configuration where applicable. Do not simply force headed mode in CI.

**CI failure debugging:** inspect the Playwright report, trace, screenshot, video where available, console logs, network failures, test output, browser version, Playwright version, environment variables and the CI runner environment. Classify the failure as application defect, test defect, environment issue, timing or flakiness, authentication issue, or infrastructure issue.

**Flaky tests:** look for arbitrary waits, race conditions, shared state, unstable selectors, test ordering, external dependency instability, random test data, authentication or session issues, network timing, and incomplete cleanup. Do not fix flakiness by blindly increasing timeouts or retries.

**Report analysis:** identify the failed test, failure step, error, locator involved, screenshot evidence, trace evidence, network evidence, possible root cause and recommended fix. Follow the evidence-driven method of the `debugging` skill, and separate observed facts from hypotheses.

## Rules

- Prefer stable locators and web-first assertions.
- Avoid arbitrary waits and fragile selectors.
- Avoid test-order dependencies.
- Avoid hard-coded secrets. Never hard-code passwords, access tokens, secrets or API keys, and never log credentials or print them in output or examples.
- Avoid unnecessary mocking and unnecessary abstractions.
- Respect existing project conventions.
- Never fabricate test results. Never claim a test passed unless it was actually executed.
- Never fabricate trace, report, screenshot or log evidence.
- Never claim a root cause without evidence. If unconfirmed, say "Root cause not yet confirmed."
- Distinguish test failures from application failures, and investigate root causes instead of masking failures.
- Treat retries as a safety mechanism, not a root-cause fix.
- Do not disable, skip or delete existing tests to make a run pass unless the user explicitly asks.
- Do not run tests against production or other sensitive environments, or against data that must not change, unless the user explicitly authorizes it.
- Follow the `testing` skill for generic principles, and do not duplicate them here.
- Do not assume an application framework, test runner language or environment unless the repository shows it.

## Output

Use the format matching the task.

### Test plan

```markdown
# Playwright Test Plan

## User Journey

## Preconditions

## Test Data

## Test Scenarios

### Smoke

### Regression

### Negative

### Edge Cases

## Assertions

## Authentication

## Cleanup

## Risks
```

### Generated tests

```markdown
# Playwright Tests

## Scenarios Covered

## Test Files

## Locators

## Assertions

## Authentication

## Test Data

## Execution

State clearly whether the tests were executed, and the result if they were.
```

### Failure analysis

```markdown
# Playwright Failure Analysis

## Failure

## Evidence

## Failure Step

## Root Cause

If unconfirmed: "Root cause not yet confirmed."

## Recommended Fix

## Validation

## Regression Prevention
```

### Test review

```markdown
# Playwright Test Review

## Strengths

## Locator Issues

## Synchronization Issues

## Assertion Issues

## Authentication Issues

## Test Data Issues

## Flakiness Risks

## Maintainability

## Recommendations
```

## Examples

Illustrative only. The page and names are invented.

**Flaky test as submitted:**

```ts
test('user can save profile', async ({ page }) => {
  await page.goto('/profile');
  await page.click('div.form > div:nth-child(3) > button.btn-x7f2');
  await page.waitForTimeout(3000);
  expect(await page.locator('.msg').count()).toBeGreaterThan(0);
});
```

**Review (abridged):**

```markdown
# Playwright Test Review

## Locator Issues

- The button locator depends on DOM hierarchy, `nth-child` and a generated class name (`btn-x7f2`). It breaks on markup or build changes.
  Recommendation: `page.getByRole('button', { name: 'Save' })`.

## Synchronization Issues

- `waitForTimeout(3000)` is an arbitrary wait. It is too slow when the app is fast and too short when the app is slow, so it causes flakiness.
  Recommendation: remove it and wait on the outcome with an assertion.

## Assertion Issues

- `.msg` count > 0 passes for any message, including an error, and the assertion does not retry.
  Recommendation: assert the specific user-visible result with a web-first assertion.

## Recommendations

~~~ts
test('user can save profile', async ({ page }) => {
  await page.goto('/profile');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByRole('status')).toHaveText('Profile saved');
});
~~~

The test was not executed. The role and message text are assumptions and must be checked against the real page.
```

## Related Skills

- [`testing`](../testing/SKILL.md): generic test strategy, scenarios, quality and regression principles that this skill specializes.
- [`debugging`](../debugging/SKILL.md): the evidence-driven method used when analyzing failures.
- [`code-review`](../code-review/SKILL.md): review the application change that the tests cover.
