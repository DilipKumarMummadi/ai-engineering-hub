---
name: observability
description: Design and use observability to understand system behavior and diagnose issues. Covers logs, metrics, traces, correlation IDs, structured logging, dashboards, alerts, SLIs and SLOs, dependency monitoring, and incident analysis that separates signals, correlation, hypotheses and validated causes. Use for instrumentation design, alert design and reading telemetry during investigations; not for fixing the underlying defect.
---

# Observability

## Purpose

Help engineers design and use observability so they can understand system behavior and diagnose problems quickly. The skill selects useful signals, connects them, turns them into actionable dashboards and alerts, and guides incident analysis without confusing correlation with cause.

The core signals are **logs, metrics and traces**. Also consider events, audit logs and business metrics.

Topics it covers:

- Structured logging, correlation IDs, distributed tracing
- Metrics for errors, latency, throughput and saturation
- Dashboards and alerts, alert design
- SLIs, SLOs, availability
- Dependency monitoring, database observability, Kubernetes observability
- Azure Monitor, Application Insights, Grafana (when the project uses them)

Follow the project's existing tools and conventions. Do not assume a tool that the repository does not show.

## When to Use

- A new service or feature needs instrumentation.
- Logs, metrics or traces are missing, noisy or impossible to connect.
- An alert is noisy, late or not actionable, or a dashboard has no clear purpose.
- SLIs and SLOs need to be defined.
- An incident or anomaly is being investigated from telemetry.

## When NOT to Use

- The task is finding and fixing the defect once it is localized. Use the [`debugging`](../debugging/SKILL.md) skill.
- The task is measuring and tuning speed. Use the [`performance`](../performance/SKILL.md) skill, which relies on these signals.
- The task is failure handling design (retries, timeouts, failover). Use the [`reliability`](../reliability/SKILL.md) skill.
- The task is choosing a monitoring vendor or platform. Use the [`architecture`](../architecture/SKILL.md) skill.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The system or problem in scope | Required | |
| System description: services, dependencies, critical user journeys | Strongly preferred | |
| Existing telemetry: log samples, metric names, traces, dashboards, alert rules | Required for review or investigation | Use only what is provided. |
| Incident data: timeline, symptoms, recent changes | Required for investigation | |
| Service-level needs (availability, latency expectations) | Optional | SLOs are derived from these, not assumed. |
| Tooling in use | Optional | |

## Process

```
Understand System → Identify Important Signals → Define SLIs → Define SLOs Where Appropriate → Instrument
→ Correlate Signals → Create Dashboards → Create Alerts → Validate Operational Usefulness
```

1. **Understand the system.** Identify the critical user journeys, components and dependencies, and how the system fails.
2. **Identify important signals.** For each journey and component, choose signals that answer operational questions: is it working, is it slow, is it failing, what is it waiting for? Cover rate, errors, duration and saturation. Use more than one signal type.
3. **Define SLIs.** Pick measurable indicators of user-visible health, such as the proportion of successful requests and the proportion of requests faster than a threshold.
4. **Define SLOs where appropriate.** Set targets from user needs and business requirements. Do not assume a target. If none is given, ask or state the target as a proposal to be agreed.
5. **Instrument.** Add logs, metrics and trace spans at boundaries (incoming requests, outgoing calls, queue operations, database calls). Use structured logs with consistent field names, and propagate a trace or correlation context across every hop, including asynchronous ones.
6. **Correlate signals.** Make it possible to go from an alert to a metric, to a trace, to the logs for that request, using shared identifiers.
7. **Create dashboards.** Each dashboard answers a question for a named audience (for example "is checkout healthy?"), with the key SLIs first.
8. **Create alerts.** Alert on symptoms users feel (error rate or latency against an SLO) and keep cause-level signals (CPU, queue depth) for dashboards or lower-urgency alerts unless they predict an imminent impact. Each alert needs a clear meaning, an owner and a response.
9. **Validate operational usefulness.** Check with a realistic scenario (a past incident or a fault test): can the team detect it, find the cause and decide what to do? Review alerts regularly for noise and gaps.

### Good practice and things to avoid

- **Logging:** structured, leveled, with correlation IDs, enough context to act on, and proportionate volume. Avoid excessive logging, secrets, credentials and personal data in logs.
- **Metrics:** stable names, bounded label values (avoid user IDs or other unbounded values as labels), units in names, histograms for latency.
- **Tracing:** propagate the standard context across HTTP calls, messages and background jobs. Name spans by operation, not by instance values. Sample thoughtfully, and keep traces for errors and slow requests.
- **Dashboards:** avoid dashboards with no operational purpose or too many panels.
- **Alerts:** avoid noisy alerts, alerts that cannot be acted on, duplicate alerts for one problem, and reliance on a single signal.
- **Dependencies and infrastructure:** monitor outbound calls (rate, errors, latency per dependency), databases (connections, slow queries, locks), Kubernetes (restarts, pod state, resource limits) and cloud services (throttling, quotas).

### Incident analysis

Keep these levels distinct:

```
Observed Signal → Correlation → Hypothesis → Validation
```

- **Observed signal:** what the telemetry shows, with time and scope.
- **Correlation:** things that changed or moved together. A deployment at the same time as an error increase is a lead, not a cause.
- **Hypothesis:** an explanation that fits the signals and makes a testable prediction.
- **Validation:** a check that could disprove the hypothesis, such as comparing versions, isolating the component, or reproducing.

Do not claim a root cause from correlation alone. Note what the available data cannot show.

## Rules

- Distinguish observed signals, correlations, hypotheses and validated causes in every analysis.
- Do not claim root cause from correlation alone.
- Do not fabricate logs, metrics, traces, dashboards, alert history or incident facts.
- Derive SLOs from requirements. Do not invent targets.
- Alert on conditions that need a human response, and give each alert an owner, a meaning and a next step.
- Do not log secrets, credentials or unnecessary personal data. Redact sensitive fields.
- Keep metric label cardinality bounded.
- Do not depend on one signal when a conclusion matters. Cross-check logs, metrics and traces.
- Prefer the project's existing observability tools and conventions.
- Keep instrumentation proportionate. State its cost (volume, performance, money) when recommending more.
- Do not change alert routing or production telemetry configuration unless the user asks for it and authorizes it.
- List open questions and the data needed.

## Output

```markdown
# Observability Analysis

## System Context

## Important Signals

## Logging

## Metrics

## Tracing

## Correlation

## Dashboards

## Alerts

## SLO/SLI Considerations

## Incident Investigation

Observed signals, correlations, hypotheses and validation steps, kept separate.

## Risks

## Recommendations

## Open Questions
```

Omit or shorten a section when it does not apply, and say why.

## Examples

Illustrative only.

**Input:** "Error rate on checkout rose at 14:05. We deployed at 14:03. It's the deployment, right?"

**Response (abridged):**

```markdown
## Incident Investigation

- Observed signal: checkout error rate increased from 14:05 (as reported).
- Correlation: a deployment happened two minutes earlier. This makes it a strong lead.
- Hypothesis: the new version introduced the errors. It predicts that errors occur only on instances running the new version, and that they stop after a rollback.
- Not established: other changes near 14:05 (dependency behavior, traffic) have not been ruled out. The data provided does not show errors by version.

## Validation

Break the error rate down by version and by dependency. Check the failing requests' traces for the failing span. Decide on rollback based on that, or as a safe mitigation while the cause is confirmed.
```

## Related Skills

- [`debugging`](../debugging/SKILL.md): use the telemetry to locate and fix the defect.
- [`reliability`](../reliability/SKILL.md): SLOs, failure modes and the signals that detect them.
- [`performance`](../performance/SKILL.md): the measurements that performance work needs.
- [`security`](../security/SKILL.md): security logging, audit trails and keeping sensitive data out of telemetry.
- [`architecture`](../architecture/SKILL.md): observability as a design concern.
