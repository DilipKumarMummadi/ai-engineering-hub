---
description: Design, implement, review, or evolve an API using the api-development-agent
argument-hint: [API requirement or change, existing endpoints, consumers]
---

# /api

Use the `api-development-agent` to handle this request. The agent is defined in `.claude/agents/api-development-agent.md`. It decides which skills to use.

Useful context, if available: the API requirement, existing endpoints, request and response contracts, consumers, authentication, authorization, database behavior, compatibility requirements. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not by itself authorize code changes, breaking contract changes, or data changes.

Request:

$ARGUMENTS
