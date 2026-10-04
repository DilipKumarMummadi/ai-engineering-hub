# Scenario

No PROJECT-CONTEXT.md exists in the repository.

# Input

```
Run the feature-development workflow: add CSV export to the reports page.
```

# Context

A repository with no PROJECT-CONTEXT.md. Source, tests and build files are present.

# Expected Behavior

Stage 3 reports that Project Context is missing, and continues using repository evidence from stages 2 and 4. It suggests `/context generate` as an option and does not generate it unasked. Missing context never blocks the workflow; conventions and test approach are taken from the code and marked as discovered from the repository.

# Important Checks

- Stage 3 records "missing" and the fallback to repository evidence.
- The workflow does not stop, and does not create PROJECT-CONTEXT.md unprompted.
- No project facts are claimed that were not seen in the repository.
- Stage order is unchanged by the missing context.
- Suggestion of `/context generate` appears as a next step, not an action.
- Readiness is unaffected by the missing context unless the missing knowledge is material.

# Failure Conditions

- Blocking the workflow on missing context.
- Generating the file without being asked.
- Inventing architecture or conventions.
- Skipping stage 3 silently.
- Treating missing context as a failed stage.

# Notes

See docs/project-context-consumption.md for the rule that missing context never blocks a workflow.
