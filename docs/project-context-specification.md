# Project Context Specification

This specification defines the canonical structure, rules and quality bar for project context in the AI Engineering Hub. For an explanation of how the Hub uses project context, see [Project Context](project-context.md). A reusable template is in [`templates/project-context/PROJECT-CONTEXT.md`](../templates/project-context/PROJECT-CONTEXT.md).

The specification is technology-neutral. The technologies, files and tools it mentions are examples of what a repository might contain. No repository is assumed to contain any of them.

## Purpose

Project context provides repository-specific facts and conventions to skills, agents and workflows, so they can act on the repository they are working in and not only on generic engineering knowledge.

It records things such as:

- programming languages and frameworks
- database technology
- repository structure
- test commands
- build commands
- API conventions
- frontend conventions
- deployment approach
- observability tools
- security constraints

Project context exists to **reduce repeated discovery**. Without it, every request starts by rediscovering the stack, the commands and the conventions. With it, the Hub starts from what is already known, verifies what matters, and spends effort on the task.

Project context is **information**, not capability. It is not a skill, an agent, a command or a workflow. It is consumed by them:

```
Skill
  ↓
Project Context
  ↓
Repository / Tools
```

A generic skill stays generic. Project context lets the agent or workflow that uses the skill give a repository-aware result. The Hub's layers are described in [Architecture](architecture.md).

## Scope

In scope:

- facts about a repository that affect how engineering work should be done in it
- conventions the repository already follows
- explicit constraints on the work
- what is not known

Out of scope:

- generic engineering guidance. That belongs in skills.
- instructions on how an agent or workflow should behave. That belongs in agents and workflows.
- secrets, credentials and personal data. See [Safety](#safety).
- a full copy of the repository's documentation. Link to the source instead.
- facts that change on every commit, such as the current branch or the latest build result.
- irrelevant detail, such as every dependency in a manifest.

One project context describes one repository. A repository with several independently owned parts (applications, services) may have one context with a section for each part, or a context per part. The scope of the context is stated in its metadata.

## Context Sources

A project context is built from evidence. Acceptable sources:

| Source | Examples (not assumed to exist) |
| --- | --- |
| Repository files | Source code, configuration, scripts |
| README and documentation | README, contribution guides, architecture notes, decision records |
| Package and project files | `package.json`, `*.csproj`, `*.sln`, `pom.xml`, `pyproject.toml`, `go.mod`, `Directory.Build.props` |
| Configuration | `appsettings.*`, `.env.example`, framework configuration |
| CI/CD definitions | Pipeline files, container build files, Helm charts, Terraform |
| Test configuration | `playwright.config.*`, test runner settings, coverage settings |
| Build configuration | `vite.config.*`, `tsconfig.*`, build scripts |
| Database artifacts | Migration files, SQL scripts, ORM configuration |
| Infrastructure configuration | Infrastructure-as-code, deployment manifests |
| Developer-provided information | Statements by the developer in a request or in a review of the context |
| Generated repository analysis | Output of a context-discovery or analysis tool |

Rules:

- Do not assume any of these files exist. A repository may use none of these tools.
- Each important fact should name its source, so it can be verified or refreshed.
- A source that cannot be read is recorded as unavailable. It is not guessed.
- Developer-provided information is a valid source and is recorded as such. It is a statement by a person and not repository evidence, and it is labeled accordingly.
- Generated analysis is an inference until confirmed, unless it only reports what a file states.

### Facts, inferences and unknowns

This distinction is central. Every entry in a project context has one of three statuses.

| Status | Meaning | Example |
| --- | --- | --- |
| **Confirmed Fact** | Directly supported by a named source, or stated by the developer. | "`package.json` lists React as a dependency." |
| **Inferred** | A reasonable conclusion from indirect evidence, not stated anywhere. | "The application appears to use a query-caching library for data fetching." |
| **Unknown** | Not available, or not determined. | "The production database configuration is not available." |

Rules:

- **Never turn an inference into a confirmed fact.** An inference stays labeled until a source confirms it.
- An inference states the evidence it rests on.
- Unknowns are written down and not left out. See [Unknowns](#unknowns).
- A fact from the developer is labeled as developer-provided and should be verified against the repository when the task depends on it.
- When sources conflict, record the conflict. Do not choose silently.

## Technology Stack

Capture the technologies that matter to the work:

- languages
- frameworks
- libraries
- runtime
- database
- cloud
- infrastructure
- testing tools
- observability tools

Rules:

- Record versions when they are known and matter (for example a supported runtime or framework version), with the source.
- Record libraries that shape how code is written or that constrain changes. Avoid listing irrelevant dependencies.
- Record "none" or "not used" when it is confirmed, because it prevents wrong recommendations. Otherwise leave it unknown.

## Repository Structure

Capture the structure that helps a reader find and change things:

- applications
- services
- libraries
- tests
- infrastructure
- scripts
- documentation

Rules:

- Do not assume a particular structure (monorepo, single project, multiple repositories).
- Describe what exists and what each part is for, in brief, with paths.
- Note where tests live relative to the code they test, and where configuration lives.
- Mark generated or vendored directories that should not be edited.

## Architecture

Capture known architectural characteristics, for example:

- monolith
- modular monolith
- microservices
- event-driven
- layered architecture
- clean architecture
- hexagonal architecture
- domain-driven design
- CQRS
- messaging

Rules:

- Record a characteristic **only** when repository evidence supports it or the developer states it. A folder named `Domain` is not proof of domain-driven design.
- State the evidence or the source of the statement.
- Record the key boundaries, integration points and external dependencies that are known.
- Characteristics that look likely but are not supported go in the inferred list.
- Do not describe the ideal architecture. Describe the one that exists, including its known deviations.

## Coding Conventions

Capture the conventions the repository follows:

- naming
- formatting
- linting
- error handling
- logging
- dependency injection
- API patterns
- frontend patterns
- database access patterns

Rules:

- Prefer conventions enforced by tooling (formatter, linter, analyzer settings), and name the configuration.
- Record how similar code is actually written when no tool enforces it, and label it as an observed pattern.
- **Existing repository conventions take precedence over generic AI recommendations**, unless following them introduces a clearly identified issue, for example a security defect. In that case, the issue is stated, and the convention is not silently overridden.
- Record known deviations and areas being migrated, so that new code follows the intended direction.

## Testing

Capture:

- unit test framework
- integration test framework
- E2E framework
- test commands
- test directory conventions
- mocking approach
- test data conventions
- coverage requirements, where known

Rules:

- Test commands come from repository evidence (scripts, pipeline definitions, documentation). Do not invent them.
- **Listing a test command in project context is not evidence that the tests pass.** Tests are reported as passing only when they were run and the result was seen.
- Record prerequisites for running tests (services, databases, accounts) without recording secrets.
- Record which test levels exist and which are missing, when known.

## Build and Run

Capture known commands:

- install
- build
- test
- lint
- run
- development server
- integration tests
- E2E tests

Rules:

- Each command names its source (a script entry, a pipeline step, a documented instruction).
- **Do not invent commands.** If a command is not known, it is listed as unknown.
- Record the working directory and prerequisites where they matter.
- Record commands that are destructive or have side effects (seeding, resetting, deploying), and mark them as such. Their presence in the context is not authorization to run them.

## Database

Capture:

- database engine
- ORM
- migrations
- schema conventions
- transaction patterns
- stored procedures
- database environments
- connection configuration

Rules:

- Record the engine and version when known, and how migrations are created and applied.
- Record where connection configuration comes from (for example a configuration key or a secret store), not its value.
- **Never include secrets.** Do not store passwords, access tokens, API keys, private credentials, or connection strings that contain credentials.
- Record which environments exist and which the AI may access, if stated. Access to an environment is not implied by its being listed.
- Migrations and data changes remain subject to the Hub's safety rules. Project context does not grant authorization.

## API Conventions

Capture:

- API style (REST, RPC, event-based)
- routing conventions
- DTO patterns
- error format
- authentication
- authorization
- versioning
- pagination
- validation

Rules:

- Link to the contract or specification file if one exists.
- Record how existing endpoints behave, so new ones stay consistent.
- Record known consumers and compatibility obligations when they are known. Unknown consumers are recorded as unknown.

## Frontend Conventions

Record this section only when the repository has a frontend. Capture:

- framework
- language
- component conventions
- state management
- data fetching
- styling
- routing
- testing
- E2E
- accessibility conventions

Rules:

- Name the configuration or the files that show the convention.
- Mark the section "not applicable" when the repository has no frontend. Do not remove it from the template silently.

## CI/CD

Capture:

- CI platform
- build pipeline
- test pipeline
- deployment mechanism
- environments
- quality gates
- containerization
- infrastructure tooling

Rules:

- Name the pipeline files that define the behavior.
- Record what runs on a pull request and what runs on release.
- **Do not store secrets.** Record that a pipeline uses a secret and where it is managed, not its value.
- Describing a deployment mechanism is not authorization to deploy.

## Observability

Capture:

- logging framework
- metrics
- tracing
- dashboards
- alerting
- correlation IDs
- monitoring platform

Rules:

- Record **only what is actually present** in the project. Tools such as Grafana, Azure Monitor, Application Insights, Datadog or Dynatrace are examples of what may exist. None is assumed.
- Record where logs and telemetry can be read, and how a request can be traced across components, where that is known.
- Record dashboard and alert locations by name or link, and never credentials.

## Security

Capture project-specific security conventions:

- authentication provider
- authorization model
- secrets management
- identity platform
- security scanning
- dependency scanning
- data classification
- security headers

Rules:

- Record how security is handled in this repository. Do not record generic security advice; that belongs in the `security` skill.
- **Never store secrets.** Record where secrets are managed, not what they are.
- Record data classification rules that affect how logs, tests and examples may contain data.

## Development Workflow

Capture:

- branching strategy
- PR requirements
- review requirements
- commit conventions
- release process
- local development requirements

Rules:

- Record **only confirmed conventions**, with their source (a contribution guide, branch protection documented in the repository, a pipeline rule, or the developer's statement).
- Do not infer a workflow from a small sample of commits and record it as fact. An observed pattern is labeled as inferred.

## Important Constraints

Capture explicit constraints on the work:

- prohibited libraries
- required libraries
- supported runtime versions
- database compatibility
- API compatibility
- deployment restrictions
- security requirements
- performance requirements

Rules:

- Constraints are **higher-priority** project context. They override conventions and generic recommendations.
- Each constraint names its source, and its reason when known.
- A constraint that the AI believes is wrong or outdated is surfaced to the developer. It is not ignored.
- Constraints of the current request (from the user) combine with these. If they conflict, the conflict is surfaced.

## Unknowns

Every project context maintains an explicit list of unknowns. Examples:

- production topology is unknown
- the exact database version is unknown
- deployment configuration is unavailable
- the contract consumers are unknown

Rules:

- Unknowns are written down when they are discovered, especially when they affect common tasks.
- **The AI must not silently fill a gap with an assumption.** When a task depends on an unknown, the AI asks, or states the assumption it is making and labels it.
- An unknown that is resolved moves to a confirmed fact, with its source.

## Freshness

Project context can become stale. Each context records:

| Item | Meaning |
| --- | --- |
| **Last reviewed** | The date the context was last checked against the repository. |
| **Source files inspected** | The files and documents the context was built from. |
| **Context owner** | The person or team responsible for keeping it current, if known. |
| **Known stale sections** | Sections known or suspected to be out of date. |

Rules:

- **Prefer current repository evidence over stale context.**
- If project context conflicts with repository evidence, the **repository evidence normally takes precedence**.
- The conflict is **surfaced** when it materially affects the task, with both sides stated and their sources. It is not silently resolved either way.
- A context with no review date is treated as potentially stale.
- Facts that are cheap to verify and important to the task (a command, a version, a path) are verified before being relied on.
- Updating the context is a separate, explicit action. See [Usage Rules](#usage-rules).

## Ownership and Commands

A project context belongs to the repository it describes. The Hub ships the specification, the template, the generator and the drift detector, and does not store any repository's context. A developer creates and maintains the context in their own repository with `/context generate`, reads it with `/context inspect`, and checks it with `/context drift`. All three target the repository of the current working directory. See [Commands](commands.md#context-generate-inspect-drift). The context stays safe to commit: it never contains secrets.

## Usage Rules

Agents, skills and workflows that use project context should:

1. **Read relevant project context.** Read the sections that bear on the task, not the whole file.
2. **Prefer project conventions** over generic recommendations.
3. **Verify important facts against repository evidence when needed**, particularly when the context is old, when the task depends on the fact, or when a wrong assumption would be costly.
4. **Avoid unnecessary discovery** when reliable context exists.
5. **Never treat unknowns as facts.**
6. **Never expose secrets.**
7. **Never modify project context automatically** without an explicit context-update workflow or an explicit request.

Additional rules:

- **Precedence**, from highest to lowest: the user's explicit instructions for the task; important constraints in project context; current repository evidence; project conventions in the context; generic skill and agent guidance. Where two levels conflict in a way that matters, surface the conflict.
- Project context does not grant authorization. A listed command, environment or deployment mechanism is not permission to run it. The Hub's safety model applies in full.
- Project context does not change what a skill or agent is. It informs the application of a skill, and the skill text stays generic.
- A fact that was used in a result should be traceable to the context or to the repository evidence, and not presented as general knowledge.
- Record only what a future task will benefit from. Do not accumulate the details of each request.

## Safety

Project context must never contain:

- passwords
- API keys
- access tokens
- private keys
- secrets
- credentials, including connection strings that contain credentials
- sensitive personal information

If secret-like content is found while analyzing a repository:

- do not copy it into project context;
- record only that a secret or sensitive configuration exists, and where it is managed, if that is necessary for the work;
- recommend secure secret management, and treat the finding as something to report to the developer.

## Structure of a Project Context

A project context is a Markdown file, using the sections of this specification in order, plus a metadata block and the lists of confirmed facts, inferred information, unknowns and sources. The template is [`templates/project-context/PROJECT-CONTEXT.md`](../templates/project-context/PROJECT-CONTEXT.md).

Entries follow this shape where they matter:

```markdown
- <statement> — <Confirmed | Inferred | Unknown> — <source>
```

Sections that do not apply are marked "not applicable", and sections that are not yet known are marked "unknown". Empty sections are not left without a note.

## Quality Checklist

A project context is ready when:

- [ ] Metadata includes the project, scope, last reviewed date, owner (if known), and files inspected.
- [ ] Every important fact names a source.
- [ ] Facts, inferences and unknowns are separated, and no inference is written as a fact.
- [ ] Commands come from repository evidence, and none are invented.
- [ ] Architectural characteristics are supported by evidence or by the developer.
- [ ] Constraints are listed with their sources.
- [ ] Unknowns are listed explicitly.
- [ ] Known stale sections are marked.
- [ ] There are no secrets, credentials or personal data.
- [ ] It does not restate skill or agent guidance.
- [ ] It does not contain details that will not help a future task.
