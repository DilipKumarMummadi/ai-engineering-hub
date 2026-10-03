# Scenario

A customer reports that an order failed at about 14:03 and they were not told why. Three .NET services were involved: `order-api`, `payment-service` and `fraud-service`. The on-call engineer cannot connect their logs and asks for help now and for the longer term.

# Input

A customer's order failed around 14:03 and I can't link the logs across the services. What can I conclude from these logs, and how do we fix this for the future?

# Context

Log lines from the three services (all times UTC, same day). These are the only lines found near the time by the engineer:

`order-api`:

```
14:03:11.204 INFO  Placing order orderId=8841 customerId=552
14:03:11.980 WARN  Payment request failed orderId=8841 status=502
```

`payment-service`:

```
14:03:11.310 INFO  Charge requested amount=120.00 customerId=552
14:03:11.902 ERROR Fraud check call failed: The operation was canceled
14:03:11.903 INFO  Charge rejected
```

`fraud-service`:

```
14:03:11.350 INFO  Scoring request received
14:03:11.351 INFO  Scoring request received
14:03:12.810 INFO  Scoring complete score=0.12
```

Facts:

- The services write plain text logs, with no shared identifier. The order id appears only in `order-api`, and the customer id only in `order-api` and `payment-service`.
- The services run on several instances each. There are no traces. The engineer can see metrics for request counts and error counts per service.
- About 40 orders per minute are placed at this time of day.
- The team uses a central log platform and wants a solution that works across HTTP calls and later across their message queue.

# Expected Behavior

The response separates what the logs show from what they do not. The lines are consistent with a story (the order was placed, payment was requested 100 ms later, the fraud call was canceled around 14:03:11.9, payment rejected, order-api saw a 502) but linking them relies on timestamps and the customer id, which is weak evidence at 40 orders per minute, especially since `fraud-service` logged two scoring requests and its line has no identifier. Scoring completed at 14:03:12.810, after the payment service gave up, which is suggestive, but it is a hypothesis (for example that the fraud call exceeded a timeout in the payment service) and not confirmed from these lines. The response does not state a root cause as fact. It suggests validation, such as checking the timeout setting of the fraud call in `payment-service` and other failures in that window. For the long term it recommends propagating a trace context (the W3C `traceparent` header is a standard choice) through every hop, including the queue messages later, logging the trace id and span id with every log entry through a logging scope in a structured format, adopting distributed tracing, keeping business identifiers like the order id as searchable fields, and avoiding personal data in logs. It recommends validating by following a test request through all three services.

# Important Checks

- Observed facts are stated and the conclusion is labeled as a hypothesis, not a root cause.
- The weakness of timestamp and customer id correlation is explained, using the traffic rate.
- The unexplained second scoring request and the timing of the fraud response are noticed.
- A concrete validation step for the hypothesis is proposed.
- The long-term fix is a propagated correlation or trace context in every hop and in log entries, not only "add an order id to logs".
- Structured logging and future queue propagation are addressed.
- Sensitive data in logs is considered.
- A way to validate the instrumentation is given.
- No log lines or facts are invented.

# Failure Conditions

- Declaring a confirmed root cause from the three log lines.
- Treating timestamps as reliable proof of linkage.
- Suggesting that each service generate its own unrelated id.
- Recommending logging full request bodies or personal data to link requests.
- Recommending a specific vendor as the fix with no mechanism.
- Not addressing how the context is passed between services.
- Inventing additional log lines or configuration.
- Ignoring the current investigation and giving only the long-term plan.

# Notes

The interesting detail is that the fraud response arrived after the payment service's failure. A response may notice this and treat it as a lead. It should not treat it as proven.
