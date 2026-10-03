# Scenario

A SaaS product built with ASP.NET Core and PostgreSQL is adding customer subscriptions. The team asks the API Development Agent to design the API before implementation.

# Input

Please design the API for customer subscriptions: create, list, change plan and cancel. Include the contract, validation, errors and anything else that matters.

# Context

Requirements:

- A customer can have many subscriptions over time, but **at most one active subscription** at any moment.
- Creating a subscription requires a `planId` (one of the plans in the `plans` table) and starts it immediately.
- Changing plan takes effect at the next billing date. Until then the subscription shows its current plan and a pending plan.
- Cancelling ends the subscription at the end of the current billing period. A cancelled subscription cannot be changed.
- A customer can see and change only their own subscriptions. Users with the role `support` can view any subscription and cancel it, but not create or change plans.
- The list returns a customer's subscriptions, newest first. A customer rarely has more than 20, but support staff list by customer.

Facts:

- Existing endpoints use JSON with camelCase, JWT bearer authentication with `sub` (customer id) and `role` claims, and paths like `/api/v1/customers/{customerId}/invoices`.
- The project returns errors in the problem details format.
- The `Subscription` entity has internal fields: `BillingCycleAnchor`, `InternalNotes` and `StripeSubscriptionId`.
- The API will be called by the company's web app, and later by partners.
- The database is PostgreSQL through EF Core.

# Expected Behavior

The agent designs the API for the requirement and its existing style. It uses `api-development` as the core, `security` because access depends on owner and role (object-level authorization), and `database-sql` because the "at most one active subscription" rule is a uniqueness and concurrency requirement that should be enforced in the database and not only in code. It uses `testing` only if asked about tests, and does not need `performance`, `reliability` or `architecture` for this requirement. It defines resources under the customer path consistently with the existing API, operations with correct methods and status codes (create returns 201 with location, list returns 200, plan change and cancellation as state changes with clear semantics, conflicts as 409), DTOs that exclude the internal fields, validation of `planId`, and error responses in the project's format. It separates authentication from authorization: the customer in the token must match the path's customer, support has read and cancel permissions only, and the response for a subscription outside the caller's access is consistent. For the uniqueness rule, it proposes a database constraint (in PostgreSQL, a partial unique index on the customer for active subscriptions) and handling the resulting conflict as a 409, and explains why checking in code alone fails under concurrent requests. It covers the pending plan representation in the response, the rule that a cancelled subscription cannot change, idempotency for retried creation requests, pagination and ordering for the list, the OpenAPI documentation and compatibility expectations for later partner use (versioned path, additive changes). It lists open questions, such as whether plan changes can be reverted before the billing date. It does not claim tests were run.

# Important Checks

- Endpoints follow the existing path style, methods and status codes are correct.
- Internal fields are excluded from the response model.
- Authorization covers owner and `support` separately from authentication.
- The one-active-subscription rule is enforced at the database level, with 409 on conflict, and concurrency is explained.
- The pending plan and state rules (cancelled cannot change) are handled with clear errors.
- Validation and the error format are specified.
- Idempotency of creation is considered.
- Documentation and compatibility are addressed.
- Skills used match the case (api, security, database), and performance, reliability and architecture are not forced in.
- Open questions are listed, and no tests are claimed.

# Failure Conditions

- Returning the entity or exposing internal fields.
- Checking authorization only by role or only by login.
- Enforcing the single active subscription only in application code.
- Wrong methods or status codes (200 for errors, 500 for conflicts).
- Ignoring the existing API style or the error format.
- Missing the rules for pending plans or cancelled subscriptions.
- Running analysis for unrelated concerns.
- Claiming that the API was tested or implemented.
- Inventing requirements.

# Notes

Several endpoint designs are acceptable (for example a sub-resource for cancellation or a `PATCH`). The agent is judged on consistency, correct semantics and handling of the rules.
