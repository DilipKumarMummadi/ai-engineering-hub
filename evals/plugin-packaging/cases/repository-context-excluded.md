# Scenario

A repository-specific `PROJECT-CONTEXT.md` and an `mcp.json` appear in the package.

# Input

In a scratch copy, create `skills/testing/PROJECT-CONTEXT.md`, `com.github.copilot/PROJECT-CONTEXT.md`, and a root `mcp.json`. Also confirm `templates/project-context/PROJECT-CONTEXT.md` (the blank template) is not flagged.

# Context

Scratch copy of the package.

# Expected Behavior

The context files and `mcp.json` are reported. The blank template is allowed because it is a template, not a repository's context. Also confirm by search that the real repository has no `PROJECT-CONTEXT.md` and no `mcp.json`.

# Important Checks

- Case-exact matching: `docs/project-context.md` is not flagged.
- The template is not flagged.

# Failure Conditions

- A repository context packaged.
- Any MCP file accepted.
- The specification doc or template flagged.

# Notes

Project Context stays repository-specific; no MCP.
