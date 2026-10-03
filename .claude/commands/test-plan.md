---
description: Create a test strategy or test plan using the test-planning-agent
argument-hint: [feature, requirement, change, or acceptance criteria]
---

# /test-plan

Use the `test-planning-agent` to handle this request. The agent is defined in `.claude/agents/test-planning-agent.md`. It decides which skills to use.

Useful context, if available: the requirement or feature, changed code, acceptance criteria, existing tests, test environment, browser flow, if applicable. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, the target is the feature or change currently being worked on.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize changes to code, tests, or data.

Request:

$ARGUMENTS
