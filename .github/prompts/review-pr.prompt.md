---
description: Review a GitHub pull request by URL or number, using the pr-intelligence-agent
agent: agent
---

# /review-pr

Use the `pr-intelligence-agent` to handle this request. The agent is defined in `.github/agents/pr-intelligence-agent.md`. It decides which skills to use.

The request names a pull request: a URL such as `https://github.com/org/repo/pull/123`, or a number such as `123` for the repository of the current directory. The agent retrieves the pull request through the source-control capability, which is an MCP server the client has connected and signed in to. This command never handles credentials. Do not ask the user for a token, and do not try to authenticate.

Useful context, if available: notes from the user, known constraints, a locally available diff to fall back on. Pass along whatever you already have.

Tell the agent the request came from `/review-pr` so it reports in the PR review form. Pass the full request below unchanged. Do not summarize or drop detail. Keep the constraints the user stated.

If the request below is empty, ask for a pull request URL or number.

Do not add engineering instructions of your own. If important information is missing, let the agent identify what is needed.

This command is analysis only. It does not authorize approvals, merges, comments or changes on the pull request, nor edits, commits, pushes or deployments.

The request is everything the user wrote after this prompt, plus any attached files, selection, or chat context.
