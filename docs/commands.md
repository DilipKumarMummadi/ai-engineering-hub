# Commands

Commands are lightweight, user-facing entry points. A command routes a request to the right agent, or to one workflow, and passes the user's context along. It contains no engineering logic of its own.

```
Command → Agent → Skills → Validation
```

| Layer | Role |
| --- | --- |
| **Command** | A user-facing entry point that invokes an agent |
| **Agent** | Orchestrates skills for a broader task (see the [Agent Registry](agent-registry.md) and [Agent Specification](agent-specification.md)) |
| **Skill** | A focused engineering capability |
| **Evaluation** | Validates the corresponding layer |

The engineering instructions live in the agents and skills. A command only names its agent and states how to pass the request.

`/review-pr` is an entry variant of `/pr-intelligence`: the same agent, started from a pull request URL or number that the agent retrieves through the `source-control` capability.

Six commands are **workflow commands**: they route to exactly one workflow file instead of an agent (see [Workflow Commands](#workflow-commands)). `/incident` is the existing entry for the production-incident workflow and stays an agent command.

One command is different. [`/context`](#context-generate-inspect-drift) is a **tool command**: it runs the Hub's Project Context Generator on the repository you are working in instead of routing to an agent.

## Available Commands

| Command | Agent | Purpose |
| --- | --- | --- |
| `/review` | pr-review-agent | Start a PR or code review |
| `/debug` | bug-investigation-agent | Investigate an unexpected behavior or failure |
| `/test-plan` | test-planning-agent | Create a test strategy or test plan |
| `/architecture` | architecture-agent | Analyze or design system architecture |
| `/api` | api-development-agent | Design, implement, review or evolve an API |
| `/database` | database-troubleshooting-agent | Investigate or design database and SQL behavior |
| `/incident` | production-incident-agent | Investigate an active or recent production incident |
| `/review-pr` | pr-intelligence-agent | Review a GitHub pull request by URL or number, using a connected source-control MCP |
| `/requirement` | requirement-intelligence-agent | Analyze, refine and assess the readiness of a requirement or Jira issue (`analyze`, `refine`, `readiness`, `update`) |
| `/feature`, `/bug-fix`, `/api-change`, `/database-change`, `/e2e`, `/pr-prep` | a workflow (none) | See [Workflow Commands](#workflow-commands) |

## Workflow Commands

A workflow command starts one multi-stage workflow. It names the workflow file, passes the full request unchanged, and adds no stages or engineering instructions. The workflow decides the stages, agents, skills and human checkpoints. Reusable mechanics are in [Workflow Common Guidance](workflow-common.md).

| Command | Workflow | Purpose |
| --- | --- | --- |
| `/feature` | [feature-development](../.claude/workflows/feature-development.md) | Take a feature from requirement to a validated change |
| `/bug-fix` | [bug-fix](../.claude/workflows/bug-fix.md) | Fix a defect on a supported root cause, with a regression test |
| `/api-change` | [api-change](../.claude/workflows/api-change.md) | Design, implement and validate an API change |
| `/database-change` | [database-change](../.claude/workflows/database-change.md) | Plan, implement and validate a schema, data or query change |
| `/e2e` | [e2e-test-creation](../.claude/workflows/e2e-test-creation.md) | Create a browser E2E test, or recommend a lower level |
| `/pr-prep` | [pr-preparation](../.claude/workflows/pr-preparation.md) | Prepare a finished change for a pull request |

Use `/incident` for the production-incident workflow and `/pr-intelligence` or `/review-pr` for readiness assessment. Use `/debug`, `/api` or `/database` when a single agent is enough.

Workflow commands do not authorize applying migrations, deployments, merges, pushes, approvals or production changes. The workflow's requirements-and-plan checkpoint comes before any edit.

## `/context`: Generate, Inspect, Drift

Project Context belongs to the **consuming repository**. The Hub provides the capability; it never stores another repository's context.

```
AI Engineering Hub  ── installed into / available to ──►  your-repository
                                                              │
                                                              ▼
                                                        /context generate
                                                              │
                                                              ▼
                                                   your-repository/PROJECT-CONTEXT.md
```

| Request | Does | Writes |
| --- | --- | --- |
| `/context generate` | Creates or minimally updates the current repository's `PROJECT-CONTEXT.md` with the existing generator. `--dry-run` shows the result and writes nothing. | `PROJECT-CONTEXT.md` only |
| `/context inspect` | Reads the existing context and summarizes it. Never regenerates. | Nothing |
| `/context drift` | Runs the existing read-only drift check and reports whether the context may be stale. | Nothing |

The command identifies the target with `git rev-parse --show-toplevel` from the current working directory, so a subdirectory of a repository works. It stops and asks when the directory is not a project, and when the target is the Hub itself. It locates the generator through the plugin root, or `AI_HUB_HOME`, or by asking, and never copies it into your repository. Every operation passes `--repo <target root>`.

Claude Code: `/context ...` in the Hub repository, or `/ai-engineering-hub:context ...` when the plugin is installed. GitHub Copilot: the `context` prompt in `.github/prompts/`; it has no plugin root, so set `AI_HUB_HOME` to a Hub checkout. Both follow the same rules.

**CLI status.** There is no global `ai-hub` executable, and none is faked. The generator's own entry point is `scripts/project-context/project-context` (`generate`, `update`, `drift`, `--dry-run`). A future `ai-hub context generate | inspect | drift` would wrap the same operations and is not implemented.

**Developer instructions.** From inside your repository: run `/context generate --dry-run`, read the summary, run `/context generate`, review `PROJECT-CONTEXT.md` and commit it. Later, run `/context drift`, and `/context generate` when it reports material drift.

## `/review-pr`

```
/review-pr https://github.com/org/repo/pull/123
/review-pr 123            # the repository of the current directory
```

The command passes the reference to `pr-intelligence-agent`. The agent retrieves the pull request (metadata, commits, changed files, the diff, existing comments and checks, linked items) through the `source-control` capability, which the GitHub MCP provides when the client has it connected and signed in. It then applies change-intelligence, code-review and only the supporting skills the PR calls for, using the repository's Project Context when there is one, and returns a `# PR Review` ending in READY, NEEDS_CHANGES or NEEDS_INFORMATION.

Authentication is entirely the client's. The command never asks for a token. Without a connected provider the agent says live PR information is unavailable and reviews a locally available diff if there is one. It never approves, merges, comments on or changes the pull request. Setup per client is in [MCP clients](mcp-clients/README.md). In Claude Code with the plugin installed, the command is `/ai-engineering-hub:review-pr`.

## Skills Used Indirectly

A command never invokes a skill itself. The agent chooses skills from the request. The table shows the agent's primary skills, and the supporting skills it may select when the context calls for them. An agent does not use every supporting skill.

| Command | Primary skills | Supporting skills (selected by the agent) |
| --- | --- | --- |
| `/review` | code-review | security, database-sql, performance, architecture, testing, refactoring, api-development |
| `/debug` | debugging | observability, database-sql, performance, reliability, security, architecture |
| `/test-plan` | testing | playwright, api-development, debugging, code-review |
| `/architecture` | architecture | security, performance, reliability, observability, database-sql, api-development, refactoring |
| `/api` | api-development | security, database-sql, performance, reliability, testing, architecture |
| `/database` | database-sql | debugging, performance, reliability, security, architecture |
| `/incident` | debugging, observability, reliability | performance, database-sql, security, architecture, api-development |

This mirrors the [Agent Registry](agent-registry.md), which is the source of truth.

## Useful Context

Users are not required to fill in a form. Anything in the list helps the agent, and the agent asks for what it still needs.

| Command | Useful context |
| --- | --- |
| `/review` | changed files, PR description, diff, related requirements, test results, known constraints |
| `/debug` | error message, logs, stack trace, reproduction steps, expected and actual behavior, recent changes, environment |
| `/test-plan` | requirement or feature, changed code, acceptance criteria, existing tests, test environment, browser flow |
| `/architecture` | requirements, current architecture, constraints, scale, integrations, reliability and security requirements, cost constraints |
| `/api` | API requirement, existing endpoints, contracts, consumers, authentication, authorization, database behavior, compatibility requirements |
| `/database` | schema, SQL, error, query plan, data examples, database engine, transaction behavior, expected result |
| `/incident` | incident description, impact, timeline, logs, metrics, traces, alerts, recent deployments, affected services, dependencies |

## Examples

Write the command, then describe the request and paste the context.

```
/review
Review the current changes.
```

```
/debug
The API started returning 500 errors after today's deployment.
Here is the stack trace:
...
```

```
/test-plan
Plan tests for the new transfer endpoint. CI time is tight, so avoid browser tests unless they are needed.
```

```
/database
This query returns some customers twice. Schema and SQL below.
...
```

```
/incident
Checkout latency jumped at 09:40. Version 5.8 was rolling out. Metrics below.
...
```

The text after the command is passed to the agent as written. Constraints the user states, such as "avoid browser tests", are preserved.

## How Commands Behave

- Pass the user's full request and context to the agent without summarizing away technical detail.
- Proceed when enough context exists. When important information is missing, the agent identifies what it needs. Commands do not require a fixed form.
- Add no engineering instructions of their own, and do not repeat agent or skill instructions.
- An empty command uses the natural default: `/review` with no text means the current changes. The others let the agent ask for what it needs.

## Safety Boundaries

A command is a request to start work. It is not authorization to change anything.

- `/database` does not authorize `DELETE`, `UPDATE`, `DROP`, `TRUNCATE`, `ALTER` or any statement that changes data or schema. The database agent's safety rules still apply.
- `/incident` does not authorize production changes such as rollback, restart, scaling, failover, feature flag or configuration changes, killing sessions or data changes. The incident agent proposes reversible mitigation and asks for authorization.
- `/review-pr` does not authorize approvals, merges, comments or changes on the pull request, and never involves credentials.
- `/requirement` does not authorize implementation, edits, commits or any other change. Its `update` word prepares a ticket update and does not authorize writing it: the ticket is written only after the user explicitly approves the exact difference shown. See the [Requirement Intelligence Specification](requirement-intelligence-specification.md).
- `/review` does not authorize edits, merges, approvals, pushes or comments on a pull request.
- `/context` modifies only `PROJECT-CONTEXT.md` of the target repository, only through the generator, and only for `generate`. It does not authorize editing source or configuration, commits, pushes or deployments, and it never reproduces a secret.
- `/feature`, `/bug-fix`, `/api-change`, `/database-change`, `/e2e` and `/pr-prep` do not authorize applying migrations, deployments, merges, pushes, approvals or production changes. Planning is never authorization, and the workflow's checkpoints still apply.
- `/debug`, `/architecture`, `/test-plan` and `/api` do not authorize changes to code, data, configuration or infrastructure by themselves.

Authorization is given explicitly by the user, for a specific action. A command that names a risky action ("/database delete the duplicates") still goes through the agent's safety rules.

## Where Commands Live

| Platform | Location | Format |
| --- | --- | --- |
| Claude Code | `.claude/commands/<name>.md` | A Markdown command file. `$ARGUMENTS` receives the text after the command. |
| GitHub Copilot | `.github/prompts/<name>.prompt.md` | A Markdown prompt file with front matter. The text after the prompt name is the request. |

The two formats are not identical, but the behavior and intent are the same: name the agent (or workflow), pass the full request, add no engineering logic, and keep the safety boundaries. The command files and the registry are listed in the [Command Registry](command-registry.md).

## Adding or Changing a Command

- A command must route to exactly one existing agent, or be a workflow command naming exactly one existing workflow, and contain no engineering logic. Two commands must not route to the same agent or the same workflow (`/review-pr` is the one declared entry variant). The only exception is a tool command such as `/context`, which runs an existing Hub tool and is listed in the validator's tool-command set.
- Create both the Claude command and the Copilot prompt, with equivalent behavior.
- Add evaluation cases under `evals/commands/<name>/`. See [evals/commands](../evals/commands/README.md).
- Update the [Command Registry](command-registry.md).
