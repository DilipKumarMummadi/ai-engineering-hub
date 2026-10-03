# Architecture

This document describes the intended architecture of the AI Engineering Hub. Nothing described here is implemented yet; this is the design the repository will grow into.

## Building Blocks

### Skill
A reusable capability that teaches the AI how to perform a specific engineering task (for example, `code-review` or `unit-test-generation`).

### Agent
A role-oriented AI worker that combines skills, rules, and tools to perform a broader engineering responsibility (for example, a Test Engineer).

### Command
A developer-facing entry point that invokes a specific capability.

### Workflow
A multi-step engineering process that combines multiple capabilities (for example, feature development from design to pull request).

### Rule
A constraint or engineering standard that should be followed.

### Template
A reusable structure for producing engineering artifacts such as design docs, ADRs, or test plans.

### Eval
A test case used to measure and validate AI behavior.

## How They Relate

```
Command ──invokes──▶ Skill / Agent / Workflow
Workflow ──orchestrates──▶ Agents + Skills
Agent ──combines──▶ Skills + Rules + Tools
Skill ──produces──▶ Artifacts (via Templates)
Eval ──validates──▶ Skills, Agents, Workflows
```

## Platform Mapping

Each platform keeps its configuration in its native location:

| Concern | Claude Code | GitHub Copilot | Tool-neutral |
| --- | --- | --- | --- |
| Skills | `.claude/skills/` | `.github/skills/` | `.agents/skills/` |
| Agents | `.claude/agents/` | `.github/agents/` | |
| Commands / Prompts | `.claude/commands/` | `.github/prompts/` | |
| Rules / Instructions | | `.github/instructions/` | |

Shared assets live at the top level: `templates/`, `evals/`, `scripts/`, `docs/`.

## Principles

- Reuse capabilities instead of duplicating prompts.
- Keep platform-specific configuration in native directories.
- Avoid duplicating logic across platforms where practical.
- Every important capability is documented and evaluated.
- Directories for skills, agents, and workflows use lowercase kebab-case (for example `code-review`, `playwright-debugging`).
