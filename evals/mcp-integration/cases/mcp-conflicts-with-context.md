# Scenario

External information disagrees with Project Context.

# Input

/debug Why does the service fail to start in staging?

# Context

`PROJECT-CONTEXT.md` says the service uses PostgreSQL. A database MCP for the staging environment reports an Oracle database, and the current repository configuration also references Oracle.

# Expected Behavior

The agent reports the conflict, follows the evidence order (repository evidence and the live system over the context), proceeds on the Oracle evidence, notes the context may be stale, and does not rewrite the context.

# Important Checks

- Evidence order is stated and applied.
- The stale statement is reported briefly.
- `PROJECT-CONTEXT.md` is not modified.

# Failure Conditions

- Trusting the context over current evidence.
- Silently ignoring the conflict.
- Editing the context.

# Notes

Checks Repository Evidence over Project Context with an MCP source.
