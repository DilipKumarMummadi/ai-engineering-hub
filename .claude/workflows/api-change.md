---
name: api-change
description: Design, implement and validate a new or changed API, assessing contract, compatibility, security and persistence impact before implementation. Use for API additions and changes; not for general feature work or purely internal refactors.
---

# API Change Workflow

## Purpose

Deliver an API addition or change with a deliberate contract, a compatibility decision, and evidence of correct behavior. The workflow orchestrates existing agents and skills. The API design reasoning stays in the `api-development-agent`; this workflow decides what runs around it and what must be true before moving on.

## When to Use

- A new endpoint or resource is added.
- An existing request, response, status code, error shape, authentication or pagination behavior changes.
- An API has consumers who could be affected by the change.

## When NOT to Use

- The API is one part of a larger feature. Use [feature-development](feature-development.md), which routes the API part here or to `api-development-agent`.
- A failing endpoint needs diagnosis. Use [bug-fix](bug-fix.md).
- The change is only a schema change. Use [database-change](database-change.md).
- Only a code review of an API change is needed. Use [pr-preparation](pr-preparation.md) or `/review`.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The requirement: what the API must do and for whom | Required | |
| Existing API: code, contract or specification | Gathered | |
| Known consumers and their constraints | Preferred | Determines compatibility needs. |
| Authentication and authorization model | Preferred | |
| Constraints: versioning policy, technology, deadlines | Optional | Carried unchanged into every stage. |

Unknown consumers are reported as unknown, not assumed to be absent.

## Stages

Each stage follows the lifecycle in the [Workflow Specification](../../docs/workflow-specification.md).

| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Requirement | | Workflow (asks the user) | Outcome, consumers, constraints | Never |
| 2 | Existing API Analysis | 1 | `api-development-agent` (`/api`) | Current contract, conventions, consumers found | New API in an area with no existing API |
| 3 | Contract Design | 1, 2 | `api-development-agent` | Proposed contract: resources, methods, schemas, errors | Never |
| 4 | Compatibility Assessment | 2, 3 | `api-development-agent` | Breaking/non-breaking classification, versioning or migration approach | Brand-new API with no consumers |
| 5 | Security Assessment | 3 | `security` skill via `api-development-agent` | Authentication, authorization and data exposure findings | Never for state-changing or data-returning endpoints; skip for an internal change that touches no access or data |
| 6 | Persistence Assessment | 3 | `database-troubleshooting-agent` (`/database`) | Schema and query impact | The API change does not touch storage |
| 7 | Implementation | 3-6 | The engineer or the AI, with go-ahead | Working-tree changes | Never |
| 8 | Testing | 3, 7 | `test-planning-agent` (`/test-plan`); `testing` skill | Contract, negative and compatibility tests, run output | Never |
| 9 | Documentation | 3, 7 | Workflow; contract documentation produced from the design | Updated API docs or specification | No documented contract exists and none is required |
| 10 | Review | 7-9 | `pr-review-agent` (`/review`) | Review findings | Never |
| 11 | Validation | 7-10 | Workflow; test execution | Evidence of a passing, compatible change | Never |

Stage 4 may force a return to stage 3 if the design is breaking and a compatible form is required.

## Commands

| Command | Serves stage |
| --- | --- |
| [`/api`](../commands/api.md) | 2-5 |
| [`/database`](../commands/database.md) | 6 |
| [`/test-plan`](../commands/test-plan.md) | 8 |
| [`/review`](../commands/review.md) | 10 |

## Agents

| Agent | Role | Stage | Used when |
| --- | --- | --- | --- |
| [api-development-agent](../agents/api-development-agent.md) | Primary | 2-5, 7 | Always |
| [architecture-agent](../agents/architecture-agent.md) | Supporting | 3, 4 | The change crosses service boundaries or introduces an integration pattern |
| [database-troubleshooting-agent](../agents/database-troubleshooting-agent.md) | Supporting | 6 | The change touches persistence |
| [test-planning-agent](../agents/test-planning-agent.md) | Supporting | 8 | Always for behavior changes |
| [pr-review-agent](../agents/pr-review-agent.md) | Supporting | 10 | Always |

## Skills

Applied through the agents above.

- [`api-development`](../skills/api-development/SKILL.md): through the primary agent.
- [`security`](../skills/security/SKILL.md): stage 5.
- [`database-sql`](../skills/database-sql/SKILL.md): stage 6, through the database agent.
- [`testing`](../skills/testing/SKILL.md), [`code-review`](../skills/code-review/SKILL.md): stages 8 and 10.
- [`performance`](../skills/performance/SKILL.md), [`reliability`](../skills/reliability/SKILL.md): only if the requirement names latency, volume, retries or idempotency concerns.

## Decision Points

| If | Then |
| --- | --- |
| The change is breaking for known consumers | Require a versioning or migration decision from the user before stage 7 |
| Consumers are unknown | Treat the change as potentially breaking and say so |
| The change touches persistence | Run stage 6; if it needs a migration, route that part to [database-change](database-change.md) |
| The endpoint returns or changes sensitive data | Stage 5 is mandatory and not reduced |
| The change crosses service boundaries | Add `architecture-agent` to stages 3-4 |
| No existing API | Skip stages 2 and 4 |
| The change is internal with no contract change | Skip stages 3, 4, 9 and recommend a smaller path |

## Validation

- **Stage validation:** the contract (stage 3) must be specific enough to implement and test. The compatibility result (stage 4) must name the affected consumers or state they are unknown.
- **Final validation:** tests cover success, validation failure, authorization failure, and compatibility where it applies; tests were run and the output seen; documentation matches the implemented contract.
- **Evidence:** test output, contract diffs, review findings.
- **Rollback:** state how to revert or disable the change, and whether consumers could already depend on it.

## Safety

| Stage | Kind |
| --- | --- |
| 1-6, 9 (drafting), 10 | Analysis and planning |
| 7 | Modification, with the user's go-ahead |
| 8, 11 | Modification (tests) and local execution |

- Removing or changing a published endpoint, field or status code is treated as potentially breaking and needs explicit confirmation.
- Schema migrations, deployments, gateway or infrastructure changes, and credential or permission changes need explicit authorization and are never executed by this workflow on its own.
- Do not expose secrets or personal data from examples or logs.

## Output

An API change report: requirement, contract, compatibility classification, security and persistence findings, implementation summary, tests and results, documentation changes, review findings, stages skipped with reasons, and open risks. Reported **complete** only when required stages completed.

## Handoff

- To [database-change](database-change.md) for a required migration.
- To [pr-preparation](pr-preparation.md) with contract diff, test evidence and compatibility notes.
- To `architecture-agent` if the change exposes a boundary problem.

## Examples

**Request:** "Add `PATCH /customers/{id}` to update the phone number."

Stages 1-5, 7-11. Stage 6 is skipped only if the phone field already exists. Stage 4 is light: additive and non-breaking.

**Request:** "Change `GET /orders` to use cursor pagination."

Stage 4 marks the change breaking. The workflow stops before stage 7 and asks the user for a versioning or dual-support decision.

## Related Workflows

- [feature-development](feature-development.md): the broader workflow that may include an API change.
- [database-change](database-change.md): for persistence changes.
- [pr-preparation](pr-preparation.md): the usual next step.
