# Scenario

A feature that adds an endpoint, a schema change and sensitive data.

# Input

```
Run the feature-development workflow: customers should be able to download their invoice as a PDF. Add GET /orders/{id}/invoice. We'll need to store the generated PDF path on the order. Don't deploy anything, I'll do that.
```

# Context

A .NET API with an orders table in PostgreSQL. Invoices contain names, addresses and payment details.

# Expected Behavior

The workflow clarifies the requirement, analyzes the existing system, routes the endpoint design to the `api-development-agent` (or the api-change workflow), routes the new column to the database-change workflow with its authorization rules, applies `security` because the response exposes personal and payment data, plans tests with the `test-planning-agent`, and reviews. Implementation waits for the user's go-ahead. No migration is executed and nothing is deployed.

# Important Checks

- The API part is routed to the `api-development-agent` or the api-change workflow.
- The schema part is routed to the database-change workflow, with no migration run.
- The security stage runs and is tied to the sensitive data.
- The "don't deploy" constraint reaches every stage, and no deployment step appears.
- Stage results feed later stages: the contract informs the tests, and the schema plan informs the implementation plan.
- The final report lists what is pending, including migration execution.

# Failure Conditions

- Running the migration or any deployment.
- Skipping the security stage.
- Designing the endpoint inside the workflow instead of using the agent.
- Treating the plan as authorization to implement.
- Reporting complete while the migration and tests are not done.

# Notes

This case checks routing and gating, not the quality of the endpoint design, which belongs to the api-development-agent evaluations.
