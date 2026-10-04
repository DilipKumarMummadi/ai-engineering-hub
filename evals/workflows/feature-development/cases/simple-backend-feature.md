# Scenario

A small, self-contained backend feature that fits existing structure. The workflow should stay light.

# Input

```
Run the feature-development workflow: add a `DaysSinceLastLogin` computed property to the existing `UserSummary` service response. No schema change, no new endpoint.
```

# Context

A .NET service with an existing `UserSummary` mapper, unit tests and a current PROJECT-CONTEXT.md. `last_login_at` is already stored.

# Expected Behavior

Stages 1-3 confirm the requirement (Confirmed/Inferred/Unknown) and read the repository and context. Stage 4 locates the mapper and its callers. Stage 5 (Architecture/Design) is skipped as the change fits the existing structure. Stage 6 produces a short plan and stops at PLAN READY. After confirmation, stages 7-8 implement and run the `test-planning-agent` plan with the `testing` skill. Stage 9 is skipped (no trust boundary, no sensitive data), stage 10 runs briefly, then review, PR preparation, PR Intelligence and final validation. Jira and GitHub MCP are used only if connected.

# Important Checks

- Stage 5 and stage 9 are recorded as skipped with a reason; no other stage is silently dropped.
- `architecture-agent`, `api-development-agent` and `database-troubleshooting-agent` are not invoked.
- PLAN READY is reached and confirmed before any file is edited; IMPLEMENTATION READY precedes validation.
- Existing test results are reported as run or not run, with command and outcome.
- Project Context is used for conventions and test approach, and repository evidence wins where they differ.
- The final readiness is READY only with passing tests and evidence; no migration or deployment is run.

# Failure Conditions

- Running architecture or security stages for a computed property.
- Editing code before PLAN READY is confirmed.
- Reporting READY without executing tests or stating they were not run.
- Starting api-change or database-change.
- Fabricating a requirement source or test output.

# Notes

The question is whether the workflow scales down. Running all 14 stages in full here fails orchestration even if each is well done.
