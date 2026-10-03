# Scenario

Product wants a customer's name split into first and last name in an API that has several consumers. The developer plans to replace the existing field. The team asks the API Development Agent to design the change.

# Input

Product wants separate `firstName` and `lastName` on customers. I was going to just replace `name` in `GET /api/v1/customers/{id}` and the create and update requests. Please design this change.

# Context

Current contract (v1):

```json
GET /api/v1/customers/42
{ "id": 42, "name": "Ana María Pérez", "email": "ana@example.com" }

POST /api/v1/customers      { "name": "...", "email": "..." }
PUT  /api/v1/customers/42   { "name": "...", "email": "..." }
```

Consumers:

- The company's web app, deployed together with the API.
- The mobile app. Released versions use `name`. Users update slowly, and the oldest supported version is about 8 months old. A new release takes about 2 weeks to reach most users.
- A partner integration that reads customers nightly and creates customers through the API. The partner's contract says v1 is supported for 12 months after notice of any change.
- An internal reporting job that reads `name` from the API.

Facts:

- Existing customers have `name` stored as one column. There is no reliable rule for splitting names (for example "Ana María Pérez", "Li Wei", "Madonna").
- Some customers are companies, not people.
- The API is versioned by path. The team has not retired a version before.
- The project uses OpenAPI documentation generated from the code, and has a contract test suite for the partner endpoints.

# Expected Behavior

The agent treats this as a compatibility problem first. It uses `api-development` as the core, `testing` for compatibility validation (contract tests), and `database-sql` for the data migration since splitting stored names is involved. It does not need `security`, `performance`, `reliability` or `architecture` for this change. It explains that replacing `name` would break the mobile app, the partner and the reporting job, including the partner's 12-month commitment. It proposes an additive, compatible evolution: keep `name` in v1 and add `firstName` and `lastName` as new optional fields; define precedence when a client sends `name` alone (store it, leave the split fields empty or null) versus new fields alone (compute `name` from them), versus both (define which wins or reject inconsistent input); keep `name` populated in responses from the stored data. It addresses data: do not guess a split for existing names; keep the new fields empty until users or staff provide them, and consider company customers that have no first and last name. It describes the deprecation path for `name` (announce, document, communicate to the partner, set a sunset date consistent with the 12-month commitment) and offers a new version only if a clean break is wanted later. It specifies validation rules and error responses for the new fields, updates to the OpenAPI documentation, and compatibility tests (existing clients' requests and responses unchanged, contract tests for the partner endpoints). It lists breaking changes avoided and any that remain, and open questions (how the web app will collect names, the sunset date). It does not implement anything unrequested or claim tests ran.

# Important Checks

- The planned replacement is identified as breaking, with each affected consumer named.
- The partner's 12-month commitment is used in the reasoning.
- An additive design keeps `name` working for reads and writes.
- Precedence rules for `name` versus the new fields are specified.
- Splitting existing names automatically is avoided, with the reason.
- Company customers and name formats are considered.
- A deprecation and communication path is proposed.
- Compatibility tests and documentation updates are planned.
- Skills used match the case, and unrelated skills are not forced in.
- No implementation or test result is claimed.

# Failure Conditions

- Agreeing to replace `name`.
- Creating v2 immediately without considering an additive change, or ignoring the partner's commitment.
- Auto-splitting existing names on spaces.
- Leaving the write behavior for old clients undefined.
- Ignoring the mobile app's slow update cycle.
- No compatibility testing.
- Removing `name` from responses.
- Inventing additional consumers or requirements.
- Claiming to have implemented or tested the change.

# Notes

Introducing a v2 later is acceptable as a long-term option. The case tests whether the agent reaches for the compatible path first and treats the break as a decision with a cost.
