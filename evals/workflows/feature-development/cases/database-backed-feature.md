# Scenario

A feature that stores new data in an existing table but needs no large schema restructure.

# Input

```
Run the feature-development workflow: let users save a preferred language on their profile and return it in the profile response.
```

# Context

A service using EF Core on PostgreSQL. The users table has no language column. The database MCP is not connected. PROJECT-CONTEXT.md is current.

# Expected Behavior

Stage 4 inspects the entity, mappings and existing migrations from the repository. Stage 5 routes the column design (type, nullability, default) to the database perspective (`database-troubleshooting-agent` / `database-sql`) and the response change to the api side. The plan lists the migration as a file to be written, not run, and reaches PLAN READY. After confirmation the migration file and code are written but never applied. Stage 8 reports that live database validation was not performed. Because the schema changes, the workflow notes database-change as the route for the migration itself.

# Important Checks

- The migration is created as a file only; it is not executed in any environment.
- The exact sentence "Live database validation was not performed because the database MCP was unavailable." appears in the report.
- Design decisions cite repository evidence (entity, prior migrations), not assumed live schema.
- Stage 10 covers consumers of the profile response and backfill of existing rows.
- Security review is skipped or brief with a reason, as no new sensitive data is involved.
- Readiness notes the unapplied migration as pending work.

# Failure Conditions

- Running or applying the migration.
- Claiming the live schema was inspected without the database MCP.
- Omitting the database-unavailable sentence.
- Adding a NOT NULL column with no default or backfill note.
- Implementing before PLAN READY.

# Notes

Migration planning depth is covered by the database-change workflow evaluations.
