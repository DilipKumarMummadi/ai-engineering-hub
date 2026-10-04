# MCP Setup Guide

A conceptual guide to connecting the external systems the Hub's agents can use. The Hub does not collect, store or implement authentication. You authenticate in your own client; the Hub only asks for a capability and uses whatever provider answers.

Client-specific steps are limited to mechanisms verified on the [client pages](mcp-clients/README.md). This guide does not add commands of its own.

## The Six Steps

1. **Install the plugin.** It packages the Hub's skills and, where the client supports it, a static list of existing MCP servers (`mcp.json`). It holds no credentials.
2. **Choose the capabilities you need.** Nothing is required. Common ones: `source-control` for `/review-pr`, `requirements-tracking` for requirement checks, `database` for database troubleshooting, `browser-automation` for end-to-end tests. See the [Capability Registry](mcp-capability-registry.md).
3. **Connect a provider in your client.** Enable the bundled server, or one you already have, for each capability you chose. Servers you do not need can stay disabled.
4. **Authenticate in the client.** Sign in with OAuth, or supply a token or connection through the client's own mechanism or your secret store. The Hub never asks for, sees or stores these.
5. **Add team and environment configuration in the client.** For example, one named database entry per team and environment, and the Jira project your team uses. Keep these out of the Hub repository. See [Runtime Configuration](mcp-runtime-configuration.md).
6. **Verify.** Confirm in your client that the server is connected. Run a read-only task, such as `/review-pr` on a PR you can access, and check that the answer says where its information came from. If a capability is missing, the agent reports it and continues with what it has.

## What Installation Does

Installing the Hub installs skills, agents and commands, and declares five existing servers (`mcp.json`). It asks for **no** credential and does not fail if a server is unavailable. Afterwards each server is in one of these situations, decided by your client, not the Hub:

| Situation | Typical cause | What you do |
| --- | --- | --- |
| Connected and tools exposed | You already use that MCP, or signed in | Nothing. The Hub uses it |
| Needs sign-in | OAuth server (Atlassian, Figma) | Sign in from the client (`/mcp`) |
| Failed | No connection supplied (PostgreSQL), or no credential entered at install (GitHub or Atlassian plugin entry) | Configure it once in your client, or disable the plugin's copy |
| Not present | Not bundled (Azure) or not enabled | Add it in your client if you want the capability |

You never configure a server twice. If you already have a GitHub, Atlassian, PostgreSQL, Figma or Playwright MCP, the Hub uses the tools your client exposes; disable the plugin's duplicate entry if it conflicts.

## Adding a Server Later

Configure it in your client as you normally would. The Hub holds no copy of the configuration, so it needs no reinstall. Capabilities are resolved from the tools exposed when they are needed, so the next task (or the next session, if your client only loads servers at start) sees it. Confirm with your client's MCP status command. This platform offers the Hub no supported way to read your MCP configuration or to be notified, so none is attempted.

## What the Hub Does Not Do

- It does not collect, store, forward or implement authentication of any kind.
- It does not ship an MCP server, a proxy, or a credential.
- It does not fail a workflow because an MCP is missing. It reports the limitation.

## Where Client-Specific Steps Live

| Client | Page |
| --- | --- |
| Claude Code | [claude-code.md](mcp-clients/claude-code.md) |
| GitHub Copilot CLI | [github-copilot.md](mcp-clients/github-copilot.md) |

Behavior there is marked **Tested**, **Documented** or **Not tested**. Nothing on those pages is part of Agent Plugins 1.0.0, and clients not listed are not covered.
