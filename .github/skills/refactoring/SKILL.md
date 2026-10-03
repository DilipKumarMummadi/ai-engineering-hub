---
name: refactoring
description: Improve the internal structure, readability, maintainability and design of existing code while preserving its behavior. Covers duplication, large methods and classes, coupling, naming, conditionals, dead code, dependency injection, async code, React/TypeScript structure, EF Core data access and API structure. Use for cleanup and restructuring; not for fixing bugs, adding features or optimizing performance.
---

# Refactoring

## Purpose

Help engineers improve the internal structure, readability, maintainability and design of existing code **while preserving existing behavior**, unless a behavior change is explicitly requested.

Typical targets:

- Duplicate code
- Large methods and large classes
- Poor separation of concerns and excessive coupling
- Unclear naming
- Complex conditional logic
- Unnecessary abstractions
- Dead code
- Dependency injection and testability problems
- `async`/`await` misuse
- React component structure and TypeScript typing
- EF Core and other database access structure
- API structure

Work from the repository's actual code and conventions. Do not assume a language, framework or architecture that the code does not show.

### Refactoring is not other work

| Activity | Changes behavior? | Goal |
| --- | --- | --- |
| **Refactoring** | No | Better structure, same behavior |
| **Bug fixing** | Yes, to match intended behavior | Correct a defect |
| **Feature development** | Yes, adds behavior | New capability |
| **Performance optimization** | Not functionally, but changes cost | Measured speed or resource gain |

Keep these separate. If a bug, feature need or performance issue shows up during refactoring, report it and let the user decide. Do not fold it silently into the refactor.

## When to Use

- The user asks to clean up, simplify, restructure, de-duplicate or modernize code without changing what it does.
- Code is hard to test, read or change because of its structure.
- A change is hard to make until the surrounding code is restructured ("make the change easy, then make the easy change").

## When NOT to Use

- The goal is to fix a defect. Use the [`debugging`](../debugging/SKILL.md) skill.
- The goal is to add or change behavior. Do that as a separate step, after or before the refactor.
- The goal is faster code. Measure first; a performance change needs evidence and is not a refactor.
- The goal is a system-level redesign. Use the [`architecture`](../architecture/SKILL.md) skill.
- The goal is only to assess quality. Use the [`code-review`](../code-review/SKILL.md) skill.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The code to refactor (files, classes, methods) and the goal | Required | If the goal is unclear, ask what should improve. |
| Existing tests | Gathered as needed | Needed to know whether behavior is protected. |
| Callers and dependents | Gathered as needed | Needed to know the impact of signature changes. |
| Project conventions and architecture | Gathered as needed | Follow them. |
| Known constraints (public API, database, configuration) | Optional | Determines risk. |

## Process

1. **Understand.** Clarify the objective and the scope. Read the code and its callers.
2. **Establish current behavior.** Determine what the code does today, including edge cases, error paths and side effects. Find the tests that protect it. If behavior is unprotected, say so and recommend characterization tests before changing anything significant.
3. **Identify opportunities.** List real problems that get in the way of reading, testing or changing the code. Skip changes that are only preference.
4. **Assess risk.** Note what could change behavior: public signatures, serialization, database queries and schema, configuration, timing, exception types, logging, ordering. Rate the risk of each step.
5. **Plan small changes.** Break the work into small, independently verifiable steps, lowest risk first.
6. **Refactor.** Make one step at a time, following project conventions. Keep each step behavior-preserving.
7. **Test.** Run the relevant tests after each meaningful step where tools allow. Add characterization tests if coverage was missing.
8. **Validate behavior.** Confirm the behavior is unchanged: tests, public contracts, and a review of the diff for accidental changes.
9. **Summarize.** Report what changed, why, what was verified, and what was left alone.

### Opportunity checklist

Use what applies.

- **Duplication:** extract only when the duplicated code is truly the same concept. Compare the copies closely. Differences may be intentional, so preserve them and flag them.
- **Large methods and classes:** split by responsibility, not by line count.
- **Separation of concerns and coupling:** separate I/O, business rules and presentation; reduce hidden dependencies.
- **Naming:** rename to reveal intent, using the project's vocabulary.
- **Conditional logic:** simplify with guard clauses, clearer conditions or table-driven logic where that reads better.
- **Unnecessary abstractions:** remove or avoid wrappers, layers and interfaces that add indirection without value.
- **Dead code:** remove only after confirming it is unused (search references, reflection, configuration, serialization).
- **Dependency injection and testability:** inject collaborators that make a class hard to test (clock, file system, network, email). Follow the existing DI style.
- **Async/await:** avoid blocking on async code, avoid `async void` outside event handlers, propagate cancellation where the project does, do not add `async` where it is not needed.
- **React/TypeScript:** split components by responsibility, move logic into hooks or functions where that clarifies, tighten types, avoid `any` where a real type is available, keep state close to where it is used.
- **EF Core and database access:** keep query logic where the project keeps it, avoid changing generated SQL unintentionally, be careful with tracking, loading and transaction boundaries.
- **API structure:** keep controllers or handlers thin, keep contracts unchanged, do not expose internal models by accident.

## Rules

- Preserve behavior unless a behavior change is explicitly requested.
- Avoid unnecessary rewrites. Prefer the smallest change that solves the stated problem.
- Make incremental changes that can each be verified and reverted.
- Inspect related tests before and after changing code.
- Respect the project's architecture and conventions over generic best practice.
- Avoid unnecessary abstractions and unnecessary dependencies.
- Do not change public APIs, database schema, serialized formats or configuration unless asked. Identify the risk when a step touches any of them and get confirmation first.
- Do not silently fix bugs or add features. Report them separately.
- Do not claim a performance improvement without measurement.
- Do not claim tests passed unless they were actually executed. State clearly when they were not.
- Do not delete code or files you have not confirmed are unused.
- Never expose secrets found in the code.
- Separate verified facts from assumptions.

## Output

```markdown
# Refactoring Analysis

## Objective

What is to be improved and the scope.

## Current Implementation

How the code works today, including relevant behavior and existing tests.

## Refactoring Opportunities

Real problems found, in order of value. Note anything out of scope (bugs, features, performance).

## Recommended Approach

The ordered sequence of small steps.

## Changes

What was changed, or will be changed, step by step.

## Behavior Preservation

Why behavior is unchanged, and any places where it might be at risk.

## Risks

Risks for public APIs, database, configuration, and so on.

## Testing

Existing tests, tests added or recommended, and which were executed.

## Validation

How the result was checked. State clearly what was and was not run.

## Summary

The outcome in a few sentences, and anything left for later.
```

## Examples

Illustrative only.

**Situation:** Two methods in an order service repeat the same 12 lines of validation. One copy checks `quantity > 0`. The other checks `quantity >= 0`.

**Response (abridged):**

```markdown
## Refactoring Opportunities

- The validation blocks are nearly identical and could share one method.
- They differ: `CreateOrder` rejects quantity 0, `UpdateOrder` accepts it. I cannot tell from the code whether this is intended.

## Recommended Approach

1. Extract the identical parts into a shared method.
2. Keep the quantity rule as it is in each caller (pass it in, or leave that check in place) so behavior does not change.
3. Report the difference as a question for the owner. Do not unify it here, because that would change behavior.

## Behavior Preservation

Both methods keep their current accept/reject outcomes. The existing tests for each method cover the quantity 0 case: not executed in this analysis.
```

## Related Skills

- [`code-review`](../code-review/SKILL.md): review the resulting change.
- [`testing`](../testing/SKILL.md): add characterization tests before risky refactoring.
- [`debugging`](../debugging/SKILL.md): investigate bugs found along the way.
- [`architecture`](../architecture/SKILL.md): for structural change beyond a local refactor.
