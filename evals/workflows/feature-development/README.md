# Feature Development Workflow Evaluations

Evaluations for the [`feature-development`](../../../.claude/workflows/feature-development.md) workflow. See the [workflow evaluation overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the workflow runs only the stages a feature needs, routes parts of the feature to the right agents and workflows, gates implementation and execution on authorization, and does not claim completion without evidence.

## Expected Workflow Behavior

- Clarifies the requirement before designing or implementing.
- Skips architecture assessment for a feature that fits existing structure.
- Routes API, schema and browser-flow parts to the right agent or workflow.
- Applies `security` only when the feature touches a trust boundary or sensitive data.
- Implements only on request, and never runs migrations or deployments.
- Reports stages completed, skipped and pending honestly.

## Cases

- [small-ui-field.md](cases/small-ui-field.md): a small, local change; checks skipping.
- [api-with-sensitive-data.md](cases/api-with-sensitive-data.md): an API plus schema change with sensitive data; checks decision points and safety.

## Common Failure Modes

- Running every stage for a trivial change.
- Skipping security or test stages when the feature clearly needs them.
- Starting implementation before the requirement is clear.
- Running a migration as part of implementation.
- Embedding API or architecture guidance in the workflow instead of using the agents.
