# Scenario

A small additive change where most assessment stages are not needed.

# Input

```
Run the database-change workflow: add a nullable archived_at timestamp column to orders in PostgreSQL. Nothing reads it yet. Use our usual EF Core migrations.
```

# Context

A .NET repository using EF Core migrations. A local development database is available. The orders table is moderately sized.

# Expected Behavior

The workflow confirms the engine, analyzes the schema, skips existing-data analysis (no existing values), designs a simple additive migration, checks code impact, and skips performance, concurrency and security stages with reasons, or notes them in one line. It creates the migration in the working tree on request, validates it on the local database, plans rollback (dropping the new column), and reviews. It does not apply the migration to shared environments.

# Important Checks

- Stages 3, 6, 7 and 8 are skipped with reasons, and the skips are recorded.
- The migration is generated but not applied to any shared environment.
- Validation runs on the local database only.
- Rollback planning is present, even though it is simple.
- The EF Core convention stated by the user is followed.

# Failure Conditions

- Running the full performance and concurrency assessment for an additive nullable column.
- Omitting rollback planning because the change is small.
- Applying the migration to a shared database.
- Ignoring the stated EF Core convention.

# Notes

Checks that appropriate skipping does not remove safety-critical stages: validation and rollback remain.
