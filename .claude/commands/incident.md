---
description: Investigate an active or recent production incident using the production-incident-agent
argument-hint: [what is failing, impact, timeline, logs, metrics, recent deployments]
---

# /incident

Use the `production-incident-agent` to handle this request. The agent is defined in `.claude/agents/production-incident-agent.md`. It decides which skills to use.

Useful context, if available: incident description, impact, timeline, logs, metrics, traces, alerts, recent deployments, affected services, dependencies. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request below, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request below is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize production changes such as rollback, restart, scaling, failover, feature flag or configuration changes, killing sessions, or data changes. The agent's safety rules still apply.

Request:

$ARGUMENTS
