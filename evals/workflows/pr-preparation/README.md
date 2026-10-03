# PR Preparation Workflow Evaluations

Evaluations for the [`pr-preparation`](../../../.claude/workflows/pr-preparation.md) workflow. See the [workflow evaluation overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the workflow applies only the reviews the change needs, runs validation for real, and prepares a PR summary that matches the diff and states what was and was not tested.

## Expected Workflow Behavior

- Classifies the change before choosing reviews.
- Uses the pr-review-agent as primary.
- Skips security, performance and architecture reviews when they do not apply.
- Reports tests and builds as run or not run, truthfully.
- Does not push, open, approve or merge anything.

## Cases

- [docs-only-change.md](cases/docs-only-change.md): a documentation change; checks that irrelevant reviews are skipped.
- [security-sensitive-change.md](cases/security-sensitive-change.md): a sensitive change where tests cannot run; checks relevant reviews and honest validation.

## Common Failure Modes

- Running every review on every change.
- Skipping the security review for an authorization change.
- Claiming tests passed when they were not run.
- A PR summary that does not match the diff.
- Opening or merging the PR without authorization.
