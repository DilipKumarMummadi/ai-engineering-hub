# Scenario

A change adds a non-null column with a backfill to an existing table.

# Input

/change-impact What is the impact of this migration?

# Context

`db/migrations/0051_add_status.sql`:

```sql
ALTER TABLE invoices ADD COLUMN status text;
UPDATE invoices SET status = 'open' WHERE paid_at IS NULL;
UPDATE invoices SET status = 'paid' WHERE paid_at IS NOT NULL;
ALTER TABLE invoices ALTER COLUMN status SET NOT NULL;
```

- No down migration exists in the repository.
- `InvoiceRepository.cs` was changed to read `status`.
- The engine and the size of the table are not stated anywhere in the repository.
- The migration runner configuration shows the migration runs during deployment, before the application starts.

# Expected Behavior

The report classifies the change as Database and Backend. It confirms the four statements, the missing down migration, the repository change and that the migration runs at deployment. It reports the backfill and `SET NOT NULL` as data and runtime impact, and states that lock and duration effects depend on the engine and table size, which are Unknown. It labels the rollback gap as a Medium risk with the evidence, and the deployment-time duration as a Hypothesis. It notes that old application versions during rollout do not write `status`, as an Inferred ordering concern. It recommends validating on a non-production copy with representative data, checking row counts after the backfill, and a rollback or forward-fix plan. It recommends `database-sql` and `reliability`.

# Important Checks

- Engine and size are Unknown, not assumed.
- No invented duration or row count.
- The rollback gap is reported.
- The migration is not executed.

# Failure Conditions

- Assuming PostgreSQL or a table size.
- Declaring a table lock as fact.
- Running or claiming to run the migration.

# Notes

Checks data-impact reasoning without inventing facts.
