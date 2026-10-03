# Scenario

A developer opens a pull request for a .NET pricing service. The PR description says: "Apply the customer's percentage discount when calculating an order total." The reviewer is asked to review the change before merge.

# Input

Please review this pull request. The description and the changed file are below.

# Context

PR description: "Apply the customer's percentage discount when calculating an order total. A 10 means 10% off."

`Pricing/OrderCalculator.cs`:

```csharp
public decimal CalculateTotal(IEnumerable<OrderLine> lines, decimal discountPercent)
{
    var subtotal = lines.Sum(l => l.UnitPrice * l.Quantity);
    var total = subtotal - discountPercent;
    return total;
}
```

Only this file changed. No tests were added or changed.

# Expected Behavior

The review notices that `discountPercent` is subtracted as a flat amount instead of being applied as a percentage. A discount of 10 on a subtotal of 200 gives 190 instead of 180, and a subtotal below the discount value gives a negative total. It explains the impact on customer charges and recommends applying the percentage to the subtotal. It also notes that no tests cover the change. It rates the bug as serious, since every discounted order gets the wrong total, but not as a security or data-loss issue.

# Important Checks

- The flat-subtraction mistake is identified as the cause, with the correct expected behavior stated.
- The impact is explained in terms of wrong order totals, with an example or equivalent reasoning.
- The recommendation is specific and small.
- Severity is high or close to it, and not critical or trivial.
- The missing tests are mentioned.
- Findings stay tied to the code shown.

# Failure Conditions

- The bug is missed.
- The bug is described wrongly, for example as a rounding issue.
- The response invents other defects not supported by the code, such as thread safety or overflow concerns.
- The bug is rated as a suggestion or as critical without justification.
- The review is dominated by style or naming comments.
- The response proposes rewriting the pricing design.
- The response assumes details not in the context, such as a currency library in use.

# Notes

A reasonable reviewer may also mention that a discount above 100 or a negative discount is not validated. That is acceptable if it is clearly secondary and worded as a question about intended behavior, and not reported as a confirmed defect.
