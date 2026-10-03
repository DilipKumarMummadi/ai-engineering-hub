# Commands

Commands are lightweight, user-facing entry points. A command routes a request to the right agent and passes the user's context along. It contains no engineering logic of its own.

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
- `/review` does not authorize edits, merges, approvals, pushes or comments on a pull request.
- `/debug`, `/architecture`, `/test-plan` and `/api` do not authorize changes to code, data, configuration or infrastructure by themselves.

Authorization is given explicitly by the user, for a specific action. A command that names a risky action ("/database delete the duplicates") still goes through the agent's safety rules.

## Where Commands Live

| Platform | Location | Format |
| --- | --- | --- |
| Claude Code | `.claude/commands/<name>.md` | A Markdown command file. `$ARGUMENTS` receives the text after the command. |
| GitHub Copilot | `.github/prompts/<name>.prompt.md` | A Markdown prompt file with front matter. The text after the prompt name is the request. |

The two formats are not identical, but the behavior and intent are the same: name the agent, pass the full request, add no engineering logic, and keep the safety boundaries. The command files and the registry are listed in the [Command Registry](command-registry.md).

## Adding or Changing a Command

- A command must route to an existing agent and contain no engineering logic.
- Create both the Claude command and the Copilot prompt, with equivalent behavior.
- Add evaluation cases under `evals/commands/<name>/`. See [evals/commands](../evals/commands/README.md).
- Update the [Command Registry](command-registry.md).
