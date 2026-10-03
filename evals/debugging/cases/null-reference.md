# Scenario

A .NET API using Entity Framework Core and PostgreSQL returns HTTP 500 for one customer summary request. The team's first idea is to "just add a null check".

# Input

`GET /customers/1042/summary` returns 500 and the log shows a NullReferenceException. Please investigate and tell me how to fix it.

# Context

Log line:

```
System.NullReferenceException: Object reference not set to an instance of an object.
   at CustomerService.GetSummaryAsync(Int32 id) in CustomerService.cs:line 31
```

`CustomerService.cs`:

```csharp
public async Task<CustomerSummary> GetSummaryAsync(int id)
{
    var customer = await _db.Customers
        .FirstOrDefaultAsync(c => c.Id == id);                      // line 29

    return new CustomerSummary(customer.Name, customer.Address.City); // line 31
}
```

Known facts:

- Customer 1042 exists in the `customers` table, and has one row in the `addresses` table that references it.
- `Customer.Address` is a navigation property to the `Address` entity.
- Lazy loading is not configured in this project.
- Customer 1043, which also has an address row, fails the same way.

# Expected Behavior

The response reasons that line 31 dereferences two things, `customer` and `customer.Address`. The known facts rule out `customer` being null, because customer 1042 exists. The remaining candidate is `Address`, which has a row in the database, so the data is not the issue. The query does not load the navigation property and lazy loading is off, so `Address` is null in memory. The response states this as the likely cause and gives a way to validate it, such as checking that `Address` is null after the query or inspecting the generated SQL for a join. It recommends loading the related data in the query (or projecting what is needed), not a null check that hides the failure. It recommends a regression test for a customer that has an address.

# Important Checks

- The response identifies which object is null and uses the known facts to rule out the other.
- It explains why the object is null, in terms of how the data is loaded.
- It does not treat a null check as the fix. If it mentions a null check, it is only for a separate valid "customer not found" case.
- The cause is presented as a hypothesis with a validation step, or as confirmed only if the response explains what evidence confirms it.
- The fix changes how the data is loaded.
- A regression test is recommended.
- Nothing is fabricated about the environment.

# Failure Conditions

- The first and main recommendation is to add a null check or a null-conditional operator.
- The response blames bad data in the database, against the stated facts.
- The response claims a root cause that the evidence does not support, such as a connection problem.
- The response ignores that two dereferences happen on the same line.
- The response asks for information that is already in the context.
- The response proposes rewriting the data layer.

# Notes

A good response may also point out that `FirstOrDefaultAsync` can return null for a missing customer and that the endpoint should return a not-found result. That is a valid secondary point.

The facts show that two customers with address rows fail. They do not show whether customers with no address row also fail, so a response should not claim to know that.
