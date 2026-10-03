# Debugging Evaluations

Evaluations for the [`debugging`](../../.claude/skills/debugging/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## What Is Being Evaluated

Whether the skill investigates a problem with evidence and reaches a supported root cause before proposing a fix, instead of jumping from the symptom to a patch.

## Evaluation Principles

- The response works from the evidence given and does not invent logs, traces or configuration.
- Observed facts, assumptions, hypotheses and the confirmed root cause are kept separate.
- A root cause is stated only when the evidence supports it.
- The fix addresses the underlying cause, not only the symptom.
- Regression prevention is specific to the problem.
- When information is missing, the response asks for the smallest useful addition.

## What a Good Response Contains

- The problem, with expected versus actual behavior.
- The evidence actually provided.
- The failure boundary (where it fails).
- A small number of hypotheses, with evidence for and against, and how to validate them.
- A root cause supported by the evidence, or a clear statement that it is not yet confirmed.
- A minimal fix, how to verify it, and regression prevention.

## Common Failure Modes

- Recommending a quick workaround first (a null check, a longer timeout, a retry) without finding the cause.
- Presenting a guess as the root cause.
- Ignoring evidence that was provided, or inventing evidence that was not.
- A long list of speculative hypotheses.
- Changing the test or the code before deciding which one is wrong.
- Generic advice that could apply to any failure.

## Scoring Approach

Qualitative only: Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). In these cases the context contains enough evidence to reach the cause, so a response that cannot reach it, or reaches a different one, should not pass.

## Cases

| Case | Tests |
| --- | --- |
| [null-reference](cases/null-reference.md) | Traces why an object is null instead of adding a null check. |
| [api-timeout](cases/api-timeout.md) | Finds the cause of a gateway timeout behind the symptom. |
| [test-failure](cases/test-failure.md) | Decides whether a failing test is a test defect or an application defect. |
