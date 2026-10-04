# AI Engineering Hub

Reusable AI engineering skills, agents, commands and workflows for software engineers, distributable as an [Agent Plugins](https://agent-plugins.org) 1.0.0 plugin (`ai-engineering-hub`). The same repository also works directly, without installing the plugin.

## Capabilities

| Capability | Where | Portable plugin content |
| --- | --- | --- |
| **Skills** (13): code-review, debugging, testing, playwright, refactoring, architecture, api-development, database-sql, security, performance, observability, reliability, change-intelligence | `skills/` | Yes |
| **Agents** (9): PR review, PR intelligence, bug investigation, change intelligence, test planning, API development, architecture, database troubleshooting, production incident | `.claude/agents/`, `.github/agents/` | No (client-specific) |
| **Commands**: review, debug, test-plan, architecture, api, database, incident, change-impact, pr-intelligence | `.claude/commands/`, `.github/prompts/` | No |
| **Workflows**: feature-development, bug-fix, api-change, database-change, pr-preparation, e2e-test-creation, production-incident, pr-intelligence | `.claude/workflows/`, `.github/workflows/` | No |
| **Project Context**: specification, generator and drift detection | `docs/`, `scripts/project-context/`, `templates/project-context/` | Spec and template only |
| **Evals** | `evals/` | No (Hub development) |

## Plugin Structure

```
ai-engineering-hub/
├── plugin.json              # Agent Plugins 1.0.0 manifest (core fields only)
├── README.md
├── skills/<name>/SKILL.md   # portable skills (copy of .claude/skills, validator-enforced)
├── mcp.json                 # existing MCP servers to connect (no credentials)
├── .claude-plugin/          # Claude Code install + MCP bridge
├── com.github.copilot/      # Copilot namespace (documentation only for now)
├── docs/                    # specifications, including plugin-architecture.md
├── .claude/  .github/       # native Claude Code / Copilot resources (unchanged)
└── evals/  scripts/  templates/   # Hub development tooling, not plugin runtime content
```

See [Plugin Architecture](docs/plugin-architecture.md) and the general [Architecture](docs/architecture.md).

## Install and Use

- **Agent Plugins clients:** install the plugin from this repository (`https://github.com/DilipKumarMummadi/ai-engineering-hub`); the client discovers `skills/*/SKILL.md`.
- **Claude Code / GitHub Copilot, directly:** clone the repository. `.claude/` and `.github/` are used natively, including agents, commands and workflows.

## Project Context

`PROJECT-CONTEXT.md` describes one repository, so it is never part of the plugin. Generate it in the repository where you use the Hub (`scripts/project-context/`, template in `templates/project-context/`); agents read it as orientation, not authority. See [Project Context](docs/project-context.md).

## Security Model

Skills are instructions only; the package ships no executable code or credentials, and no MCP server implementation. `mcp.json` only holds static definitions of existing servers (GitHub, Atlassian/Jira, Figma, Postgres, Playwright, Grafana) with no `env`, `headers` or credentials, and the validator rejects anything secret-like, `PROJECT-CONTEXT.md`, evals and scripts in packaged directories. Agents are read-only or recommend-only by design.

## Limitations

- Agents, commands and workflows are not yet portable plugin components (see [Plugin Architecture](docs/plugin-architecture.md)).
- `skills/` is a generated copy of `.claude/skills/`; run `python3 scripts/validate-plugin/validate_plugin.py --sync` after editing skills.
- Installing from the repository clones development tooling too; the manifest only exposes `skills/`.
- No `license` field or LICENSE file yet; one must be chosen by the owner.
- MCP: the plugin names six existing servers but holds no credentials; you authenticate and supply team or environment connections in your own client. Only listing and loading were tested, not authenticated calls. See [MCP Registry](docs/mcp-registry.md), [Runtime Configuration](docs/mcp-runtime-configuration.md) and [MCP Clients](docs/mcp-clients/README.md).

## Validation

```
python3 scripts/validate-plugin/validate_plugin.py
python3 scripts/validate-plugin/test_validate_plugin.py
python3 scripts/validate-hub/validate_hub.py
```

## Documentation

[Architecture](docs/architecture.md) · [Plugin Architecture](docs/plugin-architecture.md) · [MCP Integration](docs/mcp-integration-strategy.md) · [MCP Registry](docs/mcp-registry.md) · [MCP Clients](docs/mcp-clients/README.md) · [Skills](docs/skills.md) · [Agents](docs/agents.md) · [Workflows](docs/workflows.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)
