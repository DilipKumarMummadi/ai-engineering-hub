# API Change Workflow Evaluations

Evaluations for the [`api-change`](../../../.claude/workflows/api-change.md) workflow. See the [workflow evaluation overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the workflow makes a compatibility decision before implementation, applies the security and persistence stages where they matter, and skips them where they do not.

## Expected Workflow Behavior

- Analyzes the existing API before designing the change.
- Classifies the change as breaking or non-breaking and treats unknown consumers as unknown.
- Stops for a versioning decision on a breaking change.
- Runs the persistence stage only when storage is touched, and routes migrations to database-change.
- Does not reduce the security stage for endpoints that return or change sensitive data.

## Cases

- [breaking-pagination-change.md](cases/breaking-pagination-change.md): a breaking change; checks the compatibility gate.
- [additive-endpoint.md](cases/additive-endpoint.md): an additive endpoint on existing storage; checks appropriate skipping.

## Common Failure Modes

- Implementing a breaking change without a versioning decision.
- Assuming there are no consumers.
- Skipping the security stage for a state-changing endpoint.
- Running the persistence stage when storage is untouched.
- Restating API design rules in the workflow.
