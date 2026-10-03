# Scenario

A busy week of ordinary development: many source, test, comment and documentation edits, and no change to the shape of the repository. The case checks that none of it is called drift.

# Input

```
We merged a lot this week. Is PROJECT-CONTEXT.md out of date? Use the Project Context Drift Specification.
```

# Context

A .NET and React repository with a generated context. Changes since the context was written:

- `src/Shop.Api/Controllers/OrdersController.cs` rewritten; `NewController.cs` added.
- `src/shop-web/src/App.tsx` edited; new components added under `src/shop-web/src/`.
- A unit test added under `tests/Shop.Api.Tests/`.
- `README.md` rewritten; `docs/decisions.md` added.
- Comments changed throughout.
- `dist/` and `node_modules/` contents changed.

No manifest, pipeline, infrastructure, API definition or migration changed.

# Expected Behavior

Status NO DRIFT. The report may carry an Informational note about the volume of file changes if version control is available, and it says explicitly that file changes alone are not drift. CI mode exits 0. Nothing is written.

# Important Checks

- No Material or Potentially Material finding.
- The report does not list changed source files as findings.
- `dist/` and `node_modules/` are not scanned.
- A new `docs/` directory is at most Informational.
- Without version control the report still works and omits the note.

# Failure Conditions

- Reporting any source, test, comment or documentation change as drift.
- Failing CI.
- Treating the number of commits as a reason to regenerate.
- Depending on Git being present.

# Notes

This is the case that protects trust. If this case regresses, developers will stop reading the report.

The reference implementation reproduces this case as `EvalSourceOnlyChange` in `scripts/project-context/tests/test_drift_evals.py`. Related checks are in `test_drift.py`.
