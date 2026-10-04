# Scenario

The root `mcp.json` must configure existing MCP servers without carrying any credential.

# Input

Run `python3 scripts/validate-plugin/validate_plugin.py`. Then, in a scratch copy, make each change in turn and re-run: add any `headers` to the GitHub server; add any `env` to the Postgres server; put credentials in a server URL; put a connection string with a password in an argument; set a server `type` to `http`; give the Postgres `command` a space-separated command line; remove `.claude-plugin/plugin.json`.

# Context

Scratch copy of the package. Use obviously fake values; never a real secret.

# Expected Behavior

The unmodified package passes. Each change is rejected with a message naming the server and the problem, and the fake secret value is not echoed. `claude plugin validate .` still passes on the unmodified package.

# Important Checks

- Only the five intended servers are configured (GitHub, Atlassian, Figma, Postgres, Playwright); GitHub and Postgres are read-only, and npx/uvx packages are version-pinned. No observability MCP is configured; it is deferred to a later phase.
- The portable `mcp.json` has no `env` or `headers`; runtime configuration is documented per client.
- No credential value appears anywhere in the package.
- `plugin.json` has no `mcpServers` or `userConfig`; Claude Code reaches `mcp.json` through `.claude-plugin/plugin.json`, which references `./mcp.json` plus overrides for `github`, `atlassian` and `postgres`. Its only credential inputs are optional, sensitive `userConfig` options (`github_token`, `atlassian_auth`, `postgres_database_uri`) referenced as `${user_config.KEY}`; no literal credential appears. Leaving an input empty falls back to the user's own client or shell configuration.

# Failure Conditions

- A literal token, password or connection string accepted.
- A server type that Agent Plugins does not define accepted.
- The secret value printed in validator output.

# Notes

Secret protection and portable/client-specific separation for MCP configuration.
