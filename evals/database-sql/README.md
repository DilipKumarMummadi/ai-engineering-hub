# Database & SQL Evaluations

Evaluations for the [`database-sql`](../../.claude/skills/database-sql/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the skill produces correct SQL, reasons about performance from evidence, and treats data-changing operations with the required care.

## Evaluation Principles

- Correctness comes before optimization.
- The schema and data given are inspected before assumptions are made.
- Join grain, duplicate rows and NULL behavior are considered.
- Index and performance advice follows from the query pattern, selectivity, existing indexes, plan and workload, including write cost.
- Destructive operations are labeled, previewed, scoped and made reversible, and are not executed without authorization.
- Engine-specific behavior is identified as such.
- No results, row counts or timings are invented.

## Expected Behavior

A good response explains what the data and query really do, finds the correctness or performance problem from the facts given, proposes a targeted fix, says how to verify it, and clearly separates what was and was not run.

## Common Failure Modes

- Fixing duplicates with `DISTINCT` instead of correcting the join grain.
- Recommending an index without checking selectivity, existing indexes or write overhead.
- Claiming a speedup with no plan or measurement.
- Ignoring NULL semantics.
- Giving an `UPDATE` or `DELETE` with no preview, scope, transaction or rollback plan.
- Presenting a made-up execution result.
- Mixing PostgreSQL-specific behavior into generic advice.

## Qualitative Evaluation

Outcomes are Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [duplicate-join](cases/duplicate-join.md) | Finds a join fan-out that inflates an aggregate and fixes the grain. |
| [slow-query](cases/slow-query.md) | Reasons about a slow query from the plan, selectivity and write workload before indexing. |
| [unsafe-update](cases/unsafe-update.md) | Handles a destructive update safely, including NULL behavior. |
