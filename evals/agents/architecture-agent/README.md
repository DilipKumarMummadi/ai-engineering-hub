# Architecture Agent Evaluations

Evaluations for the [`architecture-agent`](../../../.claude/agents/architecture-agent.md). See the [evaluation suite overview](../../README.md) for the case format, outcomes and how to run a case, and section 14 of the [agent specification](../../../docs/agent-specification.md) for what agents are evaluated on.

## Purpose

To check that the agent reasons from requirements and constraints to a justified architecture with honest trade-offs, and that it brings in supporting perspectives only where the design depends on them.

## Expected Agent Behavior

- Separates functional and non-functional requirements, constraints, assumptions and open questions.
- Describes the current state from the evidence given and does not invent system details.
- Compares a few realistic options against ranked quality attributes, including operational cost and team capability.
- Addresses failure scenarios, security, observability and deployment where they matter.
- Recommends an approach with reasons, or states what would decide between valid alternatives.
- Proposes incremental, reversible migration with risks and validation.
- Stays read-only and does not invent numbers.

## Skill Selection Expectations

- `architecture` is always the core.
- `security`, `performance`, `reliability`, `observability`, `database-sql`, `api-development` and `refactoring` are added only when the design depends on them (for example trust boundaries changing, strict latency needs, data ownership).
- Supporting skills are run once and merged into the analysis. They are not added as parallel reports.

Judge selection by the perspectives that show up in the reasoning.

## Common Failure Modes

- Recommending a fashionable pattern (microservices, events) without tying it to the requirements.
- Presenting one option as the only answer.
- Ignoring team size, skills, cost or operational overhead.
- Missing failure scenarios or security implications that the case makes relevant.
- Inventing numbers or system facts.
- Big-bang migrations with no rollback.
- Invoking every supporting skill.

## Evaluation Process

1. Give the case's `# Input` and `# Context` to the agent.
2. Compare the analysis with Expected Behavior, Important Checks and Failure Conditions.
3. Judge the quality of reasoning, not which design was chosen, unless it contradicts the stated requirements.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [service-boundary](cases/service-boundary.md) | Weighs several ways to reduce compliance scope and brings in security and data ownership perspectives. |
| [event-driven-system](cases/event-driven-system.md) | Decides whether and how to use events from the latency, loss and operational constraints. |
| [migration-plan](cases/migration-plan.md) | Plans a database platform migration incrementally with cutover, validation and rollback. |
