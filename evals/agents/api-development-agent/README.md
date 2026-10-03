# API Development Agent Evaluations

Evaluations for the [`api-development-agent`](../../../.claude/agents/api-development-agent.md). See the [evaluation suite overview](../../README.md) for the case format, outcomes and how to run a case, and section 14 of the [agent specification](../../../docs/agent-specification.md) for what agents are evaluated on.

## Purpose

To check that the agent designs and evolves APIs with sound contracts, validation, authorization, compatibility, resilience and documentation, and that it brings in supporting skills only when the API depends on them.

## Expected Agent Behavior

- Starts from the requirement and the existing API style, and models resources and operations with correct HTTP semantics.
- Defines validation, one consistent error format, and separate authentication and authorization, including object-level checks.
- Treats compatibility with existing consumers as a design input and lists breaking changes.
- Considers idempotency, concurrency, timeouts and retries where they matter.
- Plans testing and documentation, and never claims an API was tested unless it was.
- Does not expose internal models or make unrelated changes.

## Skill Selection Expectations

- `api-development` is always the core.
- `security`, `database-sql`, `performance`, `reliability`, `testing` and `architecture` are added only when the case calls for them.
- Supporting skills are run once and merged into the output sections.

Judge selection by the perspectives that show in the reasoning.

## Common Failure Modes

- Breaking existing clients without saying so.
- Treating a valid login as permission.
- Verb-based or inconsistent endpoints, wrong status codes or leaked internals.
- Retrying unsafe operations, or blocking on an unreliable dependency.
- Over-designing simple endpoints and running every supporting skill.
- Claiming tests passed or documentation was updated without doing it.

## Evaluation Process

1. Give the case's `# Input` and `# Context` to the agent.
2. Compare the response with Expected Behavior, Important Checks and Failure Conditions.
3. Judge the contract quality, security, compatibility, resilience, skill selection and output quality.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [new-resource-api](cases/new-resource-api.md) | Designs a resource API, with authorization and a database-enforced business rule. |
| [breaking-api-change](cases/breaking-api-change.md) | Evolves a contract for several consumers without breaking them. |
| [external-dependency](cases/external-dependency.md) | Designs an endpoint that depends on an unreliable service, with timeouts, fallback and retry safety. |
