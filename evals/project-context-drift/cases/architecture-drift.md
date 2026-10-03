# Scenario

A new service project was added and a documented application was removed. The case checks that structural changes are detected, and that edits inside an existing project are not.

# Input

```
Has the architecture described in PROJECT-CONTEXT.md changed? Use the Project Context Drift Specification.
```

# Context

The existing context (generated) lists application components `src/Shop.Api` (ASP.NET Core) and `src/shop-web` (Node.js package), and library projects `Shop.Application`, `Shop.Domain`, `Shop.Infrastructure`.

Current repository:

- `src/Payment/Payment.csproj` exists (Worker SDK project).
- `src/shop-web/` has been deleted.
- `src/Shop.Api/Controllers/OrdersController.cs` has been edited, and `src/Shop.Domain/Order.cs` was added.

# Expected Behavior

- **Potentially Material:** a new project `src/Payment` is detected. Evidence: `src/Payment/Payment.csproj`.
- **Material:** `src/shop-web` is documented but no longer detected.
- Technologies that disappeared with `shop-web` (for example React) are also reported, under Technology.
- The edited controller and the new domain class are not reported.

Status is DRIFT DETECTED.

# Important Checks

- A new project is Potentially Material; a removed documented application is Material.
- The report names the path of each project.
- No finding is produced for files inside an existing project.
- The removed application appears under Stale Context as a quoted statement, not as a deletion.

# Failure Conditions

- Reporting `OrdersController.cs` or `Order.cs`.
- Missing the new project because the solution file was not changed.
- Declaring an architecture style ("now microservices").
- Marking the new project Material without a reason, or ignoring it.

# Notes

Adding a project is a prompt to look, not proof that the context is wrong. Deleting an application the context describes is proof.

The reference implementation reproduces this case as `EvalArchitectureDrift` in `scripts/project-context/tests/test_drift_evals.py`. Related checks are in `test_drift.py`.
