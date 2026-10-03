# Scenario

An e-commerce backend places orders by calling three internal services one after another. When one of them is down, orders fail. The team is considering an event-driven redesign.

# Input

Order placement is failing whenever billing is slow or down. We're thinking about going event-driven. Please analyze the design options and recommend an approach.

# Context

Current flow, executed synchronously inside the "place order" request:

1. Inventory service reserves stock.
2. Billing service charges the customer.
3. Notification service sends a confirmation email.

Requirements and observations:

- An order must never be accepted for stock that is not available (overselling is not allowed).
- A customer must never be charged twice for the same order.
- Billing is allowed to complete up to 5 minutes after the order is accepted, as long as the customer sees the order as "pending payment" meanwhile. If payment fails, the order is cancelled and stock is released.
- The confirmation email may be delayed by several minutes. Losing one is undesirable but not critical.
- Billing has been unavailable for short periods several times a month, and the whole order request fails when it is.
- The team has about 10 engineers, uses .NET and PostgreSQL, and has a managed message broker available from the cloud provider. No one has run an event-driven system in production.
- Peak traffic is in the low hundreds of orders per minute.

# Expected Behavior

The response separates the three steps by their consistency requirements. Reserving stock has a strict requirement at order time, so it likely stays synchronous or within one transaction boundary. Billing and email tolerate delay, so they are candidates for asynchronous handling. It explains the design that follows from this and what the customer experience becomes (pending payment status). It addresses failure scenarios: the broker or consumer being down, messages delivered more than once (so consumers need to be idempotent, especially billing, to avoid double charges), messages lost between saving the order and publishing it (for example a transactional outbox), poison messages and retries, payment failure compensation (cancel and release stock), and ordering. It considers operational cost for a team new to this, including monitoring and dead-letter handling, and compares with simpler options such as retries, timeouts and circuit breakers on the current synchronous call, or a durable queue only for billing. It recommends an approach or options with conditions. It lists open questions and does not invent numbers.

# Important Checks

- The three steps are analyzed separately against their consistency and latency needs.
- The customer-visible behavior change (pending payment) is stated.
- Duplicate delivery and double charge prevention are addressed.
- The gap between committing the order and publishing the event is addressed.
- Compensation for a failed payment is addressed.
- A simpler alternative is considered and compared.
- Operational overhead and team experience are part of the reasoning.
- Failure scenarios include the broker and consumers being unavailable.
- The response does not treat "event-driven" as automatically better.

# Failure Conditions

- Making all three steps asynchronous without considering overselling.
- Not addressing duplicate messages or double charging.
- Assuming exactly-once delivery without explanation.
- Not covering what happens if the event is not published after the order is saved.
- Ignoring the team's lack of experience and the operational burden.
- Naming a specific broker or framework as the answer with no reasoning.
- Inventing throughput, latency or cost figures.
- Ignoring the stated requirement that billing may be delayed by up to 5 minutes.

# Notes

More than one design is acceptable, including a hybrid with a synchronous stock reservation and an asynchronous billing step, or a durable queue only where needed. Evaluate how well the failure modes and trade-offs are understood.
