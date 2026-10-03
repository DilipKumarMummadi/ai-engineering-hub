# Scenario

A developer pastes a slow query and its plan.

# Input

```
/database

This lookup takes over 2 seconds. We have an index on email.

SELECT id, full_name FROM users WHERE lower(email) = lower($1);

Seq Scan on users (actual time=2140.8..2140.9 rows=1 loops=1)
  Filter: (lower(email) = 'ana@example.com'::text)
  Rows Removed by Filter: 7999999
```

# Context

PostgreSQL is the engine, mentioned in the project files.

# Expected Behavior

The command routes the whole message, including the SQL, the plan output and the mention of the existing index, to the `database-troubleshooting-agent` unchanged. It does not interpret the plan or suggest a fix.

# Important Checks

- The request is routed to `database-troubleshooting-agent`.
- The SQL, the full plan text and the index remark are preserved verbatim.
- The command does not diagnose the problem or recommend an index.
- The command adds no SQL guidance.

# Failure Conditions

- Truncating or paraphrasing the plan.
- The command says what is wrong.
- Routing to the performance skill or another agent directly.
- The command runs the query.

# Notes

Diagnosing the unused index is agent reasoning.
