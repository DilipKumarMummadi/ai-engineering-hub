---
description: Start a PR or code review using the pr-review-agent
agent: agent
---

# /review

Handle this request with the `pr-review-agent`. Read `.github/agents/pr-review-agent.md` and follow it. The agent decides which skills to use.

Useful context, if available: changed files, PR description, the diff, related requirements, test results, known constraints. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, the target is the current uncommitted and branch changes.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize edits, merges, approvals, pushes, or comments on a pull request.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
