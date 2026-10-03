# Reliability Evaluations

Evaluations for the [`reliability`](../../.claude/skills/reliability/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the skill reasons about how systems fail, chooses safe retry, timeout and recovery behavior, handles duplicate processing, and designs degradation and recovery that match requirements.

## Evaluation Principles

- Failure modes are enumerated from the dependencies and steps involved.
- Timeouts exist and are derived from evidence. Retries are bounded, backed off and only used where safe.
- Duplicate delivery and restarts are expected, and idempotency is designed in.
- Degraded behavior is intentional and agreed with the business.
- Recovery targets (RTO, RPO, SLO) come from requirements, not assumption.
- Testing of failure scenarios and recovery is part of the answer.
- Nothing is invented about the system.

## Expected Behavior

A good response names the critical function, walks through what can fail and what each failure does, proposes mechanisms sized to the requirement, describes how recovery works and how it will be tested, and lists open questions.

## Common Failure Modes

- "Just add retries" without regard to idempotency or load.
- Unbounded or immediate retries.
- Assuming exactly-once delivery.
- Health checks that cause restart loops.
- Ignoring what happens between a write and a publish, or in the middle of a job.
- Inventing RTO or RPO.
- Over-engineering (multi-region, new infrastructure) for a modest requirement.

## Qualitative Evaluation

Outcomes are Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [dependency-timeout](cases/dependency-timeout.md) | Timeout, retry, circuit breaker and degradation design for a slow dependency. |
| [duplicate-message](cases/duplicate-message.md) | Idempotent handling of at-least-once message delivery. |
| [background-job-failure](cases/background-job-failure.md) | Making a long job resumable, safe to re-run and detectable when it fails. |
