# API Development Evaluations

Evaluations for the [`api-development`](../../.claude/skills/api-development/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the skill designs and reviews APIs with correct HTTP semantics, clear contracts, consistent errors, sound security and attention to compatibility and retries.

## Evaluation Principles

- HTTP methods and status codes are used for their meaning.
- Contracts are explicit and do not leak internal models or details.
- Validation and errors are consistent and useful to clients.
- Authentication and authorization are treated as separate concerns, including object-level access.
- Changes to existing APIs consider existing consumers.
- Operations that clients may retry are safe to repeat.
- Recommendations fit the stated framework and conventions.

## Expected Behavior

A good response identifies the resources and operations, defines request and response shapes and status codes, covers validation, errors and security, explains the compatibility and idempotency implications, and lists open questions. For existing APIs it points out concrete problems and migrates carefully.

## Common Failure Modes

- Returning 200 with an error body, or 500 for client mistakes.
- Exposing internal errors, SQL or entity models.
- Mixing up authentication and authorization, or checking only the endpoint and not the object.
- Breaking existing clients with no migration path.
- Retry-unsafe operations with no duplicate protection.
- Designing for a framework the project does not use.
- Over-engineering simple endpoints.

## Qualitative Evaluation

Outcomes are Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). Several valid designs usually exist, so judge the reasoning and consistency, not exact paths. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [resource-api-design](cases/resource-api-design.md) | Designs a resource API with correct semantics, authorization and pagination. |
| [error-handling](cases/error-handling.md) | Repairs inconsistent error handling without breaking current clients. |
| [idempotent-operation](cases/idempotent-operation.md) | Makes a retried POST safe, including under concurrent duplicates. |
