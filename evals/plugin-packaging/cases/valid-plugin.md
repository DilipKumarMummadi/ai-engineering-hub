# Scenario

The unmodified repository is validated as an Agent Plugin.

# Input

Run `python3 scripts/validate-plugin/validate_plugin.py` and `python3 scripts/validate-plugin/test_validate_plugin.py`.

# Context

Repository at its packaged state: `plugin.json`, 13 skills under `skills/`, `README.md`, `docs/plugin-architecture.md`.

# Expected Behavior

The validator reports OK with 13 skills. The manifest uses the canonical 1.0.0 `$schema`, name `ai-engineering-hub`, semantic version, and only permitted core fields. Tests pass.

# Important Checks

- Exactly 13 skills are discovered.
- `skills/` matches `.claude/skills/`.
- No MCP, evals or scripts in packaged directories.

# Failure Conditions

- Any error on an unmodified package.
- A skill missing or extra.

# Notes

Manifest correctness, package structure and skill discovery.
