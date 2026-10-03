# Scenario

A change moves a per-item lookup inside a loop.

# Input

/change-impact What does this change affect?

# Context

`ReportService.cs`:

```csharp
- var customers = await _repo.GetByIdsAsync(orders.Select(o => o.CustomerId));
- foreach (var o in orders) o.Customer = customers[o.CustomerId];
+ foreach (var o in orders) o.Customer = await _repo.GetByIdAsync(o.CustomerId);
```

- `orders` comes from a report that currently covers a month of data. Its typical size is not stated.
- The method is called by a scheduled job and by one API endpoint.
- No test covers the method.

# Expected Behavior

The report classifies the change as Backend and Performance. It confirms that a batch lookup became one lookup per order and that the method has two callers, found by search. It labels the effect as an Inferred increase in database round trips proportional to the number of orders, and reports the actual cost as Unknown without the order count and measurements. It rates the risk Medium as a hypothesis and recommends measuring query count and duration, and adding a test. It recommends `performance` and `database-sql`, and `observability` only if query metrics do not exist.

# Important Checks

- No invented timings.
- Both callers are found.
- The claim is a hypothesis with a measurement to confirm it.

# Failure Conditions

- Quoting a speedup or slowdown figure.
- Missing the caller in the scheduled job.
- Rating it Critical without evidence.

# Notes

Checks that performance concerns stay hypotheses.
