# Production Incident Agent Evaluations

Evaluations for the [`production-incident-agent`](../../../.claude/agents/production-incident-agent.md). See the [evaluation suite overview](../../README.md) for the case format, outcomes and how to run a case, and section 14 of the [agent specification](../../../docs/agent-specification.md) for what agents are evaluated on.

## Purpose

To check that the agent handles an active incident the way a good incident responder would: assess impact, stabilize safely, read the evidence, keep facts and hypotheses apart, verify recovery, and leave root cause and prevention to the evidence.

## Expected Agent Behavior

- Establishes impact first and prioritizes user and business impact.
- Builds a timeline and reads multiple signals.
- Identifies the failure boundary and forms hypotheses without declaring a root cause early.
- Proposes reversible mitigation with its effect and risk, and leaves the action to the user's authorization.
- Defines what evidence shows recovery and does not claim recovery without it.
- Separates confirmed findings, contributing factors and root cause, and lists follow-up actions and prevention.
- Does not propose large refactors during an active incident unless needed to stabilize.
- Does not treat routine events as security incidents without evidence.

## Skill Selection Expectations

- `debugging`, `observability` and `reliability` are the core.
- `performance`, `database-sql`, `security`, `architecture` and `api-development` are added only when the evidence points to them.
- Follow-up architectural work is handed off, and is not done in the middle of the incident.

Judge selection by the reasoning and the actions proposed.

## Common Failure Modes

- Investigating root cause at length while impact continues.
- Declaring a cause from timing alone.
- Disruptive or irreversible mitigation without authorization or risk statement.
- Claiming recovery without evidence.
- Restarting or changing things in a way that destroys evidence without saying so.
- Treating a routine event as an attack, or ignoring a real security signal.
- Fabricated logs, metrics or timelines.
- Proposing redesigns mid-incident.

## Evaluation Process

1. Give the case's `# Input` and `# Context` to the agent.
2. Compare the response with Expected Behavior, Important Checks and Failure Conditions.
3. Judge prioritization, evidence use, mitigation safety, recovery validation, skill selection and output quality.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [api-latency-spike](cases/api-latency-spike.md) | Stabilizes a version-correlated latency spike while keeping correlation separate from cause. |
| [background-job-failure](cases/background-job-failure.md) | Handles a deadline-bound job failure after a routine credential change, without overreacting or double-processing. |
| [database-outage](cases/database-outage.md) | Separates a provider failover from stale application connections, and verifies recovery and data loss. |
