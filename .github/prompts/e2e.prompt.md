---
description: Create a browser end-to-end test using the e2e-test-creation workflow
agent: agent
---

# /e2e

Handle this request with the `e2e-test-creation` workflow. Read `.github/workflows/e2e-test-creation.md` and follow it. It decides the stages, the agents and the human checkpoints; the agents decide which skills to use.

Useful context, if available: user flow, acceptance criteria, environment, existing tests, test data and authentication. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted requirements, logs, code, errors, and constraints, to the workflow unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, pass that fact on and let the workflow identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the workflow identify what is needed instead of asking the user for a fixed form.

This command does not authorize applying migrations, deployments, merges, pushes, approvals, or production changes. The workflow's requirements-and-plan checkpoint comes before any edit, and its safety rules and human checkpoints still apply.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
