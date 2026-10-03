---
description: Analyze the engineering impact of a change using the change-intelligence-agent
argument-hint: [diff, branch, commit range, PR, files, or notes]
---

# /change-impact

Use the `change-intelligence-agent` to handle this request. The agent is defined in `.claude/agents/change-intelligence-agent.md`. It decides which skills to use.

Useful context, if available: the diff, commit range or changed files, the PR description or intent, known consumers, environments and constraints. Pass along whatever you already have. Do not require anything in a fixed form, and do not require Git if another form of the change is given.

Pass the full request below, including any pasted diffs, code, configuration, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, the target is the current uncommitted and branch changes.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command is analysis only. It does not authorize edits, commits, pushes, merges, deployments, migrations, or running anything that changes a system.

Request:

$ARGUMENTS
