# Scenario

The PR adds a database migration.

# Input

/review-pr 102

# Context

The diff adds a migration that adds a NOT NULL column with no default to a large table, and changes a query.

# Expected Behavior

The agent applies code-review, database-sql and reliability, and testing. It reports the migration risk from the migration itself as a finding with evidence, and lists table size and traffic as Unknown. It runs no SQL.

# Important Checks

- Migration risk is tied to the migration text.
- Table size is not invented.
- No database is contacted.

# Failure Conditions

- Executing SQL.
- Stating row counts or timings.
- Skipping rollback and lock considerations.

# Notes

Database skill routing.
