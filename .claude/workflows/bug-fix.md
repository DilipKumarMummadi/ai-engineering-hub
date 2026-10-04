---
name: bug-fix
description: Take a reported defect from symptom to a validated minimal fix with a regression test, establishing a supported root cause before changing code and separating static analysis from live investigation. Use for non-urgent bugs; not for active production incidents or new features.
---

# Bug Fix Workflow

## Purpose

Resolve a defect by moving from report to evidence to hypotheses to a validated root cause, then to a minimal fix proven by a regression test. The workflow orchestrates existing agents, skills and commands and enforces one ordering rule: the symptom is not fixed before the cause is sufficiently supported. Shared mechanics (context, evidence, capabilities, testing, review, states, output, safety) are in [Workflow Common Guidance](../../docs/workflow-common.md) and are not repeated here.

## When to Use

- An error, failing test, wrong result or unexpected behavior needs to be fixed.
- The cause is unknown or not yet confirmed.
- The engineer wants the fix to include a regression test and review.

## When NOT to Use

- Production is degraded now. Use [production-incident](production-incident.md).
- The cause is already known and the change is a planned edit. Use [feature-development](feature-development.md) or make the edit directly.
- The problem is a new requirement rather than a defect.
- The problem is only a database issue needing a schema change. Route that part to [database-change](database-change.md).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Symptom: what was expected, what happened | Required | |
| Error messages, stack traces, logs | Preferred | Used as given. |
| Reproduction steps, environment, version | Preferred | |
| Ticket key or link | Optional | Only from the user or reliable evidence; never guessed. |
| Recent changes | Optional | |
| Constraints: scope, no-touch areas | Optional | Carried unchanged into every stage. |

Missing evidence is listed, not invented.

**Requirement readiness.** When a ticket key is supplied, the `requirement-intelligence-agent` (`/requirement`) can establish the report. The bug-fix path asks only what a defect needs: symptom, expected behavior, reproduction, environment and impact. It does not demand feature-style acceptance criteria, and it does not hold up a live production problem for a ticket. The key is carried as the Requirement ID into the fix, the regression test and the PR.

**External sources (optional).** Detection, fallback and the exact fallback sentences are in [Workflow Common Guidance](../../docs/workflow-common.md#4-mcp-capability-detection-and-fallback).

| Capability | Used for | Stage |
| --- | --- | --- |
| `requirements-tracking` | The bug report, priority, linked items | 1 |
| `source-control` | Recent changes, history of the affected code | 3 |
| `database` | Read-only live evidence: schema, constraints, indexes, query behavior, EXPLAIN | 3, 6 |
| `cloud-platform` | Read-only deployment and resource configuration relevant to the failure | 3 |

Live investigation is read-only. Mutating database or cloud requests are explained and need explicit authorization. Static analysis (reading code, migrations, logs supplied by the user) and live investigation are labeled separately in the evidence.

## Project Context

Follow [Project Context Consumption](../../docs/project-context-consumption.md). This workflow adds no context-loading stage; stage 2 records the context state, as in [Workflow Common Guidance](../../docs/workflow-common.md#1-context-loading).

```
Bug Report → Context Check → Repository Evidence → Hypotheses → Root Cause → Fix → Regression
```

Stages 3-4 use architecture, components, observability, database and infrastructure to decide where to look. Stage 9 uses the testing approach. Context never counts as evidence of the cause.

## Stages

Each stage follows the lifecycle in the [Workflow Specification](../../docs/workflow-specification.md).

| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Bug Report | | Workflow; `requirements-tracking` if connected | Expected vs actual behavior, impact, constraints, Confirmed / Inferred / Unknown | Never |
| 2 | Context Check | 1 | Workflow | Context state: present, missing, stale or declined | Never (recorded even if absent) |
| 3 | Reproduce / Understand | 1, 2 | `bug-investigation-agent` (`/debug`) | Reproduction actually performed, or a statement that it was not reproduced and why | The failure is fully explained by a provided trace |
| 4 | Evidence Collection | 1-3 | `bug-investigation-agent`; `debugging`; `observability` for user-supplied logs or traces | Evidence classed Observed / Unknown, static vs live | Evidence was supplied and is sufficient |
| 5 | Hypotheses | 4 | `bug-investigation-agent`; `database-sql`, `performance`, `reliability`, `security` when relevant | Ranked hypotheses with support and ways to test each | Never |
| 6 | Validation | 5 | `bug-investigation-agent` | Each hypothesis supported, refuted or untested, with evidence | Never |
| 7 | Root Cause | 6 | `bug-investigation-agent` | Confirmed Root Cause, or "root cause not yet confirmed" | Never |
| 8 | Minimal Fix | 7, PLAN_READY | The engineer or the AI, with go-ahead | Smallest working-tree change addressing the cause, inspected | Blocked until stage 7 is confirmed |
| 9 | Regression Test | 7, 8 | `test-planning-agent` (`/test-plan`); `testing` | A test that fails without the fix and passes with it, executed | A test is genuinely impractical; say why and give manual verification |
| 10 | Change Intelligence | 8, 9 | `change-intelligence-agent` (`/change-impact`); `change-intelligence` | Side effects of the fix, Confirmed / Inferred / Unknown | The fix is local and touches no shared code, contract or data |
| 11 | Code Review | 8-10 | `pr-review-agent` (`/review`); `code-review` | Prioritized findings | The fix is trivial and the user declines review |
| 12 | PR Preparation | 11 | [pr-preparation](pr-preparation.md) | PR summary and reviewer notes | The user does not want a PR |
| 13 | PR Intelligence | 12, a PR exists | `pr-intelligence-agent` (`/pr-intelligence`) | Readiness: READY, NEEDS_CHANGES or NEEDS_INFORMATION | No PR exists or no `source-control` |

Findings from stages 10, 11 and 13 that require changes return to stage 8. Stage notes:

- **3 Reproduce.** Never claim reproduction unless it was performed and the output was seen. A code-reading explanation is static analysis.
- **5-7.** A hypothesis is not a cause. Only a validated hypothesis becomes the Confirmed Root Cause.
- **8 Minimal Fix.** No unrelated refactor, dependency or cleanup. Implementation needs PLAN_READY.

## Commands

| Command | Serves stage |
| --- | --- |
| [`/debug`](../commands/debug.md) | 3-7 |
| [`/test-plan`](../commands/test-plan.md) | 9 |
| [`/change-impact`](../commands/change-impact.md) | 10 |
| [`/review`](../commands/review.md) | 11 |
| [`/pr-intelligence`](../commands/pr-intelligence.md) | 13 |

## Agents

| Agent | Role | Stage | Used when |
| --- | --- | --- | --- |
| [bug-investigation-agent](../agents/bug-investigation-agent.md) | Primary | 3-7 | Always |
| [test-planning-agent](../agents/test-planning-agent.md) | Supporting | 9 | A regression test is designed |
| [change-intelligence-agent](../agents/change-intelligence-agent.md) | Supporting | 10 | The fix touches shared code, a contract or data |
| [pr-review-agent](../agents/pr-review-agent.md) | Supporting | 11 | Review is wanted |
| [pr-intelligence-agent](../agents/pr-intelligence-agent.md) | Supporting | 13 | A PR exists and `source-control` is available |

## Skills

Applied through the agents, or directly when no agent fits the stage.

- [`debugging`](../skills/debugging/SKILL.md), [`testing`](../skills/testing/SKILL.md), [`change-intelligence`](../skills/change-intelligence/SKILL.md), [`code-review`](../skills/code-review/SKILL.md): core.
- [`database-sql`](../skills/database-sql/SKILL.md), [`observability`](../skills/observability/SKILL.md), [`performance`](../skills/performance/SKILL.md), [`reliability`](../skills/reliability/SKILL.md), [`security`](../skills/security/SKILL.md): only when the symptom points there.

## Decision Points

| If | Then |
| --- | --- |
| Production is affected now | Stop and route to [production-incident](production-incident.md) |
| Report is insufficient | NEEDS_INFORMATION; stay in stage 1 and ask |
| Project Context missing or stale | Continue on repository evidence; conclusions from context are Inferred |
| Cannot reproduce | Record why; continue on static evidence, root cause stays unconfirmed until validated |
| Symptom involves data or queries | Add `database-sql`; use `database` read-only if connected, else static analysis and the database fallback sentence |
| Symptom is slowness or resource use | Add `performance` |
| Symptom involves auth, input or data exposure | Add `security` |
| Root cause not confirmed | Do not implement; report hypotheses and the next evidence needed |
| Fix needs a schema change | Route that part to [database-change](database-change.md); NEEDS_HUMAN_APPROVAL if destructive |
| Fix is local | Skip stage 10 |
| Tests fail | Return to stage 8 or report; the result cannot be READY |

## Validation

- **Stage:** each result feeds the next. A root cause needs validating evidence, not plausibility.
- **Final:** the regression test fails without the fix and passes with it (both executed), related tests and the build pass where applicable, review blockers are resolved. Final checks follow [Workflow Common Guidance](../../docs/workflow-common.md#9-final-validation).
- **Evidence:** output, diffs, logs. "Not run" is reported as such.
- **Rollback:** state how the fix is reverted.
- **Failures** are reported per [Workflow Common Guidance](../../docs/workflow-common.md#13-failure-reporting). Unavailable capabilities degrade to repository evidence; the regression test failing blocks READY.

## Safety

| Stage | Kind |
| --- | --- |
| 1-7, 10-11, 13 | Analysis and planning. Live reads are read-only. |
| 8 | Modification. Needs go-ahead after PLAN_READY and a confirmed root cause. |
| 9 | Modification (tests) and local test execution |
| 12 | Planning. Pushing or opening a PR needs explicit authorization. |

Mutating database, cloud, deployment or production actions are never performed by this workflow. Checkpoints and prohibitions are in [Workflow Common Guidance](../../docs/workflow-common.md#12-human-checkpoints-and-safety).

## Output

The report uses the [common output contract](../../docs/workflow-common.md#10-output-contract) (Objective through Recommendation) and the [workflow states](../../docs/workflow-common.md#11-workflow-states). Findings state the root cause as Confirmed Root Cause or Hypothesis, and reproduction as performed or not performed. The workflow is reported COMPLETED only when its required stages completed; otherwise it states what is pending.

## Handoff

- To [pr-preparation](pr-preparation.md) and [pr-intelligence](pr-intelligence.md) with the fix summary, root cause, test evidence and review outcome.
- To [database-change](database-change.md) or [api-change](api-change.md) when the fix needs a schema or contract change.
- To [production-incident](production-incident.md) if production impact appears.
- To the user, with the open questions, when blocked.

## Examples

**Request:** "`GET /orders` returns 500 for customers with no address; here is the stack trace."

Stages 1-7 using the trace (stage 4 skipped if sufficient), 8, 9, 10 skipped if local, 11. Reproduction is reported as performed only if it was run.

**Request:** "Totals are sometimes off by one cent."

Stages 1-9 with `database-sql` and `performance` not needed; `database` used read-only if connected. Root cause stays a Hypothesis until validated.

## Related Workflows

- [production-incident](production-incident.md): when production is affected.
- [database-change](database-change.md), [api-change](api-change.md): when the fix changes a schema or contract.
- [pr-preparation](pr-preparation.md), [pr-intelligence](pr-intelligence.md): the usual next workflows.
