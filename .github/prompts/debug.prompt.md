---
description: Investigate an unexpected behavior or failure using the bug-investigation-agent
agent: agent
---

# /debug

Handle this request with the `bug-investigation-agent`. Read `.github/agents/bug-investigation-agent.md` and follow it. The agent decides which skills to use.

Useful context, if available: error message, logs, stack trace, reproduction steps, expected behavior, actual behavior, recent changes, environment. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize changes to code, data, configuration, or infrastructure.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
