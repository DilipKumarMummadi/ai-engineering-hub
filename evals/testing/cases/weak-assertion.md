# Scenario

A .NET team has unit tests for invoice creation. All tests are green, but finance reports that invoice totals in production are too high. The team asks whether the tests can be trusted.

# Input

Our invoice tests all pass, but totals are wrong in production. Review these tests and tell me why they didn't catch it and how to improve them.

# Context

Requirement: an invoice total is the sum of its line amounts plus 20% tax on that sum.

`InvoiceService.cs`:

```csharp
public Invoice Create(IReadOnlyList<Line> lines)
{
    var subtotal = lines.Sum(l => l.Amount);
    var tax = subtotal * 0.20m;
    var total = subtotal + tax;
    total += tax;                 // added during a refactor
    return new Invoice(lines, total);
}
```

`InvoiceServiceTests.cs`:

```csharp
[Fact]
public void Creates_invoice()
{
    var invoice = _service.Create(new[] { new Line("Design", 100m), new Line("Build", 50m) });
    Assert.NotNull(invoice);
}

[Fact]
public void Total_is_positive()
{
    var invoice = _service.Create(new[] { new Line("Design", 100m) });
    Assert.True(invoice.Total > 0);
}
```

# Expected Behavior

The response explains that both tests would pass whether the total is right or wrong. One checks only that an object exists, and the other that the total is above zero. The implementation adds tax twice, so a 150 subtotal gives 210 instead of 180, and neither test notices. The response identifies the double tax as the production defect, if it inspects the implementation, and explains that the tests failed to catch it because the assertions do not check the required value. It recommends asserting the exact expected total from the requirement with simple, hand-calculated inputs (for example 150 plus 20% gives 180), and checking tax and line items too. It may recommend a few more cases such as an empty invoice.

# Important Checks

- The response explains why each existing assertion cannot detect the defect.
- It links the failing production behavior to the tests' weakness, and not only to the code.
- The recommended assertions compare against values computed from the requirement, not from the implementation.
- The example expectation is calculated correctly from the requirement (180 for a 150 subtotal).
- The double-tax line is identified.
- It does not suggest removing tests or adding tests only to increase coverage.
- The advice is concrete.

# Failure Conditions

- Saying the tests are fine, or that the problem is only in production data.
- Suggesting assertions that copy the implementation's logic, so a wrong implementation would still pass.
- Missing the double tax entirely and blaming something unrelated, such as rounding.
- Proposing the tax be fixed without explaining the test gap, or explaining the gap without the specific stronger assertion.
- Recommending integration or E2E tests to catch what a simple unit assertion would catch.
- Incorrect arithmetic in the proposed expected values.

# Notes

The order of discovery does not matter. A response may start from the tests or from the implementation, as long as it connects the two.
