---
description: Analyze, refine and assess the readiness of a requirement or Jira issue, using the requirement-intelligence-agent
agent: agent
---

# /requirement

Handle this request with the `requirement-intelligence-agent`. Read `.github/agents/requirement-intelligence-agent.md` and follow it. The agent decides which skills to use.

The request normally starts with an issue key such as `BR-7368`, or with requirement text. An optional word after it selects the mode: `analyze`, `refine`, `readiness`, `inspect` or `update`. With no mode word, the agent starts an interactive, read-only session: it shows the requirement, its analysis and readiness, and asks the most valuable clarification question if one is needed. The user then answers, adds context or rewrites the requirement in plain language, and the agent keeps going. Pass the words to the agent as written. Do not parse or rewrite them.

Useful context, if available: the requirement text, acceptance criteria, affected areas, constraints, deadlines. Pass along whatever you already have. Do not require anything in a fixed form.

Pass the full request, including any pasted requirements, logs, code and constraints, to the agent unchanged. Do not summarize or drop technical detail. Keep the constraints the user stated.

If the request is empty, pass that fact on and let the agent identify what it needs.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed instead of asking the user for a fixed form.

This command is analysis and preparation only. It does not authorize implementation, edits, commits, pushes, merges, deployments, migrations or production changes. In particular, the `update` word prepares a ticket update and shows the exact difference. It does not authorize writing it. A ticket is written only after the user explicitly approves the difference the agent has shown.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
