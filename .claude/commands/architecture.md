---
description: Analyze or design system architecture using the architecture-agent
argument-hint: [problem, requirements, constraints, current architecture]
---

# /architecture

Use the `architecture-agent` to handle this request. The agent is defined in `.claude/agents/architecture-agent.md`. It decides which skills to use.

Useful context, if available: requirements, current architecture, constraints, scale, integrations, reliability requirements, security requirements, cost constraints. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize changes to code, infrastructure, or configuration.

Request:

$ARGUMENTS
