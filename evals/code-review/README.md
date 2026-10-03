# Code Review Evaluations

Evaluations for the [`code-review`](../../.claude/skills/code-review/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## What Is Being Evaluated

Whether the skill produces reviews that are evidence-based, correctly prioritized and actionable. It should find real problems in the code it is shown, and not invent problems.

## Evaluation Principles

- Real issues are found and supported by the code.
- Severity reflects impact and likelihood, not preference.
- Each finding says why it matters and gives a concrete recommendation.
- The review follows the code's existing stack and conventions.
- Nitpicks and unnecessary rewrites are avoided.
- Missing tests are identified when relevant.
- Where context is missing, the review says so.

## What a Good Response Contains

- A summary of what was reviewed.
- Findings grouped by severity, each with file, location, issue, why it matters and recommendation.
- A Testing section covering existing, missing and recommended tests.
- Review Notes stating assumptions and limits.
- A plain statement when nothing significant is found.

## Common Failure Modes

- Missing the main defect.
- Inventing defects the code does not show.
- Wrong severity, such as a correctness bug rated as a suggestion.
- Vague recommendations ("improve this").
- Style and naming comments that bury the real issue.
- Rewriting the whole design instead of fixing the problem.
- Assuming libraries or frameworks that are not in the context.

## Scoring Approach

Qualitative only: Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). Judge the reasoning, not the wording.

## Cases

| Case | Tests |
| --- | --- |
| [obvious-bug](cases/obvious-bug.md) | Finds a plain correctness bug in business logic and rates it sensibly. |
| [security-issue](cases/security-issue.md) | Finds an injection flaw in a data-access path and explains the impact. |
| [missing-test](cases/missing-test.md) | Notices that correct code lacks boundary and state tests, without inventing a bug. |
