---
name: pr-preparation
description: Prepare a finished change for pull request by reviewing the diff, checking tests, documentation and relevant security, performance and architecture concerns, running validation and writing the PR summary. Use before opening a PR; not for implementing changes.
---

# PR Preparation Workflow

## Purpose

Take a completed change to a reviewable, honestly described PR. The workflow applies only the reviews the change needs, confirms validation actually ran, and prepares the summary. It orchestrates existing agents and skills and does not restate how review works.

## When to Use

- A change is written and about to be proposed.
- The engineer wants a self-review and a PR description.
- Another workflow hands off a finished change.

## When NOT to Use

- The change is not written yet. Use [feature-development](feature-development.md) or [bug-fix](bug-fix.md).
- Someone else's PR needs a review only. Use `/review` with `pr-review-agent`.
- Production is failing. Use [production-incident](production-incident.md).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The change: diff, branch or files | Required | |
| The intent: issue, requirement or description | Preferred | |
| Test commands and CI expectations | Preferred | |
| PR template and conventions | Gathered | From the repository. |
| Constraints: reviewers, scope, release timing | Optional | Carried unchanged into every stage. |

## Project Context

Follow [Project Context Consumption](../../docs/project-context-consumption.md). Context is consumed where it changes what a stage does. This workflow adds no context-loading stage. The agent performing the stage loads what it needs, and later stages reuse it.

```
Change → Project Context (as needed) → Review → Validation → Summary
```

Stages 2 and 6 use conventions and architecture for review. Stage 8 uses build and run commands for validation. Skip loading context for a small change that needs none.

The workflow does not assume the context is current. If it is missing, the workflow proceeds from repository evidence. Stale or conflicting context is reported when it affects the outcome. Secrets in a context are never reproduced.

## Stages

Each stage follows the lifecycle in the [Workflow Specification](../../docs/workflow-specification.md).

| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Understand Change | | Workflow; repository reading; `change-intelligence-agent` (`/change-impact`) when the change spans more than one area or touches a contract, data or configuration | Intent, scope, areas touched, change categories, impact and validation needs | Never (the agent is skipped for a single-area change with no contract, data or configuration effect) |
| 2 | Review Diff | 1 | `pr-review-agent` (`/review`) | Prioritized findings on the change | Never |
| 3 | Check Tests | 1, 2 | `testing` skill; `test-planning-agent` (`/test-plan`) if gaps are found | Coverage assessment, gaps, test run results | Documentation-only change |
| 4 | Review Security | 1 | `security` skill via `pr-review-agent` | Security findings | The change touches no auth, input, data, secrets or dependencies |
| 5 | Review Performance Where Relevant | 1 | `performance` skill via `pr-review-agent` | Performance findings | No hot path, query, loop over data or resource use changes |
| 6 | Review Architecture Where Relevant | 1 | `architecture-agent` (`/architecture`) | Boundary and coupling findings | The change stays within one component and existing patterns |
| 7 | Check Documentation | 1 | Workflow; repository reading | Docs, changelog or API docs needing updates | Nothing user-visible or contract-related changed |
| 8 | Run Validation | 2-7 | Workflow; local build and test execution | Actual build and test output | Never |
| 9 | Prepare PR Summary | 1-8 | Workflow with results of earlier stages | PR title and description | Never |
| 10 | Final Review | 8, 9 | `pr-review-agent` | Confirmation that the summary matches the diff and that blockers are resolved | Never |

Stages 3-7 are independent of each other and may run in any order. Findings that require code changes stop the workflow and are returned to the engineer; this workflow does not apply fixes unless asked.

## Commands

| Command | Serves stage |
| --- | --- |
| [`/review`](../commands/review.md) | 2, 4, 5, 10 |
| [`/test-plan`](../commands/test-plan.md) | 3 |
| [`/change-impact`](../commands/change-impact.md) | 1 |
| [`/architecture`](../commands/architecture.md) | 6 |

## Agents

| Agent | Role | Stage | Used when |
| --- | --- | --- | --- |
| [pr-review-agent](../agents/pr-review-agent.md) | Primary | 2, 4, 5, 10 | Always |
| [test-planning-agent](../agents/test-planning-agent.md) | Supporting | 3 | Tests are missing or weak |
| [architecture-agent](../agents/architecture-agent.md) | Supporting | 6 | The change crosses boundaries or alters structure |
| [change-intelligence-agent](../agents/change-intelligence-agent.md) | Supporting | 1 | The change spans several areas or touches a contract, data or configuration |

## Skills

Applied through the agents above. None is required for every change.

- [`code-review`](../skills/code-review/SKILL.md): through the primary agent.
- [`testing`](../skills/testing/SKILL.md): stage 3.
- [`security`](../skills/security/SKILL.md): stage 4.
- [`performance`](../skills/performance/SKILL.md): stage 5.
- [`architecture`](../skills/architecture/SKILL.md): stage 6.
- [`change-intelligence`](../skills/change-intelligence/SKILL.md): stage 1, through its agent. Its impact findings decide which of stages 3-6 run.

## Decision Points

| If | Then |
| --- | --- |
| Documentation-only change | Run stages 1, 2, 7, 9, 10. Skip 3-6 |
| The change touches auth, input handling, secrets or dependencies | Run stage 4 |
| The change touches queries, loops over data, caching or resource use | Run stage 5 |
| The change adds a component, boundary or integration | Run stage 6 |
| The change spans several areas | Use `change-intelligence-agent` in stage 1, and let its impact findings decide which of stages 3-6 run |
| The change includes a schema or migration | Confirm it followed [database-change](database-change.md); otherwise route there |
| The change alters an API | Confirm it followed [api-change](api-change.md); otherwise route there |
| Tests are missing for behavior changes | Report the gap; offer `test-planning-agent` |
| Blocking findings exist | Stop before stage 9 and return them |
| CI or tests cannot be run locally | Report "not run" and list the commands |

## Validation

- **Stage validation:** every review stage either produced findings or stated that nothing applies. Skipped reviews are recorded with reasons.
- **Final validation:** build and tests were run and their output seen, or are explicitly reported as not run; the PR summary matches the diff; no blocker remains open.
- **Evidence:** findings tied to the diff, test and build output.
- **Rollback:** the PR notes how the change is reverted, for risky changes.

## Safety

| Stage | Kind |
| --- | --- |
| 1-7, 9, 10 | Analysis and planning. Read-only. |
| 8 | Local execution of build and tests |

- The workflow does not modify code, push branches, open or merge PRs, post comments or approve anything without explicit authorization.
- A clean review is not an approval to merge or deploy.
- Secrets or personal data found in the diff are reported by location, not repeated.

## Output

A PR-readiness report: change summary, review findings by priority, test and validation results, stages skipped with reasons, documentation status, open issues, and the drafted PR title and description. The PR description states what was and was not tested. The workflow is reported **complete** only when required stages completed.

## Handoff

- To the engineer, with findings to fix, or the drafted PR text.
- To `test-planning-agent` for test gaps.
- To [bug-fix](bug-fix.md) if review finds a defect that needs investigation.
- To `architecture-agent` for structural concerns beyond the PR.

## Examples

**Request:** "Prepare the PR for my change to the invoice service."

Stage 1 shows a new endpoint touching customer data. Stages 2, 3, 4, 7, 8, 9, 10 run. Stage 5 is skipped (no hot path). Stage 6 is skipped (same component).

**Request:** "Get this README edit ready."

Stages 1, 2, 7, 9, 10. All others are skipped as irrelevant.

## Related Workflows

- [feature-development](feature-development.md), [bug-fix](bug-fix.md): the usual predecessors.
- [api-change](api-change.md), [database-change](database-change.md): specialized predecessors.
