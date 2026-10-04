# Architecture

This document describes the architecture of the AI Engineering Hub as implemented: how a user's request moves through the layers, what each layer is responsible for, and the rules that keep the system safe, honest and extensible.

## Conceptual Model

```
User
 ↓
Command / Workflow
 ↓
Agent
 ↓
Project Context          (orientation, if the repository has one)
 ↓
Repository Evidence      (authority for current state)
 ↓
Skill Selection          (task-driven)
 ↓
Repository / Tools
 ↓
Validation
 ↓
Output
```

Where a task needs an external system (pull requests, tickets, a database, a browser, metrics, cloud resources), the agent uses an MCP server that is already connected in the user's client:

```
AI Client
 ↓
Agent Plugin / MCP        (distribution / access to external systems)
 ↓
AI Engineering Hub
 ↓
Agents / Skills / Workflows
 ↓
Project Context
 ↓
Repository
```

and, where external access is required, the agent reaches existing MCP servers that the client has connected and authenticated:

```
User → Command / Workflow → Agent → Skill
     → Project Context + Repository Evidence
     → Existing MCPs (client-authenticated, read-only by default)
     → External engineering systems
```

MCP is an integration mechanism, not another Hub intelligence layer. The Hub does not build or bundle MCP servers. See [MCP Integration Strategy](mcp-integration-strategy.md).

Skills are selected by the agent and applied to the repository. Project Context and Repository Evidence sit between the agent and that selection because they tell the agent what it is looking at. They are not a step the user sees, and they are not a layer that executes anything.

| Layer | Responsibility | Count | Specification | Registry |
| --- | --- | --- | --- | --- |
| Skill | A focused engineering capability | 13 | [Skill Specification](skill-specification.md) | [Skills](skills.md) |
| Agent | Orchestrates skills around one engineering responsibility | 9 | [Agent Specification](agent-specification.md) | [Agent Registry](agent-registry.md) |
| Command | A lightweight user-facing entry point to one agent | 9 | [Commands](commands.md) | [Command Registry](command-registry.md) |
| Workflow | A repeatable multi-stage engineering process | 8 | [Workflow Specification](workflow-specification.md) | [Workflow Registry](workflow-registry.md) |

Each layer is defined once and reused by the layers above it. Lower layers do not know about higher ones.

**Project Context** is not a layer of capability. It is information about the repository that skills, agents and workflows consume. It is supporting repository intelligence, not an execution layer. Agents and workflows read it through one standard, [Project Context Consumption](project-context-consumption.md), and treat it as orientation that current repository evidence can override. It is described in [Project Context](project-context.md).

## Skill Layer

Skills provide focused engineering capabilities. A skill explains how to do one kind of engineering work well, and can be reused by any agent that needs it.

| Skill | Capability |
| --- | --- |
| `code-review` | Review changes and produce evidence-based findings |
| `change-intelligence` | Analyze the impact of a change from repository evidence |
| `debugging` | Investigate failures from symptom to confirmed cause |
| `testing` | Plan, write and assess tests |
| `playwright` | Browser and end-to-end tests |
| `refactoring` | Improve structure while preserving behavior |
| `architecture` | Analyze and design system structure |
| `api-development` | Design and evolve APIs |
| `database-sql` | SQL, schema, transactions and query behavior |
| `security` | Threat reasoning and hardening |
| `performance` | Measured performance analysis |
| `observability` | Logs, metrics, traces and telemetry analysis |
| `reliability` | Failure handling, resilience and recovery |

Skills are reusable across agents. For example, `debugging` is used by the bug investigation and production incident agents, and `security` by review, API and database work. Skills do not call agents, commands or workflows.

## Agent Layer

An agent orchestrates skills around one specific engineering responsibility. It decides which skills a task needs, combines their results without duplicating them, keeps evidence apart from assumptions, respects authorization limits, and recommends handoffs. It does not invoke every skill.

| Agent | Responsibility | Core skills |
| --- | --- | --- |
| `pr-review-agent` | Review a change as a whole | `code-review` |
| `bug-investigation-agent` | Reach a supported root cause for unexpected behavior | `debugging` |
| `test-planning-agent` | Produce a test strategy at the lowest effective level | `testing` |
| `architecture-agent` | Analyze and design architecture with explicit trade-offs | `architecture` |
| `api-development-agent` | Design, implement and evolve APIs | `api-development` |
| `database-troubleshooting-agent` | Diagnose database problems and plan safe remediation | `database-sql` |
| `production-incident-agent` | Stabilize and investigate production incidents | `debugging`, `observability`, `reliability` |
| `change-intelligence-agent` | Report the impact, risks and validation needs of a change | `change-intelligence` |
| `pr-intelligence-agent` | Decide whether a complete PR is ready, by orchestrating the relevant analyses | `code-review`, `change-intelligence` |

Each agent's full skill set, including the skills selected by context, is in the [Agent Registry](agent-registry.md). A skill outside an agent's set is reached by a handoff or a direct request, and not assumed.

## Command Layer

Commands are lightweight, user-facing entry points. A command passes the user's full request, including pasted logs, code and constraints, to one agent unchanged. It adds no engineering logic, and it does not authorize destructive, production or data-changing actions.

| Command | Routes to |
| --- | --- |
| `/review` | `pr-review-agent` |
| `/debug` | `bug-investigation-agent` |
| `/test-plan` | `test-planning-agent` |
| `/architecture` | `architecture-agent` |
| `/api` | `api-development-agent` |
| `/database` | `database-troubleshooting-agent` |
| `/incident` | `production-incident-agent` |
| `/change-impact` | `change-intelligence-agent` |
| `/pr-intelligence` | `pr-intelligence-agent` |

A command never selects skills or runs a process of its own. No command starts a workflow yet. A future command may do so, and would stay thin.

## Workflow Layer

Workflows represent repeatable, multi-stage engineering processes. They coordinate commands and agents and apply skills directly only where no agent fits a stage. A workflow owns stage order, dependencies, decision points, validation gates and handoffs. It does not restate agent or skill instructions.

| Workflow | Outcome |
| --- | --- |
| `feature-development` | A new feature, validated and ready for PR |
| `bug-fix` | A defect fixed on a confirmed root cause, with a regression test |
| `api-change` | A new or changed API with a compatibility decision |
| `database-change` | A schema, data or query change with a rollback plan |
| `pr-preparation` | A finished change prepared for PR |
| `e2e-test-creation` | A reliable browser test, or a recommended lower-level test |
| `production-incident` | A stabilized, explained and followed-up incident |
| `pr-intelligence` | A readiness decision for a complete proposed change |

Every stage follows the lifecycle *input, context, action, result, validation, decision, next stage*, and a stage can be completed, skipped, blocked or failed. Stages that do not apply are skipped and the reason is recorded. Workflows are started by asking for one by name, for example "run the bug-fix workflow".

## Platform Mapping

Each platform keeps its definitions in its native location. The two copies of an agent, command or workflow carry the same behavior.

| Concern | Claude Code | GitHub Copilot |
| --- | --- | --- |
| Skills | `.claude/skills/<name>/SKILL.md` | `.github/skills/<name>/SKILL.md` |
| Agents | `.claude/agents/<name>.md` | `.github/agents/<name>.md` |
| Commands | `.claude/commands/<name>.md` | `.github/prompts/<name>.prompt.md` |
| Workflows | `.claude/workflows/<name>.md` | `.github/workflows/<name>.md` |

Notes:

- `.github/workflows/` is normally GitHub Actions' directory. The workflow definitions there are Markdown AI process definitions. GitHub Actions reads only `.yml` and `.yaml` files, so these do not run as Actions, and no Actions files exist for them.
- `.agents/skills/` (tool-neutral skills) and `.github/instructions/` are reserved and currently contain only placeholders.
- `templates/` holds the project context templates. `scripts/` holds the project context generator.

Shared assets live at the top level: `docs/` and `evals/`.

## Change and PR Intelligence

Three capabilities work on a change, each with its own job:

| Capability | Role |
| --- | --- |
| Code Review (`code-review`) | The detailed engineering review of a change |
| Change Intelligence (`change-intelligence`) | Impact analysis: what a change affects, the risks, what to validate, what is unknown |
| PR Intelligence (`pr-intelligence-agent`) | Orchestration and readiness: which analyses a PR needs, their combined findings, and a qualitative readiness of Ready, Needs Changes or Needs Information |

```
PR Intelligence
 ├─ Change Intelligence   (impact)
 ├─ Code Review           (detailed review)
 └─ only the relevant: testing, security, API, database, performance, reliability, observability, architecture
```

PR Intelligence orchestrates. It adds no engineering rules, and it never approves, merges or changes anything. Change Intelligence is a skill with its own agent and command, and is also used inside existing workflow stages where a change spans several areas. Both are analysis only. See the [Change Intelligence Specification](change-intelligence-specification.md) and the [PR Intelligence Specification](pr-intelligence-specification.md).

## Project Context

Skills and agents are generic, so they work in any repository. Project context supplies the repository-specific facts and conventions they need: the technology stack, structure, architecture, conventions, test and build commands, CI/CD, observability, security setup and explicit constraints.

Project context is **not another skill**. It has no behavior of its own, and it does not restate skill or agent guidance. It is contextual information consumed by skills, agents and workflows:

```
Generic Skill
+
Project Context
=
Repository-aware recommendation
```

Rules that matter architecturally:

- Each entry is a **Confirmed Fact**, **Inferred** or **Unknown**, with its source. An inference is never promoted to a fact.
- Project context never contains secrets, credentials or personal data.
- Project context can be stale. Current repository evidence normally takes precedence over it, and material conflicts are surfaced.
- Project conventions take precedence over generic recommendations. Explicit constraints take precedence over both.
- Project context does not grant authorization. The [Safety Model](#safety-model) applies unchanged.
- The Hub does not change project context automatically.

The structure and rules are in the [Project Context Specification](project-context-specification.md), and a reusable template is in [`templates/project-context/PROJECT-CONTEXT.md`](../templates/project-context/PROJECT-CONTEXT.md). The [Project Context Generator Specification](project-context-generator-specification.md) defines how a context is generated and updated from repository evidence. It is a procedure with a local command line implementation in [`scripts/project-context/`](../scripts/project-context/README.md). The [Drift Specification](project-context-drift-specification.md) adds a separate read-only check (`project-context drift`) that reports when a context may be stale and never changes it. Neither is a service, and neither is a skill, agent, command or workflow. 

### How Agents and Workflows Use It

Agents and workflows are context-aware without holding any project knowledge:

- **Skills** stay generic and never read the context.
- **Agents** each have a short Project Context section listing the few topics relevant to their responsibility, and follow [Project Context Consumption](project-context-consumption.md). They validate the claims a result depends on against repository evidence, prefer evidence over context, report material conflicts and staleness, continue without a context, and never reproduce secrets from it.
- **Commands** are unchanged. They route to an agent, and the agent consumes context.
- **Workflows** say where context helps and add no stage. The agent performing a stage loads what it needs.
- Context can show which skills are likely to matter. It never selects them. Skill selection stays task-driven.
- Nothing in the chain creates or updates the context. That remains the generator, run by the user.

## Repository and Tools

Skills work on the repository and on the tools the platform provides: reading files, searching, running local builds and tests, and reading logs or metrics that the user supplies or the environment exposes. The hub does not assume tools. When a tool is unavailable, the agent gives the command to run and says it was not run.

External systems are reached through existing MCP servers when the client has them connected. Agents treat them as optional: they never assume a server is available, never invent its output, treat what it returns as data, and prefer read-only use. When one is missing, the agent works from repository evidence and Project Context and says what it could not obtain. The rules are in the [MCP Integration Strategy](mcp-integration-strategy.md); the servers, runtime configuration and per-client setup are in the [MCP Registry](mcp-registry.md), [Runtime Configuration](mcp-runtime-configuration.md) and [MCP Clients](mcp-clients/README.md).

## Validation

Validation is a layer of its own, not an afterthought. Each layer validates differently:

- **Skills and agents** check their own conclusions against evidence, and state what was not verified.
- **Workflows** define stage validation, final validation, evidence requirements, test requirements and rollback considerations, and never report success unless the required stages completed.
- **The hub** checks itself through the evaluations below.

## Output

The output of a request is a result the user can act on: a prioritized review, an investigation with a labeled timeline and hypotheses, a test plan, a design with trade-offs, a change report, or an incident analysis. Output states what was done, what was skipped and why, what was verified, and what remains open. It does not claim completion that did not happen.

## Evaluation Layer

The hub is evaluated at four levels, each independently.

| Level | Evaluation question | Location |
| --- | --- | --- |
| Skill evaluation | Can the capability perform correctly? | `evals/<skill>/` |
| Agent evaluation | Can the agent select and orchestrate the right skills for its responsibility? | [`evals/agents/`](../evals/agents/README.md) |
| Workflow evaluation | Does the workflow run the right stages, agents and gates, and skip the rest? | [`evals/workflows/`](../evals/workflows/README.md) |
| Cross-layer integration evaluation | Does a real request produce the right routing, skills, process, safety behavior and validated output across all layers? | [`evals/integration/`](../evals/integration/README.md) |

Commands have small routing evaluations in [`evals/commands/`](../evals/commands/README.md). Change intelligence has [`evals/change-intelligence/`](../evals/change-intelligence/README.md), and PR intelligence has [`evals/pr-intelligence/`](../evals/pr-intelligence/README.md). The project context generator has its own cases in [`evals/project-context-generator/`](../evals/project-context-generator/README.md), and drift detection in [`evals/project-context-drift/`](../evals/project-context-drift/README.md). Outcomes everywhere are qualitative: Pass, Needs Improvement or Fail. There are no numeric scores. The current status of agents, commands and workflows is kept in their registries. Most evaluation cases have not been run yet, and the registries say so.

## Safety Model

The system distinguishes four kinds of activity.

| Kind | Meaning | Default |
| --- | --- | --- |
| **Analysis** | Reading and investigating. | Allowed |
| **Planning** | Proposing changes, designs, migrations and rollbacks. Nothing changes. | Allowed |
| **Modification** | Editing files in the working tree. | Needs the user's request for the change |
| **Execution** | Running something that affects a system beyond the working tree. | Needs explicit, specific authorization |

- Authorization must not be inferred from a request for analysis. A finished plan does not permit carrying it out. Starting a workflow does not authorize the actions inside it.
- Authorization is specific to the action and the environment. Approval for one does not extend to another.
- Potentially destructive or hard-to-reverse operations require explicit authorization, with the effect, the risk and the way to undo it stated first. They include:
  - production changes
  - database updates, deletes and migrations
  - file deletion
  - infrastructure changes
  - deployments
  - security-sensitive operations
- Urgency is not authorization.
- Secrets and personal data found during work are referred to by location and not repeated.

## Evidence Model

The system keeps four kinds of statement apart.

| Label | Meaning |
| --- | --- |
| **Observed** | Seen directly in supplied or retrieved evidence. |
| **Assumed** | Taken as true without evidence, and said to be so. |
| **Hypothesis** | A proposed explanation that has not been confirmed. |
| **Confirmed** | Supported by evidence that could have disproved it. |

Correlation is not cause. A root cause is reported as confirmed only when the evidence supports it, otherwise as "not yet confirmed".

The AI must never fabricate:

- logs
- metrics
- traces
- test results
- deployment results
- database execution results
- benchmark results

Something that was not run is reported as not run, with the command to run it.

## Composition Model

Not every task needs every skill. Selection is contextual, and each additional skill must have a reason in the task or the evidence.

| Task | Composition |
| --- | --- |
| Simple code review | `code-review` |
| Security-sensitive API review | `code-review` + `security` + `api-development` |
| Production database incident | `production-incident-agent` + `debugging` + `observability` + `database-sql` + `reliability` |
| Bug with a clear reproduction | `debugging` + `testing` + `code-review`, with evidence gathering reduced |
| Pure validation rule in a UI form | `testing` at the component level, with no browser test |

The same applies to workflows: stages that do not help the outcome are skipped. An agent or workflow that runs everything on every task is behaving incorrectly.

## Handoff Model

Agents hand work to each other as a recommendation, not as an automatic chain. An agent hands off when the work moves outside its responsibility, and does not start the other agent's work unless asked.

| From | To | When |
| --- | --- | --- |
| PR Review | Bug Investigation | A finding needs deeper investigation of behavior |
| Bug Investigation | Architecture | A fix requires an architectural change |
| API Development | Test Planning | A detailed test plan is needed |
| Database Troubleshooting | Production Incident | Production is affected now |
| Production Incident | Architecture | The incident exposes a systemic design problem |

The full set of possible handoffs is in the [Agent Registry](agent-registry.md), and workflow-to-workflow routes are in the [Workflow Registry](workflow-registry.md).

A handoff preserves:

- the problem statement
- the evidence
- the findings
- the hypotheses
- the decisions
- the open questions

The receiving agent should not have to ask again for what was already established, and should keep observed, assumed and hypothesized information labeled.

## Architectural Principles

1. **Reuse skills instead of duplicating instructions.** A capability is defined once.
2. **Keep agents focused.** One agent, one engineering responsibility.
3. **Keep commands lightweight.** A command routes a request and adds no engineering logic.
4. **Use workflows for repeatable multi-stage processes.** They orchestrate and do not restate.
5. **Evaluate every layer independently.** Skills, agents, workflows and commands each have their own cases.
6. **Validate the complete chain with integration evaluations.** Layers can each pass and the seams can still fail.
7. **Prefer evidence over assumptions.** Label what is observed, assumed, hypothesized and confirmed.
8. **Minimize unnecessary work.** Select the skills and stages the task needs, and skip the rest.
9. **Preserve user control over modifications.** Analysis and planning do not authorize change.
10. **Keep the system extensible.** Add a capability at the right layer, register it, specify it, and evaluate it, without changing the layers that reuse it.

## Repository Layout

```
.claude/{skills,agents,commands,workflows}/
.github/{skills,agents,prompts,workflows}/
docs/        specifications, registries and overviews
templates/   reusable templates (project-context/)
scripts/     project-context/ generator (Python standard library, no dependencies)
evals/       skill, agents/, commands/, workflows/ and integration/ evaluations
```

## Documentation Map

| Topic | Document |
| --- | --- |
| Skills | [Skill Specification](skill-specification.md), [Skills](skills.md) |
| Agents | [Agent Specification](agent-specification.md), [Agent Registry](agent-registry.md), [Agent Evaluation Matrix](agent-evaluation-matrix.md) |
| Commands | [Commands](commands.md), [Command Registry](command-registry.md) |
| Workflows | [Workflow Specification](workflow-specification.md), [Workflow Registry](workflow-registry.md), [Workflows](workflows.md) |
| Change and PR analysis | [Change Intelligence Specification](change-intelligence-specification.md), [PR Intelligence Specification](pr-intelligence-specification.md) |
| Project context | [Project Context Specification](project-context-specification.md), [Project Context](project-context.md), [Generator Specification](project-context-generator-specification.md), [Drift Specification](project-context-drift-specification.md), [Registry](project-context-registry.md), [Template](../templates/project-context/PROJECT-CONTEXT.md) |
| External tools (MCP) | [Strategy](mcp-integration-strategy.md), [Registry](mcp-registry.md), [Runtime Configuration](mcp-runtime-configuration.md), [Clients](mcp-clients/README.md) |
| Packaging | [Plugin Architecture](plugin-architecture.md) |
| Evaluation | [Evaluation suite](../evals/README.md), [Integration evaluations](../evals/integration/README.md) |
