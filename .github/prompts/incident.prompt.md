---
description: Investigate an active or recent production incident using the production-incident-agent
agent: agent
---

# /incident

Handle this request with the `production-incident-agent`. Read `.github/agents/production-incident-agent.md` and follow it. The agent decides which skills to use.

Useful context, if available: incident description, impact, timeline, logs, metrics, traces, alerts, recent deployments, affected services, dependencies. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted logs, code, errors, and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command does not authorize production changes such as rollback, restart, scaling, failover, feature flag or configuration changes, killing sessions, or data changes. The agent's safety rules still apply.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
