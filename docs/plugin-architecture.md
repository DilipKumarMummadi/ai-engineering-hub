# Plugin Architecture

How the AI Engineering Hub is packaged as an [Agent Plugins](https://agent-plugins.org) 1.0.0 plugin. Packaging is additive: the Hub works directly from the repository without installing the plugin.

## Layers

```
AI Engineering Hub Repository   (source of truth)
        |
        v
Plugin Package                  (plugin.json + skills/ + com.github.copilot/ + README.md)
        |
        v
Portable Skills                 (skills/<name>/SKILL.md, technology-neutral)
        |
        v
Client-Specific Extensions      (com.github.copilot/, and the native .claude/ and .github/ trees)
        |
        v
AI Client                       (Claude Code, GitHub Copilot, other Agent Plugins clients)
```

## Plugin Is Not MCP

| | Plugin | MCP |
| --- | --- | --- |
| Role | Packaging and distribution of Hub capabilities | Access to external systems and tools |
| Delivers | Skills (instructions), client extensions, metadata | Callable tools and resources from servers that already exist |
| Owned by | The Hub | The server's maintainer; connected by the user in their client |

The plugin packages the Hub's engineering capabilities. It bundles **no MCP server implementation and no credentials**. Its root `mcp.json` is static configuration only: it names five existing servers (GitHub read-only, Atlassian for Jira, Figma, Postgres read-only, Playwright) and carries no `env`, `headers` or secret, which the validator enforces. `plugin.json` has no `mcpServers` or `userConfig`, because Agent Plugins 1.0.0 forbids inline MCP configuration and defines no portable user-secret mechanism.

Who authenticates, and to which database or endpoint, is runtime configuration supplied by the client or the user's environment; see [MCP Runtime Configuration](mcp-runtime-configuration.md), the [MCP Registry](mcp-registry.md) and the [client pages](mcp-clients/README.md). Claude Code loads the file through `.claude-plugin/plugin.json`, which declares three optional, sensitive install-time inputs (GitHub token, Atlassian Authorization value, PostgreSQL connection string) and matching per-server overrides; empty inputs fall back to the user's own client or shell configuration, and the validator rejects literal credentials and unsafe overrides. Agents depend on [capabilities](mcp-capability-registry.md); setup is in the [MCP Setup Guide](mcp-setup-guide.md). The Hub works without any server connected, and the plugin and MCP are complementary: the plugin distributes capabilities, MCP provides access.

## Package Contents

| Path | Kind | Role |
| --- | --- | --- |
| `plugin.json` | Portable | Manifest. Core fields only; no `extensions` entry. |
| `README.md` | Portable | Package documentation. |
| `mcp.json` | Portable | Static definitions of existing MCP servers. No credentials, `env`, `headers` or server code. |
| `.claude-plugin/` | Client-specific (Claude Code) | `marketplace.json` for installation, and `plugin.json` that points Claude Code at `mcp.json`. |
| `skills/<name>/SKILL.md` | Portable | 14 generic engineering skills, discovered by the client from `skills/`. |
| `com.github.copilot/` | Client-specific | Copilot namespace. Documents the Copilot resources; holds no copied logic. |
| `docs/` | Documentation | Specifications and this file. Skills link only to sibling skills and never to `docs/`. |

## What Stays Out of the Package

| Area | Classification | Why |
| --- | --- | --- |
| `evals/` | Evaluation infrastructure | Tests the Hub itself; not a runtime capability |
| `scripts/` | Development tooling | Validators, the Project Context generator and their tests |
| `.claude/agents`, `.claude/commands`, `.claude/workflows` | Client-specific (Claude Code) | Native to Claude Code; not part of the portable core |
| `.github/agents`, `.github/prompts`, `.github/workflows` | Client-specific (Copilot) | Native to Copilot; see below |
| `templates/project-context/` | Template | Blank template only |
| Any `PROJECT-CONTEXT.md` | Repository-specific | See below |

## Skills: Source and Package Copy

Agent Plugins discovers skills only in a root `skills/` directory. The Hub's canonical skills live in `.claude/skills/` (with a byte-identical copy in `.github/skills/`, already enforced by `scripts/validate-hub`). `skills/` is therefore a third, generated copy that packaging requires, kept honest by the plugin validator:

- `.claude/skills/` is the source. Edit skills there.
- `python3 scripts/validate-plugin/validate_plugin.py --sync` refreshes `skills/` from the source.
- The validator fails when `skills/` differs from `.claude/skills/`.

Symlinks were rejected because they are unreliable on Windows checkouts and in archives.

## Agents, Commands and Workflows

The core specification is portable around skills only, so none of these are core plugin content.

- **Agents** (9 per client) link to skills and to `docs/` with relative paths (`../skills/...`, `../../docs/...`) that are valid only in `.claude/agents/` and `.github/agents/`. Placing copies under `com.github.copilot/agents/` would break those links or force a rewritten duplicate of the agent logic, so they are **not** repackaged in this step. They remain intact in place. Packaging them later needs a path strategy that does not fork the definitions.
- **Commands** (Claude `.claude/commands/`, Copilot `.github/prompts/`) are thin entry points that read the agent definition by repository path.
- **Claude Code exposure (client-specific, not portable).** `.claude-plugin/plugin.json` points Claude Code at the existing files, with no copies: the commands `/context`, `/review-pr` and `/requirement` (as `/ai-engineering-hub:context`, `/ai-engineering-hub:review-pr` and `/ai-engineering-hub:requirement`) and the two agents they need, `pr-intelligence-agent` and `requirement-intelligence-agent` (as the `ai-engineering-hub:pr-intelligence-agent` and `ai-engineering-hub:requirement-intelligence-agent` subagents). Without this, a consuming repository could not reach the agent, because it is a file inside the Hub. The other eight agents are not exposed yet.
- **Workflows** are Hub orchestration documents for the same reason. Unchanged.

## Project Context

The plugin may carry the *capability*: the Project Context specification and generator live in `docs/` and `scripts/project-context/`, and the blank template in `templates/project-context/`. There is no Project Context skill, so none is packaged.

A `PROJECT-CONTEXT.md` describes one repository. It is generated in, and stays in, the repository that uses the Hub. It is never part of the package, and the validator rejects one anywhere in the packaged directories.

## Validation

`python3 scripts/validate-plugin/validate_plugin.py` checks the manifest (canonical schema URL, permitted fields, name, version), the `skills/` layout and its agreement with the source, link containment, required docs, `mcp.json` (schema, server types, no `env`, `headers` or credentials, Claude bridge consistency), forbidden content (evals, scripts, fixtures, secrets, `PROJECT-CONTEXT.md`, stray MCP config). Tests: `python3 scripts/validate-plugin/test_validate_plugin.py`. Evaluation cases: [`evals/plugin-packaging/`](../evals/plugin-packaging/README.md).
