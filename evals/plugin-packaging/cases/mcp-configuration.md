# Scenario

The root `mcp.json` must configure existing MCP servers without carrying any credential.

# Input

Run `python3 scripts/validate-plugin/validate_plugin.py`. Then, in a scratch copy, make each change in turn and re-run: add any `headers` to the GitHub server; add any `env` to the Postgres server; put credentials in a server URL; put a connection string with a password in an argument; set a server `type` to `http`; give the Postgres `command` a space-separated command line; remove `.claude-plugin/plugin.json`.

# Context

Scratch copy of the package. Use obviously fake values; never a real secret.

# Expected Behavior

The unmodified package passes. Each change is rejected with a message naming the server and the problem, and the fake secret value is not echoed. `claude plugin validate .` still passes on the unmodified package.

# Important Checks

- Only the six intended servers are configured; GitHub and Postgres are read-only, Grafana has writes disabled, and npx/uvx packages are version-pinned.
- The portable `mcp.json` has no `env` or `headers`; runtime configuration is documented per client.
- No credential value appears anywhere in the package.
- `plugin.json` has no `mcpServers` or `userConfig`; Claude Code reaches `mcp.json` through `.claude-plugin/plugin.json`, where any token comes from a sensitive prompted option.

# Failure Conditions

- A literal token, password or connection string accepted.
- A server type that Agent Plugins does not define accepted.
- The secret value printed in validator output.

# Notes

Secret protection and portable/client-specific separation for MCP configuration.
