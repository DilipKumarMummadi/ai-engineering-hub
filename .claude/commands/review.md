---
description: Start a PR or code review using the pr-review-agent
argument-hint: [PR, branch, files, or notes]
---

# /review

Use the `pr-review-agent` to handle this request. The agent is defined in `.claude/agents/pr-review-agent.md`. It decides which skills to use.

Useful context, if available: changed files, PR description, the diff, related requirements, test results, known constraints. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, the target is the current uncommitted and branch changes.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize edits, merges, approvals, pushes, or comments on a pull request.

Request:

$ARGUMENTS
