# Scenario

A small, local feature in an existing form. The workflow should stay light.

# Input

```
Run the feature-development workflow: add an optional "nickname" text field to the profile edit form. It is shown on the profile page. No backend changes, the API already returns a `nickname` property.
```

# Context

A front-end repository with an existing profile form and component tests. The API already supports the field.

# Expected Behavior

The workflow confirms the requirement, briefly looks at the existing form, plans and implements the change on request, plans tests with the `test-planning-agent`, runs them, reviews with the `pr-review-agent`, and validates. Architecture assessment and security review are skipped with reasons. No API or database workflow is started.

# Important Checks

- Stages 3 (architecture) and 7 (security) are recorded as skipped with a reason.
- `architecture-agent` and `api-development-agent` are not invoked.
- Implementation starts only after the plan and the user's go-ahead.
- Tests are planned and run before the workflow is reported complete.
- The "no backend changes" constraint is kept in every stage.

# Failure Conditions

- Running architecture assessment for a one-field change.
- Starting api-change or database-change.
- Reporting the workflow complete without running the tests.
- Dropping the "no backend changes" constraint.
- Restating testing guidance in the workflow's own words instead of using the agent.

# Notes

The question is whether the workflow scales down. A workflow that runs all ten stages here has failed at orchestration even if each stage is well done.
