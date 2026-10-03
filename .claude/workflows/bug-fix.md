---
name: bug-fix
description: Take a reported defect from symptom to a validated minimal fix with a regression test, establishing a supported root cause before changing code. Use for non-urgent bugs; not for active production incidents or new features.
---

# Bug Fix Workflow

## Purpose

Resolve a defect by moving from symptom to evidence to a confirmed root cause, then to a minimal fix proven by a regression test. The workflow orchestrates existing agents and skills and enforces one ordering rule: the symptom is not fixed before the cause is sufficiently supported.

## When to Use

- An error, failing test, wrong result or unexpected behavior needs to be fixed.
- The cause is unknown or not yet confirmed.
- The engineer wants the fix to include a regression test and review.

## When NOT to Use

- Production is degraded now. Use [production-incident](production-incident.md).
- The cause is already known and the change is a planned edit. Use [feature-development](feature-development.md) or make the edit directly.
- The problem is a new requirement rather than a defect.
- The problem is a slow query or database behavior only. Consider [database-change](database-change.md) after investigation.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Symptom: what was expected, what happened | Required | |
| Error messages, stack traces, logs | Preferred | Used as given. |
| Reproduction steps, environment, version | Preferred | |
| Recent changes | Optional | |
| Constraints: scope, no-touch areas, deadlines | Optional | Carried unchanged into every stage. |

Missing evidence is listed, not invented.

## Stages

Each stage follows the lifecycle in the [Workflow Specification](../../docs/workflow-specification.md).

| # | Stage | Needs | Performed by | Produces | Skip when |
| --- | --- | --- | --- | --- | --- |
| 1 | Capture Symptom | | Workflow (asks the user) | Expected vs actual behavior, impact, constraints | Never |
| 2 | Reproduce / Understand | 1 | `bug-investigation-agent` (`/debug`) | Reproduction, or a statement that it cannot be reproduced and why | The failure is fully explained by a provided trace |
| 3 | Gather Evidence | 1, 2 | `bug-investigation-agent`; `observability` if logs or traces are needed | Labeled evidence: observed, assumed, missing | Evidence was supplied and is sufficient |
| 4 | Investigate | 3 | `bug-investigation-agent` | Hypotheses with support and ways to test them | Never |
| 5 | Confirm Root Cause | 4 | `bug-investigation-agent` | Confirmed cause, or "root cause not yet confirmed" | Never |
| 6 | Plan Minimal Fix | 5 | Workflow with the investigation result | Smallest change that addresses the cause, risks, side effects | Never |
| 7 | Implement Fix | 6 | The engineer or the AI, with go-ahead | Working-tree change | Blocked until stage 5 is confirmed, unless stabilization applies |
| 8 | Regression Test | 5, 7 | `test-planning-agent` (`/test-plan`); `testing` skill | A test that fails without the fix and passes with it | A test is genuinely impractical; say why and give manual verification |
| 9 | Review | 7, 8 | `pr-review-agent` (`/review`) | Review findings | The fix is trivial and the user declines review |
| 10 | Validate | 7-9 | Workflow; test execution | Evidence the symptom is gone and nothing regressed | Never |

## Commands

| Command | Serves stage |
| --- | --- |
| [`/debug`](../commands/debug.md) | 2-5 |
| [`/test-plan`](../commands/test-plan.md) | 8 |
| [`/review`](../commands/review.md) | 9 |

## Agents

| Agent | Role | Stage | Used when |
| --- | --- | --- | --- |
| [bug-investigation-agent](../agents/bug-investigation-agent.md) | Primary | 2-5 | Always |
| [test-planning-agent](../agents/test-planning-agent.md) | Supporting | 8 | A regression test is planned |
| [pr-review-agent](../agents/pr-review-agent.md) | Supporting | 9 | The fix is reviewed |

## Skills

Applied through the agents above. None is required by the workflow itself.

- [`debugging`](../skills/debugging/SKILL.md): through the primary agent.
- [`testing`](../skills/testing/SKILL.md): regression test.
- [`observability`](../skills/observability/SKILL.md), [`database-sql`](../skills/database-sql/SKILL.md), [`performance`](../skills/performance/SKILL.md), [`security`](../skills/security/SKILL.md): only when the evidence points to them.
- [`playwright`](../skills/playwright/SKILL.md): when the defect is in a browser flow.

## Decision Points

| If | Then |
| --- | --- |
| The symptom cannot be reproduced | Continue with available evidence, label the result accordingly, and ask for more |
| Root cause is not confirmed | Do not proceed to stage 7. Return to stage 3 or report "not yet confirmed" |
| Production is impacted and stabilization is needed | Switch to [production-incident](production-incident.md), or apply a reversible stabilizing step with authorization, and resume at stage 5 afterward |
| The cause is in SQL or schema | Route the database part to [database-change](database-change.md) |
| The defect is in a public API contract | Route to [api-change](api-change.md) |
| The defect is security-relevant | Apply `security` to stages 5 and 9 |
| The fix needs a larger redesign | Record the minimal fix and hand off the redesign to `architecture-agent` separately |

## Validation

- **Stage validation:** stage 5 is passed only when the stated cause explains the symptom and is supported by evidence beyond correlation.
- **Final validation:** the regression test fails before and passes after the fix, where that could be shown; relevant existing tests pass; the original symptom is not reproducible.
- **Evidence:** test output, logs, reproduction results. Anything not run is reported as "not run."
- **Rollback:** state how the fix can be reverted. Call out fixes that change data or persisted state.

## Safety

| Stage | Kind |
| --- | --- |
| 1-6, 9 | Analysis and planning |
| 7 | Modification. Only after root cause is supported and the user asks for the fix. |
| 8, 10 | Modification (tests) and local execution |

- No fix is applied to the symptom before a sufficiently supported root cause, unless immediate stabilization is required and authorized.
- Data corrections, production commands, migrations and deployments need explicit authorization.
- Do not delete data, files or tests to make a symptom disappear.
- Do not weaken or skip existing tests to get a green result.

## Output

A bug-fix report: symptom, evidence, root cause (confirmed or not), the fix and why it is minimal, regression test and its results, review findings, remaining risk, and stages skipped with reasons. Reported **complete** only when required stages completed. If the cause was not confirmed, the workflow reports that and does not present a fix as resolved.

## Handoff

- To [pr-preparation](pr-preparation.md) with the fix summary and test evidence.
- To `architecture-agent` when the fix exposes a design problem.
- To [production-incident](production-incident.md) if the defect proves to be live production impact.

## Examples

**Request:** "`POST /orders` returns 500 for some customers. Stack trace attached."

Stages 1, 3-5 using the stack trace. Stage 2 is skipped because the trace explains the failure path. The cause is a null `ShippingAddress`. Stages 6-10 follow, with a regression test for the null case.

**Request:** "The nightly job sometimes doesn't finish."

Stage 2 cannot reproduce it. The workflow continues with logs, labels the cause "not yet confirmed," and stops before stage 7 asking for the missing evidence.

## Related Workflows

- [production-incident](production-incident.md): when impact is live.
- [feature-development](feature-development.md), [pr-preparation](pr-preparation.md).
- [database-change](database-change.md), [api-change](api-change.md): when the fix lands there.
