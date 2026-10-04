# Scenario

A repository-specific `PROJECT-CONTEXT.md` appears in the package, and a nested MCP configuration file appears.

# Input

In a scratch copy, create `skills/testing/PROJECT-CONTEXT.md`, `com.github.copilot/PROJECT-CONTEXT.md`, and `skills/testing/.mcp.json`. Also confirm `templates/project-context/PROJECT-CONTEXT.md` (the blank template) is not flagged.

# Context

Scratch copy of the package.

# Expected Behavior

The context files and the nested MCP file are reported (MCP configuration is allowed only in the root `mcp.json`). The blank template is allowed because it is a template, not a repository's context. Also confirm by search that the real repository has no `PROJECT-CONTEXT.md` outside the template.

# Important Checks

- Case-exact matching: `docs/project-context.md` is not flagged.
- The template is not flagged.

# Failure Conditions

- A repository context packaged.
- A nested MCP file accepted.
- The specification doc or template flagged.

# Notes

Project Context stays repository-specific; MCP configuration confined to the root file.
