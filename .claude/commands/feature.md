---
description: Develop a new feature end to end using the feature-development workflow
argument-hint: [feature requirement, ticket, acceptance criteria, constraints]
---

# /feature

Run the `feature-development` workflow for this request. The workflow is defined in `.claude/workflows/feature-development.md`. Read it and follow it. It decides the stages, the agents and the human checkpoints; the agents decide which skills to use.

Useful context, if available: requirement or ticket, acceptance criteria, affected areas, constraints, deadlines. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted requirements, logs, code, errors, and constraints, to the workflow unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the workflow identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the workflow identify what is needed instead of asking the user for a fixed form.

This command does not authorize applying migrations, deployments, merges, pushes, approvals, or production changes. The workflow's requirements-and-plan checkpoint comes before any edit, and its safety rules and human checkpoints still apply.

Request:

$ARGUMENTS
