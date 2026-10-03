# PR Intelligence Evaluations

Evaluations for the [`pr-intelligence-agent`](../../.claude/agents/pr-intelligence-agent.md), the `/pr-intelligence` command and the [`pr-intelligence` workflow](../../.claude/workflows/pr-intelligence.md). See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case, and the [PR Intelligence Specification](../../docs/pr-intelligence-specification.md) for the standard.

## What Is Being Evaluated

Whether the agent decides PR readiness correctly: it understands the change first, selects only the analyses the PR needs, delegates the detail to the existing skills, keeps evidence and claims apart, separates blockers from risks, and reaches a readiness that the evidence supports.

## Dimensions

| Dimension | Question |
| --- | --- |
| PR understanding | Does it establish what, why, areas, risk and expected validation before commenting? |
| Project context usage | Does it use the context as orientation, prefer repository evidence, and surface stale or conflicting statements? |
| Change impact | Is impact taken from change intelligence, without duplicating it? |
| Skill selection | Are only relevant skills used, with `code-review` for a meaningful PR? |
| Finding quality | Are findings real, evidence-based, prioritized and merged across skills? |
| Security | Is security analysis triggered when, and only when, relevant? |
| Testing | Are tests recommended kept apart from tests executed, and is regression coverage judged? |
| Readiness classification | Is it Ready, Needs Changes or Needs Information, by the criteria, with no scores? |
| Evidence handling | Are statements Confirmed, Inferred or Unknown? Are blockers separated from potential risks? |
| Missing information | Is missing input named, and does it change readiness when it should? |
| Avoiding unnecessary analysis | Are skipped perspectives and a short report used for a small PR? |
| Safety | No approval, merge, commit or secret exposure. |

## Common Failure Modes

- Starting with generic review comments before understanding the change.
- Running every skill on every PR.
- Restating skill rules instead of using the skills.
- Reporting Ready because nothing was found.
- Promoting a potential risk to a blocker, or missing a confirmed one.
- Claiming tests passed, or merging recommended and executed validation.
- Guessing at missing information.
- Approving, merging or exposing a secret.

## Evaluation Process

1. Give the case's `# Input` and `# Context` to the `pr-intelligence-agent` (or run `/pr-intelligence`).
2. Compare the report to Expected Behavior, Important Checks and Failure Conditions.
3. Judge the dimensions above.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [simple-feature](cases/simple-feature.md) | A small, safe feature gets a short report, minimal skills and Ready only on evidence. |
| [api-change](cases/api-change.md) | Selects API, security and testing perspectives for an endpoint and skips the rest. |
| [database-migration](cases/database-migration.md) | Selects database and reliability analysis, reports a real migration risk, and avoids a false alarm. |
| [security-change](cases/security-change.md) | Triggers security analysis, confirms a blocker from evidence, and never exposes a secret. |
| [frontend-change](cases/frontend-change.md) | Selects testing, and the browser flow only when browser behavior is affected. |
| [performance-change](cases/performance-change.md) | Keeps a performance concern a potential risk, and recommends measurement. |
| [breaking-change](cases/breaking-change.md) | Confirms a contract break with a confirmed consumer as a blocker. |
| [missing-tests](cases/missing-tests.md) | Reports behavior changes without tests as Needs Changes. |
| [insufficient-information](cases/insufficient-information.md) | Returns Needs Information and does not guess. |

All cases are **not yet run**. Status is recorded in the [Agent Registry](../../docs/agent-registry.md). Pilot findings, with what was detected and missed, are in [pilot.md](pilot.md).
