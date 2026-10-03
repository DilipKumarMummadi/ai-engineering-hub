---
name: debugging
description: Systematically investigate errors, test failures, build or CI/CD failures, runtime, API, database, frontend, container and performance problems using an evidence-driven process that separates facts from hypotheses and confirms a root cause before recommending a fix. Use when something is failing or behaving unexpectedly; do not use for reviewing or writing new code.
---

# Debugging

## Purpose

Help engineers investigate problems systematically. The skill moves from symptom to evidence, context, hypotheses, validation, root cause, fix and regression prevention. It works across technologies and never assumes a technology that the provided context does not show.

Covers application errors, exceptions, test failures, build failures, runtime failures, API failures, database errors, frontend and backend errors, CI/CD failures, container and Kubernetes failures, cloud/service failures, performance problems and unexpected application behavior.

**Core principle: do not jump from the symptom to a fix.**

```
Symptom → Evidence → Context → Hypotheses → Validation → Root Cause → Fix → Regression Prevention
```

## When to Use

- An error, exception, stack trace, failed test, failed build or failed pipeline needs to be explained.
- A system behaves differently from what is expected and the cause is unknown.
- A service, container, query, request or page is failing, slow or inconsistent.
- The user asks "why is this happening" or "how do I fix this error".

## When NOT to Use

- The task is reviewing a change for quality. Use the [`code-review`](../code-review/SKILL.md) skill.
- The cause is already known and the user only wants the change implemented.
- The task is building a new feature or writing tests with no failure to investigate.

## Inputs

All inputs are optional individually, but at least a symptom (error, failure or behavior description) is required. If none is provided, ask for it.

- Error messages, stack traces
- Logs, metrics, distributed traces
- Test output, build output
- Browser console output, network traces, screenshots
- Database errors
- Configuration, environment information, deployment information
- Source code, recent code changes
- Reproduction steps

Identify missing information when it matters. Ask for the smallest additional information needed. Never fabricate missing information.

## Process

### 1. Understand the problem

Establish:

- What is failing?
- What is the expected behavior?
- What is the actual behavior?
- Who or what is affected?
- Which environment is affected?
- When did the problem start?

Record unknowns rather than guessing.

### 2. Extract evidence

Collect and summarize only evidence that is actually available: stack trace, error message, logs, HTTP status, database error, test failure, recent deployment, recent code change. Do not invent evidence. Quote it accurately.

### 3. Identify the failure boundary

Determine where the failure appears to occur, for example:

- Frontend → API → Service → Database
- Test → Application → External dependency
- Request → API Gateway → Service → Database

State which boundary the evidence points to and which it rules out.

### 4. Generate hypotheses

Create a small number of plausible hypotheses, prioritized by evidence. For each, state:

- The hypothesis
- Evidence supporting it
- Evidence against it
- How to validate it

Do not produce a long list of speculative possibilities.

### 5. Validate

Recommend concrete validation steps, for example: inspect a specific log, check a specific configuration, reproduce with a specific input, run a specific test, inspect a database query, check the deployed version, compare environments, inspect a network request, check a dependency version.

Where tools are available (reading code, searching, running commands or tests), use them and report what was actually observed. Where tools are not available, provide commands or investigation steps for the user to run.

### 6. Identify the root cause

Call something the root cause only when the evidence supports it. If it cannot be confirmed, say "Root cause not yet confirmed." Then give the most likely hypotheses and the next validation steps. If several root causes remain possible, state that.

### 7. Recommend the fix

Recommend the smallest fix that addresses the underlying cause rather than hiding the symptom. Consider code, configuration, database, infrastructure, dependency and deployment changes. Avoid unnecessary rewrites.

### 8. Regression prevention

Recommend only prevention relevant to the problem: unit, integration or E2E test, monitoring, alert, logging, validation, documentation, guard clause, contract test.

### Area checklists

Use the ones that apply while performing steps 2 to 5.

- **Application errors:** exception type, stack trace, failing method, input and state, dependency behavior.
- **Test failures:** actual vs expected, test setup, mocks, fixtures, environment, asynchronous behavior, timing, shared state, flaky behavior.
- **API failures:** request, response, HTTP status, authentication, authorization, payload, downstream dependencies, timeout, retry behavior.
- **Database failures:** query, parameters, schema, connection, transaction, locks, indexes, constraints, data state.
- **Frontend failures:** browser console, network requests, component state, rendering, asynchronous state, API response, event handling.
- **CI/CD failures:** pipeline step, environment, dependency versions, secrets and configuration, build artifacts, runner, permissions.
- **Docker/Kubernetes failures:** container logs, image, environment variables, ports, probes, resources, configuration, service discovery, deployment state.
- **Performance problems:** latency, throughput, CPU, memory, database queries, external calls, concurrency, resource contention.

## Rules

- Never fabricate logs, stack traces or configuration.
- Never claim a root cause without evidence.
- Label every statement as one of: **observed fact**, **assumption**, **hypothesis** or **confirmed root cause**. Never present an unverified hypothesis as the root cause.
- Do not change code before the problem is understood.
- Avoid unnecessary speculation.
- Prefer minimal, targeted fixes and respect the existing architecture.
- Consider recent changes, environment differences and dependency changes.
- Consider race conditions and data or state issues where relevant.
- Recommend regression coverage.
- If multiple root causes are possible, say so.
- If the information is insufficient, ask for the smallest amount of additional information needed.
- Never expose secrets. If logs or configuration contain secrets, refer to them by name or location and do not repeat their values.
- Do not run destructive or state-changing operations (deleting data, restarting production services, force-resetting) unless the user explicitly authorizes them.
- Do not assume a technology unless the context indicates it.

## Output

Use this structure. Omit **Additional Information Required** when nothing important is missing, and repeat **Hypothesis** blocks only when useful.

```markdown
# Debugging Analysis

## Problem

Brief description of the observed problem.

## Expected vs Actual

### Expected

...

### Actual

...

## Evidence

List only evidence actually available.

## Failure Boundary

Where the failure appears to occur.

## Hypotheses

### Hypothesis 1

**Status:** Unconfirmed / Likely / Confirmed

**Evidence:**

...

**Validation:**

...

## Root Cause

If confirmed: the root cause and supporting evidence.
If not: "Root cause not yet confirmed." followed by what must be validated.

## Recommended Fix

The smallest appropriate fix that addresses the underlying cause.

## Validation

How to verify the fix.

## Regression Prevention

Appropriate tests, monitoring or safeguards.

## Additional Information Required

Only when important information is missing.
```

## Examples

Illustrative only. The error, code and names below are invented for the example.

**Input:** A .NET service returns HTTP 500. The log shows:

```
System.NullReferenceException: Object reference not set to an instance of an object.
   at OrderService.Checkout(Order order) in OrderService.cs:line 48
```

Line 48 is `var total = order.Customer.Discount.Apply(order.Subtotal);`

**Response (abridged):**

```markdown
# Debugging Analysis

## Problem

`POST /checkout` returns HTTP 500 with a NullReferenceException in `OrderService.Checkout`, line 48.

## Evidence

- Observed: NullReferenceException at OrderService.cs:line 48.
- Observed: line 48 dereferences `order.Customer` and `order.Customer.Discount`.
- Not available: which request failed, the order payload, how `Discount` is populated.

## Failure Boundary

Inside the service, at a single expression. The exception type does not point to the API or database layer.

## Hypotheses

### Hypothesis 1

**Status:** Unconfirmed

**Evidence:** `Customer.Discount` is dereferenced with no visible initialization in the code shown. Customers with no discount may leave it unset.
**Validation:** Find where `Customer.Discount` is assigned (search the codebase and the loading query). Check whether it is null for the failing customer, for example by logging or inspecting the data for the failing order.

### Hypothesis 2

**Status:** Unconfirmed

**Evidence:** `order.Customer` may itself be null if the customer relation is not loaded.
**Evidence against:** The exception could come from either dereference, but line 48 alone does not say which.
**Validation:** Split the expression or use the debugger or a log to see which value is null.

## Root Cause

Root cause not yet confirmed. The failing object is one of `order.Customer` or `order.Customer.Discount`. Next step: identify which is null, then trace why it was never set.

## Recommended Fix

Do not add a bare null check to silence the error. After the cause is confirmed, fix it at the source. For example, if customers without a discount legitimately have none, initialize `Discount` to a no-discount default when the customer is created or loaded. If the relation was not loaded, fix the query. Add a null-check only if a null is a valid state, and handle it explicitly.

## Validation

Replay the failing request and confirm it returns success with the expected total.

## Regression Prevention

Add a test for checkout with a customer who has no discount, and one for an order whose customer was loaded from storage.

## Additional Information Required

The failing order's data, and the code that creates or loads `Customer.Discount`.
```

## Related Skills

- [`code-review`](../code-review/SKILL.md): review the resulting fix for correctness and quality before merge.
