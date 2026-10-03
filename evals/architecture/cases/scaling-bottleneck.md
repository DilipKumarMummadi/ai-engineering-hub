# Scenario

A .NET API backed by PostgreSQL is getting slower as usage grows. The team plans to add more API instances and move to a larger Kubernetes cluster. The team lead asks for an architecture analysis of the scaling problem.

# Input

Our API response times are getting worse as traffic grows. We plan to double the number of API instances. Please analyze the situation and tell us how to scale.

# Context

Measurements the team has collected over the last week during peak hours:

- API: 6 instances, average CPU 30%, memory steady. Requests per second at peak is around 400.
- p95 latency of the API rose from 250 ms to 1.4 s over three months. The p50 rose from 80 ms to 120 ms.
- PostgreSQL primary: CPU at 85% at peak, up from 45% three months ago. Connection count is at 90% of the configured maximum.
- About 90% of the database load comes from `SELECT` statements. The top three statements by total time are: a dashboard summary query (runs on every page load, about 55% of total query time), a list-orders query, and an audit-log search.
- The dashboard summary aggregates the last 90 days of orders per customer. Its results change at most every few minutes.
- The database is one primary instance. No read replicas exist. The budget allows a modest increase.
- The team has 6 engineers and no dedicated database administrator.

# Expected Behavior

The response reads the measurements and locates the bottleneck: the database, not the API tier. API CPU is at 30%, while database CPU and connections are near their limits, and the slow tail (p95) grows much faster than the median, which suggests contention or heavy queries on a shared resource. It therefore explains that doubling API instances would likely not help and may make it worse by adding more database connections. It analyzes the main contributor, the dashboard summary, which is heavy, frequent and tolerant of staleness. It presents options with trade-offs: tuning the query and indexes, caching or precomputing the summary, moving read-heavy or reporting queries to a replica (with replication lag implications), connection pooling, and only then scaling the database vertically. It recommends measuring first for the specific queries (execution plans) and validating any change with the same metrics. It says what would change the recommendation and lists open questions. It does not invent figures.

# Important Checks

- The bottleneck is identified from the measurements, with the reasoning shown.
- The response says that adding API instances is unlikely to fix this, and why.
- Connection limits are considered as a risk of scaling out the API tier.
- The dashboard query's characteristics (frequency, staleness tolerance) are used.
- Options are compared with their trade-offs, including replica lag and cache invalidation.
- The order of actions is sensible: measure, cheap wins, then structural changes.
- A validation approach is given, using the same metrics.
- Costs and the small team size are considered.

# Failure Conditions

- Accepting the plan to double the API instances.
- Recommending microservices, sharding or a new data store with no link to the evidence.
- Ignoring the connection count.
- Ignoring the dashboard query that dominates the load.
- Inventing numbers that are not in the context.
- Suggesting a cache without addressing staleness and invalidation.
- Suggesting a read replica without noting replication lag.
- Making claims about the cause of the slow tail with certainty beyond the evidence.

# Notes

Several ordered plans are acceptable. The important part is reasoning from the data. A response that asks to see the execution plan for the dashboard query is behaving well.
