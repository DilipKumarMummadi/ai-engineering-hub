# Project Context

<!--
Template for the AI Engineering Hub project context. See docs/project-context-specification.md.

How to use:
- Copy this file into the repository it describes (for example as PROJECT-CONTEXT.md at the repository root).
- Fill in only what is supported by evidence. Leave a section as "Unknown" or "Not applicable" instead of guessing.
- For every important fact, name the source file. Format:  <statement> — <Confirmed | Inferred | Unknown> — <source>
- Never put passwords, API keys, tokens, private keys, credentials, connection strings containing credentials, or personal data in this file.
  Record where a secret is managed, not the secret.
- Delete these comments once the file is filled in.
-->

## Metadata

- Project:
- Description:
- Scope: <what this context covers: the whole repository, or specific applications/services>
- Last Reviewed: <date>
- Context Owner: <person or team, or "unknown">
- Source Files Inspected: <files and documents this context was built from>
- Known Stale Sections: <sections known or suspected to be out of date, or "none known">

## Technology Stack

### Languages

<!-- Languages used, with versions where known and relevant. Source: project/manifest files. -->

### Frameworks

<!-- Frameworks and libraries that shape how code is written. Omit incidental dependencies. -->

### Runtime

<!-- Runtime and platform versions, and supported versions if constrained. -->

### Database

<!-- Engine, version if known, ORM. Details go in "Database Conventions". -->

### Cloud / Infrastructure

<!-- Hosting, cloud provider, container or orchestration tooling, infrastructure-as-code. Only what is present. -->

### Testing

<!-- Test frameworks and tools. Details go in "Testing Conventions". -->

### Observability

<!-- Logging, metrics, tracing and monitoring tools. Details go in "Observability". -->

## Repository Structure

<!-- Applications, services, libraries, tests, infrastructure, scripts, documentation, with paths and purpose.
Mark generated or vendored directories that should not be edited. Do not assume a structure. -->

## Architecture

<!-- Known architectural characteristics (for example layering, service boundaries, messaging), each with supporting evidence or
"stated by developer". Key boundaries, integrations and external dependencies. Describe what exists, not the ideal. -->

## Coding Conventions

<!-- Naming, formatting, linting, error handling, logging, dependency injection, API/frontend/database access patterns.
Name the configuration that enforces each one. Label unenforced patterns as "observed". Note known deviations and migrations in progress. -->

## Testing Conventions

<!-- Unit, integration and E2E frameworks; test commands and where they come from; test directory layout; mocking approach;
test data conventions; coverage requirements; prerequisites for running tests (no secrets).
A listed command is not evidence that tests pass. -->

## Build and Run

<!-- Commands with their source. Do not invent commands; list missing ones under Unknowns.
Mark commands that are destructive or have side effects (seed, reset, deploy). Listing a command does not authorize running it.

| Purpose | Command | Working directory | Source |
| --- | --- | --- | --- |
| Install | | | |
| Build | | | |
| Test | | | |
| Lint | | | |
| Run / dev server | | | |
| Integration tests | | | |
| E2E tests | | | |
-->

## Database Conventions

<!-- Engine and version, ORM, how migrations are created and applied, schema conventions, transaction patterns, stored procedures,
environments, and where connection configuration comes from (name the key or secret store, never the value).
Listing an environment does not grant access to it. -->

## API Conventions

<!-- API style, routing, DTO patterns, error format, authentication, authorization, versioning, pagination, validation.
Link to the contract or specification file. Known consumers and compatibility obligations, or "unknown". -->

## Frontend Conventions

<!-- Framework, language, component conventions, state management, data fetching, styling, routing, testing, E2E, accessibility.
Write "Not applicable" if there is no frontend. -->

## CI/CD

<!-- CI platform, build and test pipelines (name the pipeline files), what runs on a pull request and on release, deployment mechanism,
environments, quality gates, containerization, infrastructure tooling. Record that secrets are used and where they are managed, not their values.
Describing a deployment mechanism does not authorize deploying. -->

## Observability

<!-- Logging framework, metrics, tracing, dashboards, alerting, correlation IDs, monitoring platform. Only what is present.
Where logs and telemetry can be read. Dashboard and alert locations by name or link. -->

## Security

<!-- Authentication provider, authorization model, secrets management (where, not what), identity platform, security and dependency scanning,
data classification rules, security headers. Project-specific only; generic advice belongs in skills. -->

## Development Workflow

<!-- Confirmed conventions only: branching strategy, PR and review requirements, commit conventions, release process, local development requirements.
Name the source for each. -->

## Important Constraints

<!-- Explicit constraints, each with its source and reason if known: prohibited or required libraries, supported runtime versions,
database and API compatibility, deployment restrictions, security and performance requirements.
Constraints take priority over conventions and generic recommendations. -->

## Confirmed Facts

<!-- Facts directly supported by a named source or stated by the developer. Format:
- React is a dependency of the frontend — Confirmed — package.json
- The API project targets a specific runtime — Confirmed — the API project file
-->

## Inferred Information

<!-- Conclusions from indirect evidence. State the evidence. An inference stays here until a source confirms it; then move it to Confirmed Facts.
- The frontend appears to use a query-caching library for data fetching — Inferred — imports in src/api/ (not stated in documentation)
-->

## Unknowns

<!-- Anything not available or not determined. The AI must not fill these with assumptions. Examples:
- The production topology is unknown.
- The exact database version is unknown.
- The deployment configuration is not available.
-->

## Context Sources

<!-- Files, documents and statements this context relies on. Name each. Record sources that could not be read.
- Dependencies and scripts → package.json
- API project → *.csproj
- E2E configuration → playwright.config.ts
- Pipeline definitions → the CI configuration files
- Developer-provided → <who, when>
-->
