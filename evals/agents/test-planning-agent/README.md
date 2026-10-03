# Test Planning Agent Evaluations

Evaluations for the [`test-planning-agent`](../../../.claude/agents/test-planning-agent.md). See the [evaluation suite overview](../../README.md) for the case format, outcomes and how to run a case, and section 14 of the [agent specification](../../../docs/agent-specification.md) for what agents are evaluated on.

## Purpose

To check that the agent turns a requirement, change or bug into a practical test plan that puts each scenario at the right level, covers the right risks, and uses browser E2E only where it earns its cost.

## Expected Agent Behavior

- Understands the behavior before planning, and lists assumptions and open questions where requirements are unclear.
- Identifies risk areas and designs scenarios across the relevant categories (positive, negative, edge, boundary, error, authorization, regression).
- Chooses the lowest test level that gives meaningful confidence, and justifies every E2E scenario.
- Plans test data, dependencies and execution, including smoke vs regression where browser tests exist.
- Plans regression coverage for a bug from its original failure.
- Does not write or run tests, and never claims coverage or results it did not verify.
- Hands off test writing or investigation as a recommendation.

## Skill Selection Expectations

- `testing` is always used.
- `playwright` only for scenarios that need a real browser.
- `api-development` when an API contract, validation, authorization or idempotency is involved.
- `debugging` when the task is a regression from an existing bug.
- Other skills only when relevant.

Judge selection by the reasoning and the plan, not by skill names appearing.

## Common Failure Modes

- Making most or all scenarios E2E.
- Missing categories that matter for the behavior (authorization, boundaries, concurrency).
- Generic scenarios that are not tied to the requirement.
- Omitting test data and dependencies.
- Dropping browser tests entirely for a flow that needs one.
- Regression plans that do not reproduce the original failure.
- Inventing requirements or claiming tests were run.

## Evaluation Process

1. Give the case's `# Input` and `# Context` to the agent.
2. Compare the plan with Expected Behavior, Important Checks and Failure Conditions.
3. Judge level selection, coverage of risk, test data, regression coverage, skill selection and output quality.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [new-api-feature](cases/new-api-feature.md) | Plans rule, API and concurrency tests for a new endpoint without browser tests. |
| [react-user-flow](cases/react-user-flow.md) | Splits a user flow between component tests and a small set of browser tests. |
| [regression-bug](cases/regression-bug.md) | Plans regression coverage that reproduces a known failure and its boundaries. |
