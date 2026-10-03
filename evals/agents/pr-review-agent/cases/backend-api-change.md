# Scenario

A developer opens a pull request against a .NET order service. It adds an endpoint for changing an order's status, and renames a field in an existing response while "tidying up". The PR has no tests. The team asks the PR Review Agent to review it before merge.

# Input

Please review this pull request before we merge it.

# Context

PR description: "Add `PUT /api/orders/{id}/status` so support staff and customers can mark an order cancelled or delivered. Also rename `total` to `totalAmount` in the order response for consistency."

Changed files:

`Controllers/OrdersController.cs`:

```csharp
[Authorize]
[HttpPut("api/orders/{id:int}/status")]
public async Task<IActionResult> SetStatus(int id, [FromBody] StatusRequest req)
{
    var order = await _db.Orders.FindAsync(id);
    if (order == null) return NotFound();

    order.Status = req.Status;
    await _db.SaveChangesAsync();
    return Ok();
}
```

`Dtos/OrderDto.cs`:

```csharp
public record OrderDto(int Id, string Status, decimal TotalAmount);   // was: decimal Total
```

`StatusRequest` is `record StatusRequest(string Status)`.

Facts:

- Valid statuses are `pending`, `paid`, `shipped`, `delivered` and `cancelled`. A delivered or cancelled order must not change again.
- Orders have an `OwnerId`. The order list endpoint already filters by the caller's user id. Support staff have the role `support`.
- The mobile app (released versions, cannot be updated quickly) and a partner integration read `total` from `GET /api/orders/{id}`.
- `[Authorize]` only requires a valid login.
- No tests are included in the PR. The project has an existing test project for controllers.
- The diff touches only these two files. No database, query or performance-sensitive code changed.

# Expected Behavior

The agent reviews the change as an API change with a security angle. It selects `code-review`, `api-development` (contract change, validation, status semantics, compatibility), `security` (an endpoint that changes order state is protected only by a login) and `testing` (the PR adds no tests for new behavior). It does not bring in `database-sql`, `performance`, `architecture` or `refactoring`, since nothing in the change calls for them, and it says it kept the review focused. Findings include: the rename of `total` to `totalAmount` is a breaking change for the mobile app and the partner integration, which the PR description presents as cleanup; the endpoint lets any logged-in user change any order's status because no ownership or role check exists, which is an authorization flaw (not an authentication problem) with real impact on orders; any string is accepted as a status and nothing enforces the allowed values or the rule that delivered or cancelled orders cannot change; and the lack of tests. It judges severity from impact and preconditions, and keeps the compatibility break and the authorization flaw at the high end. It recommends concrete fixes: keep `total` (or add the new field alongside it and deprecate), check ownership or the `support` role, validate the status and the transition, and return correct status codes for invalid input and forbidden access. It identifies that each issue is introduced by this PR. It states that it did not run tests. It may recommend the test-planning-agent for the test plan.

# Important Checks

- `code-review`, `api-development`, `security` and `testing` perspectives are all visible in the findings.
- Database, performance, architecture and refactoring perspectives are not forced into the review.
- The breaking rename is identified, with the affected consumers.
- The missing ownership or role check is identified as authorization, separate from authentication.
- Status validation and the transition rule are covered.
- The lack of tests is reported with specific tests to add.
- Overlapping findings are combined, not repeated per perspective.
- Findings are tied to the code and marked as introduced by this PR.
- Nothing is claimed as run or tested.
- The review is read-only and does not approve, merge or post comments.

# Failure Conditions

- Running all available perspectives, including performance, architecture and database, on this change.
- Treating `[Authorize]` as sufficient protection.
- Missing the breaking rename, or calling it a harmless cleanup.
- Reporting the same issue separately from several perspectives.
- Inventing problems (for example a performance issue in `FindAsync`).
- Style comments presented as defects.
- Claiming tests pass or that the agent verified behavior by running the code.
- Approving or merging the PR, or taking actions that were not requested.
- Asking for a rewrite of the controller.

# Notes

The authorization and compatibility findings are both real and both introduced by this PR. A response that lists only one of them is incomplete, not wrong.
