# Agents

This document describes the future agent architecture. No agents exist yet.

## Concept

An agent is a role-oriented AI worker. It combines skills, rules, and tools to take on a broader engineering responsibility than a single skill covers. Agents reuse skills rather than duplicating their instructions.

## Intended Roles

Agents will eventually represent engineering roles such as:

- Software Architect
- Backend Engineer
- Frontend Engineer
- Test Engineer
- Debugging Engineer
- DevOps Engineer
- Security Engineer
- Database Engineer

These are planned roles only and have not been created.

## Location

Agents will live in the platform-native directories: `.claude/agents/` for Claude Code and `.github/agents/` for GitHub Copilot.

## Naming

Use lowercase kebab-case, for example `software-architect` or `test-engineer`.

## Agents and External Capabilities

Agents depend on capabilities such as `source-control`, not on particular MCP servers. For example, `pr-intelligence-agent` retrieves a pull request named by `/review-pr` through the `source-control` capability, which a connected provider such as the GitHub MCP supplies, and then applies the Hub's skills to the result. It never handles credentials, never assumes a provider is connected, and reports what it could not obtain. Other capabilities: `requirements-tracking` (pr-intelligence-agent and requirement-driven workflows), `database` (database-troubleshooting-agent, bug-investigation-agent, api-development-agent where persistence matters, production-incident-agent), `browser-automation` (test-planning-agent, bug-investigation-agent for UI issues) and `cloud-platform` (architecture-agent, production-incident-agent). Flow: User → Command/Workflow → Agent → Skill → Capability → Existing MCP provider → External system. See the [MCP Capability Registry](mcp-capability-registry.md).
