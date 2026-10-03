---
name: architecture
description: Analyze, design and evolve software architecture from requirements, constraints and existing system context. Covers component and service boundaries, integration and communication patterns, data, security, scalability, reliability, observability, deployment, cost, technical debt and migration, with explicit trade-offs and ADRs. Use for design decisions and architecture reviews; not for local code cleanup.
---

# Architecture

## Purpose

Help engineers analyze, design and evolve software architecture based on requirements, constraints and the existing system. The skill produces reasoned options and trade-offs, not pattern recommendations.

Topics it covers:

- System and application architecture, component and service boundaries
- Microservices and modular monoliths, domain boundaries, dependency direction
- Integration patterns, synchronous vs asynchronous communication, event-driven architecture, messaging
- Caching and databases, API boundaries, authentication and authorization
- Scalability, availability, reliability and observability
- Deployment and cloud architecture, cost
- Technical debt and migration strategies

Never recommend an architecture because it is popular. Recommend it because it fits the requirements and constraints better than the alternatives.

## When to Use

- A new system, feature or integration needs a design.
- The team is choosing between approaches (for example modular monolith vs services, sync vs async, build vs buy).
- An existing system has a scaling, reliability, cost or maintainability problem that may need structural change.
- A migration or modernization needs a plan.
- A design decision needs to be recorded (ADR).

## When NOT to Use

- The task is restructuring code inside a class or module. Use the [`refactoring`](../refactoring/SKILL.md) skill.
- The task is designing a specific HTTP API contract. Use the [`api-development`](../api-development/SKILL.md) skill.
- The task is schema or query design. Use the [`database-sql`](../database-sql/SKILL.md) skill.
- The task is reviewing a code change. Use the [`code-review`](../code-review/SKILL.md) skill.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The problem or decision to make | Required | What needs to be designed or decided. |
| Functional requirements | Required, or elicited | Ask if they are unclear. |
| Non-functional requirements (load, latency, availability, consistency, security, compliance) | Strongly preferred | Design depends on them. Ask for the ones that matter. |
| Constraints (team size and skills, budget, timeline, existing platform, regulations) | Strongly preferred | |
| Current state (code, diagrams, infrastructure, metrics, incident history) | Gathered as needed | Inspect the repository where available. |
| Prior decisions and ADRs | Optional | Respect them unless there is a reason to revisit. |

If key information is missing, list it as open questions. Do not invent numbers or system details.

## Process

```
Requirements → Constraints → Current State → Quality Attributes → Options → Trade-offs
→ Recommended Design → Migration / Implementation Plan → Validation
```

1. **Requirements.** State functional requirements and non-functional requirements separately. Mark anything assumed.
2. **Constraints.** Identify fixed limits: team, skills, budget, deadlines, existing technology, compliance, operational capacity.
3. **Current state.** Describe the existing system from evidence (code, configuration, metrics). Note known problems and technical debt. If there is no existing system, say so.
4. **Quality attributes.** Rank the ones that matter most (for example consistency, availability, latency, scalability, security, cost, operability, changeability). Design decisions follow from this ranking.
5. **Options.** Describe a small number of realistic options, including "keep the current design with targeted changes" where it is viable. Do not include options only to make the list longer.
6. **Trade-offs.** Compare options against the ranked quality attributes and the constraints. Consider complexity, operational overhead, team capability, cost, scalability needs, reliability needs, security, maintainability and the existing ecosystem.
7. **Recommended design.** Recommend an option with reasons tied to the requirements, or, if several designs would reasonably satisfy them, say so and state what would tip the decision. Describe components, data flow, failure scenarios, security, observability and deployment.
8. **Migration or implementation plan.** Give incremental steps where there is an existing system: what to do first, how to stay reversible, how to run old and new in parallel, and how to know each step worked.
9. **Validation.** Say how the design will be checked: load tests, failure injection, prototypes, metrics to watch, review by the owning team.

### Explicit statements

Every analysis must separate and label:

- Functional requirements
- Non-functional requirements
- Constraints
- Assumptions
- Risks
- Trade-offs

### Areas to consider

Use what applies.

- **Boundaries and dependencies:** cohesion within components, dependency direction, coupling, who owns which data.
- **Communication:** synchronous for a result needed now, asynchronous when work can be deferred or decoupled. Consider failure handling, retries, duplicates, ordering and back pressure.
- **Event-driven designs and messaging:** delivery guarantees, idempotent consumers, dead-letter handling, schema evolution, and the operational cost of running the broker.
- **Data and caching:** consistency needs, transaction boundaries, cache invalidation, read/write patterns.
- **Security:** authentication, authorization, data protection, trust boundaries, secrets.
- **Reliability and scalability:** single points of failure, bottlenecks (identify from evidence), degradation behavior, capacity.
- **Observability:** logs, metrics, traces, health checks, alerting needed to operate the design.
- **Deployment and cost:** environments, release process, infrastructure cost, operational effort.

### Architecture Decision Records (ADR)

When a decision is significant, hard to reverse or likely to be questioned, record it. Follow the repository's ADR format and location if one exists. Otherwise use:

```markdown
# ADR-<number>: <decision title>

## Status
Proposed / Accepted / Superseded by ADR-<n>

## Context
The forces at play: requirements, constraints, current state.

## Decision
What was decided.

## Alternatives Considered
Each option and why it was not chosen.

## Consequences
Benefits, costs, risks, and what becomes easier or harder.
```

## Rules

- Reason from the requirements and constraints provided. Do not recommend a pattern because it is popular.
- Do not define one "correct" architecture when several designs reasonably satisfy the requirements. Present the trade-offs and state what would favor each.
- Base statements about the current system on evidence. Mark everything else as an assumption.
- Do not invent metrics, load numbers, costs or system details.
- Favor the simplest design that meets the ranked requirements. Every added component (service, broker, cache) must justify its operational cost.
- Prefer incremental, reversible migrations over big-bang rewrites.
- Address failure scenarios, security and observability explicitly. Do not leave them as afterthoughts.
- Identify bottlenecks from data, not intuition, and recommend measuring where data is missing.
- Respect existing decisions and conventions unless there is a stated reason to change them.
- Do not draw architecture diagrams unless there is enough information to draw them accurately. A simple text outline of known components is fine. Do not invent components.
- List open questions instead of guessing.
- Never expose secrets or credentials found in the repository.

## Output

```markdown
# Architecture Analysis

## Problem

## Requirements

Functional and non-functional, labeled. Assumptions marked.

## Constraints

## Current State

## Quality Attributes

Ranked by importance for this problem.

## Options

## Trade-offs

## Recommended Architecture

Or, if several options fit, the trade-off and what would decide it.

## Components

## Data Flow

## Failure Scenarios

## Security

## Observability

## Deployment

## Migration Plan

## Risks

## Open Questions
```

Omit or shorten a section when it does not apply, and say why.

## Examples

Illustrative only.

**Question:** "Should we split our modular monolith into microservices?"

**Response (abridged):**

```markdown
## Requirements and Constraints

- Requirement (stated): the reporting module needs to scale independently of the rest.
- Constraint (stated): 8 engineers, one deployment pipeline.
- Assumption: traffic growth is moderate. Not confirmed.

## Options

1. Keep the modular monolith and tighten module boundaries.
2. Extract only the reporting module as a separately scaled worker.
3. Split into many services.

## Trade-offs

- Option 3 solves the scaling need but adds deployment, networking, data ownership and on-call overhead for a team of 8, and goes well beyond the one module that needs it.
- Option 2 addresses the stated scaling need with limited new operational surface, but needs a clean boundary and a decision on how it gets data.
- Option 1 is cheapest, but does not give independent scaling.

## Recommendation

Option 2, if the reporting load is confirmed as the driver. Option 1 is reasonable if measurements show the load fits the current deployment.

## Open Questions

What are the load figures for the reporting module? Can it work from a replica or a snapshot?
```

## Related Skills

- [`api-development`](../api-development/SKILL.md): design the contracts at the boundaries this skill defines.
- [`database-sql`](../database-sql/SKILL.md): detailed schema, query and transaction design.
- [`refactoring`](../refactoring/SKILL.md): carry out local restructuring that follows from an architectural decision.
- [`code-review`](../code-review/SKILL.md): check that an implementation respects the chosen architecture.
