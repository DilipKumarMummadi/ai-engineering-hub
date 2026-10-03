# Bug Investigation Agent Evaluations

Evaluations for the [`bug-investigation-agent`](../../../.claude/agents/bug-investigation-agent.md). See the [evaluation suite overview](../../README.md) for the case format, outcomes and how to run a case, and section 14 of the [agent specification](../../../docs/agent-specification.md) for what agents are evaluated on.

## Purpose

To check that the agent investigates from the symptom and evidence to a validated root cause, uses the perspectives the evidence points to, and does not conclude early.

## Expected Agent Behavior

- Starts from the actual symptom and builds a timeline where it helps.
- Identifies the failure boundary and separates observed, assumed, hypothesized and confirmed statements.
- Forms more than one hypothesis when the evidence allows, and looks for evidence against the leading one.
- States a root cause only when the evidence supports it, and otherwise says it is not yet confirmed.
- Recommends the smallest fix for the cause, with stabilization options when production is affected, and leaves disruptive actions for the user to authorize.
- Adds regression prevention and lists missing information.
- Stays read-only and never fabricates logs, metrics or results.

## Skill Selection Expectations

- `debugging` is the core.
- `observability`, `database-sql`, `performance`, `reliability`, `security` and `architecture` are added only when the evidence points there.
- Skills with no connection to the evidence are not used.

Judge selection by the perspectives visible in the reasoning, not by names being mentioned.

## Common Failure Modes

- Jumping to a fix (a null check, a longer timeout, a retry) before the cause is known.
- Declaring a root cause from correlation or a single sample.
- Ignoring evidence that was provided, or inventing evidence that was not.
- Confirmation bias: not considering alternatives.
- Taking or recommending disruptive production actions without authorization.
- Using every available skill regardless of evidence.
- Recommending unrelated refactoring during an incident.

## Evaluation Process

1. Give the case's `# Input` and `# Context` to the agent.
2. Compare the investigation with Expected Behavior, Important Checks and Failure Conditions.
3. Judge the reasoning, evidence use, hypothesis handling, skill selection, safety, handoff and output quality.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [api-500-error](cases/api-500-error.md) | Traces an intermittent 500 to its data cause using logs, data and a code change, without a bare null check. |
| [database-timeout](cases/database-timeout.md) | Reads a lock chain, finds the blocker and handles stabilization safely. |
| [intermittent-background-job](cases/intermittent-background-job.md) | Explains an intermittent job failure from run overlap and deadlock evidence. |
