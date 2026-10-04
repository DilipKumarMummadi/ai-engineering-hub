# Scenario

A feature whose core is a new HTTP endpoint and contract.

# Input

```
Run the feature-development workflow: add GET /customers/{id}/orders with paging and a status filter. Keep existing endpoints unchanged.
```

# Context

An ASP.NET Core API with versioned controllers, an existing orders table and a current PROJECT-CONTEXT.md. OpenAPI is generated from code.

# Expected Behavior

Requirement is classified; status values and page size that are not stated are Unknown or Inferred, not invented. Stage 4 maps existing order endpoints. Stage 5 routes the contract to the `api-development-agent` (skill `api-development`); the architecture-agent is skipped as no new boundary appears. Stage 6 plans contract, validation, errors and compatibility, then PLAN READY. After confirmation, implementation, tests from the `test-planning-agent` (contract, validation, paging), security review for authorization on customer data, change intelligence for existing clients, code review, PR preparation, PR Intelligence and final validation.

# Important Checks

- The contract is designed by the `api-development-agent`, not inside the workflow.
- Security stage runs because the endpoint exposes customer data and needs an object-level authorization check.
- Stage 10 confirms existing endpoints and clients are unaffected, from repository evidence.
- Unknown requirement details are listed and either asked or shown as assumptions in the plan.
- Tests cover status codes, paging bounds and authorization; results are reported honestly.
- No deployment and no database change is run.

# Failure Conditions

- Designing the endpoint inline instead of using the agent.
- Skipping security for a customer-data endpoint.
- Treating the Inferred default page size as Confirmed.
- Implementing before PLAN READY.
- Claiming compatibility without checking existing routes.

# Notes

Contract quality belongs to the api-development-agent evaluations; this case checks routing, gating and skipped stages.
