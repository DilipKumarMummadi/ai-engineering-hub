# MCP in GitHub Copilot

Status legend: **Tested**, **Documented**, **Not tested** (see [MCP Clients](README.md)). Only GitHub Copilot CLI (1.0.84) was exercised. GitHub Copilot in VS Code and the Copilot cloud agent were **not tested** and are not described.

## How the plugin's servers load

Copilot CLI reads the plugin's root `mcp.json` directly. `copilot mcp list` shows all six servers under "Plugin servers": **Tested**. Project-level configuration is `.mcp.json` or `.github/mcp.json`, and user-level configuration is `~/.copilot/mcp-config.json`: **Documented**.

## Per-server runtime configuration

| Server | What the user does | Status |
| --- | --- | --- |
| GitHub | Use Copilot CLI's **built-in GitHub MCP server**, which needs no configuration. The plugin's `github` entry has no credentials in it; if it shows as failing, disable it with `copilot mcp disable github` | Built-in server: **Documented**. Behavior of the plugin's entry when unauthenticated, and disabling it: **Not tested** |
| Atlassian (Jira), Figma | Remote servers. The Copilot CLI documentation does not describe OAuth for remote servers, so sign-in may not be available | **Not tested** |
| PostgreSQL | Define the connection in your user-level `~/.copilot/mcp-config.json` (see below) | **Not tested** against a database |
| Grafana | Same approach for `GRAFANA_URL` and the token | **Not tested** |
| Playwright | Install Node.js | Listed: **Tested**. Driving a browser: **Not tested** |

### Local servers do not inherit your shell environment

The Copilot CLI documentation states that `PATH` is inherited and that all other environment variables must be configured in the server's `env` entry. So, unlike Claude Code, exporting `DATABASE_URI` in your shell does not reach the server. The connection has to be in Copilot's own configuration:

- Put it in your **user-level** file `~/.copilot/mcp-config.json`, never in a project file such as `.mcp.json` or `.github/mcp.json` that could be committed. Restrict the file's permissions to your user.
- Create one named entry per database, for example `postgres-development`, `postgres-uat`, `postgres-production`, each `uvx postgres-mcp==0.3.0 --access-mode=restricted` with its own `DATABASE_URI` in `env`.
- Whether Copilot CLI expands variable references or reads a secret store for `env` values is **not documented**, so this page does not claim it. The value therefore sits in a user-only file; use a `SELECT`-only database role and a short-lived credential where you can.
- Production: restricted mode and a `SELECT`-only role, both.

## Reviewing a Pull Request with `/review-pr`

Copilot CLI's built-in GitHub MCP server supplies the `source-control` capability (**Documented**). Use the `review-pr` prompt from `.github/prompts/`, which hands the request to `.github/agents/pr-intelligence-agent.md`; both must be available in the repository you are working in, because Copilot has no plugin root. The plugin does not expose the agent to Copilot. **Not tested** in Copilot.

## Limitations

- No portable secret mechanism, and no Copilot-specific prompt equivalent to Claude Code's. Credentials must be set in Copilot's own user-level configuration.
- The plugin's unconfigured servers may show as failing; they do not affect the Hub's skills.
- Everything the Hub does without an MCP (local diff, repository evidence, Project Context) works the same in Copilot.
