---
description: Investigate a database or SQL issue using the database-troubleshooting-agent
agent: agent
---

# /database

Handle this request with the `database-troubleshooting-agent`. Read `.github/agents/database-troubleshooting-agent.md` and follow it. The agent decides which skills to use.

Useful context, if available: schema, the SQL, error, query plan, data examples, database engine, transaction behavior, expected result. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize executing DELETE, UPDATE, DROP, TRUNCATE, ALTER, or any other statement that changes data or schema. The agent's safety rules still apply.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
