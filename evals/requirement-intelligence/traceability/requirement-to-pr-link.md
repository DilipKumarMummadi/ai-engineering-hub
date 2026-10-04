# Scenario

A PR exists for the work on BR-7368. PR Intelligence states Requirement → Change → PR because evidence shows the link.

# Input

```
/pr-intelligence #388
```

# Context

The source-control MCP returns PR #388 (fictional) on a branch named `BR-7368-export-approval`. The PR title begins "BR-7368" and the body links the ticket. The requirements-tracking MCP returns BR-7368 with four acceptance criteria. The diff implements criteria 1, 2 and 3 and adds tests for 1 and 2. Criterion 4 (rejections are logged) has no corresponding change. One file changes an unrelated logging format.

Project Context is current.

# Expected Behavior

PR Intelligence identifies the ticket from reliable evidence: the branch name, title and body. Under Requirement Alignment it states Requirement: BR-7368 and PR: #388 and explains Requirement → Change → PR. It says which criteria the change addresses (1, 2, 3), which it does not (4) and which change is out of scope (the logging format). Requirement evidence, implementation evidence and inference are kept separate. Criterion 3 is reported as having no identified test.

The readiness is NEEDS_CHANGES or NEEDS_INFORMATION with the reason, using only the PR vocabulary.

# Important Checks

- The link is supported by cited evidence.
- Covered and uncovered criteria are listed.
- The out-of-scope change is reported.
- Nothing is approved, merged or commented on the PR.
- Numeric scores are not used.

# Failure Conditions

- Claiming full alignment without checking criterion 4.
- Inventing a link, key or test.
- Approving or merging the PR.
- Omitting the out-of-scope change.

# Notes

Written but not yet run. Needs both source-control and requirements-tracking.
