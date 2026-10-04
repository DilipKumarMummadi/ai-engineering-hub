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

A workflow may call an agent directly when no command fits the stage. Six workflow commands start a workflow directly: `/feature`, `/bug-fix`, `/api-change`, `/database-change`, `/e2e` and `/pr-prep`. `/incident` starts the production-incident workflow through `production-incident-agent`, and `/pr-intelligence` and `/review-pr` start the pr-intelligence workflow. A workflow can also be started by name, for example "run the bug-fix workflow". Other commands such as `/review` still route to a single agent.

## Common Architecture

All workflows share one shape. Not every workflow uses every stage; the ones that do not apply are skipped with a recorded reason.

```
Requirement / Trigger
  -> Context Check
  -> Existing System Analysis
  -> Agent
  -> Skills
  -> Implementation / Investigation
  -> Testing
  -> Change Intelligence
  -> Code Review
  -> PR Preparation
  -> PR Intelligence
  -> Validation / Decision
```

Reusable mechanics live in [Workflow Common Guidance](workflow-common.md): context loading, requirement loading, evidence classification, MCP capability detection, the testing, change intelligence, code review and PR preparation stages, final validation, the output contract (Objective, Context, Evidence, Plan, Actions, Validation, Findings, Risks, Unknowns, Recommendation), workflow states (ANALYZING, PLAN_READY, IMPLEMENTING, VALIDATING, NEEDS_INFORMATION, NEEDS_HUMAN_APPROVAL, FAILED, COMPLETED), human checkpoints, safety and failure reporting.

**Dynamic skill routing.** Workflows do not run a fixed list of skills. The agent at each stage selects skills from the evidence (changed files, risk, kind of change) and skips the rest. The routing rules are in [Workflow Common Guidance](workflow-common.md).

**No Grafana MCP in this phase.** Observability-backed evidence (logs, metrics, traces) is used only when the user supplies it or an existing capability provides it. Grafana MCP is not part of Phase 4.

## Feature Development Lifecycle

`feature-development` is the most comprehensive workflow. Stage 1 includes the Requirement Intelligence readiness gate when a ticket key is supplied or the requirement needs checking: only a `READY` requirement continues ([Readiness Policy](requirement-readiness-policy.md)). It runs a 14-stage lifecycle: 1 Requirement, 2 Understand Repository, 3 Project Context, 4 Existing System Analysis, 5 Architecture/Design, 6 Implementation Plan, 7 Implementation, 8 Testing, 9 Security Review, 10 Change Intelligence, 11 Code Review, 12 PR Preparation, 13 PR Intelligence, 14 Final Validation. Irrelevant stages are skipped with a recorded reason.

- **Requirements** are classified Confirmed, Inferred or Unknown. Unknown requirements are asked about, not guessed.
- **Human checkpoints:** PLAN READY, IMPLEMENTATION READY, VALIDATION READY and PR READY. Significant architectural, destructive database, security-sensitive, infrastructure, production-impacting and broad or refactoring changes also need explicit user confirmation. Planning is never authorization, and migrations and deployments are never run.
- **Capabilities** (`source-control`, `requirements-tracking`, `database`, `browser-automation`, `cloud-platform`) are optional. Unavailable ones are reported, for example "Jira MCP is not configured, so requirement-level validation could not be performed."
- **Failures** are reported with the stage, failure, evidence, likely cause, what continues and what is blocked.
- **Final readiness** is READY, NEEDS_CHANGES or NEEDS_INFORMATION, corresponding to Ready, Needs Changes and Needs Information in the [PR Intelligence Specification](pr-intelligence-specification.md). Failing tests never give READY.

See the [feature-development workflow](../.claude/workflows/feature-development.md) and its [evaluations](../evals/workflows/feature-development/README.md).

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

## Phase 4 Workflow Summaries

Each workflow has a full definition (purpose, inputs, stages, decision points, safety, output, handoff). All seven keep the `Project Context` section and add no context stage. Common checkpoints, states and failure reporting are in [Workflow Common Guidance](workflow-common.md). Stages below are summaries.

| Workflow | Objective | Trigger | Inputs | Stages (summary) | Agents | Skills | MCP capabilities | Outputs | Safety | Human checkpoints | Failure handling |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [feature-development](../.claude/workflows/feature-development.md) | A new feature, validated and ready for PR | `/feature` | Requirement or ticket, constraints, acceptance criteria | Requirement, repository, context check, existing system analysis, design, plan, implementation, testing, security, change intelligence, review, PR prep, PR intelligence, final validation | architecture, api-development, database-troubleshooting, change-intelligence, test-planning, pr-review, pr-intelligence | By evidence: architecture, testing, code-review, change-intelligence, security, database-sql, performance, reliability, playwright | `requirements-tracking`, `source-control`, `database`, `browser-automation`, `cloud-platform`, all optional | Validated change, tests, review, PR summary, READY / NEEDS_CHANGES / NEEDS_INFORMATION | No migrations or deployments run; planning is not authorization | PLAN READY, IMPLEMENTATION READY, VALIDATION READY, PR READY | Stage, failure, evidence, cause, what continues, what is blocked |
| [bug-fix](../.claude/workflows/bug-fix.md) | A defect fixed on a confirmed root cause | `/bug-fix` | Symptom, errors, logs, reproduction | Capture symptom, reproduce, evidence, investigate, confirm root cause, minimal fix plan, fix, regression test, review, validate | bug-investigation, test-planning, pr-review, change-intelligence | debugging, testing, plus observability, database-sql, performance, security, playwright when evidence points there | `requirements-tracking`, `source-control` optional | Root cause, minimal fix, regression test, validation evidence | No fix before the cause is supported; no production changes | Root cause confirmed before the fix; fix go-ahead | Unconfirmed cause is reported, not fixed around |
| [api-change](../.claude/workflows/api-change.md) | A new or changed API with a compatibility decision | `/api-change` | API requirement, consumers, constraints | Requirement, existing API, contract design, compatibility, security, persistence, implementation, testing, documentation, review, validation | api-development, database-troubleshooting, change-intelligence, test-planning, pr-review | api-development, security, testing, code-review; database-sql, performance, reliability when needed | `requirements-tracking`, `source-control` optional | Contract, compatibility decision, tests, docs | Breaking changes need an explicit decision; unknown consumers reported | Contract and compatibility decision; implementation go-ahead | Unknown consumers and failed tests block a READY result |
| [database-change](../.claude/workflows/database-change.md) | A schema, data or query change with a rollback plan | `/database-change` | Change, engine, environment, data volume | Requirement, schema and data analysis, migration design, query impact, performance, concurrency, security, implementation, validation, rollback, review | database-troubleshooting, change-intelligence, test-planning, pr-review | database-sql, security, reliability, performance, testing | `database` (read-only), `requirements-tracking` optional | Migration scripts (not run), rollback plan, validation on a disposable database | Migrations are never applied to shared or production systems; destructive statements need explicit authorization | Migration and rollback plan; implementation go-ahead | Missing database access is reported; no fabricated results |
| [e2e-test-creation](../.claude/workflows/e2e-test-creation.md) | A reliable browser test, or a recommended lower-level test | `/e2e` | User flow, environment, test data, authentication | Flow, preconditions, data, locators, assertions, authentication, implementation, run, investigate failures, stabilize, validate | test-planning, bug-investigation, pr-review | testing, playwright, debugging | `browser-automation` optional | Test file, run evidence, or a lower-level recommendation | Runs only against environments the user names; no real data or credentials in tests | Test level decision; implementation go-ahead | A test that was not run is reported as not run; flaky tests are not reported as stable |
| [pr-preparation](../.claude/workflows/pr-preparation.md) | A finished change prepared for a reviewable PR | `/pr-prep` | Branch or diff, requirement, test results | Understand change, review diff, tests, security, performance, architecture, documentation, validation, PR summary, final review | pr-review, change-intelligence, test-planning, architecture | code-review, testing, change-intelligence, security, performance, architecture (only as the change requires) | `source-control`, `requirements-tracking` optional | PR title and description, reviewer notes, open risks | Does not push, open, approve or merge | Summary and PR READY confirmation | Unrun validation is reported, not assumed passing |
| [production-incident](../.claude/workflows/production-incident.md) | A stabilized, explained and followed-up incident |
| [pr-intelligence](../.claude/workflows/pr-intelligence.md) | A readiness decision for a complete proposed change | `/incident` | Incident description, impact, timeline, logs, metrics | Detect, impact, stabilize, evidence, timeline, investigate, validate hypothesis, recover, confirm recovery, root cause, prevention, follow-up | production-incident, bug-investigation, database-troubleshooting, architecture | debugging, observability, reliability; performance, database-sql, security when evidence calls | `database`, `cloud-platform` read-only; no Grafana MCP in this phase | Impact, timeline, evidence by class, recovery confirmation, prevention list | No rollback, restart, scaling, failover, flag, configuration or data change without explicit authorization | Mitigation authorization before recovery | Observed, hypothesis and confirmed are kept apart; recovery is claimed only with evidence |

The existing [pr-intelligence](../.claude/workflows/pr-intelligence.md) workflow (`/pr-intelligence`, `/review-pr`) is analysis only and recommends, never approves or merges.

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

## External Capabilities

Workflows may use capabilities when a provider is connected, and continue without them when not. The feature-development workflow can use all five capabilities (`source-control`, `requirements-tracking`, `database`, `browser-automation`, `cloud-platform`) when connected. The feature-development, bug-fix, api-change, database-change and pr-preparation workflows can use `requirements-tracking`; e2e-test-creation can use `browser-automation`; production-incident can use `database` and `cloud-platform`. A missing provider never fails a workflow: the limitation is reported. Flow: User → Command/Workflow → Agent → Skill → Capability → Existing MCP provider → External system. See the [MCP Capability Registry](mcp-capability-registry.md).

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
