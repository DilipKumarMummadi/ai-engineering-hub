# Scenario

The context is large and current, but most of it has nothing to do with the task. The case checks that the agent loads only relevant sections, does not import irrelevant context into the plan, and stays focused on the task.

# User Request

```
/test-plan

We're adding client-side validation to the signup form (email format, password length 12+, matching confirmation). What should we test?
```

# Context

`PROJECT-CONTEXT.md` (current) has sections for Technology Stack (React 18, Vite, Vitest, Playwright), Testing (Vitest unit tests, Playwright E2E in `e2e/`, commands), Build and Run, and also detailed Database (PostgreSQL, 14 migrations), Infrastructure (Kubernetes, Helm), Observability (OpenTelemetry, Grafana) and CI/CD (GitHub Actions deploy to AKS) sections.

The repository has `src/components/SignupForm.tsx` and an existing `SignupForm.test.tsx`.

# Expected Routing

- `/test-plan` routes to `test-planning-agent`.

# Expected Skill Composition

- Always: `testing`.
- Possibly: `playwright`, only if an end-to-end scenario is justified. Validation rules are mostly lowest-level (unit or component) behavior, so an E2E test for the full signup path, if proposed, is a single smoke scenario.
- Not applied: `api-development`, `database-sql`, `debugging`, `code-review`. Nothing calls for them.

# Expected Process

1. Find the context, and load only the Technology Stack, Testing and Build and Run sections.
2. Confirm the test tools from `package.json` and the existing test file.
3. Plan tests at the lowest effective level with Vitest and Testing Library conventions already in use, including boundaries (11 and 12 characters, mismatched confirmation, invalid email forms).
4. Decide on at most one E2E smoke scenario, or none, with a reason.
5. Give the commands recorded for running tests, verified against `package.json`.

# Important Checks

- Database, Kubernetes, Helm, OpenTelemetry and deployment sections are not loaded or mentioned.
- The plan does not propose integration tests against PostgreSQL, deployment checks or observability assertions.
- The existing test file is read and extended, not duplicated.
- Test levels are lowest-effective.
- The context is not quoted in the plan beyond naming the frameworks it confirmed.

# Safety Checks

- Read-only planning. No tests are run against a shared environment.

# Expected Output Characteristics

A compact test plan focused on the form's validation: scenarios, test data, levels and commands. No "environment" or "infrastructure" section pulled from the context.

# Failure Conditions

- Adding scenarios for the database, Kubernetes, migrations or telemetry because the context mentions them.
- Summarizing the whole context at the top of the plan.
- Proposing many E2E tests for unit-level validation rules.
- Missing the existing Vitest conventions.

# Notes

A good context is wide. A good agent takes a narrow slice.
