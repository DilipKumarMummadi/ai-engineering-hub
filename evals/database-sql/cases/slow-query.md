# Scenario

A PostgreSQL-backed .NET service shows a dashboard of recent pending jobs. The query has become slow as the table has grown. A developer wants to add indexes.

# Input

This query takes several seconds now. I'm going to add an index on every column in the WHERE and ORDER BY clauses. Is that right? What would you recommend?

# Context

Query:

```sql
SELECT id, customer_id, created_at
FROM jobs
WHERE status = 'pending'
ORDER BY created_at DESC
LIMIT 50;
```

Table and workload facts:

- `jobs` has about 20 million rows. About 0.5% of rows have `status = 'pending'`. The rest are `done` or `failed`.
- Existing indexes: the primary key on `id` and an index on `customer_id`.
- The service inserts about 500 rows per second, and job status changes from `pending` to `done` or `failed` shortly after insertion.
- The dashboard query runs about once per second.

Plan output provided by the developer (PostgreSQL `EXPLAIN (ANALYZE)` for the query on a production-like copy):

```
Limit (actual time=4210.5..4210.5 rows=50)
  -> Sort (Sort Key: created_at DESC)
       -> Seq Scan on jobs (actual rows=98412)
            Filter: (status = 'pending')
            Rows Removed by Filter: 19901588
Execution Time: 4213 ms
```

# Expected Behavior

The response reads the plan: the query scans all 20 million rows to find about 98 thousand pending ones and then sorts them, so the time is spent on the scan and the sort. It reasons about the query pattern and selectivity: the `status` filter is highly selective for `pending` (0.5%) but not for other values, and the query needs the newest 50 by `created_at`. It explains why separate single-column indexes are a poor fit: an index on `status` alone has poor selectivity for other values and would still need a sort, an index on `created_at` alone would scan newest rows across all statuses, and an index on every column adds write cost at 500 inserts per second with status updates. It recommends an index designed for this query, such as a partial index on `created_at` restricted to pending rows (or a composite index with `status` first then `created_at` descending), and explains why a partial index suits a small, hot subset: it is small, is cheap to maintain because rows leave it when they stop being pending, and serves the order and limit without sorting. It discusses write overhead and the fact that status updates will maintain it. It recommends verifying with the plan and timing after the change on representative data, building the index without blocking writes in production (`CREATE INDEX CONCURRENTLY` on PostgreSQL), and does not claim a specific speedup it has not measured. It notes that this applies to this query and that other queries need their own evidence.

# Important Checks

- The plan is read correctly (full scan, high rows removed, sort).
- Selectivity of the `pending` filter is used in the reasoning.
- Indexing every column is challenged, with reasons tied to the workload (write rate, status churn).
- A targeted index matching the filter and sort is proposed, with the trade-off explained.
- Write overhead is considered.
- Verification with the plan and timing is required, and no improvement is claimed without it.
- Production safety of the index build is considered, and the PostgreSQL-specific option is identified as such.
- The response does not fabricate a new plan or timing.

# Failure Conditions

- Agreeing to index every column.
- Recommending an index on `status` alone and expecting it to solve the problem.
- Ignoring the sort or the `LIMIT`.
- Ignoring write volume and status churn.
- Claiming a specific new execution time.
- Ignoring that the data is skewed and only 0.5% is pending.
- Suggesting a cache or hardware upgrade before looking at the query.
- Presenting PostgreSQL-only syntax as if it were valid everywhere.

# Notes

A composite index with `status` first and a partial index are both reasonable. The reasoning about selectivity, sort avoidance and write cost matters more than the exact choice.
