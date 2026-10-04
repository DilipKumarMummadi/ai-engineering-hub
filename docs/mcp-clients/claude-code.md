# MCP in Claude Code

Status legend: **Tested**, **Documented**, **Not tested** (see [MCP Clients](README.md)).

## How the plugin's servers load

Claude Code reads a plugin's MCP configuration through its own manifest. `.claude-plugin/plugin.json` sets `mcpServers` to `["./mcp.json", { "github": … }]`: the portable file first, then a Claude Code-only override of `github`. The servers appear as `plugin:ai-engineering-hub:<name>`.

- Servers listed, with Atlassian reaching `needs-auth`: **Tested**.
- `claude plugin validate` passes on the manifest: **Tested**.
- A server name declared later replaces an earlier one: **Documented**.

## Per-server runtime configuration

| Server | What the user does | Status |
| --- | --- | --- |
| Atlassian (Jira), Figma | Run `/mcp`, choose the server, sign in in the browser. Claude Code refreshes the token itself | Atlassian reaches `needs-auth`: **Tested**. Completing sign-in: **Not tested** |
| GitHub | Enter a token when Claude Code asks on enable (see below) | Manifest and load: **Tested**. The prompt and an authenticated call: **Not tested** |
| PostgreSQL | Export the connection in the shell that starts Claude Code | `failed` while `DATABASE_URI` is unset: **Tested**. Working with it set, and a live database: **Not tested** |
| Playwright | Install Node.js | Loads: **Tested**. Driving a browser: **Not tested** |

### GitHub token (Claude Code-specific)

This uses Claude Code's own plugin feature, `userConfig`. It is **not** part of Agent Plugins and is not portable. The manifest declares one optional, sensitive option; Claude Code prompts for it when the plugin is enabled, stores it in the system credential store, and substitutes it into the GitHub server's `Authorization` header at start. The token is never in the repository, `mcp.json`, a skill or a prompt.

- Create a fine-grained token with read access to only the repositories needed, and an expiry. If you are signed in to the `gh` CLI, you may use the output of `gh auth token`.
- Leave the prompt empty to skip GitHub. The server then shows as failed and nothing else is affected.
- Without GitHub, agents use the local diff.

Without this, GitHub's server offered no browser sign-in in Claude Code (it reported `failed`, not `needs-auth`): **Tested**.

### PostgreSQL

The plugin's single `postgres` entry reads `DATABASE_URI` from its environment, so set it in the shell that launches Claude Code. (That local servers receive that environment is the usual stdio behavior but was not separately verified.) Take the value from your secret manager; do not type it into a file that is committed or shared.

For named environments, add one entry per database in your own user-scope Claude Code configuration, each reading its own variable, for example `postgres-uat` reading `PG_UAT_URI`. Claude Code expands `${VAR}` in a server's `env` at launch (**Documented**), so the secret stays in your shell or secret manager and not in the Claude configuration file. The command shape, from the Claude Code documentation:

```
claude mcp add --scope user postgres-uat -e DATABASE_URI='${PG_UAT_URI}' -- uvx postgres-mcp==0.3.0 --access-mode=restricted
```

The single quotes stop your shell from expanding the variable at the time you add it. This command was **not tested**. Production entries use the same restricted flag and a `SELECT`-only database role.

## Reviewing a Pull Request with `/review-pr`

Setup, all done in the client:

1. Install the plugin. It exposes `/ai-engineering-hub:review-pr` and the `pr-intelligence-agent` subagent.
2. Enable the GitHub MCP for GitHub and sign in: either the plugin's own `github` server, which prompts for your token when the plugin is enabled (see above), or a GitHub MCP you already have at user level. The Hub does not care which, and never sees the token.
3. Open your repository and run `/ai-engineering-hub:review-pr <PR URL or number>`.

If GitHub is not connected or not signed in, the agent says live PR information is unavailable and reviews a local diff if there is one. Tested with a user-level GitHub MCP: the PR was retrieved and a review produced. The plugin's own prompted-token server was **not tested** for this flow.

## Limitations

- The GitHub prompt and token substitution exist only in Claude Code.
- Servers that are not configured show as failed or needing sign-in. Disable them in `/mcp`.
- The Figma server may not list separately if the same URL is already configured at user level.
