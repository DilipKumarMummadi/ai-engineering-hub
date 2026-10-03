---
description: Investigate a database or SQL issue using the database-troubleshooting-agent
argument-hint: [schema, SQL, error, query plan, engine, expected result]
---

# /database

Use the `database-troubleshooting-agent` to handle this request. The agent is defined in `.claude/agents/database-troubleshooting-agent.md`. It decides which skills to use.

Useful context, if available: schema, the SQL, error, query plan, data examples, database engine, transaction behavior, expected result. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize executing DELETE, UPDATE, DROP, TRUNCATE, ALTER, or any other statement that changes data or schema. The agent's safety rules still apply.

Request:

$ARGUMENTS
