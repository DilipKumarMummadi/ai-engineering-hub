# Scenario

Enough evidence is provided to explain the failure without a separate reproduction.

# Input

```
Run the bug-fix workflow: POST /orders returns 500 for some customers.

System.NullReferenceException at OrderService.BuildShipment(Order o) line 88: o.ShippingAddress.PostalCode
Failing orders all have ShippingAddress = null (pickup orders, created since 5.4).
```

# Context

The repository contains OrderService and its tests. The pickup order type was added in 5.4.

# Expected Behavior

The workflow captures the symptom, skips the reproduction stage because the trace and data explain the failure, and uses the `bug-investigation-agent` to confirm the cause from the evidence: pickup orders have no shipping address. It plans a minimal fix, implements it on request, plans and adds a regression test for a pickup order with the `test-planning-agent` and `testing`, runs the tests, reviews with the `pr-review-agent`, and validates.

# Important Checks

- Stage 2 (reproduce) is skipped with the reason that the evidence explains the failure.
- The root cause cites the trace and the pickup-order evidence.
- The fix is planned as minimal, and no redesign of order types is started.
- A regression test for the null case exists and was run.
- The pr-review-agent is used for review, and the workflow does not do its own review.

# Failure Conditions

- Demanding a reproduction when the evidence is sufficient.
- Skipping the regression test.
- Expanding into a redesign of shipment handling.
- Claiming the fix works without a test run.
- Not using the bug-investigation-agent for the investigation.

# Notes

The point is appropriate skipping. The workflow should not add stages the evidence has made unnecessary.
