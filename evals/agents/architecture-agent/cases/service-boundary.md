# Scenario

A SaaS company runs a .NET modular monolith. An upcoming compliance audit will cover every system that stores or processes payment card data. The architect proposes extracting the billing module into its own service to shrink the audit scope. The team asks the Architecture Agent for an analysis.

# Input

We want to shrink our payment-card compliance audit scope. Our architect suggests moving the billing module into a separate service. Please analyze this and tell us what you recommend.

# Context

Requirements and constraints:

- The audit must cover any component that stores, processes or transmits card data. The auditor has said that scope is set by where card data flows, not by how the code is organized.
- Today the card number is entered in a web form, posted to the monolith, passed to a payment gateway and the last four digits and a gateway token are stored. The full number is held in memory during the request and is written to application logs by an older debugging statement (the team has just discovered this).
- The monolith has 9 engineers across 2 teams. It has one database shared by all modules. Billing reads and writes the `subscriptions`, `invoices` and `customers` tables, and the subscriptions module also writes `subscriptions`.
- The team has no production experience with running multiple services. The audit is in 6 months.
- The payment gateway offers hosted payment fields, where the card data goes from the customer's browser straight to the gateway and never reaches the company's servers. The team has not evaluated it.
- Billing currently has about 3% of the monolith's traffic.
- The company has no requirement to scale billing independently.

# Expected Behavior

The agent recognizes that the goal is to reduce where card data flows, and that extracting a service is one possible means and not a guaranteed one. It uses `architecture` with `security` (trust boundaries and sensitive data flows are central), and `database-sql` for data ownership, since billing shares tables with another module. It does not need `performance`, `observability` or `api-development` unless the analysis makes them relevant, and it does not run every supporting skill. It identifies that the full card number currently reaches the server, and appears in logs, so the first finding is about the data flow itself. It presents several options with trade-offs: adopt the gateway's hosted fields so card data never reaches the company's systems (potentially the largest reduction in scope, with front-end change and dependence on the gateway); keep billing in the monolith but tighten the boundary (remove card data from logs and memory paths, isolate access, separate credentials); extract a billing service (a smaller scope only if card data flows are actually confined to it, with the cost of running a new service, splitting shared tables and data ownership, and cross-service consistency for invoices and subscriptions). It notes that the audit scope depends on data flows and should be confirmed with the auditor, treats the log finding as needing immediate attention regardless of the architecture chosen, and explains timeline and team constraints. It recommends an approach or states what would decide it, lists a migration path with validation (for example a data-flow review and log scan), risks and open questions. It does not pick the service extraction only because the architect proposed it.

# Important Checks

- The agent reframes the problem around card data flow and audit scope.
- `security` and `database-sql` perspectives are visible, and unrelated supporting skills are not forced in.
- At least three materially different options are compared, including the hosted-fields option and a non-extraction option.
- The log finding is identified as a current problem that any option must address.
- The shared tables and data ownership cost of extraction are discussed.
- Team size, experience, timeline and operational cost are used in the reasoning.
- The recommendation is justified, or the deciding factors are stated. It is not presented as universally correct.
- The migration plan is incremental, with validation and risks.
- Open questions include confirming scope with the auditor.
- No facts or numbers are invented.

# Failure Conditions

- Endorsing service extraction without examining whether it reduces where card data flows.
- Missing that card data currently reaches the server and the logs.
- Ignoring the hosted-fields alternative.
- Presenting a single option as the only answer.
- Ignoring the shared database tables.
- Ignoring team experience and timeline.
- Claiming that extraction guarantees a smaller audit scope.
- Running analysis for performance, observability and others with no basis.
- Inventing compliance requirements or standards details beyond the context.

# Notes

The agent is not required to recommend any specific option. A recommendation of hosted fields, of tightening the monolith first, or of extraction after other steps can all pass if the reasoning follows the data flow and constraints.
