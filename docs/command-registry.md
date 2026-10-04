# Command Registry

The list of implemented commands. For what commands are and how they behave, see [Commands](commands.md). The target agents are listed in the [Agent Registry](agent-registry.md).

## Status Values

| Status | Meaning |
| --- | --- |
| **Planned** | Defined but not yet implemented. |
| **In Progress** | Implemented, with evaluation cases written, but the cases have not yet been run and judged. |
| **Evaluated** | The evaluation cases have been run and judged, and the outcomes recorded. |
| **Stable** | Evaluated, with no open Needs Improvement or Fail outcomes, and in regular use. |

Statuses are qualitative. There are no scores or rankings.

## Registry

| Command | Claude location | Copilot location | Target agent | Purpose | Status |
| --- | --- | --- | --- | --- | --- |
| `/review` | [`.claude/commands/review.md`](../.claude/commands/review.md) | [`.github/prompts/review.prompt.md`](../.github/prompts/review.prompt.md) | pr-review-agent | Start a PR or code review | In Progress |
| `/debug` | [`.claude/commands/debug.md`](../.claude/commands/debug.md) | [`.github/prompts/debug.prompt.md`](../.github/prompts/debug.prompt.md) | bug-investigation-agent | Investigate an unexpected behavior or failure | In Progress |
| `/test-plan` | [`.claude/commands/test-plan.md`](../.claude/commands/test-plan.md) | [`.github/prompts/test-plan.prompt.md`](../.github/prompts/test-plan.prompt.md) | test-planning-agent | Create a test strategy or test plan | In Progress |
| `/architecture` | [`.claude/commands/architecture.md`](../.claude/commands/architecture.md) | [`.github/prompts/architecture.prompt.md`](../.github/prompts/architecture.prompt.md) | architecture-agent | Analyze or design system architecture | In Progress |
| `/api` | [`.claude/commands/api.md`](../.claude/commands/api.md) | [`.github/prompts/api.prompt.md`](../.github/prompts/api.prompt.md) | api-development-agent | Design, implement, review or evolve an API | In Progress |
| `/database` | [`.claude/commands/database.md`](../.claude/commands/database.md) | [`.github/prompts/database.prompt.md`](../.github/prompts/database.prompt.md) | database-troubleshooting-agent | Investigate or design database and SQL behavior | In Progress |
| `/incident` | [`.claude/commands/incident.md`](../.claude/commands/incident.md) | [`.github/prompts/incident.prompt.md`](../.github/prompts/incident.prompt.md) | production-incident-agent | Investigate an active or recent production incident | In Progress |
| `/change-impact` | [`.claude/commands/change-impact.md`](../.claude/commands/change-impact.md) | [`.github/prompts/change-impact.prompt.md`](../.github/prompts/change-impact.prompt.md) | change-intelligence-agent | Analyze the engineering impact of a change | In Progress |
| `/pr-intelligence` | [`.claude/commands/pr-intelligence.md`](../.claude/commands/pr-intelligence.md) | [`.github/prompts/pr-intelligence.prompt.md`](../.github/prompts/pr-intelligence.prompt.md) | pr-intelligence-agent | Assess whether a PR or change is ready | In Progress |

| `/context` | [`.claude/commands/context.md`](../.claude/commands/context.md) | [`.github/prompts/context.prompt.md`](../.github/prompts/context.prompt.md) | None (tool command; runs the Project Context Generator) | Generate, inspect or check the current repository's Project Context | In Progress |

All ten commands are In Progress because none of their evaluation cases has been run yet. Evaluation cases for the first seven are in [`evals/commands/`](../evals/commands/README.md). `/change-impact` and `/pr-intelligence` have no separate routing cases yet. They are exercised through [`evals/change-intelligence/`](../evals/change-intelligence/README.md) and [`evals/pr-intelligence/`](../evals/pr-intelligence/README.md).

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
- Check that the target agent exists in the [Agent Registry](agent-registry.md).
