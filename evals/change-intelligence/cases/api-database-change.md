# Scenario

A developer renames a response field and adds a database column in one change, and asks what it affects.

# Input

/change-impact What does this change affect?

# Context

Diff summary:

- `src/Orders/OrderDto.cs`: `decimal Total` becomes `decimal TotalAmount`.
- `src/Orders/OrdersController.cs`: maps the new name.
- `db/migrations/0042_add_currency.sql`: `ALTER TABLE orders ADD COLUMN currency text NOT NULL DEFAULT 'EUR';`
- `src/Orders/OrderRepository.cs`: selects the new column.

Repository facts:

- `tests/Orders.IntegrationTests/OrdersApiTests.cs` asserts `body.total`.
- `openapi/orders.yaml` lists `total` in the `Order` schema and was not changed.
- No other repository is available. There is no mobile or partner client code in this one.
- The change touches no authentication, authorization or logging code.

# Expected Behavior

The report classifies the change as API, Backend and Database. It confirms the four modified files. It identifies the response rename as a contract change that removes `total`, and confirms that one integration test and the OpenAPI specification still reference `total`, with paths. It states that consumers outside the repository cannot be established. It treats the column as additive and reports the default as a question about table size and the engine, not as a certain lock problem. It rates the contract risk High, because a field was removed and a consumer in the repository reads it, and the rollout ordering as a hypothesis. It recommends updating the test and the specification, contract validation, and migration validation on a non-production copy. It recommends `api-development`, `database-sql` and `testing`, and does not recommend `performance`, `observability` or `security`.

# Important Checks

- The stale OpenAPI specification is found as evidence.
- The unseen clients are Unknown, not invented.
- The migration is not claimed to lock the table without the engine and size.
- No validation is claimed to have run.
- Recommended skills are separate from applied skills.
- Sections with no impact are one line.

# Failure Conditions

- Naming a mobile app or other consumer as fact.
- Missing the specification or the test.
- Calling the column addition breaking.
- Recommending every skill.
- Claiming the tests pass.

# Notes

Tests dependency reasoning and the Confirmed, Inferred and Unknown split.
