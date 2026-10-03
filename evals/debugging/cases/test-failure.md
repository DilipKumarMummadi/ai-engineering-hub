# Scenario

A .NET team's CI pipeline started failing on one xUnit test after a second test class was added to the same project. The developer wants to change the expected value in the failing test to make the build green.

# Input

`Adds_one_item` fails in CI with "Expected 1, Actual 2". It passes when I run it alone. I'm going to change the expected value to 2. Is that right? Please investigate.

# Context

CI output:

```
Failed Adds_one_item
  Assert.Equal() Failure
  Expected: 1
  Actual:   2
```

`CartTests.cs`:

```csharp
public class CartTests
{
    internal static readonly List<string> Items = new();

    [Fact]
    public void Adds_one_item()
    {
        var cart = new Cart(Items);
        cart.Add("book");
        Assert.Equal(1, cart.Count);
    }
}
```

`CartDiscountTests.cs`, added in the same pull request:

```csharp
public class CartDiscountTests
{
    [Fact]
    public void Applies_discount_to_two_items()
    {
        var cart = new Cart(CartTests.Items);
        cart.Add("pen");
        cart.Add("cup");
        Assert.Equal(0.9m, cart.DiscountFactor);
    }
}
```

Both test classes use the same static `CartTests.Items` list. Different xUnit test classes can run in parallel by default. `Cart` stores the list it is given and adds items to it. The `Cart` class is unchanged in this pull request and its own behavior is correct.

# Expected Behavior

The response reasons that the test's intent is a new cart containing one item, so the expected value of 1 is correct and 2 would hide the problem. The actual value of 2 comes from a list shared between tests. The static list is mutable state that both classes use, so the count depends on whether the other test added items first. Running the test alone passes, which matches shared state. This is a test defect, and the application (`Cart`) is behaving correctly. The response recommends giving each test its own list and not changing the expected value. It may mention that disabling parallelism would hide the problem instead of removing it.

# Important Checks

- The response advises against changing the expected value, and explains why.
- Shared mutable static state between tests is identified as the cause, linked to the pass-alone, fail-together symptom.
- The response classifies this as a test defect, not an application defect.
- The fix isolates the state (fresh list per test).
- The response does not propose changing `Cart`.
- The response does not treat disabling parallel execution as the real fix.
- The cause is tied to the evidence given, not invented.

# Failure Conditions

- Agreeing to change the expected value to 2.
- Concluding there is a bug in `Cart`.
- Attributing the failure to flakiness or CI without explanation, with no analysis of the shared list.
- Recommending retries or a rerun as the solution.
- Missing that the second test class is the trigger.
- Recommending only disabling test parallelism.
- Inventing details such as a race in the framework.

# Notes

The failure can also depend on test execution order, so it may not reproduce on every run. A good response can note this. It is consistent with the shared-state explanation.
