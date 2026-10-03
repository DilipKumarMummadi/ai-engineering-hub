---
name: performance
description: Investigate and improve application performance using measurement rather than assumptions. Covers CPU, memory, latency, throughput, database and API performance, N+1 queries, caching, async processing, connection pools, React rendering, and Kubernetes and Azure resource usage. Use to diagnose slowness or resource problems and to plan measured optimizations; not for restructuring code without a performance goal.
---

# Performance

## Purpose

Help engineers investigate and improve application performance using evidence. The principle is **measure before optimizing**: no change is recommended as a fix until a bottleneck is supported by measurements, and no improvement is claimed without measuring again.

Topics it covers:

- CPU, memory, latency, throughput
- Database performance, EF Core and SQL, connection pools
- API and network latency, serialization
- Frontend performance and rendering, React performance
- Caching, asynchronous processing, concurrency
- Distributed systems, Kubernetes resource usage, Azure services

## When to Use

- A request, page, job or query is slower than expected.
- Resource use (CPU, memory, connections, I/O) is high or growing.
- Throughput or scalability does not meet a requirement.
- A change may affect performance and needs a measured check.
- Someone proposes an optimization and the need for it is unclear.

## When NOT to Use

- The problem is a functional bug. Use the [`debugging`](../debugging/SKILL.md) skill.
- The task is a design change for scale beyond a single bottleneck. Use the [`architecture`](../architecture/SKILL.md) skill.
- The task is purely query correctness or schema design. Use the [`database-sql`](../database-sql/SKILL.md) skill, and come back here for measured tuning.
- The task is restructuring code for readability. Use the [`refactoring`](../refactoring/SKILL.md) skill.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The symptom (what is slow or heavy, for whom, when) | Required | |
| Expected performance (target or requirement) | Strongly preferred | Without a target, "fast enough" cannot be judged. Ask. |
| Measurements: timings, traces, profiles, metrics, query logs, execution plans | Required for conclusions | Use only data actually provided. |
| Workload and data size | Strongly preferred | |
| Code and configuration on the path | Gathered as needed | |
| Environment (production or test, resources, versions) | Optional | |
| Recent changes | Optional | |

If no measurements exist, the first recommendation is how to obtain them. Do not guess a bottleneck.

## Process

```
Define Problem → Establish Baseline → Collect Evidence → Identify Bottleneck → Form Hypothesis
→ Test Hypothesis → Optimize → Measure Again → Validate Regression
```

1. **Define the performance problem.** State what is slow, how slow, for which operation and users, and what is expected.
2. **Establish the baseline.** Record current numbers under a known workload (for example p50, p95 and p99 latency, throughput, error rate, CPU, memory, query counts). Prefer percentiles over averages.
3. **Collect evidence.** Use traces, profilers, metrics, query logs and execution plans to see where the time or resource goes. Break total time into parts.
4. **Identify the bottleneck.** Find the component that dominates the time or limits throughput. Label it:
   - **Observed performance issue:** measured symptom.
   - **Suspected bottleneck:** consistent with the evidence, not yet tested.
   - **Confirmed bottleneck:** shown by a test or clear measurement.
5. **Form a hypothesis.** State what change should help and why, with the number it should move.
6. **Test the hypothesis.** Change one thing, in a representative environment, and measure. If the measurement is unavailable, give the steps to obtain it.
7. **Optimize.** Make the smallest change that addresses the confirmed bottleneck, following project conventions.
8. **Measure again.** Compare to the baseline with the same method and workload. Report the actual change. If it did not help, say so and revisit the hypothesis.
9. **Validate regression.** Check that correctness is unchanged, note trade-offs (memory, staleness, complexity), and recommend a guard: a performance test, a budget, a metric and an alert.

### Common causes and mistakes

Use what applies, as prompts for hypotheses, not as conclusions.

- **Premature optimization:** optimizing something that was never shown to matter.
- **Unnecessary caching:** adds staleness and invalidation problems. Justify with hit rate, cost of the uncached call and tolerance for stale data.
- **Excessive database calls and N+1 queries:** many small queries where one would do. Check query counts per request.
- **Unbounded queries and poor pagination:** no limit, large result sets, deep offset pagination.
- **Missing or unsuited indexes:** confirm with the plan and the query pattern before adding, and consider write cost.
- **Inefficient serialization and large payloads:** oversized responses, repeated conversion.
- **Unnecessary API calls and sequential I/O:** independent calls made one after another, calls repeated in loops.
- **Synchronous blocking:** blocking threads on I/O, thread pool starvation, locks held too long.
- **Connection pool exhaustion:** connections held across slow operations, pool too small or leaked.
- **Excessive logging:** large volume or synchronous logging on hot paths.
- **Excessive React rendering:** state kept too high in the tree, unstable props, large lists rendered in full. Use the profiler to see what rendered and why.
- **Memory:** large allocations, retained references, unbounded collections, frequent garbage collection.
- **Kubernetes and Azure:** resource requests and limits, CPU throttling, autoscaling signals, service tier limits and throttling.

## Rules

- Measure before optimizing. Do not recommend an optimization as the fix without evidence of the bottleneck.
- Do not claim a performance improvement without measurements taken before and after.
- State expected impact as a hypothesis, with how it will be measured. Never invent benchmark numbers.
- Distinguish observed issues, suspected bottlenecks and confirmed bottlenecks.
- Use percentiles and representative workloads. Averages and single runs can mislead.
- Change one variable at a time when testing a hypothesis.
- Prefer removing work (fewer calls, less data) over adding mechanisms (caches, queues), and justify any added mechanism.
- Consider correctness, consistency and operational cost of each optimization.
- Do not add caching, indexes, parallelism or scaling as a reflex.
- Check that a fix does not move the bottleneck to a shared resource, for example more parallel calls exhausting a connection pool.
- Do not run load tests or profilers on production systems unless the user authorizes it.
- Do not fabricate traces, profiles, metrics, plans or test results.
- Follow the project's stack and conventions.
- List open questions and missing measurements.

## Output

```markdown
# Performance Analysis

## Problem

## Expected Performance

## Baseline

## Evidence

## Bottleneck

Observed / Suspected / Confirmed, with the reasoning.

## Hypotheses

## Recommended Changes

## Expected Impact

A hypothesis to be measured, not a claim.

## Validation

How to measure again and compare to the baseline.

## Regression Risks

## Open Questions
```

## Examples

Illustrative only.

**Input:** "The order details page takes 2.6 s. Let's add Redis caching." A trace of one request shows: authentication 10 ms, one database query 150 ms, and eight sequential calls to the inventory service of about 300 ms each.

**Response (abridged):**

```markdown
## Evidence

- Observed (one trace): 2.6 s total. The eight inventory calls take about 2.4 s, the database 150 ms.

## Bottleneck

Suspected: sequential inventory calls, about 90% of this trace's time. Not yet confirmed, since one trace is one sample.

## Recommended Changes

- Check whether the inventory service has a batch endpoint, or whether the calls can be made in parallel with a bounded degree.
- Caching the database query would not address the dominant cost. Cache the inventory results only if stale values are acceptable.

## Validation

Collect p50/p95 for the endpoint under normal load, make the change, repeat with the same workload, and compare. Confirm with a few more traces that the pattern holds.
```

## Related Skills

- [`database-sql`](../database-sql/SKILL.md): query plans, indexes and transactions behind slow queries.
- [`api-development`](../api-development/SKILL.md): pagination, payload size, resilience and API design.
- [`observability`](../observability/SKILL.md): the metrics, traces and logs that provide the evidence.
- [`debugging`](../debugging/SKILL.md): the evidence-driven method also used here.
- [`testing`](../testing/SKILL.md): tests that guard against performance regressions, including for React components.
- [`architecture`](../architecture/SKILL.md): when the fix is structural.
