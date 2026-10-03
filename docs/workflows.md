# Workflows

A workflow is a repeatable, multi-stage engineering process that coordinates commands, agents and skills to reach an outcome. Workflows sit on top of the existing layers and do not replace them. The canonical structure is in the [Workflow Specification](workflow-specification.md). The implemented workflows are in the [Workflow Registry](workflow-registry.md).

## The Layers

```
Skill
  ↓
Agent
  ↓
Command
  ↓
Workflow
```

| Layer | What it is | Example |
| --- | --- | --- |
| **Skill** | A focused engineering capability | `debugging` |
| **Agent** | An orchestrator for one engineering responsibility | `bug-investigation-agent` |
| **Command** | A user-facing entry point to an agent | `/debug` |
| **Workflow** | A multi-stage process for one outcome | `bug-fix` |

When a workflow runs, control flows down:

```
Workflow
    ↓
Command
    ↓
Agent
    ↓
Skill
    ↓
Validation
```

A workflow may call an agent directly when no command fits the stage. Commands may also be entry points into workflows where appropriate. Today, workflows are started by name, for example "run the bug-fix workflow". A future command may start a workflow. Existing commands such as `/review` and `/incident` still route to a single agent.

## Workflows vs Agents

An agent solves one responsibility by choosing skills. A workflow delivers one outcome by choosing agents and stages. The agent owns the engineering reasoning. The workflow owns order, dependencies, decision points, validation gates and handoffs.

Workflows do not duplicate agent or skill instructions. They name the capability, state what the stage needs and must produce, and link to the definition.

## How Workflows Compose Agents

```
Feature Development Workflow
    ↓
Architecture Agent
    ↓
API Development Agent
    ↓
Test Planning Agent
    ↓
PR Review Agent
```

Each stage receives the user's request, the constraints, and the results of the earlier stages it depends on. It produces a result the next stage can use. A stage that is irrelevant is skipped and the reason is recorded. The user's constraints are passed to every agent unchanged.

## How Workflows Use Skills

Workflows apply skills mostly **through their agents**. A workflow names a skill directly only when a stage needs it and no agent covers it, for example applying `security` to a trust-boundary change or `playwright` to locator choice. A workflow lists only the skills its stages call for and does not run skills for completeness.

## Available Workflows

| Workflow | Outcome |
| --- | --- |
| [feature-development](../.claude/workflows/feature-development.md) | A new feature, validated and ready for PR |
| [bug-fix](../.claude/workflows/bug-fix.md) | A defect fixed on a confirmed root cause, with a regression test |
| [api-change](../.claude/workflows/api-change.md) | A new or changed API with a compatibility decision |
| [database-change](../.claude/workflows/database-change.md) | A schema, data or query change with a rollback plan |
| [pr-preparation](../.claude/workflows/pr-preparation.md) | A finished change prepared for PR |
| [e2e-test-creation](../.claude/workflows/e2e-test-creation.md) | A reliable browser test, or a recommended lower-level test |
| [production-incident](../.claude/workflows/production-incident.md) | A stabilized, explained and followed-up incident |

## When to Use a Workflow

Use a workflow when the outcome needs several responsibilities in sequence, when order and gates matter, or when the process repeats.

Do not use one when a single agent or command is enough. "Why is this failing?" is `/debug`. "Review this PR" is `/review`. A workflow adds coordination, and it should earn it. If a workflow would run every stage for a small change, use a narrower path.

## Workflow Lifecycle

Every stage follows the same lifecycle:

```
Input → Context → Action → Result → Validation → Decision → Next Stage
```

A stage ends as **Completed**, **Skipped**, **Blocked** or **Failed**. The decision step chooses the next stage, which may be a later stage, an earlier one, another workflow, or a stop to ask the user. See the specification for details.

## Safety Boundaries

Workflows separate four kinds of activity:

| Kind | Meaning |
| --- | --- |
| **Analysis** | Reading and investigating. Read-only. |
| **Planning** | Proposing changes. Nothing changes. |
| **Modification** | Editing files in the working tree. Requires the user's request. |
| **Execution** | Running something that affects a system beyond the working tree. Requires explicit, specific authorization. |

Analysis or planning is not authorization to modify systems. Starting a workflow does not authorize the actions inside it. Destructive or hard-to-reverse actions, including database changes and migrations, production changes, deleting files, infrastructure changes, deployments and security-sensitive operations, need explicit authorization each time.

## Validation

A workflow defines stage validation, final validation, evidence requirements, test requirements where they apply, and rollback considerations where the outcome is hard to undo.

A workflow is never reported as completed unless its required stages actually completed. Tests, builds and migrations are not reported as passing unless they ran and the output was seen. Skipped, blocked and failed stages are reported as such.

## Location

| Platform | Location |
| --- | --- |
| Claude Code | `.claude/workflows/` |
| GitHub Copilot | `.github/workflows/` |

The `.github/workflows/` files are Markdown process definitions, not GitHub Actions. GitHub Actions reads only `.yml` and `.yaml` files there, so these definitions do not run as Actions.

## Evaluation

Workflow evaluations are in [`evals/workflows/`](../evals/workflows/README.md). They test orchestration: ordering, agent and skill selection, skipping, context preservation, decision points, safety, validation and handoffs. Agent reasoning is tested by the [agent evaluations](../evals/agents/README.md).

## Naming

Use lowercase kebab-case that names the outcome, for example `feature-development` or `bug-fix`.
