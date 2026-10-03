# Scenario

An order management system notifies customers and feeds analytics using a job that polls the database once a minute. More teams now want order updates, and customers complain about slow notifications. Someone proposes "an event-driven architecture". The team asks the Architecture Agent for an analysis.

# Input

We want to get order updates to notifications and analytics faster, and more teams want to consume them. Should we go event-driven? Please analyze the options and recommend an approach.

# Context

Current state:

- Orders are stored in PostgreSQL. A scheduled job runs every minute, reads orders with `updated_at` greater than its last run time, and sends notifications and writes analytics rows.
- Occasionally orders updated at nearly the same instant as a job run are missed by the notifications (the team has seen about one such case a month, through customer support).
- Three teams want order updates: notifications, analytics and a new fraud team. Two more teams have asked.

Requirements and constraints:

- Customer notifications must be sent within 10 seconds of an order status change. Analytics can tolerate up to 5 minutes. The fraud team's needs are not yet defined.
- An order status change must never be silently lost. Occasional duplicate notifications are undesirable but tolerated if rare.
- The system handles roughly 20 order status changes per second at peak.
- The team of 8 engineers has no production experience running a message broker. The company's cloud provider offers a managed queue and a managed streaming service, and the team is allowed to use them. The budget for new services is modest.
- The orders service writes status changes in a database transaction with other data.
- Message formats will need to evolve as teams add fields.

# Expected Behavior

The agent uses `architecture` as the core, and brings in `reliability` (loss, duplicates, ordering, recovery) and `observability` (consumer lag, detecting silent loss) because the requirements make them central. It does not need `security`, `performance`, `api-development` or `refactoring` unless it justifies them, and it does not invoke `database-sql` beyond the consistency point between the database write and publishing, which it may cover under reliability or with a brief database-sql perspective since the transaction boundary is architectural. It identifies the real problems: slow notifications (polling interval), occasional misses (timestamp-based polling has a race), and the growth in consumers. It compares options with trade-offs: keep polling but shorten the interval and fix the gap (simple, limited by load on the database and still a race unless tracked by an ordered position or sequence); publish events from the orders service using a transactional outbox so that the database write and the event cannot diverge, delivered through a managed queue or stream; or capture database changes by replication-based change capture. It evaluates each against the latency targets, loss intolerance, team experience, operations and cost, and expected consumer growth. It explains failure scenarios: broker unavailable, consumer down, duplicate delivery and the need for idempotent consumers, ordering per order, poison messages, schema evolution. It recommends an approach with reasons (or two viable ones with the deciding factors), an incremental migration (run the new path alongside the polling job, compare results, cut over consumer by consumer), validation, and risks. It avoids presenting events as the only answer, and lists open questions such as the fraud team's needs and whether per-order ordering is required.

# Important Checks

- The real problems are separated: latency, the missed updates and the growing number of consumers.
- The polling race is understood as a cause of the missed updates.
- Several options are compared against the stated latency targets, loss requirement, team experience and cost.
- The gap between the database write and publishing is addressed.
- Duplicate delivery, consumer failure, ordering and schema evolution are addressed.
- Operational burden for a team new to brokers is weighed.
- Lag or loss detection is part of the design.
- Migration runs old and new paths in parallel and cuts over gradually.
- Supporting skills are used only where the case calls for them.
- Open questions are listed. No numbers are invented beyond the context.

# Failure Conditions

- Recommending an event-driven design without comparing alternatives.
- Dismissing events outright without analysis.
- Ignoring the lost-update requirement, or the write-and-publish gap.
- Assuming exactly-once delivery.
- Ignoring team experience and operational cost.
- A big-bang cutover.
- Naming a specific product as the answer with no reasoning.
- Invoking every supporting skill.
- Inventing throughput or cost figures.

# Notes

A sound answer can favor an outbox with a managed queue, or an improved polling design for now with events later. The reasoning and its honesty about trade-offs are what is evaluated.
