# Scenario

A bug let customers place orders with a quantity of zero, which created empty orders. A fix is ready. The team asks the Test Planning Agent to plan the regression coverage.

# Input

We fixed a bug where orders with quantity 0 were accepted. Please plan the regression tests so this doesn't come back.

# Context

Bug report: "Order placed with quantity 0. The order was created with total 0.00 and appeared in the warehouse queue."

Root cause (established during investigation): the validation in `OrderValidator` rejected only negative quantities.

Before the fix:

```csharp
if (line.Quantity < 0)
    errors.Add("Quantity must be positive");
```

After the fix (not yet merged):

```csharp
if (line.Quantity <= 0)
    errors.Add("Quantity must be positive");
```

Facts:

- Quantity is an integer. The maximum allowed quantity per line is 999.
- The rule applies to the API `POST /api/orders` (which returns 400 with the error list), and to the admin import, which uses the same `OrderValidator`.
- The web form prevents the user from entering 0, but the bug came through the API from a mobile client.
- An order has one or more lines. An order with several lines where one line has quantity 0 was also accepted before the fix.
- The existing tests for `OrderValidator` cover negative quantities, and valid quantities of 1 and 10. No test covers 0 or the upper limit.
- A number of orders with quantity 0 already exist in the database. Cleaning them up is a separate task.
- The team uses xUnit and an API integration test setup with a real database.

# Expected Behavior

The agent uses `debugging` to understand the original failure and `testing` to plan, and uses `api-development` for the API behavior. It does not use `playwright`: the failure occurred through the API and the form already prevents the input, so a browser test adds little. It plans around the original failure: a test that reproduces the bug (quantity 0 is rejected) and that fails against the pre-fix code, stated as a check to perform where practical before applying the fix. It plans boundary coverage around the rule, not only the reported value: quantity 0, -1, 1 and 999, and 1,000 as the upper limit (if the limit is enforced by the same validator, which should be confirmed), at the unit level for `OrderValidator`. It plans an API-level test that `POST /api/orders` returns 400 with the error for a zero-quantity line, including a multi-line order where only one line is zero, since that was also accepted. It plans a test for the admin import path because it uses the same validator, which shows the fix applies there (to be confirmed, not assumed). It identifies that existing data with zero quantities is not covered by the fix, lists it as a gap and open question for a separate cleanup, and notes a check that such orders cannot be created through any path. It avoids E2E tests. It states that no tests were run. It stays inside the facts, and does not invent other validation rules.

# Important Checks

- A test that reproduces the original failure is included, with the before/after check.
- Boundary values (0, -1, 1, 999, and the limit above it if applicable) are planned at the unit level.
- An API-level test covers the 400 response, including the multi-line case.
- The admin import path is covered or flagged for confirmation.
- Existing bad data is identified as a gap, kept separate from the test plan.
- No browser E2E test is planned, with the reason.
- The skills used are those the task calls for.
- The plan does not claim execution.
- No invented rules or requirements.

# Failure Conditions

- Testing only quantity 0 with no boundaries.
- Missing the multi-line case or the API level.
- Missing the admin import path.
- Planning E2E tests as the main regression protection.
- Ignoring the requirement to show the test fails before the fix.
- Treating the data cleanup as part of the regression tests, or ignoring it.
- Claiming tests were written or passed.
- Inventing additional validation rules.

# Notes

The limit of 999 is given as a fact about the quantity, but it is not said that the validator enforces it. A good plan asks or verifies this instead of assuming.
