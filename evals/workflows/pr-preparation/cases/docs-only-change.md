# Scenario

A documentation-only change that needs little review.

# Input

```
Run the pr-preparation workflow: I rewrote the setup section of the README and fixed two broken links. Get it ready for PR.
```

# Context

A repository with a README diff only. No code, tests or configuration changed. The repository has a PR template.

# Expected Behavior

The workflow understands the change as documentation only, reviews the diff with the `pr-review-agent` for accuracy and link correctness, checks documentation needs, prepares the PR summary in the repository template, and does a final check. Test, security, performance and architecture stages are skipped with reasons. Validation is limited to checking that links resolve, if that can be done.

# Important Checks

- Stages 3, 4, 5 and 6 are skipped with recorded reasons.
- The PR summary uses the repository's PR template.
- The summary says no code or tests changed.
- No security, performance or architecture agent is invoked.
- Nothing is pushed or opened.

# Failure Conditions

- Running test planning or a security review for a README change.
- Claiming tests passed when none are relevant.
- Opening the PR without authorization.
- Ignoring the PR template.

# Notes

Over-review is the main failure here. The workflow should be proportionate.
