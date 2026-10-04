# Changelog

## Unreleased

### Added
- `/context generate | inspect | drift`: a tool command (Claude `.claude/commands/context.md`, Copilot `.github/prompts/context.prompt.md`) that runs the existing Project Context Generator and drift detector on the current repository. Exposed by the Claude Code plugin manifest. The validator allows it as the one tool command. Documentation updates, fixture tests (`scripts/project-context/tests/test_context_command.py`) and evaluation cases (`evals/project-context-command/`). No new generator and no `ai-hub` executable.
- MCP runtime configuration model: `docs/mcp-registry.md`, `docs/mcp-runtime-configuration.md`, `docs/mcp-clients/` (Claude Code, GitHub Copilot CLI). `mcp.json` is static definitions only (now also Grafana, write-disabled); `env` and `headers` are rejected by the validator. Earlier plugin MCP configuration: root `mcp.json` (Agent Plugins 1.0.0 schema) connecting existing GitHub (read-only), Atlassian (Jira/Confluence), Figma, Postgres (read-only) and Playwright servers, with pinned package versions, `.claude-plugin/plugin.json` to bridge it to Claude Code, `docs/mcp-setup.md`, a Claude Code `userConfig` prompt for the GitHub token, and validator checks that reject literal credentials. No server code and no credentials are shipped.
- MCP integration strategy (`docs/mcp-integration-strategy.md`): the Hub consumes existing MCP servers for external access and keeps all engineering reasoning. Usage rules, capability mapping, an "External tools (optional)" note in each agent's Tool Usage and an "External sources (optional)" note in each workflow (both platforms), architecture and plugin documentation updates, and evaluation cases (`evals/mcp-integration/`). No MCP server, tools or `mcp.json` were added.
- Agent Plugin packaging (Agent Plugins 1.0.0): `plugin.json`, portable `skills/` (13 skills), `com.github.copilot/` namespace note, the plugin `README.md`, `docs/plugin-architecture.md`, a plugin validator with tests (`scripts/validate-plugin/`) and evaluation cases (`evals/plugin-packaging/`). Additive; no MCP.
- PR Intelligence: `pr-intelligence-agent`, the `/pr-intelligence` command, the `pr-intelligence` workflow, the PR Intelligence Specification (`docs/pr-intelligence-specification.md`) and evaluation cases (`evals/pr-intelligence/`). It orchestrates change intelligence, code review and only the relevant supporting analyses, and reports Ready, Needs Changes or Needs Information. It recommends only; it never approves or merges.
- Change Intelligence: the `change-intelligence` skill, `change-intelligence-agent`, the `/change-impact` command, the Change Intelligence Specification (`docs/change-intelligence-specification.md`) and evaluation cases (`evals/change-intelligence/`). Analysis only.
- Change Intelligence is used inside existing workflow stages where a change spans several areas: pr-preparation (stage 1), feature-development (stage 4), api-change (stage 4), database-change (stage 5) and bug-fix (stage 6). No stage was added or renumbered.
- Project Context Consumption standard (`docs/project-context-consumption.md`): how agents and workflows discover, validate and use `PROJECT-CONTEXT.md`
- A Project Context section in all seven agents and all seven workflows, on both platforms. It lists only the relevant topics and references the standard. Agent behavior changes: agents now check for a context, validate claims against repository evidence and report material conflicts. Behavior without a context is unchanged.
- Agent Specification section 4A and Workflow Specification section 3A, and a Project Context section in the required agent and workflow structure
- Context-aware agent evaluation cases (`evals/integration/context-aware-agents/`)
- Initial AI Engineering Hub repository structure
- Claude Code integration directories
- GitHub Copilot integration directories
- Architecture documentation
- Contribution guidelines
