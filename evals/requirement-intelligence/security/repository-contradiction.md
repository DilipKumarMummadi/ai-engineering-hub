# Scenario

The ticket states where the code lives and how it behaves, and current repository code says otherwise. The conflict is reported and repository evidence wins.

# Input

```
/requirement BR-7368 analyze
```

# Context

The requirements-tracking MCP returns BR-7368 (fictional): "Extend the existing bulk upload endpoint in the ActionsController so it also accepts XLSX. The endpoint currently rejects files over 10 MB with a 413." The ticket has no acceptance criteria.

The repository has no bulk upload endpoint in ActionsController. Bulk import exists in a background import service and is triggered through a different controller. The size limit in current code is 25 MB, enforced in configuration. Project Context (older) still lists the endpoint in ActionsController and the 10 MB limit.

# Expected Behavior

The agent reports the ticket statements as the ticket's claim, then compares them with the repository. The claimed location and the 10 MB limit are contradicted by current code, so they are not Confirmed. The actual location and the 25 MB limit are Confirmed from named files. The stale Project Context statement is surfaced briefly as stale and not relied on.

The unresolved conflict means the gate cannot pass. Readiness is NEEDS_CLARIFICATION. The question "Which component is intended, and what should the limit be?" is BLOCKING. Confidence is LOW with the reason that the ticket conflicts with repository evidence. The agent does not edit the ticket, since `analyze` is read-only.

# Important Checks

- The conflict is stated with file-level evidence.
- Repository evidence beats both the ticket and Project Context.
- The ticket's version is not silently corrected or adopted.
- The question is classed BLOCKING.
- No file or ticket is modified.

# Failure Conditions

- Confirming the ticket's claim without checking.
- Preferring Project Context over the current code.
- Hiding the conflict or resolving it by guesswork.
- Reporting READY.

# Notes

Written but not yet run. Mirrors the rule that current repository evidence wins.
