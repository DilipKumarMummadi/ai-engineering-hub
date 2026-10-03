---
name: reliability
description: Design and operate systems that stay available, recover correctly from failure and behave predictably under expected and unexpected conditions. Covers failure modes, timeouts, bounded retries, idempotency, duplicate processing, circuit breakers, graceful degradation, health checks, queues, background jobs, backups and disaster recovery with RTO and RPO derived from requirements. Use for resilience design and failure analysis; not for routine bug fixing.
---

# Reliability

## Purpose

Help engineers design and operate systems that remain available, recover correctly from failures and behave predictably under expected and unexpected conditions.

Topics it covers:

- Availability, fault tolerance, resilience, redundancy, failover
- Timeouts, retries, circuit breakers, bulkheads, graceful degradation
- Health checks
- Idempotency, duplicate processing, message delivery, queues, background jobs
- Dependency failures, distributed systems, Kubernetes and Azure considerations
- Backups, disaster recovery, RTO, RPO, SLA, SLO, SLI

**Failures are expected.** The question is what the system does when they happen.

## When to Use

- A system or feature needs a resilience design or review.
- A dependency is slow, unreliable or unavailable, and the system's behavior is unclear.
- Messages, jobs or requests may be duplicated, lost or processed out of order.
- A background job failed or may fail partway.
- Recovery expectations (RTO, RPO, backups) must be defined or checked.
- A post-incident review needs failure-mode analysis.

## When NOT to Use

- The task is a specific defect to find and fix. Use the [`debugging`](../debugging/SKILL.md) skill.
- The task is designing telemetry and alerts. Use the [`observability`](../observability/SKILL.md) skill.
- The task is overall system design. Use the [`architecture`](../architecture/SKILL.md) skill, and bring this skill in for resilience.
- The task is tuning speed. Use the [`performance`](../performance/SKILL.md) skill.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The system, function or incident in scope | Required | |
| Business requirements for availability and recovery (acceptable downtime, acceptable data loss) | Strongly preferred | RTO, RPO and SLOs are derived from these. Ask if they are missing. |
| Dependencies and how they are called (protocols, timeouts, retries, libraries) | Gathered as needed | Read the code and configuration. |
| Existing resilience mechanisms, health checks, backups | Gathered as needed | |
| Observed latencies and failure data | Optional | Use to set timeouts. Do not invent. |
| Incident timelines | Optional | |

## Process

```
Identify Critical Function → Identify Dependencies → Identify Failure Modes → Assess Impact
→ Design Resilience → Define Recovery → Test Failure Scenarios → Validate Recovery
```

1. **Identify the critical function.** Determine what must keep working and what can degrade. Rank by business impact.
2. **Identify dependencies.** List everything the function needs: services, databases, queues, caches, third parties, network, configuration, credentials, infrastructure.
3. **Identify failure modes.** For each dependency and step: it is down, slow, returns errors, returns wrong or partial data, delivers a message twice, delivers out of order, loses a message, or the process crashes midway. Also consider overload and resource exhaustion.
4. **Assess impact.** For each failure mode: who is affected, what breaks, how long, whether data can be lost or duplicated, and whether the failure can spread to other components (cascading failure).
5. **Design resilience.** Choose mechanisms that match the failure mode and impact (see the checklist). Prefer the simplest mechanism that meets the requirement.
6. **Define recovery.** Decide how the system returns to a correct state: automatic recovery, restart and resume, manual steps, restore from backup. Derive RTO and RPO from requirements.
7. **Test failure scenarios.** Plan tests that inject the failures identified: timeouts, errors, duplicates, crashes, dependency outages.
8. **Validate recovery.** Verify that the system recovers to a correct state within the targets, and that data is neither lost nor duplicated. Run restore and failover drills, not only backups.

### Design checklist

Use what applies.

- **Timeouts:** every call to an external dependency has a timeout, set from the observed latency and the overall latency budget. A library default is not a design. A default that is very long can exhaust threads or connections.
- **Retries:** retry only transient failures and only when it is safe. Bound the number of attempts, use exponential backoff with jitter, and respect an overall deadline. Retries multiply load on a struggling dependency, so avoid retry storms, including retries at several layers.
- **Idempotency:** retries, redelivery and job restarts mean operations run more than once. Make them idempotent (keys, unique constraints, conditional updates), or do not retry them.
- **Circuit breakers and bulkheads:** stop calling a failing dependency for a time, and isolate resources (pools, queues, threads) so one failing dependency cannot take everything down.
- **Graceful degradation:** decide intentionally what the system does without a dependency (cached value, default, reduced feature, clear error). A degraded mode must be acceptable to the business and visible to operators.
- **Health checks:** liveness answers "should the process be restarted?", readiness answers "should it receive traffic?". A check should reflect meaningful health. Checking every dependency in liveness can cause restarts that make an outage worse.
- **Messages and queues:** most brokers deliver at least once, so consumers must handle duplicates and out-of-order delivery. Use dead-letter handling for messages that keep failing, and bound the retries. Avoid losing messages between a database write and a publish (for example with a transactional outbox).
- **Background jobs:** make them resumable (checkpoints or per-item idempotency), detect non-completion with an alert, avoid overlapping runs, and define what happens on crash or eviction.
- **Redundancy and failover:** remove single points of failure where the requirement justifies the cost. Verify failover works, including data consistency after it.
- **Backups and disaster recovery:** backups that are not restored are unproven. Define what is backed up, how often, where it is stored, who can restore and how long a restore takes.
- **Kubernetes and Azure:** replicas and disruption budgets, resource requests and limits, probes, zone or region placement, managed-service redundancy and failover options.

### Targets

- **SLI:** a measured indicator of service behavior (for example the proportion of successful requests).
- **SLO:** the target for an SLI over a period.
- **SLA:** a commitment to customers, usually with consequences.
- **RTO:** how long the service may be unavailable after a failure.
- **RPO:** how much data loss, measured in time, is acceptable.

Do not assume targets. Derive them from stated requirements, or mark them as proposals to be agreed.

## Rules

- Assume failures will happen, and design the behavior for them.
- Every external dependency call must have a timeout.
- Retry only when appropriate: the failure is transient and the operation is idempotent or otherwise safe. Retries must be bounded, with backoff and jitter, and must not multiply across layers.
- Design for duplicate and out-of-order delivery. Do not assume exactly-once processing unless the mechanism is shown to provide it end to end.
- Avoid cascading failures with timeouts, limits, isolation and circuit breaking.
- Make graceful degradation intentional and agreed, not accidental.
- Health checks must reflect meaningful health and must not create failure loops.
- Do not assume RTO, RPO, SLA or SLO values. Derive them from requirements or ask.
- Do not fabricate incidents, failure data, latencies, test results or configuration.
- Separate observed facts, assumptions, hypotheses and recommendations.
- Do not run failure injection, restores or failover tests on production systems without explicit authorization.
- Prefer the simplest mechanism that meets the requirement. Each added mechanism has an operating cost.
- State what was and was not tested.
- List open questions.

## Output

```markdown
# Reliability Analysis

## Critical Functions

## Dependencies

## Failure Modes

## Current Resilience

## Reliability Risks

## Recommended Design

## Recovery Strategy

## RTO/RPO Considerations

## Testing

## Validation

## Operational Considerations

## Open Questions
```

Omit or shorten a section when it does not apply, and say why.

## Examples

Illustrative only.

**Input:** "Our checkout calls a shipping-rate service. When it slowed down last week, the whole site stopped responding. The HTTP client uses the library's default timeout and retries three times immediately."

**Response (abridged):**

```markdown
## Failure Modes

- Shipping service slow (observed in the incident): requests wait for the default timeout, so threads and connections are held until it expires.
- Immediate retries (observed in configuration): each checkout can produce up to four calls, so load on the struggling service rises just when it is weakest.

## Recommended Design

- Set a timeout from the service's normal latency and the checkout latency budget (needs real latency data).
- Retry only if the rate lookup is safe to repeat (a read usually is), with a small bound, backoff and jitter, and an overall deadline.
- Add a circuit breaker and a fallback that the business accepts (for example a flat rate or a cached rate), or a clear message. Agree the fallback with the business.
- Keep the failure from spreading by limiting how many concurrent calls can wait on this dependency.

## Testing

Inject latency and errors into the dependency in a test environment and confirm that checkout stays responsive. Not executed.
```

## Related Skills

- [`architecture`](../architecture/SKILL.md): resilience as part of system design and component boundaries.
- [`observability`](../observability/SKILL.md): the signals that detect failures and the SLOs that measure reliability.
- [`api-development`](../api-development/SKILL.md): idempotency, timeouts and retry behavior in API design.
- [`database-sql`](../database-sql/SKILL.md): transactions, backups and migrations' safety.
- [`debugging`](../debugging/SKILL.md): investigate failures that occur.
- [`performance`](../performance/SKILL.md): capacity and saturation problems.
