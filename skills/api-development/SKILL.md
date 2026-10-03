---
name: api-development
description: Design, implement, review and improve APIs. Covers REST and HTTP semantics, resource modeling, contracts, validation, error handling, status codes, pagination, versioning, authentication and authorization, idempotency, concurrency, resilience, documentation and compatibility, with ASP.NET Core as a worked technology. Use for API design and API changes; not for system-level architecture or database design.
---

# API Development

## Purpose

Help engineers design, implement, review and improve APIs that are correct, consistent, secure, compatible and operable.

Topics it covers:

- REST APIs and HTTP semantics (methods, status codes, headers)
- Endpoint design and resource modeling
- Request and response contracts, validation
- Error handling and error models
- Pagination, filtering, sorting
- Versioning and backward compatibility
- Authentication and authorization
- Idempotency, concurrency, rate limiting
- Retries and timeouts for dependencies
- API documentation and OpenAPI
- Observability and testing

Follow the repository's existing API style and framework. For .NET repositories, this skill considers ASP.NET Core (controllers, minimal APIs, middleware, dependency injection, DTOs, model validation) and EF Core. Do not assume a framework the repository does not use.

## When to Use

- A new endpoint or API needs to be designed or implemented.
- An existing API is being changed, reviewed or documented.
- API behavior is unclear or inconsistent (status codes, errors, validation, pagination).
- A change may break API consumers.

## When NOT to Use

- The task is choosing service boundaries or communication patterns across a system. Use the [`architecture`](../architecture/SKILL.md) skill.
- The task is schema or query design. Use the [`database-sql`](../database-sql/SKILL.md) skill.
- The task is a general code review. Use the [`code-review`](../code-review/SKILL.md) skill.
- The task is investigating a failing request. Use the [`debugging`](../debugging/SKILL.md) skill.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The requirement or API change | Required | What consumers need to do. |
| Existing API code, contracts and OpenAPI documents | Gathered as needed | Match the existing style. |
| Consumers and their constraints | Strongly preferred for changes | Needed to judge compatibility. |
| Security context (who may call, what data) | Strongly preferred | Needed for authorization. |
| Domain model and persistence | Gathered as needed | |
| Non-functional needs (latency, volume, retries by clients) | Optional | |

Ask for missing information that materially changes the design. List open questions rather than guessing.

## Process

1. **Understand the requirement.** What must consumers accomplish, and who are they?
2. **Identify the resource or domain.** Model nouns and relationships, not operations. Follow existing naming.
3. **Define the contract.** Endpoints, methods, request and response shapes, headers, status codes. Use methods for their meaning: GET is safe and idempotent, PUT and DELETE are idempotent, POST creates or performs non-idempotent actions, PATCH applies partial updates.
4. **Define validation.** Validate at the boundary: required fields, types, ranges, formats, sizes, allowed values. Reject invalid input with a clear client error.
5. **Define the error model.** Use one consistent error shape across the API (for ASP.NET Core, consider the standard problem details format if the project uses it). Map failures to correct status codes. Do not leak stack traces, SQL or internal details.
6. **Define security.** Authentication identifies the caller. Authorization decides what that caller may do with this resource. Decide them separately, and check object-level access (can this user see this record?), not only the endpoint.
7. **Define persistence and dependencies.** What data is read and written, transaction boundaries, downstream calls. Define timeouts, retries and failure behavior for dependencies.
8. **Implement.** Follow project conventions. Keep handlers thin. Map between internal models and DTOs.
9. **Test.** Cover status codes, validation, authorization (allowed and denied), error responses, boundary inputs and idempotency where relevant.
10. **Document.** Update OpenAPI or the project's API documentation to match the actual behavior.
11. **Validate compatibility.** Check that existing consumers are not broken.

### Design checklist

Use what applies.

- **HTTP semantics:** correct methods and status codes (for example 200, 201 with location, 204, 400, 401, 403, 404, 409, 412, 422, 429, 5xx). Do not return 200 with an error body.
- **Resource modeling:** stable identifiers, consistent plural/singular and casing, sub-resources only for real ownership.
- **Contracts:** explicit DTOs. Do not expose database entities or internal fields unnecessarily. Avoid returning data the caller is not allowed to see.
- **Collections:** pagination with a stable order, bounded page sizes, documented filtering and sorting. Prefer the project's existing scheme.
- **Versioning and compatibility:** adding optional fields is usually compatible. Removing or renaming fields, changing types or meaning, tightening validation, or changing status codes can break consumers. Use the project's versioning approach for breaking changes.
- **Idempotency:** PUT and DELETE should be idempotent. For POST operations that clients may retry (payments, orders), consider an idempotency key with stored results, and define what happens for the same key with a different payload.
- **Concurrency and duplicates:** concurrent updates (optimistic concurrency with ETags or version fields), simultaneous duplicate requests (unique constraints, atomic checks).
- **Rate limiting and abuse:** limits per caller where exposure warrants it, with clear 429 behavior.
- **Resilience:** timeouts on every outbound call, bounded retries with backoff only for safe or idempotent operations, cancellation.
- **Observability:** structured logs with a correlation ID, metrics for latency and error rates, no sensitive data in logs.
- **ASP.NET Core (when used):** model validation and automatic 400 responses, DTO mapping, authorization attributes or policies plus resource-based checks, middleware for cross-cutting concerns, dependency injection for services, EF Core queries that project to DTOs and avoid loading unneeded data.

## Rules

- Use correct HTTP semantics.
- Validate all input at the boundary.
- Use consistent error responses across the API.
- Treat authorization independently from authentication, including object-level checks.
- Do not expose internal database models, stack traces, connection strings or other sensitive information.
- Consider backward compatibility for every change to an existing API, and call out breaking changes explicitly.
- Consider idempotency where clients may retry.
- Consider concurrency and duplicate requests for create and update operations.
- Consider timeout and retry behavior for dependencies. Do not retry non-idempotent operations blindly.
- Follow the existing API style and framework conventions over generic preferences.
- Do not claim an API was tested unless it was actually tested. State what was and was not run.
- Do not invent consumers, endpoints or requirements. List open questions.
- Never place real secrets in examples or logs.

## Output

```markdown
# API Analysis

## Requirement

## API Contract

## Endpoints

## Request Model

## Response Model

## Validation

## Error Handling

## Authentication

## Authorization

## Persistence

## Resilience

## Observability

## Testing

## Documentation

## Compatibility

## Open Questions
```

Omit or shorten a section when it does not apply, and say why.

## Examples

Illustrative only.

**Request:** "Add an endpoint to cancel an order."

**Response (abridged):**

```markdown
## Endpoints

- `POST /orders/{id}/cancellation`, which creates a cancellation. It fits a state change that is not a simple field update.
  Alternative: `PATCH /orders/{id}` with a status change, if the project already models state changes that way. Follow the existing convention.

## Error Handling

- 404 if the order does not exist or the caller may not know it exists.
- 409 if the order is already shipped (state conflict). The body uses the project's standard error format and does not expose internal details.
- Repeating the request for an already cancelled order returns the same success result, so retries are safe.

## Authorization

- Authentication alone is not enough. The caller must own the order or have a role that allows cancellation.

## Open Questions

Are refunds triggered by cancellation? If so, the refund call needs a timeout and an idempotency key.
```

## Related Skills

- [`architecture`](../architecture/SKILL.md): service boundaries, communication patterns and system-level design.
- [`database-sql`](../database-sql/SKILL.md): persistence design behind the API.
- [`testing`](../testing/SKILL.md): test strategy for the API.
- [`code-review`](../code-review/SKILL.md): review API changes before merge.
- [`debugging`](../debugging/SKILL.md): investigate failing requests.
