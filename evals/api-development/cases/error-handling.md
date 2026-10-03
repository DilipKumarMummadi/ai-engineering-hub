# Scenario

An ASP.NET Core API has grown organically. Clients report confusing errors, and a security review found internal details in responses. The team wants the error handling fixed, but two client apps are in production.

# Input

Please review the error handling in this controller and recommend improvements. We have a mobile app and a partner integration that use this API today.

# Context

`OrdersController.cs`:

```csharp
[HttpGet("{id}")]
public async Task<IActionResult> Get(int id)
{
    try
    {
        var order = await _db.Orders.FindAsync(id);
        if (order == null)
            return Ok(new { success = false, message = "not found" });
        return Ok(new { success = true, data = order });
    }
    catch (Exception ex)
    {
        return StatusCode(500, ex.ToString());
    }
}

[HttpPost]
public async Task<IActionResult> Create(OrderRequest req)
{
    if (req.Quantity <= 0)
        return BadRequest("bad quantity");

    try
    {
        var order = new Order { ProductId = req.ProductId, Quantity = req.Quantity };
        _db.Orders.Add(order);
        await _db.SaveChangesAsync();
        return Ok(new { success = true, data = order });
    }
    catch (DbUpdateException ex)
    {
        return StatusCode(500, ex.InnerException?.Message);
    }
}
```

Facts:

- A foreign key constraint on `ProductId` exists. An unknown product currently produces a `DbUpdateException` whose inner message includes the constraint name and table.
- The mobile app checks the `success` field in the body. The partner integration checks the HTTP status code only and treats any 200 as success.
- `Order` is the EF Core entity and includes `InternalCostPrice`.
- The project has no global exception handling or shared error format.

# Expected Behavior

The response identifies the concrete problems: a missing order returns 200 with `success: false` (so the partner integration will treat it as success), validation failures return a plain string, server failures return `ex.ToString()` with a stack trace, and the database error message leaks the constraint and table names. An unknown product is a client error that is reported as 500. The entity is returned directly, exposing `InternalCostPrice`. It recommends correct status codes (404 for a missing order, 400 or 422 for validation and an unknown product, 500 only for real server errors), a single consistent error format (problem details in ASP.NET Core is a natural choice), global exception handling that logs the detail but returns a generic message, and response DTOs. It then addresses compatibility: changing a 200 to a 404 changes behavior for the partner integration, and the mobile app relies on `success`. It recommends a migration approach, for example coordinating with the clients, versioning the endpoint or temporarily keeping the old envelope while adding correct status codes, with the breaking changes called out. It recommends tests for each error case.

# Important Checks

- The specific problems in the code are identified, with the impact on each client.
- Correct status codes are proposed for each case, including the unknown product case.
- Internal details (stack trace, constraint names, `InternalCostPrice`) are flagged as leaks.
- One consistent error format is proposed, and detail is logged on the server.
- The compatibility risk for the two clients is analyzed separately for each client.
- A migration path is suggested and breaking changes are called out, not done silently.
- The approach fits ASP.NET Core and the project's conventions.
- Tests for the error cases are recommended.

# Failure Conditions

- Changing all status codes and the response shapes with no mention of existing clients.
- Keeping `200` with `success: false` as acceptable.
- Still returning exception messages to clients.
- Missing the entity exposure.
- Treating the unknown product as a server error.
- Suggesting to just catch exceptions in more places.
- Proposing a rewrite into a different framework.
- Claiming to have verified behavior that was not run.

# Notes

The partner integration treating any 200 as success is a concrete reason the current behavior is harmful. Good responses point out that the mobile app and the partner integration are affected differently.
