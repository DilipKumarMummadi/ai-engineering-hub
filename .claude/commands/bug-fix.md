---
description: Fix a defect, with a regression test, using the bug-fix workflow
argument-hint: [bug report, error, reproduction steps, expected behavior]
---

# /bug-fix

Run the `bug-fix` workflow for this request. The workflow is defined in `.claude/workflows/bug-fix.md`. Read it and follow it. It decides the stages, the agents and the human checkpoints; the agents decide which skills to use.

Useful context, if available: bug report, error message, logs, reproduction steps, expected and actual behavior, recent changes. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted requirements, logs, code, errors, and constraints, to the workflow unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the workflow identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the workflow identify what is needed instead of asking the user for a fixed form.

This command does not authorize applying migrations, deployments, merges, pushes, approvals, or production changes. The workflow's requirements-and-plan checkpoint comes before any edit, and its safety rules and human checkpoints still apply.

Request:

$ARGUMENTS
