---
description: Design, implement, review, or evolve an API using the api-development-agent
agent: agent
---

# /api

Handle this request with the `api-development-agent`. Read `.github/agents/api-development-agent.md` and follow it. The agent decides which skills to use.

Useful context, if available: the API requirement, existing endpoints, request and response contracts, consumers, authentication, authorization, database behavior, compatibility requirements. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not by itself authorize code changes, breaking contract changes, or data changes.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
