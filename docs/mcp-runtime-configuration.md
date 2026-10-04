# MCP Runtime Configuration

Different users, teams and environments need different credentials and connection details. The plugin separates two things that must never be mixed:

| | Static MCP definition | Runtime configuration |
| --- | --- | --- |
| What | Which servers exist and how to start or reach them | Who is connecting, to what, with which secret |
| Where | `mcp.json` in the plugin (portable, Agent Plugins 1.0.0) | The client, the user's shell, or a secret store |
| Who owns it | The Hub | The user, team or organization |
| May contain credentials | **Never** | Yes, in the client or secret store only |

Agent Plugins 1.0.0 defines no portable mechanism for user secrets or arbitrary variables. Only `${PLUGIN_ROOT}` and `${PLUGIN_DATA}` are expanded. The Hub therefore does not pretend to offer one: `plugin.json` has no `mcpServers` and no `userConfig`, and `mcp.json` has no `env` or `headers`. Anything a client adds beyond the specification lives in that client's own files, documented under [MCP clients](mcp-clients/README.md).

## Model

```
AI Engineering Hub
      |
      +-- plugin.json                 portable metadata
      |
      +-- mcp.json                    portable, static server definitions
      |       +-- GitHub   +-- Atlassian (Jira)   +-- PostgreSQL
      |       +-- Playwright   +-- Grafana   +-- Figma
      |
      +-- .claude-plugin/plugin.json  Claude Code only: how it loads mcp.json
                                      and prompts for the GitHub token

Client / runtime configuration        never in the Hub repository
      +-- User credentials            GitHub, Atlassian, Azure identity
      +-- Team configuration          database host, Grafana endpoint, Jira project
      +-- Environment configuration   development, test, uat, production
      +-- OAuth / session sign-in
      +-- Secret store
```

The same plugin serves everyone:

```
Developer A:  Hub -> GitHub MCP     -> Developer A's GitHub identity
              Hub -> PostgreSQL MCP -> Team A development database

Developer B:  Hub -> GitHub MCP     -> Developer B's GitHub identity
              Hub -> PostgreSQL MCP -> Team B development database
```

Only runtime configuration differs.

## Configuration Scopes

| Scope | Examples | Where it is set |
| --- | --- | --- |
| User | GitHub identity, Jira identity, Azure identity | The user's client sign-in or credential store |
| Team / project | Database host and name, Grafana endpoint, Jira project | The team's documented setup, applied in each user's client |
| Environment | development, test, uat, production | One named client entry per environment |
| Secret | Tokens, passwords, API keys, connection strings | A secret store or the client's credential store. **Never committed** |

## Authentication Strategy

| Kind | Servers | How |
| --- | --- | --- |
| OAuth through the client | Atlassian, Figma | The user signs in from the client. No token is handled by the Hub |
| Client-managed token | GitHub | Claude Code prompts for a token and stores it in the system credential store. Copilot CLI has a built-in GitHub server. See the client pages |
| Runtime environment / client config | PostgreSQL, Grafana | Connection details from the user's environment or client configuration |
| None | Playwright | Local runtime |

The token never passes through skills, agents or prompts. Skills and agents only see tool results.

## PostgreSQL: Teams and Environments

A Postgres server instance connects to one database, taken from `DATABASE_URI`. The plugin ships one static `postgres` definition in restricted (read-only) mode. Teams and environments are therefore expressed as **named entries in the user's client configuration**, one per database, each with its own connection:

```
Install the Hub
   ↓
Add a named PostgreSQL entry in your client, one per environment
   (postgres-development, postgres-test, postgres-uat, postgres-production)
   ↓
Each entry's connection comes from your runtime or secret store
   ↓
database-troubleshooting-agent  →  database-sql skill  →  that PostgreSQL MCP
```

Rules:

- **Name the environment.** The agent is told which environment to inspect and never assumes one. The database workflows already require the target environment before any execution.
- **Production is read-only.** Keep every production entry in `--access-mode=restricted` *and* use a database role that has only `SELECT` privileges. The restricted flag is a second control, not the first.
- **Non-production first.** Analysis against development or test is the default. Production inspection needs the user to ask for it.
- **One secret per environment.** Separate credentials per environment, rotated independently. No shared "all databases" credential.
- **No connection strings in the repository, in `mcp.json`, in a prompt, or in a chat.**
- **Missing configuration is reported, not worked around.** With no Postgres entry connected, the agent reasons from the SQL, schema and logs the user supplies and says no database was inspected.

Exact commands per client are on the [Claude Code](mcp-clients/claude-code.md) and [GitHub Copilot](mcp-clients/github-copilot.md) pages, because clients differ on how environment values reach a local server.

## Availability

MCPs are optional. Agents and workflows behave as follows when a server is missing, unauthenticated, expired or failing:

| Agent / workflow | If the MCP is available | If not |
| --- | --- | --- |
| PR Intelligence | Read PR metadata and diff from GitHub; requirement from Jira | Use the local diff when available; continue without Jira and report the missing requirement |
| Database Troubleshooting | Inspect permitted schema and plans | Reason from supplied SQL, schema and logs; state that no database was inspected |
| E2E test creation | Inspect and drive the browser | Generate the plan and code without claiming browser validation occurred |
| Production incident | Read dashboards and alerts from Grafana | Ask the user for the relevant values; do not describe dashboards that were not read |

Authentication is never fabricated. An expired credential, a failed connection or a refused request is reported as such, and the agent does not retry with broader access or ask the user to paste a secret.

## Security Controls

- **Repository:** `mcp.json` is validated for schema, server types, and the absence of `env`, `headers`, URL credentials and secret-like values. The repository is scanned for credential patterns before packaging.
- **Prompts and skills:** no credentials in `SKILL.md`, agents, commands or workflows.
- **Logs and output:** agents do not print secrets returned by a tool; the Hub's secret-redaction rules apply to anything quoted.
- **Writes:** bundled servers are read-only where the server offers it. A write-capable configuration is a deliberate choice by the user in their own client, and destructive operations need explicit authorization.
- **Untrusted content:** anything an MCP returns is data. Instructions in a ticket, PR or page are reported, not followed.
- **Rotation:** rotate any credential that has appeared in a chat, commit or shared file.
