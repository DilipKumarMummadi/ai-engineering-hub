# Scenario

An order creation endpoint must calculate tax using an external tax service. The tax service is sometimes slow or unavailable. The team asks the API Development Agent to design the endpoint so that order creation stays dependable.

# Input

`POST /api/v1/orders` needs to call an external tax service to calculate tax. We want the API to be dependable even when the tax service is having problems. Please design this endpoint.

# Context

Facts:

- The tax service is operated by a third party. Its latency is about 150 ms at the median and 800 ms at p99. It has had roughly two outages a month, each about 10 minutes.
- The orders API has an internal target of p95 under 1 second.
- The mobile client retries `POST /orders` automatically if it has not received a response within 5 seconds. It sends no request identifier today, but the next client release can add one.
- The business has stated: if an exact tax amount is not available when an order is placed, the order may be created with an estimated tax (a flat percentage by country), clearly marked as an estimate, and the exact tax must be computed and the order corrected within one hour. Blocking order creation on the tax service is not acceptable.
- Order creation writes the order and its lines to PostgreSQL in one transaction.
- Taxes shown to the customer on the order confirmation must match what is charged.
- The tax service has no idempotency support, and calls are read-only (they calculate, they do not record).

# Expected Behavior

The agent uses `api-development` as the core, `reliability` (timeouts, fallback, retry safety, duplicate requests) and `testing` (fault injection and contract tests) because the case centers on an unreliable dependency. It may use `performance` for the latency budget. It does not need `security` or `architecture` for this requirement, unless it justifies them. It designs the endpoint around the business rule: call the tax service with a timeout derived from its latency and the API budget (for example a few hundred milliseconds beyond its p99, within the 1-second target), use a circuit breaker so an outage does not make every request wait, and fall back to the estimated tax when the exact value is unavailable, recording that the tax is an estimate. Since the calculation is a read-only call, limited retries with backoff within the deadline are acceptable. It defines the API contract: the response includes the tax amount and a field that says whether it is an estimate, so the client can display it accordingly, and documents that the amount may change after creation. It plans the correction path (a background process that recomputes exact tax for estimated orders within the one-hour limit, with its own retry and alerting for orders that remain estimated) and how customers are informed of a change. It addresses the duplicate requests from client retries: an idempotency key supplied by the client in the next release, with database enforcement, same key and same body returning the original response, and the interim risk for older clients, which it names honestly. It specifies observability for the dependency (latency, errors, breaker state, fallback count, estimated orders pending) and alerting. It plans tests with fault injection for timeouts, outages and slow responses, and contract tests for the response shape. It lists open questions, such as how estimates are presented to customers and how discrepancies in charge are handled. It does not claim anything was tested.

# Important Checks

- The design is driven by the stated business rule, not blocking on the tax service.
- Timeout and retry behavior are derived from the latency figures and the 1-second budget.
- A circuit breaker or similar protection against outages is included.
- The fallback is explicit in the contract (estimate flag) and has a correction path with monitoring.
- Retry safety is reasoned: the tax call is read-only, and the order creation retry from the client needs an idempotency key.
- Older clients without the key are addressed.
- Observability for the dependency and the backlog of estimated orders is specified.
- Fault-injection tests and contract tests are planned.
- Skills are used where the case calls for them.
- No claim of implementation or testing, and no invented figures.

# Failure Conditions

- Blocking order creation until the tax service responds.
- Default or unlimited timeouts.
- Unbounded or immediate retries.
- A fallback that is hidden from the client and the record.
- No correction path for estimated orders.
- Ignoring client retries and duplicate orders.
- Treating the tax service's lack of idempotency as a problem for the read-only call.
- No monitoring of the fallback.
- Inventing service behavior or figures.
- Claiming to have tested the design.

# Notes

Where exactly to compute the correction (inline later, scheduled job or message) is a design choice. The requirement is that the one-hour rule is met and failures are visible.
