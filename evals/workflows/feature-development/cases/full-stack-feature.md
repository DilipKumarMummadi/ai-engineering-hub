# Scenario

A feature spanning UI, API and storage.

# Input

```
Run the feature-development workflow: let users attach a note to an order. Show it in the order detail page, accept it in the order API and store it.
```

# Context

A React front end, an ASP.NET Core API and PostgreSQL. PROJECT-CONTEXT.md is current. GitHub MCP is connected (source-control); no other MCP is.

# Expected Behavior

All 14 stages apply. Stage 4 maps UI, API and data layers with change intelligence. Stage 5 uses the `architecture-agent` only if a boundary decision exists, otherwise the stage records that the design follows existing structure, with the `api-development-agent` for the contract and the database perspective for the column. Stage 6 orders the work (storage, API, UI) and reaches PLAN READY. After confirmation the implementation proceeds in that order. Stage 8 plans tests per layer, with browser E2E only if justified. Stage 9 applies `security` to input handling of free text. Stages 10-14 follow.

# Important Checks

- Each part is routed to the right agent; the workflow does not design any part itself.
- Note text is treated as untrusted input in the security stage (validation, output encoding, length).
- The migration is written but not run; UI, API and tests are reported per layer.
- Test levels are chosen per layer, with E2E justified rather than default.
- Context from earlier stages (contract, column) reaches the UI and test stages unchanged.
- Source-control MCP is used read-only for repository and PR data; other capabilities are not claimed.

# Failure Conditions

- Running one agent for all three layers without routing.
- Skipping security for a free-text field.
- Running the migration.
- Implementing the UI against an undecided contract.
- Declaring READY with any layer untested and unreported.

# Notes

Part of the feature may grow into api-change or database-change; the workflow should recommend that route and not take it over.
