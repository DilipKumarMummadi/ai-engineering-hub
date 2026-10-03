# Scenario

An existing context, written some time ago, no longer matches the repository. The case checks stale-context detection, minimal updates, preservation of manual content, and honest freshness metadata.

# Input

```
Update PROJECT-CONTEXT.md for this repository using the Project Context Generator Specification. Show me what would change and why. Don't write the file yet.
```

# Context

Existing `PROJECT-CONTEXT.md` (abridged):

```
## Metadata
- Project: Tool Loans API
- Last Reviewed: 14 months ago
- Source Files Inspected: package.json, Jenkinsfile, README.md
- Known Stale Sections: none known

## Technology Stack
- Node.js 16 — Confirmed — .nvmrc
- Express — Confirmed — package.json
- Jest — Confirmed — package.json

## Testing Conventions
- Test command: `npm test` runs jest — Confirmed — package.json

## CI/CD
- CI runs on Jenkins — Confirmed — Jenkinsfile

## Repository Structure
- src/ (routes, services, db), test/ — Confirmed

## Important Constraints
- No new runtime dependencies without approval from the platform team — Confirmed — developer-provided

<!-- manual:start -->
## Team Notes
Release freeze every second Friday. Ask in the platform channel before touching the loan-expiry job.
<!-- manual:end -->
```

Current repository state:

- `.nvmrc` now says `20`.
- `package.json`: scripts `test` runs `vitest`; `jest` is no longer a dependency; `vitest` is a devDependency; `express` is still a dependency.
- The `Jenkinsfile` no longer exists. `.github/workflows/ci.yml` exists and runs install, lint and test on pull requests.
- A new directory `services/notifications/` exists with its own `package.json`.
- `src/` and `test/` are unchanged.
- `README.md` is unchanged.

# Expected Behavior

The generator runs in update mode. It re-verifies the entries against their named sources and finds:

- **Changed:** Node version (16 to 20, `.nvmrc`); test framework and command (Jest to Vitest, `package.json`); CI platform (Jenkins to GitHub Actions, `ci.yml`, the Jenkinsfile no longer exists).
- **Unchanged:** Express; `src/` and `test/` structure. These entries are left exactly as they are and not reworded.
- **New:** the `services/notifications/` component (a separate package), recorded as a new application component, with its own commands Unknown unless its `package.json` shows them.
- **Preserved:** the developer-provided constraint, and the manual block, both unchanged.
- **Freshness:** Last Reviewed and Source Files Inspected updated to what was inspected in this run; the stale state of the old context noted in the change summary.

The output is a diff with reasons, not a full rewrite, plus the report. Pipeline details such as the deployment approach stay Unknown unless the new workflow shows them.

# Important Checks

- The three changed entries are detected from current evidence, each with its new source.
- The Jenkins entry is not left as a fact. It is replaced because the current pipeline exists, and the removal is reported.
- Unchanged entries are not touched.
- The constraint and the manual block are preserved exactly.
- The new component is added, and the generator does not assume it shares the main application's commands.
- The change summary lists each change with its reason.
- Last Reviewed and Source Files Inspected describe this run. They do not claim files that were not inspected.
- The generator does not run the test suite or the pipeline to confirm the new command.
- No duplicate entries are created (for example both Jest and Vitest listed as current).

# Failure Conditions

- Regenerating the whole file and rewording unchanged entries.
- Keeping Jest, Node 16 or Jenkins as current.
- Removing or editing the manual block or the constraint.
- Updating the review date without re-verifying the entries.
- Dropping a stale entry without recording the change.
- Adding the new component's commands by assumption.
- Listing both the old and new values as current.

# Notes

The old context is not treated as wrong in spirit. It was right when written. The point is that the update is proportionate, visible and honest about what was re-checked.

The reference implementation reproduces this case as `EvalStaleContext` in `scripts/project-context/tests/test_evals.py`. See the implementation results in the evals README.
