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

All seven commands are In Progress because none of their evaluation cases has been run yet. Evaluation cases are in [`evals/commands/`](../evals/commands/README.md).

## Adding or Changing a Command

- Add or update the row here, with both platform locations, the target agent and the status.
- Keep the status in line with the evaluation results.
- Check that the target agent exists in the [Agent Registry](agent-registry.md).
