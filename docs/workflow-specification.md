# Workflow Specification

This specification defines the canonical structure, design principles and quality bar for AI Engineering Hub workflows. For an overview of what workflows are, see [Workflows](workflows.md). The implemented workflows are listed in the [Workflow Registry](workflow-registry.md).

A workflow is written for the AI that executes it and for the engineer who maintains it. It must be short enough to read in one sitting and specific enough to be evaluated.

## 1. Definitions

| Layer | Definition |
| --- | --- |
| **Skill** | A focused engineering capability, such as debugging, code review or SQL. See the [Skill Specification](skill-specification.md). |
| **Agent** | An orchestrator that solves one specific engineering responsibility by selecting and combining skills. See the [Agent Specification](agent-specification.md). |
| **Command** | A user-facing entry point that hands a request to an agent, or to a workflow. See [Commands](commands.md). |
| **Workflow** | A repeatable, multi-stage engineering process that coordinates commands, agents and skills to reach an outcome. |

```
Skill  →  Agent  →  Command  →  Workflow
(capability) (responsibility) (entry point) (process)
```

Execution flows the other way:

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

A workflow may invoke an agent directly when no command fits the stage. Commands remain the preferred entry point when one exists, because they preserve the user's request and safety limits.

### Workflow vs Agent

| | Agent | Workflow |
| --- | --- | --- |
| Scope | One engineering responsibility | One engineering outcome spanning several responsibilities |
| Owns | Skill selection and reasoning | Stage order, dependencies, decision points, handoffs |
| Decides | Which skills and analysis the task needs | Which stages and agents the outcome needs |
| Output | An analysis, review, design or plan | A validated outcome, built from stage results |
| Evaluated on | Reasoning and skill orchestration | Orchestration: ordering, selection, skipping, handoffs, safety |

A workflow does not reason about the engineering content itself. It decides *who* reasons about it, *when*, with *what context*, and *what must be true* before moving on.

Example:

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

### The no-duplication rule

A workflow must **not** restate the instructions, decision rules, checklists or output formats of an agent or skill. It names the capability, states what the stage needs and what it must produce, and links to the definition. If a workflow stage needs behavior an agent does not have, the fix is to improve the agent, not to embed the behavior in the workflow.

A workflow may add only what belongs to orchestration:

- the order and dependencies of stages
- conditions for running or skipping a stage
- what context is carried from one stage to the next
- gates: validation, authorization and decision points
- handoffs between agents

## 2. Design Principles

Workflows must:

- **Be outcome-oriented.** State the outcome the workflow reaches, not a list of activities.
- **Have explicit stages,** each with a clear purpose and a result the next stage can use.
- **Define dependencies.** State which stages need which earlier results.
- **Identify decision points.** Say what evidence selects a path.
- **Define validation.** Each stage and the whole workflow have checks that must hold.
- **Define handoffs.** Say what is passed when the work moves to another agent, workflow or person.
- **Preserve user constraints.** Scope limits, technology choices, deadlines and prohibitions apply to every stage, and are passed to every agent unchanged.
- **Avoid unnecessary steps.** A stage that does not help the outcome is skipped.
- **Allow stages to be skipped** when irrelevant, and record that they were skipped and why.
- **Identify missing information** instead of guessing, and continue with what can be done safely.
- **Avoid fabricating results.** Do not report a stage, test, command or check as done unless it was done.

A workflow must not blindly execute every available skill or agent. The stage table is a menu of possible stages, filtered by the task.

## 3. Stage Model

Every stage follows the same lifecycle:

```
Input
  ↓
Context
  ↓
Action
  ↓
Result
  ↓
Validation
  ↓
Decision
  ↓
Next Stage
```

| Step | Meaning |
| --- | --- |
| **Input** | What the stage receives: the user's request plus results from earlier stages. |
| **Context** | What else must be known or gathered. Missing context is identified here. |
| **Action** | The work: an agent or command is invoked, or a skill is applied. |
| **Result** | A clear output, labeled by evidence (observed, assumed, hypothesis, confirmed) where that matters. |
| **Validation** | A check that the result is sufficient and supported. |
| **Decision** | Proceed, skip ahead, go back, stop and ask, or hand off. |
| **Next Stage** | The next stage that applies, given the decision. |

Each stage must produce a clear output that the next stage can consume. A stage that produces nothing the next stage uses is a candidate for removal.

A stage can end in one of these states, and the workflow must say which it is:

| State | Meaning |
| --- | --- |
| **Completed** | The action ran and validation passed. |
| **Skipped** | Not relevant. The reason is recorded. |
| **Blocked** | Needs missing information or authorization. The need is stated. |
| **Failed** | The action ran and validation did not pass. The failure is stated. |

## 3A. Project Context

A workflow may use the repository's `PROJECT-CONTEXT.md` to understand the architecture, technology stack, testing approach, deployment model, database, API conventions, repository structure and operational constraints. The rules are in [Project Context Consumption](project-context-consumption.md). For workflows:

- **Consume where it matters.** The workflow's Project Context section names the stages that benefit and the topics they need. It does not add a context-loading stage, and does not load context at every stage. The agent performing a stage loads what that stage needs, and later stages reuse it.
- **Do not assume it is current.** Repository evidence takes precedence for current-state claims. Stale or conflicting context is reported when it affects the outcome. Missing context never blocks a workflow.
- **Stay outcome-oriented.** Context informs stages. It does not change the stage order, skip conditions or authorization gates. A context statement is not a validation result.
- **No project knowledge in the workflow.** Workflows stay generic. Project-specific facts live only in the project's context.
- **Safety.** Secrets in a context are never reproduced, and the context never authorizes a modification or execution step.

Example flows:

```
Feature:  Requirement → Project Context → Existing System → Architecture → Implementation → Testing → Review
Bug fix:  Symptom → Project Context → Repository Evidence → Investigation → Root Cause → Fix → Regression
```

## 4. Decision Points

Workflows support conditional paths. A decision point names the evidence and the path it selects.

| If | Then |
| --- | --- |
| The change alters an API | Run the API Development Agent |
| The change alters a database schema or query | Run the Database Troubleshooting Agent |
| Browser behavior changes | Test Planning Agent with the `playwright` skill |
| The change is security-sensitive | Apply the `security` skill |
| The change is a small, local edit | Skip architecture assessment |

Rules:

- A decision point is based on the task or the evidence, not on a default.
- Do not require irrelevant stages. When the condition is false, the stage is skipped.
- When the condition cannot be judged, treat the stage as **Blocked** and ask, or state the assumption.
- Decision points may route to another workflow. Say so, and pass the context.

## 5. Safety

Workflows separate four kinds of activity:

| Kind | Meaning | Default |
| --- | --- | --- |
| **Analysis** | Reading code, logs, data, diffs, plans. Read-only. | Allowed |
| **Planning** | Proposing changes, designs, migrations, rollbacks. No change is made. | Allowed |
| **Modification** | Editing files or configuration in the working tree. | Requires the user's request for the change |
| **Execution** | Running something that affects a system beyond the working tree: migrations, deployments, production commands, data changes, infrastructure. | Requires explicit, specific authorization |

Rules:

- **Analysis or planning is not authorization to modify systems.** A finished plan does not permit implementing the plan.
- Starting a workflow is not authorization for the actions inside it.
- Authorization is specific. Approval for one action does not extend to another, to a different environment, or to a later run.
- Potentially destructive or hard-to-reverse actions require explicit authorization before they run, with the effect, the risk and the way to undo it stated. These include:
  - database changes and migrations
  - production changes
  - deleting files
  - infrastructure changes
  - deployments
  - security-sensitive operations (credential, permission, key or policy changes)
- Prefer reversible actions, and define rollback before an irreversible action is proposed.
- Never expose secrets or personal data found during a stage. Refer to them by location.
- Stop and ask when a safe path is unclear.

Each workflow's `Safety` section states which stages are Analysis, Planning, Modification or Execution, and where authorization gates are.

## 6. Validation

Every workflow defines:

- **Stage validation.** What must be true before a stage counts as completed.
- **Final validation.** What must be true before the workflow counts as completed.
- **Evidence requirements.** What counts as evidence for the claims the workflow makes (test output, logs, query results, diffs).
- **Test requirements,** where the outcome changes behavior.
- **Rollback considerations,** where the outcome is hard to undo.

Rules:

- Never claim a workflow completed successfully unless its required stages actually completed.
- Never report tests, builds, migrations or checks as passing unless they ran and the output was seen. If something was not run, say "not run" and give the command.
- A skipped stage is not a completed stage. Report both honestly.
- A final report lists: stages completed, stages skipped and why, stages blocked or failed, what was validated and how, and what remains open.

## 7. Workflow Structure

Workflows are Markdown files with a YAML header and these sections, in this order.

```markdown
---
name: <workflow-name>
description: <short description>
---

# <Workflow Name>

## Purpose
## When to Use
## When NOT to Use
## Inputs
## Project Context
## Stages
## Commands
## Agents
## Skills
## Decision Points
## Validation
## Safety
## Output
## Handoff
## Examples
## Related Workflows
```

### Header

| Field | Rules |
| --- | --- |
| `name` | Lowercase kebab-case, equal to the file name without `.md`. |
| `description` | One or two sentences: what outcome the workflow reaches and when to use it. Include a "not for" clause when confusion with another workflow is likely. |

### Sections

| Section | Content |
| --- | --- |
| **Purpose** | The outcome, in a short paragraph. States that the workflow orchestrates existing capabilities. |
| **When to Use** | Situations that call for the workflow. |
| **When NOT to Use** | Situations that call for a single agent or command, or a different workflow. |
| **Inputs** | What the workflow needs, split into required, preferred and optional. States that missing inputs are identified, not invented. |
| **Project Context** | Where project context helps, by stage and topic, with a short flow. References [Project Context Consumption](project-context-consumption.md). Adds no stage. |
| **Stages** | A table: number, stage, needs (dependencies), performed by, produces, and when it may be skipped. A short note states that the stages follow the lifecycle in section 3. |
| **Commands** | The commands that serve as entry points for stages, with the stage they serve. |
| **Agents** | The primary and supporting agents, with the stage and the condition under which each is used. |
| **Skills** | Skills the workflow applies directly, or expects through its agents. Does not list a skill the workflow never calls for. |
| **Decision Points** | Conditions and the paths they select, including which stages are skipped. |
| **Validation** | Stage, final and evidence requirements, tests, and rollback considerations. |
| **Safety** | Stages by Analysis, Planning, Modification and Execution; authorization gates; prohibitions. |
| **Output** | The final report or artifacts, with the completion statement rules. |
| **Handoff** | Where work goes after the workflow, and what is passed. |
| **Examples** | One or two short examples showing stage selection and skipping. |
| **Related Workflows** | Neighboring workflows and when work moves between them. |

### Stage table

```markdown
| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Understand Requirement | | Workflow (asks the user) | Stated outcome, constraints, open questions | Never |
| 2 | Analyze Existing System | 1 | `architecture-agent` | Current-state summary | Greenfield or trivial change |
```

- *Needs* lists stage numbers whose results are required. A stage with no needs may start immediately.
- *Performed by* names a command, an agent or a skill, and links to it in the sections below. Use "Workflow" only for orchestration steps such as asking a question or recording a decision.
- *Produces* names the result, not the activity.
- *Skip when* states a condition. "Never" is allowed for stages that are always needed.

## 8. Platform Locations

Each workflow has two equivalent definitions:

| Platform | Location |
| --- | --- |
| Claude Code | `.claude/workflows/<name>.md` |
| GitHub Copilot | `.github/workflows/<name>.md` |

The two copies carry the same stages, decision points and safety rules. They differ only in the platform-specific links to agents, skills and commands.

> **Not GitHub Actions.** Workflow definitions here are AI engineering processes, not CI/CD. GitHub Actions reads only `.yml` and `.yaml` files in `.github/workflows/`. The Markdown definitions do not run as Actions and must not be renamed to YAML. Do not add Actions files for these workflows.

## 9. Relationship to Commands

Commands remain unchanged. Each command still routes to one agent. A workflow uses commands as the entry points for its stages where a command fits, for example `/architecture` for an architecture assessment stage or `/review` for a review stage.

A future command may start a workflow as a whole. Until then, a workflow is started by asking for it by name, for example "run the bug-fix workflow". A command must not duplicate a workflow's stages.

## 10. Quality Checklist

A workflow is ready when:

- [ ] The header has `name` and `description`, and `name` matches the file name.
- [ ] All sections are present and in order.
- [ ] A Project Context section says where context helps, and adds no stage.
- [ ] Every stage has dependencies, an owner, a result and a skip condition.
- [ ] Every agent and skill it references exists in the [Agent Registry](agent-registry.md) or [skills](skills.md).
- [ ] No agent or skill instructions are restated.
- [ ] Decision points exist, and at least one stage can be skipped.
- [ ] Safety separates analysis, planning, modification and execution.
- [ ] Destructive actions require explicit authorization.
- [ ] Validation includes stage, final and evidence requirements.
- [ ] The output never permits claiming success without completed stages.
- [ ] The handoff says what is passed on.
- [ ] Both platform copies match.
- [ ] Evaluation cases exist under `evals/workflows/<name>/`.

## 11. Evaluation

Workflow evaluations test **orchestration**, not the reasoning inside agents. They check stage ordering, agent and skill selection, skipping, context preservation, decision points, safety, validation and handoffs. Agent evaluations in [`evals/agents/`](../evals/agents/README.md) remain the place for agent reasoning, and workflow cases must not repeat them. See the [Workflow Evaluations](../evals/workflows/README.md).

## 12. Naming

Use lowercase kebab-case that names the outcome: `feature-development`, `bug-fix`, `production-incident`.
