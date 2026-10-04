# Scenario

A small, local UI feature in an existing form. The workflow should stay light.

# Input

```
Run the feature-development workflow: add an optional "nickname" text field to the profile edit form and show it on the profile page. No backend changes, the API already returns a `nickname` property.
```

# Context

A React/TypeScript front end with an existing profile form, component tests and a current PROJECT-CONTEXT.md. The API already supports the field.

# Expected Behavior

Requirement is confirmed; stage 4 reads the form and page components. Stage 5 is skipped with a reason. Stage 6 plans the change and tests and stops at PLAN READY. After confirmation it implements, plans tests with the `test-planning-agent` (component level, no browser E2E unless justified), runs them, skips security review, runs code review and PR stages. No API or database workflow starts.

# Important Checks

- Stages 5 and 9 are recorded as skipped with reasons.
- `architecture-agent` and `api-development-agent` are not invoked.
- The browser-automation capability is not used, and `playwright` is applied only if an E2E test is actually justified.
- The "no backend changes" constraint is kept in every stage.
- Tests are run before any readiness other than NEEDS_INFORMATION or NEEDS_CHANGES is given.
- Implementation starts only after PLAN READY is confirmed.

# Failure Conditions

- Running architecture assessment for a one-field change.
- Starting api-change or database-change.
- Reporting READY without running tests.
- Dropping the "no backend changes" constraint.
- Restating testing guidance in the workflow instead of using the agent.

# Notes

A workflow that runs all 14 stages in full here has failed at orchestration even if each stage is well done.
