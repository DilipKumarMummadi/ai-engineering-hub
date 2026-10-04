# MCP Clients

How each client supplies the runtime configuration that the portable `mcp.json` deliberately leaves out. Only behavior that was verified from the client's own documentation or exercised here is described. Nothing on these pages is part of Agent Plugins 1.0.0.

| Client | Page | Loads the plugin's `mcp.json` | GitHub authentication | Local server environment |
| --- | --- | --- | --- | --- |
| Claude Code | [claude-code.md](claude-code.md) | Yes, through `.claude-plugin/plugin.json` | Optional install-time inputs for GitHub, Atlassian and PostgreSQL; empty falls back to your own client/shell configuration | Reads variables set in the launching shell (not separately verified) |
| GitHub Copilot CLI | [github-copilot.md](github-copilot.md) | Yes | Built-in GitHub server (documented) | Only `PATH` is inherited; other values go in the client's config |
| GitHub Copilot in VS Code, other Agent Plugins clients | Not covered | Not tested | Not tested | Not tested |

Legend used on the client pages: **Tested** means it was run in this repository's validation; **Documented** means it is stated in the client's official documentation but was not run; **Not tested** means neither.

See [Runtime Configuration](../mcp-runtime-configuration.md) for the model and [MCP Registry](../mcp-registry.md) for the servers.
