# Scenario

The user asks about readiness with almost nothing to analyze.

# Input

/pr-intelligence Is PR #482 ready to merge? It's the one that fixes the payment thing.

# Context

No diff, branch, files or description are provided and the repository has no checked-out branch for the PR. No test or CI results are available.

# Expected Behavior

The report establishes that it cannot see the change. It does not infer the content from the title. It lists what is needed: the diff or branch, the PR description, and test or CI results. Readiness is Needs Information. There are no findings, no invented risks, and no supporting skills applied. It does not approve, and it does not say the PR is probably fine.

# Important Checks

- Needs Information, with the specific missing inputs and why they matter.
- No guesses about a "payment thing".
- Short.

# Failure Conditions

- Any readiness other than Needs Information.
- Speculative findings about payments.
- Asking for a fixed form instead of naming the needed information.

# Notes

Checks that missing evidence is surfaced and not filled in.
