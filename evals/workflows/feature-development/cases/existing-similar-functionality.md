# Scenario

The requested feature mostly already exists.

# Input

```
Run the feature-development workflow: add an endpoint to export orders as CSV.
```

# Context

The repository already has `GET /invoices/export` and an `ExportService` with CSV support used by invoices. Orders have the same shape of data. PROJECT-CONTEXT.md is current.

# Expected Behavior

Stage 4 finds the existing export service and endpoint and reports them as reuse candidates with file evidence. Stage 5 recommends extending the service over a new implementation, noting differences for the user to decide. PLAN READY presents reuse against new as a choice. Stage 10 covers impact on invoice exports. The plan avoids duplicate code.

# Important Checks

- Existing functionality is found and cited with paths before any new design.
- The plan prefers reuse or extension and states why, or explains clearly why not.
- The user is asked where requirements differ, rather than assumed.
- Change intelligence covers the shared code's other callers.
- Tests include regression for the existing invoice export.
- Nothing is implemented before PLAN READY.

# Failure Conditions

- Building a parallel export service.
- Not searching the repository for existing behavior.
- Modifying the shared service without impact analysis.
- Claiming the existing code already meets the requirement without checking.
- Implementing before PLAN READY.

# Notes

This checks that stage 4 actually informs stage 5.
