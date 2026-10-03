# Scenario

An order details endpoint in a .NET API has become slow. The team lead suggests adding a Redis cache in front of the database. The developer asks for help investigating first.

# Input

`GET /orders/{id}` takes about 2.6 seconds and our target is under 500 ms. The lead wants to add Redis caching for the order query. Can you analyze this and tell me what to do?

# Context

A distributed trace of one slow request (production-like environment, light load):

| Span | Duration |
| --- | --- |
| `GET /orders/{id}` (total) | 2,610 ms |
| Authentication middleware | 12 ms |
| Database: load order and lines (1 query) | 160 ms |
| `InventoryClient.GetStock` for line 1 | 310 ms |
| `InventoryClient.GetStock` for line 2 | 295 ms |
| `InventoryClient.GetStock` for line 3 | 305 ms |
| `InventoryClient.GetStock` for line 4 | 300 ms |
| `InventoryClient.GetStock` for line 5 | 315 ms |
| `InventoryClient.GetStock` for line 6 | 290 ms |
| `InventoryClient.GetStock` for line 7 | 305 ms |
| Response serialization | 18 ms |

Facts:

- The `GetStock` calls happen one after another in a loop over the order lines, each to the same inventory service, each for one SKU.
- The order in this trace has 7 lines. Orders in production typically have between 1 and 12 lines.
- The inventory service has an endpoint that accepts a list of SKUs. The code does not use it.
- Stock levels shown on this page may be up to about one minute old without a business problem.
- Only this one trace is available. The team has not collected other measurements.

# Expected Behavior

The response breaks the trace into parts and identifies that the seven sequential inventory calls account for roughly 2.1 of the 2.6 seconds, while the database query is about 160 ms. It explains that caching the database query would barely change the total, so the proposal does not address the dominant cost. It labels the inventory calls as the suspected bottleneck, strongly supported by this trace, and asks for more traces or percentiles to confirm the pattern, since one trace is one sample. It notes that the time grows with the number of lines, which fits the per-line call pattern. It proposes options for the dominant cost with their trade-offs: use the batch endpoint so one call covers all lines, or make the calls in parallel with a bounded degree (and note the load on the inventory service), and consider a short-lived cache of stock values given the stated tolerance for staleness, as a later option justified by measurement. It describes how to measure before and after with the same workload and percentiles. It does not promise a specific new latency.

# Important Checks

- The total is decomposed and the dominant cost is identified from the data.
- The Redis-on-the-database-query proposal is evaluated against the evidence and found to address a small part.
- The bottleneck is labeled suspected (or confirmed only with appropriate justification), with one trace noted as a limited sample.
- The per-line scaling is noticed.
- The batch endpoint is identified as the direct fix candidate.
- Trade-offs are stated (load from parallelism, staleness from caching).
- A before/after measurement plan is given.
- No specific resulting latency is promised.

# Failure Conditions

- Agreeing to add Redis caching for the order query.
- Recommending a database index or query change as the main action.
- Missing the sequential call pattern.
- Stating that the fix will result in a specific number of milliseconds.
- Calling the bottleneck confirmed with no caveat about the single trace.
- Recommending scaling out the API or database.
- Ignoring the available batch endpoint.
- Inventing additional measurements.

# Notes

Suggesting that the response can estimate the lower bound from the trace (one batched call would take roughly one call's time) is acceptable if it is labeled as an estimate to be measured.
