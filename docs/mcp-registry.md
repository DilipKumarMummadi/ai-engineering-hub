# MCP Registry

The MCP servers the Hub knows about. The Hub builds none of them. A server is listed as **Bundled** only when its official configuration was verified from the maintainer's documentation; `mcp.json` contains static definitions and nothing else. Every server is optional, and agents never assume one is connected ([strategy](mcp-integration-strategy.md)). Agents depend on [capabilities](mcp-capability-registry.md), and each server below is one provider of one. Observability MCP access (dashboards, metrics, logs, alerts) is deferred to a later phase and nothing is registered for it.

| MCP | Purpose | Transport | Bundled in `mcp.json` | Access mode | Runtime configuration (supplied by the client, never the repo) |
| --- | --- | --- | --- | --- | --- |
| GitHub | Repositories, PRs, diffs, commits, issues | Remote HTTP | Yes | Read-only endpoint (`/mcp/readonly`) | Client-managed authentication. See [Claude Code](mcp-clients/claude-code.md) and [GitHub Copilot](mcp-clients/github-copilot.md) |
| Atlassian (Jira, Confluence) | Tickets, requirements, acceptance criteria | Remote HTTP | Yes | Per the user's Atlassian permissions | OAuth sign-in through the client |
| PostgreSQL | Schema, plans, read-only queries | Local stdio (`uvx`) | Yes | Read-only (`--access-mode=restricted`) | Team and environment connection, from the user's runtime or secret store; never in the Hub |
| Playwright | Browser automation and inspection | Local stdio (`npx`) | Yes | Drives a local browser | None; needs Node.js |
| Figma | Design context | Remote HTTP | Yes | Per the user's Figma permissions | OAuth sign-in through the client |
| Azure | Cloud resources and monitoring | Local stdio (`npx`) | **No** | No read-only option documented | Azure identity (`az login`). Not bundled; see below |

## Verification

| MCP | Verified from | What was verified |
| --- | --- | --- |
| GitHub | GitHub's `github-mcp-server` remote documentation | Endpoint `https://api.githubcopilot.com/mcp/`, and the `/readonly` path for read-only mode |
| Atlassian | Atlassian Rovo MCP server documentation | Current endpoint `https://mcp.atlassian.com/v2/mcp`; OAuth 2.1; v1 is being retired, so the older `/v1/sse` is not used |
| PostgreSQL | `crystaldba/postgres-mcp` README | `uvx postgres-mcp`, connection via `DATABASE_URI`, `restricted` mode is read-only; pinned to 0.3.0 |
| Playwright | `@playwright/mcp` on npm | Package exists; pinned to 0.0.83 |
| Figma | Figma's hosted MCP endpoint, as already connected in the maintainer's client | `https://mcp.figma.com/mcp` |
| Azure | Microsoft `Azure.Mcp.Server` README | `npx -y @azure/mcp@latest server start`, Azure Identity authentication. **Not bundled** because no read-only mode is documented and the published tag is a pre-release |

Runtime behavior was checked in Claude Code and GitHub Copilot CLI only to the extent stated in each [client page](mcp-clients/README.md). Authenticated calls were not tested.

## Rules for Adding an MCP

1. Verify the official URL or package and its authentication from the maintainer's documentation. Do not guess.
2. Add a static definition only: type, URL or command, arguments. No `env`, no `headers`, no credential of any kind.
3. Prefer a read-only endpoint or flag. Pin package versions.
4. Document the runtime configuration it needs in [Runtime Configuration](mcp-runtime-configuration.md) and in each client page.
5. Run the plugin validator, which rejects credentials, `env` and `headers` in `mcp.json`.
