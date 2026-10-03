---
description: Create a test strategy or test plan using the test-planning-agent
agent: agent
---

# /test-plan

Handle this request with the `test-planning-agent`. Read `.github/agents/test-planning-agent.md` and follow it. The agent decides which skills to use.

Useful context, if available: the requirement or feature, changed code, acceptance criteria, existing tests, test environment, browser flow, if applicable. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, the target is the feature or change currently being worked on.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize changes to code, tests, or data.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
