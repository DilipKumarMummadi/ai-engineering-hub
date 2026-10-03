# Scenario

The existing Hub still works after packaging.

# Input

Run `python3 scripts/validate-hub/validate_hub.py` and `python3 scripts/project-context/project-context --help` (or its test suite), then `git status` to confirm no file under `.claude/`, `.github/`, `.agents/`, `evals/` (other than `plugin-packaging/`) or `scripts/project-context/` changed.

# Context

Repository at its packaged state.

# Expected Behavior

Hub validation reports no new problems versus before packaging (any pre-existing problem is named, not hidden). Existing tests pass. Native directories are unchanged, so the Hub works without installing the plugin.

# Important Checks

- Packaging only added files, apart from `README.md` and `CHANGELOG.md`.
- Hub link checks still pass for the rewritten README.

# Failure Conditions

- A changed or removed native Hub file.
- A new Hub validation error.

# Notes

Backward compatibility.
