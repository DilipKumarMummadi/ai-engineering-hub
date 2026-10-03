# Scenario

Client-specific resources are kept apart from the portable core.

# Input

Inspect the package: `plugin.json` has no Copilot or Claude fields and no `extensions` entry; `com.github.copilot/` holds only documentation; agents, commands and workflows remain in `.claude/` and `.github/`; add `evals/` content under `com.github.copilot/` in a scratch copy.

# Context

Repository at its packaged state, plus a scratch copy.

# Expected Behavior

No client-specific metadata is in the portable core; agent logic is not duplicated under the namespace; eval content under the namespace is rejected. `docs/plugin-architecture.md` explains why agents are not repackaged.

# Important Checks

- `diff -r .github/agents` shows the originals untouched.
- No agent, command or workflow copy exists outside its native directory.

# Failure Conditions

- Copilot fields in the core manifest.
- Duplicated agent logic.
- Evals or scripts packaged as client content.

# Notes

Separation of portable and client-specific content.
