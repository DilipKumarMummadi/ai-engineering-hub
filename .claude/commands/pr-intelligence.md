---
description: Assess whether a pull request or change is ready, using the pr-intelligence-agent
argument-hint: [PR, branch, diff, files, or notes]
---

# /pr-intelligence

Use the `pr-intelligence-agent` to handle this request. The agent is defined in `.claude/agents/pr-intelligence-agent.md`. It decides which skills to use.

Useful context, if available: the diff or changed files, the PR description, commit history, test and CI results, known constraints. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted diffs, logs, code, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, the target is the current uncommitted and branch changes.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command is analysis only. It does not authorize edits, commits, pushes, approvals, merges, deployments, or comments on a pull request.

Request:

$ARGUMENTS
