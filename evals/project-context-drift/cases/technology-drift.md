# Scenario

The repository adopted a new framework, dropped another, and moved to a new runtime major version since the context was written. The case checks that technology changes are detected in both directions, with evidence, and classified as Material.

# Input

```
Check PROJECT-CONTEXT.md against the current repository using the Project Context Drift Specification. Report what changed and how important it is.
```

# Context

The existing context (generated) states: Node.js 20 (`.nvmrc`), Express (`package.json`), Jest (`package.json`), PostgreSQL client `pg`.

Current repository:

- `.nvmrc` now says `22`.
- `package.json`: `express` is removed; `fastify` is added as a dependency; `jest` and `pg` are unchanged.
- `src/` still contains the same files, several of them edited.

# Expected Behavior

Three findings in the Technology category, all Material:

- **New:** Fastify detected; the context does not mention it. Evidence: `package.json`.
- **Removed:** Express is documented but no longer detected. It is also listed under Stale Context, and the statement is not deleted.
- **Changed:** the Node.js version recorded in the context (20) differs from the one the repository declares (22). Evidence: `.nvmrc`.

Jest and PostgreSQL are not reported. The source edits are not reported. Status is DRIFT DETECTED, and in CI mode the exit code is 1.

# Important Checks

- Both the added and the removed framework are reported, and neither is treated as "a change in the same thing" without a reason.
- The version change names the old and the new value.
- Each finding cites a repository path.
- Express is reported as potentially stale, not silently removed.
- Unchanged technologies and the edited source files are absent from the report.

# Failure Conditions

- Missing the removal because the new framework was found.
- Reporting the source edits.
- Treating the version change as Informational.
- Modifying the context.

# Notes

A declared dependency is "detected". The report should not claim the framework is used.

The reference implementation reproduces this case as `EvalTechnologyDrift` in `scripts/project-context/tests/test_drift_evals.py`. Related checks are in `test_drift.py`.
