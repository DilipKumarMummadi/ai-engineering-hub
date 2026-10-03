# Playwright Evaluations

Evaluations for the [`playwright`](../../.claude/skills/playwright/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## What Is Being Evaluated

Whether the skill produces reliable, maintainable browser tests and diagnoses browser test failures from evidence, building on the principles of the `testing` skill.

## Evaluation Principles

- Tests wait for application state, not for elapsed time.
- Locators follow what a user sees and the accessibility tree where possible, not styling or page structure.
- Assertions check user-visible outcomes and retry until they hold.
- Failures are diagnosed from the evidence given, including differences between environments.
- Masking a problem (longer timeouts, retries, forced actions, headed mode) is not accepted as a fix.
- Secrets are never hard-coded, and test results are never fabricated.

## What a Good Response Contains

- A clear diagnosis of why the test is unreliable or failing, tied to the evidence.
- A corrected test or precise steps, consistent with the existing project style.
- A reason for each change, in terms of reliability and maintainability.
- A statement of whether anything was executed.
- Prevention that fits the problem.

## Common Failure Modes

- Treating a symptom with a longer timeout, more retries or a forced click.
- Keeping fixed delays, or replacing one delay with another.
- Keeping selectors that depend on generated class names or DOM position.
- Blaming "headless mode" or "CI" without analysis.
- Rewriting the test suite architecture when a small fix is enough.
- Claiming a test now passes without running it.

## Scoring Approach

Qualitative only: Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). Judge whether the response reaches the right diagnosis and a deterministic fix. Specific API names are not required if the approach is sound.

## Cases

| Case | Tests |
| --- | --- |
| [flaky-wait](cases/flaky-wait.md) | Replaces time-based waiting with synchronization on application state. |
| [fragile-locator](cases/fragile-locator.md) | Replaces structure-dependent locators with user-facing ones. |
| [headless-failure](cases/headless-failure.md) | Diagnoses a CI-only failure as an environment state difference. |
