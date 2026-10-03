# Scenario

A repository whose context was generated recently. Nothing about the repository itself has changed. The case checks that the detector stays quiet and says so.

# Input

```
Check whether PROJECT-CONTEXT.md is still accurate for this repository, using the Project Context Drift Specification. Don't change anything.
```

# Context

A Node.js repository with a generated `PROJECT-CONTEXT.md` (reviewed last week).

- `package.json`: `express`, `pg` dependencies; `jest`, `eslint` devDependencies; scripts `start`, `test`, `lint`.
- `.nvmrc`: `20`. `Dockerfile` based on `node:20`. `.env.example` with placeholder values.
- `src/` (routes, services, db) and `test/`.
- The context records Node.js 20, Express, PostgreSQL, Jest, Docker, and the `src`/`test` layout.
- Since the context was generated, a dependency patch version was bumped in `package.json` (`express` from `^4.18.0` to `^4.19.2`), and `README.md` was reworded.

# Expected Behavior

The detector compares the context with current evidence and finds every documented capability still supported. It reports status `NO DRIFT`, has no Material or Potentially Material section, says no action is needed, and changes nothing. In CI mode it exits 0.

# Important Checks

- Status is NO DRIFT.
- The patch bump and the README rewording are not reported as drift.
- Unchanged technologies (Express, PostgreSQL, Jest, Docker) are not listed as changes.
- No file, including `PROJECT-CONTEXT.md`, was modified.
- The recommendation says no action is needed and does not suggest regenerating.

# Failure Conditions

- Reporting drift for a version bump within the same major version, or for the documentation change.
- Suggesting that the context be regenerated "to be safe".
- Writing or touching any file.
- Listing every file that changed as a finding.

# Notes

The most common failure of a drift detector is noise. A tool that cries wolf on every pull request is switched off within a week.

The reference implementation reproduces this case as `EvalNoDrift` in `scripts/project-context/tests/test_drift_evals.py`. Related checks are in `test_drift.py`.
