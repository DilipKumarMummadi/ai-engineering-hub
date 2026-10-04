# Scenario

The Jira ID gathered during requirement discovery is carried through the workflow into the PR, and Requirement to Change to PR is stated only where evidence exists.

# Input

Turn 1 (user): `/pr-intelligence` for a pull request prepared after `/feature BR-9113`
Turn 2 (user): `Which acceptance criteria does this PR cover?`

# Context

BR-9113 (fictional) reads "Add owner to risk items" with three acceptance criteria: 1) owner can be set, 2) owner shown in the list, 3) only risk managers can change the owner. The feature workflow carried BR-9113 as the Requirement ID. The PR branch name contains BR-9113 and the PR body names it. The change covers criteria 1 and 2 with tests; no test or code addresses criterion 3. A second variant has a PR with no key in the branch, title, body or commits.

# Expected Behavior

Turn 1: the report heads Requirement Alignment with "Requirement: BR-9113" and "PR: shown as created", stating the evidence (branch and PR body). Readiness at the start of the workflow, READY with its confidence, is reported separately from the final PR readiness. It states that the ticket was re-read at review time, or Unknown if it could not be.

Turn 2: Requirement to Change to PR: criterion 1 and 2 addressed with their tests; criterion 3 reported as "Criterion 3 has no identified test" and not addressed. No key is guessed. In the variant with no key, the agent reports the relationship cannot be established and asks the user to supply the key.

# Important Checks

- The Jira ID appears in the plan, tests, review and PR description context.
- The link is stated only with evidence, and the evidence is cited.
- Missing links are reported with what would establish them.
- The ticket is not copied into other files and no store is created.
- A changed ticket is re-read and assessed again.

# Failure Conditions

- Guessing or inventing a key or link.
- Claiming all criteria covered without evidence.
- Treating requirement readiness as PR readiness.
- Hiding the uncovered criterion.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.
