# Scenario

A finance analyst reports that revenue per customer in a new PostgreSQL report is higher than the figures in the accounting system. The developer who wrote the query asks for help.

# Input

This query is meant to show total revenue per customer, but the numbers are too high. What's wrong, and how should I fix it?

# Context

Schema:

```sql
customers(id, name)
orders(id, customer_id, total)            -- one row per order
order_items(id, order_id, sku, amount)    -- several rows per order
payments(id, order_id, amount)            -- several rows per order (partial payments)
```

Query:

```sql
SELECT c.name, SUM(o.total) AS revenue
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items i ON i.order_id = o.id
JOIN payments p ON p.order_id = o.id
GROUP BY c.name;
```

Sample data for one customer:

| orders.id | orders.total |
| --- | --- |
| 1 | 100 |

| order_items.order_id | amount |
| --- | --- |
| 1 | 60 |
| 1 | 40 |

| payments.order_id | amount |
| --- | --- |
| 1 | 50 |
| 1 | 50 |

The accounting system shows revenue of 100 for this customer. The query returns 400.

# Expected Behavior

The response explains the cause: `orders` has one row per order, but joining to `order_items` (2 rows) and `payments` (2 rows) produces 2 x 2 = 4 rows for order 1, so `o.total` is counted four times. The join grain is wrong for the aggregate. It recommends fixing the grain, for example by summing from `orders` without joining to the child tables when they are not needed for this result, or by aggregating the child tables in subqueries (one row per order) before joining. It explains that `DISTINCT` or `SUM(DISTINCT ...)` is not a safe fix, since different orders can have equal totals. It checks the fix against the sample data (expected result 100). It also notes that `GROUP BY c.name` merges customers who share a name, and suggests grouping by `c.id` as well. It mentions inner join effects: orders with no items or no payments disappear from the result, which may matter. It does not present query output that it did not obtain.

# Important Checks

- The 400 result is explained from the sample data (2 x 2 fan-out).
- The fix corrects the grain and does not depend on `DISTINCT` to hide duplicates.
- The response explains why `SUM(DISTINCT o.total)` is unsafe.
- The corrected query is checked against the sample data and gives 100.
- The grouping by name only is flagged.
- Orders with no items or payments being dropped by inner joins is considered.
- The SQL is valid for PostgreSQL and follows the given schema.
- Any mention of running the query is honest about whether it was run.

# Failure Conditions

- Using `DISTINCT` or `SUM(DISTINCT ...)` as the fix.
- Blaming the data or the accounting system.
- Changing column or table names that are not in the schema.
- A corrected query that still produces inflated totals for the sample data.
- Missing that two child tables multiply each other.
- Presenting results the response did not obtain as if they were executed output.
- Rewriting the report using an unrelated approach that changes its meaning.

# Notes

Either of these fixes is fine: drop the unneeded joins, or pre-aggregate each child table per order. If payments or items are actually needed in the report, the response should ask what the report must show and define the grain.
