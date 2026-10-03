---
name: database-change
description: Plan, implement and validate a database schema, data or query change, with migration design, impact assessment and rollback planning. Destructive operations require explicit authorization. Use for database changes; not for diagnosing a slow or failing query alone.
---

# Database Change Workflow

## Purpose

Deliver a database change safely: understand the current schema and data, design the migration, assess impact on queries, performance, concurrency and security, validate it, and plan rollback before anything irreversible runs. The workflow orchestrates existing agents and skills. The SQL and schema reasoning stays in the `database-troubleshooting-agent`.

## When to Use

- A table, column, index, constraint or view is added, changed or removed.
- Data is migrated, backfilled or corrected.
- A query change has significant performance or correctness impact.
- An ORM model change implies a schema change.

## When NOT to Use

- A query is slow or wrong and nothing is to be changed yet. Use `/database` with the `database-troubleshooting-agent` directly.
- Production is currently failing because of the database. Use [production-incident](production-incident.md).
- The change is an API contract change with no storage impact. Use [api-change](api-change.md).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The requirement and the reason for the change | Required | |
| Database engine and version | Required | Engine differences change the design. |
| Current schema, relevant queries, ORM models | Gathered | |
| Data volume, growth, traffic patterns, maintenance windows | Preferred | |
| Environment: which database the change targets | Required before any execution | |
| Constraints: downtime limits, compatibility, prohibitions | Optional | Carried unchanged into every stage. |

Unknown volumes or usage are reported as unknown. No row counts, plans or timings are invented.

## Stages

Each stage follows the lifecycle in the [Workflow Specification](../../docs/workflow-specification.md).

| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Requirement | | Workflow (asks the user) | Outcome, engine, environment, constraints | Never |
| 2 | Schema Analysis | 1 | `database-troubleshooting-agent` (`/database`) | Current structure, constraints, dependencies | Never |
| 3 | Existing Data Analysis | 2 | `database-troubleshooting-agent` (read-only queries) | Data shape, nulls, duplicates, volume, risks for the change | New empty table or column with no existing data |
| 4 | Migration Design | 2, 3 | `database-troubleshooting-agent` | Migration steps, ordering, compatibility with running code | Never |
| 5 | Query / Code Impact | 4 | Repository reading; `api-development-agent` if an API is affected | Affected queries, models and consumers | The change is isolated and no code uses the object |
| 6 | Performance Assessment | 4, 5 | `database-sql` and `performance` skills via the agent | Index, lock and plan implications | Small tables and no new query patterns |
| 7 | Transaction / Concurrency Assessment | 4, 5 | `database-troubleshooting-agent` | Locking, isolation and deploy-time concurrency risks | A single additive change with no concurrent writers at risk |
| 8 | Security Assessment | 4 | `security` skill | Permissions, exposure, sensitive-data findings | The change touches no sensitive data, permissions or access paths |
| 9 | Implementation | 4-8 | The engineer or the AI, with go-ahead | Migration scripts and code changes in the working tree. Not executed. | Never |
| 10 | Validation | 9 | `test-planning-agent` (`/test-plan`); local or disposable database only | Migration and query test results on a non-production database | Never |
| 11 | Rollback Planning | 4, 9 | `database-troubleshooting-agent` | Rollback or forward-fix plan, backup and restore considerations | Never for anything that alters or removes data or structure |
| 12 | Review | 9-11 | `pr-review-agent` (`/review`) | Review findings | Never |

Execution against a shared or production database is **not a stage of this workflow**. It is a separate step that needs explicit authorization after stages 10-12.

## Commands

| Command | Serves stage |
| --- | --- |
| [`/database`](../commands/database.md) | 2-4, 7, 11 |
| [`/api`](../commands/api.md) | 5, when an API is affected |
| [`/test-plan`](../commands/test-plan.md) | 10 |
| [`/review`](../commands/review.md) | 12 |

## Agents

| Agent | Role | Stage | Used when |
| --- | --- | --- | --- |
| [database-troubleshooting-agent](../agents/database-troubleshooting-agent.md) | Primary | 2-4, 6, 7, 11 | Always |
| [architecture-agent](../agents/architecture-agent.md) | Supporting | 4 | The change affects service ownership of data, replication or multi-service consistency |
| [api-development-agent](../agents/api-development-agent.md) | Supporting | 5 | An API exposes the changed data |
| [test-planning-agent](../agents/test-planning-agent.md) | Supporting | 10 | Always |
| [pr-review-agent](../agents/pr-review-agent.md) | Supporting | 12 | Always |

## Skills

Applied through the agents above.

- [`database-sql`](../skills/database-sql/SKILL.md): through the primary agent.
- [`performance`](../skills/performance/SKILL.md): stage 6, when volume or query patterns make it relevant.
- [`security`](../skills/security/SKILL.md): stage 8.
- [`reliability`](../skills/reliability/SKILL.md): stages 7 and 11, for deployment ordering, backup and recovery.
- [`testing`](../skills/testing/SKILL.md), [`code-review`](../skills/code-review/SKILL.md): stages 10 and 12.

## Decision Points

| If | Then |
| --- | --- |
| The change drops, truncates or rewrites data or structure | Treated as destructive. Require explicit authorization and a verified backup or recovery path before any execution |
| The database engine is unknown | Stay in stage 1 and ask |
| Existing data violates a new constraint | Add a data-correction step to the design, requiring authorization |
| The change must be compatible with running code during deploy | Design for expand/contract ordering in stage 4; include stage 7 |
| An API exposes the changed data | Run stage 5 with `api-development-agent`, or route to [api-change](api-change.md) |
| The table is large or heavily used | Run stage 6 and 7 in full |
| Small, additive, isolated change | Skip stages 3, 6, 7 and 8 as the conditions allow |

## Validation

- **Stage validation:** the migration design states its ordering and compatibility with the running application; the rollback plan corresponds to the actual migration.
- **Final validation:** migration and application tests ran on a non-production database with output seen; queries that use the changed objects were checked; rollback was reviewed; review blockers are resolved.
- **Evidence:** schema diffs, migration output, test output, query plans if performance is a concern. Data counts and timings come from real runs only.
- **Rollback:** required. For irreversible changes, state that and state the recovery path, such as a verified backup.

## Safety

| Stage | Kind |
| --- | --- |
| 1-8, 11, 12 | Analysis and planning. Data reads are read-only. |
| 9 | Modification of files in the working tree (migration scripts, code). Scripts are not run. |
| 10 | Execution on a local or disposable database only |
| Any run against a shared, staging or production database | Execution. Explicit, specific authorization required. |

- **Destructive operations** (`DROP`, `TRUNCATE`, `DELETE` or `UPDATE` without a verified scope, column or type changes that lose data, irreversible migrations) **require explicit authorization**, naming the action and the environment. A plan or a review does not grant it.
- Stage 3 queries are read-only, limited in size, and avoid exposing personal data.
- No migration is run on production by this workflow. Deployments and manual production SQL are outside its authority.
- Credentials and connection strings are never written to files or output.

## Output

A database change report: requirement, schema and data findings, migration design, impact on queries and code, performance and concurrency assessment, security findings, implementation summary, validation results and the environment they ran in, rollback plan, review findings, stages skipped with reasons, and the authorization still needed for execution. Reported **complete** only when required stages completed, and never as "applied" unless the migration was actually run with authorization and the result seen.

## Handoff

- To the user, for the authorization decision on executing the migration.
- To [pr-preparation](pr-preparation.md) with migration scripts, validation evidence and rollback plan.
- To [api-change](api-change.md) if the contract changes as a consequence.
- To [production-incident](production-incident.md) if a production problem is discovered.

## Examples

**Request:** "Add a nullable `archived_at` column to `orders`."

Small and additive. Stages 1, 2, 4, 5, 9-12 run. Stages 3, 6, 7 and 8 are skipped with reasons. Validation runs on a local database.

**Request:** "Drop the `legacy_status` column."

Destructive. The workflow finds its users (stage 5), designs a staged removal, plans rollback with a backup, and stops at an authorization request before any execution.

## Related Workflows

- [api-change](api-change.md), [feature-development](feature-development.md).
- [production-incident](production-incident.md): for live database failures.
- [pr-preparation](pr-preparation.md).
