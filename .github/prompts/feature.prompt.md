---
description: Develop a new feature end to end using the feature-development workflow
agent: agent
---

# /feature

Handle this request with the `feature-development` workflow. Read `.github/workflows/feature-development.md` and follow it. It decides the stages, the agents and the human checkpoints; the agents decide which skills to use.

Useful context, if available: requirement or ticket, acceptance criteria, affected areas, constraints, deadlines. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted requirements, logs, code, errors, and constraints, to the workflow unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, pass that fact on and let the workflow identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the workflow identify what is needed instead of asking the user for a fixed form.

This command does not authorize applying migrations, deployments, merges, pushes, approvals, or production changes. The workflow's requirements-and-plan checkpoint comes before any edit, and its safety rules and human checkpoints still apply.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
