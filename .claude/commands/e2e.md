---
description: Create a browser end-to-end test using the e2e-test-creation workflow
argument-hint: [user flow or scenario to cover]
---

# /e2e

Run the `e2e-test-creation` workflow for this request. The workflow is defined in `.claude/workflows/e2e-test-creation.md`. Read it and follow it. It decides the stages, the agents and the human checkpoints; the agents decide which skills to use.

Useful context, if available: user flow, acceptance criteria, environment, existing tests, test data and authentication. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted requirements, logs, code, errors, and constraints, to the workflow unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the workflow identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the workflow identify what is needed instead of asking the user for a fixed form.

This command does not authorize applying migrations, deployments, merges, pushes, approvals, or production changes. The workflow's requirements-and-plan checkpoint comes before any edit, and its safety rules and human checkpoints still apply.

Request:

$ARGUMENTS
