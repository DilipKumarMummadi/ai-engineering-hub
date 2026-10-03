# Scenario

A new endpoint changes order state.

# Input

/pr-intelligence Review and tell me whether `PUT /orders/{id}/status` is ready.

# Context

PR description: "Add endpoint to update order status."

- `OrdersController.cs`: adds `[HttpPut("{id}/status")]` taking `{ "status": "shipped" }`. There is no `[Authorize]` attribute on the action, and the controller class has none either. Other controllers in the repository use `[Authorize(Policy = ...)]`.
- `OrderService.cs`: `UpdateStatus` sets the status without checking the current status.
- `tests/`: no tests for the new endpoint.
- The endpoint returns `200` with the order on success and `500` if the order is not found.
- No performance-sensitive code is touched.

# Expected Behavior

The report understands the change as a state-changing endpoint. It applies `code-review`, `api-development` (missing-order should be `404`, the contract is undocumented), `security` (the action has no authorization and other controllers do), and `testing` (no tests). It does not apply `performance`, `database-sql`, `observability` or `architecture`. It classifies the missing authorization as a confirmed blocker, based on the code and the convention in other controllers, and rates the `500` for a missing order and the missing transition check as findings. It lists tests as recommended, none executed. Readiness is Needs Changes.

# Important Checks

- The authorization gap is a confirmed blocker with evidence, not a vague concern.
- Only the relevant supporting skills.
- Tests recommended, not executed.
- Readiness is Needs Changes.

# Failure Conditions

- Ready, or missing the authorization gap.
- Running performance or architecture analysis without basis.
- Claiming the endpoint was exercised.

# Notes

Checks skill selection and blocker classification.
