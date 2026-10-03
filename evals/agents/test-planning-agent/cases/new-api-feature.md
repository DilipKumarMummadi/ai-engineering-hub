# Scenario

A banking-style .NET service is adding an endpoint for transferring money between accounts. The team asks the Test Planning Agent for a test plan before they start implementing.

# Input

We're building a new transfer endpoint. Please create a test plan for it.

# Context

Requirement:

`POST /api/v1/transfers` with body `{ "sourceAccountId": int, "destinationAccountId": int, "amount": decimal, "currency": "EUR" }` and a required header `Idempotency-Key`.

Business rules:

- `amount` must be greater than 0 and at most 10,000.00 per transfer. It has at most two decimal places.
- Only `EUR` is supported.
- Source and destination must be different accounts, and both must exist and be active.
- The source account must have enough available balance.
- The caller must own the source account. Users with the role `operator` may transfer from any account.
- Repeating a request with the same `Idempotency-Key` and the same body returns the original result without a second transfer. The same key with a different body is rejected.
- On success it returns 201 with the transfer id. The debit and credit happen together or not at all.

Facts:

- The service uses ASP.NET Core and PostgreSQL through EF Core. The team's existing tests use xUnit, and integration tests use a real PostgreSQL in a container.
- Authentication is a JWT with user id and role claims.
- The exact error response format follows the project's existing standard error format.
- There is no user interface for this feature in this release.
- The daily transfer limit per account has been discussed but is not part of this requirement.

# Expected Behavior

The agent identifies that this is an API feature with money and concurrency risk, and uses `testing` with `api-development`. It does not use `playwright`, since no browser behavior is involved, and states that no E2E tests are needed. It breaks the behavior into testable rules and assigns levels: the amount rules, currency support and the different-accounts check are pure logic, best as fast unit tests with boundary values (0, 0.01, 10,000.00, 10,000.01, three decimal places); the API behavior (status codes for validation errors, missing or invalid header, not found, inactive accounts, insufficient balance, authentication, and authorization for owner, non-owner and operator) belongs at the API or integration level; and the atomic debit and credit, the idempotency behavior under repeated and concurrent requests with the same key, and concurrent transfers that could overdraw an account need integration tests with a real database. It covers the same-key-different-body rejection and the error format. It plans test data (accounts with specific balances and states, users with roles) created per test with cleanup, avoiding dependence on test order, and names the dependencies (the database container and token creation). It covers failure handling such as a failure between debit and credit leaving no partial transfer. It notes the daily limit is out of scope but flags it as an open question, and lists other open questions such as the response for insufficient balance. It does not claim any test was run. It may recommend the testing skill for writing the tests.

# Important Checks

- Rules are split by level, with reasons: unit for logic and boundaries, API for contract and authorization, integration for atomicity and concurrency.
- Boundary values for the amount and decimals are specific.
- Authorization scenarios cover owner, non-owner and operator.
- Idempotency scenarios include same key and same body, same key with a different body, and concurrent duplicates.
- Atomicity and concurrent overdraw are covered at the integration level.
- No browser E2E tests are planned, and the agent says why.
- Test data, isolation and dependencies are described.
- Open questions and the out-of-scope limit are stated without inventing requirements.
- The plan does not claim execution.

# Failure Conditions

- Planning mostly browser or end-to-end tests.
- Including `playwright` scenarios for a feature with no user interface.
- Missing authorization, idempotency or concurrency scenarios.
- Generic scenarios without the specific values from the requirement.
- Inventing a daily limit or other rules as if they were requirements.
- Omitting test data or isolation.
- Mocking the database for the atomicity and concurrency tests.
- Claiming tests were written or executed.

# Notes

An agent may reasonably ask whether the idempotency key has an expiry, or what happens for a key reused after a failed attempt. These are good open questions.
