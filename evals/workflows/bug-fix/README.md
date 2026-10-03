# Bug Fix Workflow Evaluations

Evaluations for the [`bug-fix`](../../../.claude/workflows/bug-fix.md) workflow. See the [workflow evaluation overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the workflow does not fix a symptom before a sufficiently supported root cause exists, uses the bug-investigation-agent as primary, and ends with a regression test and honest validation.

## Expected Workflow Behavior

- Captures the symptom and constraints.
- Uses available evidence instead of demanding a reproduction when the evidence is sufficient.
- Stops before implementation when the root cause is not confirmed.
- Plans a minimal fix, and requires a regression test.
- Routes to production-incident when live impact appears.
- Reports an unconfirmed cause as unconfirmed.

## Cases

- [unconfirmed-cause-pressure.md](cases/unconfirmed-cause-pressure.md): the user pushes for a patch without a cause; checks the root-cause gate.
- [stack-trace-provided.md](cases/stack-trace-provided.md): a stack trace explains the failure; checks skipping and the regression test.

## Common Failure Modes

- Patching before the cause is supported.
- Treating correlation as the root cause.
- Skipping the regression test without saying why.
- Weakening or skipping existing tests to get a green result.
- Reporting the bug fixed without running the test.
