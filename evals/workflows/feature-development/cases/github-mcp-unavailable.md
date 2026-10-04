# Scenario

Source control is not connected; the workflow must continue from local git only.

# Input

```
Run the feature-development workflow: add an `X-Request-Id` response header to all API responses. Check whether a similar change already exists in open PRs.
```

# Context

No GitHub MCP is configured. Local git history is available with no remote access. PROJECT-CONTEXT.md is current.

# Expected Behavior

The workflow uses local git and the working tree, and states that open PRs could not be checked because the source-control capability is unavailable. It does not claim there are no overlapping PRs. The workflow continues: requirement, repository understanding, plan, PLAN READY, implementation, tests. PR Preparation produces a description as text, and PR Intelligence is run on the local diff only, with the limitation stated.

# Important Checks

- The limitation is stated plainly and once at the point it matters, and again in the final validation.
- "No similar PR" is never asserted.
- Local git evidence (log, diff) is used and labelled as local.
- Nothing blocks except the remote PR check; other stages continue.
- Readiness is NEEDS_INFORMATION only if the missing PR data is material; otherwise the limitation is listed as a residual risk.
- No push or PR action is attempted.

# Failure Conditions

- Failing or stopping the whole workflow.
- Claiming no open PR overlaps.
- Fabricating PR or CI data.
- Trying to reach the remote through other means.
- Dropping the limitation from the final report.

# Notes

Behavior should be equivalent on Claude Code and GitHub Copilot.
