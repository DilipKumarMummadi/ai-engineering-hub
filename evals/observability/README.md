# Observability Evaluations

Evaluations for the [`observability`](../../.claude/skills/observability/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the skill chooses useful signals, connects them, designs alerts that lead to action, and keeps correlation separate from root cause during investigations.

## Evaluation Principles

- Signals are chosen to answer operational questions, and more than one signal type is used.
- Requests can be followed across services through shared identifiers.
- Alerts reflect user impact and have a clear response.
- SLOs come from requirements, not assumption.
- Sensitive data is kept out of telemetry.
- Observed signals, correlations, hypotheses and validated causes are not mixed.
- Nothing is invented about the incident or the system.

## Expected Behavior

A good response states what the data shows and does not show, proposes specific instrumentation or alert changes tied to the problem, and gives validation steps. In investigations it names the leading hypothesis and how to test it, without declaring it the cause.

## Common Failure Modes

- Adding more logs, dashboards or alerts without purpose.
- Alerting on causes (CPU) and not on user impact.
- Declaring a root cause from timing alone.
- Logging secrets or personal data to help correlation.
- Correlating by timestamps alone without stating the uncertainty.
- Proposing a specific vendor as the answer.
- Assuming SLO targets.

## Qualitative Evaluation

Outcomes are Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [missing-correlation-id](cases/missing-correlation-id.md) | Designs correlation across services and handles the limits of weak correlation today. |
| [noisy-alert](cases/noisy-alert.md) | Redesigns an alert around user impact and action. |
| [distributed-request](cases/distributed-request.md) | Reads a trace, finds the critical path and keeps correlation separate from cause. |
