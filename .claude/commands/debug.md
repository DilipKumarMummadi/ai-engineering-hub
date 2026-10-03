---
description: Investigate an unexpected behavior or failure using the bug-investigation-agent
argument-hint: [error, stack trace, logs, what you expected vs what happened]
---

# /debug

Use the `bug-investigation-agent` to handle this request. The agent is defined in `.claude/agents/bug-investigation-agent.md`. It decides which skills to use.

Useful context, if available: error message, logs, stack trace, reproduction steps, expected behavior, actual behavior, recent changes, environment. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize changes to code, data, configuration, or infrastructure.

Request:

$ARGUMENTS
