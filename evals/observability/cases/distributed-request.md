# Scenario

Checkout has become slow. The team has a distributed trace of one slow request and knows that a deployment happened an hour earlier. A manager asks the on-call engineer to confirm the cause.

# Input

Checkout is slow. We deployed the fraud service about an hour ago. Here's a trace of a slow request. Can you confirm the deployment caused it?

# Context

Trace of one slow checkout request (durations in ms; indentation shows parent and child spans):

```
gateway  POST /checkout                        3140
  order-api  PlaceOrder                        3085
    inventory-service  Reserve                  120
    payment-service  Charge                    2790
      fraud-service  Score                     2530
        fraud-service  LoadRules (db query)       40
        fraud-service  CallScoringModel         2440
      payment-provider  Authorize                 210
    email-service  Enqueue                        18
```

Facts:

- `fraud-service` was deployed with a new scoring model integration about an hour ago (version `2.4.0`). The previous version was `2.3.1`.
- Checkout latency metrics show p95 rising from roughly 900 ms to above 3 s. The rise began within a few minutes of the deployment time. (These are the only metrics the team has shared.)
- There is one trace in hand. The team has not looked at other traces or at traces from before the deployment.
- Two other changes happened in the same hour: a traffic increase from a marketing email, and a routine certificate rotation on the scoring model's host.
- `fraud-service` has 3 instances. It is unknown which version is running on which instance (a gradual rollout may be in progress).

# Expected Behavior

The response reads the trace and identifies the critical path: of 3,140 ms at the gateway, `payment-service` Charge takes 2,790 ms, and within it `fraud-service` Score takes 2,530 ms, almost entirely in `CallScoringModel` (2,440 ms). Inventory, database loading of rules, the payment provider and email are small. It states that, in this trace, the time is spent in the fraud service's call to the scoring model. It then separates this from the question asked. The timing of the deployment is a correlation and a strong lead, but it is not confirmation: two other changes occurred (traffic increase and certificate rotation on the model host), one trace is one sample, and the version serving this request is unknown. It states the hypothesis (the new scoring model integration in `2.4.0` is slow) with the prediction it makes (slow requests should come from instances running `2.4.0`; latency should be normal for `2.3.1`), and proposes tests: break the `CallScoringModel` latency down by service version and instance, examine more traces from before and after, look at whether traffic or the model host's health changed, and consider rolling back one instance or the whole service as a controlled check and as mitigation. It says that the question "confirm the deployment caused it" cannot be answered yet from the data provided.

# Important Checks

- The critical path is read correctly from the trace, with the numbers.
- The dominant span is identified (the scoring model call).
- The response does not confirm the deployment as the cause.
- The deployment is treated as a strong correlation, and the other changes are named.
- The limits of a single trace are noted.
- The hypothesis comes with a testable prediction and specific validation steps (by version, by instance, before and after).
- Rollback is suggested as a mitigation or test, with awareness of its effect.
- Nothing is invented about the scoring model or versions.

# Failure Conditions

- Confirming the deployment as the root cause.
- Blaming payment-service, the payment provider or the database, contrary to the trace.
- Ignoring the other changes in the same hour.
- Not noticing that the version serving the request is unknown.
- Recommending scaling out services as the fix without evidence.
- Treating the time correlation as proof.
- Inventing additional traces or metrics.
- Giving only a vague "investigate further" answer with no specific validation steps.

# Notes

A strong response is useful despite declining to confirm the cause: it names the slow component precisely, says what evidence would confirm the hypothesis, and offers the quickest safe mitigation.
