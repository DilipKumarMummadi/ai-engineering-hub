# Scenario

A developer opens a pull request that adds a `region` column to a large PostgreSQL table, creates an index on it, and adds a query for "latest orders in a region". The team asks the PR Review Agent to review it.

# Input

Please review this PR that adds regional filtering to the orders list.

# Context

PR description: "Add `region` to orders, index it, and add a regional orders list."

`Migrations/20250310_AddRegion.sql`:

```sql
ALTER TABLE orders ADD COLUMN region text NOT NULL DEFAULT 'EU';

CREATE INDEX idx_orders_region ON orders (region);
```

`Repositories/OrderRepository.cs` (new method):

```csharp
public Task<List<Order>> LatestByRegionAsync(string region) =>
    _db.Orders
        .Where(o => o.Region == region)
        .OrderByDescending(o => o.CreatedAt)
        .Take(50)
        .ToListAsync();
```

Facts:

- The database is PostgreSQL 14. The `orders` table has about 50 million rows and takes roughly 300 inserts per second, around the clock.
- There are three regions: `EU` (about 70% of rows), `US` (about 25%) and `APAC` (about 5%).
- The new query is the only use of `region`. It runs on every page load of the dashboard.
- The migration tool runs the SQL in a single transaction during deployment, and there is no rollback script in the PR.
- The repository already has a different index on `created_at`.
- The PR touches no authentication, authorization or API contract code.

# Expected Behavior

The agent reviews a database change. It selects `code-review` and `database-sql`, and adds `performance` because the index and query behavior are at issue on a very large table. It does not bring in `security`, `architecture`, `refactoring` or `api-development`, since the change does not touch them. The findings rest on the facts. It does not flag the `ADD COLUMN ... NOT NULL DEFAULT 'EU'` as a long table rewrite or lock problem, since in PostgreSQL 11 and later adding a column with a constant default is a metadata change (the agent should recognize this for version 14, or say it checked the version). It does find that `CREATE INDEX` without the concurrent option takes a lock that blocks writes to the table for the duration of the build, which on 50 million rows with 300 writes per second will stall inserts, and that the migration runs inside a transaction, which also prevents the concurrent build from being used as written. It reasons about index design: an index on `region` alone has low selectivity (three values), and the query needs the newest 50 orders in a region, so an index that matches both the filter and the sort order serves the query better than one on `region` only, with the cost of maintaining it at the write rate stated. It notes the missing rollback plan. It recommends verifying with the query plan on representative data, and does not claim a speedup. It does not claim to have run anything. It may suggest that the deployment step for the index be separated from the transactional migration.

# Important Checks

- `database-sql` and `performance` reasoning is applied; security, architecture and refactoring are not forced in.
- The `ADD COLUMN` with a constant default on PostgreSQL 14 is not reported as a blocking rewrite.
- The blocking index build on a hot table is identified, with the write rate and size as evidence.
- The in-transaction migration is noted as conflicting with a non-blocking build.
- Index design is reasoned from the selectivity, the filter, the sort and the write cost.
- The missing rollback is reported.
- Verification is by plan and measurement, with no invented numbers.
- The engine-specific behavior is identified as PostgreSQL-specific.
- Overlaps between database and performance findings are merged.

# Failure Conditions

- Flagging the `ADD COLUMN` default as a table rewrite on this PostgreSQL version.
- Missing the write-blocking index build.
- Recommending an index on `region` alone as sufficient without reasoning, or dismissing the index without reasoning.
- Adding security, architecture or refactoring commentary with no basis.
- Claiming a specific performance improvement.
- Inventing table statistics or plan output.
- Running or claiming to have run the migration or query.
- Ignoring the missing rollback.

# Notes

This case contains one well-known false alarm (the column default) and one real risk (the blocking index build). The agent is judged on telling them apart from the facts given.
