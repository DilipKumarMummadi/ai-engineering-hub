# Scenario

An EF Core endpoint that lists orders with customer names has become slower as page sizes grew. A developer suspects the database is slow and wants to upgrade its tier.

# Input

The orders list endpoint takes about 260 ms for a page of 100 orders. We think the database is underpowered and want to upgrade the tier. Can you look at this and tell me what's going on?

# Context

Controller code:

```csharp
var orders = await _db.Orders
    .OrderByDescending(o => o.CreatedAt)
    .Take(100)
    .ToListAsync();

var result = orders.Select(o => new OrderListItem(
    o.Id,
    o.Total,
    o.Customer.Name));          // Customer is a navigation property

return Ok(result);
```

Facts:

- Lazy loading proxies are enabled in `AppDbContext`.
- EF Core SQL logging for one request shows 101 queries:
  - One query: `SELECT ... FROM orders ORDER BY created_at DESC LIMIT 100` (took 4 ms).
  - 100 queries of the form `SELECT ... FROM customers WHERE id = @p0` (each about 2 ms).
- Database CPU during the test was under 10%. The database is in the same region as the API.
- For a page size of 20, the same endpoint takes about 55 ms.
- Many of the 100 orders share the same customer.

# Expected Behavior

The response reads the evidence: 101 queries per request where one or two would do. Each query is fast (2 to 4 ms), the database is lightly loaded, and the time scales with page size (55 ms for 20 and 260 ms for 100). That fits a classic N+1 pattern caused by lazy loading of `Customer` inside the projection loop, not an underpowered database. It explains that upgrading the tier would not change the number of round trips and so is unlikely to help. It recommends loading what is needed in a single query, by projecting to the needed fields in the query so that the customer name comes in the same SQL statement, or using eager loading for the navigation property, with a note about choosing the projection because only the name is needed. It warns about trade-offs, such as over-fetching with eager loading of entire entities, and that lazy loading may hide the same pattern elsewhere. It recommends checking the generated SQL and the query count after the change, measuring the latency at both page sizes, and adding a guard, for example a test that asserts the number of queries. It does not promise a specific latency.

# Important Checks

- N+1 is identified from the query log, with the arithmetic (101 queries, each a few ms) tied to the latency.
- The low database CPU and the scaling with page size are used to reject the "underpowered database" hypothesis.
- The cause is tied to lazy loading in the code shown.
- The fix retrieves the data in one query, and the choice (projection vs eager loading) is explained.
- The response does not recommend caching or a tier upgrade as the first action.
- Verification is defined in terms of query count and latency.
- A regression guard is suggested.
- No specific resulting latency is promised.

# Failure Conditions

- Agreeing to upgrade the database tier.
- Recommending an index on `customers.id` (it is already a key lookup, and each query is fast).
- Recommending adding a cache as the main fix.
- Missing the lazy loading cause.
- Promising a specific resulting latency.
- Recommending disabling lazy loading globally with no mention of consequences and verification.
- Ignoring the evidence of query count.
- Inventing measurements.

# Notes

Mentioning that the fix should be checked for a different problem, such as a join that multiplies rows if collections are included, is a good addition. It is not required, because only a single-valued navigation is involved here.
