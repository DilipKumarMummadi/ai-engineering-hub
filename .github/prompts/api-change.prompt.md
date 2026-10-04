---
description: Design, implement and validate an API change using the api-change workflow
agent: agent
---

# /api-change

Handle this request with the `api-change` workflow. Read `.github/workflows/api-change.md` and follow it. It decides the stages, the agents and the human checkpoints; the agents decide which skills to use.

Useful context, if available: API requirement, existing endpoints, contracts, consumers, compatibility requirements, authentication and authorization. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted requirements, logs, code, errors, and constraints, to the workflow unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, pass that fact on and let the workflow identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the workflow identify what is needed instead of asking the user for a fixed form.

This command does not authorize applying migrations, deployments, merges, pushes, approvals, or production changes. The workflow's requirements-and-plan checkpoint comes before any edit, and its safety rules and human checkpoints still apply.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
