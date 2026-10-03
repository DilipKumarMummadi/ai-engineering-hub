# AI Engineering Hub

A centralized repository of reusable AI engineering capabilities for software engineers.

> **Status:** Foundation only. This version establishes the repository structure and documents the intended architecture. No skills, agents, commands, or workflows exist yet. They will be added incrementally.

## Purpose

The hub will eventually provide:

- **AI Skills**: reusable capabilities for specific engineering tasks
- **AI Agents**: role-based AI workers
- **Commands**: developer-facing entry points
- **Engineering Workflows**: multi-step engineering processes
- **Engineering Rules**: standards and constraints
- **Templates**: reusable engineering artifacts
- **Evaluations**: quality and regression tests for AI capabilities
- **Tool/MCP integrations**

It is intended to support:

- Claude Code
- GitHub Copilot
- Future AI coding tools where practical

## Core Philosophy

| Concept | Meaning |
| --- | --- |
| **Skills** | Reusable capabilities |
| **Agents** | Role-based AI workers |
| **Commands** | Developer-facing entry points |
| **Workflows** | Multi-step engineering processes |
| **Rules** | Engineering standards and constraints |
| **Templates** | Reusable engineering artifacts |
| **Evals** | Quality and regression testing for AI capabilities |

See [docs/architecture.md](docs/architecture.md) for details.

## Architecture

```
AI Engineering Hub
        |
        +-- Skills
        |
        +-- Agents
        |
        +-- Commands
        |
        +-- Workflows
        |
        +-- Rules
        |
        +-- Templates
        |
        +-- Evals
        |
        +-- Tool Integrations
        |
        +-- Claude Code
        |
        +-- GitHub Copilot
```

## Repository Layout

```
ai-engineering-hub/
├── .claude/        # Claude Code native config (skills, agents, commands)
├── .github/        # GitHub Copilot native config (skills, agents, instructions, prompts)
├── .agents/        # Tool-neutral skills location
├── docs/           # Architecture and design documentation
├── templates/      # Reusable engineering artifact templates
├── evals/          # Evaluations for AI capabilities
├── scripts/        # Tooling and automation
├── README.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```

Platform-specific configuration lives in each platform's native directory. Empty directories are preserved with `.gitkeep` files.

## Documentation

- [Architecture](docs/architecture.md)
- [Skills](docs/skills.md)
- [Agents](docs/agents.md)
- [Workflows](docs/workflows.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Roadmap

The repository is built incrementally. The current version only establishes the foundation; capabilities will be added one at a time, each documented and evaluated.
