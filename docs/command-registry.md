# Command Registry

The list of implemented commands. For what commands are and how they behave, see [Commands](commands.md). The target agents are listed in the [Agent Registry](agent-registry.md) and the target workflows in the [Workflow Registry](workflow-registry.md).

## Status Values

| Status | Meaning |
| --- | --- |
| **Planned** | Defined but not yet implemented. |
| **In Progress** | Implemented, with evaluation cases written, but the cases have not yet been run and judged. |
| **Evaluated** | The evaluation cases have been run and judged, and the outcomes recorded. |
| **Stable** | Evaluated, with no open Needs Improvement or Fail outcomes, and in regular use. |

Statuses are qualitative. There are no scores or rankings.

## Registry

| Command | Claude location | Copilot location | Target agent | Target workflow | Purpose | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `/review` | [`.claude/commands/review.md`](../.claude/commands/review.md) | [`.github/prompts/review.prompt.md`](../.github/prompts/review.prompt.md) | pr-review-agent | None | Start a PR or code review | In Progress |
| `/debug` | [`.claude/commands/debug.md`](../.claude/commands/debug.md) | [`.github/prompts/debug.prompt.md`](../.github/prompts/debug.prompt.md) | bug-investigation-agent | None | Investigate an unexpected behavior or failure | In Progress |
| `/test-plan` | [`.claude/commands/test-plan.md`](../.claude/commands/test-plan.md) | [`.github/prompts/test-plan.prompt.md`](../.github/prompts/test-plan.prompt.md) | test-planning-agent | None | Create a test strategy or test plan | In Progress |
| `/architecture` | [`.claude/commands/architecture.md`](../.claude/commands/architecture.md) | [`.github/prompts/architecture.prompt.md`](../.github/prompts/architecture.prompt.md) | architecture-agent | None | Analyze or design system architecture | In Progress |
| `/api` | [`.claude/commands/api.md`](../.claude/commands/api.md) | [`.github/prompts/api.prompt.md`](../.github/prompts/api.prompt.md) | api-development-agent | None | Design, implement, review or evolve an API | In Progress |
| `/database` | [`.claude/commands/database.md`](../.claude/commands/database.md) | [`.github/prompts/database.prompt.md`](../.github/prompts/database.prompt.md) | database-troubleshooting-agent | None | Investigate or design database and SQL behavior | In Progress |
| `/incident` | [`.claude/commands/incident.md`](../.claude/commands/incident.md) | [`.github/prompts/incident.prompt.md`](../.github/prompts/incident.prompt.md) | production-incident-agent | None | Investigate an active or recent production incident | In Progress |
| `/change-impact` | [`.claude/commands/change-impact.md`](../.claude/commands/change-impact.md) | [`.github/prompts/change-impact.prompt.md`](../.github/prompts/change-impact.prompt.md) | change-intelligence-agent | None | Analyze the engineering impact of a change | In Progress |
| `/pr-intelligence` | [`.claude/commands/pr-intelligence.md`](../.claude/commands/pr-intelligence.md) | [`.github/prompts/pr-intelligence.prompt.md`](../.github/prompts/pr-intelligence.prompt.md) | pr-intelligence-agent | None | Assess whether a PR or change is ready | In Progress |
| `/review-pr` | [`.claude/commands/review-pr.md`](../.claude/commands/review-pr.md) | [`.github/prompts/review-pr.prompt.md`](../.github/prompts/review-pr.prompt.md) | pr-intelligence-agent (shared with `/pr-intelligence`) | None | Review a GitHub PR by URL or number through the source-control capability | In Progress |
| `/context` | [`.claude/commands/context.md`](../.claude/commands/context.md) | [`.github/prompts/context.prompt.md`](../.github/prompts/context.prompt.md) | None (tool command; runs the Project Context Generator) | None | Generate, inspect or check the current repository's Project Context | In Progress |
| `/feature` | [`.claude/commands/feature.md`](../.claude/commands/feature.md) | [`.github/prompts/feature.prompt.md`](../.github/prompts/feature.prompt.md) | None (workflow command) | [feature-development](../.claude/workflows/feature-development.md) | Develop a feature from requirement to a validated change | In Progress |
| `/bug-fix` | [`.claude/commands/bug-fix.md`](../.claude/commands/bug-fix.md) | [`.github/prompts/bug-fix.prompt.md`](../.github/prompts/bug-fix.prompt.md) | None (workflow command) | [bug-fix](../.claude/workflows/bug-fix.md) | Fix a defect with a supported root cause and a regression test | In Progress |
| `/api-change` | [`.claude/commands/api-change.md`](../.claude/commands/api-change.md) | [`.github/prompts/api-change.prompt.md`](../.github/prompts/api-change.prompt.md) | None (workflow command) | [api-change](../.claude/workflows/api-change.md) | Design, implement and validate an API change | In Progress |
| `/database-change` | [`.claude/commands/database-change.md`](../.claude/commands/database-change.md) | [`.github/prompts/database-change.prompt.md`](../.github/prompts/database-change.prompt.md) | None (workflow command) | [database-change](../.claude/workflows/database-change.md) | Plan, implement and validate a database change | In Progress |
| `/e2e` | [`.claude/commands/e2e.md`](../.claude/commands/e2e.md) | [`.github/prompts/e2e.prompt.md`](../.github/prompts/e2e.prompt.md) | None (workflow command) | [e2e-test-creation](../.claude/workflows/e2e-test-creation.md) | Create a browser E2E test, or recommend a lower level | In Progress |
| `/pr-prep` | [`.claude/commands/pr-prep.md`](../.claude/commands/pr-prep.md) | [`.github/prompts/pr-prep.prompt.md`](../.github/prompts/pr-prep.prompt.md) | None (workflow command) | [pr-preparation](../.claude/workflows/pr-preparation.md) | Prepare a finished change for a pull request | In Progress |

All seventeen commands are In Progress because none of their evaluation cases has been run yet. Evaluation cases for the first seven are in [`evals/commands/`](../evals/commands/README.md). The six workflow commands are exercised through the [workflow evaluations](../evals/workflows/README.md). `/review-pr` is evaluated in [`evals/pr-intelligence/mcp/`](../evals/pr-intelligence/mcp/README.md). `/change-impact` and `/pr-intelligence` have no separate routing cases yet. They are exercised through [`evals/change-intelligence/`](../evals/change-intelligence/README.md) and [`evals/pr-intelligence/`](../evals/pr-intelligence/README.md).

## `/context` Operations

Underlying capability for all three: the [Project Context Generator and Drift Detector](../scripts/project-context/README.md), specified in the [Generator](project-context-generator-specification.md) and [Drift](project-context-drift-specification.md) specifications. Evaluation: [`evals/project-context-command/`](../evals/project-context-command/README.md).

| Operation | Purpose | Inputs | Output | Safety behavior |
| --- | --- | --- | --- | --- |
| `/context generate` | Create or update the current repository's `PROJECT-CONTEXT.md` | Current working directory; optional `--dry-run` | The written (or proposed) context, counts of Confirmed, Inferred and Unknown entries, key unknowns, secret-detection status, conflicts | Writes only `PROJECT-CONTEXT.md` in the target, through the generator. Preserves developer-provided and manual content. Never writes a secret. Stops on an unrecognizable directory or the Hub itself. No commit |
| `/context inspect` | Summarize the existing context | Current working directory | Summary by area, with freshness and unknowns; says when the context is absent | Read-only. Never regenerates. Never reproduces a secret |
| `/context drift` | Report whether the context may be stale | Current working directory | Drift status, findings by materiality, recommendation | Read-only. Never modifies the context, and recommends `generate` without running it |

## Adding or Changing a Command

- Add or update the row here, with both platform locations, the target agent and the status.
- Keep the status in line with the evaluation results.
- Check that the target agent exists in the [Agent Registry](agent-registry.md), or that the target workflow exists in the [Workflow Registry](workflow-registry.md). A command names one agent or one workflow, never both.
