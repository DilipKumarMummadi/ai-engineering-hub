# Scenario

A React and TypeScript dashboard calls a .NET API for a monthly report. The day after a release, the report page shows "Request failed" for most customers.

# Input

Since yesterday's release the monthly report fails with a gateway timeout. The gateway timeout is 30 seconds. Can we just raise it to 60 seconds? Please investigate.

# Context

Observed facts:

- The browser shows `GET /api/reports/monthly?customerId=...` returning 504 after about 30 seconds.
- API logs for the same requests show they completed after 41 to 44 seconds. The API did not error, and the gateway gave up first.
- Before the release, the p95 duration of this endpoint was about 300 ms.
- The endpoint runs one SQL query against PostgreSQL:

```sql
SELECT date_trunc('day', created_at) AS day, SUM(total) AS revenue
FROM orders
WHERE customer_id = $1 AND created_at >= $2 AND created_at < $3
GROUP BY 1;
```

- The query plan for a customer with recent orders shows `Seq Scan on orders` with a filter on `customer_id`. The `orders` table has about 8 million rows.
- Yesterday's release included migration `0042`. It contains `DROP INDEX ix_orders_customer_id;` and nothing that creates an index on `customer_id`.
- No application code for this endpoint changed in the release.

# Expected Behavior

The response separates the symptom (gateway 504) from the cause. The API finishes after the gateway timeout, so the gateway is reporting slowness and is not the fault. The duration went from about 300 ms to over 40 s after a release that changed no endpoint code, and the plan shows a full table scan where an index on `customer_id` used to serve the filter. Migration `0042` dropped that index. The response gives this as the cause, with the supporting evidence, and may suggest confirming by comparing the plan before and after or by checking the index list. It recommends restoring an index that supports the filter (and reviewing why the migration dropped it), not raising the gateway timeout. It recommends a safeguard such as reviewing index changes in migrations, or alerting on query duration.

# Important Checks

- The 504 is treated as a symptom, and the slow query as the problem.
- The timeline (release, migration, slowdown) and the query plan are connected into one explanation.
- The response does not recommend only raising the timeout. If it mentions it, it is as a temporary mitigation with the caveat that the query would still take over 40 seconds.
- The fix restores index support for the filter on `customer_id`.
- Validation is described (compare plan and duration after the fix).
- Prevention is relevant: migration review, or a performance check or alert.
- No facts are invented, such as table sizes or load numbers not in the context.

# Failure Conditions

- Agreeing to raise the timeout as the solution.
- Blaming the frontend, the network or the gateway with no supporting evidence.
- Missing the dropped index despite it being in the context.
- Recommending unrelated changes such as caching, rewriting the query, or scaling up the database before addressing the index.
- Claiming certainty without connecting the evidence.
- Adding a list of speculative causes that the evidence already excludes.

# Notes

A correct response may say the cause is "very likely" and suggest one confirming step. That is better than claiming certainty, and it is also better than withholding a conclusion the evidence supports.
