# Workflow Registry

The list of implemented workflows. For what workflows are, see [Workflows](workflows.md). For their structure, see the [Workflow Specification](workflow-specification.md). The agents and commands they use are listed in the [Agent Registry](agent-registry.md) and the [Command Registry](command-registry.md).

Each workflow exists in two equivalent definitions: `.claude/workflows/<name>.md` for Claude Code and `.github/workflows/<name>.md` for GitHub Copilot. These are AI engineering process definitions, not GitHub Actions.

## Status Values

| Status | Meaning |
| --- | --- |
| **Planned** | Defined but not yet implemented. |
| **In Progress** | Implemented, with evaluation cases written, but the cases have not yet been run and judged. |
| **Evaluated** | The evaluation cases have been run and judged, and the outcomes recorded. |
| **Stable** | Evaluated, with no open Needs Improvement or Fail outcomes, and in regular use. |

Statuses are qualitative. There are no scores or rankings.

## Registry

| Workflow | Purpose | Entry command | Primary agents | Supporting agents | Stage commands | Evaluation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [feature-development](../.claude/workflows/feature-development.md) | Take a new feature through a 14-stage lifecycle, from requirement to a validated change ready for PR, with human checkpoints | `/feature` | None (the workflow orchestrates) | architecture-agent, api-development-agent, database-troubleshooting-agent, change-intelligence-agent, test-planning-agent, pr-review-agent, pr-intelligence-agent | `/architecture`, `/api`, `/database`, `/change-impact`, `/test-plan`, `/review`, `/pr-intelligence` | [`evals/workflows/feature-development/`](../evals/workflows/feature-development/README.md) | In Progress |
| [bug-fix](../.claude/workflows/bug-fix.md) | Fix a defect after establishing a supported root cause, with a regression test | `/bug-fix` | bug-investigation-agent | test-planning-agent, pr-review-agent | `/debug`, `/test-plan`, `/review` | [`evals/workflows/bug-fix/`](../evals/workflows/bug-fix/README.md) | In Progress |
| [api-change](../.claude/workflows/api-change.md) | Design, implement and validate a new or changed API with a compatibility decision | `/api-change` | api-development-agent | architecture-agent, database-troubleshooting-agent, test-planning-agent, pr-review-agent | `/api`, `/database`, `/test-plan`, `/review` | [`evals/workflows/api-change/`](../evals/workflows/api-change/README.md) | In Progress |
| [database-change](../.claude/workflows/database-change.md) | Plan, implement and validate a schema, data or query change with rollback planning | `/database-change` | database-troubleshooting-agent | architecture-agent, api-development-agent, test-planning-agent, pr-review-agent | `/database`, `/api`, `/test-plan`, `/review` | [`evals/workflows/database-change/`](../evals/workflows/database-change/README.md) | In Progress |
| [pr-preparation](../.claude/workflows/pr-preparation.md) | Prepare a finished change for PR with only the reviews it needs | `/pr-prep` | pr-review-agent | test-planning-agent, architecture-agent | `/review`, `/test-plan`, `/architecture` | [`evals/workflows/pr-preparation/`](../evals/workflows/pr-preparation/README.md) | In Progress |
| [e2e-test-creation](../.claude/workflows/e2e-test-creation.md) | Create a reliable browser E2E test, or recommend a lower test level | `/e2e` | test-planning-agent | bug-investigation-agent, pr-review-agent | `/test-plan`, `/debug` | [`evals/workflows/e2e-test-creation/`](../evals/workflows/e2e-test-creation/README.md) | In Progress |
| [production-incident](../.claude/workflows/production-incident.md) | Respond to a production incident from detection to prevention, stabilization first | `/incident` | production-incident-agent | bug-investigation-agent, database-troubleshooting-agent, architecture-agent | `/incident`, `/debug`, `/database`, `/architecture` | [`evals/workflows/production-incident/`](../evals/workflows/production-incident/README.md) | In Progress |
| [pr-intelligence](../.claude/workflows/pr-intelligence.md) | Assess whether a complete proposed change is ready for review or merge, analysis only | `/pr-intelligence`, `/review-pr` | pr-intelligence-agent | test-planning-agent | `/pr-intelligence`, `/test-plan` | [`evals/pr-intelligence/`](../evals/pr-intelligence/README.md) | In Progress |

Each workflow also has a Project Context section, following [Project Context Consumption](project-context-consumption.md). It names where context helps and adds no stage.

All eight workflows are In Progress because none of their evaluation cases has been run yet.

The entry command starts the workflow; stage commands are the commands a workflow uses inside its stages. `/feature`, `/bug-fix`, `/api-change`, `/database-change`, `/e2e` and `/pr-prep` are workflow commands that route to one workflow file. `/incident` is an agent command that starts the production-incident workflow. Shared mechanics (context, requirements, evidence classes, MCP detection, testing, change intelligence, code review routing, PR preparation, final validation, the output contract, states and checkpoints) are in [Workflow Common Guidance](workflow-common.md). The seven Phase 4 workflows (every workflow except pr-intelligence) are summarized, with inputs, agents, skills, capabilities, outputs, safety, checkpoints and failure handling, in [Workflows](workflows.md#phase-4-workflow-summaries). No Grafana MCP is used in this phase.

`change-intelligence-agent` (`/change-impact`) is also used inside existing stages, where the change spans several areas: stage 1 of pr-preparation, stage 10 of feature-development, stage 4 of api-change, stage 5 of database-change, and stage 6 of bug-fix. It adds no stage.

## Relationships

Workflows may hand work to each other. These are possible routes, not required chains.

| From | Can route to | When |
| --- | --- | --- |
| feature-development | api-change, database-change, e2e-test-creation | Part of the feature grows into its own change |
| | pr-preparation | The change is finished |
| bug-fix | pr-preparation | The fix is finished |
| | production-incident | The defect proves to be live production impact |
| | database-change, api-change | The fix lands in storage or a contract |
| api-change | database-change | Persistence changes are needed |
| | pr-preparation | The change is finished |
| database-change | api-change | The contract changes as a result |
| | pr-preparation | The change is finished |
| e2e-test-creation | bug-fix | The test exposes a product defect |
| | pr-preparation | The test is finished |
| production-incident | bug-fix, database-change | The fix after stabilization |
| pr-preparation | pr-intelligence | An independent readiness view is wanted |
| pr-intelligence | pr-preparation | The author still needs the PR prepared |

## Adding or Changing a Workflow

- Follow the [Workflow Specification](workflow-specification.md) and its quality checklist.
- Add or update both platform definitions, and this row, with primary and supporting agents, commands, evaluation location and status.
- Check that every agent, skill and command it references exists.
- Add evaluation cases under `evals/workflows/<name>/`.
- Keep the status in line with the evaluation results.
- Do not add GitHub Actions YAML files for a workflow.
