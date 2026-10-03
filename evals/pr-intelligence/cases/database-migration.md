# Scenario

A migration adds a column and an index on a large table.

# Input

/pr-intelligence Is this migration PR ready?

# Context

PR description: "Add `region` to orders and index it."

`db/migrations/0060_region.sql`:

```sql
ALTER TABLE orders ADD COLUMN region text NOT NULL DEFAULT 'EU';
CREATE INDEX idx_orders_region ON orders (region);
```

- The repository documents PostgreSQL 14. The runbook says `orders` has about 50 million rows and takes steady writes.
- The migration runner wraps each file in a transaction.
- No rollback script. `OrderRepository.cs` adds one query filtering on `region`.
- Integration tests exist for the repository and were not updated.

# Expected Behavior

The report selects `code-review`, `database-sql`, `reliability` and `testing`, and `performance` because the index and query behavior on a large table are at issue. It does not flag the constant-default `ADD COLUMN` as a table rewrite on PostgreSQL 14. It identifies that `CREATE INDEX` without `CONCURRENTLY` blocks writes for the duration of the build, which is a risk shown by the migration itself and the documented size, and that the transactional wrapper prevents a concurrent build as written. It reports the missing rollback and the un-updated tests. It separates the index build (a confirmed blocker if the size and write rate are accepted as documented, otherwise a potential risk) from the rest. Readiness is Needs Changes.

# Important Checks

- The `ADD COLUMN` default is not a false alarm.
- The blocking index build is found with its evidence.
- Engine-specific claims are tied to the documented engine.
- Nothing is executed against a database.

# Failure Conditions

- Flagging the column default as a rewrite.
- Missing the blocking build or the missing rollback.
- Running the migration, or inventing table statistics.

# Notes

Mirrors a well-known false alarm and a real risk.
