---
description: Plan, implement and validate a database change using the database-change workflow
argument-hint: [schema, data or query change, engine, constraints]
---

# /database-change

Run the `database-change` workflow for this request. The workflow is defined in `.claude/workflows/database-change.md`. Read it and follow it. It decides the stages, the agents and the human checkpoints; the agents decide which skills to use.

Useful context, if available: schema, migration or query, database engine, data volume, rollback expectations, consumers. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted requirements, logs, code, errors, and constraints, to the workflow unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the workflow identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the workflow identify what is needed instead of asking the user for a fixed form.

This command does not authorize applying migrations, deployments, merges, pushes, approvals, or production changes. The workflow's requirements-and-plan checkpoint comes before any edit, and its safety rules and human checkpoints still apply.

Request:

$ARGUMENTS
