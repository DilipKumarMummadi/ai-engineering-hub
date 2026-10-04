---
name: api-change
description: Take an API requirement through existing-API analysis, contract design, compatibility and security analysis, persistence impact, implementation and API tests to a reviewed change, stopping for approval on breaking changes. Use for adding or changing an API; not for whole features, database-only changes or bugs.
---

# API Change Workflow

## Purpose

Deliver an API addition or change with a defined contract, known compatibility impact, security considered and tests that prove the behavior. The workflow orchestrates existing agents, skills and commands. Shared mechanics (context, evidence, capabilities, testing, review, states, output, safety) are in [Workflow Common Guidance](../../docs/workflow-common.md) and are not repeated here.

## When to Use

- An endpoint, request/response contract, error model or API behavior is added or changed.
- An API change has compatibility, security or persistence implications.

## When NOT to Use

- A full feature with UI, jobs and more. Use [feature-development](feature-development.md).
- A schema or data change only. Use [database-change](database-change.md).
- An existing API misbehaves. Use [bug-fix](bug-fix.md).
- A local edit that changes no contract. Make the edit.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The API requirement and intended consumers | Required | |
| Existing API definition, controllers, OpenAPI spec | Preferred | Found in the repository if not supplied. |
| Compatibility expectations, versioning policy | Preferred | |
| Ticket key or link | Optional | Only from the user or reliable evidence; never guessed. |
| Constraints: technology, deadline, scope | Optional | Carried unchanged into every stage. |

Missing inputs are identified, not invented.

**External sources (optional).** Detection and fallback, including the exact fallback sentences, are in [Workflow Common Guidance](../../docs/workflow-common.md#4-mcp-capability-detection-and-fallback).

| Capability | Used for | Stage |
| --- | --- | --- |
| `requirements-tracking` | Requirement, acceptance criteria | 1 |
| `source-control` | Existing consumers, related code and pull requests | 2, 12 |
| `database` | Read-only schema inspection for persistence impact | 7 |

## Project Context

Follow [Project Context Consumption](../../docs/project-context-consumption.md). This workflow adds no context-loading stage; stage 3 records the context state.

```
Requirement → Existing API → Context Check → Contract → Compatibility → Security → Persistence → Implementation → Tests
```

Stages 2, 4 and 5 use the API conventions, versioning and authentication model. Stage 7 uses the database. Stage 9 uses the testing approach. Repository evidence wins over stale context.

## Stages

Each stage follows the lifecycle in the [Workflow Specification](../../docs/workflow-specification.md).

| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Requirement | | Workflow; `requirements-tracking` if connected | Requirement, consumers, constraints as Confirmed / Inferred / Unknown | Never |
| 2 | Existing API Analysis | 1 | `api-development-agent` (`/api`) | Current contract, conventions, consumers, related code | Greenfield API with no neighbors |
| 3 | Context Check | 1, 2 | Workflow | Context state: present, missing, stale or declined | Never (recorded even if absent) |
| 4 | API Contract | 1-3 | `api-development-agent`; `api-development` | Proposed contract: resources, HTTP semantics, validation, errors, pagination/filtering/sorting, idempotency, documentation | Never |
| 5 | Compatibility Analysis | 2, 4 | `api-development-agent`; `architecture` where boundaries change | Breaking vs non-breaking verdict, versioning approach, affected consumers | The API is new and has no consumers |
| 6 | Security | 4 | `api-development-agent`; `security` | Authentication, authorization and data exposure findings | The change touches none of the security triggers |
| 7 | Database / Persistence Impact | 4 | `database-sql`; `database` read-only if connected | Schema, query, transaction and concurrency impact | No persistence is involved |
| 8 | Implementation | 4-7, PLAN_READY | The engineer or the AI, with go-ahead | Working-tree changes, inspected | Never |
| 9 | API Tests | 4, 8 | `test-planning-agent` (`/test-plan`); `testing` | Tests added or updated and executed results | Never for behavior changes |
| 10 | Change Intelligence | 8, 9 | `change-intelligence-agent` (`/change-impact`); `change-intelligence` | Impact on consumers, contracts, data, Confirmed / Inferred / Unknown | Never |
| 11 | Code Review | 8-10 | `pr-review-agent` (`/review`); `code-review` | Prioritized findings | Never before a PR |
| 12 | PR Intelligence | 11, a PR exists | `pr-intelligence-agent` (`/pr-intelligence`) | Readiness: READY, NEEDS_CHANGES or NEEDS_INFORMATION | No PR exists or no `source-control` |

Findings from stages 10-12 that require changes return to stage 8. Stage notes:

- **4 Contract.** Evaluates HTTP method semantics, request/response shape, validation, error model, authentication, authorization, pagination, filtering, sorting, idempotency, concurrency (for example ETags), timeout and retry behavior, and documentation. The agent and skill own the how; the workflow requires the result.
- **5 Compatibility.** A change is breaking if an existing consumer could fail (removed or renamed field, changed type, stricter validation, changed status code or semantics). A breaking change stops at NEEDS_HUMAN_APPROVAL.
- **8 Implementation.** No code is changed until the contract is agreed and PLAN_READY is confirmed. Follow repository conventions; add no unnecessary abstraction.

## Commands

| Command | Serves stage |
| --- | --- |
| [`/api`](../prompts/api.prompt.md) | 2, 4-6 |
| [`/test-plan`](../prompts/test-plan.prompt.md) | 9 |
| [`/change-impact`](../prompts/change-impact.prompt.md) | 10 |
| [`/review`](../prompts/review.prompt.md) | 11 |
| [`/pr-intelligence`](../prompts/pr-intelligence.prompt.md) | 12 |

## Agents

| Agent | Role | Stage | Used when |
| --- | --- | --- | --- |
| [api-development-agent](../agents/api-development-agent.md) | Primary | 2, 4-6 | Always |
| [test-planning-agent](../agents/test-planning-agent.md) | Supporting | 9 | Behavior changes |
| [change-intelligence-agent](../agents/change-intelligence-agent.md) | Supporting | 10 | Always |
| [pr-review-agent](../agents/pr-review-agent.md) | Supporting | 11 | Always before a PR |
| [pr-intelligence-agent](../agents/pr-intelligence-agent.md) | Supporting | 12 | A PR exists and `source-control` is available |

## Skills

Applied through the agents, or directly when no agent fits the stage.

- [`api-development`](../skills/api-development/SKILL.md), [`testing`](../skills/testing/SKILL.md), [`change-intelligence`](../skills/change-intelligence/SKILL.md), [`code-review`](../skills/code-review/SKILL.md): core.
- [`security`](../skills/security/SKILL.md): stage 6 and review.
- [`database-sql`](../skills/database-sql/SKILL.md): when persistence changes.
- [`performance`](../skills/performance/SKILL.md), [`reliability`](../skills/reliability/SKILL.md): with volume, latency, retry or availability requirements.
- [`architecture`](../skills/architecture/SKILL.md): when a service boundary or integration pattern is affected.

## Decision Points

| If | Then |
| --- | --- |
| Requirement is insufficient | NEEDS_INFORMATION; stay in stage 1 and ask |
| Project Context missing or stale | Continue on repository evidence; repository wins |
| The change is breaking | NEEDS_HUMAN_APPROVAL; present options (new version, additive change, deprecation) |
| The API is new with no consumers | Skip stage 5 |
| The change touches authn/authz, user input, uploads, secrets or sensitive data | Run stage 6; it finishes before review |
| Persistence changes | Run stage 7; route schema work to [database-change](database-change.md) |
| Result sets may be large | Contract covers pagination, filtering and sorting; add `performance` |
| Writes may be retried or concurrent | Contract covers idempotency and concurrency; add `reliability` |
| Tests fail | Return to stage 8 or report; the result cannot be READY |
| No PR exists | Skip stage 12 and say why |

## Validation

- **Stage:** a contract is not done without stated error cases and compatibility verdict. Tests are not done unless executed.
- **Final:** contract tests and existing API tests pass with output seen, each acceptance criterion maps to evidence, review blockers are resolved. See [Workflow Common Guidance](../../docs/workflow-common.md#9-final-validation).
- **Evidence:** test output, diffs, OpenAPI differences, review findings. "Not run" is reported as such.
- **Rollback:** state how the change is reverted or versioned out; a breaking change needs a consumer migration path.
- **Failures** are reported per [Workflow Common Guidance](../../docs/workflow-common.md#13-failure-reporting). Unavailable capabilities degrade to repository evidence.

## Safety

| Stage | Kind |
| --- | --- |
| 1-7, 10-12 | Analysis and planning. Database access is read-only. |
| 8 | Modification. Needs go-ahead after PLAN_READY; a breaking change needs explicit approval. |
| 9 | Modification (tests) and local test execution |

Migrations, deployments, consumer notifications, pushing a PR and production changes are never performed by this workflow. Checkpoints and prohibitions are in [Workflow Common Guidance](../../docs/workflow-common.md#12-human-checkpoints-and-safety).

## Output

The report uses the [common output contract](../../docs/workflow-common.md#10-output-contract) (Objective through Recommendation) and the [workflow states](../../docs/workflow-common.md#11-workflow-states). Findings include the contract summary, the compatibility verdict and security findings. Completion follows the common rule: COMPLETED only when required stages completed.

## Handoff

- To [database-change](database-change.md) for schema work.
- To [pr-preparation](pr-preparation.md) and [pr-intelligence](pr-intelligence.md) with the contract, compatibility verdict, test evidence and review outcome.
- To [feature-development](feature-development.md) when the API is part of a larger feature.
- To the user, with the open questions or the breaking-change decision, when blocked.

## Examples

**Request:** "Add `GET /orders/{id}/invoice` returning a PDF."

Stages 1-4, 6 (customer data), 8-11; stage 5 skipped (new endpoint), stage 7 skipped (no schema change). Stage 12 only if a PR exists.

**Request:** "Rename `customerName` to `name` in the order response."

Stage 5 finds a breaking change and stops at NEEDS_HUMAN_APPROVAL with options before any implementation.

## Related Workflows

- [feature-development](feature-development.md): when the API is part of a feature.
- [database-change](database-change.md): persistence work.
- [bug-fix](bug-fix.md): when an existing API is wrong.
- [pr-preparation](pr-preparation.md), [pr-intelligence](pr-intelligence.md): the usual next workflows.
