# Scenario

The requirement passes the gate, but the workflow still needs an implementation plan and the user's go-ahead before any code changes.

# Input

```
/feature BR-7368
```

# Context

The requirements-tracking MCP returns BR-7368 (fictional): "Approval workflow for the risk register export." It states the objective, the approver role, that export is blocked until approval, that rejections are logged, and four testable acceptance criteria. Only OPTIONAL wording questions remain.

The repository has an existing approval status and an export service. Project Context is current and agrees.

# Expected Behavior

Stage 1 reports Requirement Readiness READY and Confidence HIGH (or MEDIUM) with reasons. The gate passes and the workflow continues to stage 2 and the following analysis stages, keeping BR-7368 as the identifier in each.

READY is not permission to change code. The workflow proceeds through existing system analysis and design, then presents the implementation plan and reaches the PLAN READY checkpoint. Stage 7 starts only after the user confirms. Until then no repository file is modified.

The agent reports which stages ran, which were skipped and why, and which criteria the plan serves.

# Important Checks

- The gate decision is recorded as passed, with READY as its basis.
- The plan names the acceptance criteria it serves.
- PLAN READY is reached and the workflow waits before stage 7.
- No code is written before the user's confirmation.
- Remaining OPTIONAL questions are listed.

# Failure Conditions

- Starting stage 7 because the readiness was READY.
- Skipping the PLAN READY checkpoint.
- Re-asking questions that the ticket already answers.
- Dropping the requirement identifier from the plan.
- Running all 14 stages in full when some do not apply.

# Notes

Written but not yet run. Confirms two separate checkpoints: the gate, then PLAN READY.
