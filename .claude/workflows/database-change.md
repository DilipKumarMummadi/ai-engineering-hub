---
name: database-change
description: Take a schema, data or query change from requirement through schema and data-impact analysis, migration design, application impact, validation, rollback analysis and review, stopping for authorization on destructive operations. Use for migrations and schema changes; not for general features, API-only changes or bugs.
---

# Database Change Workflow

## Purpose

Deliver a schema, data or query change that is safe to roll out: understood impact, a migration designed for safety and backward compatibility, validation, a rollback path and review. The workflow orchestrates existing agents, skills and commands. Shared mechanics (context, evidence, capabilities, testing, review, states, output, safety) are in [Workflow Common Guidance](../../docs/workflow-common.md) and are not repeated here.

## When to Use

- A table, column, index, constraint, view, migration or data change is needed.
- A query or persistence change has data, locking or performance implications.

## When NOT to Use

- A database symptom with an unknown cause. Use [bug-fix](bug-fix.md), or [production-incident](production-incident.md) if production is affected.
- An API-only change. Use [api-change](api-change.md).
- A full feature. Use [feature-development](feature-development.md).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The requirement and intended data outcome | Required | |
| Target database and engine (for example PostgreSQL, Oracle) | Preferred | Found in the repository if not supplied. |
| Data volume, availability and downtime constraints | Preferred | Unknown volume is reported as Unknown. |
| Ticket key or link | Optional | Only from the user or reliable evidence; never guessed. |
| Constraints: scope, deadline, prohibitions | Optional | Carried unchanged into every stage. |

Missing inputs are identified, not invented.

**Requirement readiness.** When a ticket key is supplied or the request is a new requirement, the `requirement-intelligence-agent` (`/requirement`) assesses it first, weighting schema and data requirements, migration, rollback, performance, transactions and concurrency, and testing. Only `READY` lets the workflow continue to migration design. `NEEDS_CLARIFICATION` or `BLOCKED` stops it with the blocking questions. Readiness does not authorize running a migration. The key is carried as the Requirement ID through the migration, tests and PR. See the [Readiness Policy](../../docs/requirement-readiness-policy.md).

**External sources (optional).** Detection and fallback, including the exact fallback sentences, are in [Workflow Common Guidance](../../docs/workflow-common.md#4-mcp-capability-detection-and-fallback).

| Capability | Used for | Stage |
| --- | --- | --- |
| `requirements-tracking` | Requirement, acceptance criteria | 1 |
| `database` (PostgreSQL) | Read-only live validation: schema, constraints, indexes, row counts, EXPLAIN | 2, 4, 6, 11 |
| `source-control` | Related code, migration history, pull requests | 2, 8, 16 |

- With the `database` capability, live use is read-only and the user names the environment; the Hub holds no connection details. Live findings are labeled as observed.
- Without it, analyze statically from EF Core models, migrations, SQL, repository code and schema definitions, and state: "Live database validation was not performed because the database MCP was unavailable."

## Project Context

Follow [Project Context Consumption](../../docs/project-context-consumption.md). This workflow adds no context-loading stage; stage 3 records the context state.

```
Requirement → Current Schema → Context Check → Data Impact → Migration Design → Application Impact → Validation → Rollback
```

Stages 2, 4 and 5 use the database technology, data ownership and migration tooling. Stage 8 uses deployment and operational constraints. Repository evidence wins over stale context.

## Stages

Each stage follows the lifecycle in the [Workflow Specification](../../docs/workflow-specification.md).

| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Requirement | | Workflow; `requirements-tracking` if connected | Requirement, constraints as Confirmed / Inferred / Unknown | Never |
| 2 | Current Schema Analysis | 1 | `database-troubleshooting-agent` (`/database`); `database-sql` | Current tables, constraints, indexes, migrations, usage; live if connected, else static | Never |
| 3 | Context Check | 1, 2 | Workflow | Context state: present, missing, stale or declined | Never (recorded even if absent) |
| 4 | Data Impact | 2, 3 | `database-troubleshooting-agent`; `database-sql` | Affected data, volume, NULLs, duplicates, integrity risks, Confirmed / Inferred / Unknown | The change adds an unused object with no existing data |
| 5 | Migration Design | 4 | `database-troubleshooting-agent`; `database-sql`; `architecture` for cross-service data | Migration steps, ordering, backward compatibility (expand/contract where needed), locking and transaction behavior | Never |
| 6 | Application Impact | 5 | `change-intelligence-agent` (`/change-impact`); `api-development-agent` (`/api`) if a contract changes | Code, queries, ORM mappings, APIs and jobs affected | No application code depends on the change |
| 7 | Performance | 4, 5 | `performance`; `database-sql` | Index, query-plan and migration-runtime impact | Small tables and no new query paths |
| 8 | Transaction / Concurrency | 5 | `reliability`; `database-sql` | Locking, isolation, concurrent-writer and rollout-overlap behavior | The change takes no locks and adds no write path |
| 9 | Security | 5, 6 | `security` | Data exposure, permissions, sensitive-data handling | The change touches no sensitive data or permissions |
| 10 | Implementation | 5-9, PLAN_READY | The engineer or the AI, with go-ahead | Migration and application changes in the working tree, inspected | Never |
| 11 | Migration Validation | 10 | `database` read-only if connected; otherwise static review | Evidence the migration is well-formed and safe; nothing is applied to a shared database | Never |
| 12 | Testing | 10, 11 | `test-planning-agent` (`/test-plan`); `testing` | Tests added or updated and executed results | Never for behavior changes |
| 13 | Rollback Analysis | 5, 10 | `database-troubleshooting-agent`; `reliability` | Rollback or roll-forward plan, data-loss implications | Never |
| 14 | Change Intelligence | 10-13 | `change-intelligence-agent` (`/change-impact`); `change-intelligence` | Impact of the resulting change, Confirmed / Inferred / Unknown | Never |
| 15 | Code Review | 10-14 | `pr-review-agent` (`/review`); `code-review` | Prioritized findings | Never before a PR |
| 16 | PR Intelligence | 15, a PR exists | `pr-intelligence-agent` (`/pr-intelligence`) | Readiness: READY, NEEDS_CHANGES or NEEDS_INFORMATION | No PR exists or no `source-control` |

Findings from stages 14-16 that require changes return to stage 10. Stage notes:

- **5 Migration Design.** Always considers migration safety, backward compatibility with the running application, locking, transactions, integrity, NULL behavior, duplicates, indexes and production rollout risk. The agent and skill own the how.
- **10 Implementation.** No code is written until the migration design is agreed and PLAN_READY is confirmed. The workflow writes migration files; it never applies them.
- **11 Migration Validation.** Live validation is read-only. Applying a migration to any shared or production database is Execution and needs explicit authorization.

## Commands

| Command | Serves stage |
| --- | --- |
| [`/database`](../commands/database.md) | 2, 4, 5, 13 |
| [`/api`](../commands/api.md) | 6 |
| [`/test-plan`](../commands/test-plan.md) | 12 |
| [`/change-impact`](../commands/change-impact.md) | 6, 14 |
| [`/review`](../commands/review.md) | 15 |
| [`/pr-intelligence`](../commands/pr-intelligence.md) | 16 |

## Agents

| Agent | Role | Stage | Used when |
| --- | --- | --- | --- |
| [database-troubleshooting-agent](../agents/database-troubleshooting-agent.md) | Primary | 2, 4, 5, 13 | Always |
| [change-intelligence-agent](../agents/change-intelligence-agent.md) | Supporting | 6, 14 | Application code depends on the change |
| [api-development-agent](../agents/api-development-agent.md) | Supporting | 6 | A contract changes |
| [test-planning-agent](../agents/test-planning-agent.md) | Supporting | 12 | Behavior changes |
| [pr-review-agent](../agents/pr-review-agent.md) | Supporting | 15 | Always before a PR |
| [pr-intelligence-agent](../agents/pr-intelligence-agent.md) | Supporting | 16 | A PR exists and `source-control` is available |

## Skills

Applied through the agents, or directly when no agent fits the stage.

- [`database-sql`](../skills/database-sql/SKILL.md), [`testing`](../skills/testing/SKILL.md), [`change-intelligence`](../skills/change-intelligence/SKILL.md), [`code-review`](../skills/code-review/SKILL.md): core.
- [`performance`](../skills/performance/SKILL.md), [`reliability`](../skills/reliability/SKILL.md), [`security`](../skills/security/SKILL.md): stages 7-9 and review, when they apply.
- [`architecture`](../skills/architecture/SKILL.md): when data ownership or service boundaries are affected.

## Decision Points

| If | Then |
| --- | --- |
| Requirement is insufficient | NEEDS_INFORMATION; stay in stage 1 and ask |
| Project Context missing or stale | Continue on repository evidence; repository wins |
| `database` capability unavailable | Static analysis; report the database fallback sentence; live findings stay Unknown |
| The change drops, truncates, renames or rewrites existing data or columns | NEEDS_HUMAN_APPROVAL; state effect, risk and undo before any work on that step |
| The change is not backward compatible with the running application | Redesign as expand/contract, or NEEDS_HUMAN_APPROVAL |
| The table is large or the migration takes locks | Stages 7 and 8 are required; propose a low-lock approach |
| A new query path or index is involved | Stage 7 required |
| The change is additive and the table is small or unused | Skip stages 7 and 8 |
| The API contract changes | Route that part to [api-change](api-change.md) |
| Tests fail | Return to stage 10 or report; the result cannot be READY |
| No PR exists | Skip stage 16 and say why |

### Human checkpoints

| Checkpoint | After | Meaning |
| --- | --- | --- |
| PLAN_READY | Stages 2-9 | Impact, migration design and rollback are agreed; required before any code change |
| NEEDS_HUMAN_APPROVAL | Any destructive or production-impacting step | Explicit authorization required before that step |

Other checkpoints follow [Workflow Common Guidance](../../docs/workflow-common.md#12-human-checkpoints-and-safety).

## Validation

- **Stage:** a migration design is not done without the backward-compatibility verdict and rollback. Tests are not done unless executed.
- **Final:** tests pass with output seen, the migration is validated (live read-only or static, labeled), rollback is defined, review blockers are resolved. See [Workflow Common Guidance](../../docs/workflow-common.md#9-final-validation).
- **Evidence:** schema definitions, migration files, query plans, test output. Live results exist only if a query ran; never fabricate database results.
- **Rollback:** required output of stage 13; irreversible steps are flagged and need explicit approval.
- **Failures** are reported per [Workflow Common Guidance](../../docs/workflow-common.md#13-failure-reporting). An unavailable database capability does not block static work.

## Safety

| Stage | Kind |
| --- | --- |
| 1-9, 13-16 | Analysis and planning. Database access is read-only. |
| 10 | Modification. Needs go-ahead after PLAN_READY. |
| 11 | Read-only validation; never applies a migration |
| 12 | Modification (tests) and local test execution |

- Applying migrations, DDL or DML to a shared, staging or production database, deleting data, deployments and infrastructure changes are never performed by this workflow without explicit, specific authorization and tooling support.
- Destructive operations state the effect, risk and way to undo before they are proposed. Checkpoints are in [Workflow Common Guidance](../../docs/workflow-common.md#12-human-checkpoints-and-safety).

## Output

The report uses the [common output contract](../../docs/workflow-common.md#10-output-contract) (Objective through Recommendation) and the [workflow states](../../docs/workflow-common.md#11-workflow-states). Findings include data impact, migration safety verdict, rollback plan and whether validation was live or static. Completion follows the common rule: COMPLETED only when required stages completed.

## Handoff

- To [api-change](api-change.md) when a contract changes.
- To [pr-preparation](pr-preparation.md) and [pr-intelligence](pr-intelligence.md) with the migration, rollback plan, test evidence and review outcome.
- To the user, with the open questions or the destructive-operation decision, when blocked.

## Examples

**Request:** "Add a nullable `nickname` column to `profiles`."

Stages 1-6, 10-15. Stages 4, 7, 8 skipped as the change is additive; stage 9 skipped (no sensitive data). No live validation unless `database` is connected.

**Request:** "Make `orders.email` NOT NULL and drop `legacy_code`."

Stages 1-9 all run. Dropping the column stops at NEEDS_HUMAN_APPROVAL. Backfill, NULL and duplicate risks are analyzed before implementation.

## Related Workflows

- [api-change](api-change.md): contract work.
- [feature-development](feature-development.md): when the change is part of a feature.
- [bug-fix](bug-fix.md), [production-incident](production-incident.md): database symptoms.
- [pr-preparation](pr-preparation.md), [pr-intelligence](pr-intelligence.md): the usual next workflows.
