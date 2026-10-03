# Testing Evaluations

Evaluations for the [`testing`](../../.claude/skills/testing/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## What Is Being Evaluated

Whether the skill helps engineers design and judge tests by the behavior they verify, picks the right level of test, and reviews tests critically instead of counting them.

## Evaluation Principles

- Tests are judged by whether they would catch a real defect.
- Business rules, boundaries and failure paths matter more than coverage numbers.
- The lowest-level test that gives reliable confidence is preferred.
- Recommendations are specific: concrete inputs and expected results.
- Existing conventions and frameworks are respected.
- The response never claims tests ran or passed unless they did.

## What a Good Response Contains

- The behavior under test, derived from the requirement.
- Specific missing scenarios or weak assertions, each tied to the code shown.
- A reasoned choice of test type.
- Concrete recommended tests or improvements.
- A statement of execution status when tests are generated.

## Common Failure Modes

- Approving tests that would pass even if the code were wrong.
- Vague advice such as "add more tests".
- Asking for more tests at the highest level (E2E) by default.
- Chasing coverage or test count.
- Inventing defects in correct code.
- Introducing new frameworks or heavy mocking without need.
- Claiming test results without running anything.

## Scoring Approach

Qualitative only: Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes).

## Cases

| Case | Tests |
| --- | --- |
| [missing-edge-case](cases/missing-edge-case.md) | Finds important untested boundaries and rules in an existing test suite. |
| [weak-assertion](cases/weak-assertion.md) | Recognizes tests that pass despite a defect and strengthens them. |
| [wrong-test-type](cases/wrong-test-type.md) | Challenges an E2E-heavy plan and chooses appropriate test levels. |
