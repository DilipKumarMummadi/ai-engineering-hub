# Scenario

A behavior change ships with no tests.

# Input

/pr-intelligence Is this ready?

# Context

PR description: "Apply a 10% discount for orders over 100."

- `PricingService.cs`: adds `if (total > 100) total *= 0.9m;` inside `CalculateTotal`.
- No test file changed. `PricingServiceTests.cs` exists and tests `CalculateTotal` without discounts.
- Boundary behavior at exactly 100 is not specified in the description.
- Rounding behavior for the discount is not specified.

# Expected Behavior

The report applies `code-review` and `testing`. It confirms that a behavior change has no test and that existing tests do not cover the discount. It raises the unspecified boundary at 100 and rounding as findings or questions, not as defects. It recommends tests at the lowest level (unit) for below, at and above the threshold, and for rounding, and states that none were run. Readiness is Needs Changes for the missing validation, and the questions are listed under Missing Information.

# Important Checks

- Missing tests lead to Needs Changes.
- No specialized skills.
- Boundary and rounding are questions, not invented defects.
- Tests recommended, none executed.

# Failure Conditions

- Ready.
- Claiming the existing tests pass with the change.
- Adding security or performance analysis.

# Notes

Checks the testing gate.
