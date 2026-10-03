---
description: Assess whether a pull request or change is ready, using the pr-intelligence-agent
agent: agent
---

# /pr-intelligence

Handle this request with the `pr-intelligence-agent`. Read `.github/agents/pr-intelligence-agent.md` and follow it. The agent decides which skills to use.

Useful context, if available: the diff or changed files, the PR description, commit history, test and CI results, known constraints. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted diffs, logs, code, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, the target is the current uncommitted and branch changes.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command is analysis only. It does not authorize edits, commits, pushes, approvals, merges, deployments, or comments on a pull request.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
