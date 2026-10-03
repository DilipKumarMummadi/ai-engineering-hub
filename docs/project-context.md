# Project Context

Project context gives the AI Engineering Hub repository-specific information, so it can work on the repository in front of it instead of relying only on generic engineering knowledge. The canonical structure and rules are in the [Project Context Specification](project-context-specification.md). A reusable template is in [`templates/project-context/PROJECT-CONTEXT.md`](../templates/project-context/PROJECT-CONTEXT.md).

```
User
 ↓
Command / Workflow
 ↓
Agent
 ↓
Skill
 ↓
Project Context
 ↓
Repository / Tools
 ↓
Validation
 ↓
Output
```

Project context is **not another skill**. It has no behavior of its own. It is information that skills, agents and workflows consume. See [Architecture](architecture.md).

## Why It Exists

Skills and agents are deliberately generic, so they work in any repository. That also means that, without help, every request begins with discovery: which language, which test command, which database, which conventions. Project context records what has already been established so that work starts from it.

It serves two purposes:

- **Less repeated discovery.** The stack, the commands and the conventions are read, not rediscovered.
- **Repository-aware results.** Recommendations follow the repository's own conventions and constraints.

## What Belongs There

- Technology stack: languages, frameworks, runtime, database, test and observability tools.
- Repository structure and architecture characteristics that are supported by evidence.
- Conventions: coding, API, frontend, database access.
- Test, build and run commands, with their sources.
- CI/CD, observability and security setup, in terms of what exists and where.
- Development workflow: branching, PRs, reviews, releases, when confirmed.
- Explicit constraints.
- Unknowns, and how fresh the context is.

Each important fact names its source and is marked **Confirmed**, **Inferred** or **Unknown**.

## What Does Not Belong There

| Not in project context | Where it goes |
| --- | --- |
| Generic engineering guidance ("consider transaction boundaries") | A skill |
| How an agent or workflow should behave | The agent or workflow |
| Secrets: passwords, API keys, tokens, private keys, credentials, connection strings containing credentials, personal data | Nowhere in the repository context. Record only where a secret is managed. |
| Dependencies that do not shape the work | Omit. The manifest is the source. |
| Values that change on every commit (current branch, last build result) | Read them from the repository when needed |
| Details of a single request | The request |
| Guesses written as facts | Inferred information, labeled, or Unknowns |

Project context never grants authorization. Listing a deploy command, a database environment or a migration script does not permit running it. The [safety model](architecture.md#safety-model) applies as always.

## How Layers Use It

### Skills

A skill stays generic. It is applied with project context, which tells the skill what the repository actually uses.

A generic database skill says:

> Consider transaction boundaries.

Project context says:

> This repository uses PostgreSQL and EF Core, with migrations in `Migrations/`.

The agent combines them:

```
Generic Skill
+
Project Context
=
Repository-aware recommendation
```

The recommendation names the repository's actual transaction patterns, ORM behavior and migration approach. The skill text does not change, and the context does not restate the skill.

### Agents

An agent reads the sections of project context that bear on the task, before and while it selects skills. It uses the context to:

- avoid rediscovering the stack and the commands;
- choose skills with the right technology in mind (for example which test tools exist, when planning tests);
- prefer the repository's conventions in its recommendations;
- check its output against the constraints;
- label what it relied on, and what it had to verify.

An agent still verifies facts that matter and is still responsible for its own reasoning and safety rules. Each agent has a short Project Context section that names only the topics relevant to it and points to [Project Context Consumption](project-context-consumption.md), which defines discovery, validation, staleness, conflicts, missing context and secret handling once for all agents. Without a context, an agent proceeds from repository evidence.

### Workflows

A workflow uses project context at the stages where it changes the work. For example, the stage that runs tests uses the known test command, and the stage that plans a migration uses the known migration approach. A workflow adds no context-loading stage: its Project Context section names the stages and topics, and the agent performing each stage loads what it needs. A workflow does not assume the context is current, and it proceeds without one. See [Project Context Consumption](project-context-consumption.md).

### Commands

Commands remain thin. They do not read or interpret project context. The agent or workflow they lead to does.

## Example

A hypothetical request: "Add an endpoint for exporting orders." In this example, the repository's context records (with sources) an ASP.NET Core API, a specific error-response format, cursor pagination, EF Core on PostgreSQL, and an integration test project with a documented test command. The constraint says no new third-party libraries without approval.

- `api-development-agent` designs the endpoint in the existing error format and pagination style, without re-reading the codebase for them.
- Its persistence step uses the repository's migration approach and the EF Core patterns in the context.
- The test plan uses the integration test project and names the test command, reporting it as *not run* until it is run.
- The export library needs are checked against the constraint.
- The unknown "expected export volume" is asked about, not assumed.

## Facts, Inferences and Unknowns

| Status | Example |
| --- | --- |
| Confirmed | "`package.json` contains React." |
| Inferred | "The application appears to use a query-caching library." |
| Unknown | "The production database configuration is not available." |

An inference is never promoted to a fact without a source. Unknowns are listed so that nobody fills them in silently.

## Staleness

Project context ages. It records when it was last reviewed, which files it was built from, who owns it if known, and which sections are known to be stale.

- Current repository evidence is preferred over stale context.
- A context with no review date is treated as potentially stale.
- Facts that are cheap to check and important to the task, such as a command, a version or a path, are verified before being relied on.
- When a section is known to be stale, it is read as a lead and not as a fact.

The Hub does not update project context by itself. Updates are explicit, by the developer or by running the generator procedure on request.

## Resolving Conflicts

Sources of guidance can disagree. The order, from highest to lowest priority:

1. The user's explicit instructions for the task.
2. Important constraints in project context.
3. Current repository evidence.
4. Project conventions recorded in the context.
5. Generic skill and agent guidance.

In practice:

- **Context versus repository evidence:** the repository evidence normally wins, because it is current. The conflict is surfaced if it affects the task, with both sides and their sources.
- **Convention versus a generic recommendation:** the convention wins, unless following it introduces a clearly identified issue, for example a security defect. Then the issue is stated and the developer decides.
- **Constraint versus a better idea:** the constraint stands. If the AI thinks it is wrong or outdated, it says so and leaves the decision to the developer.
- **User instruction versus context:** the user's instruction for this task is followed. If it conflicts with a constraint, the conflict is surfaced before proceeding.

Conflicts are reported and not silently resolved.

## Generating and Updating Context

The [Project Context Generator Specification](project-context-generator-specification.md) defines a procedure for generating a first draft of project context from a repository, and for updating it as the repository changes. It is a procedure that an AI assistant follows. A local command line implementation of its deterministic part is in [`scripts/project-context/`](../scripts/project-context/README.md): `project-context generate`, `update` and `--dry-run`. The specification covers evidence collection, classification, update, staleness, conflicts, secret protection and validation, and it is not repeated here.

## Detecting Drift

The generator creates or updates the context. It does not say when an update is needed. The [Project Context Drift Specification](project-context-drift-specification.md) defines a separate, read-only check: it compares the existing `PROJECT-CONTEXT.md` with current repository evidence and reports material changes, stale statements and conflicts. It never modifies the context. The developer reads the report, then decides whether to run the generator. Ordinary source, test and documentation changes are not drift. The tool offers it as `project-context drift`, with `--ci` for pipelines.

## Discovery Order

The generator inspects evidence in this order, and only the files relevant to each step. Nothing is assumed to exist, so steps that do not apply are skipped.

| # | Step | Looks at | Produces |
| --- | --- | --- | --- |
| 1 | Repository root | Top-level layout, obvious ecosystems | Candidate structure, where to look next |
| 2 | README and documentation | README, contribution and architecture documents | Stated purpose, conventions, workflow, constraints |
| 3 | Project manifests | Package and project files for the ecosystems found | Languages, frameworks, libraries, runtime versions |
| 4 | Build configuration | Build and bundling settings, scripts | Build and run commands |
| 5 | Test configuration | Test runner and E2E configuration | Test frameworks, commands, layout |
| 6 | CI/CD | Pipeline definitions, container build files | Pipelines, environments, quality gates |
| 7 | Infrastructure | Infrastructure-as-code, deployment manifests | Hosting and deployment approach |
| 8 | Application configuration | Non-secret configuration structure | Configuration keys and sources, authentication setup |
| 9 | Database configuration | Migrations, schema scripts, ORM configuration | Engine, ORM, migration approach |
| 10 | Observability configuration | Logging, metrics and tracing setup | Observability tools and conventions |

The generator proposes a draft for the developer to review. It writes the file only when asked, and it never copies secrets.

## Safety

Project context must never contain passwords, API keys, access tokens, private keys, secrets, credentials or sensitive personal information. If such content is found while analyzing a repository, do not copy it into project context. Identify only that a secret or configuration exists, if necessary, and recommend secure secret management.

## Location

The Hub provides the specification, the template, and the generator procedure and tool with its optional [configuration template](../templates/project-context/GENERATOR-CONFIG.md). A repository that uses project context keeps its own copy, for example as `PROJECT-CONTEXT.md` at its root. The Hub's own repository does not contain a project-specific context.
