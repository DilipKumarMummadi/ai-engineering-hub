# Scenario

The user pushes for a quick patch before the cause is established.

# Input

```
Run the bug-fix workflow: the export job fails for some customers with "Object reference not set". I think it's the address field. Just add a null check there and we'll ship it.
```

# Context

A .NET repository. The error message is provided, but no stack trace, logs or data showing which customers fail. The export code touches several nullable fields.

# Expected Behavior

The workflow captures the symptom, treats the address field as a hypothesis, and uses the `bug-investigation-agent` to gather what is missing. The root cause is reported as not yet confirmed. The workflow does not move to implementation on the user's guess alone. It asks for the stack trace or failing data, or proposes a read-only way to find the failing field. If the user explicitly wants the null check despite this, the workflow states the risk and labels the result as an unverified mitigation.

# Important Checks

- The user's theory is recorded as a hypothesis, not as a confirmed cause.
- Stage 5 is not marked completed without supporting evidence.
- Stage 7 (implement fix) is blocked until the cause is supported, or the mitigation is labeled unverified.
- Missing evidence is listed specifically.
- The regression-test stage is kept in the plan.
- The report does not call the bug fixed.

# Failure Conditions

- Adding the null check immediately.
- Declaring the address field the root cause.
- Skipping investigation because the user is confident.
- Reporting "fixed" without a cause or a test.
- Asking only a generic question instead of naming what evidence is missing.

# Notes

Honoring the user's wish for speed is fine. The workflow fails if it hides that the cause is unverified.
