# Scenario

A team building a React and TypeScript checkout wants coverage for shipping cost rules. They plan one browser test per rule combination. A tech lead asks for a review of the plan.

# Input

We plan to cover the shipping cost rules with 12 Playwright tests, one for each combination. Does this plan make sense? What would you recommend?

# Context

The rules live in a pure function with no side effects:

```ts
export function shippingCost(weightKg: number, zone: 'domestic' | 'eu' | 'international'): number
```

Rules table: four weight bands (0 to 1 kg, over 1 to 5 kg, over 5 to 20 kg, over 20 kg) crossed with the three zones gives 12 combinations, each with a fixed price. Orders over 20 kg to the `international` zone are not allowed and the function throws an error.

The planned browser tests would each log in, fill a cart, enter an address and read the shipping price on the checkout page. Each takes about 40 seconds. The CI budget for the E2E suite is already close to its limit.

The checkout page displays the value returned by `shippingCost` and does not change it.

# Expected Behavior

The response recognizes that the rules are deterministic logic in a pure function, so all 12 combinations, the band boundaries (1, 5 and 20 kg exactly) and the disallowed case belong in fast unit tests. It explains that browser tests add time and flakiness without extra confidence about the rules themselves. It recommends keeping a small number of E2E checks, for example one journey showing that the checkout page displays a shipping price and handles the disallowed order, since the page does not change the value. It states the trade-off against the CI budget. It does not fabricate numbers.

# Important Checks

- The response says the rule coverage belongs at unit level and gives a reason tied to the context (pure function, display-only page, slow tests, CI budget).
- Boundary values between the weight bands are identified as needing coverage.
- The disallowed case (over 20 kg international) is included, with the expected error.
- A small number of E2E tests is still recommended for the page integration.
- The response does not reject E2E testing altogether.
- The recommendation is concrete, with example inputs and expected results.
- The reasoning considers cost and confidence, not preference.

# Failure Conditions

- Approving the 12 browser tests as proposed.
- Recommending no E2E coverage at all for the checkout.
- Recommending the rules be tested only through the API or UI.
- Missing the band boundaries or the disallowed case.
- Giving Playwright implementation details as the main answer instead of a test-level decision.
- Making up prices for the rules table that are not in the context.
- Asking to measure coverage percentages instead of covering behavior.

# Notes

The context deliberately does not give the prices, so a good response describes expected results generically (for example "the price for the 1 to 5 kg band in zone X") or asks for the table.
