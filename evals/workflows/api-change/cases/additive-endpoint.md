# Scenario

A small additive endpoint on existing storage.

# Input

```
Run the api-change workflow: add GET /customers/{id}/preferences returning the existing preferences JSON column. Authenticated users can read their own preferences only.
```

# Context

An ASP.NET Core API with a customers table that already has a `preferences` column. Authentication is in place. No existing endpoint exposes the column. There are no known consumers because the endpoint is new.

# Expected Behavior

The workflow runs requirement, contract design, security assessment (ownership check), implementation on request, testing, documentation, review and validation. Existing API analysis and compatibility assessment are lightly handled or skipped because the endpoint is new and additive. Persistence assessment is skipped because the column already exists and the query is a simple read. No database-change workflow is started.

# Important Checks

- The security stage runs and covers the "own preferences only" rule.
- Stage 6 (persistence) is skipped with a reason.
- Compatibility is recorded as additive with no known consumers.
- Tests include an unauthorized or other-user case.
- The `database-troubleshooting-agent` is not invoked.

# Failure Conditions

- Starting database-change for a read of an existing column.
- Skipping the security stage.
- Running a compatibility assessment as if a consumer were affected, with no basis.
- Skipping tests or documentation without a reason.

# Notes

The workflow should scale down while keeping the security stage, which the data makes necessary.
