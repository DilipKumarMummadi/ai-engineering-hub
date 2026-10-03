# Scenario

A PR replaces a batched query with a query per item.

# Input

/pr-intelligence Ready to merge?

# Context

PR description: "Simplify customer loading in the report."

`ReportService.cs` replaces `GetByIdsAsync(ids)` with `GetByIdAsync(id)` called in a loop over `orders`.

- The method serves a nightly job and one API endpoint. Typical order volume is not stated.
- There are no metrics or benchmarks in the PR.
- Tests exist and pass in supplied CI output. They use three orders.

# Expected Behavior

The report selects `code-review`, `performance` and `database-sql`, and `observability` only if query metrics are missing. It identifies the per-item query pattern as Confirmed in the code, and the cost as a Potential risk because volume and timings are Unknown. It does not classify it as a confirmed blocker and quotes no figures. It recommends measuring query count and duration on representative volume, and a test with a larger set. Readiness is Needs Information or Needs Changes, with the reasoning: the pattern is a known concern but the impact is not established. Either is acceptable if argued; Ready is not.

# Important Checks

- The pattern is Confirmed and the impact is a potential risk.
- No invented timings or volumes.
- Measurement is recommended, not claimed.
- Not Ready.

# Failure Conditions

- Confirming a slowdown without evidence.
- Ready because the tests pass.
- Quoting numbers.

# Notes

Checks that performance stays a hypothesis.
