# Refactoring Evaluations

Evaluations for the [`refactoring`](../../.claude/skills/refactoring/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the skill improves structure without changing behavior, picks changes that are worth making, and keeps refactoring separate from bug fixes, features and performance work.

## Evaluation Principles

- Behavior is preserved, and any place where it could change is called out.
- Real problems are targeted. Preference-only changes and rewrites are avoided.
- Changes are small, ordered and verifiable.
- Existing tests and project conventions are respected.
- Bugs and feature ideas found on the way are reported separately, not silently applied.
- Nothing is claimed as tested or faster without evidence.

## Expected Behavior

A good response explains the current behavior, identifies the genuine opportunities, proposes a small sequence of changes, says how behavior is protected, and states what was and was not run. Differences between apparent duplicates are noticed and handled deliberately.

## Common Failure Modes

- Unifying code that only looks the same, which silently changes behavior.
- Fixing a bug or adding a feature inside the refactor without saying so.
- Adding layers, interfaces or dependencies that the code does not need.
- Large rewrites where a local change would do.
- Claiming tests pass or performance improved without running or measuring anything.
- Ignoring the project's existing style and architecture.

## Qualitative Evaluation

Outcomes are Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [duplicated-service-logic](cases/duplicated-service-logic.md) | Removes duplication without erasing an intentional-looking difference. |
| [large-method](cases/large-method.md) | Splits a large method while keeping its behavior, including a questionable one, and reports it. |
| [unnecessary-abstraction](cases/unnecessary-abstraction.md) | Resists adding layers, and makes the one change that improves testability. |
