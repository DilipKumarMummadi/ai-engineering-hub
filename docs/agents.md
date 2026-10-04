# Agents

This document describes the agent architecture and lists the agents that exist today.

## Concept

An agent is a role-oriented AI worker. It combines skills, rules, and tools to take on a broader engineering responsibility than a single skill covers. Agents reuse skills rather than duplicating their instructions.

## Existing Agents

Ten agents exist. See the [Agent Registry](agent-registry.md) for status and details.

| Agent | Purpose |
| --- | --- |
| `requirement-intelligence-agent` | Retrieve, refine and assess the readiness of a requirement before implementation |
| `pr-review-agent` | Review a pull request or proposed change as a whole |
| `pr-intelligence-agent` | Assess whether a change is ready for review or merge |
| `bug-investigation-agent` | Reach an evidence-supported root cause for unexpected behavior |
| `change-intelligence-agent` | Report the engineering impact of a change |
| `test-planning-agent` | Produce a test strategy and test plan |
| `api-development-agent` | Design, implement, review and evolve APIs |
| `architecture-agent` | Analyze and design software architecture |
| `database-troubleshooting-agent` | Diagnose database problems and propose safe remediation |
| `production-incident-agent` | Investigate and stabilize production incidents |

Roles such as Backend Engineer, Frontend Engineer, DevOps Engineer and Test Engineer are not separate agents; their concerns are covered by the agents above and by the skills they use.

## Location

Agents live in the platform-native directories: `.claude/agents/` for Claude Code and `.github/agents/` for GitHub Copilot.

## Naming

Use lowercase kebab-case, with an `-agent` suffix, for example `pr-review-agent` or `test-planning-agent`.

## Agents and External Capabilities

Agents depend on capabilities such as `source-control`, not on particular MCP servers. For example, `pr-intelligence-agent` retrieves a pull request named by `/review-pr` through the `source-control` capability, which a connected provider such as the GitHub MCP supplies, and then applies the Hub's skills to the result. It never handles credentials, never assumes a provider is connected, and reports what it could not obtain. Other capabilities: `requirements-tracking` (pr-intelligence-agent and requirement-driven workflows), `database` (database-troubleshooting-agent, bug-investigation-agent, api-development-agent where persistence matters, production-incident-agent), `browser-automation` (test-planning-agent, bug-investigation-agent for UI issues) and `cloud-platform` (architecture-agent, production-incident-agent). Flow: User → Command/Workflow → Agent → Skill → Capability → Existing MCP provider → External system. See the [MCP Capability Registry](mcp-capability-registry.md).
