# MCP in Claude Code

Status legend: **Tested**, **Documented**, **Not tested** (see [MCP Clients](README.md)).

## How the plugin's servers load

Claude Code reads a plugin's MCP configuration through its own manifest. `.claude-plugin/plugin.json` sets `mcpServers` to `["./mcp.json", { "github": …, "atlassian": …, "postgres": … }]`: the portable file first, then Claude Code-only overrides for the three servers that can take a credential. The servers appear as `plugin:ai-engineering-hub:<name>`.

- Servers listed, with Atlassian reaching `needs-auth`: **Tested**.
- `claude plugin validate` passes on the manifest: **Tested**.
- A server name declared later replaces an earlier one: **Documented**.
- An optional `userConfig` value left empty is substituted as an empty string and the server still loads (it does not drop the plugin): **Documented**.

## Install-time inputs (Claude Code-specific, all optional)

This uses Claude Code's own plugin feature, `userConfig`. It is **not** part of Agent Plugins and is not portable. The manifest declares three optional, sensitive options. Claude Code prompts for them when the plugin is enabled, stores them in the system credential store, and substitutes them into the matching server at start. None is in the repository, `mcp.json`, a skill or a prompt, and the Hub never reads them.

| Option | Server | Where it goes | What to enter |
| --- | --- | --- | --- |
| `github_token` | GitHub | `Authorization: Bearer <token>` | A fine-grained token with read access to only the repositories needed, and an expiry. If signed in to `gh`, you may use `gh auth token` |
| `atlassian_auth` | Atlassian (Jira) | `Authorization: <value>` | The full header value: `Basic <base64 of email:api_token>` or `Bearer <service account key>` |
| `postgres_database_uri` | PostgreSQL | `HUB_DATABASE_URI` for the server process | A connection string for a **read-only** database user |

### Leaving an input empty: fallback to your local configuration

Every input is optional. Leave it empty and the Hub falls back to what you already have locally:

| Server | Empty input means |
| --- | --- |
| GitHub, Atlassian | The plugin's entry is sent an empty credential and shows `failed` (GitHub, **Tested**) or needs sign-in (Atlassian, **Not tested** with an empty header). Use the server you configured yourself at user or project level, or, for Atlassian, sign in through `/mcp`. The Hub reads the tools the client exposes, so it uses whichever server answers. Disable the plugin's copy in `/mcp` if the failed entry bothers you |
| PostgreSQL | The wrapper falls back to `DATABASE_URI` from the shell that starts Claude Code (unchanged behavior), then to a PostgreSQL MCP you configured yourself |

A value entered at install takes precedence over the shell variable for the plugin's PostgreSQL entry only. To change or clear an input later, use the plugin's configuration in Claude Code (`/plugin`).

Precedence is per server and never merges credentials: the Hub does not look inside your own MCP configuration (see [Discovery, not configuration](../mcp-runtime-configuration.md#discovery-not-configuration)).

## Per-server runtime configuration

| Server | What the user does | Status |
| --- | --- | --- |
| Atlassian (Jira) | Enter the Authorization value at install, or leave empty and run `/mcp` to sign in in the browser, or use your own Atlassian MCP | Atlassian reaches `needs-auth`: **Tested**. Token-header auth and completing sign-in: **Not tested** |
| Figma | Run `/mcp`, choose the server, sign in in the browser | Not prompted at install (no credential option). Completing sign-in: **Not tested** |
| GitHub | Enter a token at install, or leave empty and use your own GitHub MCP | Manifest and load: **Tested**. The prompt and an authenticated call with the plugin's token: **Not tested**. A user-level GitHub MCP returning data: **Tested** |
| PostgreSQL | Enter a connection string at install, or export `DATABASE_URI` in the shell that starts Claude Code | `failed` while both are unset: **Tested** (earlier manifest). Working with either set, and a live database: **Not tested** |
| Playwright | Install Node.js | Loads: **Tested**. Driving a browser: **Not tested** |

Without GitHub, agents use the local diff. Without Jira, agents ask for the requirement text.

### PostgreSQL

The plugin's `postgres` entry uses the connection string entered at install (`postgres_database_uri`) if there is one, and otherwise reads `DATABASE_URI` from the environment, so set it in the shell that launches Claude Code. (That local servers receive that environment is the usual stdio behavior but was not separately verified.) Take the value from your secret manager; do not type it into a file that is committed or shared.

For named environments, add one entry per database in your own user-scope Claude Code configuration, each reading its own variable, for example `postgres-uat` reading `PG_UAT_URI`. Claude Code expands `${VAR}` in a server's `env` at launch (**Documented**), so the secret stays in your shell or secret manager and not in the Claude configuration file. The command shape, from the Claude Code documentation:

```
claude mcp add --scope user postgres-uat -e DATABASE_URI='${PG_UAT_URI}' -- uvx postgres-mcp==0.3.0 --access-mode=restricted
```

The single quotes stop your shell from expanding the variable at the time you add it. This command was **not tested**. Production entries use the same restricted flag and a `SELECT`-only database role.

## Reviewing a Pull Request with `/review-pr`

Setup, all done in the client:

1. Install the plugin. It exposes `/ai-engineering-hub:review-pr` and the `pr-intelligence-agent` subagent.
2. Have GitHub connected: enter a token when the plugin is enabled, or use a GitHub MCP you already have. The Hub does not care which one, and never sees the token.
3. Open your repository and run `/ai-engineering-hub:review-pr <PR URL or number>`.

If GitHub is not connected or not signed in, the agent says live PR information is unavailable and reviews a local diff if there is one. Tested with a user-level GitHub MCP: the PR was retrieved and a review produced. 

## Limitations

- The Hub cannot see why a server is missing; use `/mcp` or `claude mcp list`.
- The plugin's `github` and `playwright` entries can duplicate servers you already run. Two Playwright servers contend for one browser profile (**Tested**: the second reported the browser already in use). Disable the plugin's copy in `/mcp` if you keep your own.
- Servers that are not configured show as failed or needing sign-in. Disable them in `/mcp`.
- The Figma server may not list separately if the same URL is already configured at user level.

## Runtime validation record (2026-10-04)

Observed in one Claude Code 2.1.285 session with the Hub installed with only the GitHub token prompt (before the Atlassian and PostgreSQL inputs were added). "Callable" means a real tool call returned.

| MCP | Status from `claude mcp list` | Tools exposed to the agent | Representative call | Result |
| --- | --- | --- | --- | --- |
| GitHub, plugin entry | Connected | Yes | `get_me` | Returned the signed-in user. **Callable** |
| GitHub, user-level | Connected | Yes | `get_me` | Returned the same user. **Callable** |
| Atlassian, plugin and user-level | Needs authentication | No Jira tools | None possible | Not runtime-visible. **Not callable** |
| PostgreSQL, plugin entry | Failed (`CONNECTION_CLOSED`, no `DATABASE_URI`) | No | None possible | **Not callable** |
| PostgreSQL, three user-level entries | Connected | Yes | `get_connection_status` on one | Returned server status. A schema query was **not** run (needs a connection string the Hub must not obtain), so schema inspection is unproven |
| Figma, user-level | Connected | Yes | `whoami` | Returned the signed-in account. **Callable**. The plugin's Figma entry did not list separately |
| Playwright, user-level | Connected | Yes | `browser_tabs` list | Returned one blank tab. **Callable** |
| Playwright, plugin entry | Connected | Yes | `browser_tabs` list | Error: browser already in use by the other Playwright server. Visible, not callable while the other holds the profile |
| Azure | Not configured | No | None | Not applicable |

A `grafana` server appeared in the session's tool list under the plugin's namespace but is not in this repository's `mcp.json` or in `claude mcp list`; it was not used and its origin was not investigated.
