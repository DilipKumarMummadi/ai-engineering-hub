---
name: pr-intelligence
description: Assess whether a complete proposed change is ready for review or merge by understanding it, analyzing its impact, selecting only the relevant analyses, reviewing it, checking tests, validating the evidence and reporting a qualitative readiness. Analysis only. Use to judge PR readiness; not to prepare, implement or merge a change.
---

# PR Intelligence Workflow

## Purpose

Take a complete proposed change to an evidence-based readiness decision: Ready, Needs Changes or Needs Information. The workflow owns stage order, skip conditions and the readiness gate. The analysis itself is performed by the `pr-intelligence-agent`, which applies existing skills. The workflow does not restate how review, impact analysis or any specialized analysis works. See the [PR Intelligence Specification](../../docs/pr-intelligence-specification.md).

## When to Use

- A change or PR needs a readiness assessment before review or merge.
- An author has finished [pr-preparation](pr-preparation.md) and wants an independent readiness view.
- A reviewer wants risks, blockers and missing validation stated up front.

## When NOT to Use

- The change is not written yet. Use [feature-development](feature-development.md) or [bug-fix](bug-fix.md).
- The author needs the change prepared and the PR text written. Use [pr-preparation](pr-preparation.md).
- Only a code review is wanted. Use `/review` with `pr-review-agent`.
- Production is failing. Use [production-incident](production-incident.md).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The change: diff, branch, PR or files | Required | Without a readable change the result is Needs Information. |
| PR description or intent | Preferred | |
| Commit history | Where relevant | |
| Test and CI results | Optional | Used only if supplied or run. |
| Constraints: reviewers, release timing, known consumers | Optional | Carried unchanged into every stage. |

**External sources (optional).** If connected, a source-control MCP can supply pull request metadata, the diff, commits and checks, and a work-tracking MCP the requirement, acceptance criteria and linked tickets. The MCP supplies information and the Hub reasons over it; see the [MCP Integration Strategy](../../docs/mcp-integration-strategy.md). The workflow does not assume a server is connected, never invents its output, and proceeds from supplied and repository evidence when it is not.

## Project Context

Follow [Project Context Consumption](../../docs/project-context-consumption.md). Context is consumed where it changes what a stage does. This workflow adds no context-loading stage. The agent performing the stage loads what it needs, and later stages reuse it.

```
Change → Project Context (as needed) → Impact → Review → Validation → Readiness
```

Stage 1 loads the context as part of understanding the PR. Stage 2 uses architecture and components. Stage 5 uses the testing approach and build commands. Stage 6 uses API, database, security and observability conventions.

Repository evidence outranks context, and context outranks assumptions. If the context is missing, the workflow proceeds from repository evidence. Stale or conflicting context is reported when it affects the outcome. Secrets in a context are never reproduced.

## Stages

Each stage follows the lifecycle in the [Workflow Specification](../../docs/workflow-specification.md).

| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Understand PR | | `pr-intelligence-agent` (`/pr-intelligence`); repository reading | What is changing, why, areas affected, likely risk, expected validation, missing information | Never |
| 2 | Analyze Change Impact | 1 | `pr-intelligence-agent` applying `change-intelligence` | Direct, dependency, contract, data and runtime impact, with evidence labels | The change is single-area with no contract, data or configuration effect, and stage 1 already covers it |
| 3 | Select Relevant Perspectives | 1, 2 | `pr-intelligence-agent` | The analyses this PR needs, with reasons, and notable ones skipped | Never |
| 4 | Review | 1-3 | `pr-intelligence-agent` applying `code-review` | Severity-ranked review findings on the whole change | Never for a meaningful PR; brief for documentation-only |
| 5 | Testing Analysis | 1, 2, 4 | `pr-intelligence-agent` applying `testing`; `test-planning-agent` (`/test-plan`) if gaps need a plan | Tests affected, missing tests, the right level, tests executed versus recommended | Documentation-only change |
| 6 | Specialized Analysis Where Relevant | 3 | `pr-intelligence-agent` applying the selected skills | Security, API, database, performance, reliability and observability findings for the areas touched | No specialized perspective was selected in stage 3 |
| 7 | Validate Evidence | 2, 4-6 | `pr-intelligence-agent` | Findings re-checked against the code, unsupported ones dropped, each labeled Confirmed, Inferred or Unknown | Never |
| 8 | Determine Readiness | 7 | `pr-intelligence-agent` | Ready, Needs Changes or Needs Information, with blockers and risks separated | Never |
| 9 | Produce Report | 1-8 | `pr-intelligence-agent` | The PR Intelligence Report | Never |

Stages 5 and 6 are independent and may run in either order. Skipped stages are recorded with the reason. The workflow does not fix anything. Findings that need code changes are returned to the engineer.

## Commands

| Command | Serves stage |
| --- | --- |
| [`/pr-intelligence`](../commands/pr-intelligence.md) | 1-9 |
| [`/test-plan`](../commands/test-plan.md) | 5, when gaps need a detailed plan |

## Agents

| Agent | Role | Stage | Used when |
| --- | --- | --- | --- |
| [pr-intelligence-agent](../agents/pr-intelligence-agent.md) | Primary | 1-9 | Always |
| [test-planning-agent](../agents/test-planning-agent.md) | Supporting | 5 | Tests are missing or weak and need a detailed plan |

## Skills

Applied through the primary agent, and only the ones the change calls for. None except `code-review` is required for every PR.

- [`code-review`](../skills/code-review/SKILL.md): stage 4. The detailed review capability.
- [`change-intelligence`](../skills/change-intelligence/SKILL.md): stage 2. The impact analysis capability.
- [`testing`](../skills/testing/SKILL.md): stage 5.
- [`security`](../skills/security/SKILL.md), [`api-development`](../skills/api-development/SKILL.md), [`database-sql`](../skills/database-sql/SKILL.md), [`performance`](../skills/performance/SKILL.md), [`reliability`](../skills/reliability/SKILL.md), [`observability`](../skills/observability/SKILL.md): stage 6, when the change touches their area.
- [`architecture`](../skills/architecture/SKILL.md): stage 6, when the change alters boundaries or dependencies.
- [`playwright`](../skills/playwright/SKILL.md): stage 5, when browser behavior is affected.

## Decision Points

| If | Then |
| --- | --- |
| No readable change is available | Stop after stage 1. Readiness is Needs Information |
| Documentation-only change | Run stages 1, 4, 7, 8, 9. Skip 2, 3, 5 and 6 |
| Single-area change with no contract, data or configuration effect | Skip stage 2 |
| The change touches auth, input handling, secrets or dependencies | Include `security` in stage 6 |
| The change includes a schema or migration | Include `database-sql` and `reliability` in stage 6 |
| The change alters an API | Include `api-development` in stage 6 |
| The change alters hot paths or query behavior | Include `performance` in stage 6 |
| Behavior changed and no tests were found | Report the gap. Readiness is Needs Changes unless the change is trivial |
| A confirmed blocker exists | Readiness is Needs Changes, even if information is missing |
| Missing information prevents ruling out a blocker | Readiness is Needs Information, naming what is needed |
| Nothing was found | Do not report Ready unless the readiness criteria are met |

## Validation

- **Stage validation:** each stage produced its result or recorded why it was skipped.
- **Final validation:** every finding was re-checked against the code; tests executed are kept apart from tests recommended; the readiness follows the criteria; the report states what was not examined.
- **Evidence:** findings tied to the diff, repository files and tool output.

## Safety

| Stage | Kind |
| --- | --- |
| 1-9 | Analysis. Read-only. Local test execution only if it is safe and normal for the project. |

- The workflow never merges, approves, commits, pushes, deploys or modifies code, and never posts to the PR without explicit authorization.
- A Ready result is not an approval. Approval and merge are human decisions.
- Never claim tests passed unless they ran. Secrets found are reported by location and type, never repeated.

## Output

The PR Intelligence Report defined by the agent, with a readiness of Ready, Needs Changes or Needs Information, confirmed blockers apart from potential risks, validation performed apart from validation recommended, and missing information. The workflow is reported **complete** only when the required stages completed.

## Handoff

- To the engineer, with blockers to fix or information to supply.
- To [pr-preparation](pr-preparation.md) if the author still needs the PR prepared.
- To `test-planning-agent` for test gaps, `bug-investigation-agent` for a finding that needs investigation, `architecture-agent` for a design concern.
- To [database-change](database-change.md) or [api-change](api-change.md) if the PR reveals that the change skipped the matching process.

## Examples

**Request:** "Is this PR ready?" with a diff that adds an endpoint and a migration.

Stages 1-9 run. Stage 6 includes API, database, reliability and security, because the endpoint changes state. Performance and observability are skipped.

**Request:** "Is this ready?" with a one-word comment fix. Stages 1, 4, 7, 8, 9 run. All others are skipped.

**Request:** "Is this ready?" with only a PR title. Stage 1 finds no readable change. Readiness is Needs Information.

## Related Workflows

- [pr-preparation](pr-preparation.md): prepares the author's change and writes the PR text. PR Intelligence assesses readiness.
- [feature-development](feature-development.md), [bug-fix](bug-fix.md), [api-change](api-change.md), [database-change](database-change.md): the usual predecessors.
